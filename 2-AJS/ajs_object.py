from typing import Any


class AJSObject:
    def __init__(self, object_type: str, object_value: Any):
        # ERROR HANDLING
        if not isinstance(object_type, str):
            raise TypeError(f"INCORRECT TYPE FOR `object_type`:\n"
                f"# PROVIDED: {type(object_type)}\n"
                f"# EXPECTED: `str`")
        
        self.type = object_type
        self.value = object_value
    
    def __str__(self) -> str:
        return f"({self.type}: {self.value})"