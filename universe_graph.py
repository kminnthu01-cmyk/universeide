"""
Universe IDE - Knowledge Graph Module

Graph database for knowledge representation.
"""

from typing import Any, Dict, List, Set, Optional
from collections import deque


# ============================================================================
# NODE
# ============================================================================

class Node:
    """Graph node"""
    
    def __init__(self, node_id: str, label: str, properties: Dict = None):
        self.node_id = node_id
        self.label = label
        self.properties = properties or {}
        self.edges = []
        
    def add_edge(self, edge: "Edge"):
        self.edges.append(edge)


# ============================================================================
# EDGE
# ============================================================================

class Edge:
    """Graph edge"""
    
    def __init__(self, from_node: Node, to_node: Node, relationship: str):
        self.from_node = from_node
        self.to_node = to_node
        self.relationship = relationship


# ============================================================================
# GRAPH
# ============================================================================

class KnowledgeGraph:
    """Knowledge graph"""
    
    def __init__(self):
        self.nodes = {}
        
    def add_node(self, node: Node):
        self.nodes[node.node_id] = node
        
    def add_edge(self, from_id: str, to_id: str, relationship: str):
        if from_id in self.nodes and to_id in self.nodes:
            edge = Edge(
                self.nodes[from_id],
                self.nodes[to_id],
                relationship
            )
            self.nodes[from_id].add_edge(edge)
            
    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)
        
    def find_path(self, from_id: str, to_id: str) -> List[str]:
        """BFS path finding"""
        if from_id not in self.nodes or to_id not in self.nodes:
            return []
            
        queue = deque([(from_id, [from_id])])
        visited = {from_id}
        
        while queue:
            current, path = queue.popleft()
            
            if current == to_id:
                return path
                
            node = self.nodes[current]
            for edge in node.edges:
                next_node = edge.to_node.node_id
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))
                    
        return []
        
    def query(self, label: str) -> List[Node]:
        return [n for n in self.nodes.values() if n.label == label]


# ============================================================================
# GRAPH DATABASE
# ============================================================================

class GraphDB:
    """Graph database"""
    
    def __init__(self):
        self.graph = KnowledgeGraph()
        
    def create(self, node_id: str, label: str, properties: Dict = None) -> Node:
        node = Node(node_id, label, properties)
        self.graph.add_node(node)
        return node
        
    def connect(self, from_id: str, to_id: str, relationship: str):
        self.graph.add_edge(from_id, to_id, relationship)
        
    def traverse(self, start_id: str, depth: int = 1) -> List[Node]:
        node = self.graph.get_node(start_id)
        if not node:
            return []
            
        results = [node]
        current_level = [node]
        
        for _ in range(depth):
            next_level = []
            for n in current_level:
                for edge in n.edges:
                    next_level.append(edge.to_node)
            results.extend(next_level)
            current_level = next_level
            
        return results


# Global instance
_graph = None

def get_graph() -> GraphDB:
    global _graph
    if _graph is None:
        _graph = GraphDB()
    return _graph


__all__ = ["Node", "Edge", "KnowledgeGraph", "GraphDB", "get_graph"]