import calendar
import unittest
from datetime import date, datetime, timedelta

from codenotes import parse_args
from codenotes.util.args import date_args_empty, dates_to_search


class TestDateArgsNeededEmpty(unittest.TestCase):
    def test_no_args(self):
        args = parse_args(["task", "search"])

        self.assertTrue(date_args_empty(args))

    def test_only_date(self):
        args = parse_args(["task", "search", "--today"])

        self.assertFalse(date_args_empty(args))

    def test_only_text(self):
        args = parse_args(["task", "search", "New", "task", "added"])

        self.assertFalse(date_args_empty(args))

    def test_text_and_date(self):
        args = parse_args(["task", "search", "New", "task", "added", "--today"])

        self.assertFalse(date_args_empty(args))


class TestDateToSearch(unittest.TestCase):
    def test_today(self):
        search_date = datetime.now().date()
        args = parse_args(["task", "search", "--today"])

        self.assertEqual(dates_to_search(args), search_date)

    def test_yesterday(self):
        search_date = datetime.now().date() - timedelta(days=1)
        args = parse_args(["task", "search", "--yesterday"])

        self.assertEqual(dates_to_search(args), search_date)

    def test_month(self):
        now = datetime.now()
        num_days = calendar.monthrange(now.year, now.month)[1]
        days = [date(now.year, now.month, 1), date(now.year, now.month, num_days)]

        args = parse_args(["task", "search", "--month"])

        self.assertListEqual(dates_to_search(args), days)

    def test_week(self):
        now = datetime.now().date()
        first_day = now - timedelta(days=now.weekday())
        last_day = first_day + timedelta(days=6)
        days = [first_day, last_day]

        args = parse_args(["task", "search", "--week"])

        self.assertListEqual(dates_to_search(args), days)


if __name__ == "__main__":
    unittest.main()
