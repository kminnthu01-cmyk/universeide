"""
Universe IDE - Streaming System

Real-time agent output streaming.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, AsyncIterator, Callable


# ============================================================================
# STREAM EVENT TYPES
# ============================================================================

class StreamEventType(Enum):
    """Stream event types"""
    TOKEN = "token"
    START = "start"
    END = "end"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    STATUS = "status"
    PROGRESS = "progress"


# ============================================================================
# STREAM EVENT
# ============================================================================

@dataclass
class StreamEvent:
    """Stream event"""
    event_type: StreamEventType
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)
    agent_id: str = ""


# ============================================================================
# STREAM MANAGER
# ============================================================================

class StreamManager:
    """
    Real-time streaming manager.
    """
    
    def __init__(self):
        self.subscribers: dict[str, asyncio.Queue] = {}
        self.handlers: dict[str, Callable] = {}
        
    def subscribe(self, stream_id: str) -> asyncio.Queue:
        """Subscribe to stream"""
        if stream_id not in self.subscribers:
            self.subscribers[stream_id] = asyncio.Queue()
        return self.subscribers[stream_id]
        
    def unsubscribe(self, stream_id: str):
        """Unsubscribe from stream"""
        if stream_id in self.subscribers:
            del self.subscribers[stream_id]
            
    async def publish(self, stream_id: str, event: StreamEvent):
        """Publish event"""
        if stream_id in self.subscribers:
            await self.subscribers[stream_id].put(event)
            
    async def stream_tokens(self, stream_id: str, tokens: list[str]):
        """Stream tokens one by one"""
        await self.publish(stream_id, StreamEvent(
            event_type=StreamEventType.START,
            data={"total": len(tokens)},
        ))
        
        for i, token in enumerate(tokens):
            await self.publish(stream_id, StreamEvent(
                event_type=StreamEventType.TOKEN,
                data={"token": token, "index": i},
            ))
            await asyncio.sleep(0)  # Yield to event loop
            
        await self.publish(stream_id, StreamEvent(
            event_type=StreamEventType.END,
            data={"total": len(tokens)},
        ))
        
    def register_handler(self, stream_id: str, handler: Callable):
        """Register stream handler"""
        self.handlers[stream_id] = handler


# ============================================================================
# ASYNC GENERATOR
# ============================================================================

async def stream_async(
    stream_id: str,
    generator: Callable[[], AsyncIterator[str]]
) -> AsyncIterator[str]:
    """Wrap async generator with streaming"""
    manager = StreamManager()
    queue = manager.subscribe(stream_id)
    
    async def event_writer():
        async for token in generator():
            await manager.publish(stream_id, StreamEvent(
                event_type=StreamEventType.TOKEN,
                data=token,
            ))
            yield token
            
        await manager.publish(stream_id, StreamEvent(
            event_type=StreamEventType.END,
            data={"done": True},
        ))
        
    async for token in event_writer():
        yield token


# ============================================================================
# PROGRESS TRACKER
# ============================================================================

class ProgressTracker:
    """
    Track progress of agent tasks.
    """
    
    def __init__(self, task_id: str, total: int):
        self.task_id = task_id
        self.total = total
        self.current = 0
        
    def update(self, count: int = 1):
        """Update progress"""
        self.current += count
        
    @property
    def percent(self) -> float:
        """Get completion percentage"""
        return (self.current / self.total * 100) if self.total > 0 else 0
        
    @property
    def is_complete(self) -> bool:
        """Check if complete"""
        return self.current >= self.total


# ============================================================================
# EVENT LISTENER
# ============================================================================

class EventListener:
    """Listen to stream events"""
    
    def __init__(self):
        self.callbacks: dict[StreamEventType, list[Callable]] = {
            etype: [] for etype in StreamEventType
        }
        
    def on(self, event_type: StreamEventType, callback: Callable):
        """Register callback"""
        self.callbacks[event_type].append(callback)
        
    async def emit(self, event: StreamEvent):
        """Emit event to callbacks"""
        for callback in self.callbacks[event.event_type]:
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)


# Global
_stream = None

def get_stream_manager() -> StreamManager:
    """Get global stream manager"""
    global _stream
    if _stream is None:
        _stream = StreamManager()
    return _stream


__all__ = [
    "StreamEventType",
    "StreamEvent",
    "StreamManager",
    "stream_async",
    "ProgressTracker",
    "EventListener",
    "get_stream_manager",
]