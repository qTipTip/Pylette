"""Pure, immutable palette operations over lists of :class:`~pylette.src.color.Color`.

This module holds the numeric core for the palette operations exposed as thin
methods on :class:`~pylette.src.color.Color` and
:class:`~pylette.src.palette.Palette`. Functions here take and return plain
``list[Color]`` (or a single ``Color``); they never mutate their inputs except
for the private ``_normalize_frequencies`` helper, which only touches colors it
was handed to finalize a freshly built result.
"""

import colorsys

import numpy as np

from pylette.src.color import Color
from pylette.src.colorspaces import oklab_to_srgb
from pylette.src.exceptions import InvalidHarmonyError
from pylette.src.types import HarmonyKind, coerce_to_enum


def weighted_oklab_mean(colors: list[Color]) -> tuple[tuple[float, float, float], float]:
    """Frequency-weighted mean of ``colors`` in OKLab, returned as ``(srgb, opacity)``.

    The mean is computed in OKLab (perceptually even) then projected back to
    gamma-encoded sRGB. Opacity is averaged with the same weights. If the total
    frequency is zero, uniform weights are used so the call never divides by zero.
    """
    labs = np.array([c.oklab for c in colors], dtype=np.float64)
    opacities = np.array([c.opacity for c in colors], dtype=np.float64)
    weights = np.array([c.frequency for c in colors], dtype=np.float64)
    if weights.sum() == 0:
        weights = np.ones_like(weights)
    mean_lab = np.average(labs, axis=0, weights=weights)
    mean_opacity = float(np.average(opacities, weights=weights))
    return oklab_to_srgb((float(mean_lab[0]), float(mean_lab[1]), float(mean_lab[2]))), mean_opacity


def _normalize_frequencies(colors: list[Color]) -> list[Color]:
    """Assign equal frequencies summing to 1.0 across ``colors`` in place."""
    n = len(colors)
    for color in colors:
        color.frequency = 1.0 / n
    return colors


def sort_perceptual(colors: list[Color], descending: bool = False) -> list[Color]:
    """Return a new list of ``colors`` sorted by OKLab lightness (L).

    Python's ``sorted`` is stable, so equal-lightness colors keep their relative
    order; sorting an already-sorted list is a no-op (idempotent).
    """
    return sorted(colors, key=lambda c: c.oklab[0], reverse=descending)


def merge_similar(colors: list[Color], delta_e: float) -> list[Color]:
    """Merge colors within ``delta_e`` of each other (OKLab ΔE) into single swatches.

    Greedy single pass over ``colors`` (extractor order is deterministic, so the
    result is too): each color joins the first existing cluster whose running
    representative is within ``delta_e``, otherwise it starts a new cluster. Each
    cluster's representative is the frequency-weighted OKLab mean of its members,
    with the summed frequency, so the total frequency is preserved.

    Raises:
        ValueError: If ``delta_e`` is negative.
    """
    if delta_e < 0:
        raise ValueError(f"delta_e must be non-negative, got {delta_e}.")
    clusters: list[list[Color]] = []
    reps: list[Color] = []
    for color in colors:
        for i, rep in enumerate(reps):
            if color.delta_e(rep) <= delta_e:
                clusters[i].append(color)
                srgb, opacity = weighted_oklab_mean(clusters[i])
                reps[i] = Color.from_srgb_float(srgb, sum(c.frequency for c in clusters[i]), alpha=opacity)
                break
        else:
            clusters.append([color])
            reps.append(color)
    return reps


def interpolate(a: Color, b: Color, steps: int) -> list[Color]:
    """Return ``steps`` colors interpolated from ``a`` to ``b`` in OKLab (inclusive).

    Interpolating in OKLab gives a perceptually even ramp. Opacity is
    interpolated linearly. The result has equal frequencies summing to 1.0.

    Raises:
        ValueError: If ``steps`` is less than 2.
    """
    if steps < 2:
        raise ValueError(f"steps must be at least 2, got {steps}.")
    la = a.oklab
    lb = b.oklab
    result: list[Color] = []
    for i in range(steps):
        t = i / (steps - 1)
        lab = (la[0] + t * (lb[0] - la[0]), la[1] + t * (lb[1] - la[1]), la[2] + t * (lb[2] - la[2]))
        opacity = a.opacity + t * (b.opacity - a.opacity)
        result.append(Color.from_srgb_float(oklab_to_srgb(lab), frequency=0.0, alpha=opacity))
    return _normalize_frequencies(result)


def dedup(colors: list[Color]) -> list[Color]:
    """Collapse exactly-equal colors (same 8-bit RGB), summing their frequencies.

    Cheap and lossless: the representative keeps the float precision of the first
    occurrence and its opacity; only frequencies are combined. First-seen order
    is preserved.
    """
    groups: dict[tuple[int, int, int], list[Color]] = {}
    order: list[tuple[int, int, int]] = []
    for color in colors:
        key = color.rgb
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(color)
    result: list[Color] = []
    for key in order:
        group = groups[key]
        rep = group[0]
        frequency = sum(c.frequency for c in group)
        result.append(Color.from_srgb_float(rep.rgb_float, frequency, alpha=rep.opacity))
    return result


# Hue offsets (fraction of the 360° wheel) per harmony, seed listed first.
_HARMONY_OFFSETS: dict[HarmonyKind, tuple[float, ...]] = {
    HarmonyKind.COMPLEMENTARY: (0.0, 0.5),  # +180°
    HarmonyKind.TRIADIC: (0.0, 1.0 / 3.0, 2.0 / 3.0),  # ±120°
    HarmonyKind.ANALOGOUS: (-1.0 / 12.0, 0.0, 1.0 / 12.0),  # ±30°, seed in the middle
}


def harmony(seed: Color, kind: HarmonyKind | str) -> list[Color]:
    """Generate a color-harmony scheme from ``seed`` by rotating hue in HSV.

    Complementary (+180°), triadic (±120°), or analogous (±30°). The returned
    colors share the seed's saturation, value, and opacity and get equal
    frequencies summing to 1.0.

    Raises:
        InvalidHarmonyError: If ``kind`` is not a valid :class:`HarmonyKind`.
    """
    kind = coerce_to_enum(kind, HarmonyKind, error_cls=InvalidHarmonyError)
    h, s, v = seed.hsv
    result: list[Color] = []
    for offset in _HARMONY_OFFSETS[kind]:
        new_h = (h + offset) % 1.0
        r, g, b = colorsys.hsv_to_rgb(new_h, s, v)
        result.append(Color.from_srgb_float((r, g, b), frequency=0.0, alpha=seed.opacity))
    return _normalize_frequencies(result)
