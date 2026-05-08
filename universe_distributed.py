"""
Universe IDE - Distributed Computing

Multi-node, distributed agent orchestration.
"""

import asyncio
import hashlib
import json
import os
import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


# ============================================================================
# NODE DISCOVERY
# ============================================================================

@dataclass
class NodeInfo:
    """A node in the distributed system"""
    node_id: str
    address: str
    port: int
    capacity: int
    status: str = "online"
    last_seen: datetime = field(default_factory=datetime.now)


class NodeRegistry:
    """
    Registry of nodes in the cluster.
    """
    
    def __init__(self):
        self.nodes: dict[str, NodeInfo] = {}
        self.local_node = f"node_{uuid.uuid4().hex[:8]}"
        
    def register_node(self, node: NodeInfo):
        """Register a node"""
        self.nodes[node.node_id] = node
        
    def unregister_node(self, node_id: str):
        """Unregister a node"""
        if node_id in self.nodes:
            del self.nodes[node_id]
            
    def get_nodes(self, status: Optional[str] = None) -> list[NodeInfo]:
        """Get nodes"""
        nodes = list(self.nodes.values())
        if status:
            nodes = [n for n in nodes if n.status == status]
        return nodes
        
    def get_leader(self) -> Optional[NodeInfo]:
        """Get leader node"""
        online = self.get_nodes("online")
        if not online:
            return None
        # Simple leader election
        return min(online, key=lambda n: n.node_id)


# ============================================================================
# DISTRIBUTED TASK QUEUE
# ============================================================================

@dataclass
class DistributedTask:
    """A distributed task"""
    task_id: str
    payload: dict
    status: str = "pending"
    assigned_to: Optional[str] = None
    result: Optional[Any] = None
    created_at: datetime = field(default_factory=datetime.now)


class DistributedQueue:
    """
    Distributed task queue.
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.pending: list[DistributedTask] = []
        self.processing: dict[str, DistributedTask] = {}
        self.completed: dict[str, DistributedTask] = {}
        
    def enqueue(self, payload: dict) -> str:
        """Add task to queue"""
        task = DistributedTask(
            task_id=f"task_{uuid.uuid4().hex[:12]}",
            payload=payload,
        )
        self.pending.append(task)
        return task.task_id
        
    def dequeue(self) -> Optional[DistributedTask]:
        """Get next task"""
        if not self.pending:
            return None
        task = self.pending.pop(0)
        task.status = "processing"
        task.assigned_to = self.node_id
        self.processing[task.task_id] = task
        return task
        
    def complete(self, task_id: str, result: Any):
        """Mark task complete"""
        if task_id in self.processing:
            task = self.processing.pop(task_id)
            task.status = "completed"
            task.result = result
            self.completed[task_id] = task
            
    def get_status(self) -> dict:
        """Get queue status"""
        return {
            "pending": len(self.pending),
            "processing": len(self.processing),
            "completed": len(self.completed),
        }


# ============================================================================
# SHARDING
# ============================================================================

class ShardManager:
    """
    Data sharding for distributed storage.
    """
    
    def __init__(self, num_shards: int = 8):
        self.num_shards = num_shards
        self.shards: dict[int, list] = {i: [] for i in range(num_shards)}
        
    def _get_shard(self, key: str) -> int:
        """Get shard for key"""
        hash_val = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return hash_val % self.num_shards
        
    def put(self, key: str, value: Any):
        """Put value"""
        shard = self._get_shard(key)
        self.shards[shard].append((key, value))
        
    def get(self, key: str) -> Optional[Any]:
        """Get value"""
        shard = self._get_shard(key)
        for k, v in self.shards[shard]:
            if k == key:
                return v
        return None
        
    def get_shard分布(self) -> dict:
        """Get distribution"""
        return {shard: len(items) for shard, items in self.shards.items()}


# ============================================================================
# CONSENSUS (RAFT-LIKE)
# ============================================================================

class ConsensusModule:
    """
    Consensus for leader election.
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.votes: dict[str, str] = {}
        self.is_leader = False
        
    def request_vote(self, candidate_id: str) -> bool:
        """Request vote from node"""
        # Simple random election
        should_vote = random.random() > 0.5
        if should_vote:
            self.votes[candidate_id] = self.node_id
        return should_vote
        
    def become_leader(self) -> bool:
        """Become leader"""
        if len(self.votes) > len(self.votes) // 2:
            self.is_leader = True
            return True
        return False


# ============================================================================
# DISTRIBUTED CACHE
# ============================================================================

class DistributedCache:
    """
    Distributed cache with invalidate.
    """
    
    def __init__(self):
        self.local_cache: dict = {}
        self.version: int = 0
        
    def set(self, key: str, value: Any):
        """Set value"""
        self.local_cache[key] = value
        self.version += 1
        
    def get(self, key: str) -> Optional[Any]:
        """Get value"""
        return self.local_cache.get(key)
        
    def invalidate(self, key: str):
        """Invalidate key"""
        if key in self.local_cache:
            del self.local_cache[key]
            self.version += 1
            
    def broadcast_invalidate(self, key: str):
        """Broadcast to other nodes"""
        print(f"  Would broadcast invalidate: {key}")


# ============================================================================
# Gossip Protocol
# ============================================================================

class GossipProtocol:
    """
    Gossip for eventual consistency.
    """
    
    def __init__(self, node_id: str, peers: list[str]):
        self.node_id = node_id
        self.peers = peers
        self.state: dict = {}
        
    def share(self, key: str, value: Any):
        """Share state"""
        self.state[key] = value
        
    def gossip(self):
        """Gossip with random peers"""
        if not self.peers:
            return []
        # Pick random peers
        k = min(3, len(self.peers))
        targets = random.sample(self.peers, k)
        for peer in targets:
            print(f"  Gossiping with {peer}")
        return targets


# ============================================================================
# DISTRIBUTED ORCHESTRATOR
# ============================================================================

class DistributedOrchestrator:
    """
    Full distributed orchestration.
    """
    
    def __init__(self, node_id: str, num_nodes: int = 4):
        self.node_id = node_id
        self.registry = NodeRegistry()
        self.queue = DistributedQueue(node_id)
        self.shard = ShardManager(num_nodes)
        self.consensus = ConsensusModule(node_id)
        self.cache = DistributedCache()
        self.gossip = GossipProtocol(node_id, [])
        
    def add_node(self, address: str, port: int, capacity: int):
        """Add node to cluster"""
        node = NodeInfo(
            node_id=f"node_{uuid.uuid4().hex[:8]}",
            address=address,
            port=port,
            capacity=capacity,
        )
        self.registry.register_node(node)
        return node.node_id
        
    def submit_task(self, payload: dict) -> str:
        """Submit distributed task"""
        return self.queue.enqueue(payload)
        
    def process_task(self) -> Optional[dict]:
        """Process next task"""
        task = self.queue.dequeue()
        if not task:
            return None
        # Simulate processing
        result = {"status": "done", "node": self.node_id}
        self.queue.complete(task.task_id, result)
        return result
        
    def get_status(self) -> dict:
        """Get cluster status"""
        nodes = self.registry.get_nodes()
        return {
            "nodes": len(nodes),
            "leader": self.registry.get_leader(),
            "queue": self.queue.get_status(),
            "shards": self.shard.get_shard分布(),
            "is_leader": self.consensus.is_leader,
        }


# Global instance
_distributed = None

def get_distributed(node_id: str = None) -> DistributedOrchestrator:
    """Get distributed orchestrator"""
    global _distributed
    if _distributed is None:
        _distributed = DistributedOrchestrator(node_id or f"node_{uuid.uuid4().hex[:8]}")
    return _distributed


__all__ = [
    "NodeInfo",
    "NodeRegistry", 
    "DistributedTask",
    "DistributedQueue",
    "ShardManager",
    "ConsensusModule",
    "DistributedCache",
    "GossipProtocol",
    "DistributedOrchestrator",
    "get_distributed",
]