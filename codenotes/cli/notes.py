from argparse import Namespace
from datetime import datetime, date
from typing import final, Union, Any

from rich.tree import Tree
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console

import codenotes.db.utilities.notes as notes
import codenotes.db.utilities.notes_categories as categories
from codenotes.cli import PrintFormatted
from codenotes.db.connection import SQLiteConnection
from codenotes.util.sql import add_conditions_sql
from codenotes.util.args import date_args_empty, dates_to_search, format_argument_text, add_note_args_empty


def sorter(query: tuple)-> Any:
    """ Function used to get the key that will be used in the built-in function sorted()

    Parameters
    ----------
    query: tuple
        Row from the query done to the database, which contains the variables that will be used to sort the query

    Returns
    -------
    key: Any
        Returns the key that will be used
    """
    return query[2]


@final
class AddNote:

    category_id: int = 1 # Default Id of 'General' category
    category_name: str = 'General' # Default category name
    note_title: str = None
    note_text: str = None
    creation_date: date # Today's date

    def __init__(self, args: Namespace) -> None:
        """ Constructor of AddTask class 
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        self.console = Console()
        self.db = SQLiteConnection()
        self.creation_date = datetime.now().date()

        if not add_note_args_empty(args):
            try:
                if args.new_category:
                    self.category_name = format_argument_text(args.new_category)
                    self.save_category()

                if args.text or args.title:
                    self._set_note_content(args)

                    if args.preview:
                        self._show_preview()

                    else:
                        self.save_note()
            except KeyboardInterrupt:
                self.console.print('[bold yellow]\nCorrectly Cancelled[/bold yellow]')


    @classmethod
    def set_args(cls, args: Namespace) -> None:
        """ Set args and initialize class
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        cls(args)

    def save_category(self) -> None:
        """ Creates and saves a new category"""
        if len(self.category_name) <= 30: # Category name can't be longer than 30 characters
            sql = f'INSERT INTO {categories.TABLE_NAME} ({categories.COLUMN_CATEGORY_NAME}) VALUES (?)'
            cursor = self.db.exec_sql(sql, (self.category_name,))

            self.category_id = cursor.lastrowid

            self.db.commit()
            PrintFormatted.print_category_creation(self.category_name)
        else:
            self._ask_category()

    def save_note(self) -> None:
        """ Saves the note created in the database and setting category to store """
        sql = f'INSERT INTO {notes.TABLE_NAME} ({notes.COLUMN_NOTE_TITLE}, {notes.COLUMN_NOTE_CONTENT}, ' \
              f'{notes.COLUMN_NOTE_CATEGORY}, {notes.COLUMN_NOTE_CREATION}) VALUES (?,?,?,?);'

        with self.console.status('[bold yellow]Saving Note') as status:
            values = (self.note_title, self.note_text, self.category_id, self.creation_date)
            self.db.exec_sql(sql, values)

            PrintFormatted.print_content_storage(self.note_title, self.category_name)

            self.console.print('[bold green]✔️ Note Correctly Saved')
            status.stop()

        self.db.commit()
        self.db.close()

    def _set_note_content(self, args) -> None:

        if args.text:
            self.note_text = format_argument_text(args.text)

            if not args.title:
                self.note_title = self.note_text[:30]
            else:
                self.note_title = format_argument_text(args.title)
                self._check_note_title()
        else:
            if args.title:
                self.note_title = format_argument_text(args.title)
                self._check_note_title()

    def _ask_category(self) -> None:
        """ Function that asks to the user to introduce different category name """

        text = '⚠️[yellow]Category name is too long (Max. 30).[/yellow] Write another name:'
        self.category_name = self.console.input(text).strip()

        while len(self.category_name) == 0 or len(self.category_name) > 30:
            self.category_name = self.console.input(text).strip()
        else:
            self.save_category()

    def _check_note_title(self) -> None:
        if len(self.note_title) > 30:
            text = '⚠️[yellow]Note title is too long(Max. 30).[/yellow] Write another title:'
            self.note_title = self.console.input(text).strip()

            while len(self.note_title) == 0 or len(self.note_title) > 30:
                self.note_text = self.console.input(text).strip()

    def _show_preview(self) -> None:
        """ Method that displays a panel with the title and text of the note """

        self.console.rule('Preview', style='purple')
        self.console.print(
                Panel(self.note_text if self.note_text else '[red bold]Empty note[/red bold]', title=self.note_title)
            )

        if PrintFormatted.ask_confirmation(
                '[yellow]Do you want to save it?(y/n):[/yellow]'
            ):
            self.save_note()


@final
class SearchNote:
    """ Class to search and display notes in the database

    This class only has the purpouse to search and display the notes. The arguments that will be used to filter the
    search are text and date(s). The SQL statement for the query will be dinamycally generate depending on the captured
    (and previously mentioned arguments).

    Attributes
    ----------
    console: Console
        (Rich) Console for beatiful printting

    db: SQLiteConnection
        Connection with the dabatase

    search_date: Union[date, list[date]]
        Date or list of dates to search the notes

    search_text: str
        Text to search in the title of the notes
    """

    console: Console
    db: SQLiteConnection
    search_date: Union[list[date], date]
    search_text: str

    def __init__(self, args: Namespace) -> None:
        """ SearchNote constructor

        Parameters
        ----------
        args: Namespace
            Arguments of argparse
        """
        self.console = Console()
        self.db  = SQLiteConnection()
        self.search_date = dates_to_search(args)
        self.search_text = format_argument_text(args.text)

        if not date_args_empty(args):
            self.search_note()

    @classmethod
    def set_args(cls, args: Namespace) -> None:
        """ Class method that initializes the class and automatically will do the search

        Parameters
        ----------
        args: Namespace
            Arguments of argparse
        """
        cls(args)

    def sql_query(self) -> list[tuple]:
        """ Function that makes a query of related information of notes, and also adds more statements to the main sql
        
        Returns
        -------
        query: list[tuple]
            Query done to the database
        """
        sql = f"SELECT {notes.TABLE_NAME}.{notes.COLUMN_NOTE_TITLE}, {notes.TABLE_NAME}.{notes.COLUMN_NOTE_CONTENT}, " \
            f"{categories.TABLE_NAME}.{categories.COLUMN_CATEGORY_NAME}, " \
            f"{notes.TABLE_NAME}.{notes.COLUMN_NOTE_README}, {notes.TABLE_NAME}.{notes.COLUMN_NOTE_CREATION} FROM " \
            f"{notes.TABLE_NAME} INNER JOIN {categories.TABLE_NAME} ON " \
            f"{notes.TABLE_NAME}.{notes.COLUMN_NOTE_CATEGORY} = {categories.TABLE_NAME}.{categories.COLUMN_CATEGORY_ID}"

        if self.search_date:
            if isinstance(self.search_date, date):
                sql = add_conditions_sql(sql, f'{notes.COLUMN_NOTE_CREATION} LIKE date("{self.search_date}")')

            elif isinstance(self.search_date, list):
                first_day, last_day = self.search_date
                sql = add_conditions_sql(sql, f'{notes.COLUMN_NOTE_CREATION} BETWEEN date("{first_day}") '
                                              f'AND date("{last_day}")')
        if self.search_text:
            sql = add_conditions_sql(sql, f'{notes.COLUMN_NOTE_TITLE} LIKE "%{self.search_text}%"', 'AND')

        query = self.db.exec_sql(sql)

        return query.fetchall()

    def search_note(self) -> None:
        """ Function that displays a tree with Panels as child nodes with the notes searched """
        root = Tree('📒[bold #964B00] List of Notes Found')
        query = self.sql_query()

        if query:
            notes_sorted = sorted(query, key=sorter)
            actual_note = notes_sorted[0]
            actual_category = actual_note[2]

            child_node = root.add(f':file_folder:[#d898ed]{actual_category}')
            for actual_note in notes_sorted:
                if actual_note[2] != actual_category:

                    actual_category = actual_note[2]
                    child_node = root.add(f':file_folder: [#d898ed]{actual_category}')
                
                if actual_note[3] == 0:
                    child_node.add(
                            Panel(
                                actual_note[1] if actual_note[1] else '[red bold]Empty note[/red bold]',
                                title=f'{actual_note[0]} {actual_note[4]}'
                                )
                        )
                else:  # actual_note[3] == 1
                    markdown = Markdown( actual_note[1] if actual_note[1] else '# Note Empty')
                    child_node.add(
                            Panel(
                                markdown,
                                title=f'{actual_note[0]} {actual_note[4]}'
                                )
                        )
            
        else:
            root.add('[red]❌ No Note Found')
        self.console.print(root)
        
        # self.db.close() # FIXME: DATABASE DONT CLOSE CORRECTLY
