from rich.console import Console
from datetime import datetime
from typing import List, Union, overload

from codenotes.db.connection import SQLiteConnection
import codenotes.db.utilities.todo as todo


@overload
def format_todo_text(text: str) -> List[str]: ...


@overload
def format_todo_text(text: str) -> str: ...


def format_todo_text(text: str) -> Union[List[str], str]:
    todo_text = ' '.join(text)
    if ';' in todo_text:
        todo_task_list = []
        for todo_tasks in todo_text.split(';'):
            todo_task_list.append(todo_tasks.strip())
        return todo_task_list
    else:
        return todo_text


class AddTodo:

    def __init__(self, args):
        """ Constructor fro AddTodo class """
        self.console = Console()
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        self.date = datetime.now().date()

        if args.text:
            self.todo_task = format_todo_text(args.text)
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

            self.cursor.execute(sql, values)
            self.db.conn.commit()
        elif isinstance(self.todo_task, str):
            values = (self.todo_task, creation_date)
            self.cursor.execute(sql, values)
            self.db.conn.commit()

    def show_preview(self):
        pass


class SearchTodo:

    def __init__(self):
        pass
