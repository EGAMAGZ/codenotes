import unittest

from codenotes import parse_args
from codenotes.cli.category import CreateCategory, SearchCategory


class TestCreateCategory(unittest.TestCase):
    def test_create_bad_input(self) -> None:
        args = parse_args(["category", "create", ";", "--note"])
        create_category = CreateCategory(args)

        self.assertTrue(isinstance(create_category.category_name, list))
        self.assertListEqual(create_category.category_name, [])

    def test_create_one(self) -> None:
        expected_category = "New category #1"

        args = parse_args(["category", "create", "New", "category", "#1", "--task"])
        create_category = CreateCategory(args)

        self.assertTrue(isinstance(create_category.category_name, str))
        self.assertEqual(create_category.category_name, expected_category)

        # TODO: CREATE NEW CATEGORY IN NOTES, AND TEST IT

    def test_create_many(self) -> None:
        expected_categories = ["New category #2", "New category #3"]

        args = parse_args(
            ["category", "create", "New", "category", "#2", ";", "New", "category", "#3", "--task"]
        )
        create_category = CreateCategory(args)

        self.assertTrue(isinstance(create_category.category_name, list))
        self.assertListEqual(create_category.category_name, expected_categories)


class TestSearchCategory(unittest.TestCase):
    def test_search_notes(self) -> None:
        expected_categories = [[("General",)]]

        args = parse_args(["category", "search", "--note"])

        query = SearchCategory(args).sql_query()
        self.assertListEqual(query, expected_categories)

        expected_categories = [[("General",)]]

        args = parse_args(["category", "search", "Gen", "--note"])

        query = SearchCategory(args).sql_query()
        self.assertListEqual(query, expected_categories)

    def test_search_tasks(self) -> None:
        expected_categories = [
            [
                ("TODO Tasks",),
                ("New category #2",),
                ("New category #3",),
                ("New category #1",),
            ]
        ]

        args = parse_args(["category", "search", "--task"])

        query = SearchCategory(args).sql_query()
        self.assertListEqual(query, expected_categories)

        expected_categories = [
            [("New category #2",), ("New category #3",), ("New category #1",)]
        ]

        args = parse_args(["category", "search", "categ", "--task"])

        query = SearchCategory(args).sql_query()
        self.assertListEqual(query, expected_categories)

    def test_search_all(self) -> None:
        expected_categories = [
            [
                ("TODO Tasks",),
                ("New category #2",),
                ("New category #3",),
                ("New category #1",),
            ],
            [("General",)],
        ]

        args = parse_args(["category", "search", "--all"])

        query = SearchCategory(args).sql_query()
        self.assertListEqual(query, expected_categories)

        expected_categories = [
            [("New category #2",), ("New category #3",), ("New category #1",)],
            [("General",)],
        ]

        args = parse_args(["category", "search", "ne", "--all"])

        query = SearchCategory(args).sql_query()
        self.assertListEqual(query, expected_categories)


if __name__ == "__main__":
    unittest.main()
