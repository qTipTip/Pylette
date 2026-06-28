"""OKLab-based color extraction.

OKLab (Björn Ottosson, 2020 -- https://bottosson.github.io/posts/oklab/) is a
perceptual color space built so that Euclidean distance approximates perceived
color difference. Running k-means in OKLab therefore groups colors the way the
eye does.

Pipeline::

    sRGB8 -> [0,1] -> linear sRGB -> OKLab -> k-means -> centroids (OKLab)
    centroids -> linear sRGB -> sRGB8

The sRGB <-> linear step (the IEC 61966-2-1 transfer function) is not optional:
OKLab is defined on *linear* light, so skipping linearization distort the
kmeans clustering.

Two deliberate differences from the plain-RGB ``KMeans`` extractor:

* Alpha is not folded into the distance metric. Clustering happens on the three
  OKLab channels; a representative alpha is recovered per cluster by averaging
  the alpha of its member pixels.
* Empty clusters are dropped rather than emitted as spurious swatches.
"""

import numpy as np
from numpy.typing import NDArray
from typing_extensions import override

from pylette.src.color import Color
from pylette.src.extractors.protocol import NP_T, ColorExtractorBase
from pylette.src.extractors.registry import register
from pylette.src.types import ExtractionMethod, FloatArray


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
# Forward matrices are the ones from the webpage. the inverse matrices are derived
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


@register(ExtractionMethod.OKLAB)
class OKLabKMeansExtractor(ColorExtractorBase):
    """K-means clustering performed in OKLab (perceptual) space."""

    @override
    def extract(self, arr: NDArray[NP_T], palette_size: int) -> list[Color]:
        """Extract a palette by clustering pixels in OKLab space.

        Parameters:
            arr: Pixel array of shape ``(..., C)`` with ``C >= 3``; RGB(A), uint8.
            palette_size: Number of clusters / colors to extract.

        Returns:
            list[Color]: One color per non-empty cluster, with frequencies that
            sum to 1.
        """
        from sklearn.cluster import KMeans

        pixels = np.asarray(arr).reshape(-1, arr.shape[-1])
        rgb8 = pixels[:, :3].astype(np.float64)
        has_alpha = pixels.shape[1] >= 4
        alpha = pixels[:, 3].astype(np.float64) if has_alpha else np.full(len(pixels), 255.0)

        # sRGB8 -> OKLab
        lab = linear_srgb_to_oklab(srgb_to_linear(rgb8 / 255.0))

        model = KMeans(n_clusters=palette_size, n_init="auto", init="k-means++", random_state=2024)
        labels = model.fit_predict(lab)
        centers_lab = np.asarray(model.cluster_centers_)

        # OKLab centroids -> float sRGB in [0, 1], kept pre-quantization so the
        # Color stores full precision; out-of-gamut values are clamped.
        centers_srgb = np.clip(linear_to_srgb(oklab_to_linear_srgb(centers_lab)), 0.0, 1.0)

        counts = np.bincount(labels, minlength=palette_size)
        total = float(counts.sum())

        colors: list[Color] = []
        for i in range(palette_size):
            if counts[i] == 0:
                continue
            mean_alpha = float(alpha[labels == i].mean()) / 255.0
            r, g, b = (float(c) for c in centers_srgb[i])
            colors.append(Color.from_srgb_float((r, g, b), counts[i] / total, alpha=mean_alpha))
        return colors
