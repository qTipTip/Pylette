from pathlib import Path

from Pylette import batch_extract_colors


def test_batch_processing():
    image_path = Path(__file__).parent.parent / "data/test_image.png"

    palettes = batch_extract_colors(images=[image_path] * 2, max_workers=1)

    print(palettes)
