import curses
import py_cui


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

    def __init__(self, root: ImpPyCUI):
        self.root = root

        self.todo_text_block = self.root.add_text_box('New Todo Task', 0, 0, column_span=4)
        self.todo_tasks_list = self.root.add_scroll_menu('Todo tasks to add', 1, 0, column_span=4)

        self.__config()

    def __config(self):
        self.root.set_title('Codenotes - Add TODO Tasks')
