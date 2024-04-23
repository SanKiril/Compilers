from typing import Any, List, Union
from ajs_lexer import AJSLexer


type_map = {
    "PLUS": {
        "INT": "INT",
        "FLOAT": "FLOAT",
        "CHARACTER": "CHARACTER"
    },
    "MINUS": {
        "INT": "INT",
        "FLOAT": "FLOAT",
        "CHARACTER": "CHARACTER"
    },
    "TIMES": {
        "INT": "INT",
        "FLOAT": "FLOAT"
    },
    "DIVIDE": {
        "INT": "INT",
        "FLOAT": "FLOAT"
    },
    "LE": {
        "INT": "BOOLEAN",
        "FLOAT": "BOOLEAN",
        "CHARACTER": "BOOLEAN"
    },
    "LT": {
        "INT": "BOOLEAN",
        "FLOAT": "BOOLEAN",
        "CHARACTER": "BOOLEAN"
    },
    "GE": {
        "INT": "BOOLEAN",
        "FLOAT": "BOOLEAN",
        "CHARACTER": "BOOLEAN"
    },
    "GT": {
        "INT": "BOOLEAN",
        "FLOAT": "BOOLEAN",
        "CHARACTER": "BOOLEAN"
    },
    "EQ": {
        "INT": "BOOLEAN",
        "FLOAT": "BOOLEAN",
        "CHARACTER": "BOOLEAN",
        "BOOLEAN": "BOOLEAN"
    },
    "AND": {
        "BOOLEAN": "BOOLEAN"
    },
    "OR": {
        "BOOLEAN": "BOOLEAN"
    },
    "NOT": {
        "BOOLEAN": "BOOLEAN"
    }
}

type_conversions = ["CHARACTER", "INT", "FLOAT"]


class AJSOperator:
    def __init__(self, operator_input_type: Union[str, List[str]], operator_type: str, operator_value: Any):
        # ERROR HANDLING
        if not isinstance(operator_input_type, (str, list)):
            raise TypeError(f"INCORRECT TYPE FOR `operator_input_type`:\n"
                f"# PROVIDED: {type(operator_input_type)}\n"
                f"# EXPECTED: `list` || `str`")
        
        if not isinstance(operator_type, str):
            raise TypeError(f"INCORRECT TYPE FOR `operator_type`:\n"
                f"# PROVIDED: {type(operator_type)}\n"
                f"# EXPECTED: `str`")
        
        operator_input_type = list(operator_input_type)
        if not all(item in list(AJSLexer().reserved.keys()) for item in operator_input_type):
            raise ValueError(f"INCORRECT VALUE FOR `operator_input_type`:\n"
                f"# PROVIDED: {operator_input_type}\n"
                f"# EXPECTED: Any of {list(AJSLexer().reserved.keys())}")

        self.type = operator_type
        self.value = operator_value
        self.return_type = self.__map_types(operator_input_type)
    
    def __map_types(self, operator_input_type: List[str]) -> Union[str, None]:
        # unary operators
        if len(operator_input_type) == 1:
            # try to get the type of the input
            try:
                return type_map[self.type][operator_input_type[0]]
            except KeyError:
                return
        # binary operators
        else:
            # try to get the type of the input
            try:
                type_map[self.type][operator_input_type[0]]
                type_map[self.type][operator_input_type[1]]
            except KeyError:
                return