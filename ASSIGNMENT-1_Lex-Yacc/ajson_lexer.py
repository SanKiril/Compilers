from decimal import Decimal
from typing import List, TextIO
import ply.lex as lex


# DEFINE RESERVED TOKENS
reserved = {
    "TR": "TR",
    "FL": "FL",
    "NULL": "NULL"
}

# DEFINE TOKENS
tokens = [
    "NUMBER",
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
    "SEPARATOR_FIELDS",
    "SEPARATOR_INSTANCES",
    "COMPARATOR"
] + list(reserved.values())


# RECOGNIZE TOKENS
t_BLOCK_START = r'\{'
t_BLOCK_END = r'\}'
t_SEPARATOR_FIELDS = r'\:'
t_SEPARATOR_INSTANCES = r'\,'
t_COMPARATOR = r'\=\=|\>\=|\>|\<\=|\<'

def t_SCIENTIFIC(t):
    r'\-?([1-9]\d*|0)?(\.\d+)?[eE]\-?([1-9]\d*|0)'
    t.value = Decimal(t.value)
    t.type = "NUMBER"
    return t

def t_REAL(t):
    r'\-?([1-9]\d*|0)?\.\d+'
    t.value = float(t.value)
    t.type = "NUMBER"
    return t

def t_HEXADECIMAL(t):
    r'0[xX][0-9a-fA-F]+'
    t.value = int(t.value, 16)
    t.type = "NUMBER"
    return t

def t_OCTAL(t):
    r'0[0-7]+'
    t.value = int(t.value, 8)
    t.type = "NUMBER"
    return t

def t_BINARY(t):
    r'0[bB][01]+'
    t.value = int(t.value, 2)
    t.type = "NUMBER"
    return t

def t_INTEGER(t):
    r'\-?([1-9]\d*|0)'
    t.value = int(t.value)
    t.type = "NUMBER"
    return t

def t_STRING_EXPLICIT(t):
    r'\"[^\"\n\r]*\"'
    return t

def t_STRING_IMPLICIT(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value.upper(), "STRING_IMPLICIT")
    return t


t_ignore = ' \t'


def t_newline(token):
    r'\n+'
    token.lexer.lineno = token.value.count('\n')

def t_error(token):
    print("[Exit][Lexer] Illegal character", token.value)
    token.lexer.skip(1)


# BUILD THE LEXER
lexer = lex.lex()


# RUN THE LEXER
def tokenize(file: TextIO) -> List[lex.LexToken]:
    lexer.input(file.read())
    return [token for token in lexer]