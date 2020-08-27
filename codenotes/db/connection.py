import os
import sqlite3
from sqlite3.dbapi2 import Cursor
from typing import overload, Union

import codenotes.db.utilities.notes as notes
import codenotes.db.utilities.tasks as tasks
import codenotes.db.utilities.tasks_categories as categories


class SQLiteConnection:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_NAME = 'codenotes.db'
    DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

    def __init__(self):
        """ SQLiteConnection Constructor """
        self.conn = sqlite3.connect(self.DATABASE_PATH)
        self.cursor = self.conn.cursor()

        self.exec_sql(notes.CREATE_NOTES_TABLE)  # Notes Table
        self.exec_sql(categories.CREATE_TODOS_CATEGORY_TABLE)  # Task Category Table
        self.cursor.execute(categories.INSERT_DEFAULT_CATEGORY)  # Insert Default Category
        self.exec_sql(tasks.CREATE_TASKS_TABLE)  # Tasks Table

        self.conn.commit()

    @overload
    def exec_sql(self, sql: str) -> Cursor: ...

    @overload
    def exec_sql(self, sql: str) -> None: ...

    def exec_sql(self, sql: str) -> Union[Cursor, None]:
        """ Function that executes sql command 
        
        Parameters
        ----------
        sql : str
            SQL statement to be executed

        Returns
        -------
        cursor : Union[Cursor, None]
            Method will return None or Cursor, depending of the statement executed
        """
        self.cursor.execute(sql)

    def get_cursor(self) -> Cursor:
        """ Return cursor created 
        
        Returns
        -------
        cursor : Cursor
            Returns the cursor of the class
        """
        return self.cursor

    def close(self):
        """ Close database and cursor connection """
        self.cursor.close()
        self.conn.close()
