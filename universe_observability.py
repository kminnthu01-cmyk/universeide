"""
Universe IDE - Observability Module

Metrics, tracing, and logging.
"""

from typing import Any, Dict, List
import time
from collections import deque


# ============================================================================
# METRICS
# ============================================================================

class MetricsCollector:
    """Collect system metrics"""
    
    def __init__(self):
        self.metrics = {}
        
    def record(self, name: str, value: float):
        if name not in self.metrics:
            self.metrics[name] = deque(maxlen=1000)
        self.metrics[name].append({"value": value, "timestamp": time.time()})
        
    def get(self, name: str) -> Dict:
        if name not in self.metrics:
            return {}
        values = list(self.metrics[name])
        return {
            "count": len(values),
            "avg": sum(v["value"] for v in values) / len(values) if values else 0,
            "min": min(v["value"] for v in values) if values else 0,
            "max": max(v["value"] for v in values) if values else 0,
        }
        
    def all(self) -> Dict:
        return {name: self.get(name) for name in self.metrics}


# ============================================================================
# TRACER
# ============================================================================

class Tracer:
    """Distributed tracing"""
    
    def __init__(self):
        self.spans = {}
        self.active = {}
        
    def start_span(self, name: str, trace_id: str = None) -> str:
        if not trace_id:
            trace_id = f"trace_{time.time()}"
        self.active[trace_id] = {"name": name, "start": time.time()}
        return trace_id
        
    def end_span(self, trace_id: str):
        if trace_id in self.active:
            span = self.active.pop(trace_id)
            span["end"] = time.time()
            span["duration"] = span["end"] - span["start"]
            self.spans[trace_id] = span
            return span
        return {}


# ============================================================================
# LOGGER
# ============================================================================

class StructuredLogger:
    """Structured logging"""
    
    def __init__(self, service: str = "universe"):
        self.service = service
        
    def log(self, level: str, message: str, **kwargs):
        entry = {
            "timestamp": time.time(),
            "level": level,
            "message": message,
            "service": self.service,
            **kwargs
        }
        print(f"[{level.upper()}] {message}")


# ============================================================================
# OBSERVABILITY
# ============================================================================

class Observability:
    """Complete observability"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.tracer = Tracer()
        self.logger = StructuredLogger()


# Global
_observability = None

def get_observability() -> Observability:
    global _observability
    if _observability is None:
        _observability = Observability()
    return _observability


__all__ = ["MetricsCollector", "Tracer", "StructuredLogger", "Observability", "get_observability"]