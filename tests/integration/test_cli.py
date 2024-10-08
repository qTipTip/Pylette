from typer.testing import CliRunner

from Pylette.cmd import pylette_app

runner = CliRunner()


def test_app_no_input():
    result = runner.invoke(pylette_app, [])
    assert result.exit_code == 1
    assert "Please provide either a filename or an image-url" in result.stdout


def test_app_both_input():
    result = runner.invoke(pylette_app, ["--filename", "test.jpg", "--image-url", "https://test.com/image.jpg"])
    assert result.exit_code == 1
    assert "Please provide either a filename or an image-url, but not both" in result.stdout
