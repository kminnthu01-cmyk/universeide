"""
Universe IDE - Notification System

Real-time notifications and alerts.
"""

import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List


# ============================================================================
# NOTIFICATIONS
# ============================================================================

class Notification:
    """Notification"""
    
    TYPES = ["info", "success", "warning", "error", "debug"]
    
    def __init__(
        self,
        message: str,
        type: str = "info",
        title: str = ""
    ):
        self.id = str(uuid.uuid4())[:8]
        self.message = message
        self.type = type if type in self.TYPES else "info"
        self.title = title
        self.timestamp = datetime.now()
        self.read = False


# ============================================================================
# NOTIFIER
# ============================================================================

class Notifier:
    """Manage notifications"""
    
    def __init__(self, max_size: int = 100):
        self.notifications = deque(maxlen=max_size)
        
    def send(
        self,
        message: str,
        type: str = "info",
        title: str = ""
    ) -> str:
        notif = Notification(message, type, title)
        self.notifications.append(notif)
        return notif.id
    
    def get_all(self) -> List[Notification]:
        return list(self.notifications)
    
    def get_unread(self) -> List[Notification]:
        return [n for n in self.notifications if not n.read]
    
    def mark_read(self, notif_id: str) -> bool:
        for notif in self.notifications:
            if notif.id == notif_id:
                notif.read = True
                return True
        return False
    
    def clear(self):
        self.notifications.clear()


# ============================================================================
# ALERTS
# ============================================================================

class Alert:
    """System alerts"""
    
    def __init__(self):
        self.handlers = {}
        
    def on(self, level: str, handler: Callable):
        if level not in self.handlers:
            self.handlers[level] = []
        self.handlers[level].append(handler)
        
    def trigger(self, level: str, message: str):
        if level in self.handlers:
            for handler in self.handlers[level]:
                handler(message)


# ============================================================================
# INAPP MESSAGES
# ============================================================================

class InAppMessages:
    """In-app messaging"""
    
    def __init__(self):
        self.messages = []
        
    def show(self, text: str, duration: int = 3000):
        self.messages.append({
            "text": text,
            "duration": duration,
        })
        
    def get_pending(self) -> List[Dict]:
        return self.messages


# Global
_notifier = None

def get_notifier() -> Notifier:
    global _notifier
    if _notifier is None:
        _notifier = Notifier()
    return _notifier


__all__ = ["Notification", "Notifier", "Alert", "InAppMessages", "get_notifier"]