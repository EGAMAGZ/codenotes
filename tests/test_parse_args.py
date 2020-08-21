import unittest

from codenotes import parse_args


class TestAddTodoParseArgs(unittest.TestCase):

    def test_add_todo_empty(self):
        expected_vars = {'subargs': 'add', 'type': 'todo', 'text': [], 'preview': False}
        args = parse_args(['add', 'todo'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_todo_one(self):
        expected_vars = {'subargs': 'add', 'type': 'todo', 'text': ['New', 'task', '#1'], 'preview': False}
        args = parse_args(['add', 'todo', 'New', 'task', '#1'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_todo_many(self):
        expected_vars = {'subargs': 'add', 'type': 'todo', 'text': ['New', 'task', '#1;', 'New', 'todo', 'task', '#2'], 'preview': False}
        args = parse_args(['add', 'todo', 'New', 'task', '#1;', 'New', 'todo', 'task', '#2'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_todo_preview(self):
        expected_vars = {'subargs': 'add', 'type': 'todo', 'text': ['New', 'task', '#1'], 'preview': True}
        args = parse_args(['add', 'todo', 'New', 'task', '#1', '-p'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)


class TestSearchTodoParseArgs(unittest.TestCase):
    
    def test_search_two_dates(self):
        self.assertRaises(SystemExit,parse_args,['search', 'todo', '--today','--month'])

    def test_search_today_todo(self):
        expected_vars = {'month':False, 'subargs':'search', 'text':[],'today':True, 'type':'todo','week':False,'yesterday':False}
        args = parse_args(['search', 'todo', '--today'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_search_text_todo(self):
        expected_vars = {'month':False, 'subargs':'search', 'text':['New','task'],'today':False, 'type':'todo','week':False,'yesterday':False}
        args = parse_args(['search', 'todo', 'New', 'task'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

if __name__ == '__main__':
    unittest.main()
