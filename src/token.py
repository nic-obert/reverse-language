import enum

from typing import Any, List, Tuple


@enum.unique
class TokenType(enum.IntEnum):
    
    def _generate_next_value_(name: str, start: int, count: int, last_values: List[int]) -> int:
        return count
    
    # Literals
    NUMBER = enum.auto()
    STRING = enum.auto()
    BOOLEAN = enum.auto()
    ARRAY = enum.auto()
    NULL = enum.auto()

    # References
    IDENTIFIER = enum.auto()
    
    # Arithmetical operators
    PLUS = enum.auto()
    MINUS = enum.auto()
    MULTIPLY = enum.auto()
    DIVIDE = enum.auto()
    MODULO = enum.auto()
    INCREMENT = enum.auto()
    DECREMENT = enum.auto()

    # Comparison operators
    EQUAL = enum.auto()
    NOT_EQUAL = enum.auto()
    GREATER_THAN = enum.auto()
    LESS_THAN = enum.auto()
    GREATER_THAN_OR_EQUAL = enum.auto()
    LESS_THAN_OR_EQUAL = enum.auto()

    # Logical operators
    AND = enum.auto()
    OR = enum.auto()
    NOT = enum.auto()

    # Assignment operators
    ASSIGNMENT = enum.auto()
    ASSIGNMENT_ADD = enum.auto()
    ASSIGNMENT_SUB = enum.auto()
    ASSIGNMENT_MUL = enum.auto()
    ASSIGNMENT_DIV = enum.auto()
    ASSIGNMENT_MOD = enum.auto()

    # Other operators
    COMMA = enum.auto()
    PARENTHESIS = enum.auto()
    INDEX = enum.auto()
    SCOPE = enum.auto()
    SEMICOLON = enum.auto()

    # Keywords
    IF = enum.auto()
    ELSE = enum.auto()
    WHILE = enum.auto()


token_priority_table: Tuple[int] = \
(
    0,  # NUMBER
    0,  # STRING
    0,  # BOOLEAN
    0,  # ARRAY
    0,  # NULL

    0,  # IDENTIFIER

    6,  # PLUS
    6,  # MINUS
    7,  # MULTIPLY
    7,  # DIVIDE
    7,  # MODULO
    9,  # INCREMENT
    9,  # DECREMENT

    4,  # EQUAL
    4,  # NOT_EQUAL
    5,  # GREATER_THAN
    5,  # LESS_THAN
    5,  # GREATER_THAN_OR_EQUAL
    5,  # LESS_THAN_OR_EQUAL

    3,  # AND
    2,  # OR
    8,  # NOT

    1,  # ASSIGNMENT
    1,  # ASSIGNMENT_ADD
    1,  # ASSIGNMENT_SUB
    1,  # ASSIGNMENT_MUL
    1,  # ASSIGNMENT_DIV
    1,  # ASSIGNMENT_MOD

    1,  # COMMA
    9,  # PARENTHESIS
    9,  # INDEX
    0,  # SCOPE
    0,  # SEMICOLON

    0,  # IF
    0,  # ELSE
    0,  # WHILE
)

MAX_PRIORITY = token_priority_table[TokenType.PARENTHESIS]


class Token:

    def __init__(self, type: TokenType, base_priority: int, value: Any = None) -> None:
        self.type = type
        self.priority = base_priority + token_priority_table[type]
        self.value = value


    def __str__(self) -> str:
        return f'<{self.type.name}: {self.value} ({self.priority})>'

    def __repr__(self) -> str:
        return self.__str__()

