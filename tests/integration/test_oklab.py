"""Tests for the OKLab extractor.
These focus on the OKLab color math (must match Ottosson's reference vectors and
round-trip near machine precision).
"""

import numpy as np
import pytest
from PIL import Image

from Pylette import extract_colors
from Pylette.src.extractors.oklab import (
    linear_srgb_to_oklab,
    linear_to_srgb,
    oklab_to_linear_srgb,
    srgb_to_linear,
)
from Pylette.types import ExtractionMethod


class TestOKLabTransforms:
    # Reference vectors from Ottosson (linear sRGB -> OKLab).
    REFERENCES = [
        ((1.0, 1.0, 1.0), (1.0, 0.0, 0.0)),
        ((1.0, 0.0, 0.0), (0.627955, 0.224863, 0.125846)),
        ((0.0, 1.0, 0.0), (0.866440, -0.233888, 0.179498)),
        ((0.0, 0.0, 1.0), (0.452014, -0.032457, -0.311528)),
    ]

    @pytest.mark.parametrize("linear_rgb,expected_oklab", REFERENCES)
    def test_forward_matches_reference(self, linear_rgb, expected_oklab):
        got = linear_srgb_to_oklab(np.array([linear_rgb], dtype=float))[0]
        np.testing.assert_allclose(got, expected_oklab, atol=1e-5)

    def test_oklab_roundtrip_is_near_exact(self):
        rng = np.random.default_rng(0)
        lin = rng.random((5000, 3))
        rt = oklab_to_linear_srgb(linear_srgb_to_oklab(lin))
        np.testing.assert_allclose(lin, rt, atol=1e-10)

    def test_full_srgb8_pipeline_roundtrip(self):
        rng = np.random.default_rng(1)
        srgb = rng.integers(0, 256, size=(5000, 3)).astype(float) / 255.0
        back = linear_to_srgb(oklab_to_linear_srgb(linear_srgb_to_oklab(srgb_to_linear(srgb))))
        assert np.max(np.abs(srgb - back)) * 255 < 1e-6


class TestOKLabExtraction:
    @pytest.fixture
    def gradient_image(self) -> Image.Image:
        arr = np.zeros((64, 64, 3), dtype=np.uint8)
        xs = np.arange(64)
        arr[..., 0] = (xs[None, :] * 4) % 256
        arr[..., 1] = (xs[:, None] * 4) % 256
        arr[..., 2] = ((xs[None, :] + xs[:, None]) * 2) % 256
        return Image.fromarray(arr, "RGB")

    def test_respects_palette_size(self, gradient_image):
        palette = extract_colors(gradient_image, palette_size=6, mode=ExtractionMethod.OKLAB)
        assert len(palette) <= 6

    def test_frequencies_sum_to_one(self, gradient_image):
        palette = extract_colors(gradient_image, palette_size=5, mode=ExtractionMethod.OKLAB)
        assert sum(palette.frequencies) == pytest.approx(1.0)

    def test_colors_are_valid_rgb(self, gradient_image):
        palette = extract_colors(gradient_image, palette_size=5, mode=ExtractionMethod.OKLAB)
        for color in palette.colors:
            assert all(0 <= channel <= 255 for channel in color.rgb)

    def test_deterministic(self, gradient_image):
        a = extract_colors(gradient_image, palette_size=5, mode=ExtractionMethod.OKLAB)
        b = extract_colors(gradient_image, palette_size=5, mode=ExtractionMethod.OKLAB)
        assert [c.rgb for c in a.colors] == [c.rgb for c in b.colors]
