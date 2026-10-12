"""Import public GitHub issue forms as review-stage event records; approve after manual checks."""
from __future__ import annotations

import argparse
from datetime import date, datetime, time, timedelta
import json
import re
from pathlib import Path
from zoneinfo import ZoneInfo

from build import HERE, CATEGORIES, safe_url, validate, load_json

FIELDS = {
    "Event name": "title",
    "Public event source URL": "source_url",
    "Organizer name": "organizer_name",
    "Community": "community",
    "Date (YYYY-MM-DD)": "day",
    "Start time (HH:MM, 24-hour local time; leave blank if unknown)": "start",
    "End time (HH:MM, 24-hour local time; leave blank if unknown)": "end",
    "Public venue or location": "venue",
    "Event type": "category",
    "Cost": "cost",
    "Possible mutual aid highlight": "candidate",
    "Public attendance or eligibility restriction (optional)": "audience",
}

ISSUE_HEADER = re.compile(r"^### (.+?)\s*$", re.MULTILINE)
ID_RE = re.compile(r"[^a-z0-9]+")
TZ = ZoneInfo("America/Chicago")


def read_issue(body: str) -> dict:
    headings = list(ISSUE_HEADER.finditer(body))
    if not headings:
        raise ValueError("Expected a GitHub issue form with ### headings")
    fields = {}
    for i, match in enumerate(headings):
        raw = body[match.end():headings[i+1].start() if i+1 < len(headings) else len(body)]
        fields[match.group(1)] = raw.strip()
    result = {}
    for heading, field in FIELDS.items():
        if heading not in fields:
            raise ValueError(f"Missing issue field: {heading}")
        content = fields[heading].strip()
        if content == "_No response_":
            content = ""
        result[field] = content
    return result


def timestamp(day: date, text: str, label: str):
    try:
        parsed = time.fromisoformat(text)
    except ValueError:
        raise ValueError(f"{label} needs HH:MM in 24-hour local time") from None
    if parsed.second or parsed.microsecond or len(text) != 5:
        raise ValueError(f"{label} needs HH:MM in 24-hour local time")
    dt = datetime.combine(day, parsed, tzinfo=TZ)
    if dt.replace(fold=0).utcoffset() != dt.replace(fold=1).utcoffset():
        raise ValueError("Ambiguous or nonexistent local time during daylight saving transition")
    if dt.astimezone(ZoneInfo('UTC')).astimezone(TZ).replace(tzinfo=None) != dt.replace(tzinfo=None):
        raise ValueError("Nonexistent local time during daylight saving transition")
    return dt


def slug(value: str):
    result = ID_RE.sub("-", value.casefold()).strip("-")
    if not result:
        raise ValueError("Event title cannot produce an ID")
    return result[:65].rstrip('-')


def make_draft(fields: dict, organizers: list) -> dict:
    required = ("title", "source_url", "organizer_name", "community", "day", "venue", "category", "cost", "candidate")
    for field in required:
        if not fields[field]:
            raise ValueError(f"Field is required: {field}")
    safe_url(fields["source_url"])
    orgs = [org for org in organizers if org["name"].casefold() == fields["organizer_name"].casefold()]
    if len(orgs) != 1:
        raise ValueError("Organizer not in organizer directory; verify and add it first: " + fields["organizer_name"])
    day = date.fromisoformat(fields["day"])
    category = fields["category"].casefold()
    if category not in CATEGORIES:
        raise ValueError("Invalid event category")
    cost = fields["cost"].casefold()
    if cost not in {"free", "unknown"}:
        raise ValueError("Cost must be Free or Unknown until verified")
    candidate = fields["candidate"].casefold()
    if candidate not in {"yes", "no"}:
        raise ValueError("Mutual aid candidate must be Yes or No")
    event = {
        "id": f"{slug(fields['title'])}-{day.isoformat()}",
        "organizer_id": orgs[0]["id"],
        "title": fields["title"],
        "venue": fields["venue"],
        "community": fields["community"],
        "category": category,
        "cost": cost,
        "mutual_aid_candidate": candidate == "yes",
        "source_url": fields["source_url"],
        "review_status": "needs_review",
    }
    if fields["audience"]:
        event["audience"] = fields["audience"]
    start, end = fields["start"], fields["end"]
    if bool(start) != bool(end):
        raise ValueError("Either supply both times, or leave both blank")
    if start:
        first = timestamp(day, start, "Start time")
        last = timestamp(day, end, "End time")
        if last <= first:
            raise ValueError("End time must be after start time; multi-day events need manual handling")
        event["start"], event["end"] = first.isoformat(), last.isoformat()
    else:
        event["start_date"] = day.isoformat()
    return event


def register_organizer(organizers, name, website, events_url, community):
    for url in (website, events_url):
        safe_url(url)
    if not all(v.strip() for v in (name, community)):
        raise ValueError("Organizer name and community are required")
    org_id = slug(name)
    if any(o["id"] == org_id or o["name"].casefold() == name.casefold() for o in organizers):
        raise ValueError("Organizer already exists")
    organizer = {
        "id": org_id,
        "name": name.strip(),
        "website": website,
        "events_url": events_url,
        "facebook_url": None,
        "base_community": community.strip(),
        "research_status": "needs_review",
    }
    return organizers + [organizer], organizer


def write_json(path, content):
    # Only write after all records validate; use atomic replacement to avoid corrupting source.
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding='utf-8')
    temp.replace(path)


def ingest_issue(issue_text, events, organizers, copy):
    draft = make_draft(read_issue(issue_text), organizers)
    if any(e["id"] == draft["id"] for e in events):
        raise ValueError("Event already exists with this ID: " + draft["id"])
    proposed = events + [draft]
    validate(organizers, proposed, copy)
    return proposed, draft


def review_event(events, organizers, copy, event_id, status, verified_on=None, feature=False):
    updated = [dict(e) for e in events]
    matches = [e for e in updated if e["id"] == event_id]
    if len(matches) != 1:
        raise ValueError("Unknown event ID: " + event_id)
    event = matches[0]
    if status == "approved":
        if feature and not event["mutual_aid_candidate"]:
            raise ValueError("An event must be a candidate before it can be featured")
        if verified_on is None:
            raise ValueError("Approval requires --verified-on YYYY-MM-DD after checking the official source")
        day = date.fromisoformat(verified_on)
        if day > datetime.now(TZ).date():
            raise ValueError("Verification date cannot be in the future")
        event["source_checked_date"] = day.isoformat()
        event["feature_approved"] = feature
    else:
        event["feature_approved"] = False
    event["review_status"] = status
    validate(organizers, updated, copy)
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    command = parser.add_subparsers(dest="command", required=True)
    inc = command.add_parser("import-issue", help="Import a public GitHub issue-form body as a draft")
    inc.add_argument("issue_file", type=Path)
    review = command.add_parser("review", help="Change status after a person verifies the event")
    review.add_argument("event_id")
    review.add_argument("status", choices=["needs_review", "approved", "rejected"])
    review.add_argument("--verified-on")
    review.add_argument("--feature", action="store_true", help="Explicitly approve mutual aid featuring")
    org = command.add_parser("add-organizer", help="Create a pending organizer directory record")
    org.add_argument("--name", required=True)
    org.add_argument("--website", required=True)
    org.add_argument("--events-url", required=True)
    org.add_argument("--community", required=True)
    command.add_parser("list", help="Show event IDs, dates, organizers and review state")
    args = parser.parse_args()
    events, organizers, copy = load_json("events.json"), load_json("organizers.json"), load_json("copy.json")
    if args.command == "list":
        for e in events:
            print(e["id"], e.get("start_date", e.get("start", "")[:10]), e["review_status"])
        return
    if args.command == "add-organizer":
        organizers, organizer = register_organizer(organizers, args.name, args.website, args.events_url, args.community)
        validate(organizers, events, copy)
        write_json(HERE / "organizers.json", organizers)
        print("Created organizer pending review:", organizer["id"])
    elif args.command == "import-issue":
        events, draft = ingest_issue(args.issue_file.read_text(encoding="utf-8"), events, organizers, copy)
        write_json(HERE / "events.json", events)
        print("Created review-stage event:", draft["id"])
    elif args.command == "review":
        events = review_event(events, organizers, copy, args.event_id, args.status, args.verified_on, args.feature)
        write_json(HERE / "events.json", events)
        print("Updated event:", args.event_id, args.status)


if __name__ == "__main__":
    main()
