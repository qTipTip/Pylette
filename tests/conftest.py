import pathlib

import pytest


@pytest.fixture
def test_image_path_as_str():
    test_image = pathlib.Path(__file__).parent / "data/test_image.png"

    yield str(test_image.absolute().resolve())


@pytest.fixture
def test_image_path_as_pathlike():
    test_image = pathlib.Path(__file__).parent / "data/test_image.png"

    yield test_image


@pytest.fixture
def test_image_as_bytes():
    test_image = pathlib.Path(__file__).parent / "data/test_image.png"

    with open(test_image, "rb") as f:
        yield f.read()


@pytest.fixture
def test_image_as_url(requests_mock):
    test_image = pathlib.Path(__file__).parent / "data/test_image.png"
    test_image_url = "https://my-test-image.com/test_image.png"
    with open(test_image, "rb") as f:
        requests_mock.get(test_image_url, content=f.read(), headers={"Content-Type": "image/png"})

        yield test_image_url
