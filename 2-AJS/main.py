import sys
import os
from ajs_lexer import AJSLexer
from ajs_parser import AJSParser


def main():
    # CHECK ARGUMENT NUMBER
    if len(sys.argv) < 3:
        raise ValueError(f"INCORRECT ARGUMENT NUMBER:\n"
            f"# PROVIDED: {len(sys.argv)}\n"
            f"# EXPECTED: 3\n"
            f"# USAGE: python3 ./main.py <path>.ajs -<mode>\n"
            f"# - <path>: path to an AJS file. Examples in ./2-AJS/tests\n"
            f"# - <mode>: lex = lexer || par = parser")
    
    # CHECK MODE
    if sys.argv[2] not in ["-lex", "-par"]:
        raise ValueError(f"INCORRECT MODE:\n"
            f"# PROVIDED: {sys.argv[2]}\n"
            f"# EXPECTED: lex || par\n"
            f"# USAGE: python3 ./main.py ... -<mode>\n"
            f"# - ...\n"
            f"# - <mode>: lex = lexer || par = parser")
    
    # CHECK FILE EXTENSION
    if os.path.splitext(sys.argv[1])[1] != ".ajs":
        raise ValueError(f"INCORRECT FILE EXTENSION:\n"
            f"# PROVIDED: {os.path.splitext(sys.argv[1])[1]}\n"
            f"# EXPECTED: .ajs")
    
    if sys.argv[2] == "-par":  # lexer & parser
        parser = AJSParser()
        parser.parse(sys.argv[1])
    else:  # lexer
        lexer = AJSLexer()
        lexer.tokenize(sys.argv[1])


if __name__ == "__main__":
    main()