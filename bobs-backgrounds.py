import time
from pathlib import Path
from shutil import move
from sqlite3 import connect

from PIL.Image import Image, open as open_image
from PIL.ImageFont import truetype, FreeTypeFont

DB = connect("resources/data/db.sqlite")


def get_template_image(path: str = "resources/images/template.png") -> Image:
    """
    Get the template image.
    :param path: The path to the location of the template image.
    :return: The template image.
    """
    return open_image(path)


def get_font(path: str = "resources/fonts/font.ttf", size: int = 48) -> FreeTypeFont:
    """
    Get the font.
    :param path: The path to the location of the font's TTF file.
    :param size: The size to use for the font.
    :return:
    """
    return truetype(path, size)


def save_output_image(image: Image, path: str = "output/bobs-background.png") -> Path:
    path = Path(path).absolute()
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        archive_image(path)

    image.save(path)
    return path


def archive_image(path: Path) -> Path:
    archive_dir = path.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = (archive_dir / (time.strftime("%Y%m%d-%H%M%S") + path.suffix)).absolute()

    move(path.absolute(), archive_path)

    return archive_path


def main():
    image: Image = get_template_image()

    # TODO: Add text to image

    save_output_image(image)


if __name__ == '__main__':
    main()
