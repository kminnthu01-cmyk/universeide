"""
Universe IDE - Storage Module

Object storage.
"""

from typing import Any, Dict, List, Optional
import time


# ============================================================================
# OBJECT
# ============================================================================

class StorageObject:
    """Storage object"""
    
    def __init__(self, key: str, data: Any, metadata: Dict = None):
        self.key = key
        self.data = data
        self.metadata = metadata or {}
        self.created_at = time.time()
        self.size = len(str(data))


# ============================================================================
# OBJECT STORE
# ============================================================================

class ObjectStore:
    """Object storage"""
    
    def __init__(self):
        self.objects = {}
        
    def put(self, key: str, data: Any, metadata: Dict = None):
        obj = StorageObject(key, data, metadata)
        self.objects[key] = obj
        return obj
        
    def get(self, key: str) -> Optional[StorageObject]:
        return self.objects.get(key)
        
    def delete(self, key: str) -> bool:
        if key in self.objects:
            del self.objects[key]
            return True
        return False
        
    def list_keys(self) -> List[str]:
        return list(self.objects.keys())


# Global
_store = None

def get_object_store() -> ObjectStore:
    global _store
    if _store is None:
        _store = ObjectStore()
    return _store


__all__ = ["StorageObject", "ObjectStore", "get_object_store"]