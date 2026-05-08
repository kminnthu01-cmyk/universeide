"""
Universe IDE - Agent Communication System

Inter-agent messaging and communication.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# MESSAGE TYPES
# ============================================================================

class MessageType(Enum):
    """Agent message types"""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    COMMAND = "command"
    RESULT = "result"
    ERROR = "error"


# ============================================================================
# AGENT MESSAGE
# ============================================================================

@dataclass
class AgentMessage:
    """Agent-to-agent message"""
    message_id: str
    from_agent: str
    to_agent: str
    message_type: MessageType
    content: Any
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: str = ""


# ============================================================================
# MESSAGE BUS
# ============================================================================

class MessageBus:
    """
    Agent message bus for inter-agent communication.
    """
    
    def __init__(self):
        self.inbox: dict[str, list[AgentMessage]] = {}
        self.outbox: list[AgentMessage] = []
        self.handlers: dict[str, Callable] = {}
        
    def send(
        self, 
        from_agent: str, 
        to_agent: str, 
        content: Any,
        message_type: MessageType = MessageType.REQUEST
    ) -> str:
        """Send message to agent"""
        import uuid
        msg = AgentMessage(
            message_id=f"msg_{uuid.uuid4().hex[:8]}",
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
        )
        
        if to_agent not in self.inbox:
            self.inbox[to_agent] = []
        self.inbox[to_agent].append(msg)
        
        self.outbox.append(msg)
        
        # Handle if handler registered
        if to_agent in self.handlers:
            self.handlers[to_agent](msg)
            
        return msg.message_id
        
    def broadcast(self, from_agent: str, content: Any):
        """Broadcast to all agents"""
        for agent_id in self.inbox.keys():
            self.send(from_agent, agent_id, content, MessageType.BROADCAST)
            
    def receive(self, agent_id: str) -> list[AgentMessage]:
        """Receive messages"""
        return self.inbox.get(agent_id, [])
        
    def register_handler(self, agent_id: str, handler: Callable):
        """Register message handler"""
        self.handlers[agent_id] = handler
        
    def clear(self, agent_id: str):
        """Clear agent inbox"""
        if agent_id in self.inbox:
            self.inbox[agent_id] = []


# ============================================================================
# AGENT INBOX/OUTBOX
# ============================================================================

class AgentInbox:
    """Per-agent inbox"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.messages: list[AgentMessage] = []
        
    def add(self, message: AgentMessage):
        """Add message"""
        self.messages.append(message)
        
    def get_unread(self) -> list[AgentMessage]:
        """Get unread messages"""
        return [m for m in self.messages if not getattr(m, 'read', False)]
        
    def mark_read(self, message_id: str):
        """Mark as read"""
        for m in self.messages:
            if m.message_id == message_id:
                m.read = True


# ============================================================================
# DISTRIBUTED MESSAGING
# ============================================================================

class DistributedMessageBus(MessageBus):
    """Message bus with distributed support"""
    
    def __init__(self):
        super().__init__()
        self.subscriptions: dict[str, set[str]] = {}
        
    def subscribe(self, agent_id: str, topic: str):
        """Subscribe to topic"""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
        self.subscriptions[topic].add(agent_id)
        
    def publish_to_topic(self, topic: str, content: Any):
        """Publish to topic subscribers"""
        if topic in self.subscriptions:
            for agent_id in self.subscriptions[topic]:
                self.send("system", agent_id, content, MessageType.BROADCAST)


# ============================================================================
# GLOBAL MESSAGE BUS
# ============================================================================

_message_bus = None

def get_message_bus() -> MessageBus:
    """Get global message bus"""
    global _message_bus
    if _message_bus is None:
        _message_bus = MessageBus()
    return _message_bus


__all__ = [
    "MessageType",
    "AgentMessage",
    "MessageBus",
    "AgentInbox",
    "DistributedMessageBus",
    "get_message_bus",
]