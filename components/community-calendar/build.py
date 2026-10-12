"""Render an accessible, static-first calendar from editorial copy and reviewed data."""
from __future__ import annotations

import argparse
from datetime import date, datetime
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
TOKEN = re.compile(r"{{([a-zA-Z0-9_.-]+)}}")
TZ = ZoneInfo("America/Chicago")
STATUS = {"needs_review", "approved", "rejected"}
CATEGORIES = {"resources", "civic", "arts", "community", "volunteer"}
COSTS = {"free", "unknown"}


def load_json(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def safe_url(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("External links must be public HTTPS URLs")
    return escape(url, quote=True)


def string(value):
    return escape(str(value), quote=True)


def event_datetime(event):
    if "start_date" in event:
        if "start" in event or "end" in event:
            raise ValueError("All-day events cannot also have start/end timestamps")
        day = date.fromisoformat(event["start_date"])
        return day, None, None
    start = datetime.fromisoformat(event["start"])
    if start.tzinfo is None:
        raise ValueError("Event timestamp must have an explicit timezone offset")
    start_local = start.astimezone(TZ)
    end = datetime.fromisoformat(event["end"])
    if end.tzinfo is None or end <= start:
        raise ValueError("Event end must be after start and timezone-aware")
    end_local = end.astimezone(TZ)
    if start_local.date() != end_local.date():
        raise ValueError("Multi-day timed events require explicit design review")
    return start_local.date(), start_local, end_local


def date_label(day):
    return f"{day:%a}, {day:%b} {day.day}, {day.year}"


def time_label(t):
    return t.strftime("%I:%M %p").lstrip("0")


def validate(organizers, events, copy):
    if not isinstance(organizers, list) or not isinstance(events, list):
        raise ValueError("Organizers and events must be arrays")
    if len({o["id"] for o in organizers}) != len(organizers):
        raise ValueError("Duplicate organizer ID")
    org_ids = {o["id"] for o in organizers}
    if len({e["id"] for e in events}) != len(events):
        raise ValueError("Duplicate event ID")
    for org in organizers:
        safe_url(org["website"])
        safe_url(org["events_url"])
        if org.get("facebook_url"):
            safe_url(org["facebook_url"])
    for event in events:
        if not re.fullmatch(r"[a-z0-9-]+", event["id"]):
            raise ValueError("Event ID must be a safe HTML fragment slug")
        if event["organizer_id"] not in org_ids:
            raise ValueError(f"Unknown organizer for {event['id']}")
        if event["category"] not in CATEGORIES:
            raise ValueError(f"Invalid category in {event['id']}")
        if event["cost"] not in COSTS:
            raise ValueError(f"Invalid cost in {event['id']}")
        if event["review_status"] not in STATUS:
            raise ValueError(f"Invalid review status in {event['id']}")
        date.fromisoformat(event["source_checked_date"])
        safe_url(event["source_url"])
        event_datetime(event)
    needed = set(TOKEN.findall((HERE / "prototype.template.html").read_text(encoding="utf-8")))
    computed = {"preview_banner", "featured_section", "area_options", "category_options", "event_cards", "no_results_hidden"}
    missing = needed - set(copy) - computed
    if missing:
        raise ValueError("Missing copy keys: " + ", ".join(sorted(missing)))


def card(event, organizer, copy):
    day, start, end = event_datetime(event)
    if start is None:
        when = f'<time datetime="{day.isoformat()}">{string(date_label(day))}</time>'
        end_iso = ""
    else:
        when = (f'<time datetime="{start.isoformat()}">{string(date_label(day))}</time>'
                f'<span class="time-range">{string(time_label(start))}–{string(time_label(end))}</span>')
        end_iso = end.isoformat()
    category = string(copy["category." + event["category"]])
    cost = string(copy["cost." + event["cost"]])
    audience = (f'<p class="event-audience">{string(copy["event.audience"])}: '
                f'{string(event["audience"])}</p>') if event.get("audience") else ""
    highlight = (f'<span class="highlight-tag">{string(copy["event.highlight"])}</span>'
                 if event["mutual_aid_candidate"] else "")
    return f'''<article class="event-card" id="event-{string(event['id'])}"
      data-area="{string(event['community'])}" data-category="{string(event['category'])}"
      data-cost="{string(event['cost'])}" data-day="{day.isoformat()}" data-end="{string(end_iso)}">
      <div class="card-main">
        <div class="event-meta">{when}{highlight}</div>
        <h3>{string(event['title'])}</h3>
        <p>{string(event['venue'])} · {string(event['community'])}</p>
        <p>{string(copy['event.organizer'])}: {string(organizer['name'])}</p>
        {audience}
        <p class="event-tags"><span>{category}</span><span>{cost}</span></p>
        <p><a href="{safe_url(event['source_url'])}" rel="noopener noreferrer">{string(copy['event.source_link'])}</a></p>
      </div>
    </article>'''


def render(as_of: date, preview=False, require_copy=False):
    copy = load_json("copy.json")
    organizers = load_json("organizers.json")
    events = load_json("events.json")
    validate(organizers, events, copy)
    if (require_copy or not preview) and any("[WRITE:" in value for value in copy.values()):
        raise ValueError("Editorial copy must be provided before public release")
    org_by_id = {o["id"]: o for o in organizers}
    eligible = []
    for e in events:
        day, _start, _end = event_datetime(e)
        if day < as_of:
            continue
        if not preview and e["review_status"] != "approved":
            continue
        if preview and e["review_status"] == "rejected":
            continue
        eligible.append(e)
    eligible.sort(key=lambda e: (event_datetime(e)[0], e.get("start", ""), e["title"].casefold()))
    cards = "\n".join(card(e, org_by_id[e["organizer_id"]], copy) for e in eligible)
    areas = sorted({e["community"] for e in eligible})
    categories = sorted({e["category"] for e in eligible})
    area_options = "".join(f'<option value="{string(a)}">{string(a)}</option>' for a in areas)
    category_options = "".join(f'<option value="{string(c)}">{string(copy["category." + c])}</option>' for c in categories)
    featured = [e for e in eligible if e["mutual_aid_candidate"]][:5]
    featured_section = ""
    if featured:
        links = "\n".join(
            f'<li data-feature-ref="event-{string(e["id"])}"><a href="#event-{string(e["id"])}">{string(e["title"])}</a></li>'
            for e in featured
        )
        featured_section = f'''<section class="featured" aria-labelledby="featured-heading" id="featured-section">
            <h2 id="featured-heading">{string(copy['featured.heading'])}</h2>
            <ul>{links}</ul>
        </section>'''
    values = {k: string(v) for k, v in copy.items()}
    values.update({
        "preview_banner": (f'<p class="preview-note">{string(copy["preview.notice"])}</p>' if preview else ""),
        "featured_section": featured_section,
        "area_options": area_options,
        "category_options": category_options,
        "event_cards": cards,
        "no_results_hidden": "hidden" if eligible else "",
    })
    template = (HERE / "prototype.template.html").read_text(encoding="utf-8")

    def substitute(match):
        key = match.group(1)
        if key not in values:
            raise ValueError(f"Missing template token: {key}")
        return values[key]

    output = TOKEN.sub(substitute, template)
    if TOKEN.search(output):
        raise ValueError("Unresolved template tokens")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", type=date.fromisoformat, default=datetime.now(TZ).date())
    parser.add_argument("--preview", action="store_true", help="Include needs_review event leads")
    parser.add_argument("--require-copy", action="store_true", help="Require finished user-authored copy")
    parser.add_argument("--output", default="prototype.html")
    args = parser.parse_args()
    target = HERE / args.output
    target.write_text(render(args.as_of, args.preview, args.require_copy), encoding="utf-8")
    print(f"Created {target.name}")


if __name__ == "__main__":
    main()
