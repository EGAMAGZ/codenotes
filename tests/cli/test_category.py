import unittest

from codenotes import parse_args
from codenotes.cli.category import CreateCategory


class TestCreateCategory(unittest.TestCase):

    def test_create_bad_input(self) -> None:
        args = parse_args(['category', 'create', ';', '--note'])
        create_category = CreateCategory(args)

        self.assertTrue(isinstance(create_category.category, list))
        self.assertListEqual(create_category.category, [])


    def test_create_one(self) -> None:
        args = parse_args(['category', 'create', 'New', 'category', '#1', '--task'])
        create_category = CreateCategory(args)

        self.assertTrue(isinstance(create_category.category, str))
        self.assertEqual(create_category.category, 'New category #1')

    def test_create_many(self) -> None:
        expected_categories = [
            'New category #2', 'New category #3'
        ]

        args = parse_args([
            'category', 'create', 'New','category', '#2',';', 'New','category', '#3', '--task'
            ])
        create_category = CreateCategory(args)

        self.assertTrue(isinstance(create_category.category, list))
        self.assertListEqual([
            'New category #2', 'New category #3'
        ], expected_categories)


if __name__ == '__main__':
    unittest.main()
