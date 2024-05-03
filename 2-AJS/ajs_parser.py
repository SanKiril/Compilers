import os
from ply.yacc import yacc
from ajs_lexer import AJSLexer
from ajs_object import AJSObject
from ajs_operator import AJSOperator


class AJSParser:
    def __init__(self):
        self.parser = yacc(module=self)
        self.__symbols = {}
        self.__functions = {}
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
        p[0] = p[2]
    
    def p_declaration_content(self, p):
        """
        declaration_content : item ',' declaration_content
            | item
        """
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]
    
    def p_item(self, p):
        """
        item : STRING_IMPLICIT ':' STRING_IMPLICIT
            | STRING_IMPLICIT
        """
        if p[1] in self.__registers:
            raise ValueError(f"[ERROR][SEMANTIC]: Variable already declared: {p[1]}")
        elif p[1] in self.__symbols:
            raise ValueError(f"[ERROR][SEMANTIC]: Variable name can not be a type name: {p[1]}")
        if len(p) == 4:
            if p[3] not in self.__symbols:
                raise ValueError(f"[ERROR][SEMANTIC]: Type not declared: {p[3]}")
            self.__registers[p[1]] = AJSObject(p[3], None)
        else:
            self.__registers[p[1]] = AJSObject("NULL", None)
        p[0] = p[1]
    
    def p_declaration_assignment(self, p):
        """
        assignment : declaration ASSIGN assignment_content
        """
        for item in p[1]:
            if p[3].type == "NULL":  # null assignment
                if self.__registers[item].type in self.__symbols:
                    p[3].type = self.__registers[item].type  # preserve type
                else:
                    p[3].type = "NULL"
            elif p[3].type == "OBJECT":  # object assignment
                if self.__registers[item].type not in self.__symbols:
                    raise ValueError(f"[ERROR][SEMANTIC]: Variable is not declared as an object: {item}")
                p[3].type = self.__registers[item].type  # assign object type
                self.__type_structure(p[3])  # check object type compatibility
            elif p[3].type in self.__symbols:  # object variable assignment
                if self.__registers[item].type != p[3].type:
                    raise ValueError(f"[ERROR][SEMANTIC]: Variable must be a compatible object: {item}")
            else:  # other expressions
                if self.__registers[item].type in self.__symbols:
                    raise ValueError(f"[ERROR][SEMANTIC]: Variable value must be an object: {item}")
            self.__registers[item] = p[3]
    
    def p_assignment(self, p):
        """
        assignment : STRING_IMPLICIT ASSIGN assignment_content
        """
        if p[1] not in self.__registers:
            raise ValueError(f"[ERROR][SEMANTIC]: Variable not declared: {p[1]}")
        if p[3].type == "NULL":  # null assignment
            if self.__registers[p[1]].type in self.__symbols:
                p[3].type = self.__registers[p[1]].type  # preserve type
        elif p[3].type == "OBJECT":  # object assignment
            if self.__registers[p[1]].type not in self.__symbols:
                raise ValueError(f"[ERROR][SEMANTIC]: Variable is not declared as an object: {p[1]}")
            p[3].type = self.__registers[p[1]].type  # assign object type
            self.__type_structure(p[3])  # check object type compatibility
        elif p[3].type in self.__symbols:  # object variable assignment
            if self.__registers[p[1]].type != p[3].type:
                raise ValueError(f"[ERROR][SEMANTIC]: Variable must be a compatible object: {p[1]}")
        else:  # other expressions
            if self.__registers[p[1]].type in self.__symbols:
                raise ValueError(f"[ERROR][SEMANTIC]: Variable value must be an object: {p[1]}")
        self.__registers[p[1]] = p[3]
    
    def p_object_call_assignment(self, p):
        """
        assignment : object_call ASSIGN assignment_content
        """
        if p[3].type == "OBJECT":  # object assignment
            if p[1].type not in self.__symbols:
                raise ValueError(f"[ERROR][SEMANTIC]: Object attribute is not declared as an object: {p[1].type}")
            p[3].type = p[1].type  # assign object type
            self.__type_structure(p[3])  # check object type compatibility
        else:  # other expressions
            if p[3].type != p[1].type:  # object attribute type can not be changed
                raise ValueError(f"[ERROR][SEMANTIC]: Invalid type for object attribute: {p[3].type} != {p[1].type}")
        p[1].value = p[3].value
    
    def p_assignment_content(self, p):
        """
        assignment_content : expression
            | object
        """
        p[0] = p[1]
    
    def p_definition(self, p):
        """
        definition : TYPE STRING_IMPLICIT ASSIGN definition_object
        """
        if p[2] in self.__symbols:
            raise ValueError(f"[ERROR][SEMANTIC]: Type already defined: {p[2]}")
        self.__symbols[p[2]] = AJSObject(p[2], p[4])
    
    def p_definition_object(self, p):
        """
        definition_object : '{' definition_object_content '}'
        """
        p[0] = p[2]
    
    def p_definition_object_content(self, p):
        """
        definition_object_content : definition_object_item ',' definition_object_content
            | definition_object_item
            | definition_object_item ','
        """
        p[0] = p[1]
        if len(p) == 4:
            p[0].update(p[3])
    
    def p_definition_object_item(self, p):
        """
        definition_object_item : key ':' type
        """
        p[0] = {p[1]: p[3]}
    
    def p_object(self, p):
        """
        object : '{' object_content '}'
        """
        p[0] = AJSObject("OBJECT", p[2])
    
    def p_object_content(self, p):
        """
        object_content : object_item ',' object_content
            | object_item
            | object_item ','
        """
        p[0] = p[1]
        if len(p) == 4:
            p[0].update(p[3])

    def p_object_item(self, p):
        """
        object_item : key ':' assignment_content
        """
        p[0] = {p[1]: p[3]}
    
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
        """
        p[0] = p[1].upper()
    
    def p_object_type(self, p):
        """
        type : STRING_IMPLICIT
        """
        if p[1] not in self.__symbols:
            raise ValueError(f"[ERROR][SEMANTIC]: Type not defined: {p[1]}")
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
        function : FUNCTION function_head '{' block_body RETURN expression ';' '}'
        """
        if p[6].type != self.__functions[p[2][0]].type:
            raise ValueError(f"[ERROR][SEMANTIC]: Function return type mismatch: {p[6].type} != {self.__functions[p[2][0]].type}")
            del self.__functions[p[2][0]]
        for key in self.__functions[p[2][0]].value:
            if key in p[2][1]:
                self.__registers[key] = p[2][1][key]  # restore conflicting global variables
            else:
                del self.__registers[key]  # delete local variables
    
    def p_function_head(self, p):
        """
        function_head : STRING_IMPLICIT '(' argument_list ')' ':' type
        """
        p[0] = (p[1], p[3][1])  # (name, conflicting global variables)
        self.__functions[p[1]] = AJSObject(p[6], p[3][0])
    
    def p_argument_list(self, p):
        """
        argument_list : argument_list_nonempty
            | empty
        """
        p[0] = ({},{}) if p[1] is None else (p[1],{})  # (local variables, conflicting global variables)
        for key in p[0][0]:
            if key in p[0][1]:
                p[0][1].update({key: self.__registers[key]})  # save conflicting global variable
            else:
                self.__registers[key] = AJSObject(p[0][0][key], None)  # use local variable
    
    def p_argument_list_nonempty(self, p):
        """
        argument_list_nonempty : STRING_IMPLICIT ':' type ',' argument_list_nonempty
            | STRING_IMPLICIT ':' type
        """
        p[0] = {p[1]: p[3]}
        if len(p) == 6:
            p[0].update(p[5])
    
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
        if p[1] in self.__registers:
            p[0] = self.__registers[p[1]]
        else:
            raise ValueError(f"[ERROR][SEMANTIC]: Variable not declared: {p[1]}")
    
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
        if p[1] not in self.__functions:
            raise ValueError(f"[ERROR][SEMANTIC]: Function not declared: {p[1]}")
        if len(p[3]) != len(self.__functions[p[1]].value.keys()):
            raise ValueError(f"[ERROR][SEMANTIC]: Incorrect number of arguments for function: {p[1]}")
        for argument in self.__functions[p[1]].value:
            if p[3][0].type != self.__functions[p[1]].value[argument]:
                raise ValueError(f"[ERROR][SEMANTIC]: Incorrect argument type for function: {p[3][0].type} is not the correct type for {argument}")
            del p[3][0]
        p[0] = AJSObject(self.__functions[p[1]].type, None)
    
    def p_function_call_list(self, p):
        """
        function_call_list : function_call_list_nonempty
            | empty
        """
        p[0] = [] if p[1] is None else p[1]
    
    def p_function_call_list_nonempty(self, p):
        """
        function_call_list_nonempty : expression ',' function_call_list_nonempty
            | expression
        """
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]
    
    def p_object_call(self, p):
        """
        object_call : STRING_IMPLICIT object_attribute_list
        """
        if p[1] not in self.__registers:
            raise ValueError(f"[ERROR][SEMANTIC]: Variable not declared: {p[1]}")
        try:
            attribute = self.__registers[p[1]]
            for key in p[2]:
                if isinstance(attribute.value, dict):
                    attribute = attribute.value
                attribute = attribute[key]
            p[0] = attribute
        except (KeyError, TypeError):
            raise ValueError(f"[ERROR][SEMANTIC]: Incorrect object structure: {p[1]}")
    
    def p_object_attribute_list(self, p):
        """
        object_attribute_list : '[' STRING_EXPLICIT ']' object_attribute_list
            | '.' STRING_IMPLICIT object_attribute_list
        """
        if len(p) == 5:
            p[0] = [p[2]] + p[4]
        else:
            p[0] = [p[2]] + p[3]
    
    def p_object_attribute(self, p):
        """
        object_attribute_list : '[' STRING_EXPLICIT ']'
            | '.' STRING_IMPLICIT
        """
        p[0] = [p[2]]

    def p_empty(self, p):
        """
        empty :
        """
        pass
    
    # AUXILAR METHODS
    def __type_structure(self, object: AJSObject):
        # length
        if len(self.__symbols[object.type].value.keys()) != len(object.value.keys()):
            raise ValueError(f"[ERROR][SEMANTIC]: Incorrect object structure: {object.type}")
        # object items
        for key in object.value:
            try:
                # object item type
                if object.value[key].type == "OBJECT":
                    object.value[key].type = self.__symbols[object.type].value[key]
                    self.__type_structure(object.value[key])
                elif self.__symbols[object.type].value[key] != object.value[key].type:
                    raise ValueError(f"[ERROR][SEMANTIC]: Incorrect object structure: {object.type}")
            except KeyError:
                raise ValueError(f"[ERROR][SEMANTIC]: Incorrect object structure: {object.type}")

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
        
        # symbols output file
        with open("./output/" + os.path.splitext(os.path.basename(file_path))[0] + ".symbol", 'w', encoding="UTF-8") as file:
            file.write("\n".join([f"{s}: {self.__symbols[s]}" for s in self.__symbols]))
            file.write("\n".join([f"{f}: {self.__functions[f]}" for f in self.__functions]))
        
        # registers output file
        with open("./output/" + os.path.splitext(os.path.basename(file_path))[0] + ".register", 'w', encoding="UTF-8") as file:
            file.write("\n".join([f"{r}: {self.__registers[r]}" for r in self.__registers]))