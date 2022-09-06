import flet
from flet import Page

from codenotes.ui.screens import CodenotesApp


def app(page: Page):
    page.title = "Codenotes"

    codenotes_app = CodenotesApp()
    page.add(codenotes_app)


def run_app() -> None:
    flet.app(name="Codenotes", target=app)


if __name__ == '__main__':
    flet.app(name="Codenotes", target=app)
