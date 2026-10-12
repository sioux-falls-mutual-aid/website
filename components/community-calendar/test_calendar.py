"""Behavior checks for the community calendar build (stdlib only)."""
from datetime import date
from html.parser import HTMLParser
import json
import unittest
from unittest.mock import patch
import build

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles = []
        self.static_links = 0
        self.fields = set()
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "article" and "event-card" in values.get("class", ""):
            self.articles.append(values)
        if tag == "a" and values.get("href", "").startswith("https://"):
            self.static_links += 1
        if tag in {"select", "input"} and "id" in values:
            self.fields.add(values["id"])
        if tag == "script":
            self.scripts.append(values)

class CalendarTests(unittest.TestCase):
    def test_preview_has_sourced_events_and_static_html(self):
        html = build.render(date(2026, 10, 11), preview=True)
        tree = CalendarParser()
        tree.feed(html)
        self.assertEqual(6, len(tree.articles))
        self.assertGreaterEqual(tree.static_links, 6)
        self.assertTrue({"filter-area", "filter-category", "filter-range", "filter-free"} <= tree.fields)
        self.assertIn('id="event-health-connect-festival-2026"', html)
        self.assertIn('id="event-vermillion-library-board-2026-10-21"', html)
        self.assertIn('id="event-helpline-family-volunteer-day-2026"', html)
        self.assertIn('id="event-filters" action="" method="get" hidden', html)
        self.assertEqual([{"src":"calendar.js", "defer":None}], tree.scripts)

    def test_expired_events_are_excluded_at_build_time(self):
        html = build.render(date(2026, 11, 1), preview=True)
        self.assertNotIn('id="event-health-connect-festival-2026"', html)
        self.assertNotIn('id="event-prism-halloween-homecoming-2026"', html)
        self.assertIn('id="event-helpline-family-volunteer-day-2026"', html)

    def test_public_render_requires_editorial_copy(self):
        with self.assertRaisesRegex(ValueError, "Editorial copy"):
            build.render(date(2026, 10, 11))

    def test_preview_does_not_include_rejected(self):
        orgs = build.load_json('organizers.json')
        events = build.load_json('events.json')
        events[0]['review_status'] = 'rejected'
        original_load = build.load_json
        with patch.object(build, 'load_json', side_effect=lambda name: events if name == 'events.json' else original_load(name)):
            html = build.render(date(2026, 10, 11), preview=True)
        self.assertNotIn('id="event-health-connect-festival-2026"', html)

    def test_public_only_approved_after_copy_review(self):
        events = build.load_json('events.json')
        events[0]['review_status'] = 'approved'
        copy = {k: v.replace('[WRITE:', 'Label:') for k,v in build.load_json('copy.json').items()}
        original_load = build.load_json
        with patch.object(build, 'load_json', side_effect=lambda name: events if name == 'events.json' else copy if name == 'copy.json' else original_load(name)):
            html = build.render(date(2026, 10, 11))
        p = CalendarParser();p.feed(html)
        self.assertEqual(1, len(p.articles))
        self.assertIn('id="event-health-connect-festival-2026"', html)
        self.assertNotIn('id="event-vermillion-library-board-2026-10-21"', html)

    def test_event_title_and_url_are_safely_escaped(self):
        orgs = build.load_json('organizers.json')
        events = build.load_json('events.json')
        events[0]['title'] = '<img src=x onerror=alert(1)>'
        copy = build.load_json('copy.json')
        html = build.card(events[0], orgs[0], copy)
        self.assertNotIn('<img', html)
        self.assertIn('&lt;img', html)
        events[0]['source_url'] = 'javascript:alert(1)'
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            build.validate(orgs, events, copy)

    def test_accessibility_structure_no_dependency_on_js(self):
        html = build.render(date(2026,10,11), preview=True)
        self.assertIn('<main class="calendar-shell"',html)
        self.assertIn('<h1>',html)
        self.assertIn('<h2 id="events-heading">',html)
        self.assertIn('aria-live="polite"',html)
        self.assertIn('href="https://www.healthconnectsd.org/festival"',html)
        self.assertIn('hidden>',html)

if __name__ == '__main__':
    unittest.main()
