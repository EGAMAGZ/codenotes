import calendar
from argparse import Namespace
from datetime import date, datetime, timedelta
from typing import Optional, Union, overload


def date_args_empty(args: Namespace) -> bool:
    """Check if arguments required to search are empty

    Parameters
    ----------
    args: Namespace
        Arguments capture

    Returns
    -------
    empty: bool
        Return boolean value if all related args to search are empty
    """
    args_needed = [
        args.month,
        args.text,
        args.today,
        args.week,
        args.yesterday,
        args.ever,
    ]

    if any(args_needed):
        return False
    return True


@overload
def dates_to_search(args: Namespace) -> Optional[list[date]]:
    ...


@overload
def dates_to_search(args: Namespace) -> Optional[date]:
    ...


def dates_to_search(args: Namespace) -> Optional[Union[list[date], date]]:
    """Returns date to search depending of the user selection

    Parameters
    ----------
    args: Namespace
        Arguments capture

    Returns
    -------
    search_date: Optional[Union[list[date], date]]
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
        days = [date(now.year, now.month, 1), date(now.year, now.month, num_days)]

        return days

    elif args.ever:
        return None


def format_argument_text(arg_text: list[str]) -> str:
    """Function use to join the list of strings passed in the arguments

    Parameters
    ----------
    arg_text: list[str]
        list of strings capture by argparse

    Returns
    -------
    text_joined: str
        Returns text that was joined
    """
    text = " ".join(arg_text)

    return text.strip()
