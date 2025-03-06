import sys
import os
import time
import lexer, lexer3, lexerRE

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def compare_lexers(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    start_time = time.time()
    tokens_lexer = list(lexer.tokenize(content))
    lexer_time = time.time() - start_time

    start_time = time.time()
    lexer3_instance = lexer3.Lexer(content)
    tokens_lexer3 = list(lexer3_instance.tokenize())
    lexer3_time = time.time() - start_time

    start_time = time.time()
    tokens_lexerRE = list(lexerRE.tokenize(content))
    lexerRE_time = time.time() - start_time

    print(f"File: {file_path}")
    print(f"lexer: {len(tokens_lexer)} tokens, Time: {lexer_time:.6f} seconds")
    print(f"lexer3: {len(tokens_lexer3)} tokens, Time: {lexer3_time:.6f} seconds")
    print(f"lexerRE: {len(tokens_lexerRE)} tokens, Time: {lexerRE_time:.6f} seconds")

    detailed_comparison = True

    if detailed_comparison:
        print("\nDetailed comparison:")
        max_len = max(len(tokens_lexer), len(tokens_lexer3), len(tokens_lexerRE))

        for i in range(max_len):
            token_lexer = tokens_lexer[i] if i < len(tokens_lexer) else None
            token_lexer3 = tokens_lexer3[i] if i < len(tokens_lexer3) else None
            token_lexerRE = tokens_lexerRE[i] if i < len(tokens_lexerRE) else None

            if token_lexer != token_lexer3 or token_lexer != token_lexerRE:
                print(f"Difference at position {i}:")
                print(f"  lexer:   {token_lexer}")
                print(f"  lexer3:  {token_lexer3}")
                print(f"  lexerRE: {token_lexerRE}")


if __name__ == "__main__":
    test_files = [
        "./example_files/implementTypeHints.rh",
    ]

    for file in test_files:
        compare_lexers(file)
        print("\n" + "-" * 50 + "\n")
