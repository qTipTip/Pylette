import os
import urllib.parse
from enum import Enum
from io import BytesIO
from typing import Any, Literal, TypeAlias, Union

import numpy as np
import requests  # type: ignore
from numpy.typing import NDArray
from PIL import Image

from Pylette.src.extractors.k_means import k_means_extraction
from Pylette.src.extractors.median_cut import median_cut_extraction
from Pylette.src.palette import Palette

ImageType_T: TypeAlias = Union["os.PathLike[Any]", bytes, NDArray[float], str]


class ImageType(str, Enum):
    PATH = "path"
    BYTES = "bytes"
    ARRAY = "array"
    URL = "url"
    NONE = "none"


def _parse_image_type(image: ImageType_T) -> ImageType:
    """
    Determines the type of the input image.

    Parameters:
    image (ImageType_T): The input image.

    Returns:
    ImageType: The type of the input image.
    """
    match image:
        case np.ndarray():
            image_type = ImageType.ARRAY
        case os.PathLike():
            image_type = ImageType.PATH
        case bytes():
            image_type = ImageType.BYTES
        case str():
            try:
                result = urllib.parse.urlparse(image)
                if all([result.scheme, result.netloc]):
                    image_type = ImageType.URL
                else:
                    image_type = ImageType.PATH
            except ValueError:
                image_type = ImageType.PATH
        case _:
            image_type = ImageType.NONE
    return image_type


def extract_colors(
    image: ImageType_T,
    palette_size: int = 5,
    resize: bool = True,
    mode: Literal["KM"] | Literal["MC"] = "KM",
    sort_mode: Literal["luminance", "frequency"] | None = None,
    alpha_mask_threshold: int | None = None,
) -> Palette:
    """
    Extracts a set of 'palette_size' colors from the given image.

    Parameters:
        image: The input image.
        palette_size: The number of colors to extract.
        resize: Whether to resize the image before processing.
        mode: The color quantization algorithm to use.
        sort_mode: The mode to sort colors.
        alpha_mask_threshold: Optional integer between 0, 255.
            Any pixel with alpha less than this threshold will be discarded from calculations.
    Returns:
        Palette: A palette of the extracted colors.

    Examples:
        Colors can be extracted from a variety of sources, including local files, byte streams, URLs, and numpy arrays.

        >>> extract_colors("path/to/image.jpg", palette_size=5, resize=True, mode="KM", sort_mode="luminance")
        >>> extract_colors(b"image_bytes", palette_size=5, resize=True, mode="KM", sort_mode="luminance")
    """

    image_type = _parse_image_type(image)

    match image_type:
        case ImageType.PATH:
            img_obj = Image.open(image)
        case ImageType.BYTES:
            assert isinstance(image, bytes)
            img_obj = Image.open(BytesIO(image))
        case ImageType.URL:
            assert isinstance(image, str)
            img_obj = request_image(image)
        case ImageType.ARRAY:
            img_obj = Image.fromarray(image)
        case ImageType.NONE:
            raise ValueError(f"Unable to parse image source. Got image type {type(image)}")

    # Convert to RGBA
    img = img_obj.convert("RGBA")

    # open the image
    if resize:
        img = img.resize((256, 256))

    width, height = img.size
    arr = np.asarray(img)

    if alpha_mask_threshold is None:
        alpha_mask_threshold = 0

    alpha_mask = arr[:, :, 3] <= alpha_mask_threshold
    valid_pixels = arr[~alpha_mask]

    if mode == "KM":
        colors = k_means_extraction(valid_pixels, height, width, palette_size)
    elif mode == "MC":
        colors = median_cut_extraction(valid_pixels, height, width, palette_size)
    else:
        raise NotImplementedError("Extraction mode not implemented")

    if sort_mode == "luminance":
        colors.sort(key=lambda c: c.luminance, reverse=False)
    else:
        colors.sort(reverse=True)

    return Palette(colors)


def request_image(image_url: str) -> Image.Image:
    """
    Requests an image from a given URL.

    Parameters:
        image_url (str): The URL of the image.

    Returns:
        Image.Image: The requested image.

    Raises:
        ValueError: If the URL does not point to a valid image.
    """
    response = requests.get(image_url)
    # Check if the request was successful and content type is an image
    if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
        img = Image.open(BytesIO(response.content))
        return img
    else:
        raise ValueError("The URL did not point to a valid image.")
