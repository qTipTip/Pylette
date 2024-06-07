import pathlib

import numpy as np
import pytest
from numpy.testing import assert_approx_equal

from Pylette.src.color_extraction import extract_colors


@pytest.fixture
def test_image_path_as_str():
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"

    yield str(test_image.absolute().resolve())


@pytest.fixture
def test_image_as_bytes():
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"

    with open(test_image, "rb") as f:
        yield f.read()


@pytest.fixture()
def test_kmean_extracted_palette(test_image_path_as_str):
    return extract_colors(
        image=test_image_path_as_str, palette_size=10, mode="KM", resize=True
    )


@pytest.mark.parametrize("palette_size", [1, 5, 10, 100])
@pytest.mark.parametrize(
    "extraction_mode",
    [
        "KM",
        pytest.param(
            "MC",
            marks=pytest.mark.skip(
                "Currently a bug in the MC algorithm, causing frequencies not summing to one"
            ),
        ),
    ],
)
def test_palette_invariants_with_image_path(
    test_image_path_as_str, palette_size, extraction_mode
):
    palette = extract_colors(
        image=test_image_path_as_str,
        palette_size=palette_size,
        mode=extraction_mode,
        resize=True,
    )

    assert (
        len(palette) == palette_size
    ), f"Expected {palette_size} colors in palette, got {len(palette)}"
    assert (
        palette.number_of_colors == palette_size
    ), f"Expected {palette_size} colors in palette, got {palette.number_of_colors}"
    assert (
        len(palette.colors) == palette_size
    ), f"Expected {palette_size} colors in palette, got {len(palette.colors)}"
    assert (
        palette.colors[0].freq >= palette.colors[-1].freq
    ), "Expected colors to be sorted by frequency in descending order"
    assert (
        palette.colors[0].freq > 0.0
    ), "Expected the most frequent color to have a frequency greater than 0.0"
    assert (
        palette.colors[0].freq <= 1.0
    ), "Expected the most frequent color to have a frequency less than or equal to 1.0"

    assert_approx_equal(
        sum(c.freq for c in palette.colors),
        1.0,
        err_msg="Expected the sum of all frequencies to be 1.0",
    )


@pytest.mark.parametrize("palette_size", [1, 5, 10, 100])
@pytest.mark.parametrize(
    "extraction_mode",
    [
        "KM",
        pytest.param(
            "MC",
            marks=pytest.mark.skip(
                "Currently a bug in the MC algorithm, causing frequencies not summing to one"
            ),
        ),
    ],
)
def test_palette_invariants_with_image_bytes(
    test_image_as_bytes, palette_size, extraction_mode
):
    palette = extract_colors(
        image_bytes=test_image_as_bytes,
        palette_size=palette_size,
        mode=extraction_mode,
        resize=True,
    )

    assert (
        len(palette) == palette_size
    ), f"Expected {palette_size} colors in palette, got {len(palette)}"
    assert (
        palette.number_of_colors == palette_size
    ), f"Expected {palette_size} colors in palette, got {palette.number_of_colors}"
    assert (
        len(palette.colors) == palette_size
    ), f"Expected {palette_size} colors in palette, got {len(palette.colors)}"
    assert (
        palette.colors[0].freq >= palette.colors[-1].freq
    ), "Expected colors to be sorted by frequency in descending order"
    assert (
        palette.colors[0].freq > 0.0
    ), "Expected the most frequent color to have a frequency greater than 0.0"
    assert (
        palette.colors[0].freq <= 1.0
    ), "Expected the most frequent color to have a frequency less than or equal to 1.0"

    assert_approx_equal(
        sum(c.freq for c in palette.colors),
        1.0,
        err_msg="Expected the sum of all frequencies to be 1.0",
    )


def test_colorspace_invariants_hls(test_kmean_extracted_palette):
    for color in test_kmean_extracted_palette:
        h, l, s = color.get_colors(colorspace="hls")
        assert 0 <= h <= 360, f"Expected 0 <= h <= 360, got {h}"
        assert 0 <= l <= 1, f"Expected 0 <= l <= 1, got {l}"
        assert 0 <= s <= 1, f"Expected 0 <= s <= 1, got {s}"


def test_colorspace_invariants_hsv(test_kmean_extracted_palette):
    for color in test_kmean_extracted_palette:
        h, s, v = color.get_colors(colorspace="hsv")
        assert 0 <= h <= 360, f"Expected 0 <= h <= 360, got {h}"
        assert 0 <= s <= 1, f"Expected 0 <= s <= 1, got {s}"
        assert 0 <= v <= 1, f"Expected 0 <= v <= 1, got {v}"


def test_colorspace_invariants_rgb(test_kmean_extracted_palette):
    for color in test_kmean_extracted_palette:
        r, g, b = color.rgb
        assert 0 <= r <= 255, f"Expected 0 <= r <= 255, got {r}"
        assert 0 <= g <= 255, f"Expected 0 <= g <= 255, got {g}"
        assert 0 <= b <= 255, f"Expected 0 <= b <= 255, got {b}"
