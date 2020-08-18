from rich import box
from yaspin import yaspin
from rich.table import Table
from datetime import datetime
from rich.console import Console
from prompt_toolkit.styles import Style
from typing import List, Union, overload
from prompt_toolkit import HTML, print_formatted_text

import codenotes.db.utilities.todo as todo
from codenotes.tui import AddTodoTUI, ImpPyCUI
from codenotes.db.connection import SQLiteConnection


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
        self.print = print_formatted_text  # Print use for prompt toolkit package
        self.print_style = Style.from_dict({  # Style use for prints related with saving process
            'msg': '#d898ed bold',
            'task-txt': '#616161 italic'
        })

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
        with yaspin(text='Saving todo tasks', color='yellow') as spinner:   # TODO:THIS COULD BE TRANSFORM INTO FUNCTION
            if isinstance(self.todo_task, List):
                for task in self.todo_task:
                    spinner.hide()
                    values = (task, creation_date)
                    self.cursor.execute(sql, values)
                    self.db.conn.commit()
                    self.print(HTML(
                       u'<b>></b><msg>Todo task saved: </msg><task-txt>{}</task-txt>'.format(task[:30])
                    ), style=self.print_style)
                    spinner.show()

            elif isinstance(self.todo_task, str):
                spinner.hide()
                values = (self.todo_task, creation_date)
                self.cursor.execute(sql, values)
                self.db.conn.commit()
                self.print(HTML(
                    u'<b>></b><msg>Todo task saved: </msg><task-txt>{}</task-txt>'.format(self.todo_task[:30])
                ), style=self.print_style)
                spinner.show()
            spinner.ok("✔")  # TODO: WHEN TASK PASSED IS ;, DISPLAY 'NOT SAVED TASKS'
        self.cursor.close()
        self.db.conn.close()

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
        pass

    @classmethod
    def set_args(cls, args):
        return cls(args)
