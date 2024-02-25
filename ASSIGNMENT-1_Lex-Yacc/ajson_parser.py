import ply.yacc as yacc
from ajson_lexer import tokens


# DEFINE PRODUCTION RULES
def p_file():
    """
    file ::= BLOCK_START content BLOCK_END
    """
    p[0] = p[2]


# BUILD THE PARSER
parser = yacc.yacc()


# RUN THE PARSER
def parse(token_list: list):
    return parser.parse(token_list)