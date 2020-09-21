import unittest

from codenotes import parse_args
from codenotes.cli.notes import AddNote, add_note_args_empty


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


class TestAddNote(unittest.TestCase):

    def setUp(self) -> None:
        self.expected_note_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ' \
                                  'incididunt ut labore et dolore magna aliqua.'

    def test_add_category_and_complete_note(self):
        args = parse_args([
            'add', 'note', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing',
            'elit,', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
            'magna', 'aliqua.', '--title', 'Lorem', 'ipsum', 'Note', '--new-category', 'CLI', 'Category'
        ])
        add_note = AddNote(args)

        self.assertEqual(add_note.category_id, 2)
        self.assertEqual(add_note.category_name, 'CLI Category')
        self.assertEqual(add_note.note_text, self.expected_note_text)
        self.assertEqual(add_note.note_title, 'Lorem ipsum Note')
    
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
