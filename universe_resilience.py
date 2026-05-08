"""
Universe IDE - Error Recovery & Resilience

Features:
- Automatic error recovery
- Retry strategies
- Circuit breaker
- Graceful degradation
"""

import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# ERROR CLASSES
# ============================================================================

class ErrorType(Enum):
    """Types of errors"""
    RETRYABLE = "retryable"
    TRANSIENT = "transient"
    FATAL = "fatal"
    TIMEOUT = "timeout"


@dataclass
class ErrorRecord:
    """Record of an error"""
    error_type: ErrorType
    message: str
    timestamp: datetime
    retry_count: int = 0
    recovered: bool = False


# ============================================================================
# RETRY STRATEGIES
# ============================================================================

class RetryStrategy(Enum):
    """Retry strategies"""
    IMMEDIATE = "immediate"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    FIBONACCI = "fibonacci"


class RetryConfig:
    """Configuration for retries"""
    max_retries: int = 3
    base_delay: float = 0.1
    max_delay: float = 30.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    
    def get_delay(self, attempt: int) -> float:
        """Calculate delay for attempt"""
        if self.strategy == RetryStrategy.IMMEDIATE:
            return 0
        elif self.strategy == RetryStrategy.LINEAR:
            delay = self.base_delay * attempt
        elif self.strategy == RetryStrategy.EXPONENTIAL:
            delay = self.base_delay * (2 ** attempt)
        elif self.strategy == RetryStrategy.FIBONACCI:
            delay = self.base_delay * self._fib(attempt)
        else:
            delay = self.base_delay
            
        return min(delay, self.max_delay)
        
    def _fib(self, n: int) -> int:
        """Fibonacci"""
        if n <= 1:
            return 1
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a + b
        return b


def with_retry(
    func: Callable,
    config: Optional[RetryConfig] = None,
    error_filter: Optional[Callable[[Exception], bool]] = None
) -> Callable:
    """
    Decorator to add retry logic.
    
    Usage:
        @with_retry(config=RetryConfig(max_retries=3))
        def my_function():
            ...
    """
    config = config or RetryConfig()
    
    def wrapper(*args, **kwargs):
        last_error = None
        
        for attempt in range(config.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                # Check if should retry
                if error_filter and not error_filter(e):
                    raise
                    
                if attempt < config.max_retries:
                    delay = config.get_delay(attempt)
                    time.sleep(delay)
                    
        raise last_error
        
    return wrapper


# ============================================================================
# CIRCUIT BREAKER
# ============================================================================

class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"        # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class CircuitConfig:
    """Circuit breaker configuration"""
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout_seconds: float = 30.0


class CircuitBreaker:
    """
    Circuit breaker pattern for fault tolerance.
    
    Prevents cascading failures by failing fast.
    """
    
    def __init__(self, name: str = "default", config: Optional[CircuitConfig] = None):
        self.name = name
        self.config = config or CircuitConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call function with circuit breaker"""
        # Check state
        if self.state == CircuitState.OPEN:
            # Check if should try half-open
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpen(f"Circuit {self.name} is OPEN")
                
        try:
            result = func(*args, **kwargs)
            
            # Success
            self._on_success()
            return result
            
        except Exception as e:
            # Failure
            self._on_failure()
            raise
            
    def _should_attempt_recovery(self) -> bool:
        """Check if should attempt recovery"""
        if self.last_failure_time is None:
            return True
        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.config.timeout_seconds
        
    def _on_success(self):
        """Handle success"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.state == CircuitState.CLOSED:
            # Reset on success in closed state
            if self.failure_count > 0:
                self.failure_count = max(0, self.failure_count - 1)
                
    def _on_failure(self):
        """Handle failure"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.success_count = 0
        
        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            
    def get_state(self) -> dict:
        """Get circuit state"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failures": self.failure_count,
            "successes": self.success_count,
        }


# ============================================================================
# GRACEFUL DEGRADATION
# ============================================================================

@dataclass
class DegradationConfig:
    """Configuration for graceful degradation"""
    enabled_features: dict = field(default_factory=dict)
    fallback_values: dict = field(default_factory=dict)


class GracefulDegradation:
    """
    Allow system to degrade gracefully.
    
    Features can be disabled one at a time.
    """
    
    def __init__(self):
        self.disabled_features: set = set()
        self.fallbacks: dict = {}
        
    def disable_feature(self, name: str):
        """Disable a feature"""
        self.disabled_features.add(name)
        
    def enable_feature(self, name: str):
        """Enable a feature"""
        self.disabled_features.discard(name)
        
    def is_enabled(self, name: str) -> bool:
        """Check if feature is enabled"""
        return name not in self.disabled_features
        
    def register_fallback(self, name: str, fallback: Callable):
        """Register fallback for feature"""
        self.fallbacks[name] = fallback
        
    def call_with_fallback(self, name: str, func: Callable, *args, **kwargs) -> Any:
        """Call with fallback"""
        if name in self.disabled_features:
            fallback = self.fallbacks.get(name)
            if fallback:
                return fallback(*args, **kwargs)
            return None
            
        try:
            return func(*args, **kwargs)
        except Exception:
            if name in self.fallbacks:
                return self.fallbacks[name](*args, **kwargs)
            raise
            
    def get_status(self) -> dict:
        """Get degradation status"""
        return {
            "disabled": list(self.disabled_features),
            "fallbacks": list(self.fallbacks.keys()),
        }


# ============================================================================
# RESILIENCE MANAGER
# ============================================================================

class ResilienceManager:
    """
    Central resilience management.
    """
    
    def __init__(self):
        self.circuits: dict[str, CircuitBreaker] = {}
        self.degradation = GracefulDegradation()
        self.retry_config = RetryConfig()
        
    def get_circuit(self, name: str) -> CircuitBreaker:
        """Get or create circuit breaker"""
        if name not in self.circuits:
            self.circuits[name] = CircuitBreaker(name)
        return self.circuits[name]
        
    def with_resilience(
        self, 
        circuit_name: str,
        func: Callable,
        *args, 
        **kwargs
    ) -> Any:
        """Call function with all resilience"""
        circuit = self.get_circuit(circuit_name)
        
        # Wrap with retry
        retry_func = with_retry(func, self.retry_config)
        
        # Call with circuit
        return circuit.call(retry_func, *args, **kwargs)
        
    def get_status(self) -> dict:
        """Get resilience status"""
        return {
            "circuits": {n: c.get_state() for n, c in self.circuits.items()},
            "degradation": self.degradation.get_status(),
        }


# Global instance
_resilience = None

def get_resilience() -> ResilienceManager:
    """Get global resilience manager"""
    global _resilience
    if _resilience is None:
        _resilience = ResilienceManager()
    return _resilience


__all__ = [
    "ErrorType",
    "ErrorRecord",
    "RetryConfig",
    "RetryStrategy", 
    "with_retry",
    "CircuitBreaker",
    "CircuitState",
    "CircuitConfig",
    "GracefulDegradation",
    "ResilienceManager",
    "get_resilience",
]