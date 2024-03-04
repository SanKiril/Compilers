import sys
import os
from ajson_lexer import AJSONLexer
from ajson_parser import AJSONParser


def main():
    # CHECK ARGUMENT NUMBER
    if len(sys.argv) != 2:
        raise ValueError(f"INCORRECT ARGUMENT NUMBER:\n- PROVIDED: {len(sys.argv)}\n- EXPECTED: 2\n# USAGE: python3 ./main.py <file_path>.ajson")
    
    # CHECK FILE EXTENSION
    if os.path.splitext(sys.argv[1])[1] != ".ajson":
        raise ValueError(f"INCORRECT FILE EXTENSION:\n- PROVIDED: {os.path.splitext(sys.argv[1])[1]}\n- EXPECTED: .ajson")

    # OPEN <file_path>.ajson
    try:
        with open(sys.argv[1], 'r', encoding="UTF-8") as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"FILE PATH NOT EXIST:\n- PROVIDED: {sys.argv[1]}")
    
    # LEXER
    lexer = AJSONLexer()
    token_str = lexer.tokenize(data)

    # PARSER
    parser = AJSONParser()
    return parser.parse(data)


if __name__ == "__main__":
    main()