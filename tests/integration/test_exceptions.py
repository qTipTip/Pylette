"""
Every Pylette-originated failure derives from ``PyletteError`` and is
identified by its type, while remaining a ``ValueError`` for backward
compatibility.
"""

import numpy as np
import pytest
from PIL import Image

from pylette import (
    InvalidColorspaceError,
    InvalidImageError,
    NoValidPixelsError,
    PyletteError,
    UnknownExtractionMethodError,
    batch_extract_colors,
    extract_colors,
)
from pylette.src.color import Color
from pylette.src.extractors.registry import get_extractor


@pytest.fixture
def opaque_image() -> Image.Image:
    arr = np.random.default_rng(0).integers(0, 256, (16, 16, 3), dtype=np.uint8)
    return Image.fromarray(arr, "RGB")


@pytest.fixture
def fully_transparent_image() -> Image.Image:
    """16x16 RGBA image that is fully transparent (alpha = 0 everywhere)."""
    arr = np.zeros((16, 16, 4), dtype=np.uint8)
    arr[..., :3] = 200
    return Image.fromarray(arr, "RGBA")


def test_unsupported_image_type_raises_invalid_image_error() -> None:
    with pytest.raises(InvalidImageError):
        extract_colors(12345)  # type: ignore[arg-type]


def test_missing_file_raises_invalid_image_error() -> None:
    with pytest.raises(InvalidImageError):
        extract_colors("does/not/exist.png")


def test_corrupt_bytes_raise_invalid_image_error() -> None:
    with pytest.raises(InvalidImageError):
        extract_colors(b"not a real image")


def test_invalid_url_image_raises_invalid_image_error(requests_mock) -> None:  # type: ignore[no-untyped-def]
    url = "https://example.com/not-an-image"
    requests_mock.get(url, text="<html>nope</html>", headers={"Content-Type": "text/html"})
    with pytest.raises(InvalidImageError):
        extract_colors(url)


def test_fully_masked_image_raises_no_valid_pixels_error(fully_transparent_image: Image.Image) -> None:
    """The all-masked #76 case stays pinned to a typed error."""
    with pytest.raises(NoValidPixelsError):
        extract_colors(fully_transparent_image, alpha_mask_threshold=0, resize=None)


def test_unknown_mode_raises_unknown_extraction_method_error(opaque_image: Image.Image) -> None:
    with pytest.raises(UnknownExtractionMethodError):
        extract_colors(opaque_image, mode="NotARealMethod")


def test_get_extractor_unknown_raises_unknown_extraction_method_error() -> None:
    with pytest.raises(UnknownExtractionMethodError):
        get_extractor("NotARealMethod")


def test_invalid_colorspace_in_to_json_raises_invalid_colorspace_error(opaque_image: Image.Image) -> None:
    palette = extract_colors(opaque_image, palette_size=2)
    with pytest.raises(InvalidColorspaceError):
        palette.to_json(colorspace="not-a-space")


def test_invalid_colorspace_in_color_to_raises_invalid_colorspace_error() -> None:
    color = Color(rgba=(10, 20, 30, 255), frequency=1.0)
    with pytest.raises(InvalidColorspaceError):
        color.to("not-a-space")


@pytest.mark.parametrize(
    "exc_cls",
    [InvalidImageError, NoValidPixelsError, UnknownExtractionMethodError, InvalidColorspaceError],
)
def test_every_error_is_a_pylette_error_and_value_error(exc_cls: type[PyletteError]) -> None:
    """Acceptance: ``except PyletteError`` catches all; ``except ValueError`` still works."""
    assert issubclass(exc_cls, PyletteError)
    assert issubclass(exc_cls, ValueError)


def test_pylette_error_catches_pipeline_failures(opaque_image: Image.Image) -> None:
    with pytest.raises(PyletteError):
        extract_colors(opaque_image, mode="bogus")


def test_batch_classifies_failures_by_exception_type(opaque_image: Image.Image, tmp_path) -> None:
    """The batch layer preserves the typed exception per failed source."""
    good = tmp_path / "good.png"
    opaque_image.save(good)

    results = batch_extract_colors(images=[str(good), 12345])  # type: ignore[list-item]
    by_success = {r.success: r for r in results}

    assert by_success[True].palette is not None
    failed = by_success[False]
    assert isinstance(failed.error, InvalidImageError)
    assert isinstance(failed.error, PyletteError)
