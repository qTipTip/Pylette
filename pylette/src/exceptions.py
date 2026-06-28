"""Typed exception hierarchy for Pylette.

Every error Pylette raises derives from :class:`PyletteError`, so a caller can
``except PyletteError`` to catch any Pylette-originated failure and branch on the
concrete subclass to identify the failure mode. The concrete subclasses also
derive from the builtin (:class:`ValueError`).
"""


class PyletteError(Exception):
    """Base class for every error raised by Pylette."""


class InvalidImageError(PyletteError, ValueError):
    """An input image could not be loaded, or its type is unsupported."""


class NoValidPixelsError(PyletteError, ValueError):
    """No pixels remain to extract a palette from (e.g. a fully alpha-masked image)."""


class UnknownExtractionMethodError(PyletteError, ValueError):
    """The requested extraction method is not a registered/known method."""


class InvalidColorspaceError(PyletteError, ValueError):
    """The requested color space is not recognized."""


class InvalidHarmonyError(PyletteError, ValueError):
    """The requested color-harmony kind is not recognized."""
