# Event intake and review — implementation notes

The public directory is rendered from `events.json` and `organizers.json`, not from issue text. GitHub issues are **leads**, never automatically published.

## Intake (nontechnical contributor)

Create a new **Community event suggestion** issue using `.github/ISSUE_TEMPLATE/community-event.yml` when it is enabled on the feature branch or merged. Use a public organizer/event source link and public event details. Do not paste private-group posts or someone's assistance request into a public issue.

## Import (maintainer)

1. Check the event's source link. Locate the organizer in `organizers.json`.
2. If the organizer is missing, register a draft organizer first (its actual website and events page must be known):

   ```bash
   python event_admin.py add-organizer --name 'Organization' --website 'https://example.org' --events-url 'https://example.org/events' --community 'Vermillion'
   ```

3. Save the GitHub issue body as local `suggestion.md` and run:

   ```bash
   python event_admin.py import-issue suggestion.md
   ```

   This writes a new `needs_review` entry. It refuses duplicate IDs, unknown organizers, invalid URLs and dates, malformed or incomplete times, and daylight-saving ambiguity. It does not automatically publish anything.

## Review (editor)

After checking the event directly with the organizer/official source, confirm time, date, location, cost, audience, accessibility details, and whether the event should have a mutual aid highlight. Use the checked date, not the issue submission date:

```bash
python event_admin.py list
python event_admin.py review event-slug-2026-10-25 approved --verified-on 2026-10-12
# Feature separately, only with explicit editorial approval:
python event_admin.py review event-slug-2026-10-25 approved --verified-on 2026-10-12 --feature
# Or decline it:
python event_admin.py review event-slug-2026-10-25 rejected
```

An approved event still will not appear on the public calendar until the owner-authored copy placeholders in `copy.json` are replaced and the static calendar is rebuilt. Publication is a separate human-reviewed change.

## Builds and maintenance

```bash
python -m unittest -v test_calendar.py test_event_admin.py
python build.py --preview --as-of 2026-10-12
python test_browser.py
# After approved data and owner-authored copy are ready:
python build.py --require-copy --output public.html
```

No JavaScript: visitors can read all events that were current when the HTML was generated. JavaScript: past events hide themselves in the viewer's current session. **A scheduled static rebuild is still needed** to keep the no-JavaScript calendar current. No automated publishing is part of this prototype.

Do not mark an event verified based only on unverified Facebook comments or a secondary listing. Do not publish private meeting details, shelter addresses, attendee names, or private organizer contact information.
