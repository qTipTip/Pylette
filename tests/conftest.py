import pathlib
from typing import Generator

import pytest


@pytest.fixture
def test_image_path_as_str() -> Generator[str, None, None]:
    test_image = pathlib.Path(__file__).parent / "data/test_image.png"

    yield str(test_image.absolute().resolve())


@pytest.fixture
def test_image_path_as_pathlike() -> Generator[pathlib.Path, None, None]:
    test_image = pathlib.Path(__file__).parent / "data/test_image.png"

    yield test_image


@pytest.fixture
def test_image_as_bytes() -> Generator[bytes, None, None]:
    test_image = pathlib.Path(__file__).parent / "data/test_image.png"

    with open(test_image, "rb") as f:
        yield f.read()


@pytest.fixture
def test_image_as_url(requests_mock) -> Generator[str, None, None]:  # type: ignore
    test_image = pathlib.Path(__file__).parent / "data/test_image.png"
    test_image_url = "https://my-test-image.com/test_image.png"
    with open(test_image, "rb") as f:
        requests_mock.get(test_image_url, content=f.read(), headers={"Content-Type": "image/png"})

        yield test_image_url
