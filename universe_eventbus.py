"""
Universe IDE - Event Bus Module

Event bus for event-driven architecture.
"""

from typing import Any, Callable, Dict, List
from collections import defaultdict
import time


# ============================================================================
# EVENT
# ============================================================================

class Event:
    """Event"""
    
    def __init__(self, event_type: str, data: Any):
        self.event_type = event_type
        self.data = data
        self.timestamp = time.time()


# ============================================================================
# EVENT BUS
# ============================================================================

class EventBus:
    """Event bus"""
    
    def __init__(self):
        self.handlers = defaultdict(list)
        
    def subscribe(self, event_type: str, handler: Callable):
        self.handlers[event_type].append(handler)
        
    def publish(self, event: Event):
        for handler in self.handlers[event.event_type]:
            handler(event)
            
    def unsubscribe(self, event_type: str, handler: Callable):
        if handler in self.handlers[event_type]:
            self.handlers[event_type].remove(handler)


# Global
_bus = None

def get_event_bus() -> EventBus:
    global _bus
    if _bus is None:
        _bus = EventBus()
    return _bus


__all__ = ["Event", "EventBus", "get_event_bus"]