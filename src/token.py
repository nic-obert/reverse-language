import enum
import copy
from typing import Any, List, Tuple, Union

from src.utils import SourceCodeLocation


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
    SQUARE_BRACKET = enum.auto()
    CURLY_BRACKET = enum.auto()
    SEMICOLON = enum.auto()

    # Keywords
    IF = enum.auto()
    ELSE = enum.auto()
    WHILE = enum.auto()
    RETURN = enum.auto()
    BREAK = enum.auto()
    CONTINUE = enum.auto()

    # Utils
    LITERAL = enum.auto()
    ARRAY_INDEXING = enum.auto()
    FUNCTION_CALL = enum.auto()
    FUNCTION_DECLARATION = enum.auto()
    FUNCTION = enum.auto()


def is_literal_type(token_type: TokenType) -> bool:
    match token_type:
        case TokenType.NUMBER | \
            TokenType.STRING | \
            TokenType.BOOLEAN | \
            TokenType.ARRAY | \
            TokenType.NULL:
            return True
            
    return False


token_priority_table: Tuple[int] = \
(
    0,  # NUMBER
    0,  # STRING
    0,  # BOOLEAN
    0,  # ARRAY
    0,  # NULL

    0,  # IDENTIFIER

    8,  # PLUS
    8,  # MINUS
    9,  # MULTIPLY
    9,  # DIVIDE
    9,  # MODULO
    11, # INCREMENT
    11, # DECREMENT

    6,  # EQUAL
    6,  # NOT_EQUAL
    7,  # GREATER_THAN
    7,  # LESS_THAN
    7,  # GREATER_THAN_OR_EQUAL
    7,  # LESS_THAN_OR_EQUAL

    5,  # AND
    4,  # OR
    10,  # NOT

    3,  # ASSIGNMENT
    3,  # ASSIGNMENT_ADD
    3,  # ASSIGNMENT_SUB
    3,  # ASSIGNMENT_MUL
    3,  # ASSIGNMENT_DIV
    3,  # ASSIGNMENT_MOD

    0,  # COMMA
    12, # PARENTHESIS
    12, # SQUARE_BRACKET
    12, # CURLY_BRACKET
    0,  # SEMICOLON

    1,  # IF
    2,  # ELSE
    1,  # WHILE
    1,  # RETURN
    1,  # BREAK
    1,  # CONTINUE

    0,  # LITERAL
    0,  # ARRAY_INDEXING
    0,  # FUNCTION_CALL
    0,  # FUNCTION_DECLARATION
    0,  # FUNCTION

)

MAX_PRIORITY = token_priority_table[TokenType.PARENTHESIS]


expression_result_types_table: Tuple[Tuple[TokenType]] = \
(
    (TokenType.NUMBER,),        # NUMBER
    (TokenType.STRING,),        # STRING
    (TokenType.BOOLEAN,),       # BOOLEAN
    (TokenType.ARRAY,),         # ARRAY
    (TokenType.NULL,),          # NULL

    (TokenType.LITERAL,),       # IDENTIFIER

    (TokenType.NUMBER, TokenType.STRING, TokenType.ARRAY),   # PLUS
    (TokenType.NUMBER,),        # MINUS
    (TokenType.NUMBER,),        # MULTIPLY
    (TokenType.NUMBER,),        # DIVIDE
    (TokenType.NUMBER,),        # MODULO
    (TokenType.NUMBER,),        # INCREMENT
    (TokenType.NUMBER,),        # DECREMENT

    (TokenType.BOOLEAN,),       # EQUAL
    (TokenType.BOOLEAN,),       # NOT_EQUAL
    (TokenType.BOOLEAN,),       # GREATER_THAN
    (TokenType.BOOLEAN,),       # LESS_THAN
    (TokenType.BOOLEAN,),       # GREATER_THAN_OR_EQUAL
    (TokenType.BOOLEAN,),       # LESS_THAN_OR_EQUAL

    (TokenType.BOOLEAN,),       # AND
    (TokenType.BOOLEAN,),       # OR
    (TokenType.BOOLEAN,),       # NOT

    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),    # ASSIGNMENT
    (TokenType.NUMBER, TokenType.STRING, TokenType.ARRAY),    # ASSIGNMENT_ADD
    (TokenType.NUMBER,),        # ASSIGNMENT_SUB
    (TokenType.NUMBER,),        # ASSIGNMENT_MUL
    (TokenType.NUMBER,),        # ASSIGNMENT_DIV
    (TokenType.NUMBER,),        # ASSIGNMENT_MOD

    (TokenType.COMMA,),         # COMMA
    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),   # PARENTHESIS
    (TokenType.SQUARE_BRACKET,),# SQUARE_BRACKET
    (TokenType.CURLY_BRACKET,), # CURLY_BRACKET
    (TokenType.SEMICOLON,),     # SEMICOLON

    (TokenType.IF,),            # IF
    (TokenType.ELSE,),          # ELSE
    (TokenType.WHILE,),         # WHILE
    (TokenType.RETURN,),        # RETURN
    (TokenType.BREAK,),         # BREAK
    (TokenType.CONTINUE),       # CONTINUE

    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),    # LITERAL
    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),    # ARRAY_INDEXING
    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),    # FUNCTION_CALL
    (TokenType.FUNCTION_DECLARATION,),  # FUNCTION_DECLARATION
    (TokenType.FUNCTION),               # FUNCTION

)

def get_expression_result_types(token_type: TokenType) -> Union[Tuple[TokenType], None]:
    return expression_result_types_table[token_type]


supported_operand_types_table: Tuple[Union[
    Tuple[TokenType],
    None
]] = \
(
    None,  # NUMBER
    None,  # STRING
    None,  # BOOLEAN
    None,  # ARRAY
    None,  # NULL

    None,  # IDENTIFIER

    (TokenType.NUMBER, TokenType.STRING, TokenType.ARRAY),  # PLUS
    (TokenType.NUMBER,),  # MINUS
    (TokenType.NUMBER,),  # MULTIPLY
    (TokenType.NUMBER,),  # DIVIDE
    (TokenType.NUMBER,),  # MODULO
    (TokenType.NUMBER,),  # INCREMENT
    (TokenType.NUMBER,),  # DECREMENT

    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),  # EQUAL
    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),  # NOT_EQUAL
    (TokenType.NUMBER,),  # GREATER_THAN
    (TokenType.NUMBER,),  # LESS_THAN
    (TokenType.NUMBER,),  # GREATER_THAN_OR_EQUAL
    (TokenType.NUMBER,),  # LESS_THAN_OR_EQUAL

    (TokenType.BOOLEAN,),  # AND
    (TokenType.BOOLEAN,),  # OR
    (TokenType.BOOLEAN,),  # NOT

    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),  # ASSIGNMENT
    (TokenType.NUMBER, TokenType.STRING, TokenType.ARRAY),  # ASSIGNMENT_ADD
    (TokenType.NUMBER,),  # ASSIGNMENT_SUB
    (TokenType.NUMBER,),  # ASSIGNMENT_MUL
    (TokenType.NUMBER,),  # ASSIGNMENT_DIV
    (TokenType.NUMBER,),  # ASSIGNMENT_MOD

    None,  # COMMA
    None,  # PARENTHESIS
    None,  # SQUARE_BRACKET
    None,  # CURLY_BRACKET
    None,  # SEMICOLON

    None,  # IF
    None,  # ELSE
    None,  # WHILE
    (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),  # RETURN
    None,  # BREAK
    None,  # CONTINUE

    None,  # LITERAL
    None,  # ARRAY_INDEXING
    None,  # FUNCTION_CALL
    None,  # FUNCTION_DECLARATION
    None,  # FUNCTION

)


def get_supported_operand_types(token_type: TokenType) -> Tuple[TokenType]:
    return supported_operand_types_table[token_type]


class Token:

    def __init__(self, type: TokenType, base_priority: int, source_location: SourceCodeLocation, value: Any = None) -> None:
        self.type = type
        
        type_priority = token_priority_table[type]
        self.priority = 0 if type_priority == 0 else base_priority + type_priority
        
        self.value = value
        self.source_location = copy.copy(source_location)
        self.children: List[Token] = []


    def __str__(self) -> str:
        match self.type:

            case TokenType.FUNCTION_DECLARATION:
                # value = [body: Token, parameters: List[Token], name: Token]
                name: str = self.value[2].value
                parameter_tokens: List[Token] = self.value[1]
                parameter_names = ', '.join([parameter_token.value for parameter_token in parameter_tokens])
                return f'<{TokenType.FUNCTION_DECLARATION.name}: {name} ({parameter_names})>'

            case TokenType.FUNCTION_CALL:
                # value = [arguments: List[Token], name: Token]
                name: str = self.value[1].value
                argument_tokens: List[Token] = self.value[0]
                argument_values = ', '.join([str(argument_token.value) for argument_token in argument_tokens])
                return f'<{TokenType.FUNCTION_CALL.name}: {name} ({argument_values})>'

        return f'<{self.type.name}: {self.value} ({self.priority})>'

    def __repr__(self) -> str:
        return self.__str__()

