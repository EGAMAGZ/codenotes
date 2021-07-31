class MissingArgsException(Exception):
    """Exception raised if a required argparse argument is missing"""

    pass


class CategoryNotExistsError(Exception):
    """Exception raised after validation that a category doesn't exists"""

    pass
