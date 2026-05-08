"""
Universe IDE - Error Handling & Bug Fixes

Comprehensive error handling, logging, and bug fixes.
"""

import logging
import traceback
from collections import deque
from datetime import datetime
from typing import Any, Dict, Optional


# ============================================================================
# ERROR TRACKING
# ============================================================================

class ErrorTracker:
    """Track and log errors"""
    
    def __init__(self, max_size: int = 1000):
        self.errors = deque(maxlen=max_size)
        self.logger = logging.getLogger("universe_errors")
        
    def record(
        self,
        error: Exception,
        context: str = "",
        severity: str = "error"
    ) -> str:
        error_id = f"ERR-{len(self.errors):05d}"
        
        error_record = {
            "id": error_id,
            "type": type(error).__name__,
            "message": str(error),
            "context": context,
            "severity": severity,
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now(),
        }
        
        self.errors.append(error_record)
        self.logger.error(f"[{error_id}] {context}: {error}")
        
        return error_id
        
    def get_recent(self, count: int = 10) -> list:
        return list(self.errors)[-count:]


# ============================================================================
# GRACEFUL DEGRADATION
# ============================================================================

class GracefulDegradation:
    """Handle failures gracefully"""
    
    def __init__(self):
        self.fallbacks = {}
        
    def register_fallback(self, func_name: str, fallback_fn):
        self.fallbacks[func_name] = fallback_fn
        
    def with_fallback(self, func_name: str, default=None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if func_name in self.fallbacks:
                        return self.fallbacks[func_name](*args, **kwargs)
                    return default
            return wrapper
        return decorator


# ============================================================================
# INPUT VALIDATION
# ============================================================================

class InputValidator:
    """Validate inputs"""
    
    @staticmethod
    def validate_agent_count(count: int) -> tuple:
        errors = []
        
        if count < 0:
            errors.append("Agent count cannot be negative")
        if count > 10000:
            errors.append("Agent count exceeds maximum (10000)")
            
        return (len(errors) == 0, errors)
        
    @staticmethod
    def validate_api_key(key: str) -> tuple:
        errors = []
        
        if not key:
            errors.append("API key is required")
        if key and len(key) < 10:
            errors.append("API key too short")
            
        return (len(errors) == 0, errors)


# ============================================================================
# MEMORY LEAK PREVENTION
# ============================================================================

class MemoryManager:
    """Prevent memory leaks"""
    
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.caches = {}
        
    def register_cache(self, name: str, cache):
        self.caches[name] = cache
        
    def clear_all(self):
        for name, cache in self.caches.items():
            if hasattr(cache, 'clear'):
                cache.clear()
                
    def get_memory_info(self) -> Dict:
        total = sum(
            len(c) if hasattr(c, '__len__') else 0 
            for c in self.caches.values()
        )
        return {
            "caches": len(self.caches),
            "total_items": total,
            "max_size": self.max_size,
        }


# ============================================================================
# THREAD SAFETY
# ============================================================================

class ThreadSafeCounter:
    """Thread-safe counter"""
    
    def __init__(self, initial: int = 0):
        self._value = initial
        import threading
        self._lock = threading.Lock()
        
    def increment(self, amount: int = 1) -> int:
        with self._lock:
            self._value += amount
            return self._value
            
    def decrement(self, amount: int = 1) -> int:
        with self._lock:
            self._value -= amount
            return self._value
            
    @property
    def value(self) -> int:
        with self._lock:
            return self._value


# ============================================================================
# BUG FIXES
# ============================================================================

def safe_execute(func, *args, default=None, **kwargs) -> Any:
    """Safely execute function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception:
        return default


def retry_with_backoff(
    func,
    max_attempts: int = 3,
    delay: float = 1.0
) -> Any:
    """Retry with exponential backoff"""
    import time
    
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(delay * (2 ** attempt))
            else:
                raise e


# Global tracker
_tracker = None

def get_error_tracker() -> ErrorTracker:
    global _tracker
    if _tracker is None:
        _tracker = ErrorTracker()
    return _tracker


__all__ = [
    "ErrorTracker",
    "GracefulDegradation",
    "InputValidator",
    "MemoryManager",
    "ThreadSafeCounter",
    "safe_execute",
    "retry_with_backoff",
    "get_error_tracker",
]