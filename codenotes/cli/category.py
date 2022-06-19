import logging

from rich import box
from rich.table import Table
from sqlalchemy.exc import IntegrityError

from codenotes.cli.print_formatted import PrintFormatted
from codenotes.db.dao.category import CategoryDao
from codenotes.db.models.category import CategoryModel


class CreateCategory:
    """
    Creates a new category and stores it in the database.

    Attributes
    ----------
    category_name : str
        The name of the category that will be created.

    print_formatted : PrintFormatted
        Instance of PrintFormatted that will be used to print messages about
        the process.

    preview : bool
        Flag indicating whether the category creation should be previewed or
        not.
    """
    category_name: str
    print_formatted: PrintFormatted
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
        self.print_formatted = PrintFormatted()

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
                self.print_formatted.success("Task saved successfully")
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


class SearchCategory:
    """
    Search for categories in the database.

    Attributes
    ----------
    category_name : str
        The name of the category to search for.

    print_formatted: PrintFormatted
        Instance of PrintFormatted that will be used to print messages about
        the process.
    """
    category_name: str
    print_formatted: PrintFormatted

    def __init__(self, category_name: str) -> None:
        """
        SearchCategory constructor.

        Parameters
        ----------
        category_name : str
            The name of the category to be searched for.
        """
        self.print_formatted = PrintFormatted()

        self.category_name = category_name

    def search(self) -> None:
        """
        Searches for the category with the given name and displays the results
        in a table. If none is found, a message is printed indicating this.
        """
        categories = CategoryDao.get_by_name(self.category_name)
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
