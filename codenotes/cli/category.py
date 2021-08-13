from argparse import Namespace
from typing import Final, Union, final

from rich import box
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

import codenotes.db.utilities.notes_categories as notes_categories
import codenotes.db.utilities.tasks_categories as task_categories
from codenotes.abstract import CreateABC, DeleteABC, SearchABC
from codenotes.cli import PrintFormatted
from codenotes.db.connection import SQLiteConnection
from codenotes.exceptions import MissingArgsException
from codenotes.util.args import format_argument_text
from codenotes.util.sql import add_conditions_sql
from codenotes.util.text import format_list_text


def create_args_empty(args: Namespace) -> bool:
    """Checks if arguments required to create a category in a type of annotation are empty

    Parameters
    ----------
    args: Namespace
        Arguments capture

    Returns
    -------
    empty: bool
        Return boolean value if any args are empty
    """
    args_needed = [args.note, args.task]
    if any(args_needed) and args.text:
        return False
    return True


def search_args_empty(args: Namespace) -> bool:
    """Checks if arguments required to search a category in the types of annotations are empty

    Parameters
    ----------
    args: Namespace
        Arguments capture

    Returns
    -------
    empty: bool
        Return boolean value if any args are empty
    """
    args_needed = [args.note, args.task, args.all]
    if any(args_needed):
        return False
    return True


@final
class CreateCategory(CreateABC):
    """Class to create new categories in the database

    This class only hast the purpose to create and display the preview of categories. The arguments that will be used
    to create it are the name of the category and the type of annotation where it wil be created, both required.

    Attributes
    ----------
    category: Union[list[str], str]
        Single or list of category names that will be stored

    category_table_name: str
        Name of the annotation type table where the categories will be stored

    category_id_column: str
        Name of the annotation type id column used to check if a category already exists

    category_name_column: str
        Name of the annotation type name column where the categories will be stored

    console: Console
        (Rich) Console for beatiful printting

    db: SQLiteConnection
        Connection with the dabatase
    """

    category_name: Union[list[str], str]
    category_table_name: str
    category_id_column: str
    category_name_column: str
    console: Console
    db: SQLiteConnection

    def __init__(self, args: Namespace) -> None:
        """CreateCategory Constructor

        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        self.console = Console()
        self.db = SQLiteConnection()

        try:
            if create_args_empty(args):
                raise MissingArgsException

            self.__get_category_table(args)
            self.category_name = format_list_text(args.text)
            self._check_category_name()

            if args.preview:
                self.show_preview()

            else:
                self.save()

        except KeyboardInterrupt:
            PrintFormatted.interruption()

        except MissingArgsException:
            print("ERROR")

    @classmethod
    def set_args(cls, args: Namespace) -> None:
        """Class method that initializes the class and automatically will do the search

        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        cls(args)

    def __get_category_table(self, args: Namespace) -> None:
        """Sets a single or a list of table names and columns to store the category in a type of annation

        Parameters
        ----------
        args: Namespace
            Arguments of argparse
        """
        if args.note:
            self.category_table_name = notes_categories.TABLE_NAME
            self.category_id_column = notes_categories.COLUMN_ID
            self.category_name_column = notes_categories.COLUMN_NAME

        elif args.task:
            self.category_table_name = task_categories.TABLE_NAME
            self.category_id_column = task_categories.COLUMN_ID
            self.category_name_column = task_categories.COLUMN_NAME

    def _check_category_name(self) -> None:
        """Check if the category name can be saved

        The name of the categories can't be longer than 30 characters
        """
        if isinstance(self.category_name, str):
            if len(self.category_name) > 30:
                text = "⚠️[yellow]Category name is too long(Max. 30).[/yellow] Write another title:"
                self.category_name = self.console.input(text).strip()

                while len(self.category_name) == 0 or len(self.category_name) > 30:
                    self.category_name = self.console.input(text).strip()

        elif isinstance(self.category_name, list):
            index = 0
            for category in self.category_name:
                if len(category) > 30:
                    text = f'⚠️[yellow]"{category}" is too long(Max. 30).[/yellow] Write another title:'
                    category = self.console.input(text).strip()

                    while len(category) == 0 or len(category) > 30:
                        category = self.console.input(text).strip()
                    self.category_name[index] = category
                index += 1

    def category_exists(self, category_name: str) -> bool:
        """Checks if the typed category exists

        Returns
        -------
        exists: bool
            Boolean value flag if the category already exists
        """
        sql = (
            f"SELECT {self.category_id_column} FROM {self.category_table_name} WHERE "
            f"{self.category_name_column} = '{category_name}'"
        )
        query = self.db.exec_sql(sql)
        categories_list: list[tuple] = query.fetchall()

        if categories_list:  # categories_list == []
            return True
        return False

    def show_preview(self) -> None:
        """Displays a table with the categories that will be stored"""
        table = Table(box=box.ROUNDED)
        table.add_column("Categories")

        if isinstance(self.category_name, list):
            for category in self.category_name:
                table.add_row(category)

        elif isinstance(self.category_name, str):
            table.add_row(self.category_name)

        self.console.rule("Preview", style="purple")
        self.console.print(table, justify="center")

        if PrintFormatted.ask_confirmation(
            "[yellow]Do you want to save them?(y/n):[/yellow]"
        ):
            self.save()

    def save(self) -> None:
        """Stores the categories in the database"""

        sql = f"INSERT INTO {self.category_table_name} ({self.category_name_column}) VALUES(?)"

        with self.console.status("[bold yellow]Saving Category...") as status:
            if isinstance(self.category_name, list):
                for category in self.category_name:
                    if not self.category_exists(category):
                        values = (category,)
                        self.db.exec_sql(sql, values)

                        PrintFormatted.print_category_creation(category)

                    else:
                        PrintFormatted.custom_print(
                            f'❌ [bold] [red]"{category}"[/bold] already exists'
                        )

            elif isinstance(self.category_name, str):
                if not self.category_exists(self.category_name):
                    values = (self.category_name,)
                    self.db.exec_sql(sql, values)

                    PrintFormatted.print_category_creation(self.category_name)

                else:
                    PrintFormatted.custom_print(
                        f'❌ [bold] [red]"{self.category_name}"[/bold] already exists'
                    )

            if self.category_name:
                self.console.print("[bold green]✔️ Category Saved")

            else:
                self.console.print("[bold red] 💥 No Category Saved")

            status.stop()

        self.db.commit()
        self.db.close()


class SearchCategory(SearchABC):
    """Class to search and display categories in the database

    This class only has the purpose to search and display the categories. The arguments that wil be used to filter the
    search are text and type(s) of annotation. The SQL statement for the query will be dinamycally generate depending
    on the captured (and previously mentioned arguments).

    Attributes
    ----------
    ANNOTATIONS_TYPE: Final[list[str]]
        Contant list with all the types of annotations

    console: Console
        (Rich) Console for beautiful printting

    db: SQLiteConnection
        Connection with the dabatase

    search_category: str
        Name of the category that will be searched in the type of annotations

    category_table_name: str
        Name of the annotation type table where the categories will be searched

    category_id_column: str
        Name of the annotation type id column used to check if a category already exists

    category_name_column: str
        Name of the annotation type name column where the categories will be seached
    """

    ANNOTATIONS_TYPES: Final[list[str]] = ["Tasks", "Notes"]

    console: Console
    db: SQLiteConnection
    search_category: str
    category_table_name: Union[list[str], str]
    category_id_column: Union[list[str], str]
    category_name_column: Union[list[str], str]

    def __init__(self, args: Namespace) -> None:
        """SearchCategory Constructor

        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        self.console = Console()
        self.db = SQLiteConnection()
        try:
            if search_args_empty(args):
                raise MissingArgsException

            self.search_category = format_argument_text(args.text)

            self.__get_category_table(args)

            self.search()

        except KeyboardInterrupt:
            PrintFormatted.interruption()

        except MissingArgsException:
            print("Error")

    @classmethod
    def set_args(cls, args: Namespace) -> None:
        """Class method that initializes the class and automatically will do the search

        Parameters
        ----------
        args: Namespace
            Arguments of argparse
        """
        cls(args)

    def __get_category_table(self, args: Namespace) -> None:
        """Sets a single or a list of table names and columns to search the category in the types of annations

        Parameters
        ----------
        args: Namespace
            Arguments of argparse
        """
        if args.note:
            self.category_table_name = notes_categories.TABLE_NAME
            self.category_id_column = notes_categories.COLUMN_ID
            self.category_name_column = notes_categories.COLUMN_NAME

        elif args.task:
            self.category_table_name = task_categories.TABLE_NAME
            self.category_id_column = task_categories.COLUMN_ID
            self.category_name_column = task_categories.COLUMN_NAME

        elif args.all:
            self.category_table_name = [
                task_categories.TABLE_NAME,
                notes_categories.TABLE_NAME,
            ]
            self.category_id_column = [
                task_categories.COLUMN_ID,
                notes_categories.COLUMN_ID,
            ]
            self.category_name_column = [
                task_categories.COLUMN_NAME,
                notes_categories.COLUMN_NAME,
            ]

    def category_exists(self, category_name: str) -> bool:
        pass

    def sql_query(self) -> list[list[tuple]]:
        """Makes a query of related information of tasks, and also adds more statements to the main sql
        sql

        Returns
        -------
        query: list[list[tuple]]
            Query done to the database
        """
        query_list = []

        if isinstance(self.category_table_name, str):
            sql = f"SELECT {self.category_name_column} FROM {self.category_table_name}"

            if self.search_category:
                sql = add_conditions_sql(
                    sql, f'{self.category_name_column} LIKE "%{self.search_category}%"'
                )

            query_list.append(self.db.exec_sql(sql).fetchall())

        elif isinstance(self.category_table_name, list):
            for i in range(len(self.ANNOTATIONS_TYPES)):
                sql = f"SELECT {self.category_name_column[i]} FROM {self.category_table_name[i]}"

                if self.search_category:
                    sql = add_conditions_sql(
                        sql,
                        f'{self.category_name_column[i]} LIKE "%{self.search_category}%"',
                    )

                query_list.append(self.db.exec_sql(sql).fetchall())

        return query_list

    def search(self) -> None:
        """Displays a tree with tables as child nodes with the categories searched"""
        root = Tree("📒[bold blue] List of Categories Found")
        query = self.sql_query()

        if query:
            index = 0
            for categories_list in query:
                child_branch = root.add(f"📒[#d898ed]{self.ANNOTATIONS_TYPES[index]}")

                table = Table()
                table.add_column("Name")

                for categories in categories_list:
                    table.add_row(categories[0])

                child_branch.add(table)
                index += 1

        else:
            root.add("[red]❌ No Category Found")
        self.console.print(root)


class DeleteCategory(DeleteABC):
    def __init__(self, args: Namespace) -> None:
        pass

    @classmethod
    def set_args(cls, args: Namespace) -> None:
        pass

    def category_exists(self, category_name: str) -> bool:
        pass

    def sql_query(self) -> tuple:
        pass

    def delete(self) -> None:
        pass
