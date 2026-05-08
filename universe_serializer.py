"""
Universe IDE - Serializer Module

Data serialization.
"""

from typing import Any, Dict
import json


# ============================================================================
# SERIALIZER
# ============================================================================

class Serializer:
    """Serializer"""
    
    def __init__(self):
        self.handlers = {"json": json.dumps, "jsonb": json.dumps}
        
    def serialize(self, data: Any, format: str = "json") -> str:
        if format in self.handlers:
            return self.handlers[format](data)
        return str(data)
        
    def deserialize(self, data: str, format: str = "json") -> Any:
        if format == "json":
            return json.loads(data)
        return data


__all__ = ["Serializer"]