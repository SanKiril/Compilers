import os
from decimal import Decimal
import ply.lex as lex


class AJSLexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)
    
    # DEFINE LITERALS
    literals = ['{', '}', '(', ')', '[', ']', ':', ',', ';']
    
    # DEFINE RESERVED TOKENS
    reserved = {
        "tr": True,
        "fl": False,
        "let": "let",
        "int": "int",
        "float": "float",
        "character": "character",
        "while": "while",
        "boolean": "boolean",
        "function": "function",
        "return": "return",
        "type": "type",
        "if": "if",
        "else": "else",
        "null": None
    }
    
    # DEFINE TOKENS
    tokens = [
        "SCIENTIFIC",
        "REAL",
        "HEXADECIMAL",
        "OCTAL",
        "BINARY",
        "INTEGER",
        "STRING_EXPLICIT",
        "STRING_IMPLICIT",
        "COMPARATOR"
    ] + list(reserved.keys())
    
    # RECOGNIZE TOKENS
    t_COMPARATOR = r'\=\=|\>\=|\>|\<\=|\<'

    def t_SCIENTIFIC(self, t):
        r'\-?([1-9]\d*|0)?(\.\d+)?[eE]\-?([1-9]\d*|0)'
        t.value = Decimal(t.value)
        return t

    def t_REAL(self, t):
        r'\-?([1-9]\d*|0)?\.\d+'
        t.value = float(t.value)
        return t

    def t_HEXADECIMAL(self, t):
        r'0[xX][0-9a-fA-F]+'
        t.value = int(t.value, 16)
        return t

    def t_OCTAL(self, t):
        r'0[0-7]+'
        t.value = int(t.value, 8)
        return t

    def t_BINARY(self, t):
        r'0[bB][01]+'
        t.value = int(t.value, 2)
        return t

    def t_INTEGER(self, t):
        r'\-?([1-9]\d*|0)'
        t.value = int(t.value)
        return t

    def t_STRING_EXPLICIT(self, t):
        r'\"[^\"\n\r]*\"'
        t.value = t.value[1:-1]
        return t

    def t_STRING_IMPLICIT(self, t):
        r'[a-zA-Z_]\w*'
        upper_value = t.value.upper()
        if upper_value in self.reserved:
            t.type = upper_value
            t.value = self.reserved[upper_value]
        return t

    # INPUT BEHAVIOR
    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n|\r\n?'
        t.lexer.lineno = t.value.count(os.linesep)

    # ERROR HANDLING
    def t_error(self, t):
        raise ValueError(f"[ERROR][LEXER]: Illegal character:\n"
            f"# PROVIDED: {t.value[0]}")

    # RUN
    def tokenize(self, file_path: str):
        # open file
        try:
            with open(file_path, 'r', encoding="UTF-8") as file:
                data = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"FILE PATH NOT EXIST:\n"
                f"# PROVIDED: {sys.argv[1]}")
        
        # tokenize
        self.lexer.input(data)
        
        # output directory
        if not os.path.exists("./output/"):
            os.makedirs("./output/")

        # output file
        with open(os.path.splitext(os.path.basename(sys.argv[1]))[0] + ".lexer", 'w', encoding="UTF-8") as file:
            file.write(data)