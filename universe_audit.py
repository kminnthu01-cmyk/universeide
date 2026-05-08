"""
Universe IDE - Audit Module

Audit logging and compliance.
"""

from typing import Any, Callable, Dict, List
import time
from collections import deque


# ============================================================================
# AUDIT LOG
# ============================================================================

class AuditLog:
    """Audit log entry"""
    
    def __init__(self, action: str, user: str, resource: str):
        self.action = action
        self.user = user
        self.resource = resource
        self.timestamp = time.time()
        self.result = "success"
        
    def to_dict(self) -> Dict:
        return {
            "action": self.action,
            "user": self.user,
            "resource": self.resource,
            "timestamp": self.timestamp,
            "result": self.result,
        }


# ============================================================================
# AUDIT TRAIL
# ============================================================================

class AuditTrail:
    """Audit trail tracking"""
    
    def __init__(self, max_entries: int = 10000):
        self.entries = deque(maxlen=max_entries)
        
    def log(self, action: str, user: str, resource: str):
        entry = AuditLog(action, user, resource)
        self.entries.append(entry)
        return entry
        
    def search(self, user: str = None, action: str = None) -> List[Dict]:
        results = []
        for entry in self.entries:
            if user and entry.user != user:
                continue
            if action and entry.action != action:
                continue
            results.append(entry.to_dict())
        return results
        
    def recent(self, count: int = 10) -> List[Dict]:
        return [e.to_dict() for e in list(self.entries)[-count:]]


# ============================================================================
# COMPLIANCE
# ============================================================================

class ComplianceChecker:
    """Check compliance rules"""
    
    def __init__(self):
        self.rules = {}
        
    def add_rule(self, name: str, checker: Callable):
        self.rules[name] = checker
        
    def check(self, data: Dict) -> Dict:
        results = {}
        for name, checker in self.rules.items():
            try:
                results[name] = checker(data)
            except:
                results[name] = False
        return results


# Global
_audit = None

def get_audit() -> AuditTrail:
    global _audit
    if _audit is None:
        _audit = AuditTrail()
    return _audit


__all__ = ["AuditLog", "AuditTrail", "ComplianceChecker", "get_audit"]