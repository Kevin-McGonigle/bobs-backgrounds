import helpers.fonts as fonts
import helpers.images as images


def main() -> None:
    template = images.get_template()

    font = fonts.get_font()

    image = images.add_text(template, "", font)

    images.save(image)


if __name__ == '__main__':
    main()
