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
        ("nonassoc", "STRING_IMPLICIT"),
        ("right", "ASSIGN"),
        ("left", "OR", "AND"),
        ("nonassoc", "LE", "LT", "EQ", "GE", "GT"),
        ("left", "PLUS", "MINUS"),
        ("left", "BINARY"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "UNARY", "NOT"),
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
        block_body : '{' block_body_code '}'
        """
        p[0] = p[2]
    
    def p_block_body_code(self, p):
        """
        block_body_code : statement block_body_code
            | simple_block block_body_code
            | statement
            | simple_block
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
        function : FUNCTION STRING_IMPLICIT '(' argument_list ')' ':' type '{' block_body_code RETURN expression ';' '}'
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
            | expression binary_operator expression %prec BINARY
            | unary_operator expression %prec UNARY
            | INTEGER
            | REAL
            | CHAR
            | TR
            | FL
            | NULL
            | STRING_IMPLICIT
            | function_call
            | object_call
            | object
        """
        if len(p) == 4:
            print(p[1], p[2], p[3])
            p[0] = eval(f"{p[1]} {p[2]} {p[3]}")
            print(p[0])
        if len(p) == 3:
            print(p[1], p[2])
        if len(p) == 2:
            p[0] = p[1]
            print(p[0])
    
    '''
    def p_expression_unary(self, p):
        """
        expression : unary_operator expression %prec UNARY
        """
        if p[1][0] == "logic" and p[2][0] == "boolean":
            p[0] = (p[2][0], eval(f"{p[1][1]}{p[2][1]}"))
        elif p[1][0] == "arithmetic" and (p[2][0] == "int" or p[2][0] == "float" or p[2][0] == "character"):
            p[0] = (p[2][0], eval(f"{p[1][1]}{p[2][1]}"))
        else:
            print("!!!!!!!!!!!!! CANOT APPLY UNARY OPERATION !!!!!!!!!!!!!!!")
    '''

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
        p[0] = p[1]
    
    def p_unary_operator(self, p):
        """
        unary_operator : PLUS %prec UNARY
            | MINUS %prec UNARY
            | NOT
        """
        p[0] = p[1]

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