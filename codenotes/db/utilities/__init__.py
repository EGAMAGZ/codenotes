from dataclasses import dataclass

from codenotes.util import abbreviate_menu_text


@dataclass
class Category:
    """ Dataclass Category """
    category_id: int
    category_name: str

    def __str__(self) -> str:
        return abbreviate_menu_text(self.category_name)
