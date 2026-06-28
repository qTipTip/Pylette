"""
`resize` accepts an int sample size or None (no resize)
"""

import numpy as np
import pytest
from PIL import Image

from pylette import batch_extract_colors, extract_colors

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")


@pytest.fixture
def image() -> Image.Image:
    # Distinctive, non-square original size so "no resize" is detectable.
    arr = np.random.default_rng(0).integers(0, 256, (30, 40, 3), dtype=np.uint8)
    return Image.fromarray(arr, "RGB")


def _processed_size(palette) -> tuple[int, int]:  # type: ignore[no-untyped-def]
    assert palette.metadata
    return palette.metadata["image_info"]["processed_size"]


def test_default_resize_is_256(image: Image.Image) -> None:
    palette = extract_colors(image)
    assert _processed_size(palette) == (256, 256)
    assert palette.metadata["extraction_params"]["resize"] == 256


def test_explicit_int_resize(image: Image.Image) -> None:
    palette = extract_colors(image, resize=64)
    assert _processed_size(palette) == (64, 64)
    assert palette.metadata["extraction_params"]["resize"] == 64


def test_none_disables_resize(image: Image.Image) -> None:
    palette = extract_colors(image, resize=None)
    # PIL size is (width, height) == (40, 30) for a (30, 40, 3) array.
    assert _processed_size(palette) == (40, 30)
    assert palette.metadata["extraction_params"]["resize"] is None


def test_invalid_resize_raises(image: Image.Image) -> None:
    with pytest.raises(ValueError):
        extract_colors(image, resize=0)
    with pytest.raises(ValueError):
        extract_colors(image, resize=-5)


def test_default_call_emits_no_deprecation_warning(image: Image.Image) -> None:
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        extract_colors(image)  # default resize=256, must not warn


@pytest.mark.parametrize("flag, expected_size", [(True, (256, 256)), (False, (40, 30))])
def test_bool_resize_is_deprecated_but_works(image: Image.Image, flag: bool, expected_size: tuple[int, int]) -> None:
    with pytest.warns(DeprecationWarning):
        palette = extract_colors(image, resize=flag)
    assert _processed_size(palette) == expected_size


def test_batch_bool_resize_is_deprecated_but_works(image: Image.Image, tmp_path) -> None:  # type: ignore[no-untyped-def]
    # batch uses each source as a dict key, so sources must be hashable (paths).
    paths = []
    for i in range(2):
        p = tmp_path / f"img_{i}.png"
        image.save(p)
        paths.append(str(p))

    with pytest.warns(DeprecationWarning):
        results = batch_extract_colors(paths, resize=True)
    assert all(r.success for r in results)
    assert all(_processed_size(r.palette) == (256, 256) for r in results)
