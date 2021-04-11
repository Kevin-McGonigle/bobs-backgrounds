from PIL.ImageFont import FreeTypeFont, truetype


def get_font(path: str = "../resources/fonts/font.ttf", size: int = 36) -> FreeTypeFont:
    """
    Get the specified font.
    :param path: The path to the location of the font's TTF file.
    :param size: The size to use for the font.
    :return: The font.
    """
    return truetype(path, size)
