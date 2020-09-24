import unittest

from codenotes.db.utilities import Category
from codenotes.tui import AddNoteTUI, ImpPyCUI


class TestAddNoteTUI(unittest.TestCase):

    def setUp(self) -> None:
        self.root = ImpPyCUI(5, 4)
        self.add_note_tui = AddNoteTUI(self.root)


class TestDefaultCategory(TestAddNoteTUI):

    def test_add_note(self):
        self.add_note_tui.note_content_text_block.set_text(
            'Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, ' \
            'extensive prebuilt components, and powerful JavaScript plugins.'
        )
        self.add_note_tui.selected_category = Category(1, 'General')
        self.add_note_tui.save_note()

        self.assertEqual(self.add_note_tui.note_title, 'Quickly design and customize r')

    def test_add_title(self):
        self.add_note_tui.note_title_text_box.set_text('Empty Bootstrap Note')
        self.add_note_tui.selected_category = Category(1, 'General')
        self.add_note_tui.save_note()

    def test_add_complete_note(self):
        self.add_note_tui.note_content_text_block.set_text(
            'Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, ' \
            'extensive prebuilt components, and powerful JavaScript plugins.'
        )
        self.add_note_tui.note_title_text_box.set_text('Bootstrap Note')
        self.add_note_tui.selected_category = Category(1, 'General')
        self.add_note_tui.save_note()

    def test_initial_Categories(self):
        self.assertEqual(self.add_note_tui.selected_category, None)

        expected_categories = [
            (1, 'General'),
            (2, 'CLI Category')
        ]

        categories_list = self.add_note_tui.get_categories()
        self.assertCountEqual(categories_list, expected_categories)

        expected_categories_menu = [
            Category(1, 'General'),
            Category(2, 'CLI Category')
        ]

        self.add_note_tui._load_categories_menu()
        self.assertCountEqual(self.add_note_tui.categories_list, expected_categories_menu)
