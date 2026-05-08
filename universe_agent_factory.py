"""
Universe IDE - AI Agent Factory

Create custom AI agents easily.
"""

import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# AGENT TEMPLATES
# ============================================================================

class AgentTemplates:
    """Pre-built agent templates"""
    
    TEMPLATES = {
        "coder": {
            "role": "Coder",
            "capabilities": ["write_code", "refactor", "debug"],
            "personality": "Precise and methodical",
        },
        "reviewer": {
            "role": "Code Reviewer",
            "capabilities": ["analyze", "review", "suggest"],
            "personality": "Thorough and critical",
        },
        "tester": {
            "role": "Tester",
            "capabilities": ["test", "verify", " validate"],
            "personality": "Detail-oriented",
        },
        "writer": {
            "role": "Technical Writer",
            "capabilities": ["document", "explain", "summarize"],
            "personality": "Clear and concise",
        },
        "debugger": {
            "role": "Debugger",
            "capabilities": ["debug", "fix", "optimize"],
            "personality": "Analytical",
        },
    }
    
    @classmethod
    def get(cls, name: str) -> Optional[Dict]:
        return cls.TEMPLATES.get(name)
    
    @classmethod
    def list_all(cls) -> List[str]:
        return list(cls.TEMPLATES.keys())


# ============================================================================
# AGENT FACTORY
# ============================================================================

@dataclass
class AIAgent:
    """Custom AI agent"""
    id: str
    name: str
    role: str
    capabilities: List[str]
    config: Dict = field(default_factory=dict)


class AgentFactory:
    """Create custom AI agents"""
    
    def __init__(self):
        self.agents = {}
        
    def create(
        self,
        name: str,
        role: str = "General",
        capabilities: List[str] = None,
        template: str = None,
    ) -> str:
        # Use template if provided
        if template and template in AgentTemplates.TEMPLATES:
            tmpl = AgentTemplates.TEMPLATES[template]
            role = tmpl["role"]
            capabilities = tmpl["capabilities"]
            
        # Create agent
        agent_id = str(uuid.uuid4())[:12]
        
        self.agents[agent_id] = AIAgent(
            id=agent_id,
            name=name,
            role=role,
            capabilities=capabilities or [],
        )
        
        return agent_id
    
    def get(self, agent_id: str) -> Optional[AIAgent]:
        return self.agents.get(agent_id)
    
    def list_all(self) -> List[AIAgent]:
        return list(self.agents.values())
    
    def delete(self, agent_id: str) -> bool:
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False


# ============================================================================
# AGENT POOL
# ============================================================================

class AgentPool:
    """Manage multiple agents"""
    
    def __init__(self, size: int = 10):
        self.size = size
        self.factory = AgentFactory()
        self.active = []
        
    def spawn(self, template: str = None) -> str:
        agent_id = self.factory.create(
            name=f"agent-{len(self.active)}",
            template=template,
        )
        self.active.append(agent_id)
        return agent_id
    
    def spawn_team(self, count: int, template: str = None) -> List[str]:
        return [self.spawn(template) for _ in range(count)]
    
    def get_stats(self) -> Dict:
        return {
            "size": self.size,
            "active": len(self.active),
            "available": self.size - len(self.active),
        }


# ============================================================================
# AGENT ORCHESTRATOR
# ============================================================================

class AgentOrchestrator:
    """Coordinate multiple agents"""
    
    def __init__(self):
        self.pool = AgentPool()
        self.tasks = {}
        
    def assign_task(self, agent_id: str, task: Callable) -> str:
        task_id = str(uuid.uuid4())[:8]
        self.tasks[task_id] = {
            "agent_id": agent_id,
            "task": task,
            "status": "assigned",
        }
        return task_id
    
    def execute_task(self, task_id: str) -> Any:
        if task_id in self.tasks:
            task_data = self.tasks[task_id]
            result = task_data["task"]()
            task_data["status"] = "completed"
            return result
        return None
    
    def get_task_status(self, task_id: str) -> str:
        return self.tasks.get(task_id, {}).get("status", "not found")


# Global
_factory = None

def get_factory() -> AgentFactory:
    global _factory
    if _factory is None:
        _factory = AgentFactory()
    return _factory


__all__ = [
    "AgentTemplates",
    "AIAgent",
    "AgentFactory",
    "AgentPool",
    "AgentOrchestrator",
    "get_factory",
]