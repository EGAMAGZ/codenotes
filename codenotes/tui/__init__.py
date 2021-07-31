from argparse import Namespace

import py_cui

from codenotes.tui.windows import TaskWindow


class ImpPyCUI(py_cui.PyCUI):
    def __init__(
        self,
        num_rows,
        num_cols,
        auto_focus_buttons=True,
        exit_key=py_cui.keys.KEY_Q_LOWER,
        simulated_terminal=None,
    ):
        """Initializer of ImpPyCUI class"""
        super().__init__(
            num_rows, num_cols, auto_focus_buttons, exit_key, simulated_terminal
        )
        self.toggle_unicode_borders()


class App:

    root: ImpPyCUI

    def __init__(self, root: ImpPyCUI, args: Namespace) -> None:
        self.root = root

        if args.type == "note":
            pass
        elif args.type == "task":
            self._set_task_widget_set()

    def _set_task_widget_set(self):
        self.root.apply_widget_set(TaskWindow.create_widget_set(self.root))

    def _set_note_widget_set(self):
        pass
