from typing import Callable, Dict, List, Tuple, Union

import errors
from token import MAX_PRIORITY, Token, TokenType
from keywords import get_keyword_type


def is_identifier(char: str) -> bool:
    return char.isalnum() or char == '_'


def is_identifier_start(char: str) -> bool:
    return char.isalpha() or char == '_'


def tokenize_source_code(source_code: str) -> List[Token]:
    base_priority = 0
    parenthesis_depth = 0
    token: Union[Token, None] = None
    tokens: List[Token] = []
    line_number = 1
    line_start = 0

    for index, character in enumerate(source_code):
        
        if token is not None:
            match token.type:
                case TokenType.NUMBER:
                    if character.isdigit():
                        token.value *= 10
                        token.value += int(character)
                        continue
                    else:
                        tokens.append(token)
                        token = None
                
                case TokenType.STRING:
                    if character == '"':
                        tokens.append(token)
                        token = None
                    else:
                        token.value += character
                        continue
                
                case TokenType.PLUS:
                    if character == '+':
                        tokens.append(Token(TokenType.INCREMENT, base_priority))
                        token = None
                        continue
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_ADD, base_priority))
                        token = None
                        continue
                
                case TokenType.MINUS:
                    if character == '-':
                        tokens.append(Token(TokenType.DECREMENT, base_priority))
                        token = None
                        continue
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_SUB, base_priority))
                        token = None
                        continue

                case TokenType.MULTIPLY:
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_MUL, base_priority))
                        token = None
                        continue

                case TokenType.DIVIDE:
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_DIV, base_priority))
                        token = None
                        continue

                case TokenType.MODULO:
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_MOD, base_priority))
                        token = None
                        continue

                case TokenType.ASSIGNMENT:
                    if character == '=':
                        tokens.append(Token(TokenType.EQUALS, base_priority))
                        token = None
                        continue

                case TokenType.NOT:
                    if character == '=':
                        tokens.append(Token(TokenType.NOT_EQUAL, base_priority))
                        token = None
                        continue

                case TokenType.AND:
                    if character == '&':
                        tokens.append(Token(TokenType.AND, base_priority))
                        token = None
                        continue
                    errors.unexpected_character(character, line_number, line_start, source_code)

                case TokenType.OR:
                    if character == '|':
                        tokens.append(Token(TokenType.OR, base_priority))
                        token = None
                        continue
                    errors.unexpected_character(character, line_number, line_start, source_code)

                case TokenType.GREATER_THAN:
                    if character == '=':
                        tokens.append(Token(TokenType.GREATER_THAN_OR_EQUAL, base_priority))
                        token = None
                        continue
                case TokenType.LESS_THAN:
                    if character == '=':
                        tokens.append(Token(TokenType.LESS_THAN_OR_EQUAL, base_priority))
                        token = None
                        continue
                
                case TokenType.IDENTIFIER:
                    if is_identifier(character):
                        token.value += character
                        continue
                    
                    word_type = get_keyword_type(token.value)
                    if word_type is not None:
                        if word_type == TokenType.BOOLEAN:
                            token.value = True if token.value == 'true' else False
                        else:
                            token = Token(word_type, base_priority)
            

            tokens.append(token)
            token = None


        if character.isdigit():
            token = Token(TokenType.NUMBER, base_priority, int(character))
            continue

        if is_identifier_start(character):
            token = Token(TokenType.IDENTIFIER, base_priority, character)
            continue
        

        match character:

            case '"':
                token = Token(TokenType.STRING, base_priority)
                continue

            case '+':
                token = Token(TokenType.PLUS, base_priority)
                continue
            case '-':
                token = Token(TokenType.MINUS, base_priority)
                continue
            case '*':
                token = Token(TokenType.MULTIPLY, base_priority)
                continue
            case '/':
                token = Token(TokenType.DIVIDE, base_priority)
                continue
            case '%':
                token = Token(TokenType.MODULO, base_priority)
                continue

            case '=':
                token = Token(TokenType.ASSIGNMENT, base_priority)
                continue
            
            case '!':
                token = Token(TokenType.NOT, base_priority)
                continue

            case '>':
                token = Token(TokenType.GREATER_THAN, base_priority)
                continue
            case '<':
                token = Token(TokenType.LESS_THAN, base_priority)
                continue
            
            case '&':
                token = Token(TokenType.AND, base_priority)
                continue
            case '|':
                token = Token(TokenType.OR, base_priority)
                continue

            case '(':
                parenthesis_depth += 1
                token = Token(TokenType.PARENTHESIS, base_priority, '(')
                base_priority += MAX_PRIORITY
                continue
            case ')':
                parenthesis_depth -= 1
                base_priority -= MAX_PRIORITY
                token = Token(TokenType.PARENTHESIS, base_priority, ')')
                continue

            case ',':
                token = Token(TokenType.COMMA, base_priority)
                continue

            case ' ':
                continue
            case '\n':
                line_number += 1
                line_start = index + 1
                continue
            case '\t':
                continue
            case '\r':
                continue
            case ';':
                tokens.append(Token(TokenType.SEMICOLON, base_priority))
                continue
        
        errors.unexpected_character(character, line_number, line_start, source_code)
    
    if token is not None:
        tokens.append(token)
    
    if parenthesis_depth != 0:
        errors.unbalanced_parenthesis(parenthesis_depth, line_number, line_start, source_code)
    
    return tokens

