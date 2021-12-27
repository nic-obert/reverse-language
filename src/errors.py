from typing import Tuple, Union

from src.utils import SourceCodeLocation
from src.token import TokenType
from src.state import State


def unexpected_character(character: str, source_location: SourceCodeLocation) -> None:
    print(f'Unexpected character "{character}" at line {source_location.line_number}')
    line = State.source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def unbalanced_parentheses(source_location: SourceCodeLocation) -> None:
    print(f'Unbalanced parenthesis at line {source_location.line_number}')
    line = State.source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def unbalanced_square_brackets(source_location: SourceCodeLocation) -> None:
    print(f'Unbalanced square brackets at line {source_location.line_number}')
    line = State.source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def unbalanced_curly_brackets(source_location: SourceCodeLocation) -> None:
    print(f'Unbalanced curly brackets at line {source_location.line_number}')
    line = State.source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def type_error(expected_types: Tuple[TokenType], actual_type: Union[TokenType, Tuple[TokenType]], operator: TokenType, source_location: SourceCodeLocation) -> None:
    if type(actual_type) == tuple:
        actual_types_string = ' or '.join(map(lambda t: t.name, actual_type))
    else:
        actual_types_string = actual_type.name

    expected_types_string = ', '.join(map(lambda t: t.name, expected_types))
    
    print(f'Type error: operator {operator.name} at line {source_location.line_number} supports {expected_types_string}, but got {actual_types_string}')
    line = State.source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def undefined_identifier(identifier: str, source_location: SourceCodeLocation) -> None:
    print(f'Undefined identifier "{identifier}" at line {source_location.line_number}')
    line = State.source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def division_by_zero(source_location: SourceCodeLocation) -> None:
    print(f'Division by zero at line {source_location.line_number}')
    line = State.source_code[source_location.line_start:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)

