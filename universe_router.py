"""
Universe IDE - Intelligent Task Router

AI-powered routing for optimal agent assignment.
"""

import asyncio
import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# ROUTING TYPES
# ============================================================================

class TaskType(Enum):
    """Task type classification"""
    QUERY = "query"
    GENERATE = "generate"
    ANALYZE = "analyze"
    EXECUTE = "execute"
    SEARCH = "search"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


@dataclass
class Task:
    """Routable task"""
    id: str
    description: str
    task_type: TaskType = TaskType.QUERY
    complexity: float = 0.5
    data: Any = None


@dataclass
class AgentProfile:
    """Agent capability profile"""
    id: str
    name: str
    capabilities: List[str] = field(default_factory=list)
    speed: float = 1.0  # relative speed
    accuracy: float = 0.9  # 0-1
    cost: float = 1.0  # relative cost
    current_load: float = 0.0  # 0-1


# ============================================================================
# TASK CLASSIFIER
# ============================================================================

class TaskClassifier:
    """Classify tasks by type and complexity"""
    
    # Keywords for classification
    TASK_KEYWORDS = {
        TaskType.QUERY: ["get", "list", "find", "check", "what", "show"],
        TaskType.GENERATE: ["create", "make", "generate", "write", "build", "new"],
        TaskType.ANALYZE: ["analyze", "review", "check", "optimize", "improve", "debug"],
        TaskType.EXECUTE: ["run", "execute", "do", "perform", "start"],
        TaskType.SEARCH: ["search", "find", "lookup", "query"],
        TaskType.CREATE: ["create", "new", "add"],
        TaskType.UPDATE: ["update", "edit", "change", "modify"],
        TaskType.DELETE: ["remove", "delete", "clear"],
    }
    
    def classify(self, description: str) -> TaskType:
        """Classify task type"""
        desc_lower = description.lower()
        
        for task_type, keywords in self.TASK_KEYWORDS.items():
            for kw in keywords:
                if kw in desc_lower:
                    return task_type
                    
        return TaskType.QUERY  # default
        
    def estimate_complexity(self, description: str) -> float:
        """Estimate complexity (0-1)"""
        complexity = 0.5
        
        # Length
        if len(description) > 200:
            complexity += 0.2
            
        # Keywords indicating complexity
        complex_markers = [
            "analyze", "compare", "multiple", "complex",
            "optimize", "refactor", "review", "generate full"
        ]
        simple_markers = ["get", "list", "show", "print"]
        
        for marker in complex_markers:
            if marker in description.lower():
                complexity += 0.1
                
        for marker in simple_markers:
            if marker in description.lower():
                complexity -= 0.1
                
        return max(0.1, min(1.0, complexity))


# ============================================================================
# AGENT MATCHER
# ============================================================================

class AgentMatcher:
    """Match tasks to optimal agents"""
    
    def __init__(self):
        self.classifier = TaskClassifier()
        self.agents: Dict[str, AgentProfile] = {}
        
    def register_agent(self, agent: AgentProfile):
        """Register agent"""
        self.agents[agent.id] = agent
        
    def match(self, task: Task) -> Optional[AgentProfile]:
        """Find best agent for task"""
        candidates = []
        
        for agent in self.agents.values():
            # Skip overloaded agents
            if agent.current_load > 0.8:
                continue
                
            # Score agent
            score = 0.0
            
            # Capability match
            task_keywords = self.classifier.TASK_KEYWORDS.get(task.task_type, [])
            capability_match = any(
                kw in agent.capabilities 
                for kw in task_keywords
            )
            if capability_match:
                score += 0.4
                
            # Speed match based on complexity
            if task.complexity > 0.7 and agent.speed < 1.0:
                score -= 0.2  # Slow agent for complex task
            elif task.complexity < 0.3 and agent.speed > 1.0:
                score += 0.1  # Fast agent bonus for simple
                
            # Accuracy match
            if task.complexity > 0.8:
                score += agent.accuracy * 0.3  # Need high accuracy
                
            # Cost efficiency
            score -= (agent.cost - 1.0) * 0.1
            
            # Current load (prefer idle)
            score += (1.0 - agent.current_load) * 0.2
            
            candidates.append((score, agent))
            
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]
            
        return None
        
    def get_agent_loads(self) -> Dict[str, float]:
        """Get all agent loads"""
        return {a.id: a.current_load for a in self.agents.values()}


# ============================================================================
# LOAD BALANCER
# ============================================================================

class LoadBalancer:
    """Distribute load across agents"""
    
    STRATEGY_ROUND_ROBIN = "round_robin"
    STRATEGY_LEAST_LOADED = "least_loaded"
    STRATEGY_WEIGHTED = "weighted"
    STRATEGY_ADAPTIVE = "adaptive"
    
    def __init__(self, strategy: str = STRATEGY_ADAPTIVE):
        self.strategy = strategy
        self.agent_list: List[str] = []
        self.current_index = 0
        self.agent_loads: Dict[str, float] = {}
        
    def add_agent(self, agent_id: str, weight: float = 1.0):
        """Add agent with weight"""
        self.agent_list.append(agent_id)
        
    def get_next(self) -> str:
        """Get next agent based on strategy"""
        if not self.agent_list:
            raise ValueError("No agents available")
            
        if self.strategy == self.STRATEGY_ROUND_ROBIN:
            agent = self.agent_list[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.agent_list)
            return agent
            
        elif self.strategy == self.STRATEGY_LEAST_LOADED:
            if not self.agent_loads:
                return self.agent_list[0]
                
            min_load = min(self.agent_loads.values())
            for agent_id in self.agent_list:
                if self.agent_loads.get(agent_id, 0) == min_load:
                    return agent_id
            return self.agent_list[0]
            
        else:  # adaptive
            # Pick least loaded most of the time
            return self.get_next()
            
    def set_load(self, agent_id: str, load: float):
        """Update agent load"""
        self.agent_loads[agent_id] = load


# ============================================================================
# TASK QUEUE
# ============================================================================

class PriorityTaskQueue:
    """Priority-based task queue"""
    
    def __init__(self):
        self.high_PRIORITY_queue: List[Task] = []
        self.normal_queue: List[Task] = []
        self.low_PRIORITY_queue: List[Task] = []
        
    def enqueue(self, task: Task, priority: int = 2):
        """Add task to queue"""
        if priority >= 3:
            self.high_PRIORITY_queue.append(task)
        elif priority >= 2:
            self.normal_queue.append(task)
        else:
            self.low_PRIORITY_queue.append(task)
            
    def dequeue(self) -> Optional[Task]:
        """Get next task"""
        # High priority first
        if self.high_PRIORITY_queue:
            return self.high_PRIORITY_queue.pop(0)
        if self.normal_queue:
            return self.normal_queue.pop(0)
        if self.low_PRIORITY_queue:
            return self.low_PRIORITY_queue.pop(0)
        return None
        
    def size(self) -> dict:
        """Get queue sizes"""
        return {
            "high": len(self.high_PRIORITY_queue),
            "normal": len(self.normal_queue),
            "low": len(self.low_PRIORITY_queue),
            "total": len(self.high_PRIORITY_queue) + len(self.normal_queue) + len(self.low_PRIORITY_queue),
        }


# ============================================================================
# ROUTER
# ============================================================================

class TaskRouter:
    """Main task router"""
    
    def __init__(self):
        self.classifier = TaskClassifier()
        self.matcher = AgentMatcher()
        self.balancer = LoadBalancer()
        self.queue = PriorityTaskQueue()
        
    def route(self, description: str) -> tuple:
        """Route task to optimal agent"""
        # Classify
        task_type = self.classifier.classify(description)
        complexity = self.classifier.estimate_complexity(description)
        
        # Create task
        task = Task(
            id=hashlib.md5(description.encode()).hexdigest()[:8],
            description=description,
            task_type=task_type,
            complexity=complexity,
        )
        
        # Match
        agent = self.matcher.match(task)
        
        if agent is None:
            # Fall back to load balancer
            agent_id = self.balancer.get_next()
            return task, agent_id, task_type
            
        return task, agent.id, task_type
        
    async def route_batch(self, descriptions: List[str]) -> List[tuple]:
        """Route batch of tasks"""
        results = []
        
        for desc in descriptions:
            result = self.route(desc)
            results.append(result)
            
        return results


# Global
_router = None

def get_router() -> TaskRouter:
    """Get router"""
    global _router
    if _router is None:
        _router = TaskRouter()
    return _router


__all__ = [
    "TaskType",
    "Task",
    "AgentProfile",
    "TaskClassifier",
    "AgentMatcher",
    "LoadBalancer",
    "PriorityTaskQueue",
    "TaskRouter",
    "get_router",
]