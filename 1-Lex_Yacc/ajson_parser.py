from typing import Union
import ply.yacc as yacc
from ajson_lexer import AJSONLexer


class AJSONParser:
    def __init__(self):
        self.parser = yacc.yacc(module=self)

    tokens = AJSONLexer().tokens

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
    def parse(self, data: str) -> str:
        data = self.parser.parse(data)
        output = self.__output(data)
        return None if output is None else output[:-1]
    
    def __output(self, data: Union[dict, None], parent_key=""):
        if data is None:
            return None
        output = ""
        for key, value in data.items():
            if isinstance(value, dict):
                output += self.__output(value, f"{parent_key}.{key}" if parent_key else key)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    output += self.__output(item, f"{parent_key}.{key}.{index}" if parent_key else f"{key}.{index}")
            else:
                if parent_key:
                    output += f"{{ {parent_key}.{key}: {value} }}\n"
                else:
                    output += f"{{ {key}: {value} }}\n"
        return output