import codenotes.db.utilities.notes as notes

from codenotes.db import SQLiteHelper


class SQLiteConnection(SQLiteHelper):

    def __init__(self):
        super().__init__()
        self.exec_sql(notes.CREATE_NOTES_TABLE)
