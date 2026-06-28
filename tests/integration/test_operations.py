import pytest

from pylette import Color
from pylette.src import operations


def test_delta_e_is_zero_for_identical_colors() -> None:
    c = Color(rgba=(120, 60, 200, 255), frequency=1.0)
    assert c.delta_e(c) == pytest.approx(0.0, abs=1e-9)


def test_delta_e_is_symmetric_and_positive() -> None:
    a = Color(rgba=(10, 20, 30, 255), frequency=0.5)
    b = Color(rgba=(200, 180, 50, 255), frequency=0.5)
    assert a.delta_e(b) == pytest.approx(b.delta_e(a))
    assert a.delta_e(b) > 0.0


def test_harmony_kind_coerces_from_string() -> None:
    from pylette import HarmonyKind
    from pylette.src.types import coerce_to_enum

    assert coerce_to_enum("triadic", HarmonyKind) is HarmonyKind.TRIADIC
    assert coerce_to_enum("COMPLEMENTARY", HarmonyKind) is HarmonyKind.COMPLEMENTARY
    assert coerce_to_enum(HarmonyKind.ANALOGOUS, HarmonyKind) is HarmonyKind.ANALOGOUS


def test_weighted_oklab_mean_of_identical_colors_is_that_color() -> None:
    colors = [Color(rgba=(40, 160, 90, 255), frequency=0.3) for _ in range(3)]
    srgb, opacity = operations.weighted_oklab_mean(colors)
    assert srgb == pytest.approx(colors[0].rgb_float, abs=1e-6)
    assert opacity == pytest.approx(1.0)


def test_weighted_oklab_mean_uses_frequency_weights() -> None:
    dark = Color(rgba=(0, 0, 0, 255), frequency=0.9)  # opacity 1.0
    light = Color(rgba=(255, 255, 255, 0), frequency=0.1)  # opacity 0.0
    (r, g, b), opacity = operations.weighted_oklab_mean([dark, light])
    (ur, ug, ub), _ = operations.weighted_oklab_mean(
        [
            Color(rgba=(0, 0, 0, 255), frequency=0.5),
            Color(rgba=(255, 255, 255, 255), frequency=0.5),
        ]
    )
    # 90% weight on black pulls the mean darker than the 50/50 midpoint
    assert r < ur and g < ug and b < ub
    # opacity is frequency-weighted: 0.9*1.0 + 0.1*0.0
    assert opacity == pytest.approx(0.9)


def test_weighted_oklab_mean_zero_total_frequency_uses_uniform_weights() -> None:
    zero = [
        Color(rgba=(0, 0, 0, 255), frequency=0.0),
        Color(rgba=(255, 255, 255, 255), frequency=0.0),
    ]
    uniform = [
        Color(rgba=(0, 0, 0, 255), frequency=0.5),
        Color(rgba=(255, 255, 255, 255), frequency=0.5),
    ]
    result_zero, _ = operations.weighted_oklab_mean(zero)
    result_uniform, _ = operations.weighted_oklab_mean(uniform)
    # zero total frequency falls back to uniform weights -> same result as 50/50
    assert result_zero == pytest.approx(result_uniform, abs=1e-9)


def test_normalize_frequencies_sums_to_one() -> None:
    colors = [Color(rgba=(i, i, i, 255), frequency=0.0) for i in (10, 20, 30, 40)]
    normalized = operations._normalize_frequencies(colors)
    assert sum(c.frequency for c in normalized) == pytest.approx(1.0)
    assert all(c.frequency == pytest.approx(0.25) for c in normalized)


def test_normalize_frequencies_empty_list() -> None:
    assert operations._normalize_frequencies([]) == []
