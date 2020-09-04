import sys
import argparse

from codenotes.console.tasks import AddTask, SearchTask


__version__ = '0.0.1'


def parse_args(args):

    parser = argparse.ArgumentParser(prog='codenotes')
    parser.add_argument('--version', '-v', action='version', version=__version__)
    subparsers = parser.add_subparsers(dest='subargs')

    add = subparsers.add_parser('add')

    type_file = add.add_subparsers(dest='type')

    task = type_file.add_parser('task')
    task.add_argument('text', type=str, nargs='*', action='store')
    task.add_argument('--preview', '-p', action='store_true')

    note = type_file.add_parser('note')
    note.add_argument('text', type=str, nargs='*', action='store')
    note.add_argument('--preview', '-p', action='store_true')

    search = subparsers.add_parser('search')

    search.add_argument('type', choices=['note', 'task'])
    search.add_argument('text', action='store', nargs='*')
    
    search_group = search.add_mutually_exclusive_group()

    search_group.add_argument('--today', '-t', action='store_true')
    search_group.add_argument('--yesterday', '-y', action='store_true')
    search_group.add_argument('--week', '-w', action='store_true')
    search_group.add_argument('--month', '-m', action='store_true')

    return parser.parse_args(args)


def main():

    args = parse_args(sys.argv[1:])
    print(args)
    if len(sys.argv) > 1:
        if args.subargs == 'add':
            if args.type == 'task':
                AddTask.set_args(args)
            elif args.type == 'note':
                pass
        elif args.subargs == 'search':
            if args.type == 'task':
                SearchTask.set_args(args)
    else:
        pass
