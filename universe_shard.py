"""
Universe IDE - Shard Module

Data sharding.
"""

from typing import Any, Dict, List


# ============================================================================
# SHARD
# ============================================================================

class Shard:
    """Data shard"""
    
    def __init__(self, shard_id: str):
        self.shard_id = shard_id
        self.data = {}
        
    def write(self, key: str, value: Any):
        self.data[key] = value
        
    def read(self, key: str) -> Any:
        return self.data.get(key)


# ============================================================================
# SHARD MANAGER
# ============================================================================

class ShardManager:
    """Shard manager"""
    
    def __init__(self, num_shards: int = 4):
        self.num_shards = num_shards
        self.shards = [Shard(str(i)) for i in range(num_shards)]
        
    def get_shard(self, key: str) -> Shard:
        return self.shards[hash(key) % self.num_shards]


__all__ = ["Shard", "ShardManager"]