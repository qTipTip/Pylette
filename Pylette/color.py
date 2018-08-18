from PIL import Image
import colorsys


class Color(object):

    def __init__(self, RGB, frequency):
        self.rgb = tuple([c for c in RGB])
        self.freq = frequency

    def display(self, w=50, h=50):
        """
        Displays the represented color in a w x h window.
        :param w: width in pixels
        :param h: height in pixels
        """

        img = Image.new('RGB', size=(w, h), color=self.rgb)
        img.show()

    def __lt__(self, other):
        return self.freq < other.freq

    @property
    def hsv(self):
        return colorsys.rgb_to_hsv(*self.rgb)

    @property
    def hls(self):
        return colorsys.rgb_to_hls(*self.rgb)
