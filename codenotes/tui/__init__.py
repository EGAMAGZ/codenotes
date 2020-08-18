import curses
import py_cui
from typing import List

WHITE_ON_MAGENTA = 11


class ImpPyCUI(py_cui.PyCUI):

    def __init__(self, num_rows, num_cols, auto_focus_buttons=True, exit_key=py_cui.keys.KEY_Q_LOWER,
                 simulated_terminal=None):
        super().__init__(num_rows, num_cols, auto_focus_buttons, exit_key, simulated_terminal)
        self.toggle_unicode_borders()

    def _initialize_colors(self):
        super()._initialize_colors()
        curses.init_pair(WHITE_ON_MAGENTA, curses.COLOR_WHITE, curses.COLOR_MAGENTA)


class AddTodoTUI:

    tasks_list_menu: py_cui.widgets.ScrollMenu
    todo_text_block: py_cui.widgets.TextBox

    def __init__(self, root: ImpPyCUI):
        self.root = root

        self.todo_text_block = self.root.add_text_box('New Todo Task', 0, 0, column_span=4)
        self.tasks_list_menu = self.root.add_scroll_menu('Todo tasks to add', 1, 0, column_span=4, row_span=4)

        self.__config()

    @classmethod
    def set_root(cls, root: ImpPyCUI):
        return cls(root)

    def _add_todo_task(self):
        text = self.todo_text_block.get()
        self.tasks_list_menu.add_item(text)
        self.todo_text_block.clear()

    def _remove_todo_task(self):
        self.tasks_list_menu.remove_selected_item()

    def _save_todo_tasks(self):
        pass

    def __config(self):
        self.todo_text_block.add_key_command(py_cui.keys.KEY_ENTER, self._add_todo_task)

        self.tasks_list_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self._remove_todo_task)

        self.root.set_title('Codenotes - Add TODO Tasks')
