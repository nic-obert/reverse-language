from typing import List, Union

from token import Token


def tokenize_source_code(source_code: str) -> List[Token]:
    
    token: Union[Token, None] = None
    base_priority = 0
    tokens: List[Token] = []
    parenthesis_depth = 0

    for index, character in enumerate(source_code):
        pass

    if token is not None:
        tokens.append(token)

    return tokens
