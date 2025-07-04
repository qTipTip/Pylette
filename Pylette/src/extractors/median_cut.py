import numpy as np
from numpy.typing import NDArray

from Pylette.src.color import Color
from Pylette.src.extractors.protocol import NP_T, ColorExtractorBase
from Pylette.src.utils import ColorBox


class MedianCutExtractor(ColorExtractorBase):
    def extract(self, arr: NDArray[NP_T], height: int, width: int, palette_size: int) -> list[Color]:
        """
        Extracts a color palette using the median cut algorithm.

        Parameters:
            arr (np.ndarray): The input array.
            height (int): The height of the image.
            width (int): The width of the image.
            palette_size (int): The number of colors to extract from the image.

        Returns:
            list[Color]: A list of colors extracted from the image.
        """

        arr = self._reshape_array(arr=arr, height=height, width=width)
        valid_pixel_count = arr.shape[0]
        boxes = [ColorBox(arr)]
        while len(boxes) < palette_size:
            largest_box_idx = np.argmax(boxes)  # type: ignore
            boxes = boxes[:largest_box_idx] + boxes[largest_box_idx].split() + boxes[largest_box_idx + 1 :]

        return [Color(tuple(map(int, box.average)), box.pixel_count / valid_pixel_count) for box in boxes]


def median_cut_extraction(arr: np.ndarray, height: int, width: int, palette_size: int) -> list[Color]:
    """
    Extracts a color palette using the median cut algorithm.

    Parameters:
        arr (np.ndarray): The input array.
        height (int): The height of the image.
        width (int): The width of the image.
        palette_size (int): The number of colors to extract from the image.

    Returns:
        list[Color]: A list of colors extracted from the image.
    """

    return MedianCutExtractor().extract(arr, height, width, palette_size)
