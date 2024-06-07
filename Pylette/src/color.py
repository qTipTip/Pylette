import colorsys

import numpy as np
from PIL import Image

luminance_weights = np.array([0.2126, 0.7152, 0.0722])


class Color(object):
    def __init__(self, RGB, frequency):
        self.rgb: tuple[int, int, int] = tuple([c for c in RGB])
        self.freq: float = frequency

    def display(self, w=50, h=50) -> None:
        """
        Displays the represented color in a w x h window.
        :param w: width in pixels
        :param h: height in pixels
        """

        img = Image.new("RGB", size=(w, h), color=self.rgb)
        img.show()

    def __lt__(self, other) -> bool:
        return self.freq < other.freq

    def get_colors(self, colorspace="rgb") -> tuple[int, ...] | tuple[float, ...]:
        """
        Get the color in terms of a colorspace (string).

        :param colorspace: rgb/hsv/hls
        :return: corresponding color values
        """
        colors = {"rgb": self.rgb, "hsv": self.hsv, "hls": self.hls}
        return colors[colorspace]

    @property
    def hsv(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hsv(r=self.rgb[0], g=self.rgb[1], b=self.rgb[2])

    @property
    def hls(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hls(r=self.rgb[0], g=self.rgb[1], b=self.rgb[2])

    @property
    def luminance(self) -> float:
        return np.dot(luminance_weights, self.rgb)
