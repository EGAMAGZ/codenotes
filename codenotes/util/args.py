import calendar
from argparse import Namespace
from typing import overload, Union
from datetime import datetime, date, timedelta

def date_args_empty(args: Namespace) -> bool:
    """ Check if arguments required to search are empty

    Parameters
    ----------
    args: Namespace
        Arguments capture

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
def dates_to_search(args: Namespace) -> list[date]: ...


@overload
def dates_to_search(args: Namespace) -> date: ...


def dates_to_search(args: Namespace) -> Union[list[date], date]:
    """ Returns date to search depending of the user selection

    Parameters
    ----------
    args: Namespace
        Arguments capture

    Returns
    -------
    search_date : Union[list[date], date]
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


def create_note_args_empty(args: Namespace) -> bool:
    """ Functions that checks if the arguments required to create a new note are empty

    Parameters
    ----------
    args: Namespace
        Arguments capture with argparse
    
    Returns
    -------
    empty: bool
        Boolean value that indicates if the arguments required for a note are empty
    """
    args_needed = [
        args.title,
        args.category,
        args.text
    ]

    if any(args_needed):
        return False
    return True


def create_task_args_empty(args: Namespace) -> bool:
    """ Functions that checks if the arguments required to create a new task are empty

    Parameters
    ----------
    args: Namespace
        Arguments capture with argparse
    
    Returns
    -------
    empty: bool
        Boolean value that indicates if the arguments required for a task are empty
    """
    args_needed = [
        args.text,
        args.category
    ]

    if any(args_needed):
        return False
    return True


def format_argument_text(arg_text: list[str]) -> str:
    """ Function use to join the list of strings passed in the arguments
    
    Parameters
    ----------
    arg_text: list[str]
        list of strings capture by argparse

    Returns
    -------
    text_joined: str
        Returns text that was joined
    """
    text = ' '.join(arg_text)

    return text.strip()

def create_category_args_empty(args: Namespace) -> bool:
    """ Check if arguments required to select an annotation type

    Parameters
    ----------
    args: Namespace
        Arguments capture

    Returns
    -------
    empty : bool
        Return boolean value if any args are empty
    """
    args_needed = [
        args.note,
        args.task
    ]
    if any(args_needed):
        return False
    return True
