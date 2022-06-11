from rich import box
from rich.table import Table
from sqlalchemy.exc import IntegrityError

from codenotes.cli.print_formatted import PrintFormatted
from codenotes.db.dao.category import CategoryDao
from codenotes.db.models.category import CategoryModel


class CreateCategory:
    category_name: str
    dao: CategoryDao
    print_formatted: PrintFormatted
    preview: bool

    def __init__(self, category_name: str, preview: bool):
        self.dao = CategoryDao()
        self.print_formatted = PrintFormatted()

        self.category_name = category_name
        self.preview = preview

    def show_preview(self) -> None:
        table = Table(box=box.ROUNDED, title="Preview")
        table.add_column("Category", overflow="fold")
        table.add_row(self.category_name)

        self.print_formatted.console.print(table, justify="left")

        if self.print_formatted.ask_confirmation(
            "Are you sure to create the category?"
        ):
            self.save()

    def save(self) -> None:
        with self.print_formatted.console.status(status="Saving category...") as status:
            try:
                category = CategoryModel(name=self.category_name)
                self.dao.create(category)
                self.print_formatted.success("Task saved successfully")
            except IntegrityError:
                self.print_formatted.error(
                    "Error trying to create category. Category might already " "exists."
                )
            finally:
                status.stop()

    def start(self) -> None:
        if self.preview:
            self.show_preview()
        else:
            self.save()


class SearchCategory:
    category_name: str
    dao: CategoryDao
    print_formatted: PrintFormatted

    def __init__(self, category_name: str) -> None:
        self.dao = CategoryDao()
        self.print_formatted = PrintFormatted()

        self.category_name = category_name

    def search(self) -> None:
        categories = self.dao.get_by_name(self.category_name)
        if categories:
            table = Table()
            table.add_column("Categories")

            for category in categories:
                table.add_row(category.name)

            self.print_formatted.console.print(table)
        else:
            self.print_formatted.console.print("[missing]No categories found.[/missing]")

    def start(self) -> None:
        self.search()
