# Community calendar: prototype implementation

**Development-only.** This folder is not wired to WordPress or deployed anywhere. It contains a static-first calendar renderer, a local organizer directory, and a small set of official-source event records awaiting editorial review.

## Local preview

From this folder:

```bash
python build.py --preview
python -m http.server 8000
```

Open `http://localhost:8000/prototype.html`. A local file preview also works. The generated HTML already contains event titles, dates, organizer names, locations and links, so visitors can read the calendar without JavaScript. JS adds filtering and hides events after their end timestamps pass. Regenerate the HTML regularly to expire entries for visitors without JavaScript.

The preview includes `needs_review` records; this is intentional for testing. It should **never be published as the public calendar**. Public rendering ignores all entries except `approved` and refuses to build until all copy placeholders in `copy.json` have been replaced by user-authored copy.

## Data ownership

- `organizers.json`: Public organizational information, with links to the official source and optional verified Facebook page URLs.
- `events.json`: Official-source event leads, review state, category, community, cost, and a `mutual_aid_candidate` curation flag. `needs_review` is the default; never mark an event `approved` without editorial approval.
- `copy.json`: Every reader-facing label and introductory phrase is a placeholder. The site owner writes and approves this copy.
- `build.py`: Validates source links, timezones, review states and IDs, escapes HTML and generates complete static markup.
- `calendar.js`: Progressive enhancement only. Uses the `America/Chicago` time zone to hide past events and filter the next 14 days, area, category and free events.
- `calendar.css`: Responsive styling and keyboard focus affordances; no third-party requests.

## Review gates

Before public release:

1. Confirm dates, locations and audience restrictions against official sources, including links and event status.
2. Record organizer verification and obtain the owner's editorial approval for each event.
3. Replace **all** `[WRITE: ...]` placeholders in `copy.json` with the owner's wording.
4. Change approved event statuses from `needs_review` to `approved`.
5. Build without `--preview`: `python build.py --require-copy --output public.html`.
6. Confirm WordPress embedding method and set up a recurring rebuild/publishing process; the code is not yet integrated with the live site.
7. Test real mobile devices, keyboard navigation, a screen reader, 320px and 375px widths, 200% zoom, high contrast, and JavaScript disabled.

## Tests

```bash
python -m unittest -v test_calendar.py
node --check calendar.js
# Optional browser checks when Playwright + Chromium are available:
python test_browser.py
```

No attendee data, private group information or contact details should be stored. The browser sends no requests to organizers' websites until a visitor clicks their links.
