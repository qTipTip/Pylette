"""
Registry of color-extraction algorithms
"""

from typing import Callable, TypeVar

from pylette.src.exceptions import UnknownExtractionMethodError
from pylette.src.extractors.protocol import ColorExtractor
from pylette.src.types import ExtractionMethod, coerce_to_enum

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


def get_extractor(method: ExtractionMethod | str) -> ColorExtractor:
    """
    Return the extractor registered for ``method``.

    Raises:
        UnknownExtractionMethodError: If ``method`` is not a known method or has
            no registered extractor.
    """

    method = coerce_to_enum(method, ExtractionMethod, error_cls=UnknownExtractionMethodError)

    try:
        return _REGISTRY[method]
    except KeyError:
        available = ", ".join(sorted(m.value for m in _REGISTRY)) or "(none)"
        raise UnknownExtractionMethodError(
            f"No extractor registered for {method.value}. Registered: {available}."
        ) from None


def available_methods() -> list[ExtractionMethod]:
    """
    Return the extraction methods that currently have a registered extractor.
    """
    return list(_REGISTRY)
