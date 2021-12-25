import pathlib
from sys import argv

from utils import load_file
from tokenizer import tokenize_source_code


def main() -> None:

    if len(argv) != 2:
        print('No source code file specified.')
        exit(1)

    file = pathlib.Path(argv[1])

    source_code = load_file(file)
    tokens = tokenize_source_code(source_code)

    print(tokens)


if __name__ == "__main__":
    main()

    