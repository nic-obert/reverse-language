

def unexpected_character(character: str, line_number: int, line_start_index: int, source_code: str) -> None:
    print(f'Unexpected character "{character}" at line {line_number}')
    line = source_code[line_start_index:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)


def unbalanced_parenthesis(line_number: int, line_start_index: int, source_code: str) -> None:
    print(f'Unbalanced parenthesis at line {line_number}')
    line = source_code[line_start_index:].split('\n', maxsplit=1)[0]
    print(line)
    exit(1)

