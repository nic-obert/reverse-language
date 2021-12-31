import copy
from typing import Any, List, Tuple

import src.errors as errors
import src.operations as operations
from src.state import State
from src.symbols import SymbolTable
from src.syntax_tree import SyntaxTree
from src.token import Token, TokenType, is_literal_type


class Processor:

    def __init__(self) -> None:
        self.symbol_table = SymbolTable()
        # Push the global scope.
        self.symbol_table.push_scope()
    

    def to_literals(self, tokens: List[Token]) -> List[Token]:
        """
            Convert a list of tokens into a list of literal tokens.
        """
        literals: List[Token] = []
        for token in tokens:
            if token.type == TokenType.IDENTIFIER:
                value, type = self.get_value_and_type(token)
                literals.append(Token(type, 0, token.source_location, value))
            else:
                literals.append(token)
        
        return literals


    def get_value_and_type(self, token: Token) -> Tuple[Any, TokenType]:
        if token.type == TokenType.IDENTIFIER:
            symbol = self.symbol_table.get_symbol(token)
            return symbol.value, symbol.type
        
        elif token.type == TokenType.PARENTHESIS:
            return self.get_value_and_type(token.children[0])
                
        return token.value, token.type
    
    
    def interpret_tree(self, syntax_tree: SyntaxTree) -> None:
        """
            Interpret the given syntax tree.
        """
        self.interpret_statements(syntax_tree.statements)
    

    def interpret_statements(self, statements: List[Token]) -> None:
        for statement in statements:
            result = self.interpret_statement(copy.deepcopy(statement))
            if State.verbose:
                print(result)


    def interpret_statement(self, root: Token) -> Token:
        
        # Don't mind executing literals, except arrays. 
        # Arrays have to check their elements for identifiers at declaration.
        if root.type != TokenType.ARRAY and is_literal_type(root.type) \
            or root.type == TokenType.IDENTIFIER:
            return root

        # Interpret the statement recursively.
        if root.type not in (TokenType.IF, TokenType.WHILE):
            for index, child in enumerate(root.children):
                root.children[index] = self.interpret_statement(child)

        match root.type:

            case TokenType.PLUS:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.add(value1, type1, value2, type2, root)
                root.type = type1
            

            case TokenType.MINUS:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.subtract(value1, type1, value2, type2, root)
                root.type = TokenType.NUMBER
            

            case TokenType.MULTIPLY:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.multiply(value1, type1, value2, type2, root)
                root.type = TokenType.NUMBER
            

            case TokenType.DIVIDE:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.divide(value1, type1, value2, type2, root)
                root.type = TokenType.NUMBER
            

            case TokenType.MODULO:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.modulo(value1, type1, value2, type2, root)
                root.type = TokenType.NUMBER


            case TokenType.INCREMENT:
                identifier = root.children[0]
                symbol = self.symbol_table.get_symbol(identifier)
                
                new_value = operations.increment(symbol.value, symbol.type, root)
                
                self.symbol_table.set_symbol_value(identifier.value, new_value)
                root.value = symbol.value
                root.type = TokenType.NUMBER
            

            case TokenType.DECREMENT:
                identifier = root.children[0]
                symbol = self.symbol_table.get_symbol(root.children[0])

                new_value = operations.decrement(symbol.value, symbol.type, root)

                self.symbol_table.set_symbol_value(identifier.value, new_value)
                root.value = symbol.value
                root.type = TokenType.NUMBER


            case TokenType.EQUAL:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.equal(value1, type1, value2, type2, root)
                root.type = TokenType.BOOLEAN
            

            case TokenType.NOT_EQUAL:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.not_equal(value1, type1, value2, type2, root)
                root.type = TokenType.BOOLEAN


            case TokenType.GREATER_THAN:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.greater_than(value1, type1, value2, type2, root)
                root.type = TokenType.BOOLEAN


            case TokenType.LESS_THAN:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.less_than(value1, type1, value2, type2, root)
                root.type = TokenType.BOOLEAN


            case TokenType.GREATER_THAN_OR_EQUAL:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.greater_than_or_equal(value1, type1, value2, type2, root)
                root.type = TokenType.BOOLEAN


            case TokenType.LESS_THAN_OR_EQUAL:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.less_than_or_equal(value1, type1, value2, type2, root)
                root.type = TokenType.BOOLEAN

            case TokenType.AND:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.and_(value1, type1, value2, type2, root)
                root.type = TokenType.BOOLEAN


            case TokenType.OR:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                root.value = operations.or_(value1, type1, value2, type2, root)
                root.type = TokenType.BOOLEAN


            case TokenType.NOT:
                value1, type1 = self.get_value_and_type(root.children[0])
                root.value = operations.not_(value1, type1, root)
                root.type = TokenType.BOOLEAN


            case TokenType.ASSIGNMENT:
                value_token = root.children[0]
                value, type = self.get_value_and_type(value_token)
                value_token.value = value
                value_token.type = type
                identifier = root.children[1]

                self.symbol_table.set_symbol(identifier.value, value_token)
                root.value = value
                root.type = type


            case TokenType.ASSIGNMENT_ADD:
                value, type = self.get_value_and_type(root.children[0])

                identifier = root.children[1]
                symbol = self.symbol_table.get_symbol(identifier)

                new_value = operations.add(symbol.value, symbol.type, value, type, root)

                self.symbol_table.set_symbol_value(identifier.value, new_value)
                root.value = symbol.value
                root.type = type


            case TokenType.ASSIGNMENT_SUB:
                value, type = self.get_value_and_type(root.children[0])

                identifier = root.children[1]
                symbol = self.symbol_table.get_symbol(identifier)

                new_value = operations.subtract(symbol.value, symbol.type, value, type, root)

                self.symbol_table.set_symbol_value(identifier.value, new_value)
                root.value = symbol.value
                root.type = type


            case TokenType.ASSIGNMENT_MUL:
                value, type = self.get_value_and_type(root.children[0])

                identifier = root.children[1]
                symbol = self.symbol_table.get_symbol(identifier)

                new_value = operations.multiply(symbol.value, symbol.type, value, type, root)

                self.symbol_table.set_symbol_value(identifier.value, new_value)
                root.value = symbol.value
                root.type = type


            case TokenType.ASSIGNMENT_DIV:
                value, type = self.get_value_and_type(root.children[0])

                identifier = root.children[1]
                symbol = self.symbol_table.get_symbol(identifier)

                new_value = operations.divide(symbol.value, symbol.type, value, type, root)

                self.symbol_table.set_symbol_value(identifier.value, new_value)
                root.value = symbol.value
                root.type = type


            case TokenType.ASSIGNMENT_MOD:
                value, type = self.get_value_and_type(root.children[0])

                identifier = root.children[1]
                symbol = self.symbol_table.get_symbol(identifier)

                new_value = operations.mod(symbol.value, symbol.type, value, type, root)

                self.symbol_table.set_symbol_value(identifier.value, new_value)
                root.value = symbol.value
                root.type = type
            

            case TokenType.IF:
                body = root.children[0]
                condition = root.children[1]

                condition_value = self.interpret_statement(copy.deepcopy(condition))
                if condition_value.type == TokenType.BOOLEAN and condition_value.value == True:
                    # Condition is true, so execute the if statement body
                    self.interpret_statements(body.children)
                else:
                    # Condition is false, so skip the if statement body
                    # Check if there is an else statement, and if so, execute it
                    if len(root.children) == 3:
                        else_statement = root.children[2]
                        self.interpret_statements(else_statement.children[0].children)
 

            case TokenType.WHILE:
                body = root.children[0]
                condition = root.children[1]

                while True:
                    condition_value = self.interpret_statement(copy.deepcopy(condition))
                    if condition_value.type == TokenType.BOOLEAN and condition_value.value == True:
                        self.interpret_statements(body.children)
                    else:
                        break
            

            case TokenType.PARENTHESIS:
                root = root.children[0]
            

            case TokenType.FUNCTION_DECLARATION:
                body_token: Token = root.value[0]
                parameters_token_list: List[Token] = root.value[1]
                identifier_token: Token = root.value[2]

                # Create a new function token to store the newly declared function
                # Function token format: [[arguments], [function_body_statements]]
                # Data types:            [List[str],   List[Token]               ]    
                function = Token(TokenType.FUNCTION, 0, None)

                parameter_list: List[str] = [parameter.value for parameter in parameters_token_list]

                function.value = [parameter_list, body_token.children]

                self.symbol_table.set_symbol(identifier_token.value, function)
            

            case TokenType.FUNCTION_CALL:
                arguments_token_list: List[Token] = root.value[0]
                identifier_token: Token = root.value[1]

                # Check if the function has a built-in handler
                builtin_handler = operations.get_builtin_handler(identifier_token.value)

                if builtin_handler is not None:
                    # Parameter list will just be used to check if the number of arguments is correct
                    parameter_list = builtin_handler.supported_argument_types
                else:
                    # Get the function from the symbol table
                    function = self.symbol_table.get_symbol(identifier_token)
                    parameter_list: List[str] = function.value[0]
                    statements: List[Token] = function.value[1]

                # Check if the number of arguments matches the number of arguments in the function
                if len(arguments_token_list) != len(parameter_list):
                    errors.wrong_argument_count(
                        identifier_token.value,
                        len(parameter_list),
                        len(arguments_token_list),
                        root.source_location
                    )

                if builtin_handler is not None:
                    argument_literals = self.to_literals(arguments_token_list)
                    root = builtin_handler.call(argument_literals, root)
                else:
                    # Before pushing the new scope to the stack, retrieve eventual symbols from the previous scope
                    argument_literals = self.to_literals(arguments_token_list)

                    # Push the new scope to the stack
                    self.symbol_table.push_scope()

                    # Declare the arguments in the new scope
                    for identifier, argument in zip(parameter_list, argument_literals):
                        self.symbol_table.set_symbol(identifier, argument)
                    
                    # Extract the return statement from the function body, it will be executed at the end of the function
                    # The return statement is guaranteed to be the first statement in the function body by the SyntaxTree class parser
                    return_statement = statements[0]

                    # Execute the function body, excluding the return statement
                    # Don't directly modify the statements list, as it may be used in later function calls
                    self.interpret_statements(statements[1:])

                    # Execute the return statement and set the function call token to the return value
                    root = self.interpret_statement(return_statement)

                    # Pop the scope from the stack
                    self.symbol_table.pop_scope()

            
            case TokenType.RETURN:
                return_value = root.children[0]
                if return_value.type == TokenType.IDENTIFIER:
                    # Get the value of the identifier
                    symbol = self.symbol_table.get_symbol(return_value)
                    root = Token(symbol.type, 0, root.source_location, symbol.value)
                
                elif return_value.type == TokenType.ARRAY:
                    # Recursively get all the literal values of the array
                    root = Token(TokenType.ARRAY, 0, root.source_location, self.to_literals(return_value.children))
                
                else:
                    # If the return value is a single literal token, just return it as it is
                    root = return_value
            

            case TokenType.ARRAY_INDEXING:
                array, array_type = self.get_value_and_type(root.children[0])
                index, index_type = self.get_value_and_type(root.children[1])

                root = operations.array_index(array, array_type, index, index_type, root)


            case TokenType.ARRAY:
                content: List[Token] = root.value
                for element in content:
                    if element.type == TokenType.IDENTIFIER:
                        element_value, element_type = self.get_value_and_type(element)
                        element.type = element_type
                        element.value = element_value
        

        return root

