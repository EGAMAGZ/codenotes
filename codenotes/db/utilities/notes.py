""" Utility module with the statements and names related with notes table """
from typing import Final

import codenotes.db.utilities.notes_categories as categories

TABLE_NAME: Final = 'cn_notes'

COLUMN_NOTE_ID: Final = 'cn_note_id'
COLUMN_NOTE_TITLE: Final = 'cn_note_title'
COLUMN_NOTE_CONTENT: Final = 'cn_note_content'
COLUMN_NOTE_CATEGORY: Final = 'cn_note_category'
COLUMN_NOTE_README: Final = 'cn_note_readme'
COLUMN_NOTE_CREATION: Final = 'cn_note_creation'

CREATE_NOTES_TABLE: Final = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_NOTE_ID} INTEGER PRIMARY KEY " \
                            f"AUTOINCREMENT NULL, {COLUMN_NOTE_TITLE} NVARCHAR(30) NOT NULL, {COLUMN_NOTE_CONTENT} " \
                            f"TEXT NULL, {COLUMN_NOTE_CATEGORY} INTEGER NOT NULL, {COLUMN_NOTE_README} INTEGER NULL " \
                            f", {COLUMN_NOTE_CREATION} DATE NOT NULL, FOREIGN KEY({COLUMN_NOTE_CATEGORY}) " \
                            f"REFERENCES {categories.TABLE_NAME}({categories.COLUMN_CATEGORY_ID}));"
