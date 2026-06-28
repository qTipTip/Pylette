import numpy as np
from numpy.typing import NDArray
from typing_extensions import override

from pylette.src.color import Color
from pylette.src.extractors.protocol import NP_T, ColorExtractorBase
from pylette.src.extractors.registry import register
from pylette.types import ExtractionMethod


@register(ExtractionMethod.KM)
class KMeansExtractor(ColorExtractorBase):
    @override
    def extract(self, arr: NDArray[NP_T], palette_size: int) -> list[Color]:
        """
        Extracts a color palette using KMeans.

        Parameters:
            arr (NDArray[float]): The input array.
            height (int): The height of the image.
            width (int): The width of the image.
            palette_size (int): The number of colors to extract from the image.

        Returns:
            list[Color]: A palette of colors sorted by frequency.
        """

        from sklearn.cluster import KMeans

        arr = self._reshape_array(arr)
        # Never request more clusters than there are pixels (degenerate inputs
        # like a 1x1 image); KMeans requires n_clusters <= n_samples.
        n_colors = min(palette_size, arr.shape[0])
        model = KMeans(n_clusters=n_colors, n_init="auto", init="k-means++", random_state=2024)
        labels = model.fit_predict(arr)
        palette = np.array(model.cluster_centers_, dtype=int)
        color_count = np.bincount(labels)
        color_frequency = color_count / float(np.sum(color_count))
        colors = []
        for color, freq in zip(palette, color_frequency):
            colors.append(Color(color, freq))
        return colors
