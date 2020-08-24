from typing import Final

TABLE_NAME: Final = 'cn_tasks_categories'

COLUMN_CATEGORY_ID: Final = 'cn_tasks_category_id'
COLUMN_CATEGORY_NAME: Final = 'cn_tasks_category_name'

CREATE_TODOS_CATEGORY_TABLE: Final = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_CATEGORY_ID} INTEGER '\
                                     f'PRIMARY KEY AUTOINCREMENT NULL, {COLUMN_CATEGORY_NAME} NVARCHAR(30) NOT NULL);'

INSERT_DEFAULT_CATEGORY: Final = f'INSERT INTO {TABLE_NAME} ({COLUMN_CATEGORY_NAME}) VALUES ("TODO Tasks");'
