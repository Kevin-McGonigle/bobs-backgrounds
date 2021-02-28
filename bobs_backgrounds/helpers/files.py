import time
from pathlib import Path
from shutil import move


def archive(path: str) -> Path:
    """
    Archive the image.
    :param path: The path to the location of the image to archive.
    :return: The path to the location that the image was archived to.
    """
    path = Path(path).absolute()
    archive_dir = path.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = (archive_dir / (time.strftime("%Y%m%d-%H%M%S") + path.suffix)).absolute()

    move(path.absolute(), archive_path)

    return archive_path
