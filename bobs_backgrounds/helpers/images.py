from pathlib import Path
from typing import Optional

from dateutil.utils import today
from PIL.Image import Image as PILImage, open as open_image
from PIL.ImageDraw import Draw
from PIL.ImageFont import FreeTypeFont

from helpers import fonts
from helpers.files import archive as archive_file
from model.image import Image

CENTRE_OF_BOARD = (1070, 335)


def add_text(template: PILImage, text: str, font: Optional[FreeTypeFont] = None) -> PILImage:
    if not font:
        font = fonts.get_font()

    Draw(template).multiline_text(CENTRE_OF_BOARD, text, (255, 255, 255), font, "mm")
    return template


def archive(image: Image) -> None:
    if not image.archived_at:
        archive_file(Path(image.path))
        image.archived_at = today()


def get_template(path: str = "../resources/images/template.png") -> PILImage:
    """
    Get the template image.
    :param path: The path to the location of the template image.
    :return: The template image.
    """
    return open_image(path)


def save(image: PILImage, path: str = "../output/bobs-background.png") -> Path:
    """
    Save the image as a file.
    :param image: The image to save.
    :param path: The path to the location to save the image to.
    :return: The path to the location that the image was saved to.
    """
    path = Path(path).absolute()
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        archive_file(path)

    image.save(path)
    return path
