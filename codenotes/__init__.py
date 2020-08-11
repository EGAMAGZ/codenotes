import argparse


__version__ = '0.0.1'


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v', action='version', version=__version__)
    subparsers = parser.add_subparsers(dest='subargs')

    add = subparsers.add_parser('add')
    add.add_argument('type', choices=['note', 'todo'], type=str)
    add.add_argument('text', type=str)

    search = subparsers.add_parser('search')
    search.add_argument('type', choices=['note', 'todo'])
    search.add_argument('text', type=str)

    args = parser.parse_args()
