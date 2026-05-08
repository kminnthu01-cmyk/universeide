"""
Universe IDE - Advanced Caching

Intelligent caching system.
"""

import hashlib
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Callable, Optional


# ============================================================================
# CACHE
# ============================================================================

@dataclass
class CacheEntry:
    key: str
    value: Any
    created: float
    expires: float
    hits: int = 0


class IntelligentCache:
    """Smart cache with eviction"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self.cache = {}
        self.hits = 0
        self.misses = 0
        
    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            self.misses += 1
            return None
            
        entry = self.cache[key]
        
        # Check expiration
        if time.time() > entry.expires:
            del self.cache[key]
            self.misses += 1
            return None
            
        entry.hits += 1
        self.hits += 1
        return entry.value
        
    def set(self, key: str, value: Any, ttl: int = None):
        # Evict if full
        if len(self.cache) >= self.max_size:
            self._evict()
            
        entry = CacheEntry(
            key=key,
            value=value,
            created=time.time(),
            expires=time.time() + (ttl or self.ttl),
        )
        self.cache[key] = entry
        
    def _evict(self):
        # Remove least recently used
        if not self.cache:
            return
            
        # Find lowest hits
        key = min(self.cache.keys(), key=lambda k: self.cache[k].hits)
        del self.cache[key]
        
    def hash_key(self, *args) -> str:
        data = str(args)
        return hashlib.md5(data.encode()).hexdigest()[:16]
        
    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "size": len(self.cache),
            "max": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / max(1, total),
        }


# ============================================================================
# LRU CACHE
# ============================================================================

class LRUCache:
    """Least recently used cache"""
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}
        self.order = []
        
    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
            
        # Move to end (most recent)
        self.order.remove(key)
        self.order.append(key)
        
        return self.cache[key]
        
    def put(self, key: str, value: Any):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Remove oldest
            oldest = self.order.pop(0)
            del self.cache[oldest]
            
        self.cache[key] = value
        self.order.append(key)
        
    def __len__(self) -> int:
        return len(self.cache)


# ============================================================================
# FUNCTION CACHE
# ============================================================================

class FunctionCache:
    """Memoization wrapper"""
    
    def __init__(self):
        self.cache = IntelligentCache()
        
    def memoize(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            key = self.cache.hash_key(str(args), str(kwargs))
            result = self.cache.get(key)
            
            if result is None:
                result = func(*args, **kwargs)
                self.cache.set(key, result)
                
            return result
            
        return wrapper


# ============================================================================
# DISTRIBUTED CACHE
# ============================================================================

class DistributedCache:
    """Multi-node cache"""
    
    def __init__(self):
        self.nodes = {}
        
    def add_node(self, name: str, cache: IntelligentCache):
        self.nodes[name] = cache
        
    def get(self, key: str) -> Any:
        # Try each node
        for name, cache in self.nodes.items():
            result = cache.get(key)
            if result:
                return result
        return None
        
    def set(self, key: str, value: Any):
        # Store in first available
        for cache in self.nodes.values():
            if len(cache.cache) < cache.max_size:
                cache.set(key, value)
                return True
        return False
        
    def stats(self) -> dict:
        total = sum(n.stats() for n in self.nodes.values())
        return {
            "nodes": len(self.nodes),
            "total_size": total["size"],
        }


_cache = None

def get_cache() -> IntelligentCache:
    global _cache
    if _cache is None:
        _cache = IntelligentCache()
    return _cache


__all__ = ["IntelligentCache", "LRUCache", "FunctionCache", "DistributedCache", "get_cache"]