import pathlib
from sys import argv

from src.utils import load_file
from src.tokenizer import tokenize_source_code
from src.syntax_tree import SyntaxTree


def main() -> None:

    if len(argv) != 2:
        print('No source code file specified.')
        exit(1)

    file = pathlib.Path(argv[1])

    source_code = load_file(file)
    tokens = tokenize_source_code(source_code)

    print(tokens)

    syntax_tree = SyntaxTree()
    syntax_tree.parse_tokens(tokens, source_code)

    print(syntax_tree)


if __name__ == "__main__":
    main()

    