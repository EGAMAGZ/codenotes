import os
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from typing import Any, AnyStr, Final

import codenotes.db.utilities.notes as notes
import codenotes.db.utilities.notes_categories as notes_categories
import codenotes.db.utilities.tasks as tasks
import codenotes.db.utilities.tasks_categories as tasks_categories


class SQLiteConnection:

    """Connection with SQLite3 class

    Class has the purpouse to manage the connection with the database created with
    sqlite3. Everytime the constructor is executed, it connects to the database, then
    execute the SQL statements that creates the tables if they not exist. Also, this class
    allows you to execute sql, commit the transactions and close the connection with
    the database.

    Attributes
    ---------
    BASE_DIR: Final[AnyStr]
        Root path where the __main__ is executed

    DATABASE_NAME:Final[str]
        Name of the database

    DATABASE_PATH: Final[str]
        Complete path where is the database (its getted after joinning BASE_DIR & DATABASE_NAME)

    connection: Connection
        Connection with the database specified in DATABASE_PATH

    cursor: Cursor
        Cursor created to interact with the database
    """

    BASE_DIR: Final[AnyStr] = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    DATABASE_NAME: Final[str] = "codenotes.db"
    DATABASE_PATH: Final[str] = os.path.join(BASE_DIR, DATABASE_NAME)

    connection: Connection
    cursor: Cursor

    def __init__(self) -> None:
        """SQLiteConnection Constructor"""
        self.connection = sqlite3.connect(self.DATABASE_PATH)
        self.cursor = self.connection.cursor()

        self.exec_sql(notes_categories.CREATE_TABLE)  # Notes Category Table
        self.cursor.execute(
            notes_categories.INSERT_DEFAULT_CATEGORY
        )  # Insert Default Category
        self.exec_sql(notes.CREATE_TABLE)  # Notes Table

        self.exec_sql(tasks_categories.CREATE_TABLE)  # Task Category Table
        self.cursor.execute(
            tasks_categories.INSERT_DEFAULT_CATEGORY
        )  # Insert Default Category
        self.exec_sql(tasks.CREATE_TABLE)  # Tasks Table

        self.connection.commit()

    def exec_sql(self, sql: str, values: tuple[Any] = None) -> Cursor:
        """Method that executes sql command

        Parameters
        ----------
        sql : str
            SQL statement to be executed

        values: tuple[Any]
            Optional argument typo of tuple, which contains the values the sql statement requires

        Returns
        -------
        cursor : Cursor
            Method will return the cursor that the method execute returns
        """
        if values is not None:
            return self.cursor.execute(sql, values)
        return self.cursor.execute(sql)

    def commit(self) -> None:
        """Method commits the current transaction"""
        self.connection.commit()

    def close(self) -> None:
        """Close database and cursor connection"""
        self.cursor.close()
        self.connection.close()
