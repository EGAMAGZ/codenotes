from typing import Optional, final

from rich.console import Console
from rich.theme import Theme


@final
class PrintFormatted:
    """Class to display in the terminal beautiful text

    This class only has the purpose to print beautiful text using rich package. It is mainly created with @classmethod
    to print some specific type of text with its own theme

    Attributes
    ----------
    console: Console
        (Rich) Console for beatiful printting
    """

    console: Console

    def __init__(self, custom_theme: Optional[Theme] = None):
        """PrintFormatted Constructor

        Parameters
        ----------
        custom_theme: Optional[Theme]
            Theme use for Console class
        """

        if custom_theme is not None:
            self.console = Console(theme=custom_theme)
        else:
            self.console = Console()

    @classmethod
    def custom_print(cls, text: str, theme: Theme = None) -> None:
        """Class method used to print custom formatted text
        Parameters
        ----------
        text : HTML
            Text that will be print with format similar to html

        theme: Theme
            Theme used for the text to be displayed
        """
        print_formatted = cls(theme)
        print_formatted.console.print(text)

    @classmethod
    def print_category_creation(cls, category: str) -> None:
        """Class method used to print the creation of a new category

        Parameters
        ----------
        category: str
            Name of the category created
        """
        custom_txt = f"[msg]Created new category:[/msg][name]{category}[/name]"

        custom_theme = Theme({"msg": "#31f55f bold", "name": "#616161 italic"})

        print_formatted = cls(custom_theme)
        print_formatted.console.print(custom_txt)

    @classmethod
    def print_content_storage(cls, content: str, category: str) -> None:
        """Class method used to print the process of storage of tasks and notes

        Parameters
        ----------
        content : str
            A glance of the content that is stored

        category : str
            Category where is stored
        """
        custom_txt = f"[msg]> Saved[{category}]: [/msg][content]{content}[/content]"

        custom_theme = Theme({"msg": "#d898ed bold", "content": "#616161 italic"})

        print_formatted = cls(custom_theme)
        print_formatted.console.print(custom_txt)

    @classmethod
    def ask_confirmation(cls, text: str) -> bool:
        """Class method used to ask for confirmation

        Parameters
        ----------
        text: str
            Text that will be displayed to ask confirmation

        Returns
        -------
        confirmation: bool
            Return boolean value that indicates the confirmation
        """
        print_formatted = cls()

        custom_text = text  # Text with rich format
        answer = print_formatted.console.input(custom_text).strip()

        while answer.lower() != "n" and answer.lower() != "y":
            answer = print_formatted.console.input(custom_text)

        if answer.lower() == "y":
            return True
        return False

    @classmethod
    def print_help(cls, help_txt: str) -> None:
        """Class method used to print help text

        Parameters
        ----------
        help_txt: str
            Custom help text that will display instructions of how to use the CLI
        """
        custom_text = help_txt

        custom_theme = Theme({"header": "white bold", "quote": "purple"})

        print_formatted = cls(custom_theme)
        print_formatted.console.print(custom_text)

    @classmethod
    def interruption(cls) -> None:
        custom_text = "[bold red]Interrupted[/bold red]"

        print_formatted = cls()
        print_formatted.console.print(custom_text)
