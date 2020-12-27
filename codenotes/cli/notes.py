from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from yaspin import yaspin

from codenotes.tui import AddNoteTUI, ImpPyCUI
import codenotes.db.utilities.notes as notes
from codenotes.db.connection import SQLiteConnection
from codenotes.cli import format_argument_text, PrintFormatted
import codenotes.db.utilities.notes_categories as categories


def add_note_args_empty(args) -> bool:
    args_needed = [
        args.title,
        args.new_category,
        args.text
    ]

    if any(args_needed):
        return False
    return True


class AddNote:

    category_id: int = 1
    category_name: str = 'General'
    note_title: str = None
    note_text: str = None

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
            root = ImpPyCUI(5, 4)
            AddNoteTUI.set_root(root)
            root.start()

        else:
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
    def set_args(cls, args):
        """ Set args and initialize class
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        return cls(args)

    def save_category(self):
        """ Creates and saves a new category"""
        if len(self.category_name) <= 30:
            sql = f'INSERT INTO {categories.TABLE_NAME} ({categories.COLUMN_CATEGORY_NAME}) VALUES (?)'
            self.cursor.execute(sql, (self.category_name,))

            self.category_id = self.cursor.lastrowid

            self.db.commit()
            PrintFormatted.print_category_creation(self.category_name)
        else:
            self._ask_category()

    def save_note(self):
        sql = f'INSERT INTO {notes.TABLE_NAME} ({notes.COLUMN_NOTE_TITLE}, {notes.COLUMN_NOTE_CONTENT}, ' \
              f'{notes.COLUMN_NOTE_CATEGORY}, {notes.COLUMN_NOTE_CREATION}) VALUES (?,?,?,?);'

        with yaspin(text='Saving Note', color='yellow') as spinner:
            values = (self.note_title, self.note_text, self.category_id, self.creation_date)
            self.cursor.execute(sql, values)

            spinner.hide()
            PrintFormatted.print_content_storage(self.note_title, self.category_name)
            spinner.show()

            spinner.ok("✔")

        self.db.commit()
        self.db.close()

    def _set_note_content(self, args):

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

    def _ask_category(self):
        """ Function that asks to the user to introduce different category name """

        text = '⚠️[yellow]Category name is too long (Max. 30).[/yellow] Write another name:'
        self.category_name = self.console.input(text).strip()

        while len(self.category_name) == 0 or len(self.category_name) > 30:
            self.category_name = self.console.input(text).strip()
        else:
            self.save_category()

    def _check_note_title(self):
        if len(self.note_title) > 30:
            text = '⚠️[yellow]Note title is too long(Max. 30).[/yellow] Write another title:'
            self.note_title = self.console.input(text).strip()

            while len(self.note_title) == 0 or len(self.note_title) > 30:
                self.note_text = self.console.input(text).strip()

    def _show_preview(self):
        # TODO: FINISH
        formatted_date = self.creation_date.strftime('%Y-%m-%d')

        self.console.rule('Preview', style='purple')
        self.console.print(Panel)
