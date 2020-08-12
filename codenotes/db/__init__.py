import os
import sqlite3


class SQLiteHelper:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_NAME = 'codenotes.db'
    DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

    def __init__(self):
        conn = sqlite3.connect(self.DATABASE_PATH)
        self.cursor = conn.cursor()

    def exec_sql(self, sql: str):
        self.cursor.execute(sql)
