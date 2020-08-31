from dataclasses import dataclass
from datetime import date

from codenotes.util.menu import abbreviate_menu_text


@dataclass
class Category:
    """ Dataclass Category """
    category_id: int
    category_name: str

    def __str__(self) -> str:
        return abbreviate_menu_text(self.category_name)


@dataclass
class Task:

    id: int
    content: str
    status: str
    category: str
    creation: date

    def __str__(self) -> str:
        return self.content
