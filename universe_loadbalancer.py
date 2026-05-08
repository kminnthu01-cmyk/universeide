"""
Universe IDE - Load Balancer Module

Load balancing.
"""

from typing import Any, Callable, Dict, List
import random


# ============================================================================
# NODE
# ============================================================================

class Node:
    """Load balancer node"""
    
    def __init__(self, node_id: str, weight: int = 1):
        self.node_id = node_id
        self.weight = weight
        self.requests = 0
        
    def handle(self, request: Any) -> Dict:
        self.requests += 1
        return {"node": self.node_id, "handled": True}


# ============================================================================
# LOAD BALANCER
# ============================================================================

class LoadBalancer:
    """Load balancer"""
    
    def __init__(self, algorithm: str = "round_robin"):
        self.nodes = []
        self.algorithm = algorithm
        self.current = 0
        
    def add_node(self, node_id: str, weight: int = 1):
        self.nodes.append(Node(node_id, weight))
        
    def route(self, request: Any) -> Dict:
        if not self.nodes:
            return {"error": "No nodes"}
            
        if self.algorithm == "round_robin":
            node = self.nodes[self.current % len(self.nodes)]
            self.current += 1
        elif self.algorithm == "random":
            node = random.choice(self.nodes)
        else:  # weighted
            node = random.choice(self.nodes)
            
        return node.handle(request)
        
    def get_status(self) -> List[Dict]:
        return [{"node": n.node_id, "requests": n.requests} for n in self.nodes]


# Global
_lb = None

def get_load_balancer() -> LoadBalancer:
    global _lb
    if _lb is None:
        _lb = LoadBalancer()
    return _lb


__all__ = ["Node", "LoadBalancer", "get_load_balancer"]