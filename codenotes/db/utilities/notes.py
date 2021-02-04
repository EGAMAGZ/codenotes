""" Utility module with the statements and names related with notes table """
from typing import Final, Text

import codenotes.db.utilities.notes_categories as categories

TABLE_NAME: Final[str] = 'cn_notes'

COLUMN_NOTE_ID: Final[str] = 'cn_note_id'
COLUMN_NOTE_TITLE: Final[str] = 'cn_note_title'
COLUMN_NOTE_CONTENT: Final[str] = 'cn_note_content'
COLUMN_NOTE_CATEGORY: Final[str] = 'cn_note_category'
COLUMN_NOTE_README: Final[str] = 'cn_note_readme'
COLUMN_NOTE_CREATION: Final[str] = 'cn_note_creation'

CREATE_NOTES_TABLE: Final[Text] = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_NOTE_ID} INTEGER PRIMARY KEY " \
                            f"AUTOINCREMENT NULL, {COLUMN_NOTE_TITLE} NVARCHAR(30) NOT NULL, {COLUMN_NOTE_CONTENT} " \
                            f"TEXT NULL, {COLUMN_NOTE_CATEGORY} INTEGER NOT NULL, {COLUMN_NOTE_README} INTEGER NULL DEFAULT 0" \
                            f", {COLUMN_NOTE_CREATION} DATE NOT NULL, FOREIGN KEY({COLUMN_NOTE_CATEGORY}) " \
                            f"REFERENCES {categories.TABLE_NAME}({categories.COLUMN_CATEGORY_ID}));"
