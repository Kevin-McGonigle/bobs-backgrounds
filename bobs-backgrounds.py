from PIL.Image import Image, open as open_image


def get_template_image(custom_path: str = None) -> Image:
    path = "resources/images/template.png" if custom_path is None else custom_path
    return open_image(path)


def save_output_image(image: Image) -> None:
    pass


def main():
    image: Image = get_template_image()

    # TODO: Add text to image

    save_output_image(image)


if __name__ == '__main__':
    main()
