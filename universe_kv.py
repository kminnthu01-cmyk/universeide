"""
Universe IDE - KV Store Module

Key-value store.
"""

from typing import Any, Dict, Optional
import json


# ============================================================================
# KV STORE
# ============================================================================

class KVStore:
    """Key-value store"""
    
    def __init__(self):
        self.store = {}
        
    def set(self, key: str, value: Any):
        self.store[key] = value
        
    def get(self, key: str) -> Optional[Any]:
        return self.store.get(key)
        
    def delete(self, key: str) -> bool:
        if key in self.store:
            del self.store[key]
            return True
        return False
        
    def keys(self) -> list:
        return list(self.store.keys())
        
    def clear(self):
        self.store.clear()


# Global
_kv = None

def get_kv_store() -> KVStore:
    global _kv
    if _kv is None:
        _kv = KVStore()
    return _kv


__all__ = ["KVStore", "get_kv_store"]