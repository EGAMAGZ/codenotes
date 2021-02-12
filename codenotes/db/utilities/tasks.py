""" Utility module with the statements and names related with tasks table """
from typing import Final, Text

import codenotes.db.utilities.tasks_categories as categories


TABLE_NAME: Final[str] = 'cn_tasks'

COLUMN_ID: Final[str] = 'cn_task_id'
COLUMN_CONTENT: Final[str] = 'cn_task_content'
COLUMN_STATUS: Final[str] = 'cn_task_status'
COLUMN_CREATION: Final[str] = 'cn_task_creation'
COLUMN_CATEGORY: Final[str] = 'cn_task_category'

CREATE_TABLE: Final[Text] = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_ID} INTEGER PRIMARY KEY ' \
                            f'AUTOINCREMENT NULL , {COLUMN_CONTENT} TEXT NOT NULL, {COLUMN_STATUS} ' \
                            f'INTEGER NULL DEFAULT 0, {COLUMN_CREATION} DATE NOT NULL, {COLUMN_CATEGORY} ' \
                            f'INTEGER, FOREIGN KEY({COLUMN_CATEGORY}) REFERENCES {categories.TABLE_NAME}' \
                            f'({categories.COLUMN_ID})); '


# from datetime import datetime
# datetime.now().date()
# datetime.date(2020, 8, 12) <- This is how date is stored https://www.tutorialspoint.com/How-to-store-and-retrieve-date-into-Sqlite3-database-using-Python
