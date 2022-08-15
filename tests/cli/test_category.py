from datetime import date

import pytest
from click.testing import CliRunner

from codenotes import main


class TestCategoryCli:
    @pytest.mark.parametrize(
        "test_input",
        [
            "category create",
            "category create New category"
        ],
    )
    def test_invalid_argument_to_create_category(self, test_input) -> None:
        expected_code = 2

        runner = CliRunner()
        result = runner.invoke(main, test_input)

        assert result.exit_code == expected_code

    def test_create_new_category(self) -> None:
        expected_message = "Category created successfully."

        args = 'category create "TODOS"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output

    def test_create_category_that_exists(self) -> None:
        expected_message = (
            "Error trying to create category. Category might already exists."
        )

        args = 'category create "TODOS"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output

    @pytest.mark.parametrize(
        "args",
        [
            "category search",
            "category search New Category"
        ],
    )
    def test_invalid_arguments_to_search_category(self, args) -> None:
        expected_code = 2

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert result.exit_code == expected_code

    def test_search_category_that_not_exists(self) -> None:
        expected_message = "No categories found."

        args = 'category search "Sample"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output

    @pytest.mark.parametrize("category_name", ["TODOS", "OD", "OS", "DO"])
    def test_search_category_that_exists(self, category_name) -> None:
        expected_output = "TODOS"

        args = f'category search "{category_name}"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_output in result.output

    @pytest.mark.parametrize(
        "args",
        [
            "category show",
            'category show "TODOS" --max-items',
            "category show New Category",
        ],
    )
    def test_invalid_arguments_to_show_category(self, args) -> None:
        expected_code = 2

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert result.exit_code == expected_code

    def test_show_category_that_not_exists(self) -> None:
        expected_message = '"Sample" category doesn\'t exist.'

        args = 'category show "Sample"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output

    def test_show_category_that_exists(self) -> None:
        expected_date = str(date.today())
        expected_category = "TODOS"

        expected_tasks_found = "No task found"
        expected_total_tasks = "0"

        args = 'category show "TODOS"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_date in result.output
        assert expected_category in result.output

        assert expected_tasks_found in result.output
        assert expected_total_tasks in result.output

        assert result.exit_code == 0

    @pytest.mark.parametrize(
        "args",
        [
            "category delete",
            "category delete --force",
            "category delete Temp Category --force",
        ],
    )
    def test_invalid_arguments_to_delete_category(self, args) -> None:
        expected_exit_code = 2
        runner = CliRunner()
        result = runner.invoke(main, args)

        assert result.exit_code == expected_exit_code

    def test_delete_category_that_not_exists(self) -> None:
        category_name = "Sample"
        expected_message = "Category doesn't exist."

        args = f"category delete {category_name}"

        runner = CliRunner()
        result = runner.invoke(main, args, input=category_name)

        assert expected_message in result.output

    def test_delete_category_without_force(self) -> None:
        category_name = "TempCategory"

        runner = CliRunner()
        # Create a new category
        runner.invoke(main, f'category create "{category_name}"')
        # Search for the category created
        result = runner.invoke(main, f'category search "{category_name}"')

        assert category_name in result.output

        # Delete category
        expected_input_message = f"Type {category_name} to confirm deletion:"
        expected_output_message = "Category deleted successfully."
        result = runner.invoke(
            main, f'category delete "{category_name}"', input=category_name
        )

        assert expected_input_message in result.output
        assert expected_output_message in result.output

        # Check if category deleted exists
        expected_output_message = f'"{category_name}" category doesn\'t exist.'
        result = runner.invoke(main, f'category search "{category_name}"')

        assert expected_output_message not in result.output

    def test_delete_category_with_force(self) -> None:
        category_name = "Temp Category"

        runner = CliRunner()
        # Create a new category
        runner.invoke(main, f'category create "{category_name}"')
        # Search for the category created
        result = runner.invoke(main, f'category search "{category_name}"')

        assert category_name in result.output

        # Delete category
        expected_input_message = f"Type {category_name} to confirm deletion:"
        expected_output_message = "Category deleted successfully."
        result = runner.invoke(main,
                               f'category delete "{category_name}" --force')

        assert expected_input_message not in result.output
        assert expected_output_message in result.output

        # Check if category deleted exists
        expected_output_message = f'"{category_name}" category doesn\'t exist.'
        result = runner.invoke(main, f'category search "{category_name}"')

        assert expected_output_message not in result.output

    @pytest.fixture(scope="class", autouse=True)
    def cleanup(self, request) -> None:
        def delete_test_category():
            runner = CliRunner()
            runner.invoke(main, 'category delete "TODOS" --force')

        request.addfinalizer(delete_test_category)
