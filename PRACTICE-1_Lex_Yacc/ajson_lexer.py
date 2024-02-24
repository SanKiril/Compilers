import ply.lex as lex
import sys


reserved = {
    "TR": "TR",
    "FL": "FL",
    "NULL": "NULL"
}


tokens = [
    "STRING_NO_QUOTES",
    "STRING_QUOTES",
    "DELIMITER",
    "COMPARISION"
] + list(reserved.values())


"""
    "NUMBER",
    

def t_NUMBER(token):
    r'\d'
    if '.' in token:
        token.value = float(token.value)
    else:
        token.value = int(token.value)
    return token
"""

def t_STRING_NO_QUOTES(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, "STRING_NO_QUOTES")
    return t

def t_STRING_QUOTES(t):
    r'\"[^\"\n]*\"'
    return t

def t_DELIMITER(t):
    r'\{|\}|\:|\,'
    return t

def t_COMPARISION(t):
    r'\=\=|\>\=|\>|\<\=|\<'
    return t


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
