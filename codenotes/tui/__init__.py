import py_cui
import curses
import calendar
from yaspin import yaspin
from typing import List, Tuple, Optional, Any, Union
from datetime import date, datetime, timedelta

from codenotes.util import status_text
from codenotes.db import add_conditions_sql
import codenotes.db.utilities.tasks as tasks
from codenotes.cli import PrintFormatted
from codenotes.db.utilities import Category, Task
from codenotes.db.connection import SQLiteConnection
import codenotes.db.utilities.tasks_categories as categories

WHITE_ON_MAGENTA = 11


class ImpPyCUI(py_cui.PyCUI):

    def __init__(self, num_rows, num_cols, auto_focus_buttons=True, exit_key=py_cui.keys.KEY_Q_LOWER,
                 simulated_terminal=None):
        """ Initializer of ImpPyCUI class"""
        super().__init__(num_rows, num_cols, auto_focus_buttons, exit_key, simulated_terminal)
        self.toggle_unicode_borders()

    def _initialize_colors(self):
        """ Override of base class function"""
        super()._initialize_colors()
        curses.init_pair(WHITE_ON_MAGENTA, curses.COLOR_WHITE, curses.COLOR_MAGENTA)


class AddTaskTUI:

    tasks_list_menu: py_cui.widgets.ScrollMenu
    task_text_block: py_cui.widgets.TextBox

    categories_list: List[Category] = []
    selected_category: Category = None

    def __init__(self, root: ImpPyCUI):
        """ Constructor of AddTaskTUI class"""
        self.root = root
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()

        # -| Text Blocks |-
        self.task_text_block = self.root.add_text_box('New Task', 0, 0, column_span=4)
        # -| Scroll Menus |-
        self.task_categories_menu = self.root.add_scroll_menu('Categories', 1, 0, row_span=4)
        self.tasks_list_menu = self.root.add_scroll_menu('Tasks to add', 1, 1, column_span=3, row_span=3)
        # -| Buttons |-
        self.save_button = self.root.add_button('Save Tasks', 4, 1, column_span=3, command=self.save_tasks)

        self.__config()

    @classmethod
    def set_root(cls, root: ImpPyCUI):
        """ Sets root and initialize class
        
        Parameters
        ----------
        root : ImpPyCUI
            Root for TUI
        """
        return cls(root)

    def get_categories(self) -> List[Tuple[str]]:
        """ Gets all categories stored in database """
        sql = f'SELECT {categories.COLUMN_CATEGORY_ID},{categories.COLUMN_CATEGORY_NAME} FROM {categories.TABLE_NAME};'

        query = self.cursor.execute(sql)

        return query.fetchall()

    def _show_category_name(self):
        """ Shows message popup to display complete the whole category name """
        category = self.task_categories_menu.get()
        print(type(category))

        self.root.show_message_popup('Category Name:', category.category_name)

    def _show_missing_category(self):
        """ Shows warning popup to advice the user that he hasn't choose a category where to save the tasks """
        self.root.show_warning_popup("You Haven't Choose a Category", 'Please Select Category Where to Save the Tasks')

    def _load_menu_categories(self):
        """ Functions that creates a list of tasks and added it to the categories menu """
        self.categories_list = [Category(category[0], category[1]) for category in self.get_categories()]

        self.task_categories_menu.add_item_list(self.categories_list)

    def _set_category_option(self):
        """ Function that is executed when a category is selected """
        self.selected_category = self.task_categories_menu.get()

        self.task_categories_menu.set_title(f'{self.selected_category}')

    def _ask_new_category(self):
        """ Shows text box popup """
        self.root.show_text_box_popup('Enter new category name (Max. 30):', command=self.add_category)

    def add_category(self, category: str):
        """ Adds new category to categories menu and saves it in database """
        if category and len(category) <= 30:
            sql = f'INSERT INTO {categories.TABLE_NAME} ({categories.COLUMN_CATEGORY_NAME}) VALUES (?)'

            self.cursor.execute(sql, (category.strip(),))

            category_id = self.cursor.lastrowid
            self.task_categories_menu.add_item(Category(category_id, category))

            self.db.conn.commit()
        else:
            self._ask_new_category()

    def add_task(self):
        """  Adds task to tasks_list_menu widget """
        text = self.task_text_block.get()

        self.tasks_list_menu.add_item(text.strip())
        self.task_text_block.clear()

    def remove_task(self):
        """ Removes task from list """
        self.tasks_list_menu.remove_selected_item()

    def save_tasks(self):
        """ Function that stores the tasks added in tasks_list_menu widget """
        tasks_list = self.tasks_list_menu.get_item_list()
        creation_date = datetime.now().date()

        sql = f'INSERT INTO {tasks.TABLE_NAME} ({tasks.COLUMN_TASK_CONTENT},{tasks.COLUMN_TASK_CREATION}, '\
              f'{tasks.COLUMN_TASK_CATEGORY}) VALUES (?,?,?); '

        with yaspin(text='Saving Tasks') as spinner:
            if tasks_list:
                if self.selected_category is not None:
                    # Selected a category
                    self.root.stop()
                    for task in tasks_list:
                        values = (task, creation_date, self.selected_category.category_id)

                        self.cursor.execute(sql, values)
                        spinner.hide()
                        PrintFormatted.print_content_storage(task, self.selected_category.category_name)
                        spinner.show()
                    spinner.ok("✔")

                    self.db.conn.commit()
                    self.db.close()
                else:
                    self._show_missing_category()
            else:
                # Empty list of tasks
                self.root.stop()
                spinner.text = 'No Task Saved'
                spinner.fail("💥")
                self.db.close()

    def __config(self):
        """ Function that configures the widgets of the root """
        self._load_menu_categories()

        self.task_text_block.add_key_command(py_cui.keys.KEY_ENTER, self.add_task)
        self.task_text_block.set_focus_text('|Enter - Add New Task| Esc - Exit|')

        self.tasks_list_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.remove_task)
        self.tasks_list_menu.set_focus_text('|Backspace - Remove Task|Esc - Exit |')

        self.task_categories_menu.add_key_command(py_cui.keys.KEY_ENTER, self._set_category_option)
        self.task_categories_menu.add_key_command(py_cui.keys.KEY_N_LOWER, self._ask_new_category)
        self.task_categories_menu.add_key_command(py_cui.keys.KEY_SPACE, self._show_category_name)
        self.task_categories_menu.set_focus_text(
            '|n - New Category|Enter - Select Category|Space - Show category|Up/Down - Move|Esc - Exit|'
        )

        self.root.set_title('Codenotes - Add Tasks')
        self.root.status_bar.set_text('|q-Quit Without Saving Tasks| Arrows keys - Move| Enter - Enter Focus Mode|')


class SearchTaskTUI:

    DATE_OPTIONS: List[str] = ['Any Date', 'Today', 'Yesterday', 'Week', 'Month']
    STATUS_OPTION: List[str] = ['All', 'Incomplete', 'In Process', 'Finished']
    BASE_SQL: str = f'SELECT {tasks.TABLE_NAME}.{tasks.COLUMN_TASK_ID},' \
                    f'{tasks.TABLE_NAME}.{tasks.COLUMN_TASK_CONTENT},{tasks.TABLE_NAME}.{tasks.COLUMN_TASK_STATUS},' \
                    f'{categories.TABLE_NAME}.{categories.COLUMN_CATEGORY_NAME},' \
                    f'{tasks.TABLE_NAME}.{tasks.COLUMN_TASK_CREATION} FROM {tasks.TABLE_NAME} INNER JOIN ' \
                    f'{categories.TABLE_NAME} ON {tasks.TABLE_NAME}.{tasks.COLUMN_TASK_CATEGORY} = ' \
                    f'{categories.TABLE_NAME}.{categories.COLUMN_CATEGORY_ID}'

    task_search_text_box: py_cui.widgets.TextBox
    tasks_list_menu: py_cui.widgets.ScrollMenu
    task_categories_menu: py_cui.widgets.ScrollMenu
    task_date_menu: py_cui.widgets.ScrollMenu
    task_status_menu: py_cui.widgets.ScrollMenu

    selected_date: Union[Optional[date], Optional[List[date]]] = None
    selected_category: Optional[Category] = None
    selected_status: Optional[int] = None
    tasks_list: List[Task]
    categories_list: List[Any]

    def __init__(self, root: ImpPyCUI):
        """ Constructor of SearchTaskTUI class 

        Parameters
        ----------
        root : ImpPyCUI
            Root for TUI
        """
        self.root = root
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        # -| Text Boxes |-
        self.task_search_text_box = self.root.add_text_box('Search task:', 0, 1, column_span=5)
        # -| Scroll Menu |-
        self.tasks_list_menu = self.root.add_scroll_menu('Task', 1, 1, row_span=5, column_span=5)
        self.task_categories_menu = self.root.add_scroll_menu('Category', 0, 0, row_span=2)
        self.task_date_menu = self.root.add_scroll_menu('Date', 2, 0, row_span=2)
        self.task_status_menu = self.root.add_scroll_menu('Status', 4, 0, row_span=2)

        self.__config()

    @classmethod
    def set_root(cls, root: ImpPyCUI):
        """ Sets root and initialize class
        
        Parameters
        ----------
        root : ImpPyCUI
            Root for TUI
        """
        return cls(root)

    def get_categories(self) -> List[Tuple[str]]:
        """ Gets all categories stored in database """
        sql = f'SELECT {categories.COLUMN_CATEGORY_ID},{categories.COLUMN_CATEGORY_NAME} FROM {categories.TABLE_NAME};'

        query = self.cursor.execute(sql)

        return query.fetchall()

    def _set_status_option(self):
        """ Sets the selected status from status menu """
        index = self.task_status_menu.get_selected_item_index()
        if index == 0:  # All
            self.selected_status = None
        else:
            self.selected_status = index - 1  # Status code that goes from 0 to 2

        self._load_all_tasks()

    def _set_date_option(self):
        """ Sets the selected date from date menu """
        index = self.task_date_menu.get_selected_item_index()
        now = datetime.now().date()

        if index == 0:  # Any Date
            self.selected_date = None
        
        elif index == 1:  # Today
            self.selected_date = now

        elif index == 2:  # Yesterday
            self.selected_date = now - timedelta(days=1)

        elif index == 3:  # Week
            first_day = now - timedelta(days=now.weekday())
            last_day = first_day + timedelta(days=6)

            self.selected_date = [first_day, last_day]

        elif index == 4:  # Month
            num_days = calendar.monthrange(now.year, now.month)[1]
            self.selected_date = [
                date(now.year, now.month, 1),
                date(now.year, now.month, num_days)
            ]

        self._load_all_tasks()

    def _set_category_option(self):
        """ Sets the selected category from category menu """
        if self.task_categories_menu.get_selected_item_index() != 0:  # All Categories
            category = self.task_categories_menu.get()

            self.selected_category = category
            self.task_categories_menu.set_title(category.category_name)  # TODO: ADD ABBREVIATION

        else:
            self.selected_category = None
            self.task_categories_menu.set_title('Category')

        self._load_all_tasks()

    def _show_category_popup(self):
        """ Shows message popup to display the complete category name """
        category = self.task_categories_menu.get()
        self.root.show_message_popup('Category Name:', category.category_name)

    def _load_all_tasks(self):
        """ Loads tasks to the task list menu
        
        Will also generate the sql statement for the query
        """
        self.tasks_list = []
        self.tasks_list_menu.clear()
        sql = self.BASE_SQL

        if self.selected_date is not None:
            if isinstance(self.selected_date, date):
                sql = add_conditions_sql(sql, f'{tasks.COLUMN_TASK_CREATION} LIKE date("{self.selected_date}")')

            elif isinstance(self.selected_date, list):
                first_day, last_day = self.selected_date
                sql = add_conditions_sql(sql, f'{tasks.COLUMN_TASK_CREATION} BETWEEN date("{first_day}") '
                                              f'AND date("{last_day}")')

        if self.selected_category is not None:
            sql = add_conditions_sql(sql, f'{tasks.COLUMN_TASK_CATEGORY} = {self.selected_category.category_id}', 'AND')

        if self.selected_status is not None:
            sql = add_conditions_sql(sql, f'{tasks.COLUMN_TASK_STATUS} = {self.selected_status}', 'AND')

        if self.task_search_text_box.get():
            sql = add_conditions_sql(sql, f'{tasks.COLUMN_TASK_CONTENT} LIKE "%{self.task_search_text_box.get()}%"',
                                     'AND')

        query = self.cursor.execute(sql)

        for task in query.fetchall():
            dataclass_task = Task(task[0], task[1], task[2], task[3], task[4])
            self.tasks_list.append(dataclass_task)

            self.tasks_list_menu.add_item(
                f'{task[1]}[{status_text(task[2])}][{task[3]}]-{task[4]}'
            )

    def _load_menu_categories(self):
        """ Functions that creates a list of tasks and added it to the categories menu """
        self.categories_list = [Category(category[0], category[1]) for category in self.get_categories()]
        self.categories_list.insert(0, 'All')

        self.task_categories_menu.add_item_list(self.categories_list)

    def __config(self):
        """ Function that configures the widgets of the root """
        self._load_all_tasks()
        self._load_menu_categories()

        self.task_categories_menu.add_key_command(py_cui.keys.KEY_ENTER, self._set_category_option)
        self.task_categories_menu.add_key_command(py_cui.keys.KEY_SPACE, self._show_category_popup)
        self.task_categories_menu.set_focus_text('|Enter - Select Category|Up/Down - Move|Esc - Exit|')

        self.task_status_menu.add_item_list(self.STATUS_OPTION)
        self.task_status_menu.add_key_command(py_cui.keys.KEY_ENTER, self._set_status_option)
        self.task_status_menu.set_focus_text('|Enter - Select Status|Up/Down - Move|Esc - Exit|')

        self.task_date_menu.add_item_list(self.DATE_OPTIONS)
        self.task_date_menu.add_key_command(py_cui.keys.KEY_ENTER, self._set_date_option)
        self.task_date_menu.set_focus_text('|Enter - Select Date|Up/Down - Move|Esc - Exit|')

        self.tasks_list_menu.add_text_color_rule('Incomplete', py_cui.RED_ON_BLACK, rule_type='contains',
                                                 match_type='regex')
        self.tasks_list_menu.add_text_color_rule('In Process', py_cui.YELLOW_ON_BLACK, rule_type='contains',
                                                 match_type='regex')
        self.tasks_list_menu.add_text_color_rule('Finished', py_cui.GREEN_ON_BLACK, rule_type='contains',
                                                 match_type='regex')

        self.root.add_key_command(py_cui.keys.KEY_S_LOWER, self._load_all_tasks)
        self.root.set_title('Codenotes - Search Tasks')
