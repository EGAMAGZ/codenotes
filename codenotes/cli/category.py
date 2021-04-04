from typing import Union, final
from argparse import Namespace

from rich import box
from rich.console import Console
from rich.table import Table

import codenotes.db.utilities.tasks_categories as task_categories
import codenotes.db.utilities.notes_categories as notes_categories
from codenotes.cli import PrintFormatted
from codenotes.util.text import format_list_text
from codenotes.db.connection import SQLiteConnection
from codenotes.util.args import create_category_args_empty


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

        if create_category_args_empty(args):
            try:
                self.category = format_list_text(args.text)
                self.__get_category_table(args)

                if args.preview:
                    self._show_preview()

                else:
                    self.save_category()

            except KeyboardInterrupt:
                self.console.print('[bold yellow]\nCorrectly Cancelled[/bold yellow]')
        else:
            print("ERROR")

    @classmethod
    def set_args(cls, args: Namespace) -> None:
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

        with self.console.status('[bold yellow]Saving Tasks...') as status:
            if isinstance(self.category, list):
                for category in self.category:
                    if not self.category_exists(category):
                        values = (category,)
                        self.db.exec_sql(sql, values)

                        PrintFormatted.print_category_creation(category)
                    else:
                        PrintFormatted.custom_print(f'❌ [bold red]"{category}"[/bold] already exists')

            elif isinstance(self.category, str):
                if not self.category_exists(self.category):
                    values = (self.category,)
                    self.db.exec_sql(sql, values)

                    PrintFormatted.print_category_creation(self.category)
                else:
                    PrintFormatted.custom_print(f'❌ [bold red]"{self.category}"[/bold] already exists')
            
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
