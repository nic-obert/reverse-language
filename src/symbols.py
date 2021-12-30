from __future__ import annotations
from typing import Any, Dict, List

import src.errors as errors
from src.token import TokenType, Token


class Symbol:

    def __init__(self, type: TokenType, value: Any) -> None:
        self.type = type
        self.value = value


class Scope:

    def __init__(self) -> None:
        self.symbols: Dict[str, Symbol] = {}

    
    def set_symbol(self, name: str, value: Token) -> None:
        """
            Set the Symbol in the current scope.
            If the value is an identifier, handle it as such
            by retrieving the value from the current scope.
        """
        if value.type == TokenType.IDENTIFIER:
            symbol = self.get_symbol(value)
        elif value.type == TokenType.CURLY_BRACKET:
            # Token value is a function body, store its statements
            symbol = Symbol(TokenType.FUNCTION, value.children)
        else:
            symbol = Symbol(value.type, value.value)
        
        self.symbols[name] = symbol
    

    def get_symbol(self, identifier: Token) -> Symbol:
        """
            If the symbol is defined, return it.
            If the symbol is not defined, raise an error.
        """
        try:
            return self.symbols[identifier.value]
        except KeyError:
            errors.undefined_identifier(identifier.value, identifier.source_location)
             

    def set_symbol_value(self, name: str, value: Any) -> None:
        """
            Set the value of the symbol in the current scope.
        """
        self.symbols[name].value = value
        

class ScopeStack:

    def __init__(self) -> None:
        self.stack: List[Scope] = []

    
    def get_symbol(self, identifier: Token) -> Symbol:
        """
            Get the Symbol from the current scope.
            If the symbol is not defined, raise an error.
        """
        try:
            return self.stack[-1].get_symbol(identifier)
        except IndexError:
            errors.undefined_identifier(identifier.value, identifier.source_location)


    def set_symbol(self, name: str, value: Token) -> None:
        """
            Set the Symbol in the current scope.
        """
        self.stack[-1].set_symbol(name, value)
    

    def set_symbol_value(self, name: str, value: Any) -> None:
        """
            Set the value of the symbol in the current scope.
        """
        self.stack[-1].set_symbol_value(name, value)


    def push_scope(self) -> None:
        """
            Push a new scope onto the stack.
        """
        self.stack.append(Scope())

    
    def pop_scope(self) -> None:
        """
            Pop the current scope off the stack.
        """
        self.stack.pop()


class SymbolTable:

    def __init__(self) -> None:
        self.scope_stack = ScopeStack()

    
    def get_symbol(self, identifier: Token) -> Symbol:
        """
            Get the Symbol from the current scope.
            If the symbol is not defined, raise an error.
        """
        return self.scope_stack.get_symbol(identifier)


    def set_symbol(self, name: str, value: Token) -> None:
        """
            Set the Symbol in the current scope.
        """
        self.scope_stack.set_symbol(name, value)
    

    def set_symbol_value(self, name: str, value: Any) -> None:
        """
            Set the value of the symbol in the current scope.
        """
        self.scope_stack.set_symbol_value(name, value)


    def push_scope(self) -> None:
        """
            Push a new scope onto the stack.
        """
        self.scope_stack.push_scope()


    def pop_scope(self) -> None:
        """
            Pop the current scope off the stack.
        """
        self.scope_stack.pop_scope()
    
