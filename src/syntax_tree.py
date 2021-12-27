import enum
from typing import List, Tuple, Union

import src.errors as errors
from src.token import Token, TokenType, get_supported_operand_types, get_expression_result_types


@enum.unique
class Side(enum.IntEnum):
    LEFT = 0
    RIGHT = 1


def get_highest_priority_token(tokens: List[Token]) -> Tuple[Token, int]:
    highest_priority_token = tokens[0]
    highest_priority_index = 0

    for index, token in enumerate(tokens):

        if token.type == TokenType.SEMICOLON:
            break

        if token.priority > highest_priority_token.priority:
            highest_priority_token = token
            highest_priority_index = index
    
    return highest_priority_token, highest_priority_index


class SyntaxTree:

    def __init__(self) -> None:
        self.statements: List[Token] = []
        self.tokens: Union[List[Token], None] = None

    
    def extract_binary_operands(self, index: int) -> Tuple[Token, Token]:
        operand1 = self.tokens[index - 2]
        operand2 = self.tokens[index - 1]
        # Remove the operands from the list
        self.tokens = self.tokens[:index - 2] + self.tokens[index:]
        return operand1, operand2
    

    def extract_unary_operand(self, index: int, side: Side) -> Token:
        if side == Side.LEFT:
            operand = self.tokens.pop(index - 1)
        else:
            operand = self.tokens.pop(index + 1)
        return operand

    
    def check_operand_types(self, operator: Token, operands: Tuple[Token], supported_types: Tuple[TokenType]) -> None:
        for operand in operands:
            if operand.type != TokenType.IDENTIFIER and operand.type not in supported_types:
                errors.type_error(supported_types, operand.type, operator.type, operator.source_location)


    def parse_tokens(self, _tokens: List[Token]) -> None:

        self.tokens = _tokens

        del _tokens

        while len(self.tokens) > 0:

            token, index = get_highest_priority_token(self.tokens)
            # Pass to the next statement if there is no token with higher priority
            if token.priority == 0:
                # Append the root token to the list of statements
                if token.type != TokenType.SEMICOLON:
                    self.statements.append(token)
                self.tokens = self.tokens[index + 1:]
                continue
            
            # Set priority to 0 so that the token is not processed again
            token.priority = 0
            
            match token.type:

                case TokenType.PLUS | \
                    TokenType.MINUS | \
                    TokenType.MULTIPLY | \
                    TokenType.DIVIDE | \
                    TokenType.MODULO | \
                    TokenType.EQUAL | \
                    TokenType.NOT_EQUAL | \
                    TokenType.GREATER_THAN | \
                    TokenType.LESS_THAN | \
                    TokenType.GREATER_THAN_OR_EQUAL | \
                    TokenType.LESS_THAN_OR_EQUAL | \
                    TokenType.AND | \
                    TokenType.OR:

                    operands = self.extract_binary_operands(index)
                    supported_types = get_supported_operand_types(token.type)
                    
                    # Check if the operand types are supported by the operator
                    self.check_operand_types(token, operands, supported_types)

                    token.children = operands
                
                
                case TokenType.INCREMENT | \
                    TokenType.DECREMENT:

                    operand = self.extract_unary_operand(index, Side.LEFT)
                    self.check_operand_types(token, (operand,), (TokenType.IDENTIFIER,))
                    token.children = (operand,)


                case TokenType.ASSIGNMENT | \
                    TokenType.ASSIGNMENT_ADD | \
                    TokenType.ASSIGNMENT_SUB | \
                    TokenType.ASSIGNMENT_MUL | \
                    TokenType.ASSIGNMENT_DIV | \
                    TokenType.ASSIGNMENT_MOD:

                    identifier = self.extract_unary_operand(index, Side.RIGHT)
                    value = self.extract_unary_operand(index, Side.LEFT)

                    value_supported_types = get_supported_operand_types(token.type)
                    self.check_operand_types(token, (value,), value_supported_types)
                    self.check_operand_types(token, (identifier,), (TokenType.IDENTIFIER,))

                    token.children = (value, identifier)
                
                
                case TokenType.PARENTHESIS:
                    if token.value == ')':
                        errors.unbalanced_parentheses(token.source_location)
                    
                    children = []

                    # Find the matching parenthesis in the statement and extract the children
                    depth = 1
                    i = index + 1
                    while True:
                        tok = self.tokens[index]

                        if tok.value == '(':
                            depth -= 1
                            if depth == 0:
                                break

                        elif tok.value == ')':
                            depth += 1

                        elif tok.type == TokenType.SEMICOLON:
                            errors.unbalanced_parentheses(tok.source_location)
                        
                        elif tok.type != TokenType.COMMA:
                            children.append(tok)
                        
                        i += 1
                    
                    if len(children) > 0:
                        self.tokens = self.tokens[: index + 1] + self.tokens[i + 1 :]
                    token.children = tuple(children)


                case TokenType.SQUARE_BRACKET:
                    if token.value == ']':
                        errors.unbalanced_square_brackets(token.source_location)

                    children = []

                    # Find the matching bracket in the statement and extract the children
                    depth = 1
                    i = index + 1
                    while True:
                        tok = self.tokens[index]

                        if tok.value == '[':
                            depth -= 1
                            if depth == 0:
                                break

                        elif tok.value == ']':
                            depth += 1

                        elif tok.type == TokenType.SEMICOLON:
                            errors.unbalanced_square_brackets(tok.source_location)
                        
                        elif tok.type != TokenType.COMMA:
                            children.append(tok)
                        
                        i += 1

                    if len(children) > 0:
                        self.tokens = self.tokens[: index + 1] + self.tokens[i + 1 :]
                    # Convert the children to a tuple for performance
                    token.children = tuple(children)

                
                case TokenType.CURLY_BRACKET:
                    if token.value == '}':
                        errors.unbalanced_curly_brackets(token.source_location)

                    children = []

                    # Find the matching bracket
                    depth = 1
                    i = index + 1
                    while True:
                        tok = self.tokens[index]

                        if tok.value == '{':
                            depth -= 1
                            if depth == 0:
                                break

                        elif tok.value == '}':
                            depth += 1
   
                        elif tok.type != TokenType.COMMA:
                            children.append(tok)
                        
                        i += 1

                    if len(children) > 0:
                        self.tokens = self.tokens[: index + 1] + self.tokens[i + 1 :]
                    # Keep the children property a list, since it will have to be modified later
                    token.children = children


                case TokenType.IF | \
                    TokenType.WHILE:

                    body, condition = self.extract_binary_operands(index)
                    self.check_operand_types(token, (body), (TokenType.CURLY_BRACKET,))
                    
                    if get_expression_result_types(condition) != (TokenType.BOOLEAN,):
                        errors.type_error((TokenType.BOOLEAN,), get_expression_result_types(condition), token.type, token.source_location)

                    # Parse the code inside the curly brackets
                    content_tree = SyntaxTree()
                    content_tree.parse_tokens(body.children)
                    body.children = content_tree.statements

                    token.children = (body, condition)


                case TokenType.ELSE:
                    body = self.extract_unary_operand(index, Side.LEFT)
                    self.check_operand_types(token, (body,), (TokenType.CURLY_BRACKET,))
                    
                    # Parse the code inside the curly brackets
                    content_tree = SyntaxTree()
                    content_tree.parse_tokens(body.children)
                    body.children = content_tree.statements

                    token.children = (body,)


    def stringify_token(self, token: Token, depth: int) -> str:
        """
        Recursively convert a token into a pretty formetted string.
        """
        indent = f'{"  " * depth}-> '
        string = f'{indent}<{token.type.name}: {token.value}>\n'
        for child in token.children:
            string += f'{self.stringify_token(child, depth + 1)}'
        return string


    def __str__(self) -> str:
        string = f'<SyntaxTree>\n'
        for token in self.statements:
            string += self.stringify_token(token, 0)
        return string

    def __repr__(self) -> str:
        return self.__str__()
    
