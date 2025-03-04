from enum import Enum, auto


class Token:
    def __init__(self, value: str, type: TT):
        self.value = value
        self.type = type


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
        next = src[-1]
        nextnext = src[-2]
        next_2 = next + nextnext
        if len(next_2) < 2:  # grody hack
            next_2 = next
        if next in Symbols:
            tokens.append(Token(next, Symbols[next]))
            src.pop()
        elif next_2 in Starts_Less_Than:
            tokens.append(Token(next_2, Starts_Less_Than[next_2]))
            src.pop()
            src.pop()
        elif next in Starts_Less_Than:
            tokens.append(Token(next, Starts_Less_Than[next]))
            src.pop()
        elif next_2 in Starts_Greater_Than:
            tokens.append(Token(next_2, Starts_Greater_Than[next_2]))
            src.pop()
            src.pop()
        elif next in Starts_Greater_Than:
            tokens.append(Token(next, Starts_Greater_Than[next]))
            src.pop()
        elif next in Binary_Operators:
            tokens.append(Token(next, Binary_Operators[next]))
            src.pop()
        else:
            ### must be multiple characters
            if next == '"':
                src.pop()
                lst: list[str] = []
                while len(src) > 0 and next != '"':
                    lst.append(next)
                    src.pop()
                end_quote = src.pop()
                if end_quote != '"':
                    print("Error: Unterminated string literal.")
    return tokens
