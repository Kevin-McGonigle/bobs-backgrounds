import helpers.images as images
from model import with_session


@with_session
def main() -> None:
    image = images.add_text(images.get_template(), "This is a test.")

    images.save(image)


if __name__ == '__main__':
    main()
