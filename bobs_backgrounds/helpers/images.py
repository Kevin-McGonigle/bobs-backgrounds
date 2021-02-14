import time
from pathlib import Path
from shutil import move

from PIL.Image import Image, open as open_image
from PIL.ImageFont import FreeTypeFont


def add_text(template: Image, text: str, font: FreeTypeFont) -> Image:
    # TODO: Add text
    return template


def archive(path: Path) -> Path:
    """
    Archive the image.
    :param path: The path to the location of the image to archive.
    :return: The path to the location that the image was archived to.
    """
    archive_dir = path.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = (archive_dir / (time.strftime("%Y%m%d-%H%M%S") + path.suffix)).absolute()

    move(path.absolute(), archive_path)

    return archive_path


def get_template(path: str = "resources/images/template.png") -> Image:
    """
    Get the template image.
    :param path: The path to the location of the template image.
    :return: The template image.
    """
    return open_image(path)


def save(image: Image, path: str = "output/bobs_background.png") -> Path:
    """
    Save the image as a file.
    :param image: The image to save.
    :param path: The path to the location to save the image to.
    :return: The path to the location that the image was saved to.
    """
    path = Path(path).absolute()
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        archive(path)

    image.save(path)
    return path