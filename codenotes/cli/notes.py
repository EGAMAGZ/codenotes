from rich.console import Console

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
                category = ' '.join(args.new_category)
                self.save_category(category)

            if args.text:
                pass

    @classmethod
    def set_args(cls, args):
        """ Set args and initialize class
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        return cls(args)

    def save_category(self, category: str):
        if len(category) <= 30:
            sql = f'INSERT INTO {categories.TABLE_NAME} ({categories.COLUMN_CATEGORY_NAME}) VALUES (?)'
            self.cursor.execute(sql, (category.strip(),))

            self.category_id = self.cursor.lastrowid

            self.db.commit()

        else:
            self._ask_category()

    def _ask_category(self):
        """ Function that asks to the user to introduce different category name """

        text = 'Category name is too long(Max. 30). Write another name:'
        category = self.console.input(text)

        while len(category) == 0 or len(category) > 30:
            category = self.console.input(text)
        else:
            self.save_category(category)
