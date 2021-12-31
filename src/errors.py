from typing import Any, List, Tuple, Union

from src.utils import SourceCodeLocation
from src.token import TokenType
from src.state import State


def print_source_context(source_location: SourceCodeLocation) -> None:
    """
        Print the line of source code that the given source location is in,
        along with the 2 preceding and 2 following lines of source code, if they exist.
    """
    # Get to the beginning of the line whose number is (source_location.line_number - 2)
    lines_to_go_back = 2
    index = source_location.line_start - 1
    while index > 0 and lines_to_go_back > 0:
        index -= 1
        if State.source_code[index] == '\n':
            lines_to_go_back -= 1

    # Print up to 5 surrounding lines of source code, if they exist
    lines = State.source_code[index + 1:].split('\n', maxsplit=5)[:5]
    starting_line_number = source_location.line_number - (2 - lines_to_go_back)
    for line in lines:
        print(f'{starting_line_number}: {line}')
        starting_line_number += 1


def unexpected_character(character: str, source_location: SourceCodeLocation) -> None:
    print(f'Unexpected character "{character}" at line {source_location.line_number}')
    print_source_context(source_location)    
    exit(1)


def unbalanced_parentheses(source_location: SourceCodeLocation) -> None:
    print(f'Unbalanced parenthesis at line {source_location.line_number}')
    print_source_context(source_location)
    exit(1)


def unbalanced_square_brackets(source_location: SourceCodeLocation) -> None:
    print(f'Unbalanced square brackets at line {source_location.line_number}')
    print_source_context(source_location)
    exit(1)


def unbalanced_curly_brackets(source_location: SourceCodeLocation) -> None:
    print(f'Unbalanced curly brackets at line {source_location.line_number}')
    print_source_context(source_location)
    exit(1)


def type_error(expected_types: Tuple[TokenType], actual_type: Union[TokenType, Tuple[TokenType]], operator: TokenType, source_location: SourceCodeLocation) -> None:
    if type(actual_type) == tuple:
        actual_types_string = ' or '.join(map(lambda t: t.name, actual_type))
    else:
        actual_types_string = actual_type.name

    expected_types_string = ', '.join(map(lambda t: t.name, expected_types))
    
    print(f'Type error: operator {operator.name} at line {source_location.line_number} supports {expected_types_string}, but got {actual_types_string}')
    print_source_context(source_location)
    exit(1)


def undefined_identifier(identifier: str, source_location: SourceCodeLocation) -> None:
    print(f'Undefined identifier "{identifier}" at line {source_location.line_number}')
    print_source_context(source_location)
    exit(1)


def division_by_zero(source_location: SourceCodeLocation) -> None:
    print(f'Division by zero at line {source_location.line_number}')
    print_source_context(source_location)
    exit(1)


def expected_operand(operator: TokenType, expected_types: Tuple[TokenType], source_location: SourceCodeLocation) -> None:
    expected_types_string = ', '.join(map(lambda t: t.name, expected_types))
    print(f'Expected operand for operator {operator.name} at line {source_location.line_number} supports {expected_types_string}, but none was found')
    print_source_context(source_location)
    exit(1)


def else_without_if(source_location: SourceCodeLocation) -> None:
    print(f'Else without if at line {source_location.line_number}')
    print_source_context(source_location)
    exit(1)


def wrong_argument_count(function_name: str, expected_count: int, actual_count: int, source_location: SourceCodeLocation) -> None:
    print(f'Wrong argument count for function {function_name} at line {source_location.line_number}: expected {expected_count}, got {actual_count}')
    print_source_context(source_location)
    exit(1)


def invalid_argument(function_name: str, argument_index: int, argument_value: Any, source_location: SourceCodeLocation) -> None:
    print(f'Invalid argument {argument_index} for function {function_name} at line {source_location.line_number}: {argument_value}')
    print_source_context(source_location)
    exit(1)


def unsupported_token(token: TokenType, source_location: SourceCodeLocation) -> None:
    print(f'Unsupported token {token.name} at line {source_location.line_number}')
    print_source_context(source_location)
    exit(1)


def missing_return_statement(function_name: str, source_location: SourceCodeLocation) -> None:
    print(f'Missing return statement for function {function_name} at line {source_location.line_number}')
    print_source_context(source_location)
    exit(1)

