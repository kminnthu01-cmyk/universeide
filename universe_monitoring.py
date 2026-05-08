"""
Universe IDE - Monitoring & Telemetry

Features:
- Real-time metrics
- Event tracking
- Performance monitoring
- Alerting
- Dashboard data
"""

import json
import os
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# METRICS
# ============================================================================

@dataclass
class Metric:
    """A single metric"""
    name: str
    value: float
    timestamp: datetime
    tags: dict = field(default_factory=dict)


class MetricsCollector:
    """
    Collect and aggregate metrics.
    """
    
    def __init__(self, max_points: int = 1000):
        self.max_points = max_points
        self.metrics: dict[str, deque] = {}
        
    def record(self, name: str, value: float, tags: Optional[dict] = None):
        """Record a metric"""
        if name not in self.metrics:
            self.metrics[name] = deque(maxlen=self.max_points)
            
        metric = Metric(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {},
        )
        self.metrics[name].append(metric)
        
    def get(self, name: str, duration_seconds: int = 60) -> list:
        """Get metrics for duration"""
        if name not in self.metrics:
            return []
            
        cutoff = datetime.now() - timedelta(seconds=duration_seconds)
        return [m for m in self.metrics[name] if m.timestamp >= cutoff]
        
    def average(self, name: str, duration_seconds: int = 60) -> float:
        """Get average for duration"""
        metrics = self.get(name, duration_seconds)
        if not metrics:
            return 0
        return sum(m.value for m in metrics) / len(metrics)
        
    def get_all(self) -> dict:
        """Get all metric names"""
        return list(self.metrics.keys())


# ============================================================================
# EVENT TRACKING
# ============================================================================

@dataclass
class Event:
    """A tracked event"""
    name: str
    timestamp: datetime
    data: dict = field(default_factory=dict)


class EventTracker:
    """
    Track events for analysis.
    """
    
    def __init__(self, max_events: int = 10000):
        self.max_events = max_events
        self.events: deque = deque(maxlen=max_events)
        
    def track(self, name: str, data: Optional[dict] = None):
        """Track an event"""
        event = Event(
            name=name,
            timestamp=datetime.now(),
            data=data or {},
        )
        self.events.append(event)
        
    def get_events(
        self, 
        name: Optional[str] = None,
        since: Optional[datetime] = None
    ) -> list:
        """Get events"""
        events = list(self.events)
        
        if name:
            events = [e for e in events if e.name == name]
            
        if since:
            events = [e for e in events if e.timestamp >= since]
            
        return events
        
    def count(self, name: str, since: Optional[datetime] = None) -> int:
        """Count events"""
        return len(self.get_events(name, since))


# ============================================================================
# PERFORMANCE MONITOR
# ============================================================================

class PerformanceMonitor:
    """
    Monitor performance metrics.
    """
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.timers: dict[str, float] = {}
        
    def start_timer(self, name: str):
        """Start a timer"""
        self.timers[name] = time.time()
        
    def stop_timer(self, name: str) -> float:
        """Stop timer and record"""
        if name not in self.timers:
            return 0
            
        elapsed = time.time() - self.timers[name]
        del self.timers[name]
        
        # Record metric
        self.metrics.record(f"timer.{name}", elapsed * 1000)  # ms
        
        return elapsed
        
    def record_metric(self, name: str, value: float):
        """Record a metric"""
        self.metrics.record(name, value)
        
    def get_stats(self) -> dict:
        """Get performance stats"""
        stats = {}
        for name in self.metrics.get_all():
            avg = self.metrics.average(name)
            stats[name] = {
                "average": avg,
                "count": len(self.metrics.get(name)),
            }
        return stats


# ============================================================================
# ALERTING
# ============================================================================

class AlertLevel(Enum):
    """Alert levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Alert:
    """An alert"""
    level: AlertLevel
    message: str
    timestamp: datetime
    source: str


class AlertingSystem:
    """
    Alerting system.
    """
    
    def __init__(self):
        self.alerts: deque = deque(maxlen=100)
        self.handlers: list[Callable] = []
        self.rules: dict = {}
        
    def add_handler(self, handler: Callable):
        """Add alert handler"""
        self.handlers.append(handler)
        
    def add_rule(self, name: str, condition: Callable, level: AlertLevel):
        """Add alert rule"""
        self.rules[name] = {"condition": condition, "level": level}
        
    def trigger(self, level: AlertLevel, message: str, source: str = "system"):
        """Trigger an alert"""
        alert = Alert(
            level=level,
            message=message,
            timestamp=datetime.now(),
            source=source,
        )
        self.alerts.append(alert)
        
        # Call handlers
        for handler in self.handlers:
            try:
                handler(alert)
            except:
                pass
                
    def check_rules(self, metrics: dict):
        """Check alert rules"""
        for name, rule in self.rules.items():
            try:
                if rule["condition"](metrics):
                    self.trigger(rule["level"], f"Alert: {name}", name)
            except:
                pass
                
    def get_alerts(
        self, 
        level: Optional[AlertLevel] = None,
        since: Optional[datetime] = None
    ) -> list:
        """Get alerts"""
        alerts = list(self.alerts)
        
        if level:
            alerts = [a for a in alerts if a.level == level]
            
        if since:
            alerts = [a for a in alerts if a.timestamp >= since]
            
        return alerts


# ============================================================================
# MONITORING DASHBOARD
# ============================================================================

class MonitoringDashboard:
    """
    Unified monitoring.
    """
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.events = EventTracker()
        self.performance = PerformanceMonitor()
        self.alerts = AlertingSystem()
        
    def record_metric(self, name: str, value: float, tags: Optional[dict] = None):
        """Record a metric"""
        self.metrics.record(name, value, tags)
        
    def track_event(self, name: str, data: Optional[dict] = None):
        """Track event"""
        self.events.track(name, data)
        
    def start_timer(self, name: str):
        """Start timer"""
        self.performance.start_timer(name)
        
    def stop_timer(self, name: str) -> float:
        """Stop timer"""
        return self.performance.stop_timer(name)
        
    def alert(self, level: AlertLevel, message: str):
        """Trigger alert"""
        self.alerts.trigger(level, message)
        
    def get_snapshot(self) -> dict:
        """Get dashboard snapshot"""
        return {
            "metrics": {
                name: self.metrics.average(name)
                for name in self.metrics.get_all()
            },
            "events": {
                "total": len(self.events.events),
                "recent": self.events.count("task", since=datetime.now() - timedelta(minutes=5)),
            },
            "performance": self.performance.get_stats(),
            "alerts": {
                "total": len(self.alerts.alerts),
                "critical": len(self.alerts.get_alerts(AlertLevel.CRITICAL)),
            },
            "timestamp": datetime.now().isoformat(),
        }


# Global instance
_monitoring = None

def get_monitoring() -> MonitoringDashboard:
    """Get monitoring dashboard"""
    global _monitoring
    if _monitoring is None:
        _monitoring = MonitoringDashboard()
    return _monitoring


__all__ = [
    "MetricsCollector",
    "EventTracker",
    "PerformanceMonitor",
    "AlertingSystem",
    "MonitoringDashboard",
    "AlertLevel",
    "get_monitoring",
]