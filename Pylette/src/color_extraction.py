import urllib.parse
from io import BytesIO
from pathlib import Path
from typing import Literal

import numpy as np
import requests
from PIL import Image

from Pylette.src.extractors.k_means import k_means_extraction
from Pylette.src.extractors.median_cut import median_cut_extraction
from Pylette.src.palette import Palette
from Pylette.src.types import ImageInput, PILImage


def _is_url(image_str: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        result = urllib.parse.urlparse(image_str)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def _normalize_image_input(image: ImageInput) -> PILImage:
    """Convert any valid image input to PIL Image."""
    if isinstance(image, Image.Image):
        return image
    elif isinstance(image, (str, Path)):
        image_str = str(image)
        if _is_url(image_str):
            return request_image(image_str)
        else:
            return Image.open(image)
    elif isinstance(image, bytes):
        return Image.open(BytesIO(image))
    elif hasattr(image, "__array__"):  # More general check for array-like objects
        return Image.fromarray(image)
    else:
        raise TypeError(f"Unsupported image type: {type(image)}")


def extract_colors(
    image: ImageInput,
    palette_size: int = 5,
    resize: bool = True,
    mode: Literal["KM", "MC"] = "KM",
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

    # Normalize input to PIL Image and convert to RGBA
    img_obj = _normalize_image_input(image)
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

    match mode:
        case "KM":
            colors = k_means_extraction(valid_pixels, height, width, palette_size)
        case "MC":
            colors = median_cut_extraction(valid_pixels, height, width, palette_size)

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
