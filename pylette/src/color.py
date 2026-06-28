import colorsys
import warnings

import numpy as np

from pylette.src.exceptions import InvalidColorspaceError
from pylette.src.types import ColorSpace, coerce_to_enum

# Weights for calculating luminance
luminance_weights = np.array([0.2126, 0.7152, 0.0722])


def _clamp_unit(value: float) -> float:
    """Clamp a float into the closed unit interval [0, 1]."""
    return min(1.0, max(0.0, float(value)))


class Color(object):
    """A single palette color.

    The canonical representation is float sRGB in ``[0, 1]`` (plus a float
    alpha). 8-bit quantization happens only at the output boundaries
    (:attr:`rgb`, :attr:`rgba`, :attr:`a`, :attr:`hex`), so colors constructed
    from continuous centroids keep their precision until they are read out.
    """

    def __init__(self, rgba: tuple[int, ...], frequency: float):
        """
        Initializes a Color object from 8-bit RGBA values.

        The 8-bit input is the quantized view of the color; it is converted to
        the canonical float store on construction.

        Parameters:
            rgba (tuple[int, ...]): A tuple of RGBA values, each in [0, 255].
            frequency (float): The frequency of the color.
        """
        assert len(rgba) == 4, "RGBA values must be a tuple of length 4"
        r, g, b, alpha = (int(round(float(v))) for v in rgba)
        self._srgb: tuple[float, float, float] = (r / 255.0, g / 255.0, b / 255.0)
        self._alpha: float = alpha / 255.0
        self.frequency: float = frequency

    @classmethod
    def from_srgb_float(
        cls,
        srgb: tuple[float, float, float],
        frequency: float,
        alpha: float = 1.0,
    ) -> "Color":
        """
        Constructs a Color from float sRGB components in ``[0, 1]``.

        This is the precision-preserving entry point for extractors whose
        centroids live in continuous space (e.g. OKLab); it avoids the round
        trip through 8-bit that :meth:`__init__` performs. Components are
        clamped into ``[0, 1]`` so out-of-gamut centroids are handled gracefully.

        Parameters:
            srgb (tuple[float, float, float]): Gamma-encoded sRGB components.
            frequency (float): The frequency of the color.
            alpha (float): Alpha in ``[0, 1]`` (default fully opaque).

        Returns:
            Color: A color whose canonical store holds the given floats.
        """
        obj = cls.__new__(cls)
        r, g, b = srgb
        obj._srgb = (_clamp_unit(r), _clamp_unit(g), _clamp_unit(b))
        obj._alpha = _clamp_unit(alpha)
        obj.frequency = frequency
        return obj

    @property
    def rgb_float(self) -> tuple[float, float, float]:
        """
        The canonical color as float sRGB components in ``[0, 1]``.

        Returns:
            tuple[float, float, float]: The (r, g, b) components.
        """
        return self._srgb

    @property
    def rgb(self) -> tuple[int, int, int]:
        """
        The color as 8-bit sRGB.

        Returns:
            tuple[int, int, int]: (r, g, b) as plain Python ints in [0, 255].
        """
        r, g, b = self._srgb
        return (int(round(r * 255.0)), int(round(g * 255.0)), int(round(b * 255.0)))

    @property
    def alpha(self) -> int:
        """
        The alpha channel as a raw 8-bit value (matches :attr:`rgba`).

        Returns:
            int: Alpha as a plain Python int in [0, 255].
        """
        return int(round(self._alpha * 255.0))

    @property
    def opacity(self) -> float:
        """
        The alpha channel as a fraction (opacity) in ``[0, 1]``.

        Returns:
            float: Opacity in [0, 1].
        """
        return self._alpha

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """
        The color as 8-bit RGBA.

        Returns:
            tuple[int, int, int, int]: (r, g, b, a) as plain Python ints in [0, 255].
        """
        r, g, b = self.rgb
        return (r, g, b, self.alpha)

    @property
    def a(self) -> int:
        """Deprecated alias for :attr:`alpha`."""
        warnings.warn(
            "Color.a is deprecated and will be removed; use Color.alpha instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.alpha

    @property
    def weight(self) -> float:
        """Deprecated alias for :attr:`opacity`.

        The name is misleading: in a palette context "weight" reads as relative
        importance (frequency), but it holds opacity. Use :attr:`opacity`.
        """
        warnings.warn(
            "Color.weight is deprecated and will be removed; use Color.opacity instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.opacity

    @property
    def freq(self) -> float:
        """Deprecated alias for :attr:`frequency`."""
        warnings.warn(
            "Color.freq is deprecated and will be removed; use Color.frequency instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.frequency

    def display(self, w: int = 50, h: int = 50) -> None:
        """
        Displays the color in a window of specified width and height.

        Parameters:
        w (int): Width of the window in pixels.
        h (int): Height of the window in pixels.
        """

        from PIL import Image

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
        return self.frequency < other.frequency

    def get_colors(self, colorspace: ColorSpace | str = ColorSpace.RGB) -> tuple[int, ...] | tuple[float, ...]:
        """
        Returns the color values in the specified color space.

        Parameters:
            colorspace (ColorSpace | str): The color space to use (enum member,
                its value, or case-insensitive name).

        Returns:
            tuple[int, ...] | tuple[float, ...]: The color values in the specified color space.
        """
        colorspace = coerce_to_enum(colorspace, ColorSpace, error_cls=InvalidColorspaceError)
        colors = {ColorSpace.RGB: self.rgb, ColorSpace.HSV: self.hsv, ColorSpace.HLS: self.hls}
        return colors[colorspace]

    @property
    def hsv(self) -> tuple[float, float, float]:
        """
        Converts the color to HSV color space, derived from the canonical float store.

        Returns:
            tuple[float, float, float]: The color values in HSV color space.
        """
        return colorsys.rgb_to_hsv(*self._srgb)

    @property
    def hls(self) -> tuple[float, float, float]:
        """
        Converts the color to HLS color space, derived from the canonical float store.

        Returns:
            tuple[float, float, float]: The color values in HLS color space.
        """
        return colorsys.rgb_to_hls(*self._srgb)

    @property
    def hex(self) -> str:
        """
        Returns the color as a hexadecimal string.

        Returns:
            str: The color in hexadecimal format (e.g., "#FF5733").
        """
        r, g, b = self.rgb
        return f"#{r:02X}{g:02X}{b:02X}"

    @property
    def luminance(self) -> float:
        """
        Calculates the luminance of the color, derived from the canonical float store.

        Returns:
        float: The luminance of the color, on the same 0-255 scale as the 8-bit channels.
        """
        return float(np.dot(luminance_weights, self._srgb)) * 255.0
