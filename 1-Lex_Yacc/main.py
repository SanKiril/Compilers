import sys
import os
from ajson_lexer import AJSONLexer
from ajson_parser import AJSONParser


def main():
    # CHECK ARGUMENT NUMBER
    if len(sys.argv) != 2:
        raise ValueError(f"INCORRECT ARGUMENT NUMBER:\n- PROVIDED: {len(sys.argv)}\n- EXPECTED: 2\n# USAGE: python3 ./main.py <file_path>.ajson")
    
    # OPEN <file_path>.ajson
    try:
        file = open(sys.argv[1])
    except FileNotFoundError:
        raise FileNotFoundError(f"INCORRECT FILE PATH:\n- PROVIDED: {sys.argv[1]}")
    
    # LEXER
    lexer = AJSONLexer()
    token_str = lexer.tokenize(file)

    # PARSER
    parser = AJSONParser()
    return parser.parse(token_str)


if __name__ == "__main__":
    main()