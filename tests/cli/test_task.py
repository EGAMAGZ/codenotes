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
    def test_invalid_arguments_to_create_task(self, test_input,
                                              expected_code) -> None:
        expected_message = "Error:"

        runner = CliRunner()
        result = runner.invoke(main, test_input)

        assert expected_message in result.output
        assert result.exit_code == expected_code
