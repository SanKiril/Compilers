import os
import ply.yacc as yacc
from ajs_lexer import AJSLexer


class AJSParser:
    def __init__(self):
        self.parser = yacc.yacc(module=self)
        self.__symbols = {}
        self.__registers = {}

    tokens = AJSLexer().tokens

    # DEFINE TOKEN PRECEDENCE
    precedence = (
        #("left", PLUS, MINUS),
        #("left", TIMES, DIVIDE),
        ("nonassoc", "STRING_IMPLICIT"),  # non-associative
        ("right", "ASSIGN"),  # right associative: [OK]: a = (b + c), [NOK]: (a = b) + c
    )

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
        object_item : key ':' type
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
        function : FUNCTION STRING_IMPLICIT '(' argument_list ')' ':' type '{' code RETURN expression ';' '}'
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
            | expression binary_operator expression
            | unary_operator expression
            | term
        """
    
    def p_binary_operator(self, p):
        """
        binary_operator : PLUS
            | MINUS
            | TIMES
            | DIVIDE
            | AND
            | OR
            | LT
            | LE
            | EQ
            | GE
            | GT
        """
    
    def p_unary_operator(self, p):
        """
        unary_operator : PLUS
            | MINUS
            | NOT
        """

    def p_term(self, p):
        """
        term : INTEGER
            | REAL
            | CHAR
            | TR
            | FL
            | STRING_IMPLICIT
            | function_call
            | object_call
            | object
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