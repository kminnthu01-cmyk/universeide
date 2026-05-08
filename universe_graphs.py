"""
Universe IDE - Graph Algorithms
"""

from collections import deque


# ============================================================================
# GRAPH
# ============================================================================

class Graph:
    def __init__(self):
        self.adjacency = {}
        
    def add_edge(self, u, v):
        if u not in self.adjacency:
            self.adjacency[u] = []
        self.adjacency[u].append(v)
        
    def bfs(self, start):
        visited = {start}
        queue = deque([start])
        order = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            
            for neighbor in self.adjacency.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        return order
        
    def dfs(self, start):
        visited = set()
        order = []
        
        def dfs_util(node):
            visited.add(node)
            order.append(node)
            for neighbor in self.adjacency.get(node, []):
                if neighbor not in visited:
                    dfs_util(neighbor)
                    
        dfs_util(start)
        return order


# ============================================================================
# TREE
# ============================================================================

class Tree:
    def __init__(self, value=None):
        self.value = value
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def traverse(self):
        result = [self.value]
        for child in self.children:
            result.extend(child.traverse())
        return result


__all__ = ["Graph", "Tree"]
