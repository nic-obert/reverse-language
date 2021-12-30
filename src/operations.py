from typing import Any

import src.errors as errors
from src.token import Token, TokenType, get_supported_operand_types


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

