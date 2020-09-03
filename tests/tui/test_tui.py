from datetime import date, datetime
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
        self.maxDiff = None
        self.root = ImpPyCUI(6, 6)
        self.search_task_tui = SearchTaskTUI.set_root(self.root)
        self.current_date = datetime.now().date()

    def test_initial_values(self):
        self.assertEqual(self.search_task_tui.selected_category, None)
        self.assertEqual(self.search_task_tui.selected_date, None)
        self.assertEqual(self.search_task_tui.selected_status, None)
        self.assertEqual(self.search_task_tui.task_search_text_box.get(), '')

        expected_categories = [
            'All',
            Category(1, 'TODO Tasks'),
            Category(2, 'Custom Category')
        ]
        self.assertCountEqual(self.search_task_tui.categories_list, expected_categories)

        expected_tasks = [
            f'New task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Different task[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'TODO Task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'Custom Task #1[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #2[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #3[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}'
        ]
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

    def test_date_widget(self):
        # Any date
        self.search_task_tui.task_date_menu.set_selected_item_index(0)
        self.search_task_tui._set_date_option()
        self.assertEqual(self.search_task_tui.selected_date, None)

        # Today
        self.search_task_tui.task_date_menu.set_selected_item_index(1)
        self.search_task_tui._set_date_option()
        self.assertIsInstance(self.search_task_tui.selected_date, date)

        # Yesterday
        self.search_task_tui.task_date_menu.set_selected_item_index(2)
        self.search_task_tui._set_date_option()
        self.assertIsInstance(self.search_task_tui.selected_date, date)

        # Week
        self.search_task_tui.task_date_menu.set_selected_item_index(3)
        self.search_task_tui._set_date_option()
        self.assertIsInstance(self.search_task_tui.selected_date, list)

        # Month
        self.search_task_tui.task_date_menu.set_selected_item_index(4)
        self.search_task_tui._set_date_option()
        self.assertIsInstance(self.search_task_tui.selected_date, list)

    def test_category_widget(self):
        # All
        self.search_task_tui.task_categories_menu.set_selected_item_index(0)
        self.search_task_tui._set_category_option()
        self.assertEqual(self.search_task_tui.selected_category, None)

        # Todo Tasks
        self.search_task_tui.task_categories_menu.set_selected_item_index(1)
        self.search_task_tui._set_category_option()
        self.assertEqual(self.search_task_tui.selected_category, Category(1, 'TODO Tasks'))

        # Custom Category
        self.search_task_tui.task_categories_menu.set_selected_item_index(2)
        self.search_task_tui._set_category_option()
        self.assertEqual(self.search_task_tui.selected_category, Category(2, 'Custom Category'))

    def test_status_widget(self):
        # All
        self.search_task_tui.task_status_menu.set_selected_item_index(0)
        self.search_task_tui._set_status_option()
        self.assertEqual(self.search_task_tui.selected_status, None)

        # Incomplete
        self.search_task_tui.task_status_menu.set_selected_item_index(1)
        self.search_task_tui._set_status_option()
        self.assertEqual(self.search_task_tui.selected_status, 0)

        # In Process
        self.search_task_tui.task_status_menu.set_selected_item_index(2)
        self.search_task_tui._set_status_option()
        self.assertEqual(self.search_task_tui.selected_status, 1)

        # Finished
        self.search_task_tui.task_status_menu.set_selected_item_index(3)
        self.search_task_tui._set_status_option()
        self.assertEqual(self.search_task_tui.selected_status, 2)

    def test_search_all_tasks(self):
        expected_tasks = [
            f'New task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Different task[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'TODO Task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'Custom Task #1[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #2[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #3[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}'
        ]
        self.search_task_tui._load_all_tasks()

        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

    def test_search_by_category(self):
        # Any Category
        expected_tasks = [
            f'New task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Different task[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'TODO Task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'Custom Task #1[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #2[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #3[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}'
        ]
        self.search_task_tui.task_categories_menu.set_selected_item_index(0)
        self.search_task_tui._set_category_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)
        
        # TODO Tasks
        expected_tasks = [
            f'New task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Different task[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'TODO Task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}'
        ]

        self.search_task_tui.task_categories_menu.set_selected_item_index(1)
        self.search_task_tui._set_category_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

        # Custom Category
        expected_tasks = [
            f'Custom Task #1[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #2[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #3[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}'
        ]
        self.search_task_tui.task_categories_menu.set_selected_item_index(2)
        self.search_task_tui._set_category_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

    def test_search_by_date(self):
        expected_tasks = [
            f'New task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Different task[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'TODO Task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'Custom Task #1[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #2[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #3[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}'
        ]
        
        # Any Date
        self.search_task_tui.task_date_menu.set_selected_item_index(0)
        self.search_task_tui._set_date_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)
        
        # Today
        self.search_task_tui.task_date_menu.set_selected_item_index(1)
        self.search_task_tui._set_date_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

        # Week
        self.search_task_tui.task_date_menu.set_selected_item_index(3)
        self.search_task_tui._set_date_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

        # Month
        self.search_task_tui.task_date_menu.set_selected_item_index(4)
        self.search_task_tui._set_date_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

        expected_tasks = []

        # Yesterday
        self.search_task_tui.task_date_menu.set_selected_item_index(2)
        self.search_task_tui._set_date_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

    def test_search_by_status(self):
        expected_tasks = [
            f'New task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'New task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Different task[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'TODO Task #1[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #2[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',
            f'TODO Task #3[Incomplete][TODO Tasks]-{self.current_date.strftime("%Y-%m-%d")}',

            f'Custom Task #1[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #2[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}',
            f'Custom Task #3[Incomplete][Custom Category]-{self.current_date.strftime("%Y-%m-%d")}'
        ]
        self.search_task_tui.task_status_menu.set_selected_item_index(0)
        self.search_task_tui._set_status_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

        self.search_task_tui.task_status_menu.set_selected_item_index(1)
        self.search_task_tui._set_status_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

        expected_tasks = []

        self.search_task_tui.task_status_menu.set_selected_item_index(2)
        self.search_task_tui._set_status_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

        self.search_task_tui.task_status_menu.set_selected_item_index(3)
        self.search_task_tui._set_status_option()
        self.assertCountEqual(self.search_task_tui.tasks_list_menu.get_item_list(), expected_tasks)

    def tearDown(self) -> None:
        del self.root
        del self.search_task_tui
