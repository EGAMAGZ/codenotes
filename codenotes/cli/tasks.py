from argparse import Namespace
from datetime import date, datetime
from typing import Any, Optional, Union, final

from rich import box
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich.tree import Tree

import codenotes.db.utilities.tasks as tasks
import codenotes.db.utilities.tasks_categories as categories
import codenotes.util.help as help_text
from codenotes.abstract import CreateABC, SearchABC
from codenotes.cli import PrintFormatted
from codenotes.db.connection import SQLiteConnection
from codenotes.exceptions import CategoryNotExistsError, MissingArgsException
from codenotes.util.args import (date_args_empty, dates_to_search,
                                 format_argument_text)
from codenotes.util.sql import add_conditions_sql
from codenotes.util.text import format_list_text, status_text


def sorter(query: tuple) -> Any:
    """Function used to get the key that will be used in the built-in function sorted()

    Parameters
    ----------
    query: tuple
        Row from the query done to the database, which contains the variables that will be used to sort the query

    Returns
    -------
    key: Any
        Returns the key that will be used
    """
    return query[3]


def create_args_empty(args: Namespace) -> bool:
    """Functions that checks if the arguments required to create a new task are empty

    Parameters
    ----------
    args: Namespace
        Arguments capture with argparse

    Returns
    -------
    empty: bool
        Boolean value that indicates if the arguments required for a task are empty
    """
    args_needed = [args.text, args.category]

    if any(args_needed):
        return False
    return True


@final
class CreateTask(CreateABC):
    """Class to create new tasks and categories in the database

    This class only has the purpose to create and display the preview of tasks, also create new categories and save
    tasks in it. The arguments that will be used to create it are the task content and optionally a category

    Attributes
    ----------
    category_id: int
        Category Id where the note will be stored (Default 1)

    category_name: str
        Category name where the note will be stored (Default 'TODO Task')

    creation_date: date
        Date of the creation of the note (Today date)

    task: Union[list[str], str]
        Task or list of task that will be store in database

    console: Console
        (Rich) Console for beatiful printting

    db: SQLiteConnection
        Connection with the dabatase
    """

    category_id: int = 1
    category_name: str = "TODO Task"
    creation_date: date
    task: Union[list[str], str]
    console: Console
    db: SQLiteConnection

    def __init__(self, args: Namespace) -> None:
        """Constructor fro AddTask class

        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        self.console = Console()
        self.db = SQLiteConnection()
        self.creation_date = datetime.now().date()

        try:
            if create_args_empty(args):
                raise MissingArgsException

            if args.category:
                # Will create a new category if not exists
                self.category_name = format_argument_text(args.category)
                self.__save_category()

            if args.text:
                self.task = format_list_text(args.text)

                if args.preview:
                    self.show_preview()
                else:
                    self.save()

        except KeyboardInterrupt:
            PrintFormatted.interruption()

        except MissingArgsException:
            PrintFormatted.print_help(help_text.ADD_TASK_USAGE_TEXT)

    @classmethod
    def set_args(cls, args: Namespace) -> None:
        """Set args and initialize class

        Parameters
        ----------
        args: NameSpace
            Arguments of argparse
        """
        cls(args)

    def __save_category(self) -> None:
        """Creates and saves a new category if not exists

        When the task(s) is going to be saved and is created a new category, it will set the id of this new one and
        store the task(s) in this created category
        """
        if len(self.category_name) <= 30:
            if self.category_exists(self.category_name):

                custom_theme = Theme({"msg": "#31f55f bold", "name": "#616161 italic"})
                PrintFormatted.custom_print(
                    f"[msg]Category selected:[/msg][name]{self.category_name}[/name]",
                    custom_theme,
                )
            else:

                sql = f"INSERT INTO {categories.TABLE_NAME} ({categories.COLUMN_NAME}) VALUES (?)"
                cursor = self.db.exec_sql(sql, (self.category_name,))

                self.category_id = cursor.lastrowid

                self.db.commit()
                PrintFormatted.print_category_creation(self.category_name)
        else:
            self._ask_category()

    def _ask_category(self) -> None:
        """Function that asks to the user to introduce different category name"""

        text = "⚠️[yellow]Category name is too long (Max. 30 characters).[/yellow]Write another name:"
        self.category_name = self.console.input(text).strip()

        while len(self.category_name) == 0 or len(self.category_name) > 30:
            self.category_name = self.console.input(text).strip()
        else:
            self.__save_category()

    def category_exists(self, category_name: str) -> bool:
        """Checks if the typed category exists

        Parameters
        ----------
        category_name: str
            Name of the category which will be verified if it exists

        Returns
        -------
        exists: bool
            Boolean value flag if the category already exists
        """
        sql = (
            f"SELECT {categories.COLUMN_ID} FROM {categories.TABLE_NAME} WHERE "
            f"{categories.COLUMN_NAME} = '{category_name}'"
        )
        query = self.db.exec_sql(sql)
        categories_list: list[tuple] = query.fetchall()

        if categories_list:  # categories_list == (id,)
            self.category_id = categories_list[0][0]
            return True
        return False

    def show_preview(self) -> None:
        """Method that displays a table with the tasks that will be stored"""
        formatted_date = self.creation_date.strftime("%Y-%m-%d")

        self.console.rule("Preview", style="purple")

        table = Table(box=box.ROUNDED)
        table.add_column("Task", overflow="fold")
        table.add_column("Creation Date", justify="center", style="yellow")

        if isinstance(self.task, list):
            for task in self.task:
                table.add_row(task, formatted_date)
        elif isinstance(self.task, str):
            table.add_row(self.task, formatted_date)

        self.console.print(table, justify="center")

        if PrintFormatted.ask_confirmation(
            "[yellow]Do you want to save them?(y/n):[/yellow]"
        ):
            self.save()

    def save(self) -> None:
        """Stores the task(s) in the database"""

        sql = (
            f"INSERT INTO {tasks.TABLE_NAME} ({tasks.COLUMN_CONTENT},{tasks.COLUMN_CREATION}, "
            f"{tasks.COLUMN_CATEGORY}) VALUES (?,?,?);"
        )

        with self.console.status("[bold yellow]Saving Tasks...") as status:
            if isinstance(self.task, list):
                for task in self.task:
                    values = (task, self.creation_date, self.category_id)
                    self.db.exec_sql(sql, values)

                    PrintFormatted.print_content_storage(task, self.category_name)

            elif isinstance(self.task, str):
                values = (self.task, self.creation_date, self.category_id)
                self.db.exec_sql(sql, values)

                PrintFormatted.print_content_storage(self.task, self.category_name)

            if self.task:
                self.console.print("[bold green]✔️Task Saved")
            else:
                self.console.print("[bold red] 💥 No Task Saved")

            status.stop()

        self.db.commit()
        self.db.close()


@final
class SearchTask(SearchABC):
    """Class to search and display tasks in the database

    This class only has the purpose to search and display the tasks. The arguments that will be used to filter the
    search are text and date(s). The SQL statement for the query will be dinamycally generate depending on the captured
    (and previously mentioned arguments).

    Attributes
    ----------
    console: Console
        (Rich) Console for beautiful printting

    db: SQLiteConnection
        Connection with the dabatase

    search_date: Union[date, list[date]]
        Date or list of dates to search the tasks

    search_text: str
        Text to search in the content of the tasks

    search_category: str
        Name of the category where the notes will be searched

    search_category_id : int
        Id of the category where the notes will be searched
    """

    console: Console
    db: SQLiteConnection
    search_date: Optional[Union[date, list[date]]]
    search_text: str
    search_category: str = None
    search_category_id: int = None

    def __init__(self, args: Namespace) -> None:
        """SearchTask Constructor

        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        self.console = Console()
        self.db = SQLiteConnection()
        self.search_date = dates_to_search(args)
        self.search_text = format_argument_text(args.text)

        try:
            if date_args_empty(args):
                raise MissingArgsException

            if args.category:
                self.search_category = format_argument_text(args.category)

            self.search()

        except CategoryNotExistsError:
            PrintFormatted.custom_print(
                f'[red][bold]❌"{self.search_category}"[/bold] category does not exists[/red]'
            )

        except KeyboardInterrupt:
            PrintFormatted.interruption()

        except MissingArgsException:
            PrintFormatted.print_help(help_text.SEARCH_USAGE_TEXT)

    @classmethod
    def set_args(cls, args: Namespace) -> None:
        """Class method that initializes the class and automatically will do the search

        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        cls(args)

    def category_exists(self, category_name: str) -> bool:
        """Checks if the typed category exists

        Parameters
        ----------
        category_name: str
            Name of the category which will be verified if it exists

        Returns
        -------
        exists: bool
            Boolean value flag if the category already exists
        """
        sql = (
            f"SELECT {categories.COLUMN_ID} FROM {categories.TABLE_NAME} WHERE "
            f"{categories.COLUMN_NAME} = '{category_name}'"
        )
        query = self.db.exec_sql(sql)
        categories_list: list[tuple] = query.fetchall()

        if categories_list:  # categories_list == (id,)
            self.search_category_id = categories_list[0][0]
            return True
        return False

    def sql_query(self) -> list[tuple]:
        """Makes a query of related information of tasks, and also adds more statements to the main sql
        sql

        Returns
        -------
        query: list[tuple]
            Query done to the database
        """
        sql = (
            f"SELECT {tasks.TABLE_NAME}.{tasks.COLUMN_CONTENT},{tasks.TABLE_NAME}.{tasks.COLUMN_STATUS}, "
            f"{tasks.TABLE_NAME}.{tasks.COLUMN_CREATION}, "
            f"{categories.TABLE_NAME}.{categories.COLUMN_NAME} FROM {tasks.TABLE_NAME} INNER JOIN "
            f"{categories.TABLE_NAME} ON {tasks.TABLE_NAME}.{tasks.COLUMN_CATEGORY} = "
            f"{categories.TABLE_NAME}.{categories.COLUMN_ID}"
        )

        if self.search_date:
            if isinstance(self.search_date, date):
                sql = add_conditions_sql(
                    sql, f'{tasks.COLUMN_CREATION} LIKE date("{self.search_date}")'
                )

            elif isinstance(self.search_date, list):
                first_day, last_day = self.search_date
                sql = add_conditions_sql(
                    sql,
                    f'{tasks.COLUMN_CREATION} BETWEEN date("{first_day}") '
                    f'AND date("{last_day}")',
                )
        if self.search_text:
            sql = add_conditions_sql(
                sql, f'{tasks.COLUMN_CONTENT} LIKE "%{self.search_text}%"', "AND"
            )

        if self.search_category:
            if not self.category_exists(self.search_category):
                raise CategoryNotExistsError
            sql = add_conditions_sql(
                sql, f"{tasks.COLUMN_CATEGORY} = {self.search_category_id}", "AND"
            )

        query = self.db.exec_sql(sql)

        return query.fetchall()

    def search(self) -> None:
        """Displays a tree with tables as child nodes with the tasks searched"""
        root = Tree("📒[bold blue] List of Tasks  Found")
        query = self.sql_query()

        if query:  # When the list is not empty
            table = Table()
            table.add_column("Tasks")
            table.add_column("Status")
            table.add_column("Category")
            table.add_column("Creation Date", justify="center", style="yellow")

            tasks_sorted = sorted(query, key=sorter)
            actual_task = tasks_sorted[0]
            actual_category = actual_task[3]

            child_branch = root.add(f":file_folder:[#d898ed]{actual_category}")

            for actual_task in tasks_sorted:
                if actual_task[3] != actual_category:
                    child_branch.add(table)

                    table = Table()
                    table.add_column("Tasks")
                    table.add_column("Status")
                    table.add_column("Category")
                    table.add_column("Creation Date", justify="center", style="yellow")

                    actual_category = actual_task[3]
                    child_branch = root.add(f":file_folder: [#d898ed]{actual_category}")

                table.add_row(
                    actual_task[0],
                    status_text(actual_task[1]),
                    actual_task[3],
                    actual_task[2],
                )
            else:
                child_branch.add(table)

        else:
            root.add("[red]❌ No Task Found")
        self.console.print(root)
        # self.db.close() # FIXME: DATABASE DONT CLOSE CORRECTLY


@final
class DeleteTask:
    pass
