"""
Universe IDE - Session Module

Session management.
"""

from typing import Any, Dict
import time


# ============================================================================
# SESSION
# ============================================================================

class Session:
    """Session"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.data = {}
        self.created = time.time()
        self.expires = time.time() + 3600
        
    def set(self, key: str, value: Any):
        self.data[key] = value
        
    def get(self, key: str) -> Any:
        return self.data.get(key)


# ============================================================================
# SESSION STORE
# ============================================================================

class SessionStore:
    """Session store"""
    
    def __init__(self):
        self.sessions = {}
        
    def create(self, session_id: str) -> Session:
        session = Session(session_id)
        self.sessions[session_id] = session
        return session
        
    def get(self, session_id: str) -> Session:
        return self.sessions.get(session_id)


# Global
_store = None

def get_session_store() -> SessionStore:
    global _store
    if _store is None:
        _store = SessionStore()
    return _store


__all__ = ["Session", "SessionStore", "get_session_store"]