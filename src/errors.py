from typing import Tuple

from src.utils import SourceCodeLocation
from src.token import TokenType


def unexpected_character(character: str, source_location: SourceCodeLocation, source_code: str) -> None:
    print(f'Unexpected character "{character}" at line {source_location.line_number}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def unbalanced_parentheses(source_location: SourceCodeLocation, source_code: str) -> None:
    print(f'Unbalanced parenthesis at line {source_location.line_number}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def unbalanced_square_brackets(source_location: SourceCodeLocation, source_code: str) -> None:
    print(f'Unbalanced square brackets at line {source_location.line_number}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def unbalanced_curly_brackets(source_location: SourceCodeLocation, source_code: str) -> None:
    print(f'Unbalanced curly brackets at line {source_location.line_number}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def type_error(expected_types: Tuple[TokenType], actual_type: TokenType, operator: TokenType, source_location: SourceCodeLocation, source_code: str) -> None:
    expected_types_string = ', '.join(map(lambda t: t.name, expected_types))
    print(f'Type error: operator {operator.name} at line {source_location.line_number} supports {expected_types_string}, but got {actual_type.name}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def undefined_identifier(identifier: str, source_location: SourceCodeLocation, source_code: str) -> None:
    print(f'Undefined identifier "{identifier}" at line {source_location.line_number}')
    line = source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)

