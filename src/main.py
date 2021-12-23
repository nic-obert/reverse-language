import pathlib
from sys import argv

from utils import load_file


def main() -> None:

    if len(argv) != 2:
        print('No source code file specified.')
        exit(1)

    file = pathlib.Path(argv[1])

    source_code = load_file(file)

    print(source_code)



if __name__ == "__main__":
    main()

    