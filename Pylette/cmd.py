import argparse
import time
from enum import Enum
from pathlib import Path
from typing import List, Optional

import typer
from rich.live import Live
from rich.panel import Panel
from typer import Typer
from typing_extensions import Annotated

from Pylette import extract_colors
from Pylette.cmd_utils import create_color_box, create_rich_table
from Pylette.src.types import ColorSpace, ExtractionMode, SortMode

app = Typer()


@app.command()
def extract(
    image: Annotated[List[Path], typer.Argument(help="Path(s) to the image-file(s)")],
    palette_size: Annotated[int, typer.Option(help="Number of colors to extract")] = 5,
    sort_by: Annotated[
        SortMode, typer.Option(help="Sort by luminance or frequency")
    ] = SortMode.luminance.value,
    extraction_mode: Annotated[
        ExtractionMode, typer.Option(help="The color quantization algorithm to use")
    ] = ExtractionMode.KMeans.value,
    resize: Annotated[
        bool, typer.Option(help="Whether to resize the image before processing")
    ] = True,
    color_space: Annotated[
        ColorSpace, typer.Option(help="Color space to represent colors in")
    ] = ColorSpace.RGB.value,
    save_to_directory: Annotated[
        Optional[bool],
        typer.Option(
            help="Whether to save the csv file(s) to a directory. Will save to the image's directory, unless --output-directory is specified."
        ),
    ] = False,
    output_directory: Annotated[
        Optional[Path],
        typer.Option(
            help="Directory to save the csv file(s). Requires --save-to-directory."
        ),
    ] = None,
):
    table = create_rich_table()
    with Live(table, refresh_per_second=4, transient=False):
        for img_path in image:
            palette = extract_colors(
                img_path,
                palette_size=palette_size,
                sort_mode=sort_by,
                mode=extraction_mode,
                resize=resize,
            )

            color_grid = create_color_box(palette)
            table.add_row(f"{img_path.stem}", color_grid)

            if save_to_directory:
                if output_directory is None:
                    output_directory = img_path.parent
                if not output_directory.exists():
                    output_directory.mkdir()
                palette.to_csv(
                    filename=output_directory / f"{img_path.stem}_palette.csv",
                    frequency=True,
                    color_space=color_space,
                    stdout=False,
                )


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
