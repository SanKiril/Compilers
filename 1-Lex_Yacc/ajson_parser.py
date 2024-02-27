from typing import List
import ply.yacc as yacc
from ajson_lexer import tokens


class AJSONParser:
    def __init__(self):
        self.parser = yacc.yacc(module=self)

    # DEFINE PRODUCTION RULES
    def p_file(self):
        """
        file ::= BLOCK_START content BLOCK_END
        """
        p[0] = p[2]

    # RUN
    def parse(self, token_list: List[lex.LexToken]):
        return parser.parse(token_list)