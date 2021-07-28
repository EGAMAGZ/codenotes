from argparse import Namespace
import logging
from typing import Final, Union, final

from rich import box, table
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

import codenotes.db.utilities.notes_categories as notes_categories
import codenotes.db.utilities.tasks_categories as task_categories
from codenotes.cli import PrintFormatted
from codenotes.db.connection import SQLiteConnection
from codenotes.exceptions import MissingArgsException
from codenotes.util.args import format_argument_text
from codenotes.util.sql import add_conditions_sql
from codenotes.util.text import format_list_text


def create_args_empty(args: Namespace) -> bool:
    """ Check if arguments required to select an annotation type

    Parameters
    ----------
    args: Namespace
        Arguments capture

    Returns
    -------
    empty : bool
        Return boolean value if any args are empty
    """
    args_needed = [
        args.note,
        args.task,
        args.text
    ]
    if any(args_needed):
        return False
    return True


def search_args_empty(args: Namespace) -> bool:

    args_needed = [
        args.note,
        args.task,
        args.all    
    ]
    if any(args_needed):
        return False
    return True


@final
class CreateCategory:

    category: Union[list[str], str]
    category_table_name: str
    category_id_column: str
    category_name_column: str
    console: Console
    db: SQLiteConnection

    def __init__(self, args: Namespace) -> None:
        self.console = Console()
        self.db = SQLiteConnection()

        try:
            if create_args_empty(args):
                raise MissingArgsException

            self.category = format_list_text(args.text)
            self.__get_category_table(args)

            if args.preview:
                self._show_preview()

            else:
                self.save_category()

        except KeyboardInterrupt:
            PrintFormatted.interruption()
        
        except MissingArgsException:
            print("ERROR")

    @classmethod
    def set_args(cls, args: Namespace) -> None:
        """ Class method that initializes the class and automatically will do the search
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        cls(args)

    def category_exists(self, category_name: str) -> bool:
        """ Checks if the typed category exists

        Returns
        -------
        exists: bool
            Boolean value flag if the category already exists
        """
        sql = f"SELECT {self.category_id_column} FROM {self.category_table_name} WHERE {self.category_name_column} = '{category_name}'"
        query = self.db.exec_sql(sql)
        categories_list: list[tuple] = query.fetchall()

        if categories_list: # categories_list == []
            return True
        return False

    def save_category(self) -> None:
        sql = f'INSERT INTO {self.category_table_name} ({self.category_name_column}) VALUES(?)'
        
        with self.console.status('[bold yellow]Saving Category...') as status:
            if isinstance(self.category, list):
                # TODO: Validate if len of the category is 30
                for category in self.category:
                    if not self.category_exists(category):
                        values = (category,)
                        self.db.exec_sql(sql, values)

                        PrintFormatted.print_category_creation(category)

                    else:
                        PrintFormatted.custom_print(f'❌ [bold] [red]"{category}"[/bold] already exists')

            elif isinstance(self.category, str):
                if not self.category_exists(self.category):
                    values = (self.category,)
                    self.db.exec_sql(sql, values)

                    PrintFormatted.print_category_creation(self.category)

                else:
                    PrintFormatted.custom_print(f'❌ [bold] [red]"{self.category}"[/bold] already exists')
            
            if self.category:
                self.console.print('[bold green]✔️ Category Saved')

            else:
                self.console.print('[bold red] 💥 No Category Saved')
            
            status.stop()

        self.db.commit()
        self.db.close()

    def __get_category_table(self, args: Namespace) -> None:
        if args.note:
            self.category_table_name = notes_categories.TABLE_NAME
            self.category_id_column = notes_categories.COLUMN_ID
            self.category_name_column = notes_categories.COLUMN_NAME

        elif args.task:
            self.category_table_name = task_categories.TABLE_NAME
            self.category_id_column = task_categories.COLUMN_ID
            self.category_name_column = task_categories.COLUMN_NAME

    def _show_preview(self) -> None:
        table = Table(box=box.ROUNDED)
        table.add_column('Categories')

        if isinstance(self.category, list):
            for category in self.category:
                table.add_row(category)

        elif isinstance(self.category, str):
            table.add_row(self.category)

        self.console.print(table, justify='center')

        if PrintFormatted.ask_confirmation(
                '[yellow]Do you want to save them?(y/n):[/yellow]'
            ):
            self.save_category()


class SearchCategory:

    ANNOTATIONS_TYPES: Final[list[str]] = ['Tasks', 'Notes']
    
    console: Console
    db: SQLiteConnection
    search_category: str
    category_table_name: Union[list[str], str]
    category_id_column: Union[list[str], str]
    category_name_column: Union[list[str], str]

    def __init__(self, args: Namespace) -> None:
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
        """ Class method that initializes the class and automatically will do the search

        Parameters
        ----------
        args: Namespace
            Arguments of argparse
        """
        cls(args)

    def __get_category_table(self, args: Namespace) -> None:
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
                    notes_categories.TABLE_NAME
                ]
            self.category_id_column = [
                    task_categories.COLUMN_ID,
                    notes_categories.COLUMN_ID
                ]
            self.category_name_column = [
                    task_categories.COLUMN_NAME,
                    notes_categories.COLUMN_NAME
                ]

    def sql_query(self) -> list[list[tuple]]:
        query_list = []

        if isinstance(self.category_table_name, str):
            sql = f'SELECT {self.category_name_column} FROM {self.category_table_name}'

            if self.search_category:
                sql = add_conditions_sql(sql, f'{self.category_name_column} LIKE "%{self.search_category}%"')

            query_list.append(
                self.db.exec_sql(sql).fetchall()
            )

        elif isinstance(self.category_table_name, list):
            for i in range(len(self.ANNOTATIONS_TYPES)):
                sql = f'SELECT {self.category_name_column[i]} FROM {self.category_table_name[i]}'

                if self.search_category:
                    sql = add_conditions_sql(sql, f'{self.category_name_column[i]} LIKE "%{self.search_category}%"')

                query_list.append(
                    self.db.exec_sql(sql).fetchall()
                )

        return query_list

        
    def search(self) -> None:
        root = Tree('📒[bold blue] List of Categories Found')
        query = self.sql_query()

        if query:
            i = 0
            for categories_list in query:
                child_branch = root.add(f'📒[#d898ed]{self.ANNOTATIONS_TYPES[i]}')

                table = Table()
                table.add_column('Name')

                for categories in categories_list:
                    table.add_row(categories[0])
                
                child_branch.add(table)
                i += 1

        else:
            root.add('[red]❌ No Category Found')
        self.console.print(root)


class DeleteCategory:
    pass
