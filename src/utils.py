import pathlib


class SourceCodeLocation:

    def __init__(self, line_start: int, line_number: int) -> None:
        self.line_start = line_start
        self.line_number = line_number


def load_file(path: pathlib.Path) -> str:
    """
    Loads a file from a given path.
    :param path: pathlib.Path
    :return: str
    """
    try:
        with open(path, 'r') as file:
            return file.read()

    except FileNotFoundError:
        print(f'File not found: {path}')
        exit(1)

