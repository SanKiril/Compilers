from typing import Union
import ply.yacc as yacc
from ajs_lexer import AJSLexer


class AJSParser:
    def __init__(self):
        self.parser = yacc.yacc(module=self)

    tokens = AJSLexer().tokens

    # DEFINE PRODUCTION RULES
    def p_file(self, p):
        """
        file : object
            | empty
        """
        p[0] = None if p[1] is None else p[1]

    def p_object(self, p):
        """
        object : '{' object_content '}'
        """
        p[0] = p[2]

    def p_object_content(self, p):
        """
        object_content : object_entry ',' object_content
            | object_entry
            | empty
        """
        p[0] = None if p[1] is None else dict([p[1]])
        if len(p) == 4 and p[3] is not None:
            p[0].update(p[3])

    def p_object_entry(self, p):
        """
        object_entry : key ':' value
        """
        p[0] = (p[1], p[3])

    def p_key(self, p):
        """
        key : STRING_EXPLICIT
            | STRING_IMPLICIT
        """
        p[0] = p[1]

    def p_value(self, p):
        """
        value : array
            | object
            | comparison
            | number
            | TR
            | FL
            | NULL
            | STRING_EXPLICIT
        """
        p[0] = p[1]

    def p_array(self, p):
        """
        array : '[' array_content ']'
        """
        p[0] = p[2]

    def p_array_content(self, p):
        """
        array_content : object ',' array_content
            | object
            | empty
        """
        p[0] = [] if p[1] is None else [p[1]]
        if len(p) == 4 and p[3] is not None:
            p[0].extend(p[3])

    def p_comparison(self, p):
        """
        comparison : number COMPARATOR number
        """
        p[0] = eval(f"{p[1]} {p[2]} {p[3]}")

    def p_number(self, p):
        """
        number : SCIENTIFIC
            | REAL
            | HEXADECIMAL
            | OCTAL
            | BINARY
            | INTEGER
        """
        p[0] = p[1]

    def p_empty(self, p):
        """
        empty :
        """
        pass

    # ERROR HANDLING
    def p_error(self, p):
        p_value = None if p is None else p.value
        raise ValueError(f"[ERROR][PARSER]: Not matching production rule:\n"
            f"# PROVIDED: {p_value}")

    # RUN
    def parse(self, file_path: str):
        # open file
        try:
            with open(file_path, 'r', encoding="UTF-8") as file:
                data = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"FILE PATH NOT EXIST:\n"
                f"# PROVIDED: {file_path}")
        
        # parse
        self.parser.parse(data)

        # output directory
        if not os.path.exists("./output/"):
            os.makedirs("./output/")
        
        # output file