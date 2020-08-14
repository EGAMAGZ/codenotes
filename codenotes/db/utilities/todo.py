TABLE_NAME = 'cn_todos'

COLUMN_TODO_ID = 'cn_todo_id'
COLUMN_TODO_CONTENT = 'cn_todo_content'
COLUMN_TODO_STATUS = 'cn_todo_status'
COLUMN_TODO_CREATION = 'cn_todo_creation'

CREATE_TODOS_TABLE = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMN_TODO_ID} INTEGER PRIMARY KEY ' \
                     f'AUTOINCREMENT NULL , {COLUMN_TODO_CONTENT} TEXT NOT NULL, {COLUMN_TODO_STATUS} ' \
                     f'INTEGER NULL DEFAULT 0, {COLUMN_TODO_CREATION} DATE NOT NULL);'
#from datetime import datetime
#datetime.now().date()
#datetime.date(2020, 8, 12) <- This is how date is stored https://www.tutorialspoint.com/How-to-store-and-retrieve-date-into-Sqlite3-database-using-Python