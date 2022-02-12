import colorsys
from typing import Tuple

import numpy as np
import numpy.typing as npt
from PIL import Image

luminance_weights: npt.NDArray[np.int_] = np.array([0.2126, 0.7152, 0.0722])


class Color(object):
    def __init__(self, RGB: Tuple[int], frequency: float) -> None:
        self.rgb = tuple([c for c in RGB])
        self.freq = frequency

    def display(self, w: int=50, h:int=50) -> None:
        """
        Displays the represented color in a w x h window.
        :param w: width in pixels
        :param h: height in pixels
        """

        img = Image.new("RGB", size=(w, h), color=self.rgb)
        img.show()

    def __lt__(self, other: 'Color') -> bool:
        return bool(self.freq < other.freq)

    def get_colors(self, colorspace: str="rgb") -> Tuple[float, ...]:
        """
        Get the color in terms of a colorspace (string).

        :param colorspace: rgb/hsv/hls
        :return: corresponding color values
        """
        colors = {"rgb": self.rgb, "hsv": self.hsv, "hls": self.hls}
        return colors[colorspace]

    @property
    def hsv(self) -> Tuple[float, float, float]:
        return colorsys.rgb_to_hsv(*self.rgb)

    @property
    def hls(self) -> Tuple[float, float, float]:
        return colorsys.rgb_to_hls(*self.rgb)

    @property
    def luminance(self) -> float:
        return float(np.dot(luminance_weights, self.rgb))
