""" Utility module with the statements and names related with category notes table """
from typing import Final

TABLE_NAME: Final = 'cn_notes_categories'

COLUMN_CATEGORY_ID: Final = 'cn_notes_category_id'
COLUMN_CATEGORY_NAME: Final = 'cn_notes_category_name'

CREATE_NOTES_CATEGORY_TABLE: Final = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_CATEGORY_ID} INTEGER PRIMARY ' \
                                     f'KEY AUTOINCREMENT NULL, {COLUMN_CATEGORY_NAME} NVARCHAR(30) NOT NULL);'

INSERT_DEFAULT_CATEGORY: Final = f'INSERT INTO {TABLE_NAME} ({COLUMN_CATEGORY_NAME}) SELECT "General" WHERE NOT ' \
                                 f'EXISTS (SELECT 1 FROM {TABLE_NAME} WHERE {COLUMN_CATEGORY_ID} = 1)'
