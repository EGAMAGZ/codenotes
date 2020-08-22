import unittest
from typing import List

from codenotes.console.todo import AddTodo
from codenotes import parse_args


class TestAddTodo(unittest.TestCase):

    def test_add_one_todo(self):
        args = parse_args(['add', 'todo', 'New todo task #1'])
        add_todo = AddTodo(args)
        self.assertTrue(isinstance(add_todo.todo_task, str))
        self.assertEqual(add_todo.todo_task, 'New todo task #1')

    def test_add_many_todos(self):
        args = parse_args(['add', 'todo', 'New todo task #1;New todo task #2'])
        add_todo = AddTodo(args)
        self.assertTrue(isinstance(add_todo.todo_task, List))
        self.assertListEqual(add_todo.todo_task, ['New todo task #1', 'New todo task #2'])

    def test_add_bad_input_todo(self):
        args = parse_args(['add', 'todo', ';'])
        add_todo = AddTodo(args)
        self.assertTrue(isinstance(add_todo.todo_task, List))
        self.assertListEqual(add_todo.todo_task, [])


if __name__ == '__main__':
    unittest.main()
