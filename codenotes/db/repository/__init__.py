from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    @abstractmethod
    def add(self, value) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_all(self, value) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete(self, value) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Any]:
        raise NotImplementedError
