"""
Universe IDE - Stream Module

Data streaming.
"""

from typing import Any, Callable, Dict, List
from collections import deque


# ============================================================================
# STREAM
# ============================================================================

class Stream:
    """Data stream"""
    
    def __init__(self, name: str):
        self.name = name
        self.handlers = []
        self.buffer = deque(maxlen=1000)
        
    def write(self, data: Any):
        self.buffer.append(data)
        for handler in self.handlers:
            handler(data)
            
    def read(self) -> List:
        return list(self.buffer)
        
    def on_data(self, handler: Callable):
        self.handlers.append(handler)


# Global
_stream = None

def get_stream(name: str = "default") -> Stream:
    global _stream
    if _stream is None:
        _stream = Stream(name)
    return _stream


__all__ = ["Stream", "get_stream"]