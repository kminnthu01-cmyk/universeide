"""
Universe IDE - Security Hardening

Advanced security features.
"""

import hashlib
import hmac
import os
import secrets
import string
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional


# ============================================================================
# SECURITY LEVELS
# ============================================================================

class SecurityLevel(Enum):
    """Security clearance levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"


# ============================================================================
# PERMISSIONS
# ============================================================================

@dataclass
class Permission:
    """A permission"""
    name: str
    level: SecurityLevel = SecurityLevel.PUBLIC
    resource: str = "*"
    action: str = "*"


# ============================================================================
# ACCESS CONTROL
# ============================================================================

class AccessControl:
    """
    Role-based access control.
    """
    
    def __init__(self):
        self.roles: dict[str, set[str]] = {}
        self.permissions: dict[str, Permission] = {}
        self.user_roles: dict[str, set[str]] = {}
        
    def add_role(self, role: str, permissions: list[str]):
        """Add role with permissions"""
        self.roles[role] = set(permissions)
        
    def assign_role(self, user_id: str, role: str):
        """Assign role to user"""
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        self.user_roles[user_id].add(role)
        
    def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has permission"""
        user_roles = self.user_roles.get(user_id, set())
        
        for role in user_roles:
            role_perms = self.roles.get(role, set())
            if permission in role_perms:
                return True
                
        return False
        
    def check_access(self, user_id: str, resource: str, action: str) -> bool:
        """Check resource access"""
        for role in self.user_roles.get(user_id, set()):
            for perm_name in self.roles.get(role, set()):
                perm = self.permissions.get(perm_name)
                if perm and (perm.resource == resource or perm.resource == "*"):
                    if perm.action == action or perm.action == "*":
                        return True
        return False


# ============================================================================
# ENCRYPTION
# ============================================================================

class Encryption:
    """
    Encryption utilities.
    """
    
    @staticmethod
    def generate_key(length: int = 32) -> str:
        """Generate encryption key"""
        return secrets.token_hex(length)
        
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate secure token"""
        return secrets.token_urlsafe(length)
        
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> str:
        """Hash password"""
        if not salt:
            salt = secrets.token_hex(16)
        hash_val = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        )
        return f"{salt}${hash_val.hex()}"
        
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password"""
        try:
            salt, hash_val = hashed.split("$")
            computed = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt.encode(),
                100000
            )
            return computed.hex() == hash_val
        except:
            return False


# ============================================================================
# API KEY MANAGEMENT
# ============================================================================

class APIKeyManager:
    """
    Manage API keys.
    """
    
    def __init__(self):
        self.keys: dict[str, dict] = {}
        
    def create_key(
        self, 
        name: str, 
        level: SecurityLevel = SecurityLevel.INTERNAL,
        expires_days: int = 90
    ) -> str:
        """Create API key"""
        key = f"univ_{secrets.token_urlsafe(32)}"
        
        self.keys[key] = {
            "name": name,
            "level": level,
            "created": datetime.now(),
            "expires": datetime.now() + timedelta(days=expires_days),
            "last_used": None,
        }
        
        return key
        
    def validate_key(self, key: str) -> bool:
        """Validate API key"""
        if key not in self.keys:
            return False
            
        key_data = self.keys[key]
        
        # Check expiration
        if datetime.now() > key_data["expires"]:
            return False
            
        # Update last used
        key_data["last_used"] = datetime.now()
        
        return True
        
    def revoke_key(self, key: str) -> bool:
        """Revoke API key"""
        if key in self.keys:
            del self.keys[key]
            return True
        return False


# ============================================================================
# RATE LIMITING
# ============================================================================

@dataclass
class RateLimit:
    """Rate limit"""
    requests: int
    window_seconds: int


class RateLimiter:
    """
    Rate limiting.
    """
    
    def __init__(self, default_limit: RateLimit = None):
        self.default_limit = default_limit or RateLimit(100, 60)
        self.limits: dict[str, list[datetime]] = {}
        
    def check_limit(self, identifier: str, limit: RateLimit = None) -> bool:
        """Check rate limit"""
        limit = limit or self.default_limit
        
        now = datetime.now()
        window = now - timedelta(seconds=limit.window_seconds)
        
        if identifier not in self.limits:
            self.limits[identifier] = []
            
        # Clean old requests
        self.limits[identifier] = [
            t for t in self.limits[identifier] if t > window
        ]
        
        # Check limit
        if len(self.limits[identifier]) >= limit.requests:
            return False
            
        self.limits[identifier].append(now)
        return True


# ============================================================================
# AUDIT LOG
# ============================================================================

@dataclass
class AuditEntry:
    """Audit log entry"""
    timestamp: datetime
    user: str
    action: str
    resource: str
    result: str
    ip_address: str = ""


class AuditLog:
    """
    Audit logging.
    """
    
    def __init__(self, max_entries: int = 10000):
        self.max_entries = max_entries
        self.entries: list[AuditEntry] = []
        
    def log(
        self, 
        user: str, 
        action: str, 
        resource: str,
        result: str,
        ip_address: str = ""
    ):
        """Log action"""
        entry = AuditEntry(
            timestamp=datetime.now(),
            user=user,
            action=action,
            resource=resource,
            result=result,
            ip_address=ip_address,
        )
        
        self.entries.append(entry)
        
        # Trim
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
            
    def get_logs(
        self, 
        user: Optional[str] = None,
        since: Optional[datetime] = None
    ) -> list[AuditEntry]:
        """Get audit logs"""
        logs = self.entries
        
        if user:
            logs = [e for e in logs if e.user == user]
            
        if since:
            logs = [e for e in logs if e.timestamp >= since]
            
        return logs


# ============================================================================
# SECURITY MANAGER
# ============================================================================

class SecurityManager:
    """
    Unified security management.
    """
    
    def __init__(self):
        self.access_control = AccessControl()
        self.api_keys = APIKeyManager()
        self.rate_limiter = RateLimiter()
        self.audit_log = AuditLog()
        self.encryption = Encryption()
        
    def authenticate(self, api_key: str) -> bool:
        """Authenticate via API key"""
        valid = self.api_keys.validate_key(api_key)
        if valid:
            self.audit_log.log("system", "authenticate", "api_key", "success")
        return valid
        
    def authorize(
        self, 
        user_id: str, 
        permission: str
    ) -> bool:
        """Authorize user"""
        has_perm = self.access_control.has_permission(user_id, permission)
        self.audit_log.log(user_id, "authorize", permission, 
                         "success" if has_perm else "denied")
        return has_perm
        
    def rate_limit(self, identifier: str) -> bool:
        """Check rate limit"""
        return self.rate_limiter.check_limit(identifier)


# Global instance
_security = None

def get_security() -> SecurityManager:
    """Get security manager"""
    global _security
    if _security is None:
        _security = SecurityManager()
    return _security


__all__ = [
    "SecurityLevel",
    "Permission",
    "AccessControl",
    "Encryption",
    "APIKeyManager",
    "RateLimit",
    "RateLimiter",
    "AuditEntry", 
    "AuditLog",
    "SecurityManager",
    "get_security",
]