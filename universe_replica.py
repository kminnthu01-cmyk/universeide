"""
Universe IDE - Replica Module

Data replication.
"""

from typing import Any, Dict, List


# ============================================================================
# REPLICA
# ============================================================================

class Replica:
    """Data replica"""
    
    def __init__(self, replica_id: str):
        self.replica_id = replica_id
        self.data = {}
        
    def write(self, key: str, value: Any):
        self.data[key] = value
        
    def read(self, key: str) -> Any:
        return self.data.get(key)


# ============================================================================
# REPLICA SET
# ============================================================================

class ReplicaSet:
    """Replica set"""
    
    def __init__(self):
        self.replicas = []
        
    def add(self, replica: Replica):
        self.replicas.append(replica)
        
    def write(self, key: str, value: Any):
        for r in self.replicas:
            r.write(key, value)
            
    def read(self, key: str) -> Any:
        if self.replicas:
            return self.replicas[0].read(key)
        return None


__all__ = ["Replica", "ReplicaSet"]