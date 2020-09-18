from typing import Final


TABLE_NAME: Final = 'cn_notes'

COLUMN_NOTE_ID: Final = 'cn_note_id'
COLUMN_NOTE_TITLE: Final = 'cn_note_title'
COLUMN_NOTE_CONTENT: Final = 'cn_note_content'

CREATE_NOTES_TABLE: Final = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_NOTE_ID} INTEGER PRIMARY KEY " \
                            f"AUTOINCREMENT NULL, {COLUMN_NOTE_TITLE} NVARCHAR(30) NOT NULL, {COLUMN_NOTE_CONTENT} TEXT NOT NULL);"
