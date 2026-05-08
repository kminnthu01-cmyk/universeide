"""
Universe IDE - AI Agent Swarm

Advanced swarm intelligence.
"""

import asyncio
import random
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# AGENT
# ============================================================================

@dataclass
class Agent:
    """Swarm agent"""
    id: str
    role: str
    capabilities: List[str] = field(default_factory=list)
    state: Dict = field(default_factory=dict)


# ============================================================================
# SWARM
# ============================================================================

class SwarmIntelligence:
    """Swarm AI"""
    
    def __init__(self, size: int = 100):
        self.size = size
        self.agents = []
        self.tasks = deque(maxlen=1000)
        self.results = {}
        
        # Create agents
        roles = ["analyzer", "builder", "tester", "reviewer", "optimizer"]
        for i in range(size):
            agent = Agent(
                id=f"agent-{i:04d}",
                role=random.choice(roles),
                capabilities=self._generate_capabilities(),
            )
            self.agents.append(agent)
            
    def _generate_capabilities(self) -> List[str]:
        caps = ["code", "analyze", "test", "debug", "optimize", "document"]
        return random.sample(caps, random.randint(2, 4))
        
    def assign_task(self, task: str, handler: Callable) -> str:
        task_id = str(uuid.uuid4())[:8]
        
        # Find best agent
        best = self._find_best_agent(task)
        
        self.tasks.append({
            "id": task_id,
            "task": task,
            "agent": best.id,
            "handler": handler,
            "status": "assigned",
            "created": datetime.now(),
        })
        
        return task_id
        
    def _find_best_agent(self, task: str) -> Agent:
        # Simple matching
        task_keywords = task.lower().split()
        
        best_agent = None
        best_score = 0
        
        for agent in self.agents:
            score = sum(1 for kw in task_keywords if kw in agent.capabilities)
            if score > best_score:
                best_score = score
                best_agent = agent
                
        return best_agent or self.agents[0]
        
    def execute_task(self, task_id: str) -> Any:
        for task in self.tasks:
            if task["id"] == task_id:
                handler = task["handler"]
                result = handler()
                self.results[task_id] = result
                task["status"] = "completed"
                return result
        return None
        
    def get_status(self) -> Dict:
        completed = sum(1 for t in self.tasks if t["status"] == "completed")
        pending = sum(1 for t in self.tasks if t["status"] == "pending")
        
        return {
            "agents": len(self.agents),
            "tasks_completed": completed,
            "tasks_pending": pending,
            "roles": self._count_roles(),
        }
        
    def _count_roles(self) -> Dict[str, int]:
        roles = {}
        for agent in self.agents:
            roles[agent.role] = roles.get(agent.role, 0) + 1
        return roles


# ============================================================================
# HIVE MIND
# ============================================================================

class HiveMind:
    """Distributed consciousness"""
    
    def __init__(self):
        self.swarm = SwarmIntelligence(100)
        self.memory = deque(maxlen=100)
        
    def think(self, problem: str) -> str:
        # Consensus thinking
        task_id = self.swarm.assign_task(problem, lambda: f"solved: {problem}")
        result = self.swarm.execute_task(task_id)
        
        # Store in collective memory
        self.memory.append({
            "problem": problem,
            "solution": result,
            "timestamp": datetime.now(),
        })
        
        return result
        
    def recall(self, problem: str) -> Optional[str]:
        for mem in reversed(self.memory):
            if problem.lower() in mem["problem"].lower():
                return mem["solution"]
        return None


# ============================================================================
# SWARM ORCHESTRATOR
# ============================================================================

class SwarmOrchestrator:
    """Coordinate multiple swarms"""
    
    def __init__(self):
        self.swarms = {}
        
    def create_swarm(self, name: str, size: int) -> str:
        swarm = SwarmIntelligence(size)
        self.swarms[name] = swarm
        return name
        
    def execute(self, swarm_name: str, task: str) -> Any:
        if swarm_name not in self.swarms:
            return None
            
        swarm = self.swarms[swarm_name]
        task_id = swarm.assign_task(task, lambda: task)
        
        return swarm.execute_task(task_id)
        
    def get_swarm_status(self, name: str) -> Dict:
        if name in self.swarms:
            return self.swarms[name].get_status()
        return {}


# Global
_swarm = None

def get_swarm() -> SwarmIntelligence:
    global _swarm
    if _swarm is None:
        _swarm = SwarmIntelligence(100)
    return _swarm


__all__ = [
    "Agent",
    "SwarmIntelligence",
    "HiveMind",
    "SwarmOrchestrator",
    "get_swarm",
]