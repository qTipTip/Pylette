from typer.testing import CliRunner

from Pylette.cmd import pylette_app

runner = CliRunner()


def test_cli_no_input_is_help():
    result = runner.invoke(pylette_app, [])
    assert result.exit_code == 0

    result_help = runner.invoke(pylette_app, ["--help"])
    assert result_help.exit_code == 0
    assert result_help.stdout == result.stdout


def test_cli_both_input():
    result = runner.invoke(pylette_app, ["--filename", "test.jpg", "--image-url", "https://test.com/image.jpg"])
    assert result.exit_code == 1
    assert "Please provide either a filename or an image-url, but not both" in result.stdout


def test_cli_filename_nonexistent():
    result = runner.invoke(pylette_app, ["--filename", "this-file-does-definitely-not-exist.jpg"])
    assert result.exit_code == 1


def test_cli_image_url(test_image_as_url):
    result = runner.invoke(pylette_app, ["--image-url", test_image_as_url])
    assert result.exit_code == 0


def test_cli_image_path(test_image_path_as_str):
    result = runner.invoke(pylette_app, ["--filename", test_image_path_as_str])
    assert result.exit_code == 0


def test_cli_all_options(test_image_path_as_str, tmp_path):
    tmp_output_file = tmp_path / "output.csv"

    result = runner.invoke(
        pylette_app,
        [
            "--filename",
            test_image_path_as_str,
            "--n",
            "10",
            "--sort-by",
            "frequency",
            "--stdout",
            "--out-filename",
            tmp_output_file,
            "--no-display-colors",
            "--colorspace",
            "hsv",
        ],
    )
    assert result.exit_code == 0
    assert len(result.stdout.splitlines()) == 10
    assert tmp_output_file.exists()

    with tmp_output_file.open() as f:
        assert len(f.readlines()) == 10


def test_pylette_help():
    result = runner.invoke(pylette_app, ["--help"])
    assert result.exit_code == 0
