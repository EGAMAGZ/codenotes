import unittest

from codenotes import parse_args
from codenotes.cli.notes import add_note_args_empty


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

    def test_add_category_and_complete_note(self):
        pass
    
    def test_add_note(self):
        pass

    def test_add_title(self):
        pass
