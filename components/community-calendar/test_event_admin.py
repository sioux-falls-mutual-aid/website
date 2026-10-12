"""Workflow checks: suggestions are drafts; only explicit review can publish or feature."""
from datetime import date
import unittest

import build
import event_admin


def form(**changes):
    values = {
        'Event name': 'Neighborhood resource swap',
        'Public event source URL': 'https://example.org/events/123',
        'Organizer name': 'The Transformation Project',
        'Community': 'Sioux Falls',
        'Date (YYYY-MM-DD)': '2026-10-25',
        'Start time (HH:MM, 24-hour local time; leave blank if unknown)': '13:00',
        'End time (HH:MM, 24-hour local time; leave blank if unknown)': '15:00',
        'Public venue or location': 'Prism Community Center',
        'Event type': 'Resources',
        'Cost': 'Free',
        'Possible mutual aid highlight': 'Yes',
        'Public attendance or eligibility restriction (optional)': '_No response_',
    }
    values.update(changes)
    return '\n\n'.join(f'### {name}\n\n{value}' for name, value in values.items())


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.events = build.load_json('events.json')
        self.organizers = build.load_json('organizers.json')
        self.copy = build.load_json('copy.json')

    def test_intake_creates_unverified_draft(self):
        after, event = event_admin.ingest_issue(form(), self.events, self.organizers, self.copy)
        self.assertEqual(len(self.events) + 1, len(after))
        self.assertEqual('needs_review', event['review_status'])
        self.assertNotIn('source_checked_date', event)
        self.assertEqual('2026-10-25T13:00:00-05:00', event['start'])
        self.assertTrue(event['mutual_aid_candidate'])
        self.assertNotIn('feature_approved', event)

    def test_duplicate_submission_does_not_create_another(self):
        after, _ = event_admin.ingest_issue(form(), self.events, self.organizers, self.copy)
        with self.assertRaisesRegex(ValueError, 'already exists'):
            event_admin.ingest_issue(form(), after, self.organizers, self.copy)

    def test_unknown_organizer_requires_directory_entry(self):
        with self.assertRaisesRegex(ValueError, 'Organizer not in organizer directory'):
            event_admin.ingest_issue(form(**{'Organizer name': 'Different Community Group'}), self.events, self.organizers, self.copy)

    def test_review_does_not_approve_automatically(self):
        events, draft = event_admin.ingest_issue(form(), self.events, self.organizers, self.copy)
        with self.assertRaisesRegex(ValueError, '--verified-on'):
            event_admin.review_event(events, self.organizers, self.copy, draft['id'], 'approved')
        self.assertEqual('needs_review', events[-1]['review_status'])
        reviewed = event_admin.review_event(events, self.organizers, self.copy, draft['id'], 'approved', verified_on='2026-10-12')
        self.assertEqual('approved', reviewed[-1]['review_status'])
        self.assertFalse(reviewed[-1]['feature_approved'])
        featured = event_admin.review_event(events, self.organizers, self.copy, draft['id'], 'approved', verified_on='2026-10-12', feature=True)
        self.assertTrue(featured[-1]['feature_approved'])
        no_feature = event_admin.review_event(featured, self.organizers, self.copy, draft['id'], 'rejected')
        self.assertFalse(no_feature[-1]['feature_approved'])

    def test_bad_links_times_and_incomplete_times_rejected(self):
        for changes in ({'Public event source URL': 'javascript:alert(1)'}, {'Start time (HH:MM, 24-hour local time; leave blank if unknown)': '12:45', 'End time (HH:MM, 24-hour local time; leave blank if unknown)': ''}, {'End time (HH:MM, 24-hour local time; leave blank if unknown)': '12:00'}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                event_admin.ingest_issue(form(**changes), self.events, self.organizers, self.copy)

    def test_organizer_creation_requires_public_sources(self):
        orgs, new = event_admin.register_organizer(self.organizers, 'Neighborhood Group', 'https://example.org', 'https://example.org/events', 'Yankton')
        self.assertEqual('needs_review', new['research_status'])
        self.assertEqual(len(self.organizers) + 1, len(orgs))
        with self.assertRaisesRegex(ValueError, 'already exists'):
            event_admin.register_organizer(orgs, 'Neighborhood Group', 'https://example.org', 'https://example.org/events', 'Yankton')

    def test_dst_invalid_hour_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Ambiguous or nonexistent'):
            event_admin.timestamp(date(2026,11,1), '01:30', 'Start time')
        with self.assertRaisesRegex(ValueError, 'Ambiguous or nonexistent'):
            event_admin.timestamp(date(2027,3,14), '02:30', 'Start time')

    def test_parse_markdown_natural_github_format(self):
        body = form() + '\n\n### Public-information check\n\n- [X] No private requests'
        fields = event_admin.read_issue(body)
        self.assertEqual('Resources', fields['category'])
        self.assertEqual('', fields['audience'])


if __name__ == '__main__':
    unittest.main()
