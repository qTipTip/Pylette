"""
Registry of color-extraction algorithms
"""

from Pylette.src.extractors.protocol import ColorExtractor
from Pylette.src.types import ExtractionMethod

_REGISTRY: dict[ExtractionMethod, ColorExtractor] = {}
