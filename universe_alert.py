"""
Universe IDE - Alert Module

Alert management.
"""

from typing import Any, Callable, Dict, List


# ============================================================================
# ALERT
# ============================================================================

class Alert:
    """Alert"""
    
    def __init__(self, alert_id: str, message: str, severity: str = "info"):
        self.alert_id = alert_id
        self.message = message
        self.severity = severity
        self.created_at = 0


# ============================================================================
# ALERT MANAGER
# ============================================================================

class AlertManager:
    """Alert manager"""
    
    def __init__(self):
        self.alerts = []
        
    def create(self, alert_id: str, message: str, severity: str = "info") -> Alert:
        alert = Alert(alert_id, message, severity)
        self.alerts.append(alert)
        return alert


__all__ = ["Alert", "AlertManager"]