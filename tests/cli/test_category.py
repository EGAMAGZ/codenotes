from click.testing import CliRunner

from codenotes import main


class TestCategoryCli:
    def test_missing_category_name(self):
        args = tuple("category create".split(" "))

        runner = CliRunner()
        result = runner.invoke(main, args)
        assert result.exit_code == 2

    def test_input_category_name(self):
        args = tuple("category create Sample of category".split(" "))

        runner = CliRunner()
        result = runner.invoke(main, args)
        assert result.exit_code == 0
