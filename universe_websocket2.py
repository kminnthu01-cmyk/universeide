"""
Universe IDE - WebSocket Hub Module

WebSocket management.
"""

from typing import Any, Callable, Dict, List
import json


# ============================================================================
# WS CLIENT
# ============================================================================

class WSClient:
    """WebSocket client"""
    
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.connected = True
        
    def send(self, message: Any):
        return {"to": self.client_id, "message": message}
        
    def close(self):
        self.connected = False


# ============================================================================
# WS HUB
# ============================================================================

class WSHub:
    """WebSocket hub"""
    
    def __init__(self):
        self.clients = {}
        
    def connect(self, client: WSClient):
        self.clients[client.client_id] = client
        
    def disconnect(self, client_id: str):
        if client_id in self.clients:
            self.clients[client_id].close()
            del self.clients[client_id]
            
    def broadcast(self, message: Any):
        return [c.send(message) for c in self.clients.values()]


# Global
_hub = None

def get_ws_hub() -> WSHub:
    global _hub
    if _hub is None:
        _hub = WSHub()
    return _hub


__all__ = ["WSClient", "WSHub", "get_ws_hub"]