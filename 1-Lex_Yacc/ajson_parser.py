from typing import List
import ply.yacc as yacc
from ajson_lexer import AJSONLexer


class AJSONParser:
    def __init__(self):
        self.parser = yacc.yacc(module=self)

    tokens = AJSONLexer().tokens

    # DEFINE PRODUCTION RULES
    def p_file(self):
        """
        file : non_empty_file
            | /* empty */
        """
        p[0] = p[1]

    def p_non_empty_file(self):
        """
        non_empty_file : object
            | object SEPARATOR_INSTANCES non_empty_file
        """
        if len(p) == 4:
            p[0] = [p[1],p[2],p[3]]
        else:
            p[0] = p[1]

    def p_object(self):
        """
        object : BLOCK_START object_content BLOCK_END
        """
        p[0] = [p[1],p[2],p[3]]

    def p_object_content(self):
        """
        object_content : non_empty_object_content
            | /* empty */
        """
        p[0] = p[1]

    def p_non_empty_object_content(self):
        """
        non_empty_object_content : object_instance
            | object_instance SEPARATOR_INSTANCES non_empty_object_content
        """
        if len(p) == 4:
            p[0] = [p[1], p[2], p[3]]
        else:
            p[0] = p[1]

    def p_object_instance(self):
        """
        object_instance : key SEPARATOR_FIELDS value
        """
        p[0] = [p[1], p[2], p[3]]

    def p_key(self):
        """
        key : STRING_EXPLICIT
            | STRING_IMPLICIT
        """
        p[0] = p[1]

    def p_value(self):
        """
        value : array_object
            | comparison
            | object
            | number
            | bool
            | NULL
            | STRING_EXPLICIT
        """
        p[0] = p[1]

    def p_array_object(self):
        """
        array_object : ARRAY_START array_content ARRAY_END
        """
        p[0] = [p[1], p[2], p[3]]

    def p_array_content(self):
        """
        array_content : non_empty_array_content
            | /* empty */
        """
        p[0] = p[1]

    def p_non_empty_array_content(self):
        """
        non_empty_array_content : object
            | object SEPARATOR_INSTANCES non_empty_array_content
        """
        if len(p) == 4:
            p[0] = [p[1], p[2], p[3]]
        else:
            p[0] = p[1]

    def p_comparison(self):
        """
        comparison : number COMPARATOR number
        """
        p[0] = [p[1], p[2], p[3]]

    def p_number(self):
        """
        number : SCIENTIFIC
            | REAL
            | HEXADECIMAL
            | OCTAL
            | BINARY
            | INTEGER
        """
        p[0] = p[1]

    def p_bool(self):
        """
        bool : TR
            | FL
        """
        p[0] = p[1]

    # RUN
    def parse(self, token_list: List[lex.LexToken]):
        return parser.parse(token_list)