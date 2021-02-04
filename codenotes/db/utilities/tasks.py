""" Utility module with the statements and names related with tasks table """
from typing import Final, Text

import codenotes.db.utilities.tasks_categories as categories


TABLE_NAME: Final[str] = 'cn_tasks'

COLUMN_TASK_ID: Final[str] = 'cn_task_id'
COLUMN_TASK_CONTENT: Final[str] = 'cn_task_content'
COLUMN_TASK_STATUS: Final[str] = 'cn_task_status'
COLUMN_TASK_CREATION: Final[str] = 'cn_task_creation'
COLUMN_TASK_CATEGORY: Final[str] = 'cn_task_category'

CREATE_TASKS_TABLE: Final[Text] = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_TASK_ID} INTEGER PRIMARY KEY ' \
                            f'AUTOINCREMENT NULL , {COLUMN_TASK_CONTENT} TEXT NOT NULL, {COLUMN_TASK_STATUS} ' \
                            f'INTEGER NULL DEFAULT 0, {COLUMN_TASK_CREATION} DATE NOT NULL, {COLUMN_TASK_CATEGORY} ' \
                            f'INTEGER, FOREIGN KEY({COLUMN_TASK_CATEGORY}) REFERENCES {categories.TABLE_NAME}' \
                            f'({categories.COLUMN_CATEGORY_ID})); '


# from datetime import datetime
# datetime.now().date()
# datetime.date(2020, 8, 12) <- This is how date is stored https://www.tutorialspoint.com/How-to-store-and-retrieve-date-into-Sqlite3-database-using-Python
