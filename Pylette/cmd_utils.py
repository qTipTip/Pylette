from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style
from rich.table import Table

from Pylette.src.palette import Palette


def create_rich_table():
    table = Table(title="Extracted Palette(s)", expand=False)
    table.add_column("Image", justify="center", style="white")
    table.add_column("Colors", justify="center", style="white")

    return table


def create_color_box(palette: Palette):
    rich_colors = []
    for color in palette:
        rich_color = RichColor.from_rgb(*color.rgb)
        rich_colors.append(rich_color)
    return ColorBox(rich_colors)


class ColorBox:
    def __init__(self, list_of_colors: list[RichColor]):
        self.colors = list_of_colors

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        for color in self.colors:
            yield Segment("▄", Style(color=color, bgcolor=color))
        yield Segment.line()

    def __rich_measure__(
        self, console: "Console", options: ConsoleOptions
    ) -> Measurement:
        return Measurement(1, options.max_width)
