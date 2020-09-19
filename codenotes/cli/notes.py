from datetime import datetime

from rich.console import Console
from yaspin import yaspin

from codenotes.cli import format_argument_text, PrintFormatted
from codenotes.db.connection import SQLiteConnection
import codenotes.db.utilities.tasks_categories as categories
import codenotes.db.utilities.notes as notes


def add_note_args_empty(args) -> bool:
    args_needed = [
        args.title,
        args.new_category,
        args.text
    ]

    if any(args_needed):
        return False
    return True


class AddNotes:

    category_id: int = 1
    category_name: str
    note_title: str
    note_text: str

    def __init__(self, args):
        """ Constructor fro AddTask class 
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        self.console = Console()
        self.db = SQLiteConnection()
        self.cursor = self.db.get_cursor()
        self.creation_date = datetime.now().date()

        if add_note_args_empty(args):
            pass
        else:
            if args.new_category:
                self.category_name = format_argument_text(args.new_category)
                self.save_category()

            if args.text or args.title:

                self._set_note_content(args)

                if args.preview:
                    pass
                else:
                    self.save_note()

            self.save_note()

    @classmethod
    def set_args(cls, args):
        """ Set args and initialize class
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        return cls(args)

    def _check_note_title(self):
        if len(self.note_text) > 30:
            text = ''
            self.note_title = self.console.input(text).strip()

            while len(self.note_title) == 0 or len(self.note_title) > 30:
                self.note_text = self.console.input(text).strip()

    def save_category(self):
        """ Creates and saves a new category"""
        if len(self.category_name) <= 30:
            sql = f'INSERT INTO {categories.TABLE_NAME} ({categories.COLUMN_CATEGORY_NAME}) VALUES (?)'
            self.cursor.execute(sql, (self.category_name,))

            self.category_id = self.cursor.lastrowid

            self.db.commit()

        else:
            self._ask_category()

    def save_note(self):
        sql = f'INSERT INTO {notes.TABLE_NAME} ({notes.COLUMN_NOTE_TITLE}, {notes.COLUMN_NOTE_CONTENT}, ' \
              f'{notes.COLUMN_NOTE_CATEGORY}, {notes.COLUMN_NOTE_CREATION}) VALUES (?,?,?,?);'

        with yaspin(text='Saving Note', color='yellow') as spinner:
            values = (self.note_title, self.note_text, self.category_id, self.creation_date)
            self.cursor.execute(sql, values)
            spinner.hide()
            PrintFormatted.print_note_storage(self.note_title)  # TODO: ADD PRINT FOR EMPTY NOTE TEXT
            spinner.show()

        pass

    def _set_note_content(self, args):
        if args.text:
            self.note_text = format_argument_text(args.text)

            if not args.text:
                self.note_title = self.note_text[:30]
        else:
            self._check_note_title()

    def _ask_category(self):
        """ Function that asks to the user to introduce different category name """

        text = 'Category name is too long(Max. 30). Write another name:'
        self.category_name = self.console.input(text).strip()

        while len(self.category_name) == 0 or len(self.category_name) > 30:
            self.category_name = self.console.input(text).strip()
        else:
            self.save_category()
