import pathlib

import pytest
from typer.testing import CliRunner

from Pylette.cmd import pylette_app


@pytest.fixture
def test_image_as_url(requests_mock):
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"
    test_image_url = "https://my-test-image.com/test_image.png"
    with open(test_image, "rb") as f:
        requests_mock.get(test_image_url, content=f.read(), headers={"Content-Type": "image/png"})

        yield test_image_url


runner = CliRunner()


def test_app_no_input():
    result = runner.invoke(pylette_app, [])
    assert result.exit_code == 1
    assert "Please provide either a filename or an image-url" in result.stdout


def test_app_both_input():
    result = runner.invoke(pylette_app, ["--filename", "test.jpg", "--image-url", "https://test.com/image.jpg"])
    assert result.exit_code == 1
    assert "Please provide either a filename or an image-url, but not both" in result.stdout


def test_app_filename_nonexistent():
    result = runner.invoke(pylette_app, ["--filename", "this-file-does-definitely-not-exist.jpg"])
    assert result.exit_code == 1


def test_app_image_url(test_image_as_url):
    result = runner.invoke(pylette_app, ["--image-url", "https://my-test-image.com/test_image.png"])
    assert result.exit_code == 0


def test_app_image_path():
    result = runner.invoke(pylette_app, ["--filename", "tests/data/test_image.png"])
    assert result.exit_code == 0
