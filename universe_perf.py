"""
Universe IDE - Performance & Efficiency

Optimizations for speed and efficiency.
"""

import gc
import os
import sys
import time
from functools import lru_cache
from typing import Any, Callable


# ============================================================================
# LAZY IMPORTS
# ============================================================================

class LazyImporter:
    """
    Lazy module importing for fast startup.
    """
    
    _cache: dict = {}
    _import_map = {
        "universe": "universe",
        "universe_ide": "universe_ide",
        "universe_cli": "universe_cli",
    }
    
    @classmethod
    def import_module(cls, name: str):
        """Lazy import"""
        if name in cls._cache:
            return cls._cache[name]
            
        if name in cls._import_map:
            try:
                mod = __import__(cls._import_map[name])
                cls._cache[name] = mod
                return mod
            except:
                pass
        return None
        
    @classmethod
    def preload(cls, modules: list[str]):
        """Preload modules"""
        for m in modules:
            cls.import_module(m)


# ============================================================================
# FUNCTION CACHING
# ============================================================================

class CacheManager:
    """
    Global cache management.
    """
    
    _cache: dict = {}
    _max_size: int = 1000
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get from cache"""
        return cls._cache.get(key, default)
        
    @classmethod
    def set(cls, key: str, value: Any):
        """Set in cache"""
        if len(cls._cache) >= cls._max_size:
            # Clear oldest
            first_key = next(iter(cls._cache))
            del cls._cache[first_key]
            
        cls._cache[key] = value
        
    @classmethod
    def clear(cls):
        """Clear cache"""
        cls._cache.clear()
        
    @classmethod
    def memoize(cls, func: Callable) -> Callable:
        """Memoization decorator"""
        @lru_cache(maxsize=256)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


# ============================================================================
# MEMORY OPTIMIZER
# ============================================================================

class MemoryOptimizer:
    """
    Memory optimization.
    """
    
    @staticmethod
    def optimize():
        """Run memory optimization"""
        gc.collect()
        
    @staticmethod
    def get_usage() -> dict:
        """Get memory usage"""
        try:
            import resource
            r = resource.getrusage(resource.RUSAGE_SELF)
            return {
                "max_rss_mb": r.ru_maxrss / 1024,
                "user_time": r.ru_utime,
                "system_time": r.ru_stime,
            }
        except:
            return {"max_rss_mb": 0}
            
    @staticmethod
    def auto_tune():
        """Auto-tune based on system"""
        import gc
        gc.collect()
        
        # Adjust gc thresholds based on memory
        gc.set_threshold(50000, 500, 1000)


# ============================================================================
# FAST PATHS
# ============================================================================

def fast_import(name: str):
    """Fast module import"""
    return LazyImporter.import_module(name)


def cached_call(key: str, func: Callable, *args, **kwargs) -> Any:
    """Cached function call"""
    # Check cache
    cached = CacheManager.get(key)
    if cached is not None:
        return cached
        
    # Execute
    result = func(*args, **kwargs)
    
    # Cache result
    CacheManager.set(key, result)
    
    return result


# ============================================================================
# BENCHMARKING
# ============================================================================

class Benchmark:
    """
    Simple benchmarking.
    """
    
    def __init__(self, name: str = "benchmark"):
        self.name = name
        self.results: list = []
        
    def __enter__(self):
        self.start = time.perf_counter()
        return self
        
    def __exit__(self, *args):
        elapsed = time.perf_counter() - self.start
        self.results.append(elapsed)
        
    @property
    def last(self) -> float:
        return self.results[-1] if self.results else 0


# ============================================================================
# PERFORMANCE OPTIMIZER
# ============================================================================

class PerformanceOptimizer:
    """
    Overall performance optimization.
    """
    
    def __init__(self):
        self.memory = MemoryOptimizer()
        self.cache = CacheManager()
        self.lazy = LazyImporter()
        self.start_time = time.time()
        
    def initialize(self):
        """Initialize optimizations"""
        self.memory.auto_tune()
        
    def get_stats(self) -> dict:
        """Get performance stats"""
        return {
            "memory": self.memory.get_usage(),
            "cache_size": len(self.cache._cache),
            "uptime_seconds": time.time() - self.start_time,
        }
        
    def optimize(self):
        """Run all optimizations"""
        self.memory.optimize()


# Global
_perf = None

def get_perf() -> PerformanceOptimizer:
    """Get global optimizer"""
    global _perf
    if _perf is None:
        _perf = PerformanceOptimizer()
    return _perf


__all__ = [
    "LazyImporter",
    "CacheManager", 
    "MemoryOptimizer",
    "fast_import",
    "cached_call",
    "Benchmark",
    "PerformanceOptimizer",
    "get_perf",
]