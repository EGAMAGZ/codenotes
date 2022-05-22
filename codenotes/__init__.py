import logging

import click
from click.testing import CliRunner

from codenotes.cli.category import CreateCategory
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
def create_category(name, preview) -> None:
    create = CreateCategory(name, preview)
    create.start()


if __name__ == '__main__':
    runner = CliRunner()
    result = runner.invoke(main, ['category', 'create'])
    print(result.exit_code)
    print(result.exc_info)
