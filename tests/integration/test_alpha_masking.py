"""
A regression test: median cut must not mis-shape pixels when alpha masking
removes some of them.

Before the fix, MedianCutExtractor reshaped to (height * width, n_channels).
After alpha masking the valid-pixel count can be < height * width, so that
reshape either raised or it silently produced an array with the wrong shape.
The extractor now reshapes by the array's actual length.
"""

import numpy as np
import pytest
from PIL import Image

from Pylette import extract_colors
from Pylette.types import ExtractionMethod


@pytest.fixture
def half_transparent_image() -> Image.Image:
    """64x64 RGBA image whose odd rows are fully transparent (alpha = 0)."""
    arr = np.zeros((64, 64, 4), dtype=np.uint8)
    arr[..., :3] = np.random.default_rng(0).integers(0, 256, (64, 64, 3))
    arr[::2, :, 3] = 255
    arr[1::2, :, 3] = 0
    return Image.fromarray(arr, "RGBA")


@pytest.mark.parametrize("mode", list(ExtractionMethod))
def test_extraction_survives_alpha_masking(half_transparent_image: Image.Image, mode: ExtractionMethod):
    # threshold=0 masks the fully-transparent rows, so valid pixels < height*width.
    palette = extract_colors(
        half_transparent_image,
        palette_size=5,
        mode=mode,
        resize=False,
        alpha_mask_threshold=0,
    )
    assert len(palette) <= 5
    assert sum(palette.frequencies) == pytest.approx(1.0)
