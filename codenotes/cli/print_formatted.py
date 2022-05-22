from rich.console import Console
from rich.theme import Theme

from codenotes.cli.theme import codenotes_theme


class PrintFormatted:
    console: Console

    def __init__(self, theme: Theme = codenotes_theme) -> None:
        self.console = Console(theme=theme)

    def ask_confirmation(self, message: str) -> bool:
        base_message = f"[confirmation]{message}(y/n)[/confirmation]"
        response = self.console.input(base_message).strip()

        while len(response) > 0 and response.lower() != 'n' and response.lower() != 'y':
            response = self.console.input(message).strip()

        if response.lower() == 'y':
            return True
        return False

    def success(self, message: str) -> None:
        base_message = f"[success]✔️{message}[/success]"
        self.console.print(base_message)

    def error(self, message: str) -> None:
        base_message = f"[error]❌{message}[/error]"
        self.console.print(base_message)
