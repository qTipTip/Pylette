import os
import urllib.parse
from enum import Enum
from io import BytesIO
from typing import Any, Literal, TypeAlias, Union

import numpy as np
import requests  # type: ignore
from numpy.typing import NDArray
from PIL import Image
from sklearn.cluster import KMeans

from Pylette.src.color import Color
from Pylette.src.palette import Palette
from Pylette.src.utils import ColorBox

ImageType_T: TypeAlias = Union["os.PathLike[Any]", bytes, NDArray[float], str]


class ImageType(str, Enum):
    PATH = "path"
    BYTES = "bytes"
    ARRAY = "array"
    URL = "url"
    NONE = "none"


def median_cut_extraction(arr: np.ndarray, height: int, width: int, palette_size: int) -> list[Color]:
    """
    Extracts a color palette using the median cut algorithm.

    Parameters:
        arr (np.ndarray): The input array.
        height (int): The height of the image.
        width (int): The width of the image.
        palette_size (int): The number of colors to extract from the image.

    Returns:
        list[Color]: A list of colors extracted from the image.
    """

    arr = arr.reshape((width * height, -1))
    c = [ColorBox(arr)]
    full_box_size = c[0].size

    # Each iteration, find the largest box, split it, remove original box from list of boxes, and add the two new boxes.
    while len(c) < palette_size:
        largest_c_idx = np.argmax(c)
        # add the two new boxes to the list, while removing the split box.
        c = c[:largest_c_idx] + c[largest_c_idx].split() + c[largest_c_idx + 1 :]

    colors = [Color(tuple(map(int, box.average)), box.size / full_box_size) for box in c]

    return colors


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
) -> Palette:
    """
    Extracts a set of 'palette_size' colors from the given image.

    Parameters:
        image: The input image.
        palette_size: The number of colors to extract.
        resize: Whether to resize the image before processing.
        mode: The color quantization algorithm to use.
        sort_mode: The mode to sort colors.

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
            img = Image.open(image).convert("RGB")
        case ImageType.BYTES:
            assert isinstance(image, bytes)
            img = Image.open(BytesIO(image)).convert("RGB")
        case ImageType.URL:
            assert isinstance(image, str)
            img = request_image(image)
        case ImageType.ARRAY:
            img = Image.fromarray(image).convert("RGB")
        case ImageType.NONE:
            raise ValueError(f"Unable to parse image source. Got image type {type(image)}")

    # open the image
    if resize:
        img = img.resize((256, 256))
    width, height = img.size
    arr = np.asarray(img)

    if mode == "KM":
        colors = k_means_extraction(arr, height, width, palette_size)
    elif mode == "MC":
        colors = median_cut_extraction(arr, height, width, palette_size)
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
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img
    else:
        raise ValueError("The URL did not point to a valid image.")


def k_means_extraction(arr: NDArray[float], height: int, width: int, palette_size: int) -> list[Color]:
    """
    Extracts a color palette using KMeans.

    Parameters:
        arr (NDArray[float]): The input array.
        height (int): The height of the image.
        width (int): The width of the image.
        palette_size (int): The number of colors to extract from the image.

    Returns:
        list[Color]: A palette of colors sorted by frequency.
    """
    arr = np.reshape(arr, (width * height, -1))
    model = KMeans(n_clusters=palette_size, n_init="auto", init="k-means++", random_state=2024)
    labels = model.fit_predict(arr)
    palette = np.array(model.cluster_centers_, dtype=int)
    color_count = np.bincount(labels)
    color_frequency = color_count / float(np.sum(color_count))
    colors = []
    for color, freq in zip(palette, color_frequency):
        colors.append(Color(color, freq))
    return colors
