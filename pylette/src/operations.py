"""Pure, immutable palette operations over lists of :class:`~pylette.src.color.Color`.

This module holds the numeric core for the palette operations exposed as thin
methods on :class:`~pylette.src.color.Color` and
:class:`~pylette.src.palette.Palette`. Functions here take and return plain
``list[Color]`` (or a single ``Color``); they never mutate their inputs except
for the private ``_normalize_frequencies`` helper, which only touches colors it
was handed to finalize a freshly built result.
"""

import numpy as np

from pylette.src.color import Color
from pylette.src.colorspaces import oklab_to_srgb


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


def _normalize_frequencies(colors: list[Color]) -> list[Color]:  # pyright: ignore[reportUnusedFunction]
    """Assign equal frequencies summing to 1.0 across ``colors`` in place."""
    n = len(colors)
    for color in colors:
        color.frequency = 1.0 / n
    return colors


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
