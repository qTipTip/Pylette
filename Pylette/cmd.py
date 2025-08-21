import pathlib
from enum import Enum
from typing import Annotated, List

import typer

from Pylette.src.cli_utils import PyletteProgress
from Pylette.src.color_extraction import batch_extract_colors
from Pylette.src.types import BatchResult, ExtractionMethod


class SortBy(str, Enum):
    frequency = "frequency"
    luminance = "luminance"


class ColorSpace(str, Enum):
    rgb = "rgb"
    hsv = "hsv"
    hls = "hls"


pylette_app = typer.Typer()


@pylette_app.command(no_args_is_help=True)
def main(
    image_sources: Annotated[
        List[str], typer.Argument(help="A list of paths / directories / URLs pointing to images.")
    ],  # These can be paths or URLs
    mode: ExtractionMethod = ExtractionMethod.KM,
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
    num_threads: int | None = typer.Option(
        None, min=1, help="Number of threads used for batch extraction of color palettes"
    ),
):
    output_file_path = str(out_filename) if out_filename is not None else None

    # Set up progress bar for CLI
    with PyletteProgress(palette_size=n) as progress:
        task_id = progress.add_task("Extracting colors...", total=len(image_sources))

        def progress_callback(task_number: int, result: BatchResult):
            if result.success and result.palette:
                progress.mark_task_complete(
                    task_number=task_number,
                    task_id=task_id,
                    completed_task_name=result.palette.metadata["image_source"] if result.palette.metadata else "",
                    palette_colors=result.palette.colors,
                )
            else:
                progress.update(task_id, advance=1)

        results = batch_extract_colors(
            images=image_sources,
            palette_size=n,
            sort_mode=sort_by.value,
            mode=mode,
            alpha_mask_threshold=alpha_mask_threshold,
            max_workers=num_threads,
            progress_callback=progress_callback,
        )

    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    for success in successful:
        if success.palette is not None:
            success.palette.to_csv(
                filename=output_file_path, frequency=True, stdout=stdout, colorspace=colorspace.value
            )
            if display_colors:
                success.palette.display()

    if failed:
        print_extraction_summary(successful, failed)

    # If we have no successful extractions, return with code 1
    if not successful:
        raise typer.Exit(1)
    # Otherwise, if we have some failures, return with code 2
    elif failed:
        raise typer.Exit(2)


def print_extraction_summary(successful: list[BatchResult], failed: list[BatchResult]):
    total = len(successful) + len(failed)

    if successful:
        typer.secho(f"✓ Processed {len(successful)}/{total} images successfully", fg=typer.colors.GREEN)
    if failed:
        typer.secho(f"✗ {len(failed)} images failed:", fg=typer.colors.RED)
        for result in failed:
            error_msg = str(result.error)
            typer.secho(f"{result.source}: {error_msg}", err=True)


def main_typer() -> None:
    pylette_app()
