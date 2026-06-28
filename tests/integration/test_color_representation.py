"""
The canonical store is float sRGB in [0, 1]; 8-bit quantization happens only at
output boundaries (``.rgb``, ``.rgba``, ``.hex``).
"""

import colorsys

import numpy as np
import pytest
from PIL import Image

from pylette import Color, extract_colors
from pylette.types import ExtractionMethod


@pytest.fixture
def test_image() -> Image.Image:
    rng = np.random.default_rng(2024)
    arr = rng.integers(0, 256, size=(32, 32, 3), dtype=np.uint8)
    return Image.fromarray(arr, "RGB")


@pytest.mark.parametrize("mode", list(ExtractionMethod))
def test_rgb_is_plain_python_int_for_every_extractor(test_image: Image.Image, mode: ExtractionMethod) -> None:
    """Acceptance: ``all(isinstance(c, int) for c in color.rgb)`` for every extractor."""
    palette = extract_colors(test_image, palette_size=4, mode=mode)
    for color in palette.colors:
        assert all(isinstance(c, int) for c in color.rgb)
        assert all(not isinstance(c, np.integer) for c in color.rgb)


@pytest.mark.parametrize("mode", list(ExtractionMethod))
def test_rgb_float_in_unit_interval(test_image: Image.Image, mode: ExtractionMethod) -> None:
    palette = extract_colors(test_image, palette_size=4, mode=mode)
    for color in palette.colors:
        assert len(color.rgb_float) == 3
        assert all(isinstance(c, float) for c in color.rgb_float)
        assert all(0.0 <= c <= 1.0 for c in color.rgb_float)


def test_from_srgb_float_quantizes_to_rgb() -> None:
    red = Color.from_srgb_float((1.0, 0.0, 0.0), frequency=1.0)
    assert red.rgb == (255, 0, 0)
    assert red.hex == "#FF0000"
    assert red.rgb_float == (1.0, 0.0, 0.0)


def test_from_srgb_float_clamps_out_of_gamut() -> None:
    c = Color.from_srgb_float((1.5, -0.2, 0.5), frequency=1.0)
    assert c.rgb_float == (1.0, 0.0, 0.5)
    assert c.rgb == (255, 0, 128)


@pytest.mark.parametrize(
    "rgba, expected_hex",
    [
        ((255, 0, 0, 255), "#FF0000"),
        ((0, 255, 0, 255), "#00FF00"),
        ((142, 152, 174, 255), "#8E98AE"),
    ],
)
def test_hex_roundtrip_stable(rgba: tuple[int, int, int, int], expected_hex: str) -> None:
    """Round-trip ``Color -> hex -> Color`` is stable."""
    color = Color(rgba=rgba, frequency=0.5)
    assert color.hex == expected_hex

    r, g, b = color.rgb
    roundtripped = Color(rgba=(r, g, b, 255), frequency=0.5)
    assert roundtripped.hex == expected_hex
    assert roundtripped.rgb == color.rgb


def test_eight_bit_constructor_matches_legacy_hsv() -> None:
    """For 8-bit-constructed colors, derived spaces match the legacy formula."""
    color = Color(rgba=(142, 152, 174, 255), frequency=0.5)
    assert color.hsv == colorsys.rgb_to_hsv(142 / 255, 152 / 255, 174 / 255)
    assert color.hls == colorsys.rgb_to_hls(142 / 255, 152 / 255, 174 / 255)


def test_rgba_and_alpha_are_plain_ints() -> None:
    color = Color(rgba=(10, 20, 30, 128), frequency=0.5)
    assert color.rgba == (10, 20, 30, 128)
    assert isinstance(color.alpha, int)
    assert color.alpha == 128
    assert color.opacity == pytest.approx(128 / 255)


def test_alpha_and_opacity_are_derived() -> None:
    """`.alpha` is the raw 0-255 channel; `.opacity` is the [0, 1] float (P2a)."""
    color = Color.from_srgb_float((0.1, 0.2, 0.3), frequency=0.5, alpha=0.5)
    assert color.opacity == pytest.approx(0.5)
    assert color.alpha == 128  # round(0.5 * 255)
    assert color.rgba[3] == color.alpha


def test_frequency_is_canonical() -> None:
    color = Color(rgba=(10, 20, 30, 255), frequency=0.25)
    assert color.frequency == 0.25


@pytest.mark.parametrize(
    "deprecated_attr, canonical_attr",
    [("freq", "frequency"), ("weight", "opacity"), ("a", "alpha")],
)
def test_deprecated_aliases_warn_and_still_work(deprecated_attr: str, canonical_attr: str) -> None:
    """`.freq`, `.weight`, `.a` remain functional for one release with a warning."""
    color = Color(rgba=(10, 20, 30, 128), frequency=0.5)
    with pytest.warns(DeprecationWarning):
        deprecated_value = getattr(color, deprecated_attr)
    assert deprecated_value == getattr(color, canonical_attr)
