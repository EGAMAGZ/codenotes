from typing import overload, Union

from codenotes.util.args import format_argument_text


def text_break(complete_text: str, max_length: int = 15) -> str:
    """ Functions that breaks the text you pass after a defined length (Default 15 characters)

    Parameters
    ----------
    complete_text: str
        Whole text before breaking it

    max_length: int
        Max length to break the text and add to the ending '...'

    Returns
    -------
    text_breaked: str
        Depending in the length of the text, it's the way the text will be broken
    """

    if len(complete_text) > 15:
        return f'{complete_text[:max_length]}...'
    else:
        return complete_text

@overload
def format_list_text(text: list[str]) -> list[str]: ...


@overload
def format_list_text(text: list[str]) -> str: ...


def format_list_text(task_text: list[str]) -> Union[list[str], str]:
    """ Function that formats text passed through arguments

    Parameters
    ----------
    text : list[str]
        Text written in the arguments of argparse
    
    Returns
    -------
    tasks_list : Union[list[str], str]
        list of texts of task joined and stripped or, task of text passed in arguments and joined
    """
    task_text = format_argument_text(task_text)

    if ';' in task_text:
        tasks_list = []

        for task in task_text.split(';'):
            if task and not task.isspace():
                # Checks if is '' or ' ', and doesn't append it if so
                tasks_list.append(task.strip())  # "Trim"

        return tasks_list

    else:
        return task_text


def status_text(status_value: int) -> str:
    """ Functions that returns the status in text

    Parameters
    ----------
    status_value: int
        Integer value of the task status

    Returns
    -------
    status_txt: str
        Status text based in the integer value
    """
    if status_value == 0:
        return 'Incomplete'
    elif status_value == 1:
        return 'In Process'
    elif status_value == 2:
        return 'Finished'
