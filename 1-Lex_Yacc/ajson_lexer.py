import os
from decimal import Decimal
import ply.lex as lex


class AJSONLexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)
    
    # DEFINE LITERALS
    literals = ['{', '}', '[', ']', ':', ',']
    
    # DEFINE RESERVED TOKENS
    reserved = {
        "TR": True,
        "FL": False,
        "NULL": None
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
    def tokenize(self, data: str) -> str:
        self.lexer.input(data)
        return "\n".join([f"{t.type} {t.value}" for t in self.lexer])