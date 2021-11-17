from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Union

from rich.console import Console

from codenotes.db.connection import SQLiteConnection

Query = list[tuple]
QueriesList = list[list[tuple]]


class CreateABC(ABC):
    """Abstract class with methods required to create and store content in the database

    Attributes
    ----------
    console: Console
        (Rich) Console for beautiful printing

    db: SQLiteConnection
        Connection with the database
    """

    console: Console
    db: SQLiteConnection

    def __init__(self) -> None:
        self.console = Console()
        self.db = SQLiteConnection()

    @classmethod
    @abstractmethod
    def set_args(cls, args: Namespace) -> None:
        ...

    @abstractmethod
    def category_exists(self, category_name: str) -> bool:
        ...

    @abstractmethod
    def show_preview(self) -> None:
        ...

    @abstractmethod
    def save(self) -> None:
        ...


class SearchABC(ABC):
    """Abstract class with methods required to search content in the database

    Attributes
    ----------
    console: Console
        (Rich) Console for beautiful printing

    db: SQLiteConnection
        Connection with the database
    """

    _query: Union[Query, QueriesList]
    console: Console
    db: SQLiteConnection

    def __init__(self) -> None:
        self.console = Console()
        self.db = SQLiteConnection()

    @property
    def query(self) -> Union[Query, QueriesList]:
        return self._query

    @query.setter
    def query(self, value: Union[Query, QueriesList]) -> None:
        self._query = value

    @classmethod
    @abstractmethod
    def set_args(cls, args: Namespace) -> None:
        ...

    @abstractmethod
    def category_exists(self, category_name: str) -> bool:
        ...

    @abstractmethod
    def sql_query(self) -> Union[Query, QueriesList]:
        ...

    @abstractmethod
    def search(self) -> None:
        ...


class DeleteABC(ABC):

    console: Console
    db: SQLiteConnection

    def __init__(self) -> None:
        self.console = Console()
        self.db = SQLiteConnection()

    @classmethod
    @abstractmethod
    def set_args(cls, args: Namespace) -> None:
        ...

    @abstractmethod
    def category_exists(self, category_name: str) -> bool:
        ...

    @abstractmethod
    def sql_query(self) -> Union[Query, QueriesList]:
        ...

    @abstractmethod
    def delete(self) -> None:
        ...
