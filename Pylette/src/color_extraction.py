from PIL import Image
import numpy as np

from Pylette.src.color import Color


def extract_colors(image, palette_size=5, resize=False):
    """
    Extracts a set of 'palette_size' colors from the given image.
    :param palette_size: number of colors to extract
    :return: a list of the extracted colors
    // https://stackoverflow.com/a/18801274
    """

    def as_void(array):
        array = np.ascontiguousarray(array)
        return array.view(np.dtype((np.void, array.dtype.itemsize * array.shape[-1])))

    # open the image
    img = Image.open(image).convert('RGB')
    if resize:
        img = img.resize((32, 32))
    arr = np.asarray(img)

    color_palette, index = np.unique(as_void(arr).ravel(), return_inverse=True)
    color_palette = color_palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    color_count = np.bincount(index)
    color_order = np.argsort(color_count)

    w, h = img.size
    color_frequency = color_count / float(w * h)

    color_palette = color_palette[color_order[::-1]]
    color_frequency = color_frequency[color_order[::-1]]

    colors = []
    for color, frequency in zip(color_palette, color_frequency)[:palette_size]:
        colors.append(Color(color, frequency))

    return colors

if __name__ == '__main__':
    palette = extract_colors('test.jpg', palette_size=10, resize=False)

    for color in palette:
        print(color.rgb, color.freq)
        color.display()