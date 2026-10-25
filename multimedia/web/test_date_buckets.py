"""Spec 132 — the Tata Ibadah list's date buckets.

The rule is pure: a service date and the present day in, one bucket key out. The
present day is passed in rather than read here, so these tests never touch the
clock.
"""

from datetime import date, timedelta

from django.test import SimpleTestCase

from multimedia.web.reading import date_buckets


class DateBucketRuleTests(SimpleTestCase):
    today = date(2026, 10, 25)

    def key(self, day, today=None):
        return date_buckets.bucket_key(day, today or self.today)

    def test_today_and_the_future_are_upcoming(self):
        self.assertEqual(self.key(self.today), 'upcoming')
        self.assertEqual(self.key(self.today + timedelta(days=1)), 'upcoming')
        self.assertEqual(self.key(date(2027, 3, 1)), 'upcoming')

    def test_the_last_thirty_days_end_on_the_thirtieth_day(self):
        self.assertEqual(self.key(self.today - timedelta(days=1)), 'last-30-days')
        self.assertEqual(self.key(self.today - timedelta(days=30)), 'last-30-days')

    def test_thirty_one_days_back_in_the_same_year_is_earlier_this_year(self):
        self.assertEqual(self.key(self.today - timedelta(days=31)), 'earlier-this-year')

    def test_anything_older_is_older(self):
        self.assertEqual(self.key(date(2025, 12, 31)), 'older')
        self.assertEqual(self.key(self.today - timedelta(days=400)), 'older')

    def test_a_previous_year_inside_thirty_days_stays_recent(self):
        """Early January: December's services are recent, not "last year"."""
        today = date(2026, 1, 5)
        self.assertEqual(self.key(date(2025, 12, 20), today), 'last-30-days')
        self.assertEqual(self.key(date(2025, 11, 30), today), 'older')

    def test_the_rule_is_the_same_whichever_day_it_is_read(self):
        leap_eve = date(2028, 2, 29)
        self.assertEqual(self.key(leap_eve, leap_eve), 'upcoming')
        self.assertEqual(self.key(date(2028, 1, 30), leap_eve), 'last-30-days')
        self.assertEqual(self.key(date(2028, 1, 29), leap_eve), 'earlier-this-year')
