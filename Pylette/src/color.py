import colorsys
from typing import Literal, cast

import numpy as np
from PIL import Image

# Weights for calculating luminance
luminance_weights = np.array([0.2126, 0.7152, 0.0722])


class Color(object):
    def __init__(self, rgba: tuple[int, ...], frequency: float):
        """
        Initializes a Color object with RGBA values and frequency.

        Parameters:
            rgba (tuple[int, ...]): A tuple of RGBA values.
            frequency (float): The frequency of the color.
        """
        assert len(rgba) == 4, "RGBA values must be a tuple of length 4"
        *rgb, alpha = rgba
        self.rgb = cast(tuple[int, int, int], rgb)
        self.rgba = rgba
        self.a = alpha
        self.freq: float = frequency
        self.weight = alpha / 255.0

    def display(self, w: int = 50, h: int = 50) -> None:
        """
        Displays the color in a window of specified width and height.

        Parameters:
        w (int): Width of the window in pixels.
        h (int): Height of the window in pixels.
        """
        img = Image.new("RGBA", size=(w, h), color=self.rgba)
        img.show()

    def __lt__(self, other: "Color") -> bool:
        """
        Compares the frequency of this color with another color.

        Parameters:
            other (Color): The other Color object to compare with.

        Returns:
            bool: True if the frequency of this color is less than the frequency of the other color, False otherwise.
        """
        return self.freq < other.freq

    def get_colors(self, colorspace: Literal["rgb", "hsv", "hls"] = "rgb") -> tuple[int, ...] | tuple[float, ...]:
        """
        Returns the color values in the specified color space.

        Parameters:
            colorspace (Literal["rgb", "hsv", "hls"]): The color space to use.

        Returns:
            tuple[int, ...] | tuple[float, ...]: The color values in the specified color space.
        """
        colors = {"rgb": self.rgb, "hsv": self.hsv, "hls": self.hls}
        return colors[colorspace]

    @property
    def hsv(self) -> tuple[float, float, float]:
        """
        Converts the RGB color to HSV color space.

        Returns:
            tuple[float, float, float]: The color values in HSV color space.
        """
        return colorsys.rgb_to_hsv(r=self.rgb[0] / 255, g=self.rgb[1] / 255, b=self.rgb[2] / 255)

    @property
    def hls(self) -> tuple[float, float, float]:
        """
        Converts the RGB color to HLS color space.

        Returns:
            tuple[float, float, float]: The color values in HLS color space.
        """
        return colorsys.rgb_to_hls(r=self.rgb[0] / 255, g=self.rgb[1] / 255, b=self.rgb[2] / 255)

    @property
    def luminance(self) -> float:
        """
        Calculates the luminance of the color.

        Returns:
        float: The luminance of the color.
        """
        return np.dot(luminance_weights, self.rgb)
