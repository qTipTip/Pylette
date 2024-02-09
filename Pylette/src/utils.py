import numpy as np


class ColorBox(object):
    """
    Represents a box in the RGB color space, with associated attributes, used in the Median Cut algorithm.
    """

    def __init__(self, colors):
        """
        Initialize with a numpy array of RGB colors.
        :param colors: np.ndarray (width * height, 3)
        """

        self.colors = colors
        self._get_min_max()

    def _get_min_max(self):
        min_channel = np.min(self.colors, axis=0)
        max_channel = np.max(self.colors, axis=0)

        self.min_channel = min_channel
        self.max_channel = max_channel

    def __lt__(self, other):
        """
        Compare cubes by volume
        :param other:
        """
        return self.size < other.size

    @property
    def size(self):
        return self.volume

    def _get_dominant_channel(self):
        dominant_channel = np.argmax(self.max_channel - self.min_channel)
        return dominant_channel

    @property
    def average(self):
        """
        Returns the average color contained in ColorBox
        :return: [R, G, B]
        """

        return np.mean(self.colors, axis=0)

    @property
    def volume(self):
        return np.prod(
            self.max_channel - self.min_channel,
        )

    def split(self):
        """
        Splits the ColorBox into two ColorBoxes at the median of the dominant color channel.
        :return: [ColorBox1, ColorBox2]
        """

        # get the color channel with highest range
        dominant_channel = self._get_dominant_channel()

        # sorting colors by the dominant channel
        self.colors = self.colors[self.colors[:, dominant_channel].argsort()]

        median_index = len(self.colors) // 2

        return [
            ColorBox(self.colors[:median_index]),
            ColorBox(self.colors[median_index:]),
        ]
