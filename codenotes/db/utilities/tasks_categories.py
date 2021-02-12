""" Utility module with the statements and names related with task notes table """
from typing import Final, Text

TABLE_NAME: Final[str] = 'cn_tasks_categories'

COLUMN_ID: Final[str] = 'cn_tasks_category_id'
COLUMN_NAME: Final[str] = 'cn_tasks_category_name'

CREATE_TABLE: Final[Text] = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_ID} INTEGER ' \
                                     f'PRIMARY KEY AUTOINCREMENT NULL, {COLUMN_NAME} NVARCHAR(30) NOT NULL);'

INSERT_DEFAULT_CATEGORY: Final[Text] = f'INSERT INTO {TABLE_NAME} ({COLUMN_NAME}) SELECT "TODO Tasks" WHERE NOT ' \
                                 f'EXISTS(SELECT 1 FROM {TABLE_NAME} WHERE {COLUMN_ID} = 1); '
