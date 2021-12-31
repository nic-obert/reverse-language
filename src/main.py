import pathlib
from sys import argv

from src.utils import load_file
from src.tokenizer import tokenize_source_code
from src.syntax_tree import SyntaxTree
from src.vm import Processor
from src.state import State


def main() -> None:

    if len(argv) < 2:
        print('No source code file specified.')
        exit(1)

    file = pathlib.Path(argv[1])

    if '-v' in argv:
        State.verbose = True

    source_code = load_file(file)
    State.source_code = source_code

    tokens = tokenize_source_code(source_code)

    if State.verbose:
        print(tokens, end='\n\n')

    syntax_tree = SyntaxTree()
    syntax_tree.parse_tokens(tokens)

    if State.verbose:
        print(syntax_tree, end='\n\n')

    processor = Processor()
    processor.interpret_tree(syntax_tree)


if __name__ == "__main__":
    main()

    