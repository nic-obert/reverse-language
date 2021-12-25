from typing import Dict, Union

from token import TokenType


keyword_table: Dict[str, TokenType] = {
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'true': TokenType.BOOLEAN,
    'false': TokenType.BOOLEAN,
    'null': TokenType.NULL,
}


def get_keyword_type(word: str) -> Union[TokenType, None]:
    return keyword_table.get(word)

