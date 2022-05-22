from typing import List

from rich.console import Console
from rich.theme import Theme

from codenotes.cli.theme import codenotes_theme


class PrintFormatted:
    console: Console

    def __init__(self, theme: Theme = codenotes_theme) -> None:
        self.console = Console(theme=theme)

    def ask_confirmation(self, message: str) -> bool:
        choices: List[str] = ["y", "n"]
        base_message = f"[confirmation]{message}(y/n)[/confirmation]"
        response = self.console.input(base_message).lower().strip()

        while response not in choices:
            response = self.console.input(base_message).lower().strip()

        return response == choices[0]

    def success(self, message: str) -> None:
        base_message = f"[success]{message}[/success]"
        self.console.print(base_message)

    def error(self, message: str) -> None:
        base_message = f"[error]{message}[/error]"
        self.console.print(base_message)
