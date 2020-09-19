from typing import List, Union, overload, Tuple

from rich import box
from yaspin import yaspin
from rich.table import Table
from datetime import datetime, date
from rich.console import Console

from codenotes.util import status_text
from codenotes.db import add_conditions_sql
import codenotes.db.utilities.tasks as tasks
from codenotes.db.connection import SQLiteConnection
import codenotes.db.utilities.tasks_categories as categories
from codenotes.tui import AddTaskTUI, ImpPyCUI, SearchTaskTUI
from codenotes.cli import PrintFormatted, date_args_empty, dates_to_search, format_argument_text


@overload
def format_task_text(text: List[str]) -> List[str]: ...


@overload
def format_task_text(text: List[str]) -> str: ...


def format_task_text(text: List[str]) -> Union[List[str], str]:
    """ Function that formats text passed through arguments
    Parameters
    ----------
    text : List[str]
        Text written in the arguments of argparse
    Returns
    -------
    task_text : str
        Task of text passed in arguments and joined
    tasks_list : List[str]
        List of texts of task joined and stripped
    """
    task_text = format_argument_text(text)

    if ';' in task_text:
        tasks_list = []

        for task in task_text.split(';'):
            if task and not task.isspace():
                # Checks if is '' or ' ', and doesn't append it if so
                tasks_list.append(task.strip())  # "Trim"

        return tasks_list
    else:
        return task_text


def add_task_args_empty(args) -> bool:
    args_needed = [
        args.text,
        args.new_category
    ]

    if any(args_needed):
        return False
    return True


class AddTask:

    category_id: int = 1
    category_text: str

    def __init__(self, args):
        """ Constructor fro AddTask class 
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        self.console = Console()
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        self.creation_date = datetime.now().date()

        if add_task_args_empty(args):
            root = ImpPyCUI(5, 4)
            AddTaskTUI.set_root(root)
            root.start()

        else:

            if args.new_category:
                self.category_text = format_argument_text(args.new_category)
                self.save_category()

            if args.text:
                self.task = format_task_text(args.text)

                if args.preview:
                    self._show_preview()
                else:
                    self.save_task()

    @classmethod
    def set_args(cls, args):
        """ Set args and initialize class
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        return cls(args)

    def save_category(self):
        """ Creates and saves a new category

        When the task(s) is going to be saved and is created a new category,
        it will set the id of this new one and store the task(s) in this created category
        """
        if len(self.category_text) <= 30:
            sql = f'INSERT INTO {categories.TABLE_NAME} ({categories.COLUMN_CATEGORY_NAME}) VALUES (?)'
            self.cursor.execute(sql, (self.category_text,))

            self.category_id = self.cursor.lastrowid

            self.db.commit()
        else:
            self._ask_category()

    def save_task(self):
        """ Function in charge to store the tasks in the database"""

        sql = f'INSERT INTO {tasks.TABLE_NAME} ({tasks.COLUMN_TASK_CONTENT},{tasks.COLUMN_TASK_CREATION}, '\
              f'{tasks.COLUMN_TASK_CATEGORY}) VALUES (?,?,?);'

        with yaspin(text='Saving Tasks', color='yellow') as spinner:
            if isinstance(self.task, list):
                for task in self.task:
                    values = (task, self.creation_date, self.category_id)
                    self.cursor.execute(sql, values)
                    spinner.hide()
                    PrintFormatted.print_tasks_storage(task)
                    spinner.show()

            elif isinstance(self.task, str):
                values = (self.task, self.creation_date, self.category_id)
                self.cursor.execute(sql, values)
                spinner.hide()
                PrintFormatted.print_tasks_storage(self.task)
                spinner.show()

            if self.task:
                spinner.ok("✔")
            else:
                spinner.text = 'No Task Saved'
                spinner.fail("💥")

        self.db.commit()
        self.db.close()

    def _ask_confirmation(self) -> bool:
        """ Function that asks to the user to store or not

        Returns
        -------
        confirmed : bool
            Boolean value that indicates the storage of the tasks written
        """
        text = 'Do you want to save them?(y/n):'
        answer = self.console.input(text)
        while len(answer) > 0 and answer.lower() != 'n' and answer.lower() != 'y':
            answer = self.console.input(text)
        else:
            if answer.lower() == 'y':
                return True
            return False

    def _ask_category(self):
        """ Function that asks to the user to introduce different category name """

        text = 'Category name is too long(Max. 30). Write another name:'
        self.category_text = self.console.input(text).strip()

        while len(self.category_text) == 0 or len(self.category_text) > 30:
            self.category_text = self.console.input(text).strip()
        else:
            self.save_category()

    def _show_preview(self):
        """ Function that displays a table with the tasks written"""
        formatted_date = self.creation_date.strftime('%Y-%m-%d')
        
        self.console.rule('Preview', style='purple')
        
        table = Table(box=box.SIMPLE_HEAD)
        table.add_column('Task')
        table.add_column('Creation Date', justify='center', style='yellow')
        
        if isinstance(self.task, List):
            for task in self.task:
                table.add_row(task, formatted_date)
        elif isinstance(self.task, str):
            table.add_row(self.task, formatted_date)

        self.console.print(table, justify='center')

        if self._ask_confirmation():
            self.save_task()


class SearchTask:

    def __init__(self, args):
        """ SearchTask Constructor 
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        self.console = Console()
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        self.search_date = dates_to_search(args)
        self.search_text = format_argument_text(args.text)

        if date_args_empty(args):
            root = ImpPyCUI(6, 6)
            SearchTaskTUI.set_root(root)
            root.start()
        else:
            self.search_task()

    @classmethod
    def set_args(cls, args):
        """ Set args and initialize class
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        return cls(args)

    def sql_query(self) -> List[Tuple[str]]:
        """ Function that makes a query of related information of tasks"""
        sql = f'SELECT {tasks.TABLE_NAME}.{tasks.COLUMN_TASK_CONTENT},{tasks.TABLE_NAME}.{tasks.COLUMN_TASK_STATUS}, ' \
              f'{tasks.TABLE_NAME}.{tasks.COLUMN_TASK_CREATION}, ' \
              f'{categories.TABLE_NAME}.{categories.COLUMN_CATEGORY_NAME} FROM {tasks.TABLE_NAME} INNER JOIN ' \
              f'{categories.TABLE_NAME} ON {tasks.TABLE_NAME}.{tasks.COLUMN_TASK_CATEGORY} = ' \
              f'{categories.TABLE_NAME}.{categories.COLUMN_CATEGORY_ID}'

        if self.search_date:
            if isinstance(self.search_date, date):
                sql = add_conditions_sql(sql, f'{tasks.COLUMN_TASK_CREATION} LIKE date("{self.search_date}")')

            elif isinstance(self.search_date, list):
                first_day, last_day = self.search_date
                sql = add_conditions_sql(sql, f'{tasks.COLUMN_TASK_CREATION} BETWEEN date("{first_day}") '
                                              f'AND date("{last_day}")')
        if self.search_text:
            sql = add_conditions_sql(sql, f'{tasks.COLUMN_TASK_CONTENT} LIKE "%{self.search_text}%"', 'AND')

        query = self.cursor.execute(sql)

        return query.fetchall()

    def search_task(self):
        """ Function that displays a table with the tasks searched """
        table = Table()

        table.add_column('Tasks')
        table.add_column('Status')
        table.add_column('Category')
        table.add_column('Creation Date', justify='center', style='yellow')

        for task in self.sql_query():
            table.add_row(task[0], status_text(task[1]), task[3], task[2])
        self.console.print(table, justify='center')
        # self.cli.rule(self.search_date.strftime('%m-%d-%Y'), style='purple')

# select * from cn_todos where cn_todo_creation like date('2020-08-17');
