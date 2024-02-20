import ply.lex as lex
import sys


reserved = {
    "TR": "TR",
    "FL": "FL",
    "NULL": "NULL"
}


tokens = (
    "NUMBER",
    "STRING",
    "BOOL",
    "NULL"
    "COMPARION",
    "DELIMITER"
) + reserved


def t_NUMBER(token):
    r'\d'
    if '.' in token:
        token.value = float(token.value)
    else:
        token.value = int(token.value)
    return token


def t_STRING(token):
    r'\w'
    return token


def t_BOOL(token):
    r''
    return token


def t_NULL(token):
    r''
    return token


def t_COMPARISION(token):
    r'\=\=|\>\=|\>|\<\=|\<'
    return token


def t_DELIMITER(token):
    r'\{|\}|\:|,'
    return token


t_ignore = ' \t'


def t_newline(token):
    r'\n+'
    token.lexer.lineno = token.value.count('\n')

def t_error(token):
    print("[Exit][Lexer] Illegal character", token.value)
    token.lexer.skip(1)


# build the lexer
lexer = lex.lex()


# execute lexer from a input file
file = open(sys.argv[1])
lexer.input(file.read())
for token in lexer:
    print(token.type, token.value)
