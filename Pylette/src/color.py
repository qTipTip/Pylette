from PIL import Image
import colorsys


class Color(object):

    def __init__(self, R, G, B):
        self.RGB = (R, G, B)

    def display(self, w=50, h=50):
        """
        Displays the represented color in a w x h window.
        :param w: width in pixels
        :param h: height in pixels
        """

        img = Image.new('RGB', size=(w, h), color=self.RGB)
        img.show()

    @property
    def HSV(self):
        return colorsys.rgb_to_hsv(*self.RGB)

    @property
    def HLS(self):
        return colorsys.rgb_to_hls(*self.RGB)
