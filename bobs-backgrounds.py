from pathlib import Path

from PIL.Image import Image, open as open_image
from PIL.ImageFont import truetype, FreeTypeFont


def get_template_image(custom_path: str = None) -> Image:
    path = "resources/images/template.png" if not custom_path else custom_path
    return open_image(path)


def get_font(size: int = 48, custom_path: str = None) -> FreeTypeFont:
    path = "resources/fonts/font.ttf" if not custom_path else custom_path
    return truetype(path, size)


def save_output_image(image: Image, custom_path: str = None) -> str:
    path = "output/bobs-background.png" if not custom_path else custom_path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    return path


def main():
    image: Image = get_template_image()
    font: FreeTypeFont = get_font()

    # TODO: Add text to image

    save_output_image(image)


if __name__ == '__main__':
    main()
