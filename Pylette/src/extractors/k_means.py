import numpy as np
from numpy.typing import NDArray
from sklearn.cluster import KMeans

from Pylette.src.color import Color
from Pylette.src.extractors.protocol import NP_T, ColorExtractorBase


class KMeansExtractor(ColorExtractorBase):
    def extract(self, arr: NDArray[NP_T], height: int, width: int, palette_size: int) -> list[Color]:
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
        arr = np.squeeze(arr)
        model = KMeans(n_clusters=palette_size, n_init="auto", init="k-means++", random_state=2024)
        labels = model.fit_predict(arr)
        palette = np.array(model.cluster_centers_, dtype=int)
        color_count = np.bincount(labels)
        color_frequency = color_count / float(np.sum(color_count))
        colors = []
        for color, freq in zip(palette, color_frequency):
            colors.append(Color(color, freq))
        return colors


def k_means_extraction(arr: NDArray[NP_T], height: int, width: int, palette_size: int) -> list[Color]:
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
    return KMeansExtractor().extract(arr=arr, height=height, width=width, palette_size=palette_size)
