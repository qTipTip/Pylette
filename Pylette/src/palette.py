import json

import numpy as np
from PIL import Image

from Pylette.src.color import Color
from Pylette.src.types import ColorSpace, ExtractionParams, ImageInfo, PaletteMetaData, ProcessingStats, SourceType


class Palette:
    def __init__(self, colors: list[Color], metadata: PaletteMetaData | None = None):
        """
        Initializes a color palette with a list of Color objects.

        Parameters:
            colors (list[Color]): A list of Color objects.
        """

        self.colors = colors
        self.frequencies = [c.freq for c in colors]
        self.number_of_colors = len(colors)
        self.metadata = metadata

    def _generate_palette_image(self, w: int = 50, h: int = 50) -> Image.Image:
        """
        Helper method to generate a palette image.

        Parameters:
            w (int): Width of each color component.
            h (int): Height of each color component.

        Returns:
            PIL.Image.Image: The generated palette image.
        """
        img = Image.new("RGB", size=(w * self.number_of_colors, h))
        arr = np.asarray(img).copy()
        for i in range(self.number_of_colors):
            c = self.colors[i]
            arr[:, i * h : (i + 1) * h, :] = c.rgb
        return Image.fromarray(arr, "RGB")

    def save(
        self,
        w: int = 50,
        h: int = 50,
        filename: str = "color_palette",
        extension: str = "jpg",
    ) -> None:
        """
        Saves the color palette as an image.

        Parameters:
            w (int): Width of each color component.
            h (int): Height of each color component.
            filename (str): Filename.
            extension (str): File extension.
        """
        img = self._generate_palette_image(w, h)
        img.save(f"{filename}.{extension}")

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
        img = self._generate_palette_image(w, h)
        img.show()

        if save_to_file:
            self.save(w, h, filename, extension)

    def __getitem__(self, item: int) -> Color:
        return self.colors[item]

    def __len__(self) -> int:
        return self.number_of_colors

    def random_color(self, N: int, mode: str = "frequency") -> list[Color]:
        """
        Returns N random colors from the palette, either using the frequency of each color, or choosing uniformly.

        Parameters:
            N (int): Number of random colors to return.
            mode (str): Mode to use for selection. Can be "frequency" or "uniform".

        Returns:
            list[Color]: List of N random colors from the palette.
        """

        if mode == "frequency":
            # Convert to numpy-compatible format for weighted selection
            colors_array = np.array(range(len(self.colors)))
            indices = np.random.choice(colors_array, size=N, p=self.frequencies)
            return [self.colors[i] for i in indices]
        elif mode == "uniform":
            # Uniform selection without weights
            colors_array = np.array(range(len(self.colors)))
            indices = np.random.choice(colors_array, size=N)
            return [self.colors[i] for i in indices]
        else:
            raise ValueError(f"Invalid mode: {mode}. Must be 'frequency' or 'uniform'.")

    def to_json(
        self,
        filename: str | None = None,
        colorspace: ColorSpace = ColorSpace.RGB,
        include_metadata: bool = True,
    ) -> dict[str, object] | None:
        """
        Exports the palette to JSON format.

        Parameters:
            filename (str | None): File to save to. If None, returns the dictionary.
            colorspace (Literal["rgb", "hsv", "hls"]): Color space to use.
            include_metadata (bool): Whether to include palette metadata.

        Returns:
            dict | None: The palette data as a dictionary if filename is None.
        """

        # Build the palette data
        palette_data: dict[str, object] = {
            "colors": [],
            "palette_size": self.number_of_colors,
            "colorspace": colorspace,
        }

        colors_list = []
        # Add color data
        for color in self.colors:
            color_values = color.get_colors(colorspace)
            color_data: dict[str, object] = {
                "frequency": float(color.freq),
            }

            # Add colorspace-specific field
            colorspace_field = colorspace.value.lower()  # "rgb", "hsv", "hls"
            if colorspace == ColorSpace.RGB:
                # RGB values should be integers
                color_data[colorspace_field] = [int(v) if isinstance(v, np.integer) else v for v in color_values]
            else:
                # HSV/HLS values should be floats
                color_data[colorspace_field] = [
                    float(v) if isinstance(v, (np.integer, np.floating)) else v for v in color_values
                ]

            # Add hex (always present, derived from RGB)
            color_data["hex"] = color.hex

            # Add RGB reference if colorspace is not RGB
            if colorspace != ColorSpace.RGB:
                color_data["rgb"] = [int(v) if isinstance(v, np.integer) else v for v in color.rgb]

            colors_list.append(color_data)

        palette_data["colors"] = colors_list

        # Add metadata if requested and available
        if include_metadata and self.metadata:
            metadata_dict: dict[str, object] = {}

            if "image_source" in self.metadata:
                metadata_dict["image_source"] = self.metadata["image_source"]
            if "source_type" in self.metadata:
                metadata_dict["source_type"] = self.metadata["source_type"]
            if "extraction_params" in self.metadata:
                metadata_dict["extraction_params"] = self.metadata["extraction_params"]
            if "image_info" in self.metadata:
                metadata_dict["image_info"] = self.metadata["image_info"]
            if "processing_stats" in self.metadata:
                metadata_dict["processing_stats"] = self.metadata["processing_stats"]

            palette_data["metadata"] = metadata_dict

        # Save to file if filename provided
        if filename is not None:
            with open(filename, "w") as f:
                json.dump(palette_data, f, indent=2)
            return None

        # Return data if no filename provided
        return palette_data

    def export(
        self,
        filename: str,
        colorspace: ColorSpace = ColorSpace.RGB,
        include_metadata: bool = True,
    ) -> None:
        """
        Export palette to JSON format.

        Parameters:
            filename (str): File to save to (extension will be added automatically if not present).
            colorspace (ColorSpace): Color space to use.
            include_metadata (bool): Whether to include metadata.
        """

        # Add .json extension if not present
        if not filename.endswith(".json"):
            filename = f"{filename}.json"

        self.to_json(filename=filename, colorspace=colorspace, include_metadata=include_metadata)

    def __str__(self):
        return "".join(["({}, {}, {}, {}) \n".format(c.rgb[0], c.rgb[1], c.rgb[2], c.freq) for c in self.colors])

    # Convenient metadata accessors
    @property
    def image_source(self) -> str | None:
        """Get the image source from metadata."""
        return self.metadata.get("image_source") if self.metadata else None

    @property
    def source_type(self) -> SourceType | None:
        """Get the source type from metadata."""
        return self.metadata.get("source_type") if self.metadata else None

    @property
    def extraction_params(self) -> ExtractionParams | None:
        """Get the extraction parameters from metadata."""
        return self.metadata.get("extraction_params") if self.metadata else None

    @property
    def image_info(self) -> ImageInfo | None:
        """Get the image information from metadata."""
        return self.metadata.get("image_info") if self.metadata else None

    @property
    def processing_stats(self) -> ProcessingStats | None:
        """Get the processing statistics from metadata."""
        return self.metadata.get("processing_stats") if self.metadata else None
