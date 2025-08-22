"""
This module allows users to import types in multiple ways:
- from pylette.types import ImageInput
- import pylette.types as types
"""

from Pylette.src.types import (
    ArrayImage,
    ArrayLike,
    BatchResult,
    BytesImage,
    ColorArray,
    ColorSpace,
    ColorTuple,
    CV2Image,
    ExtractionMethod,
    ExtractionParams,
    FloatArray,
    ImageInfo,
    ImageInput,
    ImageLike,
    IntArray,
    PaletteMetaData,
    PathLikeImage,
    PILImage,
    ProcessingStats,
    RGBATuple,
    RGBTuple,
    SourceType,
    URLImage,
)

# Define what gets exported with "from pylette.types import *"
__all__ = [
    "ImageInput",
    "ImageLike",
    "ArrayLike",
    "PathLikeImage",
    "URLImage",
    "BytesImage",
    "ArrayImage",
    "CV2Image",
    "PILImage",
    "ColorArray",
    "FloatArray",
    "IntArray",
    "RGBTuple",
    "RGBATuple",
    "ColorTuple",
    "ExtractionMethod",
    "ColorSpace",
    "SourceType",
    "ExtractionParams",
    "ImageInfo",
    "ProcessingStats",
    "PaletteMetaData",
    "BatchResult",
]
