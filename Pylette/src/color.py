import colorsys
from typing import Literal, cast

import numpy as np
from PIL import Image

# Weights for calculating luminance
luminance_weights = np.array([0.2126, 0.7152, 0.0722])


class Color(object):
    def __init__(self, rgb: tuple[int, ...], frequency: float):
        """
        Initializes a Color object with RGB values and frequency.

        Parameters:
            rgb (tuple[int, ...]): A tuple of RGB values.
            frequency (float): The frequency of the color.
        """
        assert len(rgb) == 3, "RGB values must be a tuple of length 3"
        self.rgb = cast(tuple[int, int, int], rgb)
        self.freq: float = frequency

    def display(self, w: int = 50, h: int = 50) -> None:
        """
        Displays the color in a window of specified width and height.

        Parameters:
        w (int): Width of the window in pixels.
        h (int): Height of the window in pixels.
        """
        img = Image.new("RGB", size=(w, h), color=self.rgb)
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

    def _xyz_linearize(self) -> tuple[float, float, float]:
        """
        Performs the linearization step from https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ

        Returns:
            The linearized RGB value.
        """

        def conversion_function(x: int) -> float:
            c = x / 255
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

        _xyz = list(map(conversion_function, self.rgb))
        return (_xyz[0], _xyz[1], _xyz[2])

    @property
    def xyz(self):
        """
        Converts the RGB color to the XYZ color space.

        Returns:
            tuple[float, float, float]: The color values used in XYZ color space.
        """

        # Compute the linear values ("gamma expanded values")
        color_linear = np.array(self._xyz_linearize())

        # Conversion matrix from: http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
        # from SRGB to D65.
        # 0.4124564  0.3575761  0.1804375
        # 0.2126729  0.7151522  0.0721750
        # 0.0193339  0.1191920  0.9503041

        # Convert to xyz
        conversion_matrix = np.array(
            [[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]]
        )

        return tuple(conversion_matrix.dot(color_linear))

    @property
    def lms(self) -> tuple[float, float, float]:
        """
        Converts the RGB color to LMS color space (long, medium, short).

        Returns:
            tuple[float, float, float]: The color values in LMS color space.
        """

        return (0.0, 0.0, 0.0)

    @property
    def luminance(self) -> float:
        """
        Calculates the luminance of the color.

        Returns:
        float: The luminance of the color.
        """
        return np.dot(luminance_weights, self.rgb)
