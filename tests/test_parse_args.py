import unittest

from codenotes import parse_args


class TestAddTodoParseArgs(unittest.TestCase):

    def test_add_task_empty(self):
        expected_vars = {'subargs': 'add', 'type': 'task', 'text': [], 'preview': False}
        args = parse_args(['add', 'task'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_task_one(self):
        expected_vars = {'subargs': 'add', 'type': 'task', 'text': ['New', 'task', '#1'], 'preview': False}
        args = parse_args(['add', 'task', 'New', 'task', '#1'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_task_many(self):
        expected_vars = {'subargs': 'add', 'type': 'task', 'text': ['New', 'task', '#1;', 'New', 'task', 'task', '#2'], 'preview': False}
        args = parse_args(['add', 'task', 'New', 'task', '#1;', 'New', 'task', 'task', '#2'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_task_preview(self):
        expected_vars = {'subargs': 'add', 'type': 'task', 'text': ['New', 'task', '#1'], 'preview': True}
        args = parse_args(['add', 'task', 'New', 'task', '#1', '-p'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)


class TestSearchTodoParseArgs(unittest.TestCase):
    
    def test_search_two_dates(self):
        self.assertRaises(SystemExit, parse_args, ['search', 'task', '--today', '--month'])

    def test_search_today_task(self):
        expected_vars = {'month': False, 'subargs': 'search', 'text': [], 'today': True, 'type': 'task', 'week': False, 'yesterday': False}
        args = parse_args(['search', 'task', '--today'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_search_text_task(self):
        expected_vars = {'month': False, 'subargs': 'search', 'text': ['New', 'task'], 'today': False, 'type': 'task', 'week': False, 'yesterday': False}
        args = parse_args(['search', 'task', 'New', 'task'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)


if __name__ == '__main__':
    unittest.main()
