import re
from enum import Enum, auto
from typing import List
import sys
import time


class TokenType(Enum):
    ASSIGNMENT = auto()  # <-
    RETURN = auto()  # return
    LET = auto()  # let
    OPEN_CURLY = auto()  # {
    CLOSE_CURLY = auto()  # }
    OPEN_PAREN = auto()  # (
    CLOSE_PAREN = auto()  # )
    OPEN_SQUARE = auto()  # [
    CLOSE_SQUARE = auto()  # ]
    PUSH = auto()  # <<
    COMPARISONOP = auto()  # <, >, >=, <=
    POP = auto()  # >>
    BINARYOP = auto()  # +, -, *, /
    ARROW = auto()  # ->
    IDENTIFIER = auto()  # identifiers
    STRING_LITERAL = auto()  # "string"
    NUMBER = auto()  # numbers
    WHITESPACE = auto()
    INVALID = auto()
    COMMENT = auto()


TOKEN_PATTERNS = [
    # Sort by precedence
    (r"//.*", TokenType.COMMENT),  # Matches // and everything after it on the line
    (r"\s+", TokenType.WHITESPACE),  # Matches spaces, tabs, and newlines
    # Multi-character symbols
    (r"<-", TokenType.ASSIGNMENT),  # <-
    (r"<<", TokenType.PUSH),  # <<
    (r">>", TokenType.POP),  # >>
    (r"->", TokenType.ARROW),  # ->
    (r"<=", TokenType.COMPARISONOP),  # <=
    (r">=", TokenType.COMPARISONOP),  # >=
    # Single-character symbols
    (r"\{", TokenType.OPEN_CURLY),  # {
    (r"\}", TokenType.CLOSE_CURLY),  # }
    (r"\(", TokenType.OPEN_PAREN),  # (
    (r"\)", TokenType.CLOSE_PAREN),  # )
    (r"\[", TokenType.OPEN_SQUARE),  # [
    (r"\]", TokenType.CLOSE_SQUARE),  # ]
    (r"<", TokenType.COMPARISONOP),  # <
    (r">", TokenType.COMPARISONOP),  # >
    (r"\+", TokenType.BINARYOP),  # +
    (r"-", TokenType.BINARYOP),  # -
    (r"\*", TokenType.BINARYOP),  # *
    (r"/", TokenType.BINARYOP),  # /
    # Keywords
    (r"return", TokenType.RETURN),  # return
    (r"let", TokenType.LET),  # let
    # Identifiers
    (r"[a-zA-Z_][a-zA-Z0-9_]*", TokenType.IDENTIFIER),  # variable names
    # String literals
    (
        r'"[^"\\]*(?:\\.[^"\\]*)*"',
        TokenType.STRING_LITERAL,
    ),  # Matches "string" with escape sequences
    # Numbers
    (r"\d+", TokenType.NUMBER),  # Matches integers
    # Invalid tokens (fallback)
    (r".", TokenType.INVALID),  # Matches any single character not covered above
]

TOKEN_REGEX = re.compile(
    "|".join(
        f"(?P<{tok.name}_{i}>{pat})" for i, (pat, tok) in enumerate(TOKEN_PATTERNS)
    )
)


class Token:
    def __init__(self, value: str, type: TokenType):
        self.value = value
        self.type = type

    def __str__(self):
        return f"{{ Value: '{self.value}', Type: {self.type} }}"


def tokenize(source: str) -> List[Token]:
    tokens = []
    for match in TOKEN_REGEX.finditer(source):
        token_type_name = match.lastgroup
        matched = match.group()

        if token_type_name and token_type_name.split("_")[0] in [
            "WHITESPACE",
            "COMMENT",
        ]:
            continue

        if token_type_name is None:
            tokens.append(Token(matched, TokenType.INVALID))
            continue

        try:
            token_type = TokenType[token_type_name]
        except KeyError:
            tokens.append(Token(matched, TokenType.INVALID))
        else:
            if token_type == TokenType.STRING_LITERAL:
                matched = matched[1:-1]
            tokens.append(Token(matched, token_type))

    return tokens


def main(args):
    with open(args[1]) as f:
        print("Starting Lexer")
        start = time.time()
        tokens = tokenize(f.read())
        print([str(token) for token in tokens])
        elapsed = round((time.time() - start) * 1000, 5)
        print("Lexer Finished")
        print("Elapsed: ", elapsed, "ms for ", len(tokens), " tokens.")


if __name__ == "__main__":
    main(sys.argv)
