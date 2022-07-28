import pytest
from click.testing import CliRunner

from codenotes import main


class TestTaskCli:
    @pytest.mark.parametrize(
        "test_input,expected_code",
        [
            ("task create", 2),
            ("task create -c", 2),
            ("task create -c -m", 2),
            ('task create -c "TODOS" -m ', 2),
            ('task create -m -c "TODOS"', 2),
            ('task create -m "New Task" -m -c "TODOS"', 2),
        ],
    )
    def test_invalid_arguments_to_create_task(
            self, test_input, expected_code
    ) -> None:
        expected_message = "Error:"

        runner = CliRunner()
        result = runner.invoke(main, test_input)

        assert expected_message in result.output
        assert result.exit_code == expected_code

    def test_create_task_in_a_category_that_doesnt_exist(self) -> None:
        category = "New Category"
        expected_message = f'"{category}" category doesn\'t exist.'
        expected_code = 0

        args = f'task create -m "New task #1" -m "New task #2" -c "{category}"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output
        assert result.exit_code == expected_code

    @pytest.mark.parametrize(
        "test_input,expected_code,expected_message",
        [
            ('task create -m "New task #1" -c "TODOS"', 0,
             "Task #1 created successfully."),
            ('task create -m "New task #2" -m "New task #3" -c "TODOS"', 0,
             "Task #1 created successfully.\nTask #2 created successfully."),
        ],
    )
    def test_create_task_in_a_category_that_exists(
            self, test_input, expected_code, expected_message
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(main, test_input)

        assert expected_message in result.output
        assert result.exit_code == expected_code
