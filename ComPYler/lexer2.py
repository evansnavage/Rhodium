from enum import Enum, auto
import time
import sys


class TT(Enum):
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
    ### Other
    IDENTIFIER = auto()
    STRING_LITERAL = auto()
    NUMBER = auto()


class Token:
    def __init__(self, value: str, type: TT):
        self.value = value
        self.type = type

    def __str__(self):
        return "{ Value: '" + self.value + "' Type: " + self.type.__str__() + "}"


KW = {
    "return": TT.RETURN,
    "let": TT.LET,
}
Symbols = {
    "{": TT.OPEN_CURLY,
    "}": TT.CLOSE_CURLY,
    "(": TT.OPEN_PAREN,
    ")": TT.CLOSE_CURLY,
    "[": TT.OPEN_SQUARE,
    "]": TT.CLOSE_SQUARE,
}
Starts_Less_Than = {
    "<-": TT.ASSIGNMENT,
    "<<": TT.PUSH,
    "<=": TT.COMPARISONOP,
    "<": TT.COMPARISONOP,
}
Starts_Greater_Than = {
    ">=": TT.COMPARISONOP,
    ">>": TT.POP,
    ">": TT.COMPARISONOP,
}
Binary_Operators = {
    "+": TT.BINARYOP,
    "-": TT.BINARYOP,
    "/": TT.BINARYOP,
    "*": TT.BINARYOP,
}


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    src: list[str] = [c for c in source]
    src.reverse()
    while len(src) > 0:
        next_char = src[-1]
        nextnext = src[-2]
        next_2 = next_char + nextnext
        if len(next_2) < 2:  # grody hack
            next_2 = next_char
        if next_char in Symbols:
            tokens.append(Token(next_char, Symbols[next_char]))
            src.pop()
        elif next_2 in Starts_Less_Than:
            tokens.append(Token(next_2, Starts_Less_Than[next_2]))
            src.pop()
            src.pop()
        elif next_char in Starts_Less_Than:
            tokens.append(Token(next_char, Starts_Less_Than[next_char]))
            src.pop()
        elif next_2 in Starts_Greater_Than:
            tokens.append(Token(next_2, Starts_Greater_Than[next_2]))
            src.pop()
            src.pop()
        elif next_char in Starts_Greater_Than:
            tokens.append(Token(next_char, Starts_Greater_Than[next_char]))
            src.pop()
        elif next_char in Binary_Operators:
            tokens.append(Token(next_char, Binary_Operators[next_char]))
            src.pop()
        else:
            ### must be multiple characters
            if next_char == '"':
                # parse as string
                src.pop()
                lst: list[str] = []
                while len(src) > 0 and next_char != '"':
                    next_char = src[-1]
                    lst.append(next_char)
                end_quote = src.pop()
                # if end_quote != '"':
                #     print("Error: Unterminated string literal.")
                #     exit()
                string_str: str = "".join(lst)
                tokens.append(Token(string_str, TT.STRING_LITERAL))
            elif next_char.isnumeric():
                number: list[str] = []
                while len(src) > 0 and not next_char.isspace():
                    next_char = src[-1]
                    number.append(next_char)
                    src.pop()
                number_str: str = "".join(number)
                tokens.append(Token(number_str, TT.NUMBER))
            else:
                ident: list[str] = []
                # parse  as identifier/keyword
                while len(src) > 0 and not next_char.isspace():
                    next_char = src[-1]
                    ident.append(next_char)
                    src.pop()
                ident_str = "".join(ident)
                tokens.append(Token(ident_str, TT.IDENTIFIER))
        if len(src) > 0:
            src.pop()
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
