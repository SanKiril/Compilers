import os
import re
from decimal import Decimal
from ply.lex import TOKEN
import ply.lex as lex


class AJSLexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)
    
    # DEFINE LITERALS
    literals = ['{', '}', '(', ')', '[', ']', ':', ',', ';']
    
    # DEFINE RESERVED TOKENS
    reserved = {
        "TR": True,
        "FL": False,
        "LET": "let",
        "INT": "int",
        "FLOAT": "float",
        "CHARACTER": "character",
        "WHILE": "while",
        "BOOLEAN": "boolean",
        "FUNCTION": "function",
        "RETURN": "return",
        "TYPE": "type",
        "IF": "if",
        "ELSE": "else",
        "NULL": None
    }
    
    # DEFINE TOKENS
    tokens = [
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "NOT",
        "AND",
        "OR",
        "LT",
        "LE",
        "EQ",
        "GE",
        "GT",
        "ASSIGN",
        "STRING_EXPLICIT",
        "STRING_IMPLICIT",
        "CHAR",
        "COMMENT",
        "REAL",
        "INTEGER"
    ] + list(reserved.keys())

    # DEFINE COMPLEX PATTERNS
    binary = r'0[bB][01]+'
    octal = r'0[0-7]+'
    hexadecimal = r'0[xX][0-9a-fA-F]+'
    decimal = r'[1-9]\d*|0'
    integer = rf'({binary})|({octal})|({hexadecimal})|({decimal})'
    scientific = rf'(?:(?:(?:{decimal})\.\d*)|(?:\.\d+))[eE](?:{decimal})'
    floating = rf'(?:(?:{decimal})\.\d*)|(?:\.\d+)'
    real = rf'({scientific})|({floating})'
    
    # RECOGNIZE TOKENS
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_TIMES = r'\*'
    t_DIVIDE = r'\/'
    t_NOT = r'\!'
    t_AND = r'\&\&'
    t_OR = r'\|\|'
    t_LE = r'\<\='
    t_LT = r'\<'
    t_EQ = r'\=\='
    t_GE = r'\>\='
    t_GT = r'\>'
    t_ASSIGN = r'\='

    def t_STRING_EXPLICIT(self, t):
        r'\"[^\"\n\r]*\"'
        t.value = t.value[1:-1]
        return t

    def t_STRING_IMPLICIT(self, t):
        r'[a-zA-Z_]\w*'
        if t.value.islower() and t.value.upper() in self.reserved:
            t.type = t.value.upper()
            t.value = self.reserved[t.value.upper()]
        return t

    def t_CHAR(self, t):
        r'\'[\x00-\x7F]\''
        t.value = t.value[1:-1]
        return t

    def t_COMMENT(self, t):
        r'(\/\/.*)|(\/\*(?:(?!\*\/).|\n)*\*\/)'
        pass

    @TOKEN(real)
    def t_REAL(self, t):
        match = re.fullmatch(self.real, t.value)
        if match.group(1):  # arbitrary precision
            t.value = Decimal(match.group(1))
        else:  # single precision
            t.value = float(match.group(2))
        return t

    @TOKEN(integer)
    def t_INTEGER(self, t):
        match = re.fullmatch(self.integer, t.value)
        if match.group(1):  # base 2
            t.value = int(match.group(1), 2)
        elif match.group(2):  # base 8
            t.value = int(match.group(2), 8)
        elif match.group(3):  # base 16
            t.value = int(match.group(3), 16)
        else:  # base 10
            t.value = int(match.group(4))
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
                f"# PROVIDED: {file_path}")
        
        # tokenize
        self.lexer.input(data)
        
        # output directory
        if not os.path.exists("./output/"):
            os.makedirs("./output/")

        # output file
        with open("./output/" + os.path.splitext(os.path.basename(file_path))[0] + ".lexer", 'w', encoding="UTF-8") as file:
            file.write("\n".join([f"{t.type} {t.value}" for t in self.lexer]))