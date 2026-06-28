import colorsys

import numpy as np
import pytest

from pylette import Color, InvalidColorspaceError
from pylette.src.colorspaces import linear_srgb_to_oklab, srgb_to_linear, srgb_to_oklab
from pylette.src.types import ColorSpace


@pytest.fixture
def sample() -> Color:
    return Color(rgba=(142, 152, 174, 255), frequency=0.5)


def test_to_rgb_returns_int_tuple(sample: Color) -> None:
    assert sample.to(ColorSpace.RGB) == sample.rgb
    assert sample.to("rgb") == sample.rgb


def test_to_hsv_and_hls_match_colorsys(sample: Color) -> None:
    srgb = sample.rgb_float
    assert sample.to(ColorSpace.HSV) == colorsys.rgb_to_hsv(*srgb)
    assert sample.to(ColorSpace.HLS) == colorsys.rgb_to_hls(*srgb)


def test_properties_and_get_colors_delegate_to_to(sample: Color) -> None:
    assert sample.hsv == sample.to(ColorSpace.HSV)
    assert sample.hls == sample.to(ColorSpace.HLS)
    assert sample.oklab == sample.to(ColorSpace.OKLAB)
    for space in ColorSpace:
        assert sample.get_colors(space) == sample.to(space)


def test_oklab_view_matches_shared_module(sample: Color) -> None:
    assert sample.to(ColorSpace.OKLAB) == srgb_to_oklab(sample.rgb_float)
    assert sample.to("oklab") == srgb_to_oklab(sample.rgb_float)


def test_oklab_single_color_matches_batched_transform() -> None:
    """The single-color helper must agree with the batched (N, 3) transform used
    by the extractor — i.e. one source of truth for the matrices."""
    srgb = (0.2, 0.6, 0.9)
    single = srgb_to_oklab(srgb)
    batched = linear_srgb_to_oklab(srgb_to_linear(np.asarray([srgb], dtype=np.float64)))[0]
    assert single == pytest.approx(tuple(batched))


def test_oklab_white_is_lightness_one() -> None:
    white = Color(rgba=(255, 255, 255, 255), frequency=1.0)
    L, a, b = white.oklab
    assert L == pytest.approx(1.0, abs=1e-6)
    assert a == pytest.approx(0.0, abs=1e-6)
    assert b == pytest.approx(0.0, abs=1e-6)


def test_unknown_space_raises_invalid_colorspace_error(sample: Color) -> None:
    with pytest.raises(InvalidColorspaceError):
        sample.to("not-a-space")
