import os
import ply.yacc as yacc
from ajs_lexer import AJSLexer


class AJSParser:
    def __init__(self):
        self.parser = yacc.yacc(module=self)
        self.__symbols = {}
        self.__registers = {}

    tokens = AJSLexer().tokens

    # DEFINE PRODUCTION RULES
    def p_file(self, p):
        """
        file : code
            | empty
        """
        p[0] = {} if p[1] is None else p[1]
    
    def p_code(self, p):
        """
        code : statement code
            | block code
            | statement
            | block
        """
    
    def p_statement(self, p):
        """
        statement : statement_content ';'
        """
        p[0] = p[1]
    
    def p_statement_content(self, p):
        """
        statement_content : declaration
            | assignment
            | definition
            | expression
        """
        p[0] = p[1]
    
    def p_block(self, p):
        """
        block : if_conditional
            | while_loop
            | function
        """
        p[0] = p[1]
    
    def p_block_body(self, p):
        """
        block_body : '{' code '}'
        """
        p[0] = p[2]
    
    def p_declaration(self, p):
        """
        declaration : LET declaration_content
        """
        p[0] = p[2]
    
    def p_declaration_content(self, p):
        """
        declaration_content : declaration_item ',' declaration_content
            | declaration_item
        """
    
    def p_declaration_item(self, p):
        """
        declaration_item : STRING_IMPLICIT ':' STRING_IMPLICIT | STRING_IMPLICIT
        """
    
    def p_assignment(self, p):
        """
        assignment : declaration '=' expression | STRING_IMPLICIT '=' expression
        """
    
    def p_definition(self, p):
        """
        definition : TYPE STRING_IMPLICIT '=' object
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
        object_item : key ':' type
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
        if_conditional : IF condition block_body
            | IF condition block_body ELSE block_body
        """
    
    def p_while_loop(self, p):
        """
        while_loop : WHILE condition block_body
        """
    
    def p_condition(self, p):
        """
        condition : '(' expression ')'
        """
    
    def p_function(self, p):
        """
        function : FUNCTION STRING_IMPLICIT '(' argument_list ')' ':' type '{' code RETURN expression '}'
        """
    
    def p_argument_list(self, p):
        """
        argument_list : STRING_IMPLICIT ':' STRING_IMPLICIT ',' argument_list
            | STRING_IMPLICIT ':' STRING_IMPLICIT
            | empty
        """
    
    def p_expression(self, p):
        """
        expression : expression binary_operator expression
            | unary_operator expression
            | 
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