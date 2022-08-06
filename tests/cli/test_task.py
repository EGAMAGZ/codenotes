import pytest
from click.testing import CliRunner

from codenotes import main


class TestTaskCli:
    def setup_class(self) -> None:
        args = 'category create -c "TODOS"'

        runner = CliRunner()
        runner.invoke(main, args)

    @pytest.mark.parametrize(
        "args",
        [
            "task create",
            "task create -c",
            "task create -c -m",
            'task create -c "TODOS" -m ',
            'task create -m -c "TODOS"',
            'task create -m "New Task" -m -c "TODOS"',
        ],
    )
    def test_invalid_arguments_to_create_task(self, args) -> None:
        expected_code = 2

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert result.exit_code == expected_code

    def test_create_task_in_a_category_that_doesnt_exist(self) -> None:
        category = "New Category"
        expected_message = f'"{category}" category doesn\'t exist.'

        args = f'task create -m "New task #1" -m "New task #2" -c "{category}"'

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output

    @pytest.mark.parametrize(
        "args,expected_message",
        [
            (
                'task create -m "New task #1" -c "TODOS"',
                "Task #1 created successfully.",
            ),
            (
                'task create -m "New task #2" -m "New task #3" -c "TODOS"',
                "Task #1 created successfully.\nTask #2 created successfully.",
            ),
        ],
    )
    def test_create_task_in_a_category_that_exists(
        self, args, expected_message
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(main, args)

        assert expected_message in result.output

    @pytest.fixture(scope="class", autouse=True)
    def cleanup(self, request) -> None:
        def delete_test_category():
            runner = CliRunner()
            runner.invoke(main, 'category delete "TODOS" --force')

        request.addfinalizer(delete_test_category)
