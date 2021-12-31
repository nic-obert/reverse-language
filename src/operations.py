import random
import time
from typing import Any, Callable, Dict, List, Tuple, Union

import src.errors as errors
from src.token import Token, TokenType, get_supported_operand_types
from src.utils import SourceCodeLocation


def add(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.NUMBER, TokenType.NUMBER):
            return value1 + value2

        case (TokenType.STRING, TokenType.STRING):
            return value1 + value2

        case (TokenType.ARRAY, TokenType.ARRAY):
            return value1 + value2

    errors.type_error(
        get_supported_operand_types(TokenType.PLUS),
        (type1, type2),
        TokenType.PLUS,
        operator.source_location
    )


def subtract(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.NUMBER, TokenType.NUMBER):
            return value1 - value2

    errors.type_error(
        get_supported_operand_types(TokenType.MINUS),
        (type1, type2),
        TokenType.MINUS,
        operator.source_location
    )


def multiply(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.NUMBER, TokenType.NUMBER):
            return value1 * value2

    errors.type_error(
        get_supported_operand_types(TokenType.MULTIPLY),
        (type1, type2),
        TokenType.MULTIPLY,
        operator.source_location
    )


def divide(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.NUMBER, TokenType.NUMBER):
            if value2 == 0:
                errors.division_by_zero_error(operator.source_location)
            return value1 / value2

    errors.type_error(
        get_supported_operand_types(TokenType.DIVIDE),
        (type1, type2),
        TokenType.DIVIDE,
        operator.source_location
    )


def modulo(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.NUMBER, TokenType.NUMBER):
            if value2 == 0:
                errors.division_by_zero_error(operator.source_location)
            return value1 % value2

    errors.type_error(
        get_supported_operand_types(TokenType.MODULO),
        (type1, type2),
        TokenType.MODULO,
        operator.source_location
    )


def increment(value: Any, type: TokenType, operator: Token) -> Any:
    match (type):

        case (TokenType.NUMBER):
            return value + 1

    errors.type_error(
        get_supported_operand_types(TokenType.INCREMENT),
        (type,),
        TokenType.INCREMENT,
        operator.source_location
    )


def decrement(value: Any, type: TokenType, operator: Token) -> Any:
    match (type):

        case (TokenType.NUMBER):
            return value - 1

    errors.type_error(
        get_supported_operand_types(TokenType.DECREMENT),
        (type,),
        TokenType.DECREMENT,
        operator.source_location
    )


def equal(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.NUMBER, TokenType.NUMBER):
            return value1 == value2

        case (TokenType.STRING, TokenType.STRING):
            return value1 == value2

        case (TokenType.ARRAY, TokenType.ARRAY):
            # Two array are equal if they have the same length and all elements are equal
            if len(value1) != len(value2):
                return False
            for elem1, elem2 in zip(value1, value2):
                if not equal(elem1, elem2):
                    return False
            return True

        case (TokenType.BOOLEAN, TokenType.BOOLEAN):
            return value1 == value2

    return False


def not_equal(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    return not equal(value1, type1, value2, type2, operator)


def greater_than(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.NUMBER, TokenType.NUMBER):
            return value1 > value2

    errors.type_error(
        get_supported_operand_types(TokenType.GREATER_THAN),
        (type1, type2),
        TokenType.GREATER_THAN,
        operator.source_location
    )


def greater_than_or_equal(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.NUMBER, TokenType.NUMBER):
            return value1 >= value2

    errors.type_error(
        get_supported_operand_types(TokenType.GREATER_THAN_OR_EQUAL),
        (type1, type2),
        TokenType.GREATER_THAN_OR_EQUAL,
        operator.source_location
    )


def less_than(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    return not greater_than_or_equal(value1, type1, value2, type2, operator)


def less_than_or_equal(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    return not greater_than(value1, type1, value2, type2, operator)


def and_(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.BOOLEAN, TokenType.BOOLEAN):
            return value1 and value2

    errors.type_error(
        get_supported_operand_types(TokenType.AND),
        (type1, type2),
        TokenType.AND,
        operator.source_location
    )


def or_(value1: Any, type1: TokenType, value2: Any, type2: TokenType, operator: Token) -> Any:
    match (type1, type2):

        case (TokenType.BOOLEAN, TokenType.BOOLEAN):
            return value1 or value2

    errors.type_error(
        get_supported_operand_types(TokenType.OR),
        (type1, type2),
        TokenType.OR,
        operator.source_location
    )


def not_(value: Any, type: TokenType, operator: Token) -> Any:
    match (type):

        case (TokenType.BOOLEAN):
            return not value

    errors.type_error(
        get_supported_operand_types(TokenType.NOT),
        (type,),
        TokenType.NOT,
        operator.source_location
    )


def array_index(array: List[Any], array_type: TokenType, index: int, index_type: TokenType, operator: Token) -> Any:
    match (array_type, index_type):

        case (TokenType.ARRAY, TokenType.NUMBER):
            index -= 2
            if index < 0 or index >= len(array):
                errors.array_index_out_of_bounds(len(array), index + 2, operator.source_location)
            return array[index]

    errors.type_error(
        get_supported_operand_types(TokenType.ARRAY_INDEX),
        (array_type, index_type),
        TokenType.ARRAY_INDEX,
        operator.source_location
    )


class BuiltinFunction:

    def __init__(self,
                name: str,
                handler: Callable[[List[Token], Token], Token],
                supported_argument_types: Tuple[Tuple[TokenType]],
            ) -> None:
        self.name = name
        self.handler = handler
        self.supported_argument_types = supported_argument_types


    def check_argument_count(self, arguments: List[Token], source_location: SourceCodeLocation) -> None:
        if len(arguments) != len(self.supported_argument_types):
            errors.argument_count_error(self.name, len(self.supported_argument_types), len(arguments), source_location)

    
    def call(self, arguments: List[Token], caller: Token) -> Token:
        self.check_argument_count(arguments, caller.source_location)

        for index, argument in enumerate(arguments):
            if argument.type not in self.supported_argument_types[index]:
                errors.type_error(self.supported_argument_types[index], argument.type, caller.type, caller.source_location)
      
        return self.handler(arguments, caller)


def handle_print(arguments: List[Token], caller: Token) -> Token:
    argument = arguments[0]

    match argument.type:
        case TokenType.ARRAY:
            # Recursively print all elements of the array
            print('[', end='')
            for index, elem in enumerate(argument.value):
                handle_print([elem], caller)
                if index != len(argument.value) - 1:
                    print(', ', end='')
            print(']', end='')
        
        case TokenType.NULL:
            print('null', end='') 

        case _:
            print(arguments[0].value, end="")

    # Build the return token value
    return Token(TokenType.NULL, 0, caller.source_location)


def handle_println(arguments: List[Token], caller: Token) -> Token:
    return_token = handle_print(arguments, caller)
    print()
    return return_token


def handle_toNumber(arguments: List[Token], caller: Token) -> Token:
    try:
        return Token(TokenType.NUMBER, 0, caller.source_location, float(arguments[0].value))
    except ValueError:
        errors.invalid_argument('toNumber', 0, arguments[0].value, caller.source_location)


def handle_toString(arguments: List[Token], caller: Token) -> Token:
    argument = arguments[0]
    match argument.type:
        case TokenType.STRING:
            return argument
        
        case TokenType.NULL:
            return Token(TokenType.STRING, 0, caller.source_location, "null")
        
        case TokenType.BOOLEAN:
            return Token(TokenType.STRING, 0, caller.source_location, "true" if argument.value else "false")
        
        case TokenType.ARRAY:
            string = '['
            for element in argument.value:
                # element is a Token
                string += handle_toString([element], caller).value + ', '
            # Remove the trailing ", " from the string, if any
            if len(argument.value) > 0:
                string = string[:-2]
            string += ']'
            return Token(TokenType.STRING, 0, caller.source_location, string)
            
    return Token(TokenType.STRING, 0, caller.source_location, str(arguments[0].value))


def handle_toBoolean(arguments: List[Token], caller: Token) -> Token:
    argument = arguments[0]
    if argument.type == TokenType.BOOLEAN:
        return argument
    # argument.type == TokenType.NUMBER:
    # Remember that 0 is true and everything else is false
    return Token(TokenType.BOOLEAN, 0, caller.source_location, argument.value == 0)


def handle_getInput(arguments: List[Token], caller: Token) -> Token:
    return Token(TokenType.STRING, 0, caller.source_location, input())


def handle_getRandom(arguments: List[Token], caller: Token) -> Token:
    return Token(TokenType.NUMBER, 0, caller.source_location, random.random())


def handle_exit(arguments: List[Token], caller: Token) -> Token:
    code = arguments[0].value
    exit(code)
    # Return nothing, exiting the program


def handle_getLength(arguments: List[Token], caller: Token) -> Token:
    return Token(TokenType.NUMBER, 0, caller.source_location, len(arguments[0].value))


def handle_sleep(arguments: List[Token], caller: Token) -> Token:
    time.sleep(arguments[0].value)
    return Token(TokenType.NULL, 0, caller.source_location)


def handle_getTime(arguments: List[Token], caller: Token) -> Token:
    return Token(TokenType.NUMBER, 0, caller.source_location, time.time())


"""
    Table of builtin functions
    Format: name: BuiltinFunction(name, handler, supported_argument_types)
"""
builtin_function_handlers_table: Dict[str, BuiltinFunction] = \
{
    'print': BuiltinFunction('print', handle_print, ((TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),)),
    'println': BuiltinFunction('println', handle_println, ((TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),)),
    'toNumber': BuiltinFunction('toNumber', handle_toNumber, ((TokenType.NUMBER, TokenType.STRING,),)),
    'toString': BuiltinFunction('toString', handle_toString, ((TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.ARRAY, TokenType.NULL),)),
    'toBoolean': BuiltinFunction('toBoolean', handle_toBoolean, ((TokenType.NUMBER, TokenType.BOOLEAN),)),
    'getInput': BuiltinFunction('getInput', handle_getInput, ()),
    'getRandom': BuiltinFunction('getRandom', handle_getRandom, ()),
    'exit': BuiltinFunction('exit', handle_exit, ((TokenType.NUMBER,),)),
    'getLength': BuiltinFunction('getLength', handle_getLength, ((TokenType.STRING, TokenType.ARRAY),)),
    'sleep': BuiltinFunction('sleep', handle_sleep, ((TokenType.NUMBER,),)),
    'getTime': BuiltinFunction('getTime', handle_getTime, ()),
}


def get_builtin_handler(function_name: str) -> Union[BuiltinFunction, None]:
    return builtin_function_handlers_table.get(function_name)

