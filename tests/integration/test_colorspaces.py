import pathlib

import numpy as np
import pytest
from numpy.testing import assert_approx_equal

from Pylette.src.color_extraction import extract_colors


@pytest.fixture
def test_image_path_as_str():
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"

    yield str(test_image.absolute().resolve())


@pytest.mark.parametrize("palette_size", [1, 5, 10])
@pytest.mark.parametrize("extraction_mode", ["KM", "MC"])
def test_palette_invariants_with_image_path(
    test_image_path_as_str, palette_size, extraction_mode
):
    palette = extract_colors(
        image=test_image_path_as_str, palette_size=palette_size, mode=extraction_mode
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
