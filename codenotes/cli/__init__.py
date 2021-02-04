from typing import Text, final

from rich.theme import Theme
from rich.console import Console
from rich.markdown import Markdown


@final
class PrintFormatted:

    console: Console

    def __init__(self, custom_theme: Theme = None):
        """ PrintFormatted Constructor 
        
        Parameters
        ----------
        custom_theme: Theme
            Theme use for Console class
        """
        # If a theme is passed, while pass it through Console class
        if custom_theme:
            self.console = Console(theme=custom_theme)
        else:
            self.console = Console()

    @classmethod
    def print(cls, text: str, theme: Theme = None) -> None:
        """ Class method used to print custom formatted text
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
        """ Class method used to print the creation of a new category

        Parameters
        ----------
        category: str
            Name of the category created
        """
        custom_txt = '[msg]Created new category:[/msg][name]{}[/name]'.format(category)

        custom_theme = Theme({
            'msg': '#31f55f bold',
            'name': '#616161 italic'
        })

        print_formatted = cls(custom_theme)
        print_formatted.console.print(custom_txt)

    @classmethod
    def print_content_storage(cls, content: str, category: str) -> None:
        """ Class method used to print the process of storage of tasks and notes
        Parameters
        ----------
        content : str
            A glance of the content that is stored

        category : str
            Category where is stored
        """
        custom_txt = '[msg]> Saved[{}]: [/msg][content]{}[/content]'.format(category, content)

        custom_theme = Theme({
            'msg': '#d898ed bold',
            'content': '#616161 italic'
        })

        print_formatted = cls(custom_theme)
        print_formatted.console.print(custom_txt)

    @classmethod
    def ask_confirmation(cls, text: str) -> bool:
        """ Class method used to ask for confirmation

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

        while len(answer) > 0 and answer.lower() != 'n' and answer.lower() != 'y':
            answer = print_formatted.console.input(custom_text)

        if answer.lower() == 'y':
            return True
        return False
