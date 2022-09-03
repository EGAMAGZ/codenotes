import logging
from time import sleep

from rich import box
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
    Create a new category and stores it in the database.

    Attributes
    ----------
    category_name : str
        Name of the category that will be created.

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
        Show preview of the category creation. This will show the category
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
        Create a new category and display a success message. If the
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
        Start the process of creating a category.
        """
        if self.preview:
            self.show_preview()
        else:
            self.create()


class DeleteCategory(BaseCLIAction):
    """
    Delete a category from the database, and delete all content associated
    with it.

    Attributes
    ----------
    category_name : str
        Name of the category that will be created.

    force_delete : bool
        Flag indicating whether to ask or not for confirmation to delete.
    """
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
        """
        Delete the category and display a success message. In case of the
        category doesn't exist, wil display a message indicating this. Before
        deleting asks for confirmation.
        """
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

        with self.print_formatted.console.status(
            status="Deleting category..."
        ) as status:
            deleted = CategoryDao.delete_by_name(self.category_name)

            if deleted:
                self.print_formatted.success(
                    "Category deleted successfully."
                )
                logging.info(
                    f"Category {self.category_name} deleted successfully."
                )
            else:
                self.print_formatted.console.print(
                    "[missing]Category doesn't exist.[/missing]"
                )
                logging.info(
                    f"Category {self.category_name} doesn't exist.'"
                )
            status.stop()

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
        Search for the category with the given name and displays the results
        in a table. If none is found, a message is printed indicating this.
        """
        categories = CategoryDao.search_by_name(self.category_name)
        if categories:
            with self.print_formatted.console.status(
                    status="Searching categories..."
            ) as status:
                table = Table()
                table.add_column("Categories")

                for category in categories:
                    table.add_row(category.name)

                self.print_formatted.console.print(table)
                status.stop()
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
    """
    Show information about the specified category, including the last stored
    content and statistics for each annotation type.

    Parameters
    ---------
    category_name : str
        Category name to be searched.

    max_tasks : int
        Maximum number of tasks to display.
    """
    category_name: str
    max_tasks: int

    def __init__(self, category_name: str, max_tasks: int) -> None:
        """
        ShowCategory constructor.

        Parameters
        ----------
        category_name : str
            Category name to be searched.

        max_tasks : int
            Maximum number of tasks to display.
        """
        super().__init__()

        self.category_name = category_name
        self.max_tasks = max_tasks

    def generate_task_table(self, category_id: int) -> Table:
        """
        Generate table with a list of recently created tasks, the amount of
        tasks that will be queried and displayed will be determined by
        self.max_tasks.

        Parameters
        ----------
        category_id : int
            Category ID to search for tasks.

        Returns
        -------
        table : Table
            Table with a list of tasks.
        """
        if self.max_tasks >= 0:
            tasks = TaskDao.get_tasks_with_limit(category_id, self.max_tasks)
        else:
            tasks = TaskDao.get_all_tasks(category_id)

        table = Table(expand=True, show_lines=True)
        table.add_column("Content", ratio=1)
        table.add_column("Completed", justify="center")

        for task in tasks:
            table.add_row(
                task.content,
                ":white_check_mark:" if task.completed else ":cross_mark:"
            )

        return table

    def generate_task_stats(self, category_id: int) -> Panel:
        """
        Generate a panel that contains stats about the tasks completion such as
        total of tasks,total of task completed and completion percentage.

        Parameters
        ----------
        category_id : int
            Category ID to search for tasks.

        Returns
        -------
        panel : Panel
            Panel that contains stats about the tasks completion
        """
        total_tasks = TaskDao.count_tasks(category_id)
        total_tasks_completed = TaskDao.count_tasks_completed(
            category_id
        )

        if total_tasks > 0:
            percentage = round((total_tasks_completed * 100) / total_tasks)
        else:
            percentage = 0

        panel = Panel(
            Group(
                Text(f"Total: {total_tasks}"),
                Text(f"Completed: {total_tasks_completed}")
            ),
            subtitle=f"Completion percentage: {percentage}%"
        )

        return panel

    def task_information(self, category_id: int) -> Group:
        """
        Generate group with a table a list of recently created tasks (showing
        their content and if they have been completed) with a panel that
        contains stats about the tasks completion, or a text indicating that no
        tasks were created.

        Parameters
        ----------
        category_id : int
            Category ID to search for tasks.

        Returns
        -------
        group : Group
            Group containing a table with a list of recently created tasks with
            a panel that contains stats about the tasks completion, or text
            indicating that no tasks were created.
        """
        total_tasks = TaskDao.count_tasks(category_id)

        if total_tasks > 0:
            table = Table.grid(pad_edge=True, expand=True)
            table.add_column("")
            table.add_column("")
            table.add_row(
                self.generate_task_table(category_id),
                self.generate_task_stats(category_id)
            )

            group = Group(
                Panel.fit(
                    Text("Tasks")
                ),
                table
            )

        else:
            group = Group(
                Panel.fit(
                    Text("Tasks")
                ),
                Panel(
                    Text(
                        "No task found",
                        justify="center"
                    )
                )
            )

        return group

    def generate_information(self, category: CategoryModel) -> Group:
        """
        Generate group that contains information about the category and its
        annotations.

        Parameters
        ----------
        category : CategoryModel
            Category model to generate and get the information about it.

        Returns
        -------
        group : Group
            Group that contains information about the category and its
            annotations.
        """
        group = Group(
            Panel(
                Text.assemble(
                    "Category: ",
                    (f"{self.category_name}", "bold"),
                    justify="center"
                ),
                subtitle=f"Created at: [yellow]{category.created_at}[yellow]",
                box=box.DOUBLE_EDGE
            ),
            self.task_information(category.id)
        )

        return group

    def show(self) -> None:
        """
        Show information about the specified category, including the last stored
        content and statistics for each annotation type. In case of the category
        doesn't exist, wil display a message indicating this.
        """
        category = CategoryDao.get_by_name(self.category_name)

        if category:
            with self.print_formatted.console.status(
                status="Searching category..."
            ) as status:
                table = self.generate_information(category)
                self.print_formatted.console.print(table)
                status.stop()
        else:
            self.print_formatted.console.print(
                f"[missing]\"{self.category_name}\" category doesn't exist."
                "[/missing]"
            )

    def start(self) -> None:
        """
        Start the process of showing a category.
        """
        self.show()
