import pathlib
from enum import Enum

import typer

from Pylette import extract_colors


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
    filename: pathlib.Path | None = None,
    image_url: str | None = None,
    mode: ExtractionMode = ExtractionMode.KM,
    n: int = 5,
    sort_by: SortBy = SortBy.luminance,
    stdout: bool = True,
    out_filename: pathlib.Path | None = None,
    display_colors: bool = False,
    colorspace: ColorSpace = ColorSpace.rgb,
    alpha_mask_threshold: int | None = typer.Option(None, min=0, max=255, help="Alpha threshold for transparent image masking (0-255). Pixels with alpha below this value are excluded."),
):
    if filename is None and image_url is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)
    
    if filename is not None and image_url is not None:
        typer.echo("Please provide either a filename or an image-url, but not both.")
        raise typer.Exit(code=1)

    image: pathlib.Path | str | None
    if filename is not None and image_url is None:
        image = filename
    else:
        image = image_url

    output_file_path = str(out_filename) if out_filename is not None else None
    palette = extract_colors(image=image, palette_size=n, sort_mode=sort_by.value, mode=mode.value, alpha_mask_threshold=alpha_mask_threshold)
    palette.to_csv(filename=output_file_path, frequency=True, stdout=stdout, colorspace=colorspace.value)
    if display_colors:
        palette.display()


def docs():
    typer.launch("https://qtiptip.github.io/Pylette/")


def main_typer() -> None:
    pylette_app()
