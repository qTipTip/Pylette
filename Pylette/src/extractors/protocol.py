from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

import numpy as np
from numpy.typing import NDArray

from Pylette.src.color import Color

NP_T = TypeVar("NP_T", bound=np.generic, covariant=True)


@runtime_checkable
class ColorExtractor(Protocol):
    def extract(self, arr: NDArray[NP_T], height: int, width: int, palette_size: int) -> list[Color]: ...


class ColorExtractorBase(ABC):
    @abstractmethod
    def extract(self, arr: NDArray[NP_T], height: int, width: int, palette_size: int) -> list[Color]:
        pass

    def _reshape_array(self, arr: NDArray[NP_T], height: int, width: int) -> NDArray[NP_T]:
        # Reshape to (n_pixels, n_channels) from the array's actual length.
        # Spatial dimensions aren't needed for color clustering.
        return arr.reshape((-1, arr.shape[-1]))
