import unittest
import calendar
from datetime import datetime, timedelta, date

from codenotes.console import args_needed_empty, dates_to_search
from codenotes import parse_args


class TestArgsNeededEmpty(unittest.TestCase):

    def test_no_args(self):
        args = parse_args(['search', 'task'])

        self.assertTrue(args_needed_empty(args))

    def test_only_date(self):
        args = parse_args(['search', 'task', '--today'])

        self.assertFalse(args_needed_empty(args))

    def test_only_text(self):
        args = parse_args(['search', 'task', 'New', 'task', 'added'])

        self.assertFalse(args_needed_empty(args))

    def test_text_and_date(self):
        args = parse_args(['search', 'task', 'New', 'task', 'added', '--today'])

        self.assertFalse(args_needed_empty(args))


class TestDateToSearch(unittest.TestCase):

    def test_today(self):
        search_date = datetime.now().date()
        args = parse_args(['search', 'task', '--today'])

        self.assertEqual(dates_to_search(args), search_date)

    def test_yesterday(self):
        search_date = datetime.now().date() - timedelta(days=1)
        args = parse_args(['search', 'task', '--yesterday'])

        self.assertEqual(dates_to_search(args), search_date)

    def test_month(self):
        now = datetime.now()
        num_days = calendar.monthrange(now.year, now.month)[1]
        days = [
            date(now.year, now.month, 1),
            date(now.year, now.month, num_days)
        ]

        args = parse_args(['search', 'task', '--month'])

        self.assertListEqual(dates_to_search(args), days)

    def test_week(self):
        now = datetime.now().date()
        first_day = now - timedelta(days=now.weekday())
        last_day = first_day + timedelta(days=6)
        days = [first_day, last_day]

        args = parse_args(['search', 'task', '--week'])

        self.assertListEqual(dates_to_search(args), days)

if __name__ == "__main__":
    unittest.main()
