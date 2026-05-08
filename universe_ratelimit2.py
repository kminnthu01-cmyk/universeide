"""
Universe IDE - Rate Limiter Module

Rate limiting.
"""

from typing import Any, Dict
import time
from collections import deque


# ============================================================================
# RATE LIMITER
# ============================================================================

class RateLimiter:
    """Rate limiter"""
    
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = deque()
        
    def allow(self) -> bool:
        now = time.time()
        # Remove old requests
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()
            
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
        
    def reset(self):
        self.requests.clear()
        
    def get_remaining(self) -> int:
        return max(0, self.max_requests - len(self.requests))


# Global
_ratelimiter = None

def get_ratelimiter() -> RateLimiter:
    global _ratelimiter
    if _ratelimiter is None:
        _ratelimiter = RateLimiter()
    return _ratelimiter


__all__ = ["RateLimiter", "get_ratelimiter"]