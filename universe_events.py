"""
Universe IDE - Webhook & Event System

Event-driven architecture for integrations.
"""

import asyncio
import hashlib
import hmac
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# EVENT TYPES
# ============================================================================

class EventType(Enum):
    """Event types"""
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    AGENT_SPAWNED = "agent.spawned"
    AGENT_DONE = "agent.done"
    ERROR_OCCURRED = "error.occurred"
    HEALTH_CHANGED = "health.changed"


# ============================================================================
# EVENT
# ============================================================================

@dataclass
class Event:
    """An event"""
    id: str
    type: EventType
    timestamp: datetime
    data: dict = field(default_factory=dict)
    source: str = "universe"


# ============================================================================
# WEBHOOK
# ============================================================================

@dataclass
class WebhookConfig:
    """Webhook configuration"""
    url: str
    events: list[EventType]
    secret: Optional[str] = None
    enabled: bool = True


class Webhook:
    """
    Webhook for external integrations.
    """
    
    def __init__(self, config: WebhookConfig):
        self.config = config
        
    def sign_payload(self, payload: str) -> str:
        """Sign webhook payload"""
        if not self.config.secret:
            return ""
        return hmac.new(
            self.config.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
    def send(self, event: Event) -> bool:
        """Send webhook"""
        if not self.config.enabled:
            return False
        if event.type not in self.config.events:
            return False
            
        payload = json.dumps({
            "id": event.id,
            "type": event.type.value,
            "timestamp": event.timestamp.isoformat(),
            "data": event.data,
        })
        
        headers = {
            "Content-Type": "application/json",
            "X-Universe-Signature": self.sign_payload(payload),
        }
        
        # In real implementation, would use requests/aiohttp
        print(f"  Webhook would send to {self.config.url}")
        print(f"  Payload: {payload[:100]}...")
        
        return True


# ============================================================================
# EVENT BUS
# ============================================================================

class EventBus:
    """
    Event bus for internal event handling.
    """
    
    def __init__(self):
        self.subscribers: dict[EventType, list[Callable]] = {}
        self.webhooks: list[Webhook] = []
        self.event_history: list[Event] = []
        
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe to event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        
    def unsubscribe(self, event_type: EventType, handler: Callable):
        """Unsubscribe from event"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(handler)
            
    def add_webhook(self, webhook: Webhook):
        """Add webhook"""
        self.webhooks.append(webhook)
        
    def emit(self, event_type: EventType, data: Optional[dict] = None, source: str = "universe"):
        """Emit an event"""
        event = Event(
            id=f"{event_type.value}_{int(time.time()*1000)}",
            type=event_type,
            timestamp=datetime.now(),
            data=data or {},
            source=source,
        )
        
        self.event_history.append(event)
        
        # Call subscribers
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Handler error: {e}")
                    
        # Send webhooks
        for webhook in self.webhooks:
            try:
                webhook.send(event)
            except Exception as e:
                print(f"Webhook error: {e}")
                
        return event
        
    def get_history(
        self, 
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> list[Event]:
        """Get event history"""
        events = self.event_history
        if event_type:
            events = [e for e in events if e.type == event_type]
        return events[-limit:]


# ============================================================================
# SLACK INTEGRATION
# ============================================================================

class SlackIntegration:
    """
    Slack integration.
    """
    
    def __init__(self, webhook_url: str = ""):
        self.webhook_url = webhook_url
        
    def send_message(self, message: str, channel: Optional[str] = None):
        """Send message to Slack"""
        if not self.webhook_url:
            print("  No Slack webhook configured")
            return False
            
        payload = {
            "text": message,
            "channel": channel,
        }
        
        print(f"  Would send to Slack: {message[:50]}...")
        return True
        
    def send_task_update(self, task: str, status: str):
        """Send task update"""
        emoji = {"started": "▶️", "completed": "✅", "failed": "❌"}.get(status, "⚪️")
        message = f"{emoji} Task: {task} - {status}"
        return self.send_message(message)
        
    def send_alert(self, level: str, message: str):
        """Send alert"""
        emoji = {"info": "ℹ️", "warning": "⚠️", "error": "🔴", "critical": "🚨"}.get(level, "⚪️")
        return self.send_message(f"{emoji} {message}")


# ============================================================================
# DISCORD INTEGRATION  
# ============================================================================

class DiscordIntegration:
    """
    Discord integration.
    """
    
    def __init__(self, webhook_url: str = ""):
        self.webhook_url = webhook_url
        
    def send_embed(self, title: str, description: str, color: int = 0):
        """Send embed"""
        payload = {
            "embeds": [{
                "title": title,
                "description": description,
                "color": color,
                "timestamp": datetime.now().isoformat(),
            }]
        }
        
        print(f"  Would send to Discord: {title}")
        return True
        
    def send_status(self, status: str):
        """Send status"""
        colors = {
            "healthy": 0x00FF00,
            "degraded": 0xFFA500, 
            "down": 0xFF0000,
        }
        color = colors.get(status.lower(), 0xAAAAAA)
        return self.send_embed(
            f"Universe IDE Status: {status}",
            f"Current status: {status}",
            color
        )


# ============================================================================
# GLOBAL EVENT BUS
# ============================================================================

_event_bus = None

def get_event_bus() -> EventBus:
    """Get global event bus"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


__all__ = [
    "EventType",
    "Event",
    "WebhookConfig", 
    "Webhook",
    "EventBus",
    "SlackIntegration",
    "DiscordIntegration",
    "get_event_bus",
]