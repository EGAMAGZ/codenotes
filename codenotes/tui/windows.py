from typing import Final

from py_cui import PyCUI
from py_cui.widget_set import WidgetSet


class TaskWindow:

    COLUMNS: Final[int] = 5
    ROWS: Final[int] = 3

    root: PyCUI
    window: WidgetSet

    def __init__(self, root: PyCUI) -> None:
        """TaskWindow Constructor"""
        self.root = root
        self.window = self.root.create_new_widget_set(self.ROWS, self.COLUMNS)

        self.__config()

    def __config(self) -> None:
        pass

    @classmethod
    def create_widget_set(cls, root: PyCUI) -> WidgetSet:
        """
        Returns
        -------
        widget_set: WidgetSet
            Returns widgset preconfigured to be applied on root
        """
        return cls(root).window
