from PIL import Image


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
        pass

    @property
    def HSL(self):
        pass


if __name__ == '__main__':

    C = Color(35, 12, 255)
    C.display()