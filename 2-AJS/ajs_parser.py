import os
from ply.yacc import yacc
from ajs_lexer import AJSLexer
from ajs_object import AJSObject
from ajs_operator import AJSOperator


class AJSParser:
    def __init__(self):
        self.parser = yacc(module=self)
        self.__symbols = {}
        self.__registers = {}

    tokens = AJSLexer().tokens

    # DEFINE TOKEN PRECEDENCE
    precedence = (
        ("nonassoc", "STRING_IMPLICIT"),
        ("right", "ASSIGN"),
        ("left", "OR", "AND"),
        ("nonassoc", "LE", "LT", "EQ", "GE", "GT"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "UPLUS", "UMINUS", "NOT"),
    )

    # DEFINE PRODUCTION RULES
    def p_file(self, p):
        """
        file : statement file
            | block file
            | empty
        """
        p[0] = {} if p[1] is None else p[1]
    
    def p_statement(self, p):
        """
        statement : declaration ';'
            | assignment ';'
            | definition ';'
            | expression ';'
        """
        p[0] = p[1]
    
    def p_block(self, p):
        """
        block : simple_block
            | function
        """
        p[0] = p[1]
    
    def p_simple_block(self, p):
        """
        simple_block : if_conditional
            | while_loop
        """
        p[0] = p[1]
    
    def p_block_body(self, p):
        """
        block_body : block_body_nonempty
            | empty
        """
    
    def p_block_body_nonempty(self, p):
        """
        block_body_nonempty : statement block_body_nonempty
            | simple_block block_body_nonempty
            | statement
            | simple_block
        """

    def p_declaration(self, p):
        """
        declaration : LET declaration_content
        """
        p[0] = p[2]
    
    def p_declaration_content(self, p):
        """
        declaration_content : item ',' declaration_content
            | item
        """
    
    def p_item(self, p):
        """
        item : STRING_IMPLICIT ':' STRING_IMPLICIT
            | STRING_IMPLICIT
        """
        p[0] = p[1]
    
    def p_assignment(self, p):
        """
        assignment : declaration ASSIGN assignment_content
            | STRING_IMPLICIT ASSIGN assignment_content
        """
    
    def p_assignment_content(self, p):
        """
        assignment_content : expression
            | object
        """
        p[0] = p[1]
    
    def p_definition(self, p):
        """
        definition : TYPE STRING_IMPLICIT ASSIGN object
        """
    
    def p_object(self, p):
        """
        object : '{' object_content '}'
        """
        p[0] = p[2]
    
    def p_object_content(self, p):
        """
        object_content : object_item ',' object_content
            | object_item
            | empty
        """

    def p_object_item(self, p):
        """
        object_item : key ':' basic_type
            | key ':' expression
        """
    
    def p_key(self, p):
        """
        key : STRING_EXPLICIT
            | STRING_IMPLICIT
        """
        p[0] = p[1]
    
    def p_type(self, p):
        """
        type : basic_type
            | STRING_IMPLICIT
        """
        p[0] = p[1]
    
    def p_basic_type(self, p):
        """
        basic_type : INT
            | FLOAT
            | CHARACTER
            | BOOLEAN
        """
        p[0] = p[1]
    
    def p_if_conditional(self, p):
        """
        if_conditional : IF '(' expression ')' '{' block_body_nonempty '}'
            | IF '(' expression ')' '{' block_body_nonempty '}' ELSE '{' block_body_nonempty '}'
        """
    
    def p_while_loop(self, p):
        """
        while_loop : WHILE '(' expression ')' '{' block_body_nonempty '}'
        """
    
    def p_function(self, p):
        """
        function : FUNCTION STRING_IMPLICIT '(' argument_list ')' ':' type '{' block_body RETURN expression ';' '}'
        """
    
    def p_argument_list(self, p):
        """
        argument_list : argument_list_nonempty
            | empty
        """
    
    def p_argument_list_nonempty(self, p):
        """
        argument_list_nonempty : STRING_IMPLICIT ':' type ',' argument_list_nonempty
            | STRING_IMPLICIT ':' type
        """
    
    def p_expression(self, p):
        """
        expression : '(' expression ')'
            | function_call
            | object_call
        """
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = p[1]
    
    def p_int(self, p):
        """
        expression : INTEGER
        """
        p[0] = AJSObject("INT", p[1])
    
    def p_float(self, p):
        """
        expression : REAL
        """
        p[0] = AJSObject("FLOAT", p[1])
    
    def p_character(self, p):
        """
        expression : CHAR
        """
        p[0] = AJSObject("CHARACTER", p[1])
    
    def p_boolean(self, p):
        """
        expression : TR
            | FL
        """
        p[0] = AJSObject("BOOLEAN", p[1])
    
    def p_null(self, p):
        """
        expression : NULL
        """
        p[0] = AJSObject("NULL", p[1])
    
    def p_string_implicit(self, p):
        """
        expression : STRING_IMPLICIT
        """
        """
        if p[1] in self.__symbols:
            p[0] = p[1]
        elif p[1] in self.__registers:
            p[0] = p[1]
        else:
            print("ERROR")
        """

    def p_plus(self, p):
        """
        expression : PLUS expression %prec UPLUS
        """
        """
        p[1] = AJSOperator(p[2].type, "PLUS", p[1])
        if not p[1].return_type:
            print("ERROR")
        p[0] = AJSObject(p[1].return_type, eval(f"{p[1].value} {p[2].value}"))
        """
    
    def p_minus(self, p):
        """
        expression : MINUS expression %prec UMINUS
        """
        """
        p[1] = AJSOperator(p[2].type, "MINUS", p[1])
        if not p[1].return_type:
            print("ERROR")
        p[0] = AJSObject(p[1].return_type, eval(f"{p[1].value} {p[2].value}"))
        """
    
    def p_not(self, p):
        """
        expression : NOT expression
        """
        """
        p[1] = AJSOperator(p[2].type, "NOT", p[1])
        if not p[1].return_type:
            print("ERROR")
        p[0] = AJSObject(p[1].return_type, eval(f"{p[1].value} {p[2].value}"))
        """

    def p_binary_expression(self, p):
        """
        expression : expression PLUS expression
            | expression MINUS expression
            | expression TIMES expression
            | expression DIVIDE expression
            | expression AND expression
            | expression OR expression
            | expression LT expression
            | expression LE expression
            | expression EQ expression
            | expression GE expression
            | expression GT expression
        """
        """
        p[2] = AJSOperator([p[1].type, p[3].type], p[2])
        if not p[2].return_type:
            print("ERROR")
        p[0] = AJSObject(p[2].return_type, eval(f"{p[1].value} {p[2].value} {p[3].value}"))
        """

    def p_function_call(self, p):
        """
        function_call : STRING_IMPLICIT '(' function_call_list ')'
        """
    
    def p_function_call_list(self, p):
        """
        function_call_list : function_call_list_nonempty
            | empty
        """
    
    def p_function_call_list_nonempty(self, p):
        """
        function_call_list_nonempty : expression ',' function_call_list_nonempty
            | expression
        """
    
    def p_object_call(self, p):
        """
        object_call : STRING_IMPLICIT object_attribute_list
        """
    
    def p_object_attribute_list(self, p):
        """
        object_attribute_list : '[' STRING_EXPLICIT ']' object_attribute_list
            | '.' STRING_IMPLICIT object_attribute_list
            | '[' STRING_EXPLICIT ']'
            | '.' STRING_IMPLICIT
        """

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
        print(self.parser.parse(data))

        # output directory
        if not os.path.exists("./output/"):
            os.makedirs("./output/")
        
        # output file