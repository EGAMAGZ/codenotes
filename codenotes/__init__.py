import logging

import click

from codenotes.annotations import Annotations
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
    if log:
        enable_logging()
    Base.metadata.create_all(engine)
    logging.info("Database created all.")


@main.group()
def category():
    pass


@category.command(name="create")
@click.argument("name", nargs=-1, required=True)
@click.option('--preview', "-p", is_flag=True)
@click.option(
    "--annotation-type", '-a',
    type=click.Choice(Annotations.list_names(), case_sensitive=False),
    required=True,
)
def create_category(name, preview, annotation_type) -> None:
    print(name, type(name))
    print(preview)
    print(annotation_type)
