import pathlib
from sys import argv

from src.utils import load_file
from src.tokenizer import tokenize_source_code
from src.syntax_tree import SyntaxTree
from src.vm import Processor
from src.state import State


def main() -> None:

    if len(argv) != 2:
        print('No source code file specified.')
        exit(1)

    file = pathlib.Path(argv[1])

    source_code = load_file(file)
    State.source_code = source_code

    tokens = tokenize_source_code(source_code)

    print(tokens, end='\n\n')

    syntax_tree = SyntaxTree()
    syntax_tree.parse_tokens(tokens)

    print(syntax_tree, end='\n\n')

    processor = Processor()
    processor.interpret(syntax_tree)


if __name__ == "__main__":
    main()

    