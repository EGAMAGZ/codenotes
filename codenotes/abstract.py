from abc import ABC, abstractmethod

from argparse import Namespace
from typing import Union

Query = list[tuple]
QueriesList = list[list[tuple]]


class CreateABC(ABC):
    """Abstract class with methods required to create and store content in the database"""

    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        ...

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
    """Abstract class with methods required to search content in the database"""

    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        ...

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
