from rich.console import Console
from datetime import datetime
from typing import List, overload

from codenotes.db.connection import SQLiteConnection


class AddTodo:

    def __init__(self, args):
        """ Constructor fro AddTodo class """
        self.console = Console()
        self.db = SQLiteConnection()
        self.date = datetime.now().date()

        if args.text:
            self.todo_text = self.generate_todo_text(args.text)
        else:
            pass

    def save_todo(self):
        pass

    @overload
    def generate_todo_text(self, text: str) -> List[str]: ...

    def generate_todo_text(self, text: str) -> str:
        todo_text = ' '.join(text)
        if ';' in todo_text:
            todo_task_list = []
            for todo_tasks in todo_text.split(';'):
                todo_task_list.append(todo_tasks.strip())
            return todo_task_list
        else:
            return todo_text


class SearchTodo:

    def __init__(self):
        pass
