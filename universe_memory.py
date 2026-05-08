"""
Universe IDE - Persistent Memory System

Persistent storage for agent states and knowledge.
"""

import json
import os
import pickle
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


# ============================================================================
# MEMORY STORE
# ============================================================================

class MemoryStore:
    """
    Persistent in-memory store.
    """
    
    def __init__(self, path: str = "./.universe/memory"):
        self.path = path
        self.store: dict = {}
        os.makedirs(path, exist_ok=True)
        
    def set(self, key: str, value: Any, ttl: int = 0):
        """Set value with optional TTL"""
        self.store[key] = {
            "value": value,
            "timestamp": time.time(),
            "ttl": ttl,
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get value"""
        if key not in self.store:
            return default
            
        data = self.store[key]
        
        # Check TTL
        if data["ttl"] > 0:
            if time.time() - data["timestamp"] > data["ttl"]:
                del self.store[key]
                return default
                
        return data["value"]
        
    def delete(self, key: str):
        """Delete key"""
        if key in self.store:
            del self.store[key]
            
    def keys(self) -> list[str]:
        """Get all keys"""
        return list(self.store.keys())
        
    def clear(self):
        """Clear store"""
        self.store.clear()


# ============================================================================
# DISK PERSISTENCE
# ============================================================================

class DiskStore:
    """
    Disk-based persistent storage.
    """
    
    def __init__(self, path: str = "./.universe/db"):
        self.path = path
        os.makedirs(path, exist_ok=True)
        
    def _get_file(self, key: str) -> str:
        """Get file path"""
        safe_key = key.replace("/", "_").replace(":", "_")
        return os.path.join(self.path, f"{safe_key}.json")
        
    def set(self, key: str, value: Any):
        """Save to disk"""
        filepath = self._get_file(key)
        
        data = {
            "key": key,
            "value": value,
            "timestamp": datetime.now().isoformat(),
        }
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)
            
    def get(self, key: str, default: Any = None) -> Any:
        """Load from disk"""
        filepath = self._get_file(key)
        
        if not os.path.exists(filepath):
            return default
            
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            return data.get("value", default)
        except:
            return default
            
    def delete(self, key: str):
        """Delete from disk"""
        filepath = self._get_file(key)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            
    def keys(self) -> list[str]:
        """Get all keys"""
        keys = []
        
        for filename in os.listdir(self.path):
            if filename.endswith(".json"):
                keys.append(filename[:-5].replace("_", "/"))
                
        return keys


# ============================================================================
# KNOWLEDGE BASE
# ============================================================================

class KnowledgeBase:
    """
    Agent knowledge base.
    """
    
    def __init__(self):
        self.memory = MemoryStore()
        self.disk = DiskStore()
        
    def learn(self, key: str, value: Any, persist: bool = True):
        """Learn information"""
        if persist:
            self.disk.set(key, value)
        else:
            self.memory.set(key, value)
            
    def recall(self, key: str) -> Any:
        """Recall information"""
        # Check memory first
        value = self.memory.get(key)
        if value is not None:
            return value
            
        # Check disk
        return self.disk.get(key)
        
    def forget(self, key: str):
        """Forget information"""
        self.memory.delete(key)
        self.disk.delete(key)
        
    def search(self, query: str) -> list[tuple[str, Any]]:
        """Search knowledge base"""
        results = []
        
        # Search memory
        for key in self.memory.keys():
            if query.lower() in key.lower():
                results.append((key, self.memory.get(key)))
                
        # Search disk
        for key in self.disk.keys():
            if query.lower() in key.lower():
                results.append((key, self.disk.get(key)))
                
        return results


# ============================================================================
# AGENT STATE STORE
# ============================================================================

class AgentStateStore:
    """Store for agent states"""
    
    def __init__(self):
        self.disk = DiskStore("./.universe/agent_states")
        
    def save_state(self, agent_id: str, state: dict):
        """Save agent state"""
        self.disk.set(f"agent_{agent_id}", state)
        
    def load_state(self, agent_id: str) -> Optional[dict]:
        """Load agent state"""
        return self.disk.get(f"agent_{agent_id}")


# ============================================================================
# CONTEXT STORE
# ============================================================================

class ContextStore:
    """Context storage for conversations"""
    
    def __init__(self, max_contexts: int = 100):
        self.max_contexts = max_contexts
        self.contexts: dict[str, list[dict]] = {}
        
    def add_message(self, context_id: str, role: str, content: str):
        """Add message to context"""
        if context_id not in self.contexts:
            self.contexts[context_id] = []
            
        self.contexts[context_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        
        # Trim if needed
        if len(self.contexts[context_id]) > self.max_contexts:
            self.contexts[context_id] = self.contexts[context_id][-self.max_contexts:]
            
    def get_context(self, context_id: str) -> list[dict]:
        """Get conversation context"""
        return self.contexts.get(context_id, [])


# Global
_kb = None

def get_knowledge_base() -> KnowledgeBase:
    """Get global knowledge base"""
    global _kb
    if _kb is None:
        _kb = KnowledgeBase()
    return _kb


__all__ = [
    "MemoryStore",
    "DiskStore",
    "KnowledgeBase",
    "AgentStateStore",
    "ContextStore",
    "get_knowledge_base",
]