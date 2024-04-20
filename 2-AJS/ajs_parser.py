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
            | basic_expression ';'
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
        assignment : declaration ASSIGN expression
            | STRING_IMPLICIT ASSIGN expression
        """
    
    def p_expression(self, p):
        """
        expression : basic_expression
            | object
        """
        p[0] = p[1]
    
    def p_definition(self, p):
        """
        definition : TYPE STRING_IMPLICIT ASSIGN definition_object
        """
    
    def p_definition_object(self, p):
        """
        definition_object : '{' definition_object_content '}'
        """
        p[0] = p[2]
    
    def p_definition_object_content(self, p):
        """
        definition_object_content : definition_object_item ',' definition_object_content
            | definition_object_item
            | empty
        """
    
    def p_definition_object_item(self, p):
        """
        definition_object_item : key ':' type
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
        object_item : key ':' expression
        """
    
    def p_key(self, p):
        """
        key : STRING_EXPLICIT
            | STRING_IMPLICIT
        """
        p[0] = p[1]
    
    def p_type(self, p):
        """
        type : INT
            | FLOAT
            | CHARACTER
            | BOOLEAN
            | STRING_IMPLICIT
        """
        p[0] = p[1]
    
    def p_if_conditional(self, p):
        """
        if_conditional : IF '(' basic_expression ')' '{' block_body_nonempty '}'
            | IF '(' basic_expression ')' '{' block_body_nonempty '}' ELSE '{' block_body_nonempty '}'
        """
    
    def p_while_loop(self, p):
        """
        while_loop : WHILE '(' basic_expression ')' '{' block_body_nonempty '}'
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
    
    def p_basic_expression(self, p):
        """
        basic_expression : '(' basic_expression ')'
            | function_call
            | object_call
        """
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = p[1]
    
    def p_int(self, p):
        """
        basic_expression : INTEGER
        """
        p[0] = AJSObject("INT", p[1])
    
    def p_float(self, p):
        """
        basic_expression : REAL
        """
        p[0] = AJSObject("FLOAT", p[1])
    
    def p_character(self, p):
        """
        basic_expression : CHAR
        """
        p[0] = AJSObject("CHARACTER", p[1])
    
    def p_boolean(self, p):
        """
        basic_expression : TR
            | FL
        """
        p[0] = AJSObject("BOOLEAN", p[1])
    
    def p_null(self, p):
        """
        basic_expression : NULL
        """
        p[0] = AJSObject("NULL", p[1])
    
    def p_string_implicit(self, p):
        """
        basic_expression : STRING_IMPLICIT
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
        basic_expression : PLUS basic_expression %prec UPLUS
        """
        """
        p[1] = AJSOperator(p[2].type, "PLUS", p[1])
        if not p[1].return_type:
            print("ERROR")
        p[0] = AJSObject(p[1].return_type, eval(f"{p[1].value} {p[2].value}"))
        """
    
    def p_minus(self, p):
        """
        basic_expression : MINUS basic_expression %prec UMINUS
        """
        """
        p[1] = AJSOperator(p[2].type, "MINUS", p[1])
        if not p[1].return_type:
            print("ERROR")
        p[0] = AJSObject(p[1].return_type, eval(f"{p[1].value} {p[2].value}"))
        """
    
    def p_not(self, p):
        """
        basic_expression : NOT basic_expression
        """
        """
        p[1] = AJSOperator(p[2].type, "NOT", p[1])
        if not p[1].return_type:
            print("ERROR")
        p[0] = AJSObject(p[1].return_type, eval(f"{p[1].value} {p[2].value}"))
        """

    def p_binary_basic_expression(self, p):
        """
        basic_expression : basic_expression PLUS basic_expression
            | basic_expression MINUS basic_expression
            | basic_expression TIMES basic_expression
            | basic_expression DIVIDE basic_expression
            | basic_expression AND basic_expression
            | basic_expression OR basic_expression
            | basic_expression LT basic_expression
            | basic_expression LE basic_expression
            | basic_expression EQ basic_expression
            | basic_expression GE basic_expression
            | basic_expression GT basic_expression
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
        function_call_list_nonempty : basic_expression ',' function_call_list_nonempty
            | basic_expression
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