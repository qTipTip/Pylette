from typing import Literal

import numpy as np
from PIL import Image

from Pylette.src.color import Color


class Palette:
    def __init__(self, colors: list[Color]):
        """
        Initializes a color palette with a list of Color objects.

        Parameters:
            colors (list[Color]): A list of Color objects.
        """

        self.colors = colors
        self.frequencies = [c.freq for c in colors]
        self.number_of_colors = len(colors)

    def display(
        self,
        w: int = 50,
        h: int = 50,
        save_to_file: bool = False,
        filename: str = "color_palette",
        extension: str = "jpg",
    ) -> None:
        """
        Displays the color palette as an image, with an option for saving the image.

        Parameters:
            w (int): Width of each color component.
            h (int): Height of each color component.
            save_to_file (bool): Whether to save the file or not.
            filename (str): Filename.
            extension (str): File extension.
        """
        img = Image.new("RGB", size=(w * self.number_of_colors, h))
        arr = np.asarray(img).copy()
        for i in range(self.number_of_colors):
            c = self.colors[i]
            arr[:, i * h : (i + 1) * h, :] = c.rgb
        img = Image.fromarray(arr, "RGB")
        img.show()

        if save_to_file:
            img.save(f"{filename}.{extension}")

    def __getitem__(self, item: int) -> Color:
        return self.colors[item]

    def __len__(self) -> int:
        return self.number_of_colors

    def to_csv(
        self,
        filename: str | None = None,
        frequency: bool = True,
        colorspace: Literal["rgb", "hsv", "hls"] = "rgb",
        stdout: bool = True,
    ):
        """
        Dumps the palette to stdout. Saves to file if filename is specified.

        Parameters:
            filename (str | None): File to dump to.
            frequency (bool): Whether to dump the corresponding frequency of each color.
            colorspace (Literal["rgb", "hsv", "hls"]): Color space to use.
            stdout (bool): Whether to dump to stdout.
        """

        if stdout:
            for color in self.colors:
                print(",".join(map(str, color.get_colors(colorspace))))

        if filename is not None:
            with open(filename, "w") as palette_file:
                for color in self.colors:
                    palette_file.write(",".join(map(str, color.get_colors(colorspace))))
                    if frequency:
                        palette_file.write(",{}".format(color.freq))
                    palette_file.write("\n")

    def random_color(self, N, mode="frequency"):
        """
        Returns N random colors from the palette, either using the frequency of each color, or choosing uniformly.

        Parameters:
            N (int): Number of random colors to return.
            mode (str): Mode to use for selection. Can be "frequency" or "uniform".

        Returns:
            list[Color]: List of N random colors from the palette.
        """

        if mode == "frequency":
            pdf = self.frequencies
        elif mode == "uniform":
            pdf = None

        return np.random.choice(self.colors, size=N, p=pdf)

    def __str__(self):
        return "".join(["({}, {}, {}, {}) \n".format(c.rgb[0], c.rgb[1], c.rgb[2], c.freq) for c in self.colors])
