"""
Universe IDE - Multi-Agent Module

Multi-agent coordination.
"""

from typing import Any, Dict, List
import random


# ============================================================================
# AGENT TEAM
# ============================================================================

class AgentTeam:
    """Team of agents"""
    
    def __init__(self, team_id: str):
        self.team_id = team_id
        self.agents = []
        
    def add(self, agent_id: str, role: str):
        self.agents.append({"id": agent_id, "role": role})
        
    def assign_task(self, task: str) -> Dict:
        # Assign to random agent
        agent = random.choice(self.agents) if self.agents else None
        return {
            "task": task,
            "assigned_to": agent["id"] if agent else None,
            "status": "assigned",
        }
        
    def get_status(self) -> Dict:
        return {
            "team_id": self.team_id,
            "agents": len(self.agents),
            "roles": {a["role"]: a["id"] for a in self.agents},
        }


# ============================================================================
# TEAM LEADER
# ============================================================================

class TeamLeader:
    """Lead agent teams"""
    
    def __init__(self):
        self.teams = {}
        
    def create_team(self, team_id: str) -> AgentTeam:
        team = AgentTeam(team_id)
        self.teams[team_id] = team
        return team
        
    def get_team(self, team_id: str) -> AgentTeam:
        return self.teams.get(team_id)


# Global
_leader = None

def get_team_leader() -> TeamLeader:
    global _leader
    if _leader is None:
        _leader = TeamLeader()
    return _leader


__all__ = ["AgentTeam", "TeamLeader", "get_team_leader"]