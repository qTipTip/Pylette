"""
Centralized type definitions for pylette.

This module contains all the type aliases and protocols used throughout the Pylette library
to ensure type safety and consistency.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, TypeAlias, TypedDict, TypeVar

import numpy as np
from cv2.typing import MatLike
from numpy.typing import NDArray
from PIL import Image

if TYPE_CHECKING:
    from pylette.src.palette import Palette


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
CV2Image: TypeAlias = MatLike
PILImage: TypeAlias = Image.Image

# Main union type - more restrictive and logical
ImageInput: TypeAlias = PathLikeImage | URLImage | BytesImage | ArrayImage | PILImage | CV2Image

# Color array types
ColorArray: TypeAlias = NDArray[np.uint8]  # For RGB/RGBA color data
FloatArray: TypeAlias = NDArray[np.floating[Any]]  # For calculations
IntArray: TypeAlias = NDArray[np.integer[Any]]  # For integer arrays

# Color tuple types
RGBTuple: TypeAlias = tuple[int, int, int]
RGBATuple: TypeAlias = tuple[int, int, int, int]
ColorTuple: TypeAlias = RGBTuple | RGBATuple


class ExtractionMethod(str, Enum):
    MC = "MedianCut"
    KM = "KMeans"
    OKLAB = "OKLab"


class ColorSpace(str, Enum):
    RGB = "rgb"
    HSV = "hsv"
    HLS = "hls"


_EnumT = TypeVar("_EnumT", bound=Enum)


def coerce_to_enum(value: "_EnumT | str", enum_cls: type[_EnumT]) -> _EnumT:
    """Coerce ``value`` to a member of ``enum_cls``.

    Accepts an existing member, the member's value, or its (case-insensitive)
    name. This is the single place that turns user-facing strings into enums
    (e.g. ``mode`` and ``colorspace``), replacing acceptance scattered across the
    registry, ``extract_colors``, and JSON export.

    Raises:
        ValueError: If ``value`` matches no member of ``enum_cls``.
    """
    if isinstance(value, enum_cls):
        return value
    if isinstance(value, str):
        try:
            return enum_cls(value)
        except ValueError:
            pass
        try:
            return enum_cls[value.upper()]
        except KeyError:
            pass
    valid = ", ".join(f"{m.name}/{m.value}" for m in enum_cls)
    raise ValueError(f"Unknown {enum_cls.__name__} {value!r}. Valid options: {valid}.")


# PaletteMetaData Types
class SourceType(str, Enum):
    FILE_PATH = "file_path"
    URL = "url"
    BYTES = "bytes"
    PIL_IMAGE = "pil_image"
    NUMPY_ARRAY = "numpy_array"
    CV2_IMAGE = "cv2_image"
    UNKNOWN = "unknown"


class ExtractionParams(TypedDict):
    palette_size: int
    mode: ExtractionMethod
    sort_mode: str | None
    resize: bool
    alpha_mask_threshold: int | None


class ImageInfo(TypedDict):
    original_size: tuple[int, int]
    processed_size: tuple[int, int]
    format: str | None
    mode: str
    has_alpha: bool


class ProcessingStats(TypedDict):
    total_pixels: int
    valid_pixels: int
    extraction_time: float | None
    timestamp: str


class PaletteMetaData(TypedDict):
    image_source: str
    source_type: SourceType
    extraction_params: ExtractionParams
    image_info: ImageInfo
    processing_stats: ProcessingStats


# Batch extraction types
@dataclass
class BatchResult:
    source: ImageInput
    result: "Palette | None" = None
    exception: Exception | None = None

    @property
    def success(self) -> bool:
        return self.result is not None

    @property
    def palette(self) -> "Palette | None":
        return self.result

    @property
    def error(self) -> "Exception | None":
        return self.exception
