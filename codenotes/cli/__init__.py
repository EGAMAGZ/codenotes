import calendar
from typing import overload, List, Union, final
from datetime import datetime, date, timedelta

from rich.console import Console
from rich.theme import Theme

def date_args_empty(args) -> bool:
    """ Check if arguments required to search are empty
    Returns
    -------
    empty : bool
        Return boolean value if all related args to search are empty
    """
    args_needed = [
        args.month,
        args.text,
        args.today,
        args.week,
        args.yesterday
    ]

    if any(args_needed):
        return False
    return True


@overload
def dates_to_search(args) -> List[date]: ...


@overload
def dates_to_search(args) -> date: ...


def dates_to_search(args) -> Union[List[date], date]:
    """ Returns date to search depending of the user selection
    Returns
    -------
    search_date : date
        Returns date to search
    """
    now = datetime.now().date()
    if args.today:
        return now

    elif args.yesterday:
        return now - timedelta(days=1)

    elif args.week:
        first_day = now - timedelta(days=now.weekday())
        last_day = first_day + timedelta(days=6)

        days = [first_day, last_day]

        return days

    elif args.month:
        num_days = calendar.monthrange(now.year, now.month)[1]
        days = [
            date(now.year, now.month, 1),
            date(now.year, now.month, num_days)
        ]

        return days


def format_argument_text(arg_text: List[str]) -> str:
    text = ' '.join(arg_text)

    return text.strip()


@final
class PrintFormatted:

    console: Console

    def __init__(self, custom_theme: Theme = None):
        """ PrintFormatted Constructor """
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
        custom_txt = '[msg]Created category:[/msg][name]{}[/name]'.format(category)

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
        custom_txt = '[msg]> Task saved[{}]: [/msg][task]{}[/task]'.format(category, content)

        custom_theme = Theme({
            'msg': '#d898ed bold',
            'task': '#616161 italic'
        })

        print_formatted = cls(custom_theme)
        print_formatted.console.print(custom_txt)

    @classmethod
    def ask_confirmation(cls, text: str) -> bool:
        print_formatted = cls()

        custom_text = text
        answer = print_formatted.console.input(custom_text).strip()

        while len(answer) > 0 and answer.lower() != 'n' and answer.lower() != 'y':
            answer = print_formatted.console.input(custom_text)

        if answer.lower() == 'y':
            return True
        return False
