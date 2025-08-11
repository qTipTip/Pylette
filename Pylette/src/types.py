"""
Centralized type definitions for Pylette.

This module contains all the type aliases and protocols used throughout the Pylette library
to ensure type safety and consistency.
"""

from pathlib import Path
from typing import Any, Protocol, TypeAlias

import numpy as np
from numpy.typing import NDArray
from PIL import Image


class ImageLike(Protocol):
    """Protocol for image-like objects that can be converted to PIL Image."""

    pass


class ArrayLike(Protocol):
    """Protocol for array-like objects."""

    def __array__(self) -> NDArray[np.uint8]: ...


# Specific image input types
PathLikeImage: TypeAlias = str | Path
URLImage: TypeAlias = str  # URLs are strings but semantically different
BytesImage: TypeAlias = bytes
ArrayImage: TypeAlias = NDArray[np.uint8]  # Properly typed array
PILImage: TypeAlias = Image.Image

# Main union type - more restrictive and logical
ImageInput: TypeAlias = PathLikeImage | URLImage | BytesImage | ArrayImage | PILImage

# Color array types
ColorArray: TypeAlias = NDArray[np.uint8]  # For RGB/RGBA color data
FloatArray: TypeAlias = NDArray[np.floating[Any]]  # For calculations
IntArray: TypeAlias = NDArray[np.integer[Any]]  # For integer arrays

# Color tuple types
RGBTuple: TypeAlias = tuple[int, int, int]
RGBATuple: TypeAlias = tuple[int, int, int, int]
ColorTuple: TypeAlias = RGBTuple | RGBATuple
