from datetime import datetime
import unittest

from codenotes import parse_args
from codenotes.cli.notes import AddNote, SearchNote


class TestAddNote(unittest.TestCase):

    def setUp(self) -> None:
        self.expected_note_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ' \
                                  'incididunt ut labore et dolore magna aliqua.'

    def test_add_category_and_complete_note(self):
        args = parse_args([
            'add', 'note', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing',
            'elit,', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
            'magna', 'aliqua.', '--title', 'Lorem', 'ipsum', 'Note', '--category', 'CLI', 'Category'
        ])
        add_note = AddNote(args)

        self.assertEqual(add_note.category_id, 2)
        self.assertEqual(add_note.category_name, 'CLI Category')
        self.assertEqual(add_note.note_text, self.expected_note_text)
        self.assertEqual(add_note.note_title, 'Lorem ipsum Note')

        args = parse_args([
            'add', 'note', 'New', 'Note', 'in', 'the', 'same', 'category', '--category', 'CLI', 'Category'
        ])
        add_note = AddNote(args)

        self.assertEqual(add_note.category_id, 2)
        self.assertEqual(add_note.category_name, 'CLI Category')
        self.assertEqual(add_note.note_text, 'New Note in the same category')
        self.assertEqual(add_note.note_title, 'New Note in the same category')
    
    def test_add_note(self):
        args = parse_args([
            'add', 'note', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing',
            'elit,', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
            'magna', 'aliqua.'
        ])
        add_note = AddNote(args)

        self.assertEqual(add_note.note_text, self.expected_note_text)
        self.assertEqual(add_note.note_title, 'Lorem ipsum dolor sit amet, co')

    def test_add_title(self):
        args = parse_args([
            'add', 'note', '--title', 'Empty', 'Note'
        ])
        add_note = AddNote(args) 

        self.assertEqual(add_note.note_text, None)
        self.assertEqual(add_note.note_title, 'Empty Note')

    def tearDown(self) -> None:
        del self.expected_note_text


class TestSearchNote(unittest.TestCase):
    
    def setUp(self) -> None:
        self.date = datetime.now().date().strftime('%Y-%m-%d')
        self.default_note_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ' \
                                  'incididunt ut labore et dolore magna aliqua.'
        self.default_note_title = 'Lorem ipsum Note'
        self.default_category = 'General'

    def test_search_month_note(self):
        expected_notes = [
            (self.default_note_title, self.default_note_text, 'CLI Category', 0, self.date),
            ('Lorem ipsum dolor sit amet, co', self.default_note_text, self.default_category, 0, self.date),
            ('Empty Note', None, self.default_category, 0, self.date),
            ('New Note in the same category', 'New Note in the same category','CLI Category', 0, self.date)
        ]

        args = parse_args(['search', 'note', '--month'])
        query = SearchNote(args).sql_query()

        self.assertCountEqual(query, expected_notes)

    def test_search_text_date(self):
        expected_notes = [
            (self.default_note_title, self.default_note_text, 'CLI Category', 0, self.date),
            ('Lorem ipsum dolor sit amet, co', self.default_note_text, self.default_category, 0, self.date)
        ]

        args = parse_args(['search', 'note', 'Lorem', 'ipsum', '--today'])
        query = SearchNote(args).sql_query()

        self.assertCountEqual(query, expected_notes)
    
    def test_search_text_note(self):
        
        expected_notes = [
            (self.default_note_title, self.default_note_text, 'CLI Category', 0, self.date),
            ('Lorem ipsum dolor sit amet, co', self.default_note_text, self.default_category, 0, self.date)
        ]

        args = parse_args(['search', 'note', 'Lorem', 'ipsum'])
        query = SearchNote(args).sql_query()

        self.assertCountEqual(query, expected_notes)

    def test_search_today_note(self):
        expected_notes = [
            (self.default_note_title, self.default_note_text, 'CLI Category', 0, self.date),
            ('Lorem ipsum dolor sit amet, co', self.default_note_text, self.default_category, 0, self.date),
            ('Empty Note', None, self.default_category, 0, self.date),
            ('New Note in the same category', 'New Note in the same category','CLI Category', 0, self.date)
        ]

        args = parse_args(['search', 'note', '--today'])
        query = SearchNote(args).sql_query()

        self.assertCountEqual(query, expected_notes)

    def test_search_yesterday_note(self):
        expected_notes = []

        args = parse_args(['search', 'note', '--yesterday'])
        query = SearchNote(args).sql_query()

        self.assertCountEqual(query, expected_notes)

    def tearDown(self) -> None:
        del self.date
        del self.default_note_text
        del self.default_note_title
        del self.default_category
