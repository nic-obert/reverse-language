from typing import List, Tuple, Union

import errors
from token import Token, TokenType, get_supported_operand_types


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
        self.source_code: Union[str, None] = None

    
    def extract_binary_operands(self, index: int) -> Tuple[Token, Token]:
        operand1 = self.tokens[index - 2]
        operand2 = self.tokens[index - 1]
        # Remove the operands from the list
        self.tokens = self.tokens[:index - 2] + self.tokens[index:]
        return operand1, operand2
    

    def extract_unary_operand(self, index: int) -> Token:
        operand = self.tokens.pop(index - 1)
        return operand

    
    def check_operand_types(self, operator: Token, operands: Tuple[Token], supported_types: Tuple[TokenType]) -> None:
        for operand in operands:
            if operand.type != TokenType.IDENTIFIER and operand.type not in supported_types:
                errors.type_error(supported_types, operand.type, operator.type, operator.source_location, self.source_code)


    def parse_tokens(self, tokens: List[Token], source_code: str) -> None:

        self.tokens = tokens
        self.source_code = source_code

        while len(tokens) > 0:

            token, index = get_highest_priority_token(tokens)
            # Pass to the next statement if there is no token with higher priority
            if token.priority == 0:
                tokens = tokens[index + 1:]
                continue
            
            match token.type:

                case TokenType.PLUS:
                    operands = self.extract_binary_operands(index)
                    supported_types = get_supported_operand_types(TokenType.PLUS)
                    
                    # Check if the operand types are supported by the operator
                    self.check_operand_types(token, operands, supported_types)

                    token.children = operands
                
                case TokenType.MINUS:
                    operands = self.extract_binary_operands(index)
                    supported_types = get_supported_operand_types(TokenType.MINUS)
                    
                    # Check if the operand types are supported by the operator
                    self.check_operand_types(token, operands, supported_types)

                    token.children = operands
                
                case TokenType.MULTIPLY:
                    operands = self.extract_binary_operands(index)
                    supported_types = get_supported_operand_types(TokenType.MULTIPLY)
                    
                    # Check if the operand types are supported by the operator
                    self.check_operand_types(token, operands, supported_types)

                    token.children = operands
                
                case TokenType.DIVIDE:
                    operands = self.extract_binary_operands(index)
                    supported_types = get_supported_operand_types(TokenType.DIVIDE)
                    
                    # Check if the operand types are supported by the operator
                    self.check_operand_types(token, operands, supported_types)

                    token.children = operands
                
                
                

                
