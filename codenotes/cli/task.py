import logging
from typing import Tuple

from codenotes.cli import BaseCLIAction
from codenotes.db.dao.category import CategoryDao
from codenotes.db.dao.task import TaskDao
from codenotes.db.models.task import TaskModel


class CreateTask(BaseCLIAction):
    """
    Create new tasks related to a given category and stores them in the
    database.

    Attributes
    ----------
    tasks : Tuple[str]
        Tasks to be created.

    category_name: str
        Category name where the tasks are created.

    """
    tasks: Tuple[str]
    category_name: str

    def __init__(self, tasks: Tuple[str], category_name: str) -> None:
        """
        CreateTask constructor.

        Parameters
        ----------
        tasks : Tuple[str]
            Tasks to be created.

        category_name: str
            Category name where the tasks are created.
        """
        super().__init__()
        self.tasks = tasks
        self.category_name = category_name

    def create(self) -> None:
        """
        Create a single or multiple tasks related with the given category
        name, and displays a success message. If the category doesn't exist,
        it will be displayed in the console and error message.
        """
        category = CategoryDao.get_by_name(self.category_name)
        if category:
            with self.print_formatted.console.status(
                    status="Saving tasks..."
                ) as status:
                for count, task in enumerate(self.tasks, start=1):
                    new_task = TaskModel(content=task, category=category)
                    TaskDao.create(new_task)
                    self.print_formatted.success(
                        f"Task #{count} created successfully."
                    )
                    logging.info(
                        f"Task \"{task}\" created sucessfully."
                    )
                status.stop()

        else:
            self.print_formatted.console.print(
                f"[missing]\"{self.category_name}\" category doesn't exist."
                "[/missing]"
            )
            logging.info(
                f"Category {self.category_name} doesn't exist.'"
            )

    def start(self) -> None:
        """
        Start the process of creating a task or multiple tasks.
        """
        self.create()
