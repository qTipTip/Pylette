from enum import StrEnum

from Pylette.src.color import Color


class ColorBlindType(StrEnum):
    DEUTERANOPIA = "deuteranopia"
    PROTANOPIA = "protanopia"
    TRITANOPIA = "tritanopia"


def simulate_colorblindness(color: Color, cb_type: ColorBlindType = ColorBlindType.DEUTERANOPIA):
    lms = color.lms
