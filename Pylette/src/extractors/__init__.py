# Import for registration side-effect
from Pylette.src.extractors import k_means as _k_means  # type: ignore # noqa: F401
from Pylette.src.extractors import median_cut as _median_cut  # type: ignore  # noqa: F401
from Pylette.src.extractors.registry import available_methods, get_extractor, register

__all__ = ["available_methods", "get_extractor", "register"]
