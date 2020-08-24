import py_cui
import curses
from typing import List
from yaspin import yaspin
from datetime import date, datetime, timedelta

import codenotes.db.utilities.tasks as tasks
from codenotes.console import PrintFormatted
from codenotes.db.connection import SQLiteConnection


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

    def __init__(self, root: ImpPyCUI):
        """ Constructor of AddTaskTUI class"""
        self.root = root
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()

        self.task_text_block = self.root.add_text_box('New Task', 0, 0, column_span=4)
        self.task_categories_menu = self.root.add_scroll_menu('Categories', 1, 0, row_span=3)
        self.tasks_list_menu = self.root.add_scroll_menu('Tasks to add', 1, 1, column_span=3, row_span=4)

        self.__config()

    @classmethod
    def set_root(cls, root: ImpPyCUI):
        return cls(root)

    def _add_task(self):
        """  Adds task to tasks_list_menu widget """
        text = self.task_text_block.get()
        self.tasks_list_menu.add_item(text)
        self.task_text_block.clear()

    def _remove_task(self):
        """ Removes task from list """
        self.tasks_list_menu.remove_selected_item()

    def _save_tasks(self):
        """ Function that stores the tasks added in tasks_list_menu widget """
        creation_date = datetime.now().date()
        tasks_list = self.tasks_list_menu.get_item_list()
        sql = f'INSERT INTO {tasks.TABLE_NAME} ({tasks.COLUMN_TASK_CONTENT},{tasks.COLUMN_TASK_CREATION}) VALUES ' \
              f'(?,?); '
        with yaspin(text='Saving Tasks') as spinner:
            for task in tasks_list:
                values = (task, creation_date)
                self.cursor.execute(sql, values)
                self.db.conn.commit()
                spinner.hide()
                PrintFormatted.print_tasks_storage(task)
                spinner.show()
            if tasks_list:
                spinner.ok("✔")
            else:
                spinner.text = 'No Task Saved'
                spinner.fail("💥")
        self.cursor.close()
        self.db.conn.close()

    def __config(self):
        """ Function that configures the widgets of the root """
        self.task_text_block.add_key_command(py_cui.keys.KEY_ENTER, self._add_task)
        self.task_text_block.set_focus_text('|Enter - Add New Task|')

        self.tasks_list_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self._remove_task)
        self.tasks_list_menu.set_focus_text('|Backspace - Remove Task|')

        self.root.set_title('Codenotes - Add Tasks')
        self.root.status_bar.set_text('|q-Quit & Save Tasks| Arrows keys - Move| Enter - Enter Focus Mode|')
        self.root.run_on_exit(self._save_tasks)


class SearchTaskTUI:

    DATE_OPTIONS: List[str] = ['None', 'Today', 'Yesterday']

    date_search_button: py_cui.widgets.Button
    task_search_text_box: py_cui.widgets.TextBox

    search_date: date = None

    def __init__(self, root: ImpPyCUI):
        """ Constructor of SearchTaskTUI class """
        self.root = root
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()

        self.date_search_button = self.root.add_button('Select Date', 0, 3, command=self._show_menu_date_popup)
        self.task_search_text_box = self.root.add_text_box('Search task:', 0, 0)

        self.__config()

    @classmethod
    def set_root(cls, root: ImpPyCUI):
        return cls(root)

    def _show_menu_date_popup(self):
        self.root.show_menu_popup('Date Options', menu_items=self.DATE_OPTIONS, command=self._set_date_option)

    def _set_date_option(self, date_option):
        if date_option == 'None':
            title = 'Select Date'
            self.search_date = None
        elif date_option == 'Today':
            title = 'Today'
            self.search_date = datetime.now().date()
        elif date_option == 'Yesterday':
            title = 'Yesterday'
            self.search_date = datetime.now().date() - timedelta(days=1)

        self.date_search_button.set_title(title)

    def __config(self):
        """ Function that configures the widgets of the root """

        self.root.set_title('Codenotes - Search Tasks')
