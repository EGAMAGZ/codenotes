import sys
import argparse
from typing import Final, Text

from codenotes.cli import PrintFormatted
from codenotes.cli.tasks import AddTask, SearchTask
from codenotes.cli.notes import AddNote, SearchNote


__version__ = '1.0'


USAGE_TEXT: Final[Text] = "[quote]Write any thought you have without quitting from the command line[/quote]\n\n" \
"[header]USAGE[/header]\ncodenotes <command> <subcommand>\n\n[header]CORE COMMANDS[/header]\n" \
"add\tCreate new note or task with the content typed\n" \
"search\tSearch for notes or tasks with the parameters specified\n[header]SUBCOMMANDS[/header]\n" \
"note/task\tType of annotations\n\n[header]FLAGS[/header]\n" \
"--version, -v\tShow codenotes version\n\n[header]EXAMPLES[/header]\n" \
"$ codenotes add task Finish coding the tests --new-categoery Reminders\n" \
"$ codenotes add task Create documentation for the codenotes proyect; Release the proyect -p\n" \
"$ codenotes search note --today\n\n[header]FEEDBACK[/header]\nOpen an issue in [u]github.com/EGAMAGZ/codenotes[/u]"


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
    subparsers = parser.add_subparsers(dest='subargs')

    add = subparsers.add_parser('add')

    add_type_file = add.add_subparsers(dest='type')

    task = add_type_file.add_parser('task')
    task.add_argument('text', type=str, nargs='*', action='store')
    task.add_argument('--new-category', type=str, nargs='*', action='store')
    task.add_argument('--preview', '-p', action='store_true')

    note = add_type_file.add_parser('note')  # TODO: ADD ARGUMENT TO ADD FROM CLIPBOARD
    note.add_argument('text', type=str, nargs='*', action='store')
    note.add_argument('--title', '-t', type=str, nargs='*', action='store')
    note.add_argument('--category', '-c', type=str, nargs='*', action='store') #TODO: CHANGE TO CTAGEORY to CREATE IT IF NOT EXISTS
    note.add_argument('--preview', '-p', action='store_true')

    search = subparsers.add_parser('search')

    search.add_argument('type', choices=['note', 'task']) 
    search.add_argument('text', action='store', nargs='*')
    
    search_group = search.add_mutually_exclusive_group()

    search_group.add_argument('--today', '-t', action='store_true')
    search_group.add_argument('--yesterday', '-y', action='store_true')
    search_group.add_argument('--week', '-w', action='store_true')
    search_group.add_argument('--month', '-m', action='store_true')

    tui = subparsers.add_parser('tui')
    tui.add_argument('type', choices=['note', 'task'])

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
    
    PrintFormatted.print_help(USAGE_TEXT)


def main():
    """ Main function """
    args = parse_args(sys.argv[1:])
    if len(sys.argv) > 1:
        #* ADD <type>
        if args.subargs == 'add':
            if args.type == 'task':
                AddTask.set_args(args)

            elif args.type == 'note':
                AddNote.set_args(args)
        #*  SEARCH <type>
        elif args.subargs == 'search':
            if args.type == 'task':
                SearchTask.set_args(args)
            elif args.type == 'note':
                SearchNote.set_args(args)
    else:
        print_usage()
