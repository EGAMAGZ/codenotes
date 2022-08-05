import logging
from typing import Union

from rich import box
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from sqlalchemy.exc import IntegrityError

from codenotes.cli import BaseCLIAction
from codenotes.db.dao.category import CategoryDao
from codenotes.db.dao.task import TaskDao
from codenotes.db.models.category import CategoryModel


class CreateCategory(BaseCLIAction):
    """
    Creates a new category and stores it in the database.

    Attributes
    ----------
    category_name : str
        The name of the category that will be created.

    preview : bool
        Flag indicating whether the category creation should be previewed or
        not.
    """
    category_name: str
    preview: bool

    def __init__(self, category_name: str, preview: bool):
        """
        CreateCategory constructor.

        Parameters
        ----------
        category_name : str
            Name of the category that will be created.

        preview : bool
            Flag indicating whether to print preview of the category creation
            or not.
        """
        super().__init__()
        self.category_name = category_name
        self.preview = preview

    def show_preview(self) -> None:
        """
        Shows preview of the category creation. This will show the category
        that will be created and ask for confirmation.
        """
        table = Table(box=box.ROUNDED, title="Preview")
        table.add_column("Category", overflow="fold")
        table.add_row(self.category_name)

        self.print_formatted.console.print(table, justify="left")

        if self.print_formatted.ask_confirmation(
                "Are you sure to create the category?"
        ):
            self.create()

    def create(self) -> None:
        """
        Creates a new category and displays a success message. If the
        category already exists, it will be displayed in the console an error
        message.
        """
        with self.print_formatted.console.status(
                status="Saving category...") as status:
            try:
                category = CategoryModel(name=self.category_name)
                CategoryDao.create(category)
                self.print_formatted.success("Category created successfully.")
                logging.info(
                    f"Category {self.category_name} created successfully")
            except IntegrityError:
                self.print_formatted.error(
                    "Error trying to create category. Category might already "
                    "exists. "
                )
                logging.info(f"Category {self.category_name} already exists")
            finally:
                status.stop()

    def start(self) -> None:
        """
        Starts the process of creating a category.
        """
        if self.preview:
            self.show_preview()
        else:
            self.create()


class DeleteCategory(BaseCLIAction):
    category_name: str
    force_delete: bool

    def __init__(self, category_name: str, force_delete: bool) -> None:
        """
        DeleteCategory constructor.
        """
        super().__init__()
        self.category_name = category_name
        self.force_delete = force_delete

    def delete(self) -> None:
        if not self.force_delete:
            category_name = self.print_formatted.ask(
                f"Type {self.category_name} to confirm deletion: "
            )
            while self.category_name != category_name:
                self.print_formatted.error(
                    f"Sorry, your reply was invalid. "
                    f"You entered {category_name}"
                )
                category_name = self.print_formatted.ask(
                    f"Type {self.category_name} to confirm deletion: "
                )

        deleted = CategoryDao.delete_by_name(self.category_name)
        if deleted:
            self.print_formatted.success(
                "Category deleted successfully."
            )
        else:
            self.print_formatted.console.print(
                "[missing]Category doesn't exist.[/missing]"
            )

    def start(self) -> None:
        """
        Starts the process of deleting a category.
        """
        self.delete()


class SearchCategory(BaseCLIAction):
    """
    Search for categories in the database.

    Attributes
    ----------
    category_name : str
        The name of the category to search for.
    """
    category_name: str

    def __init__(self, category_name: str) -> None:
        """
        SearchCategory constructor.

        Parameters
        ----------
        category_name : str
            The name of the category to be searched for.
        """
        super().__init__()
        self.category_name = category_name

    def search(self) -> None:
        """
        Searches for the category with the given name and displays the results
        in a table. If none is found, a message is printed indicating this.
        """
        categories = CategoryDao.search_by_name(self.category_name)
        if categories:
            table = Table()
            table.add_column("Categories")

            for category in categories:
                table.add_row(category.name)

            self.print_formatted.console.print(table)
        else:
            self.print_formatted.console.print(
                "[missing]No categories found.[/missing]"
            )

    def start(self) -> None:
        """
        Starts the process of searching for a category.
        """
        self.search()


class ShowCategory(BaseCLIAction):
    category_name: str
    max_items: int

    def __init__(self, category_name: str, max_items: int) -> None:
        super().__init__()
        self.category_name = category_name
        self.max_items = max_items

    def generate_task_table(self, category_id: int) -> Union[Table, Panel]:
        tasks = TaskDao.get_tasks_with_limit(category_id, self.max_items)
        if tasks:
            renderable: Union[Table, Panel] = Table()

        else:
            renderable = Panel(
                Text("No tasks found.", justify="center")
            )

        return renderable

    def generate_task_stats(self, category_id: int) -> Panel:
        total_tasks = TaskDao.count_tasks(category_id)
        total_tasks_completed = TaskDao.count_tasks_completed(
            category_id
        )
        try:
            percentage = round((total_tasks * 100) / total_tasks)
        except ZeroDivisionError:
            percentage = 0

        panel = Panel(
            Group(
                Text(f"Total: {total_tasks}"),
                Text(f"Completed: {total_tasks_completed}")
            ),
            subtitle=f"Completion percentage: {percentage}%"
        )

        return panel

    def task_information(self, category_id: int) -> Columns:

        columns = Columns(
            [
                self.generate_task_table(category_id),
                self.generate_task_stats(category_id)
            ], expand=True
        )

        return columns

    def generate_table(self, category: CategoryModel) -> Table:
        table = Table.grid(padding=1, pad_edge=True, expand=True)
        table.title = f"[b]Category[/b]: {self.category_name}"
        table.add_column(
            "Information",
            justify="center",
            style="bold red",
            no_wrap=True
        )
        table.add_column("Details")

        table.add_row(
            "Created at",
            Panel(
                Text(
                    f"{category.created_at}",
                    justify="center",
                    style="yellow"
                )
            )
        )
        table.add_row(
            "Tasks",
            self.task_information(category.id)
        )

        return table

    def show(self) -> None:
        category = CategoryDao.get_by_name(self.category_name)
        if category:
            with self.print_formatted.console.status(
                    status="Searching") as status:
                table = self.generate_table(category)
                self.print_formatted.console.print(table)
                status.stop()
        else:
            self.print_formatted.console.print(
                f"[missing]\"{self.category_name}\" category doesn't exist."
                "[/missing]"
            )

    def start(self) -> None:
        self.show()
