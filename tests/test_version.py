from typer.testing import CliRunner

from cosmic_slop_cli import __version__
from cosmic_slop_cli.__main__ import app

runner: CliRunner = CliRunner()


def test_version():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        # assert result.output.startswith("cosmic_slop_cli, version ")
        assert result.output.strip() == (f"cosmic_slop_cli, version {__version__}")
