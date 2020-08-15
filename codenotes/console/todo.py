from rich.console import Console
from rich.table import Table
from datetime import datetime
from typing import List, Union, overload

from codenotes.db.connection import SQLiteConnection
import codenotes.db.utilities.todo as todo


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
    todo_task_list : List[str]
        List of texts of task joined and stripped
    """
    todo_text = ' '.join(text)
    if ';' in todo_text:
        todo_task_list = []
        for todo_tasks in todo_text.split(';'):
            todo_task_list.append(todo_tasks.strip())  # "Trim"
        return todo_task_list
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
            pass

    @classmethod
    def set_args(cls, args):
        return cls(args)

    def save_todo(self):
        creation_date = datetime.now().date()
        sql = f'INSERT INTO {todo.TABLE_NAME} ({todo.COLUMN_TODO_CONTENT},{todo.COLUMN_TODO_CREATION}) VALUES (?,?);'
        if isinstance(self.todo_task, List):
            values = []
            for sql_value in self.todo_task:
                values.append((sql_value, creation_date))

            self.cursor.executemany(sql, values)
            self.db.conn.commit()
        elif isinstance(self.todo_task, str):
            values = (self.todo_task, creation_date)
            self.cursor.execute(sql, values)
            self.db.conn.commit()

    def _ask_confirmation(self) -> bool:
        answer = self.console.input('Do you want to save them?')
        while len(answer) > 0 and answer.lower() != 'n' and answer.lower() != 'y':
            answer = self.console.input('Do you want to save them?(y/n):')
        else:
            if answer.lower() == 'y':
                return True
            return False

    def show_preview(self):
        formatted_date = self.creation_date.strftime('%m-%d-%Y')
        table = Table()
        table.add_column('Todo Task')
        table.add_column('Creation Date')
        if isinstance(self.todo_task, List):
            for task in self.todo_task:
                table.add_row(task, formatted_date)
        elif isinstance(self.todo_task, str):
            table.add_row(self.todo_task, formatted_date)
        self.console.print(table)
        if self._ask_confirmation():
            self.save_todo()


class SearchTodo:

    def __init__(self):
        pass
