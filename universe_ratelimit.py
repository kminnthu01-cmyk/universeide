"""
Universe IDE - API Rate Limiting

Rate limiting for API calls.
"""

import time
from collections import deque
from typing import Dict, Optional


# ============================================================================
# RATE LIMITER
# ============================================================================

class RateLimiter:
    """Rate limiter for API calls"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window = 60.0
        self.requests = deque()
        
    def allow(self) -> bool:
        now = time.time()
        
        # Remove old requests
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()
            
        if len(self.requests) < self.requests_per_minute:
            self.requests.append(now)
            return True
            
        return False
        
    def wait_time(self) -> float:
        if not self.requests:
            return 0.0
        return max(0.0, self.requests[0] + self.window - time.time())


# ============================================================================
# TOKEN BUCKET
# ============================================================================

class TokenBucket:
    """Token bucket rate limiter"""
    
    def __init__(self, capacity: int = 10, refill_rate: float = 1.0):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        
    def allow(self, tokens: int = 1) -> bool:
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
        
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now


# ============================================================================
# CIRCUIT BREAKER
# ============================================================================

class CircuitBreaker:
    """Circuit breaker pattern"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_max: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.half_open_max = half_open_max
        self.state = "closed"
        self.failures = 0
        self.last_failure = None
        self.half_open_calls = 0
        
    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure > self.timeout:
                self.state = "half-open"
                self.half_open_calls = 0
            else:
                raise Exception("Circuit breaker open")
                
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
            
    def _on_success(self):
        if self.state == "half-open":
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max:
                self.state = "closed"
                self.failures = 0
                
    def _on_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        
        if self.failures >= self.failure_threshold:
            self.state = "open"


# ============================================================================
# GLOBAL RATE LIMITER
# ============================================================================

_limiter = None

def get_rate_limiter() -> RateLimiter:
    global _limiter
    if _limiter is None:
        _limiter = RateLimiter()
    return _limiter


__all__ = ["RateLimiter", "TokenBucket", "CircuitBreaker", "get_rate_limiter"]