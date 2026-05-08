"""
Universe IDE - Analytics Engine

Advanced analytics and insights.
"""

import json
import random
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Optional


# ============================================================================
# ANALYTICS DATA
# ============================================================================

@dataclass
class Event:
    """Analytics event"""
    event_type: str
    timestamp: datetime
    properties: dict = field(default_factory=dict)
    user_id: str = ""


# ============================================================================
# ANALYTICS ENGINE
# ============================================================================

class AnalyticsEngine:
    """
    Analytics and insights engine.
    """
    
    def __init__(self):
        self.events: list[Event] = []
        self.metrics: dict[str, list] = defaultdict(list)
        
    def track(self, event_type: str, properties: dict = None, user_id: str = ""):
        """Track event"""
        event = Event(
            event_type=event_type,
            timestamp=datetime.now(),
            properties=properties or {},
            user_id=user_id,
        )
        self.events.append(event)
        
    def track_metric(self, name: str, value: float):
        """Track metric value"""
        self.metrics[name].append({
            "value": value,
            "timestamp": datetime.now(),
        })
        
    def get_events(self, event_type: str = None, since: datetime = None) -> list:
        """Get events"""
        events = self.events
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
            
        if since:
            events = [e for e in events if e.timestamp >= since]
            
        return events
        
    def get_metric(self, name: str, duration_seconds: int = 60) -> dict:
        """Get metric stats"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=duration_seconds)
        
        values = [
            m["value"] for m in self.metrics[name]
            if m["timestamp"] >= cutoff
        ]
        
        if not values:
            return {"count": 0, "avg": 0, "min": 0, "max": 0}
            
        return {
            "count": len(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "sum": sum(values),
        }


# ============================================================================
# FUNNEL ANALYTICS
# ============================================================================

class FunnelAnalytics:
    """
    Funnel conversion tracking.
    """
    
    def __init__(self, steps: list[str]):
        self.steps = steps
        self.conversions: dict[str, int] = {s: 0 for s in steps}
        
    def track_conversion(self, step: str):
        """Track conversion at step"""
        if step in self.conversions:
            self.conversions[step] += 1
            
    def get_funnel(self) -> list[dict]:
        """Get funnel data"""
        results = []
        prev = None
        
        for step in self.steps:
            count = self.conversions[step]
            conversion_rate = 0
            
            if prev and prev > 0:
                conversion_rate = (count / prev) * 100
                
            results.append({
                "step": step,
                "count": count,
                "conversion_rate": conversion_rate,
            })
            
            prev = count
            
        return results


# ============================================================================
# COHORT ANALYSIS
# ============================================================================

class CohortAnalytics:
    """
    Cohort analysis.
    """
    
    def __init__(self):
        self.cohorts: dict[str, dict] = {}
        
    def add_cohort(self, cohort_id: str, date: datetime):
        """Add cohort"""
        self.cohorts[cohort_id] = {
            "date": date,
            "users": set(),
            "metrics": defaultdict(list),
        }
        
    def add_user(self, cohort_id: str, user_id: str):
        """Add user to cohort"""
        if cohort_id in self.cohorts:
            self.cohorts[cohort_id]["users"].add(user_id)
            
    def track_metric(self, cohort_id: str, metric: str, value: float):
        """Track metric for cohort"""
        if cohort_id in self.cohorts:
            self.cohorts[cohort_id]["metrics"][metric].append(value)
            
    def get_cohort_report(self, cohort_id: str) -> dict:
        """Get cohort report"""
        if cohort_id not in self.cohorts:
            return {}
            
        cohort = self.cohorts[cohort_id]
        
        return {
            "cohort_id": cohort_id,
            "date": cohort["date"].isoformat(),
            "users": len(cohort["users"]),
            "metrics": {
                m: sum(v) / len(v) if v else 0
                for m, v in cohort["metrics"].items()
            },
        }


# ============================================================================
# DASHBOARD
# ============================================================================

class AnalyticsDashboard:
    """
    Analytics dashboard.
    """
    
    def __init__(self):
        self.engine = AnalyticsEngine()
        self.funnels: dict[str, FunnelAnalytics] = {}
        self.cohorts = CohortAnalytics()
        
    def track(self, event_type: str, properties: dict = None):
        """Track event"""
        self.engine.track(event_type, properties)
        
    def create_funnel(self, name: str, steps: list[str]) -> FunnelAnalytics:
        """Create funnel"""
        funnel = FunnelAnalytics(steps)
        self.funnels[name] = funnel
        return funnel
        
    def get_report(self, duration_seconds: int = 3600) -> dict:
        """Get analytics report"""
        # Calculate key metrics
        events = self.engine.get_events(since=datetime.now() - timedelta(seconds=duration_seconds))
        
        return {
            "total_events": len(events),
            "unique_event_types": len(set(e.event_type for e in events)),
            "events_by_type": self._group_by_type(events),
            "funnels": {
                name: f.get_funnel()
                for name, f in self.funnels.items()
            },
            "generated_at": datetime.now().isoformat(),
        }
        
    def _group_by_type(self, events: list[Event]) -> dict:
        """Group by event type"""
        by_type = defaultdict(int)
        for e in events:
            by_type[e.event_type] += 1
        return dict(by_type)


# Global
_analytics = None

def get_analytics() -> AnalyticsDashboard:
    """Get analytics dashboard"""
    global _analytics
    if _analytics is None:
        _analytics = AnalyticsDashboard()
    return _analytics


__all__ = [
    "Event",
    "AnalyticsEngine",
    "FunnelAnalytics",
    "CohortAnalytics",
    "AnalyticsDashboard",
    "get_analytics",
]