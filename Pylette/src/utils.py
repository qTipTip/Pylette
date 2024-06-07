import numpy as np
from numpy.typing import ArrayLike, NDArray


class ColorBox:
    """
    Represents a box in the RGB color space, with associated attributes, used in the Median Cut algorithm.
    """

    def __init__(self, colors: ArrayLike):
        """
        Initialize with a numpy array of RGB colors.
        :param colors: np.ndarray (width * height, 3)
        """
        self.colors = np.asarray(colors, dtype=np.uint8)
        if self.colors.ndim < 2 or self.colors.shape[-1] != 3:
            raise ValueError("Invalid color array")
        self._get_min_max()

    def _get_min_max(self) -> None:
        self.min_channel: NDArray[np.uint8, (3,)] = np.min(self.colors, axis=0)
        self.max_channel: NDArray[np.uint8, (3,)] = np.max(self.colors, axis=0)

    def __lt__(self, other: "ColorBox") -> bool:
        """
        Compare cubes by volume
        :param other:
        """
        return self.size < other.size

    @property
    def size(self) -> np.uint64:
        return self.volume

    def _get_dominant_channel(self) -> int:
        diff: NDArray[np.uint8, (3,)] = self.max_channel - self.min_channel
        dominant_channel = np.argmax(diff)
        return dominant_channel

    @property
    def average(self) -> np.ndarray:
        """
        Returns the average color contained in ColorBox
        :return: np.array([R, G, B])
        """
        avg_color = np.mean(self.colors, axis=0)
        if avg_color.shape != (3,):
            raise ValueError("Invalid number of channels in average color.")
        return avg_color

    @property
    def volume(self) -> int:
        diff: NDArray[np.uint8, (3,)] = self.max_channel - self.min_channel
        return np.prod(diff).item()

    def split(self) -> list["ColorBox"]:
        """
        Splits the ColorBox into two ColorBoxes at the median of the dominant color channel.
        :return: [ColorBox1, ColorBox2]
        """
        dominant_channel = self._get_dominant_channel()
        self.colors = self.colors[self.colors[:, dominant_channel].argsort()]
        median_index = len(self.colors) // 2

        return [
            ColorBox(self.colors[:median_index]),
            ColorBox(self.colors[median_index:]),
        ]
