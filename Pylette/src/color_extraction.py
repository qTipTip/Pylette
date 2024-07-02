import os
import urllib.parse
from enum import Enum
from io import BytesIO
from typing import TYPE_CHECKING, Any, AnyStr, Literal, Union

import numpy as np
import requests  # type: ignore
from numpy.typing import NDArray
from PIL import Image
from sklearn.cluster import KMeans

from Pylette.src.color import Color
from Pylette.src.palette import Palette
from Pylette.src.utils import ColorBox

ImageType_T = Union["os.PathLike[Any]", bytes, NDArray[float], str]


class ImageType(str, Enum):
    PATH = "path"
    BYTES = "bytes"
    ARRAY = "array"
    URL = "url"
    NONE = "none"


def median_cut_extraction(
    arr: np.ndarray, height: int, width: int, palette_size: int
) -> list[Color]:
    """
    Extracts a color palette using the median cut algorithm.
    :param arr:
    :param height:
    :param width:
    :param palette_size:
    :return:
    """

    arr = arr.reshape((width * height, -1))
    c = [ColorBox(arr)]
    full_box_size = c[0].size

    # Each iteration, find the largest box, split it, remove original box from list of boxes, and add the two new boxes.
    while len(c) < palette_size:
        largest_c_idx = np.argmax(c)
        # add the two new boxes to the list, while removing the split box.
        c = c[:largest_c_idx] + c[largest_c_idx].split() + c[largest_c_idx + 1 :]

    colors = [
        Color(tuple(map(int, box.average)), box.size / full_box_size) for box in c
    ]

    return colors


def _parse_image_type(image: ImageType_T) -> ImageType:
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
    image: ImageType_T | None = None,
    palette_size: int = 5,
    resize: bool = True,
    mode: Literal["KM"] | Literal["MC"] = "KM",
    sort_mode: Literal["luminance", "frequency"] | None = None,
) -> Palette:
    """
    Extracts a set of 'palette_size' colors from the given image.
    :param image_bytes: bytes representing the image data
    :param image: path to Image file
    :param image_url: url to the image-file
    :param palette_size: number of colors to extract
    :param resize: whether to resize the image before processing, yielding faster results with lower quality
    :param mode: the color quantization algorithm to use. Currently supports K-Means (KM) and Median Cut (MC)
    :param sort_mode: sort colors by luminance, or by frequency
    :return: a list of the extracted colors
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
            raise ValueError(
                f"Unable to parse image source. Got image type {type(image)}"
            )

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
    response = requests.get(image_url)
    # Check if the request was successful and content type is an image
    if response.status_code == 200 and "image" in response.headers.get(
        "Content-Type", ""
    ):
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img
    else:
        raise ValueError("The URL did not point to a valid image.")


def k_means_extraction(
    arr: NDArray[float], height: int, width: int, palette_size: int
) -> list[Color]:
    """
    Extracts a color palette using KMeans.
    :param arr: pixel array (height, width, 3)
    :param height: height
    :param width: width
    :param palette_size: number of colors
    :return: a palette of colors sorted by frequency
    """
    arr = np.reshape(arr, (width * height, -1))
    model = KMeans(
        n_clusters=palette_size, n_init="auto", init="k-means++", random_state=2024
    )
    labels = model.fit_predict(arr)
    palette = np.array(model.cluster_centers_, dtype=int)
    color_count = np.bincount(labels)
    color_frequency = color_count / float(np.sum(color_count))
    colors = []
    for color, freq in zip(palette, color_frequency):
        colors.append(Color(color, freq))
    return colors
