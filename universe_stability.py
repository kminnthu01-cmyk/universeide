"""
Universe IDE - Stability & Reliability

Enhanced error handling and stability features.
"""

import logging
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# LOGGING
# ============================================================================

class LogLevel(Enum):
    """Log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StabilityLogger:
    """
    Stability logging.
    """
    
    def __init__(self, name: str = "universe"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Add handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
    def log(self, level: LogLevel, message: str):
        """Log message"""
        getattr(self.logger, level.value.lower())(message)
        
    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)
        
    def info(self, message: str):
        self.log(LogLevel.INFO, message)
        
    def warning(self, message: str):
        self.log(LogLevel.WARNING, message)
        
    def error(self, message: str):
        self.log(LogLevel.ERROR, message)
        
    def critical(self, message: str):
        self.log(LogLevel.CRITICAL, message)


# ============================================================================
# ERROR HANDLING
# ============================================================================

@dataclass
class ErrorRecord:
    """Error record"""
    error_type: str
    message: str
    timestamp: datetime
    traceback: str = ""
    resolved: bool = False


class ErrorHandler:
    """
    Global error handling.
    """
    
    def __init__(self):
        self.errors: list[ErrorRecord] = []
        self.max_errors = 100
        self.logger = StabilityLogger()
        
    def handle(self, error: Exception, context: str = "") -> dict:
        """Handle error"""
        record = ErrorRecord(
            error_type=type(error).__name__,
            message=str(error),
            timestamp=datetime.now(),
            traceback=traceback.format_exc(),
        )
        
        self.errors.append(record)
        
        # Log error
        self.logger.error(f"{context}: {error}")
        
        # Trim
        if len(self.errors) > self.max_errors:
            self.errors = self.errors[-self.max_errors:]
            
        return {
            "error_type": record.error_type,
            "message": record.message,
            "resolved": record.resolved,
        }
        
    def get_errors(self, unresolved_only: bool = False) -> list:
        """Get errors"""
        errors = self.errors
        
        if unresolved_only:
            errors = [e for e in errors if not e.resolved]
            
        return errors
        
    def resolve_error(self, index: int):
        """Mark error as resolved"""
        if 0 <= index < len(self.errors):
            self.errors[index].resolved = True


# ============================================================================
# GRACEFUL DEGRADATION
# ============================================================================

class GracefulDegradation:
    """
    Graceful degradation system.
    """
    
    def __init__(self):
        self.features: dict = {}
        self.fallbacks: dict = {}
        
    def register_feature(
        self, 
        name: str, 
        func: Callable,
        fallback: Any = None
    ):
        """Register feature"""
        self.features[name] = func
        self.fallbacks[name] = fallback
        
    def call(self, name: str, *args, **kwargs) -> Any:
        """Call with fallback"""
        func = self.features.get(name)
        
        if func is None:
            return self.fallbacks.get(name)
            
        try:
            return func(*args, **kwargs)
        except Exception as e:
            StabilityLogger().error(f"Feature {name}: {e}")
            return self.fallbacks.get(name)


# ============================================================================
# RECOVERY
# ============================================================================

class RecoveryManager:
    """
    System recovery manager.
    """
    
    def __init__(self):
        self.checkpoints: list = []
        self.max_checkpoints = 10
        self.error_handler = ErrorHandler()
        
    def create_checkpoint(self, state: dict):
        """Create checkpoint"""
        self.checkpoints.append({
            "timestamp": datetime.now(),
            "state": state,
        })
        
        if len(self.checkpoints) > self.max_checkpoints:
            self.checkpoints = self.checkpoints[-self.max_checkpoints:]
            
    def restore_latest(self) -> Optional[dict]:
        """Restore latest checkpoint"""
        if self.checkpoints:
            return self.checkpoints[-1]["state"]
        return None
        
    def recover(self) -> dict:
        """Attempt recovery"""
        # Handle errors
        errors = self.error_handler.get_errors()
        
        return {
            "checkpoints": len(self.checkpoints),
            "unresolved_errors": len(errors),
            "recovery_status": "available" if self.checkpoints else "no_checkpoints",
        }


# ============================================================================
# HEALTH CHECKS
# ============================================================================

class HealthChecks:
    """
    System health checks.
    """
    
    def __init__(self):
        self.checks: dict = {}
        
    def register_check(self, name: str, check_fn: Callable):
        """Register health check"""
        self.checks[name] = check_fn
        
    def run_check(self, name: str) -> bool:
        """Run single check"""
        if name not in self.checks:
            return False
            
        try:
            return self.checks[name]()
        except:
            return False
            
    def run_all(self) -> dict:
        """Run all checks"""
        results = {}
        
        for name, check_fn in self.checks.items():
            try:
                results[name] = check_fn()
            except:
                results[name] = False
                
        return results
        
    def is_healthy(self) -> bool:
        """Check if system is healthy"""
        results = self.run_all()
        return all(results.values())


# ============================================================================
# STABILITY MANAGER
# ============================================================================

class StabilityManager:
    """
    Unified stability management.
    """
    
    def __init__(self):
        self.logger = StabilityLogger()
        self.error_handler = ErrorHandler()
        self.recovery = RecoveryManager()
        self.health = HealthChecks()
        self.degradation = GracefulDegradation()
        
    def register_health_check(self, name: str, check_fn: Callable):
        """Register health check"""
        self.health.register_check(name, check_fn)
        
    def get_status(self) -> dict:
        """Get stability status"""
        return {
            "healthy": self.health.is_healthy(),
            "errors": len(self.error_handler.get_errors()),
            "checkpoints": len(self.recovery.checkpoints),
            "health_checks": self.health.run_all(),
        }


# Global
_stability = None

def get_stability() -> StabilityManager:
    """Get global stability manager"""
    global _stability
    if _stability is None:
        _stability = StabilityManager()
    return _stability


__all__ = [
    "LogLevel",
    "StabilityLogger",
    "ErrorRecord",
    "ErrorHandler",
    "GracefulDegradation",
    "RecoveryManager",
    "HealthChecks",
    "StabilityManager",
    "get_stability",
]