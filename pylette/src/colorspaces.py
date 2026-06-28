"""
Color-space transforms

OKLab (Björn Ottosson, 2020 -- https://bottosson.github.io/posts/oklab/) is a
perceptual color space built so that Euclidean distance approximates perceived
color difference.
"""

import numpy as np

from pylette.src.types import FloatArray


# sRGB <-> linear sRGB (IEC 61966-2-1 transfer function)
def srgb_to_linear(srgb: FloatArray) -> FloatArray:
    """Map gamma-encoded sRGB in ``[0, 1]`` to linear-light sRGB in ``[0, 1]``."""
    return np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(linear: FloatArray) -> FloatArray:
    """Map linear-light sRGB in ``[0, 1]`` back to gamma-encoded sRGB in ``[0, 1]``."""
    linear = np.clip(linear, 0.0, 1.0)
    return np.where(linear <= 0.0031308, 12.92 * linear, 1.055 * np.power(linear, 1.0 / 2.4) - 0.055)


# linear sRGB <-> OKLab (Ottosson 2020)
#
# Forward matrices are the ones from the webpage. The inverse matrices are derived
# from them so the round-trip is numerically self-consistent (single source of
# truth) rather than two independently transcribed constant sets.

# linear sRGB -> LMS
_LRGB_TO_LMS = np.array(
    [
        [0.4122214708, 0.5363325363, 0.0514459929],
        [0.2119034982, 0.6806995451, 0.1073969566],
        [0.0883024619, 0.2817188376, 0.6299787005],
    ]
)
# nonlinear l'm's' -> OKLab
_LMS_TO_OKLAB = np.array(
    [
        [0.2104542553, 0.7936177850, -0.0040720468],
        [1.9779984951, -2.4285922050, 0.4505937099],
        [0.0259040371, 0.7827717662, -0.8086757660],
    ]
)
_OKLAB_TO_LMS = np.linalg.inv(_LMS_TO_OKLAB)
_LMS_TO_LRGB = np.linalg.inv(_LRGB_TO_LMS)


def linear_srgb_to_oklab(rgb: FloatArray) -> FloatArray:
    """Convert an ``(N, 3)`` array of linear sRGB to OKLab."""
    lms = rgb @ _LRGB_TO_LMS.T
    lms_nonlinear = np.cbrt(lms)
    return lms_nonlinear @ _LMS_TO_OKLAB.T


def oklab_to_linear_srgb(lab: FloatArray) -> FloatArray:
    """Convert an ``(N, 3)`` array of OKLab back to linear sRGB."""
    lms_nonlinear = lab @ _OKLAB_TO_LMS.T
    lms = lms_nonlinear**3
    return lms @ _LMS_TO_LRGB.T


def srgb_to_oklab(srgb: tuple[float, float, float]) -> tuple[float, float, float]:
    """Convert a single gamma-encoded sRGB triple in ``[0, 1]`` to OKLab ``(L, a, b)``."""
    arr = np.asarray([srgb], dtype=np.float64)
    lab = linear_srgb_to_oklab(srgb_to_linear(arr))[0]
    return (float(lab[0]), float(lab[1]), float(lab[2]))


def oklab_to_srgb(lab: tuple[float, float, float]) -> tuple[float, float, float]:
    """Convert a single OKLab ``(L, a, b)`` triple to gamma-encoded sRGB in ``[0, 1]``.

    Inverse of :func:`srgb_to_oklab`. ``linear_to_srgb`` clips into ``[0, 1]``,
    so out-of-gamut OKLab inputs (e.g. an averaged centroid) are returned clamped.
    """
    arr = np.asarray([lab], dtype=np.float64)
    srgb = linear_to_srgb(oklab_to_linear_srgb(arr))[0]
    return (float(srgb[0]), float(srgb[1]), float(srgb[2]))
