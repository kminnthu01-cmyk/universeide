"""
Universe IDE - Event Streaming

Real-time event processing with pub/sub.
"""

import asyncio
import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# EVENT TYPES
# ============================================================================

class EventType(Enum):
    """Event types"""
    AGENT_CREATED = "agent.created"
    AGENT_COMPLETED = "agent.completed"
    MESSAGE_SENT = "message.sent"
    MESSAGE_RECEIVED = "message.received"
    TASK_QUEUED = "task.queued"
    TASK_COMPLETED = "task.completed"
    SYSTEM_ERROR = "system.error"
    USER_ACTION = "user.action"


@dataclass
class Event:
    """Event"""
    id: str
    type: EventType
    data: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""


# ============================================================================
# EVENT BUS
# ============================================================================

class EventBus:
    """Event pub/sub bus"""
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = defaultdict(list)
        self._events: List[Event] = []
        self._max_events = 1000
        
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe to event"""
        self._subscribers[event_type].append(handler)
        
    def unsubscribe(self, event_type: EventType, handler: Callable):
        """Unsubscribe"""
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
            
    async def publish(self, event: Event):
        """Publish event"""
        # Store event
        self._events.append(event)
        if len(self._events) > self._max_events:
            self._events = self._events[-self._max_events:]
            
        # Notify subscribers
        handlers = self._subscribers.get(event.type, [])
        tasks = [h(event) for h in handlers]
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
    def get_events(self, event_type: EventType = None, limit: int = 100) -> List[Event]:
        """Get events"""
        if event_type:
            return [e for e in self._events if e.type == event_type][-limit:]
        return self._events[-limit:]


# ============================================================================
# EVENT QUEUE
# ============================================================================

class EventQueue:
    """Async event queue"""
    
    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        
    async def push(self, event: Event):
        """Push event"""
        await self._queue.put(event)
        
    async def pop(self) -> Event:
        """Pop event"""
        return await self._queue.get()
        
    def qsize(self) -> int:
        """Queue size"""
        return self._queue.qsize()
        
    async def process(self, handler: Callable):
        """Process events"""
        self._running = True
        
        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await handler(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error: {e}")
                
    def stop(self):
        """Stop processing"""
        self._running = False


# ============================================================================
# EVENT LOG
# ============================================================================

class EventLog:
    """Persistent event log"""
    
    def __init__(self, filename: str = "universe_events.jsonl"):
        self.filename = filename
        
    def append(self, event: Event):
        """Append to log"""
        with open(self.filename, "a") as f:
            data = {
                "id": event.id,
                "type": event.type.value,
                "data": event.data,
                "timestamp": event.timestamp.isoformat(),
                "source": event.source,
            }
            f.write(json.dumps(data) + "\n")
            
    def read(self, limit: int = 100) -> List[Event]:
        """Read events"""
        events = []
        
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    if len(events) >= limit:
                        break
                    data = json.loads(line.strip())
                    event = Event(
                        id=data["id"],
                        type=EventType(data["type"]),
                        data=data.get("data", {}),
                        source=data.get("source", ""),
                    )
                    events.append(event)
        except FileNotFoundError:
            pass
            
        return events


# ============================================================================
# EVENT STREAMS
# ============================================================================

class EventStreamer:
    """Real-time event streamer"""
    
    def __init__(self):
        self.bus = EventBus()
        self.queue = EventQueue()
        
    async def emit(self, event_type: EventType, data: dict, source: str = ""):
        """Emit event"""
        import uuid
        event = Event(
            id=uuid.uuid4().hex[:16],
            type=event_type,
            data=data,
            source=source,
        )
        
        await self.bus.publish(event)
        await self.queue.push(event)
        
    def on(self, event_type: EventType, handler: Callable):
        """Register handler"""
        self.bus.subscribe(event_type, handler)


# Global
_streamer = None

def get_streamer() -> EventStreamer:
    """Get event streamer"""
    global _streamer
    if _streamer is None:
        _streamer = EventStreamer()
    return _streamer


__all__ = [
    "EventType",
    "Event",
    "EventBus",
    "EventQueue",
    "EventLog",
    "EventStreamer",
    "get_streamer",
]