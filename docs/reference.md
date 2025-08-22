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


::: Pylette.extract_colors

::: Pylette.batch_extract_colors

::: Pylette.Palette

::: Pylette.Color

::: Pylette.ImageInput
