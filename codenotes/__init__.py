import logging

import click

from codenotes.cli.category import CreateCategory, SearchCategory, ShowCategory
from codenotes.db import Base, engine
from codenotes.utils import get_base_dir

BASE_DIR = get_base_dir()
LOG_ROOT = BASE_DIR / "codenotes.log"


def enable_logging() -> None:
    logging.basicConfig(
        filename=LOG_ROOT,
        format="%(asctime)s-%(name)s-%(levelname)s:%(message)s",
        level=logging.INFO,
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    logging.info(f"Logging enable. Log file root: {LOG_ROOT}")


@click.group()
@click.option("--log", is_flag=True, hidden=True)
def main(log) -> None:
    """A simple CLI where you can save and view all your created annotations"""
    if log:
        enable_logging()
    Base.metadata.create_all(engine)
    logging.info("Database created all.")


@main.group()
def category():
    """Show, create and search categories"""
    pass


@category.command(name="create")
@click.option(
    "--category-name",
    "-c",
    required=True,
    help="Name of the category to be " "created.",
)
@click.option(
    "--preview", "-p",
    is_flag=True,
    help="Shows a preview and ask for " "confirmation."
)
def create_category(category_name, preview) -> None:
    """Create a new category"""
    logging.info(
        f"Command executed: category create -c {category_name} -p {preview}"
    )
    create = CreateCategory(category_name, preview)
    create.start()


@category.command(name="search")
@click.option(
    "--category-name",
    "-c",
    required=True,
    help="Name of the category to be " "searched.",
)
def search_category(category_name) -> None:
    """Search all categories that match to the name that is searched"""
    logging.info(f"Command executed: category search -c {category_name}")
    search = SearchCategory(category_name)
    search.start()


@category.command(name="show")
@click.option(
    "--category-name",
    "-c",
    required=True,
    help="Name of the category to show information about it and the "
         "annotations store in it."
)
@click.option(
    '--max-items',
    type=int,
    default=5,
    show_default=True,
    help="Maximum number of items to show."
)
def show_category(category_name, max_items) -> None:
    """Show information about all annotations associated to a category"""
    logging.info(f"Command executed: category show -c {category_name}")
    show = ShowCategory(category_name, max_items)
    show.start()
