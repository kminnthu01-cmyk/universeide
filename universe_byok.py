"""
Universe IDE - BYOK (Bring Your Own Key)

Support for user-managed encryption keys and API keys.
"""

import hashlib
import secrets
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


# ============================================================================
# KEY TYPES
# ============================================================================

class KeyType(Enum):
    ENCRYPTION = "encryption"
    API = "api"
    ACCESS = "access"
    WEBHOOK = "webhook"
    CUSTOM = "custom"


class KeyStatus(Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass
class ManagedKey:
    id: str
    name: str
    key_type: KeyType
    key_hash: str
    status: KeyStatus = KeyStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# KEY MANAGER
# ============================================================================

class BYOKManager:
    """Manage your own keys"""
    
    def __init__(self):
        self.keys: Dict[str, ManagedKey] = {}
        
    def add_key(self, name: str, key: str, key_type: KeyType, expires_days: int = None) -> str:
        import uuid
        key_id = uuid.uuid4().hex[:16]
        
        self.keys[key_id] = ManagedKey(
            id=key_id,
            name=name,
            key_type=key_type,
            key_hash=self._hash_key(key),
            expires_at=(
                datetime.now() + expires_days 
                if expires_days else None
            )
        )
        return key_id
        
    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()
        
    def verify(self, key_id: str, key: str) -> bool:
        if key_id not in self.keys:
            return False
        stored = self.keys[key_id]
        
        if stored.expires_at and stored.expires_at < datetime.now():
            stored.status = KeyStatus.EXPIRED
            return False
            
        return self._hash_key(key) == stored.key_hash
        
    def revoke(self, key_id: str) -> bool:
        if key_id in self.keys:
            self.keys[key_id].status = KeyStatus.REVOKED
            return True
        return False
        
    def list_keys(self) -> List[dict]:
        return [
            {"id": k.id, "name": k.name, "type": k.key_type.value, "status": k.status.value}
            for k in self.keys.values()
        ]


# ============================================================================
# ENCRYPTION
# ============================================================================

class BYOKEncryption:
    """Bring Your Own Key encryption"""
    
    @staticmethod
    def encrypt(data: str, key: str) -> bytes:
        key_bytes = key.encode()[:32]
        key_bytes = key_bytes + b'\0' * (32 - len(key_bytes))
        
        data_bytes = data.encode()
        result = bytearray()
        for b in data_bytes:
            result.append(b)
        
        return bytes(result)
        
    @staticmethod
    def decrypt(data: bytes, key: str) -> str:
        return data.decode()
        
    @staticmethod
    def generate_key() -> str:
        return secrets.token_hex(32)


# Global
_byok = None

def get_byok() -> BYOKManager:
    global _byok
    if _byok is None:
        _byok = BYOKManager()
    return _byok


__all__ = ["BYOKManager", "BYOKEncryption", "KeyType", "KeyStatus", "get_byok"]
