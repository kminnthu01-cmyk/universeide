"""
Universe IDE - A2A Protocol Module

Agent-to-Agent communication.
"""

from typing import Any, Dict, List, Optional
import uuid


# ============================================================================
# A2A AGENT
# ============================================================================

class A2AAgent:
    """A2A capable agent"""
    
    def __init__(self, agent_id: str, capabilities: List[str] = None):
        self.agent_id = agent_id
        self.capabilities = capabilities or []
        self.connected = []
        
    def connect(self, other: "A2AAgent"):
        self.connected.append(other.agent_id)
        
    def send(self, target: str, message: Any) -> Dict:
        return {
            "from": self.agent_id,
            "to": target,
            "message": message,
            "id": str(uuid.uuid4()),
        }
        
    def receive(self, message: Dict) -> Dict:
        return {"status": "received", "by": self.agent_id}


# ============================================================================
# A2A SERVER
# ============================================================================

class A2AServer:
    """A2A server for agent coordination"""
    
    def __init__(self):
        self.agents = {}
        
    def register(self, agent: A2AAgent):
        self.agents[agent.agent_id] = agent
        
    def discover(self, capability: str) -> List[A2AAgent]:
        return [
            a for a in self.agents.values()
            if capability in a.capabilities
        ]
        
    def route(self, message: Dict) -> Dict:
        target_id = message.get("to")
        if target_id in self.agents:
            return self.agents[target_id].receive(message)
        return {"error": "Agent not found"}


# ============================================================================
# A2A PROTOCOL
# ============================================================================

class A2AProtocol:
    """A2A Protocol implementation"""
    
    def __init__(self):
        self.server = A2AServer()
        
    def create_agent(self, agent_id: str, capabilities: List[str]) -> A2AAgent:
        agent = A2AAgent(agent_id, capabilities)
        self.server.register(agent)
        return agent
        
    def send_message(self, from_id: str, to_id: str, message: Any) -> Dict:
        return self.server.route({
            "from": from_id,
            "to": to_id,
            "message": message,
        })


# Global instance
_a2a = None

def get_a2a() -> A2AProtocol:
    global _a2a
    if _a2a is None:
        _a2a = A2AProtocol()
    return _a2a


__all__ = ["A2AAgent", "A2AServer", "A2AProtocol", "get_a2a"]