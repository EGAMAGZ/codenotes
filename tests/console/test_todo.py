import unittest
from typing import List

from codenotes.console.todo import AddTodo
from codenotes import parse_args


class TestOneTodo(unittest.TestCase):
    def setUp(self) -> None:
        args = parse_args(['add', 'todo', 'New todo task #1'])
        self.add_todo = AddTodo(args)

    def test_todo_text(self):
        self.assertTrue(isinstance(self.add_todo.todo_task, str))
        self.assertEqual(self.add_todo.todo_task, 'New todo task #1')


class TestManyTodos(unittest.TestCase):
    def setUp(self) -> None:
        args = parse_args(['add', 'todo', 'New todo task #1;New todo task #2'])
        self.add_todo = AddTodo(args)

    def test_todo_text(self):
        self.assertTrue(isinstance(self.add_todo.todo_task, List))
        self.assertListEqual(self.add_todo.todo_task, ['New todo task #1', 'New todo task #2'])


if __name__ == '__main__':
    unittest.main()
