import enum
from typing import List, Tuple, Union

import src.errors as errors
from src.token import Token, TokenType, get_supported_operand_types, get_expression_result_types, is_literal_type


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

    
    def extract_binary_operands(self, index: int) -> List[Union[Token, None]]:
        """
        Extract the first and second operand from the left of a binary operator.
        Returns a list of operands, where None is used to indicate that the
        operand is not present (the error will be handled by check_operand_types()).
        """
        op1_index = index - 2
        if op1_index >= 0:
            operand1 = self.tokens[op1_index]
            # If (index - 2) is valid, (index - 1) is also valid.
            operand2 = self.tokens[index - 1]

            # Remove the operands from the list only if there was no error.
            # In case of errors, the program will terminate anyways.
            self.tokens = self.tokens[:index - 2] + self.tokens[index:]
            return [operand1, operand2]

        else:
            return [None, None]
    

    def extract_unary_operand(self, index: int, side: Side) -> Union[Token, None]:
            if side == Side.LEFT:
                operand_index = index - 1
                if operand_index >= 0:
                    return self.tokens.pop(operand_index)
                return None

            # if side == Side.RIGHT:
            operand_index = index + 1
            if operand_index < len(self.tokens):
                return self.tokens.pop(operand_index)
            return None

    
    def check_operand_types(self, operator: Token, operands: Tuple[Token], supported_types: Tuple[TokenType]) -> None:
        """
        Check if the operands are of the correct type.
        """
        for operand in operands:

            if operand is None:
                errors.expected_operand(operator.type, supported_types, operator.source_location)

            # Cannot check the type of an identifier since it is not yet defined.
            if operand.type == TokenType.IDENTIFIER:
                continue

            # Differentiate between plain literals and expression results
            if is_literal_type(operand.type):
                if operand.type not in supported_types:
                    errors.type_error(supported_types, operand.type, operator.type, operator.source_location)
            else:
                operand_types = get_expression_result_types(operand.type)
                # If the operand is an expression result, check if at least one
                # of its possible result types is supported.
                supported = False
                for type in operand_types:
                    if type in supported_types:
                        supported = True
                        break
                if not supported:
                    errors.type_error(supported_types, operand_types, operator.type, operator.source_location)
                

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

                    supported_types = get_supported_operand_types(token.type)

                    operands = self.extract_binary_operands(index)
                    
                    # Check if the operand types are supported by the operator
                    self.check_operand_types(token, operands, supported_types)

                    token.children = operands
                
                
                case TokenType.INCREMENT | \
                    TokenType.DECREMENT:

                    operand = self.extract_unary_operand(index, Side.LEFT)
                  
                    self.check_operand_types(token, (operand,), (TokenType.IDENTIFIER,))
                    token.children = [operand]


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

                    token.children = [value, identifier]
                
                
                case TokenType.PARENTHESIS:
                    if token.value == ')':
                        errors.unbalanced_parentheses(token.source_location)
                    
                    children = []

                    # Find the matching parenthesis in the statement and extract the children
                    depth = 1
                    i = index + 1
                    while True:
                        try:
                            tok = self.tokens[i]
                        except IndexError:
                            errors.unbalanced_parentheses(token.source_location)

                        if tok.type == TokenType.PARENTHESIS:
                            if tok.value == ')':
                                depth -= 1
                                if depth == 0:
                                    break

                            else:
                                depth += 1

                        elif tok.type == TokenType.SEMICOLON:
                            errors.unbalanced_parentheses(tok.source_location)
                        
                        elif tok.type != TokenType.COMMA:
                            children.append(tok)
                        
                        i += 1
                    
                    self.tokens = self.tokens[: index + 1] + self.tokens[i + 1 :]
                    token.children = children

                    # Now, check what these parentheses are used for (function call, declaration, just a parenthesis)
                    
                    # Check if the next token is an identifier
                    identifier_token_index = index + 1
                    if identifier_token_index >= len(self.tokens):
                        continue
                    identifier_token = self.tokens[identifier_token_index]
                    if identifier_token.type != TokenType.IDENTIFIER:
                        continue
                    
                    # Check if the previous token is a curly bracket
                    curly_bracket_token_index = index - 1
                    if curly_bracket_token_index >= 0:
                        curly_bracket_token = self.tokens[curly_bracket_token_index]
                        if curly_bracket_token.type == TokenType.CURLY_BRACKET:
                            # This is a function declaration: "{body} (args) name"
                            token.type = TokenType.FUNCTION_DECLARATION
                            # Update the token's value to include the function body, arguments and name
                            # New format: [body, args, name]
                            token.value = [curly_bracket_token, children, identifier_token]
                            # Remove the curly bracket and idetifier from the list of tokens
                            self.tokens = self.tokens[:curly_bracket_token_index] + [token] + self.tokens[identifier_token_index + 1:]
                            continue
                
                    # If the previous token is not a curly bracket, this is a function call
                    token.type = TokenType.FUNCTION_CALL
                    # Update the value to include the function name
                    token.value = [children, identifier_token]
                    # Remove the identifier from the list of tokens
                    self.tokens.pop(identifier_token_index)


                case TokenType.SQUARE_BRACKET:
                    if token.value == ']':
                        errors.unbalanced_square_brackets(token.source_location)

                    # Differentiate between array literal and array indexing
                    try:
                        next_token = self.tokens[index + 1]
                    except IndexError:
                        errors.unbalanced_square_brackets(token.source_location)
                    
                    # Check if brackets are empty
                    if next_token.type == TokenType.SQUARE_BRACKET and next_token.value == ']':
                        # Check if previous token is a number (the array index to be accessed)
                        try:
                            # Check if the previous token exists
                            prev_token_index = index - 1
                            if prev_token_index > 0:
                                prev_token = self.tokens[prev_token_index]
                                if prev_token.type in (TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.PARENTHESIS):
                                    # Check if the token before the previous token is an identifier
                                    try:
                                        # index - 2 is always >= 0, since index - 1 is always > 0
                                        prev_prev_token = self.tokens[index - 2]
                                        if prev_prev_token.type in (TokenType.IDENTIFIER, TokenType.ARRAY, TokenType.PARENTHESIS):
                                            # The [] is an array indexing operator
                                            token.type = TokenType.ARRAY_INDEXING
                                            token.children = [prev_prev_token, prev_token]
                                            self.tokens = self.tokens[: index - 2] + [token] + self.tokens[index + 2 :]
                                            continue
                                    
                                    except IndexError:
                                        pass   
                        except IndexError:
                            pass

                    # The token is a literal array
                    token.type = TokenType.ARRAY

                    # Find the matching bracket in the statement and extract the children
                    depth = 1
                    i = index + 1
                    while True:
                        try:
                            tok = self.tokens[i]
                        except IndexError:
                            errors.unbalanced_square_brackets(token.source_location)

                        if tok.type == TokenType.SQUARE_BRACKET:
                            if tok.value == ']':
                                depth -= 1
                                if depth == 0:
                                    break

                            else:
                                depth += 1

                        elif tok.type == TokenType.SEMICOLON:
                            errors.unbalanced_square_brackets(tok.source_location)
                        
                        elif tok.type != TokenType.COMMA:
                            token.children.append(tok)
                        
                        i += 1

                    # Lastly, remove the brackets with their contents
                    self.tokens = self.tokens[: index + 1] + self.tokens[i + 1 :]
                    token.value = token.children

                
                case TokenType.CURLY_BRACKET:
                    if token.value == '}':
                        errors.unbalanced_curly_brackets(token.source_location)

                    children: List[Token] = []

                    # Find the matching bracket
                    depth = 1
                    i = index + 1
                    while True:
                        try:
                            tok = self.tokens[i]
                        except IndexError:
                            errors.unbalanced_curly_brackets(token.source_location)

                        if tok.type == TokenType.CURLY_BRACKET:
                            if tok.value == '}':
                                depth -= 1
                                if depth == 0:
                                    break

                            else:
                                depth += 1
                            
                        children.append(tok)                        
                        i += 1

                    self.tokens = self.tokens[: index + 1] + self.tokens[i + 1 :]

                    # Parse the contents of the curly brackets into a tree structure
                    content_tree = SyntaxTree()
                    content_tree.parse_tokens(children)
                    token.children = content_tree.statements


                case TokenType.IF:
                    # Check for an else statement
                    has_else_statement = False
                    next_token_index = index + 1
                    if next_token_index < len(self.tokens):
                        else_token = self.tokens[next_token_index]
                        if else_token.type == TokenType.ELSE:
                            # The else statement is present and already parsed
                            # Else statements have higher priority than if statements
                            has_else_statement = True
                            self.tokens.pop(next_token_index)

                    body, condition = self.extract_binary_operands(index)
                    self.check_operand_types(token, (body,), (TokenType.CURLY_BRACKET,))
                    self.check_operand_types(token, (condition,), (TokenType.BOOLEAN,))

                    token.children = [body, condition]

                    if has_else_statement:
                        token.children.append(else_token)


                case TokenType.WHILE:
                    body, condition = self.extract_binary_operands(index)
                    self.check_operand_types(token, (body,), (TokenType.CURLY_BRACKET,))
                    self.check_operand_types(token, (condition,), (TokenType.BOOLEAN,))
                    
                    token.children = [body, condition]


                case TokenType.ELSE:
                    # Check if the else statement is preceded by an if statement
                    if_index = index - 2
                    if if_index < 0 or self.tokens[if_index].type != TokenType.IF:
                        errors.else_without_if(token.source_location)

                    body = self.extract_unary_operand(index, Side.LEFT)
                    self.check_operand_types(token, (body,), (TokenType.CURLY_BRACKET,))
                    
                    token.children = [body]


    def stringify_token(self, token: Union[Token, List[Token]], depth: int) -> str:
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
    
