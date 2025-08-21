import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
from typing import Callable, Literal, Sequence

import numpy as np
from PIL import Image

from Pylette.src.extractors.k_means import k_means_extraction
from Pylette.src.extractors.median_cut import median_cut_extraction
from Pylette.src.palette import Palette
from Pylette.src.types import BatchResult, ExtractionMethod, ImageInput, PaletteMetaData, PILImage


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


def batch_extract_colors(
    images: Sequence[ImageInput],
    palette_size: int = 5,
    resize: bool = True,
    mode: ExtractionMethod = ExtractionMethod.KM,
    sort_mode: Literal["luminance", "frequency"] | None = None,
    alpha_mask_threshold: int | None = None,
    max_workers: int | None = None,
    progress_callback: Callable[[int, BatchResult], None] | None = None,
) -> list[BatchResult]:
    """Extract colors from multiple images in parallel.

    Args:
        progress_callback: Optional callback function called when each task completes.
                         Receives (task_number, result) as arguments.
    """

    def thread_fn(image: ImageInput):
        return extract_colors(
            image=image,
            palette_size=palette_size,
            resize=resize,
            mode=mode,
            sort_mode=sort_mode,
            alpha_mask_threshold=alpha_mask_threshold,
        )

    results: list[BatchResult] = []
    task_number = 1

    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="pylette") as executor:
        futures_to_image_map = {executor.submit(thread_fn, image): image for image in images}

        for future in as_completed(futures_to_image_map):
            source_image = futures_to_image_map[future]
            try:
                r = future.result()
                batch_result = BatchResult(source=source_image, result=r)
                results.append(batch_result)
                if progress_callback:
                    progress_callback(task_number, batch_result)
            except Exception as e:
                batch_result = BatchResult(source=source_image, exception=e)
                results.append(batch_result)
                if progress_callback:
                    progress_callback(task_number, batch_result)
            task_number += 1

    # Return results in original order
    source_to_result = {r.source: r for r in results}
    return [source_to_result[source] for source in images]


def extract_colors(
    image: ImageInput,
    palette_size: int = 5,
    resize: bool = True,
    mode: ExtractionMethod = ExtractionMethod.KM,
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

    if len(valid_pixels) == 0:
        raise ValueError(
            f"No valid pixels remain after applying alpha mask with threshold {alpha_mask_threshold}. "
            f"Try using a lower alpha-mask-threshold value or check if your image has transparency."
        )

    match mode:
        case ExtractionMethod.KM:
            colors = k_means_extraction(valid_pixels, height, width, palette_size)
        case ExtractionMethod.MC:
            colors = median_cut_extraction(valid_pixels, height, width, palette_size)

    if colors:
        if sort_mode == "luminance":
            colors.sort(key=lambda c: c.luminance, reverse=False)
        else:
            colors.sort(reverse=True)

    return Palette(colors, metadata=PaletteMetaData(image_source=str(image), extraction_method=mode))


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

    import requests

    response = requests.get(image_url)
    # Check if the request was successful and content type is an image
    if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
        img = Image.open(BytesIO(response.content))
        return img
    else:
        raise ValueError("The URL did not point to a valid image.")
