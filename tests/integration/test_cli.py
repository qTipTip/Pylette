from pathlib import Path

from typer.testing import CliRunner

from Pylette.cmd import pylette_app

runner = CliRunner()


def test_cli_no_input_is_error():
    result = runner.invoke(pylette_app, [])
    assert result.exit_code == 2
    assert "Usage: main [OPTIONS] IMAGE_SOURCES..." in result.stderr

    result_help = runner.invoke(pylette_app, ["--help"])
    assert result_help.exit_code == 0
    assert "--mode" in result_help.stdout


def test_cli_both_input(test_image_as_url: str, test_image_path_as_str: str):
    result = runner.invoke(pylette_app, [test_image_path_as_str, test_image_as_url])
    assert result.exit_code == 0


def test_cli_filename_nonexistent():
    result = runner.invoke(pylette_app, ["this-file-does-definitely-not-exist.jpg"])
    assert result.exit_code == 1


def test_cli_filename_partial_failure(test_image_as_url: str):
    result = runner.invoke(pylette_app, [test_image_as_url, "this-file-does-definitely-not-exist.jpg"])
    assert result.exit_code == 2


def test_cli_image_url(test_image_as_url: str):
    result = runner.invoke(pylette_app, [test_image_as_url])
    assert result.exit_code == 0


def test_cli_image_path(test_image_path_as_str: str):
    result = runner.invoke(pylette_app, [test_image_path_as_str])
    assert result.exit_code == 0


def test_cli_all_options(test_image_path_as_str: str, tmp_path: Path):
    tmp_output_file = tmp_path / "output.csv"

    result = runner.invoke(
        pylette_app,
        [
            test_image_path_as_str,
            "--n",
            "10",
            "--sort-by",
            "frequency",
            "--stdout",
            "--out-filename",
            str(tmp_output_file),
            "--no-display-colors",
            "--colorspace",
            "hsv",
        ],
    )
    assert result.exit_code == 0
    assert tmp_output_file.exists()

    with tmp_output_file.open() as f:
        assert len(f.readlines()) == 10


def test_pylette_help():
    result = runner.invoke(pylette_app, ["--help"])
    assert result.exit_code == 0


def test_alpha_mask_filters_all_pixels(test_image_path_as_str: str):
    result = runner.invoke(pylette_app, [test_image_path_as_str, "--alpha-mask-threshold", "255"])
    assert result.exit_code == 1
    assert "No valid pixels remain after applying alpha mask" in result.stderr
