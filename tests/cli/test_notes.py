import unittest
from datetime import datetime

from codenotes import parse_args
from codenotes.cli.notes import CreateNote, SearchNote
from codenotes.exceptions import CategoryNotExistsError


class TestCreateNote(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_note_text = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
            "incididunt ut labore et dolore magna aliqua."
        )

    def test_add_category_and_complete_note(self):
        args = parse_args(
            [
                "note", "create", "Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,",
                "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.",
                "--title", "Lorem", "ipsum", "Note", "--category", "CLI", "Category",
            ]
        )
        add_note = CreateNote(args)

        self.assertEqual(add_note.category_id, 2)
        self.assertEqual(add_note.category_name, "CLI Category")
        self.assertEqual(add_note.note_text, self.expected_note_text)
        self.assertEqual(add_note.note_title, "Lorem ipsum Note")

        args = parse_args(
            [
                "note", "create", "New", "Note", "in", "the", "same", "category", "--category", "CLI", "Category",
            ]
        )
        add_note = CreateNote(args)

        self.assertEqual(add_note.category_id, 2)
        self.assertEqual(add_note.category_name, "CLI Category")
        self.assertEqual(add_note.note_text, "New Note in the same category")
        self.assertEqual(add_note.note_title, "New Note in the same category")

    def test_add_note(self):
        args = parse_args(
            [
                "note", "create", "Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,","sed",
                "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.",
            ]
        )
        add_note = CreateNote(args)

        self.assertEqual(add_note.note_text, self.expected_note_text)
        self.assertEqual(add_note.note_title, "Lorem ipsum dolor sit amet, co")

    def test_add_title(self):
        args = parse_args(["note", "create", "--title", "Empty", "Note"])
        add_note = CreateNote(args)

        self.assertEqual(add_note.note_text, None)
        self.assertEqual(add_note.note_title, "Empty Note")

    def tearDown(self) -> None:
        del self.expected_note_text


class TestSearchNote(unittest.TestCase):
    def setUp(self) -> None:
        self.date = datetime.now().date().strftime("%Y-%m-%d")
        self.default_note_text = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
            "incididunt ut labore et dolore magna aliqua."
        )
        self.default_note_title = "Lorem ipsum Note"
        self.default_category = "General"

    def test_search_by_category(self):
        expected_notes = [
            (
                "Lorem ipsum dolor sit amet, co",
                self.default_note_text,
                self.default_category,
                0,
                self.date,
            ),
            ("Empty Note", None, self.default_category, 0, self.date),
        ]

        args = parse_args(
            ["note", "search", "--category", self.default_category, "--ever"]
        )
        query = SearchNote(args).query

        self.assertCountEqual(query, expected_notes)

    def test_search_ever(self):
        expected_notes = [
            (
                self.default_note_title,
                self.default_note_text,
                "CLI Category",
                0,
                self.date,
            ),
            (
                "Lorem ipsum dolor sit amet, co",
                self.default_note_text,
                self.default_category,
                0,
                self.date,
            ),
            ("Empty Note", None, self.default_category, 0, self.date),
            (
                "New Note in the same category",
                "New Note in the same category",
                "CLI Category",
                0,
                self.date,
            ),
        ]

        args = parse_args(["note", "search", "--ever"])
        query = SearchNote(args).query

        self.assertCountEqual(query, expected_notes)

    def test_search_month_note(self):
        expected_notes = [
            (
                self.default_note_title,
                self.default_note_text,
                "CLI Category",
                0,
                self.date,
            ),
            (
                "Lorem ipsum dolor sit amet, co",
                self.default_note_text,
                self.default_category,
                0,
                self.date,
            ),
            ("Empty Note", None, self.default_category, 0, self.date),
            (
                "New Note in the same category",
                "New Note in the same category",
                "CLI Category",
                0,
                self.date,
            ),
        ]

        args = parse_args(["note", "search", "--month"])
        query = SearchNote(args).query

        self.assertCountEqual(query, expected_notes)

    def test_search_text_date(self):
        expected_notes = [
            (
                self.default_note_title,
                self.default_note_text,
                "CLI Category",
                0,
                self.date,
            ),
            (
                "Lorem ipsum dolor sit amet, co",
                self.default_note_text,
                self.default_category,
                0,
                self.date,
            ),
        ]

        args = parse_args(["note", "search", "Lorem", "ipsum", "--today"])
        query = SearchNote(args).query

        self.assertCountEqual(query, expected_notes)

    def test_search_text_note(self):

        expected_notes = [
            (
                self.default_note_title,
                self.default_note_text,
                "CLI Category",
                0,
                self.date,
            ),
            (
                "Lorem ipsum dolor sit amet, co",
                self.default_note_text,
                self.default_category,
                0,
                self.date,
            ),
        ]

        args = parse_args(["note", "search", "Lorem", "ipsum"])
        query = SearchNote(args).query

        self.assertCountEqual(query, expected_notes)

    def test_search_today_note(self):
        expected_notes = [
            (
                self.default_note_title,
                self.default_note_text,
                "CLI Category",
                0,
                self.date,
            ),
            (
                "Lorem ipsum dolor sit amet, co",
                self.default_note_text,
                self.default_category,
                0,
                self.date,
            ),
            ("Empty Note", None, self.default_category, 0, self.date),
            (
                "New Note in the same category",
                "New Note in the same category",
                "CLI Category",
                0,
                self.date,
            ),
        ]

        args = parse_args(["note", "search", "--today"])
        query = SearchNote(args).query

        self.assertCountEqual(query, expected_notes)

    def test_search_yesterday_note(self):
        expected_notes = []

        args = parse_args(["note", "search", "--yesterday"])
        query = SearchNote(args).query

        self.assertCountEqual(query, expected_notes)

    def tearDown(self) -> None:
        del self.date
        del self.default_note_text
        del self.default_note_title
        del self.default_category


if __name__ == "__main__":
    unittest.main()
