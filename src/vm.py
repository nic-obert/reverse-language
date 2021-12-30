import copy
from typing import Any, List, Tuple

import src.operations as operations
from src.symbols import SymbolTable
from src.syntax_tree import SyntaxTree
from src.token import Token, TokenType, is_literal_type


class Processor:

    def __init__(self) -> None:
        self.symbol_table = SymbolTable()
        # Push the global scope.
        self.symbol_table.push_scope()


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
            result = self.interpret_statement(copy.copy(statement))
            print(result)


    def interpret_statement(self, root: Token) -> Token:
        # Don't mind executing literals.
        if is_literal_type(root.type):
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
                symbol = self.symbol_table.get_symbol(root.children[0])
                
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


        return root

