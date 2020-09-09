import unittest

from codenotes import parse_args


class TestAddTaskParseArgs(unittest.TestCase):
    def test_add_new_category(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'task',
            'text': [],
            'new_category': ['CLI', 'Category'],
            'preview': False
        }
        args = parse_args(['add', 'task', '--new-category', 'CLI', 'Category'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_new_category_empty(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'task',
            'text': [],
            'new_category': [],
            'preview': False
        }
        args = parse_args(['add', 'task', '--new-category'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_task_empty(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'task',
            'text': [],
            'new_category': None,
            'preview': False
        }
        args = parse_args(['add', 'task'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_task_one(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'task',
            'text': ['New', 'task', '#1'],
            'new_category': None,
            'preview': False
        }
        args = parse_args(['add', 'task', 'New', 'task', '#1'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_task_many(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'task',
            'text': ['New', 'task', '#1;', 'New', 'task', 'task', '#2'],
            'new_category': None,
            'preview': False
        }
        args = parse_args(['add', 'task', 'New', 'task', '#1;', 'New', 'task', 'task', '#2'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_task_preview(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'task',
            'text': ['New', 'task', '#1'],
            'new_category': None,
            'preview': True
        }
        args = parse_args(['add', 'task', 'New', 'task', '#1', '-p'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)


class TestSearchTaskParseArgs(unittest.TestCase):
    
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


class TestAddNoteParseArgs(unittest.TestCase):

    def test_add_new_category(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'note',
            'text': [],
            'title': None,
            'new_category': ['New', 'category'],
            'preview': False
        }
        args = parse_args(['add', 'note', '--new-category', 'New', 'category'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_new_category_empty(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'note',
            'text': [],
            'title': None,
            'new_category': [],
            'preview': False
        }
        args = parse_args(['add', 'note', '--new-category'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_new_note(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'note',
            'text': ['New', 'task'],
            'title': None,
            'new_category': None,
            'preview': False
        }
        args = parse_args(['add', 'note', 'New', 'task'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_new_note_empty(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'note',
            'text': [],
            'title': None,
            'new_category': None,
            'preview': False
        }
        args = parse_args(['add', 'note'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_new_note_preview(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'note',
            'text': [],
            'title': None,
            'new_category': None,
            'preview': True
        }
        args = parse_args(['add', 'note', '--preview'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)

    def test_add_new_note_title(self):
        expected_vars = {
            'subargs': 'add',
            'type': 'note',
            'text': ['New', 'task'],
            'title': ['Task','title'],
            'new_category': None,
            'preview': False
        }
        args = parse_args(['add', 'note', 'New', 'task', '--title', 'Task', 'title'])
        args_vars = vars(args)
        self.assertDictEqual(args_vars, expected_vars)


if __name__ == '__main__':
    unittest.main()
