
from collections import deque
from rich.console import Console, RenderableType
from rich.progress import BarColumn, Progress, ProgressColumn, Task, TaskID, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from Pylette.src.color import Color


class RecentlyCompletedColumn(ProgressColumn):
    def __init__(self, num_items: int = 5, max_text_width: int = 20, max_num_preview_colors: int = 6) -> None:
        self.max_items = num_items
        self.max_name_width = max_text_width
        self.items = deque(maxlen=self.max_items)
        self.num_preview_colors = max_num_preview_colors

        super().__init__()

    def add_completed_task(self, task_number: int, task_name: str, colors: list[Color]) -> None:
        # Truncate name if too long
        display_name = task_name
        if len(display_name) > self.max_name_width:
            display_name = task_name[:-3] + "..."

        self.items.append(
            {
                "number": task_number,
                "name": display_name,
                "colors": colors[: self.num_preview_colors],
            }
        )

    def render(self, task: Task) -> RenderableType:
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="left", width=self.max_name_width)  # Task name
        table.add_column(justify="left")  # Palette dots

        # Add each recent task as a row (most recent first)
        for task_info in reversed(list(self.items)):
            task_name = task_info["name"]
            colors = task_info["colors"]

            # Create colored dots for palette
            dots_text = Text()
            for c in colors:
                r, g, b = c.rgb
                color = f"rgb({r},{g},{b})"
                dots_text.append("●", style=color)

            table.add_row(task_name, dots_text)

        return table


def pylette_progress_bar(palette_size: int, max_recent_items: int = 5) -> Progress:
        return Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
            RecentlyCompletedColumn(num_items=max_recent_items, max_text_width=20, max_num_preview_colors=palette_size)
        )


class PyletteProgress(Progress):
    """Custom Progress class for Pylette color extraction with palette preview"""
    
    def __init__(
        self,
        palette_size: int = 5,
        max_recent_items: int = 5,
        max_name_width: int = 20,
        console_width: int = 140,
        *args,
        **kwargs
    ):
        # Create the recently completed column
        self.recently_completed = RecentlyCompletedColumn(
            num_items=max_recent_items,
            max_text_width=max_name_width,
            max_num_preview_colors=palette_size
        )
        
        # Set up the console with appropriate width
        console = Console(width=console_width)
        
        # Initialize Progress with custom columns
        super().__init__(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=25),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
            self.recently_completed,
            console=console,
            *args,
            **kwargs
        )
    
    
    
    def add_completed_item(self, task_number: int, task_name: str, colors: list[Color]) -> None:
        """Add a completed item to the recent completions display"""
        self.recently_completed.add_completed_task(task_number, task_name, colors)
    
    def mark_task_complete(
        self, 
        task_id: TaskID, 
        task_number: int,
        completed_task_name: str, 
        palette_colors: list[Color]
    ) -> None:
        
        self.update(task_id, advance=1)
        
        # Add to recent completions
        self.add_completed_item(task_number=task_number, task_name=completed_task_name, colors=palette_colors)
