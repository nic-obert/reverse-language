from typing import Tuple
from utils import SourceCodeLocation
from token import TokenType


def unexpected_character(character: str, source_location: SourceCodeLocation, source_code: str) -> None:
    print(f'Unexpected character "{character}" at line {source_location.line_number}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def unbalanced_parenthesis(source_location: SourceCodeLocation, source_code: str) -> None:
    print(f'Unbalanced parenthesis at line {source_location.line_number}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def type_error(expected_types: Tuple[TokenType], actual_type: TokenType, operator: TokenType, source_location: SourceCodeLocation, source_code: str) -> None:
    print(f'Type error: operator {operator} at line {source_location.line_number} supports {expected_types}, but got {actual_type}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)
