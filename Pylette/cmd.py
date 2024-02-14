import argparse
from enum import Enum
from pathlib import Path
from typing import List, Optional

import typer
from typer import Typer
from typing_extensions import Annotated

from Pylette import extract_colors
from Pylette.src.types import SortMode

app = Typer()


@app.command()
def extract(
    image: Annotated[List[Path], typer.Argument(help="Path(s) to the image-file(s)")],
    palette_size: Annotated[int, typer.Option(help="Number of colors to extract")] = 5,
    sort_by: Annotated[
        SortMode, typer.Option(help="Sort by luminance or frequency")
    ] = SortMode.luminance.value,
):

    for img_path in image:
        palette = extract_colors(img_path, palette_size=palette_size, sort_mode=sort_by)
        palette.display()


@app.command()
def help():
    pass


def old_main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--filename", help="path to image file", type=str, default=None)
    group.add_argument(
        "--image-url", help="url to the image file", type=str, default=None
    )

    parser.add_argument(
        "--mode",
        help="extraction_mode (KMeans/MedianCut",
        type=str,
        default="KM",
        choices=["KM", "MC"],
    )
    parser.add_argument(
        "--n", help="the number of colors to extract", type=int, default=5
    )
    parser.add_argument(
        "--sort_by",
        help="sort by luminance or frequency",
        default="luminance",
        type=str,
        choices=["luminance", "frequency"],
    )
    parser.add_argument(
        "--stdout",
        help="whether to display the extracted color values in the stdout",
        type=bool,
        default=True,
    )
    parser.add_argument(
        "--colorspace",
        help="color space to represent colors in",
        default="RGB",
        type=str,
        choices=["rgb", "hsv", "hls"],
    )
    parser.add_argument(
        "--out_filename", help="where to save the csv file", default=None, type=str
    )
    parser.add_argument(
        "--display-colors",
        help="Open a window displaying the extracted palette",
        default=False,
        type=bool,
    )
    args = parser.parse_args()
    palette = extract_colors(
        args.filename, args.image_url, palette_size=args.n, sort_mode=args.sort_by
    )

    palette.to_csv(filename=args.out_filename, frequency="True", stdout=args.stdout)
    if args.display_colors:
        palette.display()


def main():
    app()
