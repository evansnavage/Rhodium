from enum import Enum, auto
import sys


class Token_Type(Enum):
    # need to be sorted by distinctness, if :: and : are symbols,
    # :: needs to come first
    RETURN = auto()  # return
    LET = auto()
    IDENTIFIER = auto()  # variable names
    ASSIGNMENT = auto()  # <-
    INTEGER_LITERAL = auto()  # 12
    TYPE = auto()
    PAREN_OPEN = auto()
    PAREN_CLOSE = auto()
    CURLY_OPEN = auto()
    CURLY_CLOSE = auto()
    FUNCTION_DEF = auto()
    RETURN_TYPE = auto()
    BINARY_OPERATION = auto()
    COMPARISON_OPERATION = auto()
    PUSH_POP = auto()


KEYWORDS = {
    "return": Token_Type.RETURN,
    "let": Token_Type.LET,
}

# example program
# let error_code: int32 <- 0
# return error_code


class Token:
    def __init__(self, value: str, type: Token_Type):
        self.value = value
        self.type = type

    def __str__(self):
        return "{ Value: '" + self.value + "' Type: " + self.type.__str__() + "}"


def tokenize(source: str):
    tokens: list[Token] = []
    src: list[str] = [
        character for character in source
    ]  # very non-performant way to do this, should prolly **at least** reverse and pop from the end so no re-indexing
    # but I'm writing a compiler in python
    while len(src) > 0:
        match src[0]:
            ### Parentheses
            case "(":
                tokens.append(Token("(", Token_Type.PAREN_OPEN))
            case ")":
                tokens.append(Token(")", Token_Type.PAREN_CLOSE))
            ### Curly Brace
            case "{":
                tokens.append(Token("{", Token_Type.CURLY_OPEN))
            case "}":
                tokens.append(Token("}", Token_Type.CURLY_CLOSE))
            ### Binary Operators
            case "+" | "-" | "/" | "*":
                tokens.append(Token(src[0], Token_Type.BINARY_OPERATION))
            ### Assignment and LT GT Comparison
            case "<":  ## Assign, Push, LTE, LT
                next_char = src[1]
                if next_char == "-":
                    tokens.append(Token("<-", Token_Type.ASSIGNMENT))
                    src.pop(1)
                elif next_char == "<":
                    tokens.append(Token("<<", Token_Type.PUSH_POP))
                    src.pop(1)
                elif next_char == "=":
                    tokens.append(Token("<=", Token_Type.COMPARISON_OPERATION))
                else:
                    tokens.append(Token("<", Token_Type.COMPARISON_OPERATION))
            case ">":  ## Pop, GTE, GT
                next_char = src[1]
                if next_char == ">":
                    tokens.append(Token(">>", Token_Type.PUSH_POP))
                elif next_char == "=":
                    tokens.append(Token(">=", Token_Type.COMPARISON_OPERATION))
                else:
                    tokens.append(Token(">", Token_Type.COMPARISON_OPERATION))
            case (
                _
            ):  # basically else, tells us that whatever we have cannot be determined from it's first character
                # so it's more than one letter (and not a special case like <-)
                # loop until hit space, check if it's a keyword, ie. return, let
                word = []
                while len(src) > 0 and not src[0].isspace():
                    word.append(src[0])
                    src.pop(0)
                if len(word) > 0:
                    word_str = "".join(word)
                    if word_str in KEYWORDS:
                        tokens.append(Token(word_str, KEYWORDS[word_str]))
                    elif word_str[0].isnumeric():
                        try:
                            int(word_str)
                        except ValueError:
                            print(
                                "ERORR: "
                                + "Identifiers may not start with a numeral. Attempted to create numeric value from: '"
                                + word_str
                                + "'"
                                + "\nContinuing lexing..."
                            )
                            continue
                        tokens.append(Token(word_str, Token_Type.INTEGER_LITERAL))
                    else:
                        tokens.append(Token(word_str, Token_Type.IDENTIFIER))
        ### Consume the token if it hasn't been
        if len(src) > 0:
            src.pop(0)
    return tokens


def main(args):
    with open(args[1]) as f:
        tokens = tokenize(f.read())
        print([str(token) for token in tokens])


if __name__ == "__main__":
    main(sys.argv)
