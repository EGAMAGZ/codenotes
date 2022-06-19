from typing import List

from rich.console import Console
from rich.theme import Theme

from codenotes.cli.theme import CODENOTES_THEME


class PrintFormatted:
    """
    Prints the formatted output of the CLI.

    Using this class allows you to print the output of the CLI using
    predefined styles and predefined types of messages.

    Attributes
    ----------
    console : rich.console.Console
        The console for printing formatted output.
    """

    console: Console

    def __init__(self, theme: Theme = CODENOTES_THEME) -> None:
        """
        PrintFormatted constructor.

        Creates a new instance of Console with the theme specified by the
        theme parameter, by default uses CODENOTES_THEME theme.

        Parameters
        ----------
        theme : Theme
            Theme used
        """
        self.console = Console(theme=theme)

    def ask_confirmation(self, message: str) -> bool:
        """
        Ask the user for confirmation. The message will use by default the
        style assigned for confirmation defined in CODENOTES_THEME.

        Parameters
        ----------
        message : str
            The message to be displayed.

        Returns
        -------
        confirmation : bool
            True if the user wants to continue. False otherwise.
        """
        choices: List[str] = ["y", "n"]
        base_message = f"[confirmation]{message}(y/n)[/confirmation]"
        response = self.console.input(base_message).lower().strip()

        while response not in choices:
            response = self.console.input(base_message).lower().strip()

        return response == choices[0]

    def success(self, message: str) -> None:
        """
        Display a success message in the console. The message will use by
        default the style assigned for success defined in CODENOTES_THEME.

        Parameters
        ----------
        message : str
            The message to be displayed to indicate a process has completed
            successfully.

        """
        base_message = f"[success]{message}[/success]"
        self.console.print(base_message)

    def error(self, message: str) -> None:
        """
        Display an error message in the console if a process has failed or
        can't be completed successfully. The message will use by default the
        style assigned for error defined in CODENOTES_THEME.

        Parameters
        ----------
        message : str
            The message to be displayed to indicate a process has failed or
            can not complete successfully.

        """
        base_message = f"[error]{message}[/error]"
        self.console.print(base_message)
