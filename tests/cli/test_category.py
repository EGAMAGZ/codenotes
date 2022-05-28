import pytest
from click.testing import CliRunner

from codenotes import main


class TestCategoryCli:
    @pytest.mark.parametrize('test_input,expected', [("category create", 2), ("category create -c", 2)])
    def test_invalid_argument(self, test_input, expected) -> None:
        runner = CliRunner()
        result = runner.invoke(main, test_input)
        assert result.exit_code == expected

    def test_input_category_name(self) -> None:
        args = 'category create -c "Sample of category"'

        runner = CliRunner()
        result = runner.invoke(main, args)
        assert result.exit_code == 0
