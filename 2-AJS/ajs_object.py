from typing import Any


class AJSObject:
    def __init__(self, type: str, value: Any):
        # ERROR HANDLING
        if not isinstance(type, str):
            raise TypeError(f"INCORRECT TYPE FOR `type`:\n"
                f"# PROVIDED: {type(type)}\n"
                f"# EXPECTED: `str`")
        
        self.type = type
        self.value = value
    
    def __str__(self) -> str:
        return f"({self.type}: {self.value})"