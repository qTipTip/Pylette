"""
These property tests correspond to the "Guarantees" section documented on ``extract_colors``.

The tests are parametrized over ``available_methods()`` so a newly registered
extractor is covered automatically. A Hypothesis property test fuzzes arbitrary
small images to catch degenerate inputs.
"""

import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
from PIL import Image

from pylette import NoValidPixelsError, Palette, extract_colors
from pylette.src.extractors import available_methods

METHODS = available_methods()

# Degenerate images make KMeans/OKLab emit sklearn ConvergenceWarnings; that is
# expected here and not what these tests are about.
pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")


def _assert_palette_invariants(palette: Palette, palette_size: int) -> None:
    # len(palette) <= palette_size
    assert len(palette) <= palette_size
    if len(palette) == 0:
        return
    # sum(frequencies) ~= 1.0
    assert sum(palette.frequencies) == pytest.approx(1.0)
    for color in palette.colors:
        # every channel in-gamut, plain Python ints
        assert all(isinstance(channel, int) and 0 <= channel <= 255 for channel in color.rgb)


@pytest.mark.parametrize("mode", METHODS)
@pytest.mark.parametrize("palette_size", [1, 3, 5])
@pytest.mark.parametrize("resize", [True, False])
def test_solid_image_is_handled(mode: str, palette_size: int, resize: bool) -> None:
    img = Image.new("RGB", (8, 8), (12, 200, 75))
    palette = extract_colors(img, palette_size=palette_size, mode=mode, resize=resize)
    _assert_palette_invariants(palette, palette_size)
    assert len(palette) >= 1


@pytest.mark.parametrize("mode", METHODS)
def test_one_by_one_image_is_handled(mode: str) -> None:
    img = Image.fromarray(np.array([[[10, 20, 30]]], dtype=np.uint8), "RGB")
    palette = extract_colors(img, palette_size=5, mode=mode, resize=False)
    _assert_palette_invariants(palette, 5)
    assert len(palette) >= 1


@pytest.mark.parametrize("mode", METHODS)
def test_palette_size_exceeds_distinct_colors(mode: str) -> None:
    arr = np.array([[[0, 0, 0], [255, 255, 255]], [[255, 0, 0], [0, 0, 255]]], dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    palette = extract_colors(img, palette_size=10, mode=mode, resize=False)
    _assert_palette_invariants(palette, 10)


@pytest.mark.parametrize("mode", METHODS)
def test_partial_alpha_mask_is_handled(mode: str) -> None:
    arr = np.zeros((16, 16, 4), dtype=np.uint8)
    arr[..., :3] = np.random.default_rng(0).integers(0, 256, (16, 16, 3))
    arr[::2, :, 3] = 255  # half opaque, half transparent
    img = Image.fromarray(arr, "RGBA")
    palette = extract_colors(img, palette_size=5, mode=mode, resize=False, alpha_mask_threshold=0)
    _assert_palette_invariants(palette, 5)


@pytest.mark.parametrize("mode", METHODS)
def test_total_alpha_mask_raises_typed_error(mode: str) -> None:
    arr = np.zeros((16, 16, 4), dtype=np.uint8)  # alpha = 0 everywhere
    img = Image.fromarray(arr, "RGBA")
    with pytest.raises(NoValidPixelsError):
        extract_colors(img, palette_size=5, mode=mode, resize=False, alpha_mask_threshold=0)


@pytest.mark.parametrize("mode", METHODS)
def test_deterministic_under_fixed_random_state(mode: str) -> None:
    arr = np.random.default_rng(7).integers(0, 256, (20, 20, 3), dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    a = extract_colors(img, palette_size=5, mode=mode)
    b = extract_colors(img, palette_size=5, mode=mode)
    assert [c.rgb for c in a.colors] == [c.rgb for c in b.colors]
    assert [c.frequency for c in a.colors] == [c.frequency for c in b.colors]


@pytest.mark.parametrize("mode", METHODS)
@pytest.mark.parametrize(
    "sort_mode, key, reverse",
    [
        ("luminance", lambda c: c.luminance, False),
        ("frequency", lambda c: c.frequency, True),
    ],
)
def test_sort_order_is_stable_and_idempotent(mode, sort_mode, key, reverse) -> None:  # type: ignore[no-untyped-def]
    arr = np.random.default_rng(3).integers(0, 256, (24, 24, 3), dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    palette = extract_colors(img, palette_size=6, mode=mode, sort_mode=sort_mode)
    colors = palette.colors
    # The returned palette is already in sort order, and re-sorting is a no-op.
    resorted = sorted(colors, key=key, reverse=reverse)
    assert [c.rgb for c in resorted] == [c.rgb for c in colors]


_image_arrays = arrays(
    dtype=np.uint8,
    shape=st.tuples(st.integers(1, 12), st.integers(1, 12), st.sampled_from([3, 4])),
)


@settings(max_examples=40, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(
    arr=_image_arrays,
    palette_size=st.integers(1, 8),
    mode=st.sampled_from(METHODS),
    sort_mode=st.sampled_from([None, "luminance", "frequency"]),
    resize=st.booleans(),
)
def test_property_invariants_hold_for_arbitrary_images(arr, palette_size, mode, sort_mode, resize) -> None:  # type: ignore[no-untyped-def]
    mode_str = "RGB" if arr.shape[-1] == 3 else "RGBA"
    img = Image.fromarray(arr, mode_str)
    try:
        palette = extract_colors(img, palette_size=palette_size, mode=mode, sort_mode=sort_mode, resize=resize)
    except NoValidPixelsError:
        # A fully alpha-masked image is an expected, typed failure (P4).
        return
    _assert_palette_invariants(palette, palette_size)
