import numpy as np
from numpy.typing import ArrayLike, NDArray


class ColorBox:
    """
    Represents a box in the RGB color space, with associated attributes, used in the Median Cut algorithm.
    """

    def __init__(self, colors: ArrayLike):
        """
        Initializes a ColorBox with a numpy array of RGB colors.

        Parameters:
            colors (ArrayLike): A numpy array of RGB colors with shape (width * height, 3).
        """
        self.colors = np.asarray(colors, dtype=np.uint8)
        if self.colors.ndim < 2 or self.colors.shape[-1] != 3:
            raise ValueError("Invalid color array")
        self._get_min_max()

    def _get_min_max(self) -> None:
        """
        Calculates the minimum and maximum values for each color channel in the ColorBox.
        """
        self.min_channel: NDArray[np.uint8, (3,)] = np.min(self.colors, axis=0)
        self.max_channel: NDArray[np.uint8, (3,)] = np.max(self.colors, axis=0)

    def __lt__(self, other: "ColorBox") -> bool:
        """
        Compares two ColorBoxes based on their volume.

        Parameters:
            other (ColorBox): The other ColorBox to compare with.

        Returns:
        bool: True if the volume of this ColorBox is less than the volume of the other ColorBox, False otherwise.
        """
        return self.size < other.size

    @property
    def size(self) -> np.uint64:
        """
        Returns the volume of the ColorBox.

        Returns:
            np.uint64: The volume of the ColorBox.
        """
        return self.volume

    def _get_dominant_channel(self) -> int:
        """
        Determines the dominant color channel in the ColorBox.

        Returns:
            int: The index of the dominant color channel.
        """
        diff: NDArray[np.uint8, (3,)] = self.max_channel - self.min_channel
        dominant_channel = np.argmax(diff)
        return dominant_channel

    @property
    def average(self) -> np.ndarray:
        """
        Calculates the average color contained in the ColorBox.

        Returns:
            np.ndarray: The average color as an array [R, G, B].
        """
        avg_color = np.mean(self.colors, axis=0)
        if avg_color.shape != (3,):
            raise ValueError("Invalid number of channels in average color.")
        return avg_color

    @property
    def volume(self) -> int:
        """
        Calculates the volume of the ColorBox.

        Returns:
            int: The volume of the ColorBox.
        """
        diff: NDArray[np.uint8, (3,)] = self.max_channel - self.min_channel
        return np.prod(diff).item()

    def split(self) -> list["ColorBox"]:
        """
        Splits the ColorBox into two ColorBoxes at the median of the dominant color channel.

        Returns:
            list[ColorBox]: A list containing the two new ColorBoxes.
        """
        dominant_channel = self._get_dominant_channel()
        self.colors = self.colors[self.colors[:, dominant_channel].argsort()]
        median_index = len(self.colors) // 2

        return [
            ColorBox(self.colors[:median_index]),
            ColorBox(self.colors[median_index:]),
        ]

    @property
    def pixel_count(self) -> int:
        """
        Returns the number of pixels in the ColorBox.

        Returns:
            int: The number of pixels in the ColorBox.
        """
        return len(self.colors)
