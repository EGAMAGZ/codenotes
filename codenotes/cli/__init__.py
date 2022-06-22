from abc import ABC, abstractmethod

from codenotes.cli import print_formatted
from codenotes.cli.print_formatted import PrintFormatted


class BaseCLIAction(ABC):
    print_formatted: PrintFormatted

    def __init__(self):
        self.print_formatted = PrintFormatted()

    @abstractmethod
    def start(self) -> None: ...
