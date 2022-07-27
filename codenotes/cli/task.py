from typing import Tuple

from codenotes.cli import BaseCLIAction
from codenotes.db.dao.category import CategoryDao
from codenotes.db.dao.task import TaskDao
from codenotes.db.models.task import TaskModel


class CreateTask(BaseCLIAction):
    tasks: Tuple[str]
    category_name: str

    def __init__(self, tasks: Tuple[str], category_name: str) -> None:
        super().__init__()
        self.tasks = tasks
        self.category_name = category_name

    def show_preview(self) -> None:
        pass

    def create(self) -> None:
        category = CategoryDao.get_by_name(self.category_name)
        if category:
            with self.print_formatted.console.status(
                    status="Saving tasks...") as status:
                for count, task in enumerate(self.tasks, start=1):
                    new_task = TaskModel(content=task, category=category)
                    TaskDao.create(new_task)
                    self.print_formatted.success(
                        f"Task #{count} created successfully."
                    )
                status.stop()

        else:
            self.print_formatted.console.print(
                f"[missing]\"{self.category_name}\" category doesn't exist."
                "[/missing]"
            )

    def start(self) -> None:
        self.create()
