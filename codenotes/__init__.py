import logging

import click

from codenotes.cli import NotRequiredIf


@click.group()
@click.option("--log", is_flag=True)
def main(log) -> None:
    if log:
        enable_logging()


def enable_logging() -> None:
    logging.basicConfig(
        filename="codenotes.log",
        format="%(asctime)s-%(name)s-%(levelname)s:%(message)s",
        level=logging.INFO,
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )


@main.group()
def category():
    pass


@category.command(name="create")
@click.argument("name")
@click.option("--preview", "-p", is_flag=True)
@click.option("--task", is_flag=True)
def create_category(name, preview, task):
    print(name)
    print(preview)


if __name__ == "__main__":
    main()
