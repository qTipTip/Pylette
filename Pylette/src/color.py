from PIL import Image
import colorsys


class Color(object):

    def __init__(self, RGB):
        self.rgb = tuple([c for c in RGB])

    def display(self, w=50, h=50):
        """
        Displays the represented color in a w x h window.
        :param w: width in pixels
        :param h: height in pixels
        """

        img = Image.new('RGB', size=(w, h), color=self.rgb)
        img.show()

    @property
    def hsv(self):
        return colorsys.rgb_to_hsv(*self.rgb)

    @property
    def hls(self):
        return colorsys.rgb_to_hls(*self.rgb)
