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
from pylette.src.colorspaces import linear_srgb_to_oklab, linear_to_srgb, oklab_to_linear_srgb, srgb_to_linear
from pylette.src.extractors.protocol import NP_T, ColorExtractorBase
from pylette.src.extractors.registry import register
from pylette.src.types import ExtractionMethod


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

        # Never request more clusters than there are pixels (degenerate inputs
        # like a 1x1 image); KMeans requires n_clusters <= n_samples.
        n_clusters = min(palette_size, len(pixels))
        model = KMeans(n_clusters=n_clusters, n_init="auto", init="k-means++", random_state=2024)
        labels = model.fit_predict(lab)
        centers_lab = np.asarray(model.cluster_centers_)

        # OKLab centroids -> float sRGB in [0, 1], kept pre-quantization so the
        # Color stores full precision; out-of-gamut values are clamped.
        centers_srgb = np.clip(linear_to_srgb(oklab_to_linear_srgb(centers_lab)), 0.0, 1.0)

        counts = np.bincount(labels, minlength=n_clusters)
        total = float(counts.sum())

        colors: list[Color] = []
        for i in range(n_clusters):
            if counts[i] == 0:
                continue
            mean_alpha = float(alpha[labels == i].mean()) / 255.0
            r, g, b = (float(c) for c in centers_srgb[i])
            colors.append(Color.from_srgb_float((r, g, b), counts[i] / total, alpha=mean_alpha))
        return colors
