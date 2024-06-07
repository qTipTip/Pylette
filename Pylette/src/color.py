import colorsys
from typing import Literal, cast

import numpy as np
from PIL import Image

luminance_weights = np.array([0.2126, 0.7152, 0.0722])


class Color(object):
    def __init__(self, rgb: tuple[int, ...], frequency: float):
        assert len(rgb) == 3, "RGB values must be a tuple of length 3"
        self.rgb = cast(tuple[int, int, int], rgb)
        self.freq: float = frequency

    def display(self, w: int = 50, h: int = 50) -> None:
        """
        Displays the represented color in a w x h window.
        :param w: width in pixels
        :param h: height in pixels
        """

        img = Image.new("RGB", size=(w, h), color=self.rgb)
        img.show()

    def __lt__(self, other: "Color") -> bool:
        return self.freq < other.freq

    def get_colors(
        self, colorspace: Literal["rgb", "hsv", "hls"] = "rgb"
    ) -> tuple[int, ...] | tuple[float, ...]:
        """
        Get the color in terms of a colorspace (string).

        :param colorspace: rgb/hsv/hls
        :return: corresponding color values
        """

        colors = {"rgb": self.rgb, "hsv": self.hsv, "hls": self.hls}

        return colors[colorspace]

    @property
    def hsv(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hsv(
            r=self.rgb[0] / 255, g=self.rgb[1] / 255, b=self.rgb[2] / 255
        )

    @property
    def hls(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hls(
            r=self.rgb[0] / 255, g=self.rgb[1] / 255, b=self.rgb[2] / 255
        )

    @property
    def luminance(self) -> float:
        return np.dot(luminance_weights, self.rgb)
