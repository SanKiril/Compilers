import sys
from ajson_lexer import tokenize
from ajson_parser import parse


def main():
    # CHECK ARGUMENT NUMBER
    if len(sys.argv) != 2:
        raise ValueError(f"INCORRECT ARGUMENT NUMBER:\n- PROVIDED: {len(sys.argv)}\n- EXPECTED: 2\n# USAGE: python3 ./main.py <file_path>.ajson")
    
    # OPEN <file_path>.ajson
    try:
        file = open(sys.argv[1])
    except FileNotFoundError:
        raise FileNotFoundError(f"INCORRECT FILE PATH:\n- PROVIDED: {sys.argv[1]}")
    
    token_list = tokenize(file)  # lexer
    return parse(token_list)  # parser


if __name__ == "__main__":
    main()