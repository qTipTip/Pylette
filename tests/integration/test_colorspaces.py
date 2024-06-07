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

    assert len(palette) == palette_size
    assert palette.number_of_colors == palette_size
    assert len(palette.colors) == palette_size
    assert palette.colors[0].freq >= palette.colors[-1].freq
    assert palette.colors[0].freq > 0.0
    assert palette.colors[0].freq <= 1.0

    assert_approx_equal(sum(c.freq for c in palette.colors), 1.0)
