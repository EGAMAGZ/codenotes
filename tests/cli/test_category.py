import pytest
from click.testing import CliRunner

from codenotes import main


class TestCategoryCli:
    @pytest.mark.parametrize(
        "test_input,expected",
        [("category create", 2), ("category create -c", 2)]
    )
    def test_invalid_argument_to_create_category(self, test_input,
                                                 expected) -> None:
        expected_message = "Error:"

        runner = CliRunner()
        result = runner.invoke(main, test_input)

        assert expected_message in result.output
        assert result.exit_code == expected

    def test_create_new_category(self) -> None:
        expected_message = "Task saved successfully"

        args = 'category create -c "TODOS"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output
        assert result.exit_code == 0

    def test_create_category_that_already_exists(self) -> None:
        expected_message = "Error trying to create category. Category might " \
                           "already exists."

        args = 'category create -c "TODOS"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output
        assert result.exit_code == 0

    @pytest.mark.parametrize(
        "test_input,expected",
        [("category search", 2), ("category search -c", 2)]
    )
    def test_invalid_arguments_to_search_category(self, test_input,
                                                  expected) -> None:
        expected_message = "Error:"

        runner = CliRunner()
        result = runner.invoke(main, test_input)

        assert expected_message in result.output
        assert result.exit_code == expected

    def test_search_category_that_exists(self) -> None:
        expected_message = "TODOS"

        args = 'category search -c "TODOS"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output
        assert result.exit_code == 0

    def test_search_category_that_not_exists(self) -> None:
        expected_message = "No categories found."

        args = 'category search -c "Sample"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output
        assert result.exit_code == 0
