import unittest
import calendar
from datetime import datetime, timedelta, date

from codenotes import parse_args
from codenotes.util.args import date_args_empty, dates_to_search, add_note_args_empty, add_task_args_empty


class TestDateArgsNeededEmpty(unittest.TestCase):

    def test_no_args(self):
        args = parse_args(['search', 'task'])

        self.assertTrue(date_args_empty(args))

    def test_only_date(self):
        args = parse_args(['search', 'task', '--today'])

        self.assertFalse(date_args_empty(args))

    def test_only_text(self):
        args = parse_args(['search', 'task', 'New', 'task', 'added'])

        self.assertFalse(date_args_empty(args))

    def test_text_and_date(self):
        args = parse_args(['search', 'task', 'New', 'task', 'added', '--today'])

        self.assertFalse(date_args_empty(args))


class TestAddTaskArgsEmpty(unittest.TestCase):
    
    def test_args_both(self):
        args = parse_args(['add', 'task', 'New task', '--new-category', 'Sample', 'Category'])
        self.assertFalse(add_task_args_empty(args))

    def test_args_one(self):
        args = parse_args(['add', 'task', 'New task'])
        self.assertFalse(add_task_args_empty(args))

        args = parse_args(['add', 'task', '--new-category', 'Sample', 'Category'])
        self.assertFalse(add_task_args_empty(args))

    def test_args_none(self):
        args = parse_args(['add', 'task'])
        self.assertTrue(add_task_args_empty(args))


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


class TestAddNoteArgsEmpty(unittest.TestCase):

    def test_args_three(self):
        args = parse_args(['add', 'note', 'New', 'note', '-t', 'Sample', 'title', '--new-category', 'Category'])
        self.assertFalse(add_note_args_empty(args))

    def test_args_one(self):
        args = parse_args(['add', 'note', 'New', 'note'])
        self.assertFalse(add_note_args_empty(args))

        args = parse_args(['add', 'note', '--new-category', 'Category'])
        self.assertFalse(add_note_args_empty(args))

        args = parse_args(['add', 'note', '-t', 'Title'])
        self.assertFalse(add_note_args_empty(args))

    def test_args_none(self):
        args = parse_args(['add', 'note'])
        self.assertTrue(add_note_args_empty(args))


if __name__ == "__main__":
    unittest.main()
