import argparse


__version__ = '0.0.1'


def main():

    parser = argparse.ArgumentParser(prog='codenotes')
    parser.add_argument('--version', '-v', action='version', version=__version__)
    subparsers = parser.add_subparsers(dest='subargs')

    add = subparsers.add_parser('add')
    add.add_argument('type', choices=['note', 'todo'], type=str)
    add.add_argument('text', type=str)

    search = subparsers.add_parser('search')
    search.add_argument('type', choices=['note', 'todo'])
    search.add_argument('text', action='store', nargs='?')
    search_group = search.add_mutually_exclusive_group()
    search_group.add_argument('--today', '-t', action='store_true')
    search_group.add_argument('--yesterday', '-y', action='store_true')
    search_group.add_argument('--week', '-w', action='store_true')
    search_group.add_argument('--month', '-m', action='store_true')

    args = parser.parse_args()

    if args.subargs == 'add':
        pass
    elif args.subargs == 'search':
        pass
