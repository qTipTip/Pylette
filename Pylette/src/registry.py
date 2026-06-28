"""
Registry of color-extraction algorithms
"""

from typing import Callable, TypeVar

from Pylette.src.extractors.protocol import ColorExtractor
from Pylette.src.types import ExtractionMethod

_REGISTRY: dict[ExtractionMethod, ColorExtractor] = {}
_E = TypeVar("_E", bound=ColorExtractor)


def register(method: ExtractionMethod) -> Callable[[type[_E]], type[_E]]:
    """
    Register an extractor under ``method``.

    The decorated class is instantiated once at import-time and stored in the
    registry. The decorator is transparent, as the class is returned unchanged.

    Raises:
        ValueError: If an extractor is already registered for ``method``.
    """

    def decorator(cls: type[_E]) -> type[_E]:
        if method in _REGISTRY:
            existing = type(_REGISTRY[method]).__name__
            raise ValueError(f"An extractor is already registered for {method} ({existing}).")
        _REGISTRY[method] = cls()
        return cls

    return decorator
