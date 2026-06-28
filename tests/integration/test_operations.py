import pytest

from pylette import Color, HarmonyKind, InvalidHarmonyError, Palette
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


def test_dedup_collapses_exact_duplicates_and_sums_frequency() -> None:
    colors = [
        Color(rgba=(10, 20, 30, 255), frequency=0.5),
        Color(rgba=(10, 20, 30, 255), frequency=0.2),
        Color(rgba=(200, 100, 50, 255), frequency=0.3),
    ]
    result = operations.dedup(colors)
    assert len(result) == 2
    assert result[0].rgb == (10, 20, 30)
    assert result[0].frequency == pytest.approx(0.7)
    assert result[1].rgb == (200, 100, 50)


def test_palette_dedup_is_immutable_and_returns_new_palette() -> None:
    colors = [Color(rgba=(10, 20, 30, 255), frequency=0.5), Color(rgba=(10, 20, 30, 255), frequency=0.5)]
    palette = Palette(colors)
    deduped = palette.dedup()
    assert isinstance(deduped, Palette)
    assert len(deduped) == 1
    assert len(palette) == 2  # original untouched
    assert sum(deduped.frequencies) == pytest.approx(1.0)


def test_sort_perceptual_orders_by_lightness_and_is_idempotent() -> None:
    colors = [
        Color(rgba=(255, 255, 255, 255), frequency=0.25),
        Color(rgba=(0, 0, 0, 255), frequency=0.25),
        Color(rgba=(128, 128, 128, 255), frequency=0.5),
    ]
    sorted_once = operations.sort_perceptual(colors)
    lightness = [c.oklab[0] for c in sorted_once]
    assert lightness == sorted(lightness)  # ascending by L
    sorted_twice = operations.sort_perceptual(sorted_once)
    assert [c.rgb for c in sorted_twice] == [c.rgb for c in sorted_once]  # idempotent
    assert [c.rgb for c in colors][0] == (255, 255, 255)  # input untouched


def test_palette_sort_perceptual_descending() -> None:
    palette = Palette([Color(rgba=(0, 0, 0, 255), frequency=0.5), Color(rgba=(255, 255, 255, 255), frequency=0.5)])
    result = palette.sort_perceptual(descending=True)
    assert result[0].rgb == (255, 255, 255)
    assert len(palette) == 2  # original untouched


def test_merge_similar_collapses_near_duplicates() -> None:
    colors = [
        Color(rgba=(100, 100, 100, 255), frequency=0.4),
        Color(rgba=(101, 101, 101, 255), frequency=0.3),  # ~identical to first
        Color(rgba=(10, 200, 50, 255), frequency=0.3),  # clearly different
    ]
    result = operations.merge_similar(colors, delta_e=0.05)
    assert len(result) == 2
    assert sum(c.frequency for c in result) == pytest.approx(1.0)
    # the merged grey carries the summed frequency of its two members
    assert max(c.frequency for c in result) == pytest.approx(0.7)


def test_merge_similar_idempotent_at_fixed_threshold() -> None:
    colors = [
        Color(rgba=(100, 100, 100, 255), frequency=0.4),
        Color(rgba=(101, 101, 101, 255), frequency=0.3),
        Color(rgba=(10, 200, 50, 255), frequency=0.3),
    ]
    once = operations.merge_similar(colors, delta_e=0.05)
    twice = operations.merge_similar(once, delta_e=0.05)
    assert [c.rgb for c in twice] == [c.rgb for c in once]


def test_merge_similar_rejects_negative_threshold() -> None:
    with pytest.raises(ValueError):
        operations.merge_similar([Color(rgba=(0, 0, 0, 255), frequency=1.0)], delta_e=-1.0)


def test_palette_merge_similar_is_immutable() -> None:
    palette = Palette(
        [
            Color(rgba=(100, 100, 100, 255), frequency=0.5),
            Color(rgba=(101, 101, 101, 255), frequency=0.5),
        ]
    )
    merged = palette.merge_similar(delta_e=0.05)
    assert len(merged) == 1
    assert len(palette) == 2
    assert sum(merged.frequencies) == pytest.approx(1.0)


def test_interpolate_includes_endpoints_and_normalizes() -> None:
    a = Color(rgba=(0, 0, 0, 255), frequency=1.0)
    b = Color(rgba=(255, 255, 255, 255), frequency=1.0)
    ramp = operations.interpolate(a, b, steps=5)
    assert len(ramp) == 5
    assert ramp[0].rgb == (0, 0, 0)
    assert ramp[-1].rgb == (255, 255, 255)
    assert sum(c.frequency for c in ramp) == pytest.approx(1.0)
    lightness = [c.oklab[0] for c in ramp]
    assert lightness == sorted(lightness)  # monotonic ramp


def test_interpolate_rejects_too_few_steps() -> None:
    a = Color(rgba=(0, 0, 0, 255), frequency=1.0)
    b = Color(rgba=(255, 255, 255, 255), frequency=1.0)
    with pytest.raises(ValueError):
        operations.interpolate(a, b, steps=1)


def test_color_gradient_to_returns_palette() -> None:
    a = Color(rgba=(0, 0, 0, 255), frequency=1.0)
    b = Color(rgba=(255, 0, 0, 255), frequency=1.0)
    grad = a.gradient_to(b, steps=3)
    assert isinstance(grad, Palette)
    assert len(grad) == 3


def test_palette_gradient_bridges_consecutive_swatches() -> None:
    palette = Palette(
        [
            Color(rgba=(0, 0, 0, 255), frequency=0.5),
            Color(rgba=(255, 255, 255, 255), frequency=0.5),
        ]
    )
    grad = palette.gradient(steps_between=1)
    # endpoints + 1 inserted between them = 3
    assert len(grad) == 3
    assert sum(grad.frequencies) == pytest.approx(1.0)
    assert len(palette) == 2  # original untouched


def test_palette_gradient_single_color_unchanged() -> None:
    palette = Palette([Color(rgba=(10, 20, 30, 255), frequency=1.0)])
    grad = palette.gradient(steps_between=3)
    assert len(grad) == 1
    assert grad[0].rgb == (10, 20, 30)


def test_palette_gradient_rejects_zero_steps() -> None:
    palette = Palette([Color(rgba=(0, 0, 0, 255), frequency=0.5), Color(rgba=(1, 1, 1, 255), frequency=0.5)])
    with pytest.raises(ValueError):
        palette.gradient(steps_between=0)


def test_harmony_complementary_has_two_colors() -> None:
    seed = Color(rgba=(200, 50, 50, 255), frequency=1.0)
    result = operations.harmony(seed, HarmonyKind.COMPLEMENTARY)
    assert len(result) == 2
    assert sum(c.frequency for c in result) == pytest.approx(1.0)


def test_harmony_triadic_and_analogous_counts() -> None:
    seed = Color(rgba=(200, 50, 50, 255), frequency=1.0)
    assert len(operations.harmony(seed, "triadic")) == 3
    assert len(operations.harmony(seed, "analogous")) == 3


def test_harmony_rejects_unknown_kind() -> None:
    seed = Color(rgba=(200, 50, 50, 255), frequency=1.0)
    with pytest.raises(InvalidHarmonyError):
        operations.harmony(seed, "tetradic")


def test_color_harmony_returns_palette() -> None:
    seed = Color(rgba=(200, 50, 50, 255), frequency=1.0)
    result = seed.harmony("triadic")
    assert isinstance(result, Palette)
    assert len(result) == 3


def test_palette_harmony_seeds_from_dominant_color() -> None:
    palette = Palette(
        [
            Color(rgba=(10, 20, 30, 255), frequency=0.2),
            Color(rgba=(200, 50, 50, 255), frequency=0.8),  # dominant
        ]
    )
    result = palette.harmony("complementary")
    # first color of a complementary scheme is the seed = the dominant color
    assert result[0].rgb == (200, 50, 50)


def test_palette_harmony_empty_palette() -> None:
    result = Palette([]).harmony("triadic")
    assert len(result) == 0
