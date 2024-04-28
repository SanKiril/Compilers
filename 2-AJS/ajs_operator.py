from typing import Any, List, Union
from ajs_object import AJSObject


class AJSOperator(AJSObject):
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
            "BOOLEAN": "BOOLEAN",
            "NULL": "BOOLEAN"
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

    def __init__(self, type: str, value: Any):
        super().__init__(type, value)
    
    def evaluate(self, operands: List[AJSObject]) -> AJSObject:
        # ERROR HANDLING
        if not isinstance(operands, list):
            raise TypeError(f"INCORRECT TYPE FOR `operands`:\n"
                f"# PROVIDED: {type(operands)}\n"
                f"# EXPECTED: `list`")
        
        for operand in operands:
            if not isinstance(operand, AJSObject):
                raise TypeError(f"INCORRECT TYPE FOR `operand` in `operands`:\n"
                    f"# PROVIDED: {type(operand)}\n"
                    f"# EXPECTED: `AJSObject`")
        
        # unary operators
        if len(operands) == 1:
            try:
                return AJSObject(self.type_map[self.type][operands[0].type], eval(f"{self.value} {operands[0].value}"))
            except KeyError:
                raise ValueError(f"[ERROR][SEMANTIC]: Operaion not supported: {self.value} {operands[0].value}")
        # binary operators
        else:
            try:
                return AJSObject(self.__common_type(operands), eval(f"{operands[0].value} {self.value} {operands[1].value}"))
            except KeyError:
                raise ValueError(f"[ERROR][SEMANTIC]: Operaion not supported: {operands[0].value} {self.value} {operands[1].value}")
    
    def __common_type(self, operands: List[AJSObject]) -> str:
        try:
            first_retype = self.type_map[self.type][operands[0].type]
            second_retype = self.type_map[self.type][operands[1].type]
            if self.type_conversions.index(first_retype) >= self.type_conversions.index(second_retype):
                self.__type_cast(operands[0].type, operands[1])
                return operands[0].type
            else:
                self.__type_cast(operands[1].type, operands[0])
                return operands[1].type
        except ValueError:
            return first_retype  # == second_retype
    
    def __type_cast(self, type: str, operand: AJSObject):
        if type == "FLOAT":
            operand.value = float(operand.value)
        if type == "INT":
            operand.value = int(operand.value)
