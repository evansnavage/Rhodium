import time
import sys
import lexer
import lexerVerification


def main(args):
    with open(args[1]) as f:
        # Lex File
        print("Starting Lexer")
        start = time.time()
        tokens = lexer.tokenize(f.read())
        elapsed = round((time.time() - start) * 1000, 5)
        print("Lexer Finished")
        print("Elapsed: ", elapsed, "ms for ", len(tokens), " tokens.")
        # Verify Lexer Output
        print("Verifying lexed tokens.")
        start = time.time()
        tokens = lexerVerification.verify(tokens)
        elapsed = round((time.time() - start) * 1000, 5)
        print("Elapsed: ", elapsed, "ms")

        print([str(token) for token in tokens])

if __name__ == "__main__":
    main(sys.argv)

# Parse
# Verify
# Assemble
