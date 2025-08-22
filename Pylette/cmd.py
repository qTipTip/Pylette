import json
import pathlib
from enum import Enum
from typing import Annotated, List

import typer
from rich.console import Console
from rich.table import Table

from Pylette.src.cli_utils import PyletteProgress
from Pylette.src.color_extraction import batch_extract_colors
from Pylette.src.types import BatchResult, ColorSpace, ExtractionMethod


class SortBy(str, Enum):
    frequency = "frequency"
    luminance = "luminance"


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
    colorspace: ColorSpace = ColorSpace.RGB,
    alpha_mask_threshold: int | None = typer.Option(
        None,
        min=0,
        max=255,
        help="Alpha threshold for transparent image masking (0-255). Pixels with alpha below this value are excluded.",
    ),
    num_threads: int | None = typer.Option(
        None, min=1, help="Number of threads used for batch extraction of color palettes"
    ),
    export_json: bool = typer.Option(False, "--export-json", help="Export palettes to JSON format"),
    output: pathlib.Path | None = typer.Option(
        None,
        "--output",
        help="Output file or directory for JSON export."
        "If directory: creates individual files. If file: creates combined file.",
    ),
):
    # Validate export_json requirements
    if export_json and output is None:
        typer.echo("Error: --output is required when using --export-json", err=True)
        raise typer.Exit(1)

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

    if export_json and output:
        handle_json_export(successful, output, colorspace)
    elif stdout and successful:
        # Show clean palette summary
        display_palette_summary(successful, colorspace)

    # Display colors if requested
    if display_colors:
        for success in successful:
            if success.palette is not None:
                success.palette.display()

    if failed:
        print_extraction_summary(successful, failed)

    # If we have no successful extractions, return with code 1
    if not successful:
        raise typer.Exit(1)
    # Otherwise, if we have some failures, return with code 2
    elif failed:
        raise typer.Exit(2)


def handle_json_export(
    successful_results: list[BatchResult], output_path: pathlib.Path, colorspace: ColorSpace
) -> None:
    """Handle JSON export for successful palette extractions."""

    if output_path.is_dir() or (not output_path.exists() and not output_path.suffix):
        # Directory mode: individual files
        output_dir = output_path
        output_dir.mkdir(parents=True, exist_ok=True)

        for i, result in enumerate(successful_results, 1):
            if result.palette is not None:
                filename = output_dir / f"palette_{i:03d}.json"
                result.palette.to_json(filename=str(filename), colorspace=colorspace)

        typer.echo(f"✓ Exported {len(successful_results)} palettes to {output_dir}")

    else:
        # File mode: combined file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create combined JSON structure
        combined_data: dict[str, object] = {
            "palettes": [],
            "total_count": len(successful_results),
            "colorspace": colorspace,
        }
        palettes_list = []

        for result in successful_results:
            if result.palette is not None:
                palette_data = result.palette.to_json(filename=None, colorspace=colorspace)
                if palette_data is not None:
                    palettes_list.append(palette_data)

        combined_data["palettes"] = palettes_list

        # Write combined file
        with open(output_path, "w") as f:
            json.dump(combined_data, f, indent=2)

        typer.echo(f"✓ Exported {len(successful_results)} palettes to {output_path}")


def display_palette_summary(successful_results: list[BatchResult], colorspace: ColorSpace) -> None:
    """Display a clean summary of extracted palettes."""
    console = Console()

    for result in successful_results:
        if result.palette is not None:
            palette = result.palette

            # Show extraction success message
            source = result.source
            if isinstance(source, str) and len(source) > 50:
                source = "..." + source[-47:]  # Truncate long paths

            console.print(f"\n✓ Extracted {palette.number_of_colors} colors from [bold]{source}[/bold]")

            # Create color table
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Hex", style="bold", width=8)

            # Add colorspace-specific column
            colorspace_label = colorspace.value.upper()
            if colorspace == ColorSpace.RGB:
                table.add_column(f"{colorspace_label}", width=15)
            else:
                table.add_column(f"{colorspace_label}", width=20)
                table.add_column("RGB", width=15)

            table.add_column("Frequency", width=8, justify="right")

            # Add color rows
            for color in palette.colors:
                hex_color = color.hex
                frequency = f"{color.freq:.1%}"

                # Get colorspace values
                color_values = color.get_colors(colorspace)

                if colorspace == ColorSpace.RGB:
                    rgb_str = f"({int(color_values[0])}, {int(color_values[1])}, {int(color_values[2])})"
                    table.add_row(f"[{hex_color}]{hex_color}[/{hex_color}]", rgb_str, frequency)
                else:
                    # For HSV/HLS, show both the colorspace values and RGB reference
                    if colorspace == ColorSpace.HSV:
                        cs_str = f"({color_values[0]:.2f}, {color_values[1]:.2f}, {color_values[2]:.2f})"
                    else:  # HLS
                        cs_str = f"({color_values[0]:.2f}, {color_values[1]:.2f}, {color_values[2]:.2f})"

                    rgb_str = f"({color.rgb[0]}, {color.rgb[1]}, {color.rgb[2]})"
                    table.add_row(f"[{hex_color}]{hex_color}[/{hex_color}]", cs_str, rgb_str, frequency)

            console.print(table)

    # Show helpful usage message
    console.print("\n[dim]Use --export-json for structured data or --no-stdout to suppress output.[/dim]")


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
