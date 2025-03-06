from lexer import Token, TokenType

VALID_TYPES: dict = {
    ### typename without the ': ' : size in bytes
    "i32": 4,
}


def print_line(tokens: list, line_num: int):
    print("Line with error:")
    for token in tokens:
        if token.line == line_num:
            if token.type is TokenType.STRING_LITERAL:
                print('"', end="")
            print(token.value, end=" ")
            if token.type is TokenType.STRING_LITERAL:
                print('\b"')
        if token.line > line_num:
            return


def verify_types(tokens: list[Token]):
    for token in tokens:
        errors: list = []
        if token.type is TokenType.TYPE:
            token_type = token.value.split(" ")[1]
            if token_type not in VALID_TYPES:
                errors.append(f"Found invalid type: {token_type}")
        if len(errors) > 0:
            print(f"Found errors on line {token.line}:", end=" ")
            print(errors)
            print_line(tokens, token.line)


def verify_definition(tokens: list[Token]):
    for token_idx in range(len(tokens)):
        errors: list = []
        token = tokens[token_idx]
        if token.type is TokenType.LET:
            ### next token must be an identifier
            if (
                token_idx + 1 >= len(tokens)
                or tokens[token_idx + 1].type is not TokenType.IDENTIFIER
            ):
                errors.append("Expected identifier after 'let'")
            ### token after identifier must be type
            elif (
                token_idx + 2 >= len(tokens)
                or tokens[token_idx + 2].type is not TokenType.TYPE
            ):
                errors.append("Expected type for assignment")
            elif (
                token_idx + 3 >= len(tokens)
                or tokens[token_idx + 3].type is not TokenType.ASSIGNMENT
            ):
                errors.append(
                    "Expected assignment operator (<-) in identifier declaration"
                )
        if len(errors) > 0:
            print(f"Found errors on line {token.line}:", end=" ")
            print(errors)
            print_line(tokens, token.line)


def verify(tokens: list[Token]):
    verify_types(tokens)
    verify_definition(tokens)
