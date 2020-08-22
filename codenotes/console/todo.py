from rich import box
from yaspin import yaspin
from rich.table import Table
from datetime import datetime
from rich.console import Console
from typing import List, Union, overload

import codenotes.db.utilities.todo as todo
from codenotes.util.sql import add_conditions_sql
from codenotes.db.connection import SQLiteConnection
from codenotes.tui import AddTodoTUI, ImpPyCUI, SearchTodoTUI
from codenotes.console import PrintFormatted, args_needed_empty, dates_to_search


@overload
def format_todo_text(text: str) -> List[str]: ...


@overload
def format_todo_text(text: str) -> str: ...


def format_todo_text(text: str) -> Union[List[str], str]:
    """ Function that formats text passed through arguments
    Parameters
    ----------
    text : str
        Text written in the arguments of argparse
    Returns
    -------
    todo_text : str
        Task of text passed in arguments and joined
    todo_tasks_list : List[str]
        List of texts of task joined and stripped
    """
    todo_text = ' '.join(text)
    if ';' in todo_text:
        todo_tasks_list = []
        for todo_task in todo_text.split(';'):
            if todo_task and not todo_task.isspace():
                # Checks if is '' or ' ', and doesn't append it if so
                todo_tasks_list.append(todo_task.strip())  # "Trim"
        return todo_tasks_list
    else:
        return todo_text


class AddTodo:

    def __init__(self, args):
        """ Constructor fro AddTodo class """
        self.console = Console()
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        self.creation_date = datetime.now().date()

        if args.text:
            self.todo_task = format_todo_text(args.text)
            if args.preview:
                self.show_preview()
            else:
                self.save_todo()
        else:
            root = ImpPyCUI(5, 4)
            AddTodoTUI.set_root(root)
            root.start()

    @classmethod
    def set_args(cls, args):
        return cls(args)

    def save_todo(self):
        """ Function in charge to store the todo tasks in the database"""
        creation_date = datetime.now().date()  # Actual date

        sql = f'INSERT INTO {todo.TABLE_NAME} ({todo.COLUMN_TODO_CONTENT},{todo.COLUMN_TODO_CREATION}) VALUES (?,?);'
        with yaspin(text='Saving todo tasks', color='yellow') as spinner:  # TODO:THIS COULD BE TRANSFORM INTO FUNCTION
            if isinstance(self.todo_task, List):
                for task in self.todo_task:
                    values = (task, creation_date)
                    self.cursor.execute(sql, values)
                    self.db.conn.commit()
                    spinner.hide()
                    PrintFormatted.print_tasks_storage(task)
                    spinner.show()

            elif isinstance(self.todo_task, str):
                values = (self.todo_task, creation_date)
                self.cursor.execute(sql, values)
                self.db.conn.commit()
                spinner.hide()
                PrintFormatted.print_tasks_storage(self.todo_task)
                spinner.show()
            spinner.ok("✔")  # TODO: WHEN TASK PASSED IS ;, DISPLAY 'NOT SAVED TASKS'
        self.db.close()

    def _ask_confirmation(self) -> bool:
        """ Function that asks to the user to store or not

        Returns
        -------
        confirmed : bool
            Boolean value that indicates the storage of the todo tasks written
        """
        answer = self.console.input('Do you want to save them?(y/n):')
        while len(answer) > 0 and answer.lower() != 'n' and answer.lower() != 'y':
            answer = self.console.input('Do you want to save them?(y/n):')
        else:
            if answer.lower() == 'y':
                return True
            return False

    def show_preview(self):
        """ Function that displays a table with the todo tasks written"""
        formatted_date = self.creation_date.strftime('%m-%d-%Y')
        self.console.rule('Preview', style='purple')
        table = Table(box=box.SIMPLE_HEAD)
        table.add_column('Todo Task')
        table.add_column('Creation Date', justify='center', style='yellow')
        if isinstance(self.todo_task, List):
            for task in self.todo_task:
                table.add_row(task, formatted_date)
        elif isinstance(self.todo_task, str):
            table.add_row(self.todo_task, formatted_date)
        self.console.print(table, justify='center')
        if self._ask_confirmation():
            self.save_todo()


class SearchTodo:

    def __init__(self, args):
        """ SearchTodo Constructor """
        self.console = Console()
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        self.search_date = dates_to_search(args)
        self.search_text = ' '.join(args.text)

        if args_needed_empty(args):
            root = ImpPyCUI(3, 3)
            SearchTodoTUI.set_root(root)
            root.start()
        else:
            self.search_todo()

    @classmethod
    def set_args(cls, args):
        return cls(args)

    def sql_query(self):
        base_sql = f'SELECT {todo.COLUMN_TODO_CONTENT},{todo.COLUMN_TODO_STATUS} from {todo.TABLE_NAME}'
        if self.search_date:
            base_sql = add_conditions_sql(base_sql, f'{todo.COLUMN_TODO_CREATION} like date("{self.search_date}")')
        if self.search_text:
            base_sql = add_conditions_sql(base_sql, f'{todo.COLUMN_TODO_CONTENT} LIKE "%{self.search_text}%"', 'AND')
        query = self.cursor.execute(base_sql)
        
        return query.fetchall()

    def search_todo(self):
        """ Function that displays a table with the tasks searched """
        table = Table()
        table.add_column('Tasks')
        table.add_column('Creation Date', justify='center', style='yellow')

        for task in self.sql_query():
            #formatted_text = self.search_date.strftime('%m-%d-%Y')
            table.add_row(task[0], 'formatted_text')
        self.console.print(table, justify='center')
        # self.console.rule(self.search_date.strftime('%m-%d-%Y'), style='purple')
        # self.db.close()

# select * from cn_todos where cn_todo_creation like date('2020-08-17');
