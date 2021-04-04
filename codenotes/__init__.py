from codenotes.cli.category import CreateCategory
import sys
import argparse
from typing import Final, Text

import codenotes.util.help as help_text
from codenotes.cli import PrintFormatted
from codenotes.cli.tasks import CreateTask, SearchTask
from codenotes.cli.notes import CreateNote, SearchNote


__version__ = '0.0.1'


def parse_args(sys_args: list) -> argparse.Namespace:
    """ Function incharge to declare the Argumen Parser and add arguments to it

    Parameters
    ----------
    sys_args: list
        String list of arguments capture by sys.argv

    Returns
    -------
    args: Namespace
        All the arguments that are in ArgumenParser
    """

    parser = argparse.ArgumentParser(prog='codenotes')
    parser.add_argument('--version', '-v', action='version', version=__version__)
    subparsers = parser.add_subparsers(dest='subargs') # Types of annotation

    task = subparsers.add_parser('task')
    task_actions = task.add_subparsers(dest='action')

    task_create = task_actions.add_parser('create')
    task_create.add_argument('text', type=str, nargs='*', action='store')
    task_create.add_argument('--category', '-c', type=str, nargs='*', action='store')
    task_create.add_argument('--preview', '-p', action='store_true')

    task_search = task_actions.add_parser('search')
    task_search.add_argument('text', action='store', nargs='*')

    task_search_group = task_search.add_mutually_exclusive_group()
    task_search_group.add_argument('--today', '-t', action='store_true')
    task_search_group.add_argument('--yesterday', '-y', action='store_true')
    task_search_group.add_argument('--week', '-w', action='store_true')
    task_search_group.add_argument('--month', '-m', action='store_true')

    note = subparsers.add_parser('note')
    note_actions = note.add_subparsers(dest='action')

    note_create = note_actions.add_parser('create')
    note_create.add_argument('text', type=str, nargs='*', action='store')
    note_create.add_argument('--title', '-t', type=str, nargs='*', action='store')
    note_create.add_argument('--category', '-c', type=str, nargs='*', action='store')
    note_create.add_argument('--preview', '-p', action='store_true')

    note_search = note_actions.add_parser('search')
    note_search.add_argument('text', action='store', nargs='*')

    note_search_group = note_search.add_mutually_exclusive_group()
    note_search_group.add_argument('--today', '-t', action='store_true')
    note_search_group.add_argument('--yesterday', '-y', action='store_true')
    note_search_group.add_argument('--week', '-w', action='store_true')
    note_search_group.add_argument('--month', '-m', action='store_true')

    category = subparsers.add_parser('category')
    category_actions = category.add_subparsers(dest='action')

    category_create = category_actions.add_parser('create')
    category_create.add_argument('text', type=str, nargs='*', action='store')
    category_create.add_argument('--preview', '-p', action='store_true')

    category_create_annotation = category_create.add_mutually_exclusive_group()
    category_create_annotation.add_argument('--note','-n', action='store_true')
    category_create_annotation.add_argument('--task','-t', action='store_true')

    tui = subparsers.add_parser('tui')
    tui.add_argument('window', choices=['note', 'task'])

    parser.error = print_usage

    return parser.parse_args(sys_args)


def print_usage(error_message: str = None) -> None:
    """ Print usage text with rich console, and print error message passed when this function is called by argparse

    Parameters
    ----------
    error_message: str
        Error message through
    """
    if error_message is not None:
        PrintFormatted.custom_print(f'[red]{error_message}[/red]')
    
    PrintFormatted.print_help(help_text.CLI_USAGE_TEXT)


def main():
    """ Main function """
    args = parse_args(sys.argv[1:])
    if len(sys.argv) > 1:
        if args.subargs == 'task':
            if args.action == 'create':
                CreateTask.set_args(args)
            elif args.action == 'search':
                SearchTask.set_args(args)
            else:
                print_usage()

        elif args.subargs == 'note':
            if args.action == 'create':
                CreateNote.set_args(args)
            elif args.action == 'search':
                SearchNote.set_args(args)
            else:
                print_usage()
        elif args.subargs == 'category':
            if args.action == 'create':
                CreateCategory.set_args(args)

    else:
        print_usage()
