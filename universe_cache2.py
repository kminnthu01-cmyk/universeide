"""
Universe IDE - Cache Store Module

Distributed cache.
"""

from typing import Any, Dict, Optional
import time


# ============================================================================
# CACHE ENTRY
# ============================================================================

class CacheEntry:
    """Cache entry"""
    
    def __init__(self, key: str, value: Any, ttl: int = 3600):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.created = time.time()
        
    def is_expired(self) -> bool:
        return time.time() - self.created > self.ttl


# ============================================================================
# CACHE STORE
# ============================================================================

class CacheStore:
    """Distributed cache"""
    
    def __init__(self):
        self.cache = {}
        
    def set(self, key: str, value: Any, ttl: int = 3600):
        self.cache[key] = CacheEntry(key, value, ttl)
        
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                return entry.value
            del self.cache[key]
        return None
        
    def delete(self, key: str) -> bool:
        if key in self.cache:
            del self.cache[key]
            return True
        return False
        
    def clear(self):
        self.cache.clear()


# Global
_cache = None

def get_cache_store() -> CacheStore:
    global _cache
    if _cache is None:
        _cache = CacheStore()
    return _cache


__all__ = ["CacheEntry", "CacheStore", "get_cache_store"]