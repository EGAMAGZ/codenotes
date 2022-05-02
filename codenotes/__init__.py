import logging
from pathlib import Path

import click

from codenotes.annotations import Annotations

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_ROOT = BASE_DIR / "codenotes.log"


@click.group()
@click.option("--log", is_flag=True, hidden=True)
def main(log) -> None:
    if log:
        enable_logging()


def enable_logging() -> None:
    logging.basicConfig(
        filename=LOG_ROOT,
        format="%(asctime)s-%(name)s-%(levelname)s:%(message)s",
        level=logging.INFO,
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    logging.info(f"Logging enable. Log file root: {LOG_ROOT}")


@main.group()
def category():
    pass


@category.command(name="create")
@click.argument("name", required=True)
@click.option("--preview", "-p", is_flag=True)
@click.option('--annotation-type',
              type=click.Choice(Annotations.list_names(), case_sensitive=False), required=True)
def create_category(name, preview, annotation_type):
    print(name)
    print(preview)
    print(annotation_type)
