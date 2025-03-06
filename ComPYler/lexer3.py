from enum import Enum, auto
import sys
import time
from typing import List, Optional


class TokenType(Enum):
    ### Map Searches
    ASSIGNMENT = auto()
    RETURN = auto()
    LET = auto()
    OPEN_CURLY = auto()
    CLOSE_CURLY = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    OPEN_SQUARE = auto()
    CLOSE_SQUARE = auto()
    PUSH = auto()
    COMPARISONOP = auto()
    POP = auto()
    BINARYOP = auto()
    ARROW = auto()
    ### Other
    IDENTIFIER = auto()
    STRING_LITERAL = auto()
    NUMBER = auto()


KEYWORDS = {
    "return": TokenType.RETURN,
    "let": TokenType.LET,
}
SYMBOLS = {
    "{": TokenType.OPEN_CURLY,
    "}": TokenType.CLOSE_CURLY,
    "(": TokenType.OPEN_PAREN,
    ")": TokenType.CLOSE_CURLY,
    "[": TokenType.OPEN_SQUARE,
    "]": TokenType.CLOSE_SQUARE,
    # LT, GT
    ">": TokenType.COMPARISONOP,
    "<": TokenType.COMPARISONOP,
    # Binary Operators
    "+": TokenType.BINARYOP,
    "-": TokenType.BINARYOP,
    "/": TokenType.BINARYOP,
    "*": TokenType.BINARYOP,
    ### LT+
    "<-": TokenType.ASSIGNMENT,
    "<=": TokenType.COMPARISONOP,
    "<<": TokenType.PUSH,
    ### GT+
    ">=": TokenType.COMPARISONOP,
    "->": TokenType.ARROW,
    ">>": TokenType.POP,
}


class Token:
    def __init__(self, value: str, type: TokenType):
        self.value = value
        self.type = type

    def __str__(self):
        return f"{{ Value: '{self.value}', Type: {self.type} }}"


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.position = 0
        self.line = 1
        self.column = 1

    def advance(self):
        if self.position < len(self.source):
            if self.source[self.position] == "\n":
                self.line += 1
                self.column = 0
            else:
                self.column += 1
            self.position += 1

    def skip_whitespace(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.advance()

    def skip_comment(self):
        while self.position < len(self.source) and self.source[self.position] != "\n":
            self.advance()

    def parse_string(self) -> Optional[Token]:
        self.advance()  # Skip the opening quote
        start = self.position
        while self.position < len(self.source) and self.source[self.position] != '"':
            self.advance()
        if self.position >= len(self.source):
            raise SyntaxError("Unterminated string literal")
        value = self.source[start : self.position]
        self.advance()  # Skip the closing quote
        return Token(value, TokenType.STRING_LITERAL)

    def parse_number(self) -> Optional[Token]:
        start = self.position
        while self.position < len(self.source) and self.source[self.position].isdigit():
            self.advance()
        value = self.source[start : self.position]
        return Token(value, TokenType.NUMBER)

    def parse_identifier_or_keyword(self) -> Optional[Token]:
        start = self.position
        while self.position < len(self.source) and (
            self.source[self.position].isalnum() or self.source[self.position] == "_"
        ):
            self.advance()
        value = self.source[start : self.position]
        if value in KEYWORDS:
            return Token(value, KEYWORDS[value])
        return Token(value, TokenType.IDENTIFIER)

    def parse_symbol(self) -> Optional[Token]:
        if self.position + 1 < len(self.source):
            two_char_symbol = self.source[self.position : self.position + 2]
            if two_char_symbol in SYMBOLS:
                self.advance()
                self.advance()
                return Token(two_char_symbol, SYMBOLS[two_char_symbol])
        else:
            one_char_symbol = self.source[self.position]
            if one_char_symbol in SYMBOLS:
                self.advance()
                return Token(one_char_symbol, SYMBOLS[one_char_symbol])
        return None

    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            current_char = self.source[self.position]
            if current_char.isspace():
                self.skip_whitespace()
            elif (
                current_char == "/"
                and self.position + 1 < len(self.source)
                and self.source[self.position] == "/"
            ):
                self.skip_comment()
            elif current_char == '"':
                parsed_str = self.parse_string()
                if parsed_str:
                    self.tokens.append(parsed_str)
            elif current_char.isdigit():
                parsed_num = self.parse_number()
                if parsed_num:
                    self.tokens.append(parsed_num)
            elif current_char.isalpha():
                parsed_ident_or_keyword = self.parse_identifier_or_keyword()
                if parsed_ident_or_keyword:
                    self.tokens.append(parsed_ident_or_keyword)
            else:
                parsed_symbol = self.parse_symbol()
                if parsed_symbol:
                    self.tokens.append(parsed_symbol)
                else:
                    raise SyntaxError(f"Unexpected character: {current_char}")
        return self.tokens


def main(args):
    with open(args[1], "a") as f:
        f.write("\n\n")
    with open(args[1], "r") as f:
        print("Starting Lexer")
        start = time.time()
        lexer = Lexer(f.read())
        tokens = lexer.tokenize()
        print([str(token) for token in tokens])
        elapsed = round((time.time() - start) * 1000, 5)
        print("Lexer Finished")
        print("Elapsed: ", elapsed, "ms for ", len(tokens), " tokens.")


if __name__ == "__main__":
    main(sys.argv)
