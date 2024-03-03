import os
from decimal import Decimal
from typing import List, TextIO
import ply.lex as lex


class AJSONLexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)
    
    # DEFINE RESERVED TOKENS
    reserved = {
        "TR": "TR",
        "FL": "FL",
        "NULL": "NULL"
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
        "BLOCK_START",
        "BLOCK_END",
        "ARRAY_START",
        "ARRAY_END",
        "SEPARATOR_FIELDS",
        "SEPARATOR_INSTANCES",
        "COMPARATOR"
    ] + list(reserved.values())
    
    # RECOGNIZE TOKENS
    t_BLOCK_START = r'\{'
    t_BLOCK_END = r'\}'
    t_ARRAY_START = r'\['
    t_ARRAY_END = r'\]'
    t_SEPARATOR_FIELDS = r'\:'
    t_SEPARATOR_INSTANCES = r'\,'
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
        return t

    def t_STRING_IMPLICIT(self, t):
        r'[a-zA-Z_]\w*'
        t.type = self.reserved.get(t.value.upper(), "STRING_IMPLICIT")
        return t

    # INPUT BEHAVIOR
    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n|\r\n?'
        t.lexer.lineno = t.value.count(os.linesep)

    # ERROR HANDLING
    def t_error(self, t):
        raise ValueError(f"[ERROR][LEXER]: Illegal character:\n- PROVIDED: {t.value[0]}")

    # RUN
    def tokenize(self, file: TextIO) -> List[lex.LexToken]:
        self.lexer.input(file.read())
        return [t.type for t in self.lexer]