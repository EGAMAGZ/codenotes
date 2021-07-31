from dataclasses import dataclass
from datetime import date


@dataclass
class Category:
    """Dataclass to store category information

    Parameters
    ----------
    id: int
        Id of the category

    name: str
        Category name
    """

    id: int
    name: str

    def __str__(self) -> str:
        """Return category name"""
        return self.name


@dataclass
class Task:
    """Dataclass to store task information

    Parameters
    ----------
    id: int
        Id of the task

    content: str
        Task content

    status: str
        Task status (Incomplete, In Process & Finished)

    category: str
        Category name where is the task stored

    creation: date
        Date when the task was created
    """

    id: int
    content: str
    status: str
    category: str
    creation: date

    def __str__(self) -> str:
        """Return task content"""
        return self.content
