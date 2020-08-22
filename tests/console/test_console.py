from datetime import datetime, timedelta
import unittest

from codenotes.console import args_needed_empty, dates_to_search
from codenotes import parse_args


class TestArgsNeededEmpty(unittest.TestCase):

    def test_no_args(self):
        args = parse_args(['search', 'todo'])
        self.assertTrue(args_needed_empty(args))

    def test_only_date(self):
        args = parse_args(['search', 'todo', '--today'])
        self.assertFalse(args_needed_empty(args))

    def test_only_text(self):
        args = parse_args(['search', 'todo', 'New', 'task', 'added'])
        self.assertFalse(args_needed_empty(args))

    def test_text_and_date(self):
        args = parse_args(['search', 'todo', 'New', 'task', 'added', '--today'])
        self.assertFalse(args_needed_empty(args))


class TestDateToSearch(unittest.TestCase):

    def test_today(self):
        search_date = datetime.now().date()
        args = parse_args(['search', 'todo', 'New', 'task', 'added', '--today'])
        self.assertEqual(dates_to_search(args), search_date)

    def test_yesterday(self):
        search_date = datetime.now().date() - timedelta(days=1)
        args = parse_args(['search', 'todo', 'New', 'task', 'added', '--yesterday'])
        self.assertEqual(dates_to_search(args), search_date)


if __name__ == "__main__":
    unittest.main()
