"""
Universe IDE - Queue Module

Queue management.
"""

from typing import Any, Dict


# ============================================================================
# QUEUE
# ============================================================================

class Queue:
    """Queue"""
    
    def __init__(self, name: str):
        self.name = name
        self.items = []
        
    def enqueue(self, item: Any):
        self.items.append(item)
        
    def dequeue(self) -> Any:
        if self.items:
            return self.items.pop(0)
        return None


__all__ = ["Queue"]