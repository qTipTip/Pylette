import pathlib
from enum import Enum
from typing import List

import typer

from Pylette.src.color_extraction import batch_extract_colors


class ExtractionMode(str, Enum):
    KM = "KM"
    MC = "MC"


class SortBy(str, Enum):
    frequency = "frequency"
    luminance = "luminance"


class ColorSpace(str, Enum):
    rgb = "rgb"
    hsv = "hsv"
    hls = "hls"


pylette_app = typer.Typer()


@pylette_app.command()
def main(
    ctx: typer.Context,
    image_sources: List[str],  # These can be paths or URLs
    mode: ExtractionMode = ExtractionMode.KM,
    n: int = 5,
    sort_by: SortBy = SortBy.luminance,
    stdout: bool = True,
    out_filename: pathlib.Path | None = None,
    display_colors: bool = False,
    colorspace: ColorSpace = ColorSpace.rgb,
    alpha_mask_threshold: int | None = typer.Option(
        None,
        min=0,
        max=255,
        help="Alpha threshold for transparent image masking (0-255). Pixels with alpha below this value are excluded.",
    ),
):
    if not image_sources:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)

    output_file_path = str(out_filename) if out_filename is not None else None
    try:
        palettes = batch_extract_colors(
            images=image_sources,
            palette_size=n,
            sort_mode=sort_by.value,
            mode=mode.value,
            alpha_mask_threshold=alpha_mask_threshold,
        )
    except ValueError as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)

    for palette in palettes:
        palette.to_csv(filename=output_file_path, frequency=True, stdout=stdout, colorspace=colorspace.value)
        if display_colors:
            palette.display()


def docs():
    typer.launch("https://qtiptip.github.io/Pylette/")


def main_typer() -> None:
    pylette_app()
