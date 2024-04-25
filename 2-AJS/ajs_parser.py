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
    
    def p_statement(self, p):
        """
        statement : declaration ';'
            | assignment ';'
            | definition ';'
            | expression ';'
        """
        print("statement", p[1])
    
    def p_block(self, p):
        """
        block : simple_block
            | function
        """
    
    def p_simple_block(self, p):
        """
        simple_block : if_conditional
            | while_loop
        """
    
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
    
    def p_definition(self, p):
        """
        definition : TYPE STRING_IMPLICIT ASSIGN definition_object
        """
    
    def p_definition_object(self, p):
        """
        definition_object : '{' definition_object_content '}'
        """
    
    def p_definition_object_content(self, p):
        """
        definition_object_content : definition_object_item ',' definition_object_content
            | definition_object_item
            | definition_object_item ','
        """
    
    def p_definition_object_item(self, p):
        """
        definition_object_item : key ':' type
        """
    
    def p_object(self, p):
        """
        object : '{' object_content '}'
        """
    
    def p_object_content(self, p):
        """
        object_content : object_item ',' object_content
            | object_item
            | object_item ','
        """

    def p_object_item(self, p):
        """
        object_item : key ':' assignment_content
        """
    
    def p_key(self, p):
        """
        key : STRING_EXPLICIT
            | STRING_IMPLICIT
        """
    
    def p_type(self, p):
        """
        type : INT
            | FLOAT
            | CHARACTER
            | BOOLEAN
            | STRING_IMPLICIT
        """
    
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
            | expression PLUS expression
        """
        if len(p) == 3:
            p[1] = AJSOperator("PLUS", p[1])
            p[0] = p[1].evaluate([p[2]])
        else:
            p[2] = AJSOperator("PLUS", p[2])
            p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_minus(self, p):
        """
        expression : MINUS expression %prec UMINUS
            | expression MINUS expression
        """
        if len(p) == 3:
            p[1] = AJSOperator("MINUS", p[1])
            p[0] = p[1].evaluate([p[2]])
        else:
            p[2] = AJSOperator("MINUS", p[2])
            p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_not(self, p):
        """
        expression : NOT expression
        """
        p[1] = AJSOperator("NOT", p[1])
        p[0] = p[1].evaluate([p[2]])

    def p_times(self, p):
        """
        expression : expression TIMES expression
        """
        p[2] = AJSOperator("TIMES", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_divide(self, p):
        """
        expression : expression DIVIDE expression
        """
        p[2] = AJSOperator("DIVIDE", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_and(self, p):
        """
        expression : expression AND expression
        """
        p[2] = AJSOperator("AND", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_or(self, p):
        """
        expression : expression OR expression
        """
        p[2] = AJSOperator("OR", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_lt(self, p):
        """
        expression : expression LT expression
        """
        p[2] = AJSOperator("LT", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_le(self, p):
        """
        expression : expression LE expression
        """
        p[2] = AJSOperator("LE", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_eq(self, p):
        """
        expression : expression EQ expression
        """
        p[2] = AJSOperator("EQ", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_ge(self, p):
        """
        expression : expression GE expression
        """
        p[2] = AJSOperator("GE", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])
    
    def p_gt(self, p):
        """
        expression : expression GT expression
        """
        p[2] = AJSOperator("GT", p[2])
        p[0] = p[2].evaluate([p[1], p[3]])

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
        self.parser.parse(data)

        # output directory
        if not os.path.exists("./output/"):
            os.makedirs("./output/")
        
        # output file
