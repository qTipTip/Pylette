import numpy as np

from Pylette.src.color import Color
from Pylette.src.utils import ColorBox


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

    arr = arr.reshape((width * height, -1))
    c = [ColorBox(arr)]

    # Each iteration, find the largest box, split it, remove original box from list of boxes, and add the two new boxes.
    while len(c) < palette_size:
        largest_c_idx = np.argmax(c)
        # add the two new boxes to the list, while removing the split box.
        c = c[:largest_c_idx] + c[largest_c_idx].split() + c[largest_c_idx + 1 :]

    total_pixels = width * height
    colors = [Color(tuple(map(int, box.average)), box.pixel_count / total_pixels) for box in c]

    return colors
