from rich import box
from yaspin import yaspin
from rich.table import Table
from datetime import datetime
from rich.console import Console
from typing import List, Union, overload

import codenotes.db.utilities.tasks as tasks
from codenotes.util.sql import add_conditions_sql
from codenotes.db.connection import SQLiteConnection
from codenotes.tui import AddTaskTUI, ImpPyCUI, SearchTaskTUI
from codenotes.console import PrintFormatted, args_needed_empty, dates_to_search


@overload
def format_task_text(text: str) -> List[str]: ...


@overload
def format_task_text(text: str) -> str: ...


def format_task_text(text: str) -> Union[List[str], str]:
    """ Function that formats text passed through arguments
    Parameters
    ----------
    text : str
        Text written in the arguments of argparse
    Returns
    -------
    task_text : str
        Task of text passed in arguments and joined
    tasks_list : List[str]
        List of texts of task joined and stripped
    """
    task_text = ' '.join(text)
    if ';' in task_text:
        tasks_list = []
        for task in task_text.split(';'):
            if task and not task.isspace():
                # Checks if is '' or ' ', and doesn't append it if so
                tasks_list.append(task.strip())  # "Trim"
        return tasks_list
    else:
        return task_text


def status_text(status: int) -> str:
    if status == 0:
        return 'Incomplete'
    elif status == 1:
        return 'Process'
    elif status == 2:
        return 'Finished'


class AddTask:

    def __init__(self, args):
        """ Constructor fro AddTask class """
        self.console = Console()
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        self.creation_date = datetime.now().date()

        if args.text:
            self.task = format_task_text(args.text)
            if args.preview:
                self.show_preview()
            else:
                self.save_task()
        else:
            root = ImpPyCUI(5, 4)
            AddTaskTUI.set_root(root)
            root.start()

    @classmethod
    def set_args(cls, args):
        return cls(args)

    def save_task(self):
        """ Function in charge to store the tasks in the database"""
        creation_date = datetime.now().date()  # Actual date

        sql = f'INSERT INTO {tasks.TABLE_NAME} ({tasks.COLUMN_TASK_CONTENT},{tasks.COLUMN_TASK_CREATION}) VALUES (?,?);'
        with yaspin(text='Saving Tasks', color='yellow') as spinner:  # TODO:THIS COULD BE TRANSFORM INTO FUNCTION
            if isinstance(self.task, List):
                for task in self.task:
                    values = (task, creation_date)
                    self.cursor.execute(sql, values)
                    self.db.conn.commit()
                    spinner.hide()
                    PrintFormatted.print_tasks_storage(task)
                    spinner.show()

            elif isinstance(self.task, str):
                values = (self.task, creation_date)
                self.cursor.execute(sql, values)
                self.db.conn.commit()
                spinner.hide()
                PrintFormatted.print_tasks_storage(self.task)
                spinner.show()
            spinner.ok("✔")  # TODO: WHEN TASK PASSED IS ;, DISPLAY 'NOT SAVED TASKS'
        self.db.close()

    def _ask_confirmation(self) -> bool:
        """ Function that asks to the user to store or not

        Returns
        -------
        confirmed : bool
            Boolean value that indicates the storage of the tasks written
        """
        answer = self.console.input('Do you want to save them?(y/n):')
        while len(answer) > 0 and answer.lower() != 'n' and answer.lower() != 'y':
            answer = self.console.input('Do you want to save them?(y/n):')
        else:
            if answer.lower() == 'y':
                return True
            return False

    def show_preview(self):
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
        """ SearchTask Constructor """
        self.console = Console()
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        self.search_date = dates_to_search(args)
        self.search_text = ' '.join(args.text)

        if args_needed_empty(args):
            root = ImpPyCUI(5, 6)
            SearchTaskTUI.set_root(root)
            root.start()
        else:
            self.search_task()

    @classmethod
    def set_args(cls, args):
        return cls(args)

    def sql_query(self):

        base_sql = f'SELECT {tasks.COLUMN_TASK_CONTENT},{tasks.COLUMN_TASK_STATUS}, {tasks.COLUMN_TASK_CREATION} from' \
                   f' "{tasks.TABLE_NAME}"'
        if self.search_date:
            base_sql = add_conditions_sql(base_sql, f'{tasks.COLUMN_TASK_CREATION} LIKE date("{self.search_date}")')
        if self.search_text:
            base_sql = add_conditions_sql(base_sql, f'{tasks.COLUMN_TASK_CONTENT} LIKE "%{self.search_text}%"', 'AND')
        query = self.cursor.execute(base_sql)
        
        return query.fetchall()

    def search_task(self):
        """ Function that displays a table with the tasks searched """
        table = Table()
        table.add_column('Tasks')
        table.add_column('Status')
        table.add_column('Creation Date', justify='center', style='yellow')

        for task in self.sql_query():
            table.add_row(task[0], status_text(task[1]), task[2])
        self.console.print(table, justify='center')
        # self.console.rule(self.search_date.strftime('%m-%d-%Y'), style='purple')
        # self.db.close()

# select * from cn_todos where cn_todo_creation like date('2020-08-17');
