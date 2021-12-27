from typing import Any, Tuple, Union

import src.errors as errors
from src.symbols import SymbolTable
from src.syntax_tree import SyntaxTree
from src.token import Token, TokenType, get_supported_operand_types


class Processor:

    def __init__(self) -> None:
        self.symbol_table = SymbolTable()
        # Push the global scope.
        self.symbol_table.push_scope()

    
    def get_value_and_type(self, token: Token) -> Tuple[Any, TokenType]:
        if token.type == TokenType.IDENTIFIER:
            symbol = self.symbol_table.get_symbol(token)
            return symbol.value, symbol.type
        return token.value, token.type
    

    def check_type(self, provided_type: TokenType, operator: Token) -> None:
        expected_types = get_supported_operand_types(operator.type)
        if provided_type not in expected_types:
            errors.type_error(expected_types, provided_type, operator, operator.source_location)

    
    def interpret(self, syntax_tree: SyntaxTree) -> None:
        """
            Interpret the given syntax tree.
        """
        statements = syntax_tree.statements
        for statement in statements:
            self.interpret_statement(statement)


    def interpret_statement(self, root: Token) -> Token:
        # Interpret the statement recursively.
        for index, child in enumerate(root.children):
            root.children[index] = self.interpret_statement(child)

        match root.type:

            case TokenType.PLUS:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                
                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 + value2
                root.type = type1
            
            case TokenType.MINUS:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                
                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 - value2
                root.type = TokenType.NUMBER
            
            case TokenType.MULTIPLY:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                
                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 * value2
                root.type = TokenType.NUMBER
            
            case TokenType.DIVIDE:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])
                
                self.check_type(type1, root)
                self.check_type(type2, root)

                if value2 == 0:
                    errors.division_by_zero(root.source_location)

                root.value = value1 / value2
                root.type = TokenType.NUMBER
            
            case TokenType.MODULO:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                if value2 == 0:
                    errors.division_by_zero(root.source_location)
                
                root.value = value1 % value2
                root.type = TokenType.NUMBER

            case TokenType.INCREMENT:
                identifier = root.children[0]
                symbol = self.symbol_table.get_symbol(root.children[0])
                
                self.check_type(symbol.type, root)

                self.symbol_table.set_symbol_value(identifier.value, symbol.value + 1)
                root.value = symbol.value
                root.type = TokenType.NUMBER
            
            case TokenType.DECREMENT:
                identifier = root.children[0]
                symbol = self.symbol_table.get_symbol(root.children[0])

                self.check_type(symbol.type, root)

                self.symbol_table.set_symbol_value(identifier.value, symbol.value - 1)
                root.value = symbol.value
                root.type = TokenType.NUMBER

            case TokenType.EQUAL:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 == value2
                root.type = TokenType.BOOLEAN
            
            case TokenType.NOT_EQUAL:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 != value2
                root.type = TokenType.BOOLEAN

            case TokenType.GREATER_THAN:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 > value2
                root.type = TokenType.BOOLEAN

            case TokenType.LESS_THAN:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 < value2
                root.type = TokenType.BOOLEAN

            case TokenType.GREATER_THAN_OR_EQUAL:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 >= value2
                root.type = TokenType.BOOLEAN

            case TokenType.LESS_THAN_OR_EQUAL:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 <= value2
                root.type = TokenType.BOOLEAN

            case TokenType.AND:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 and value2
                root.type = TokenType.BOOLEAN

            case TokenType.OR:
                value1, type1 = self.get_value_and_type(root.children[0])
                value2, type2 = self.get_value_and_type(root.children[1])

                self.check_type(type1, root)
                self.check_type(type2, root)

                root.value = value1 or value2
                root.type = TokenType.BOOLEAN

            case TokenType.NOT:
                value1, type1 = self.get_value_and_type(root.children[0])

                self.check_type(type1, root)

                root.value = not value1
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
                value_token = root.children[0]
                value, type = self.get_value_and_type(value_token)

                self.check_type(type, root)

                identifier = root.children[1]

                symbol = self.symbol_table.get_symbol(identifier)
                self.symbol_table.set_symbol_value(identifier.value, symbol.value + value)
                root.value = symbol.value
                root.type = type

            case TokenType.ASSIGNMENT_SUB:
                value_token = root.children[0]
                value, type = self.get_value_and_type(value_token)

                self.check_type(type, root)

                identifier = root.children[1]

                symbol = self.symbol_table.get_symbol(identifier)
                self.symbol_table.set_symbol_value(identifier.value, symbol.value - value)
                root.value = symbol.value
                root.type = TokenType.NUMBER

            case TokenType.ASSIGNMENT_MUL:
                value_token = root.children[0]
                value, type = self.get_value_and_type(value_token)

                self.check_type(type, root)

                identifier = root.children[1]

                symbol = self.symbol_table.get_symbol(identifier)
                self.symbol_table.set_symbol_value(identifier.value, symbol.value * value)
                root.value = symbol.value
                root.type = TokenType.NUMBER

            case TokenType.ASSIGNMENT_DIV:
                value_token = root.children[0]
                value, type = self.get_value_and_type(value_token)

                self.check_type(type, root)

                if value == 0:
                    errors.division_by_zero(root.source_location)

                identifier = root.children[1]

                symbol = self.symbol_table.get_symbol(identifier)
                self.symbol_table.set_symbol_value(identifier.value, symbol.value / value)
                root.value = symbol.value
                root.type = TokenType.NUMBER

            case TokenType.ASSIGNMENT_MOD:
                value_token = root.children[0]
                value, type = self.get_value_and_type(value_token)

                self.check_type(type, root)

                if value == 0:
                    errors.division_by_zero(root.source_location)

                identifier = root.children[1]

                symbol = self.symbol_table.get_symbol(identifier)
                self.symbol_table.set_symbol_value(identifier.value, symbol.value % value)
                root.value = symbol.value
                root.type = TokenType.NUMBER
        
        return root
        
