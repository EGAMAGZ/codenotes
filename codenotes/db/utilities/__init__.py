from dataclasses import dataclass


@dataclass
class Category:
    """ Dataclass Category """
    category_id: int
    category_name: str

    def __str__(self) -> str:
        return self.category_name
