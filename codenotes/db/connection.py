import os
import sqlite3
from sqlite3.dbapi2 import Cursor

import codenotes.db.utilities.notes as notes
import codenotes.db.utilities.todo as todo


class SQLiteConnection:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_NAME = 'codenotes.db'
    DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

    def __init__(self):
        """ SQLiteConnection Constructor """
        self.conn = sqlite3.connect(self.DATABASE_PATH)
        self.cursor = self.conn.cursor()

        self.exec_sql(notes.CREATE_NOTES_TABLE)
        self.exec_sql(todo.CREATE_TODOS_TABLE)

    def exec_sql(self, sql: str):
        """ Function that executes sql command """
        self.cursor.execute(sql)

    def get_cursor(self) -> Cursor:
        """ Return cursor created """
        return self.cursor

    def close(self):
        """ Close database and cursor connection """
        self.conn.close()
        self.cursor.close()
