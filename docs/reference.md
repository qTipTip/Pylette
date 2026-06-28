# Reference

Here you can find the reference for the user facing API of Pylette. This consists of
the `extract_colors` function, which is used to extract a color palette from an image,
and the `Palette` and `Color` classes, which are used to work with the extracted color palette.

## Key Features

- **JSON Export**: Export palettes to structured JSON format with metadata
- **Hex Colors**: Access hex color codes through the `Color.hex` property
- **Semantic Fields**: Export uses semantic field names (rgb, hsv, hls) instead of generic values
- **Metadata**: Rich metadata including extraction parameters, timing, and image info
- **Batch Processing**: Process multiple images with parallel execution support


::: pylette.extract_colors

::: pylette.batch_extract_colors

::: pylette.Palette

::: pylette.Color


## Exceptions

Every error Pylette raises derives from `PyletteError`, so you can catch any
Pylette-originated failure with a single `except pylette.PyletteError` and branch
on the concrete subclass to identify the failure mode. Each subclass also derives
from `ValueError`, so existing `except ValueError` handlers keep working.

::: pylette.PyletteError
::: pylette.InvalidImageError
::: pylette.NoValidPixelsError
::: pylette.UnknownExtractionMethodError
::: pylette.InvalidColorspaceError


## Core Types:

::: pylette.types.ArrayImage
::: pylette.types.ArrayLike
::: pylette.types.BatchResult
::: pylette.types.BytesImage
::: pylette.types.ColorArray
::: pylette.types.ColorSpace
::: pylette.types.ColorTuple
::: pylette.types.CV2Image
::: pylette.types.ExtractionMethod
::: pylette.types.ExtractionParams
::: pylette.types.FloatArray
::: pylette.types.ImageInfo
::: pylette.types.ImageInput
::: pylette.types.ImageLike
::: pylette.types.IntArray
::: pylette.types.PaletteMetaData
::: pylette.types.PathLikeImage
::: pylette.types.PILImage
::: pylette.types.ProcessingStats
::: pylette.types.RGBATuple
::: pylette.types.RGBTuple
::: pylette.types.SourceType
::: pylette.types.URLImage
