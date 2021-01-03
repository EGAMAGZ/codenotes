from typing import overload, List, Union

from codenotes.util.args import format_argument_text


def text_break(text: str, max_length: int = 15) -> str:

    if len(text) > 15:
        return f'{text[:max_length]}...'
    else:
        return text

@overload
def format_task_text(text: List[str]) -> List[str]: ...


@overload
def format_task_text(text: List[str]) -> str: ...


def format_task_text(text: List[str]) -> Union[List[str], str]:
    """ Function that formats text passed through arguments

    Parameters
    ----------
    text : List[str]
        Text written in the arguments of argparse
    
    Returns
    -------
    task_text : str
        Task of text passed in arguments and joined
    tasks_list : List[str]
        List of texts of task joined and stripped
    """
    task_text = format_argument_text(text)

    if ';' in task_text:
        tasks_list = []

        for task in task_text.split(';'):
            if task and not task.isspace():
                # Checks if is '' or ' ', and doesn't append it if so
                tasks_list.append(task.strip())  # "Trim"

        return tasks_list

    else:
        return task_text
