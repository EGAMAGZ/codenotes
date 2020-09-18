from rich.console import Console

from codenotes.cli import format_argument_text
from codenotes.db.connection import SQLiteConnection
import codenotes.db.utilities.tasks_categories as categories


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

        if add_note_args_empty(args):
            pass
        else:
            if args.new_category:
                self.category_name = format_argument_text(args.new_category)
                self.save_category()

            if args.text:
                self.note_text = ' '.join(args.text)
                if not args.title:
                    self.note_title = self.note_text[:30]
                else:
                    self.check_title()
            else:
                self.check_title()

    @classmethod
    def set_args(cls, args):
        """ Set args and initialize class
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        return cls(args)

    def check_title(self):
        if len(self.note_text) > 30:
            pass
        else:
            pass

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
        pass

    def _ask_category(self):
        """ Function that asks to the user to introduce different category name """

        text = 'Category name is too long(Max. 30). Write another name:'
        self.category_name = self.console.input(text).strip()

        while len(self.category_name) == 0 or len(self.category_name) > 30:
            self.category_name = self.console.input(text).strip()
        else:
            self.save_category()
