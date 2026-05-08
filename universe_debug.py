"""
Universe IDE - Metrics & Debugging

Performance monitoring and debugging tools.
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# METRICS
# ============================================================================

@dataclass
class Metric:
    """Metric data point"""
    name: str
    value: float
    unit: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


class MetricsCollector:
    """
    Collect and aggregate metrics.
    """
    
    def __init__(self):
        self.metrics: dict[str, list[Metric]] = {}
        self.counters: dict[str, int] = {}
        self.gauges: dict[str, float] = {}
        self.histograms: dict[str, list[float]] = {}
        
    def increment(self, name: str, value: int = 1):
        """Increment counter"""
        self.counters[name] = self.counters.get(name, 0) + value
        
    def gauge(self, name: str, value: float):
        """Set gauge value"""
        self.gauges[name] = value
        
    def histogram(self, name: str, value: float):
        """Add to histogram"""
        if name not in self.histograms:
            self.histograms[name] = []
        self.histograms[name].append(value)
        
    def get_counter(self, name: str) -> int:
        """Get counter value"""
        return self.counters.get(name, 0)
        
    def get_gauge(self, name: str) -> float:
        """Get gauge value"""
        return self.gauges.get(name, 0.0)
        
    def get_histogram_stats(self, name: str) -> dict:
        """Get histogram statistics"""
        values = self.histograms.get(name, [])
        if not values:
            return {"count": 0}
            
        sorted_values = sorted(values)
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "p50": sorted_values[len(values) // 2],
            "p95": sorted_values[int(len(values) * 0.95)],
            "p99": sorted_values[int(len(values) * 0.99)],
        }
        
    def all_metrics(self) -> dict:
        """Get all metrics"""
        return {
            "counters": self.counters,
            "gauges": self.gauges,
            "histograms": {
                k: self.get_histogram_stats(k) 
                for k in self.histograms
            },
        }


# ============================================================================
# PERFORMANCE TIMER
# ============================================================================

class PerformanceTimer:
    """Time code execution"""
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = 0
        self.end_time = 0
        
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
        
    def __exit__(self, *args):
        self.end_time = time.perf_counter()
        
    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in ms"""
        return (self.end_time - self.start_time) * 1000


# ============================================================================
# DEBUGGER
# ============================================================================

class Debugger:
    """
    Integrated debugger.
    """
    
    def __init__(self):
        self.breakpoints: dict[str, set[int]] = {}
        self.watches: dict[str, Any] = {}
        self.stepping = False
        
    def set_breakpoint(self, file: str, line: int):
        """Set breakpoint"""
        if file not in self.breakpoints:
            self.breakpoints[file] = set()
        self.breakpoints[file].add(line)
        
    def remove_breakpoint(self, file: str, line: int):
        """Remove breakpoint"""
        if file in self.breakpoints:
            self.breakpoints[file].discard(line)
            
    def watch(self, variable: str, value: Any):
        """Watch variable"""
        self.watches[variable] = value
        
    def get_watches(self) -> dict[str, Any]:
        """Get watched variables"""
        return self.watches.copy()
        
    def step(self):
        """Step execution"""
        self.stepping = True
        
    def cont(self):
        """Continue execution"""
        self.stepping = False


# ============================================================================
# LOG TRACER
# ============================================================================

class LogTracer:
    """Trace execution logs"""
    
    LEVELS = ["DEBUG", "INFO", "WARN", "ERROR"]
    
    def __init__(self):
        self.logs: list[dict] = []
        self.level = 1  # INFO
        
    def log(self, level: str, message: str, **kwargs):
        """Add log entry"""
        if self.LEVELS.index(level) >= self.level:
            self.logs.append({
                "level": level,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                **kwargs,
            })
            
    def debug(self, message: str, **kwargs):
        self.log("DEBUG", message, **kwargs)
        
    def info(self, message: str, **kwargs):
        self.log("INFO", message, **kwargs)
        
    def warn(self, message: str, **kwargs):
        self.log("WARN", message, **kwargs)
        
    def error(self, message: str, **kwargs):
        self.log("ERROR", message, **kwargs)
        
    def get_logs(self, level: str = None) -> list[dict]:
        """Get logs"""
        if level:
            return [l for l in self.logs if l["level"] == level]
        return self.logs
        
    def clear(self):
        """Clear logs"""
        self.logs.clear()


# ============================================================================
# PROFILER
# ============================================================================

class Profiler:
    """Profile code execution"""
    
    def __init__(self):
        self.profiles: dict[str, float] = {}
        
    def profile(self, func: Callable) -> Callable:
        """Decorator to profile function"""
        name = func.__name__
        
        async def async_profiled(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            self.profiles[name] = self.profiles.get(name, 0) + elapsed
            return result
            
        def sync_profiled(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            self.profiles[name] = self.profiles.get(name, 0) + elapsed
            return result
            
        if asyncio.iscoroutinefunction(func):
            return async_profiled
        return sync_profiled
        
    def get_report(self) -> dict:
        """Get profiling report"""
        return dict(sorted(
            self.profiles.items(), 
            key=lambda x: x[1], 
            reverse=True
        ))


# Global
_metrics = None

def get_metrics() -> MetricsCollector:
    """Get metrics collector"""
    global _metrics
    if _metrics is None:
        _metrics = MetricsCollector()
    return _metrics


__all__ = [
    "Metric",
    "MetricsCollector",
    "PerformanceTimer",
    "Debugger",
    "LogTracer",
    "Profiler",
    "get_metrics",
]