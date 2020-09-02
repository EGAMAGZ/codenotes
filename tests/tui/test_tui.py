import unittest

from codenotes.db.utilities import Category
from codenotes.tui import AddTaskTUI, ImpPyCUI, SearchTaskTUI


class TestAddTaskTUI(unittest.TestCase):

    def setUp(self) -> None:
        self.root = ImpPyCUI(5, 4)
        self.add_task_tui = AddTaskTUI(self.root)


class TestDefaultCategory(TestAddTaskTUI):

    def test_add_task(self):
        expected_categories = [
            'TODO Task #1'
        ]

        self.add_task_tui.task_text_block.set_text('TODO Task #1')
        self.add_task_tui.add_task()
        print(self.add_task_tui.tasks_list_menu.get_item_list())

        self.assertCountEqual(self.add_task_tui.tasks_list_menu.get_item_list(), expected_categories)
        self.assertEqual(self.add_task_tui.task_text_block.get(), '')

        self.add_task_tui.selected_category = Category(1, 'TODO Tasks')
        self.add_task_tui.save_tasks()

    def test_initial_categories(self):
        self.assertEqual(self.add_task_tui.selected_category, None)

        expected_categories = [
            (1, 'TODO Tasks')
        ]
        categories_list = self.add_task_tui.get_categories()
        self.assertCountEqual(categories_list, expected_categories)

        expected_categories_menu = [
            Category(1, 'TODO Tasks')
        ]
        self.add_task_tui._load_menu_categories()
        self.assertCountEqual(self.add_task_tui.categories_list, expected_categories_menu)

    def test_save_tasks(self):
        # ! EVERYTIME A TEST IS EXECUTED, THE SETUP METHOD IS ALSO EXECUTED
        expected_tasks_added = [
            'TODO Task #2',
            'TODO Task #3'
        ]
        self.add_task_tui.tasks_list_menu.add_item('TODO Task #2')
        self.add_task_tui.tasks_list_menu.add_item('TODO Task #3')

        self.assertCountEqual(self.add_task_tui.tasks_list_menu.get_item_list(), expected_tasks_added)

        self.add_task_tui.selected_category = Category(1, 'TODO Tasks')
        self.add_task_tui.save_tasks()


class TestNewCategory(TestAddTaskTUI):

    def test_add_new_category(self):
        self.add_task_tui.add_category('Custom Category')

        expected_categories = [
            (1, 'TODO Tasks'),
            (2, 'Custom Category')
        ]
        categories_list = self.add_task_tui.get_categories()
        self.assertCountEqual(categories_list, expected_categories)

        expected_categories_menu = [
            Category(1, 'TODO Tasks'),
            Category(2, 'Custom Category')
        ]
        self.add_task_tui._load_menu_categories()
        self.assertCountEqual(self.add_task_tui.categories_list, expected_categories_menu)

    def test_add_task(self):
        expected_categories = [
            'Custom Task #1'
        ]

        self.add_task_tui.task_text_block.set_text('Custom Task #1')
        self.add_task_tui.add_task()

        self.assertCountEqual(self.add_task_tui.tasks_list_menu.get_item_list(), expected_categories)
        self.assertEqual(self.add_task_tui.task_text_block.get(), '')

        self.add_task_tui.selected_category = Category(2, 'Custom Category')
        self.add_task_tui.save_tasks()

    def test_initial_categories(self):
        self.assertEqual(self.add_task_tui.selected_category, None)

        expected_categories = [
            (1, 'TODO Tasks'),
            (2, 'Custom Category')
        ]
        categories_list = self.add_task_tui.get_categories()
        self.assertCountEqual(categories_list, expected_categories)

        expected_categories_menu = [
            Category(1, 'TODO Tasks'),
            Category(2, 'Custom Category')
        ]
        self.add_task_tui._load_menu_categories()
        self.assertCountEqual(self.add_task_tui.categories_list, expected_categories_menu)

    def test_save_tasks(self):
        expected_tasks_added = [
            'Custom Task #2',
            'Custom Task #3'
        ]

        self.add_task_tui.tasks_list_menu.add_item('Custom Task #2')
        self.add_task_tui.tasks_list_menu.add_item('Custom Task #3')

        self.assertCountEqual(self.add_task_tui.tasks_list_menu.get_item_list(), expected_tasks_added)

        self.add_task_tui.selected_category = Category(2, 'Custom Category')
        self.add_task_tui.save_tasks()

class TestSearchTaskTUI(unittest.TestCase):

    def setUp(self) -> None:
        self.root = ImpPyCUI(6, 6)
        self.search_task_tui = SearchTaskTUI.set_root(self.root)

    def test_initial_values(self):
        self.assertEqual(self.search_task_tui.selected_category, None)
        self.assertEqual(self.search_task_tui.selected_date, None)
        self.assertEqual(self.search_task_tui.selected_status, None)
        self.assertEqual(self.search_task_tui.task_search_text_box.get(), '')

    def test_search_all_tasks(self):
        pass

    def tearDown(self) -> None:
        del self.root
        del self.search_task_tui
