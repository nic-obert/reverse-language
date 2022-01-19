from typing import List, Union

import src.errors as errors
from src.utils import SourceCodeLocation
from src.token import MAX_PRIORITY, Token, TokenType
from src.keywords import get_keyword_type


def is_identifier(char: str) -> bool:
    return char.isalnum() or char == '_'


def is_identifier_start(char: str) -> bool:
    return char.isalpha() or char == '_'


def tokenize_source_code(source_code: str) -> List[Token]:
    base_priority = 0
    parenthesis_depth = 0
    square_bracket_depth = 0

    token: Union[Token, None] = None
    tokens: List[Token] = []

    # Initialize the source code location at character 0, line 1
    source_location = SourceCodeLocation(0, 1)
    
    can_be_comment = False
    is_comment = False

    for index, character in enumerate(source_code):
        
        # The last character was a '\'
        if can_be_comment:
            if character == '\\':
                can_be_comment = False
                is_comment = True
                continue
        
        # Ignore the character until the end of the line if we are inside a comment
        elif is_comment:
            # Comments last until the end of the line
            if character != '\n':
                continue
            is_comment = False
            

        if token is not None:
            match token.type:

                case TokenType.NUMBER:
                    if character.isdigit():
                        # Extend the number with the new digit
                        # Shift the whole number to the left by one digit
                        token.value *= 10
                        # Add the new digit to the right
                        token.value += int(character)
                        continue
                
                case TokenType.STRING:
                    # Continue building the string until we reach the '"" character that signifies the end of the string
                    if character != '"':
                        # Extend the string value
                        token.value += character
                        continue

                    # Here character == '"'
                    # Continue because the " character is cannot be part of any other token
                    tokens.append(token)
                    token = None
                    continue
                
                case TokenType.PLUS:
                    # Operator: ++
                    if character == '+': 
                        tokens.append(Token(TokenType.INCREMENT, base_priority, source_location))
                        token = None
                        continue
                    # Operator: +=
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_ADD, base_priority, source_location))
                        token = None
                        continue
                
                case TokenType.MINUS:
                    # Operator: --
                    if character == '-':
                        tokens.append(Token(TokenType.DECREMENT, base_priority, source_location))
                        token = None
                        continue
                    # Operator: -=
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_SUB, base_priority, source_location))
                        token = None
                        continue

                case TokenType.MULTIPLY:
                    # Operator: *=
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_MUL, base_priority, source_location))
                        token = None
                        continue

                case TokenType.DIVIDE:
                    # Operator: /=
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_DIV, base_priority, source_location))
                        token = None
                        continue

                case TokenType.MODULO:
                    # Operator: %=
                    if character == '=':
                        tokens.append(Token(TokenType.ASSIGNMENT_MOD, base_priority, source_location))
                        token = None
                        continue

                case TokenType.ASSIGNMENT:
                    # Operator: ==
                    if character == '=':
                        tokens.append(Token(TokenType.EQUAL, base_priority, source_location))
                        token = None
                        continue

                case TokenType.NOT:
                    # Operator: !=
                    if character == '=':
                        tokens.append(Token(TokenType.NOT_EQUAL, base_priority, source_location))
                        token = None
                        continue

                case TokenType.AND:
                    # Operator: &&
                    if character == '&':
                        tokens.append(Token(TokenType.AND, base_priority, source_location))
                        token = None
                        continue
                    # The language does not define '&'
                    errors.unexpected_character(character, source_location)

                case TokenType.OR:
                    # Operator: ||
                    if character == '|':
                        tokens.append(Token(TokenType.OR, base_priority, source_location))
                        token = None
                        continue
                    # The language does not define '|'
                    errors.unexpected_character(character, source_location)

                case TokenType.GREATER_THAN:
                    # Operator: >=
                    if character == '=':
                        tokens.append(Token(TokenType.GREATER_THAN_OR_EQUAL, base_priority, source_location))
                        token = None
                        continue

                case TokenType.LESS_THAN:
                    # Operator: <=
                    if character == '=':
                        tokens.append(Token(TokenType.LESS_THAN_OR_EQUAL, base_priority, source_location))
                        token = None
                        continue
                
                case TokenType.IDENTIFIER:
                    # Continue until the end of the word
                    if is_identifier(character):
                        token.value += character
                        
                        # Check if the character is the last one of the source code. 
                        # If it is, the next character does not exist
                        if index != len(source_code) - 1:
                            continue
                        # This the end of the source code, so set the next character to '' (nothing)
                        character = ''

                    # Check if the word is a keyword
                    word_type = get_keyword_type(token.value)
                    # If the word is a keyword
                    if word_type is not None:
                        if word_type == TokenType.BOOLEAN:
                            # Convert the boolean keyword to a literal boolean value
                            value = True if token.value == 'true' else False
                            token = Token(TokenType.BOOLEAN, base_priority, source_location, value)
                        else:
                            # In any other case, take the keyword as it is
                            token = Token(word_type, base_priority, source_location)
            
            # The token is finished, add it to the list of tokens
            tokens.append(token)
            token = None


        if character.isdigit():
            token = Token(TokenType.NUMBER, base_priority, source_location, int(character))
            continue

        if is_identifier_start(character):
            token = Token(TokenType.IDENTIFIER, base_priority, source_location, character)
            continue
        

        match character:

            case '"':
                token = Token(TokenType.STRING, base_priority, source_location, '')
                continue

            case '+':
                token = Token(TokenType.PLUS, base_priority, source_location)
                continue
            case '-':
                token = Token(TokenType.MINUS, base_priority, source_location)
                continue
            case '*':
                token = Token(TokenType.MULTIPLY, base_priority, source_location)
                continue
            case '/':
                token = Token(TokenType.DIVIDE, base_priority, source_location)
                continue
            case '%':
                token = Token(TokenType.MODULO, base_priority, source_location)
                continue

            case '=':
                token = Token(TokenType.ASSIGNMENT, base_priority, source_location)
                continue
            
            case '!':
                token = Token(TokenType.NOT, base_priority, source_location)
                continue

            case '>':
                token = Token(TokenType.GREATER_THAN, base_priority, source_location)
                continue
            case '<':
                token = Token(TokenType.LESS_THAN, base_priority, source_location)
                continue
            
            case '&':
                token = Token(TokenType.AND, base_priority, source_location)
                continue
            case '|':
                token = Token(TokenType.OR, base_priority, source_location)
                continue

            case '(':
                # Keep track of nested parentheses
                parenthesis_depth += 1
                token = Token(TokenType.PARENTHESIS, base_priority, source_location, '(')
                # Increase base the priority in order to evaluate first tokens enclosed in parentheses
                base_priority += MAX_PRIORITY
                continue
            case ')':
                parenthesis_depth -= 1
                base_priority -= MAX_PRIORITY
                token = Token(TokenType.PARENTHESIS, base_priority, source_location, ')')
                continue

            case '{':
                token = Token(TokenType.CURLY_BRACKET, base_priority, source_location, '{')
                continue
            case '}':
                token = Token(TokenType.CURLY_BRACKET, base_priority, source_location, '}')
                continue
        
            case '[':
                square_bracket_depth += 1
                token = Token(TokenType.SQUARE_BRACKET, base_priority, source_location, '[')
                base_priority += MAX_PRIORITY
                continue
            case ']':
                square_bracket_depth -= 1
                base_priority -= MAX_PRIORITY
                token = Token(TokenType.SQUARE_BRACKET, base_priority, source_location, ']')
                continue

            case ',':
                tokens.append(Token(TokenType.COMMA, base_priority, source_location))
                continue
            case ' ':
                continue
            case '\n':
                # Upon a newline update the source location
                source_location.line_number += 1
                source_location.line_start = index + 1
                continue
            case '\t':
                continue
            case '\r':
                continue
            case ';':
                tokens.append(Token(TokenType.SEMICOLON, base_priority, source_location))
                continue
            case '':
                continue
            case '\\':
                can_be_comment = True
                continue

        # If the character wasn't handled, raise an error
        errors.unexpected_character(character, source_location)
    
    # Eventually, append the last token to the token list, if it wasn't already appended
    if token is not None:
        tokens.append(token)
    
    # If the source code ended with an unclosed parenthesis, raise an error
    if parenthesis_depth != 0:
        errors.unbalanced_parentheses(parenthesis_depth, source_location)
    
    return tokens

