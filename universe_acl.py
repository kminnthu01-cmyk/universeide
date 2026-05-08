"""
Universe IDE - ACL Module

Access control.
"""

from typing import Any, Callable, Dict, List


# ============================================================================
# PERMISSION
# ============================================================================

class Permission:
    """Permission"""
    
    def __init__(self, name: str, resource: str, action: str):
        self.name = name
        self.resource = resource
        self.action = action


# ============================================================================
# ACL
# ============================================================================

class ACL:
    """Access control"""
    
    def __init__(self):
        self.permissions = {}
        
    def grant(self, user: str, permission: Permission):
        if user not in self.permissions:
            self.permissions[user] = []
        self.permissions[user].append(permission)
        
    def check(self, user: str, resource: str, action: str) -> bool:
        if user not in self.permissions:
            return False
        for p in self.permissions[user]:
            if p.resource == resource and p.action == action:
                return True
        return False


# Global
_acl = None

def get_acl() -> ACL:
    global _acl
    if _acl is None:
        _acl = ACL()
    return _acl


__all__ = ["Permission", "ACL", "get_acl"]