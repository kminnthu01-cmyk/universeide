"""
Universe IDE - Workflow Engine

Visual workflow automation for AI agents.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# WORKFLOW TYPES
# ============================================================================

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class NodeType(Enum):
    START = "start"
    END = "end"
    TASK = "task"
    CONDITION = "condition"
    BRANCH = "branch"
    WAIT = "wait"
    API = "api"


@dataclass
class WorkflowNode:
    id: str
    type: NodeType
    config: dict = field(default_factory=dict)
    next_nodes: List[str] = field(default_factory=list)


@dataclass
class Workflow:
    id: str
    name: str
    nodes: Dict[str, WorkflowNode] = field(default_factory=dict)
    status: WorkflowStatus = WorkflowStatus.PENDING


# ============================================================================
# WORKFLOW RUNNER
# ============================================================================

class WorkflowRunner:
    """Execute workflows"""
    
    def __init__(self):
        self.running: Dict[str, bool] = {}
        
    async def run(self, workflow: Workflow, context: dict = None) -> dict:
        """Run workflow"""
        self.running[workflow.id] = True
        workflow.status = WorkflowStatus.RUNNING
        context = context or {}
        results = {}
        
        # Start from START node
        start_node = None
        for node in workflow.nodes.values():
            if node.type == NodeType.START:
                start_node = node
                break
                
        if not start_node:
            workflow.status = WorkflowStatus.FAILED
            return {"error": "No start node"}
            
        # Execute nodes
        current = start_node
        while current and self.running.get(workflow.id):
            result = await self._execute_node(current, context)
            results[current.id] = result
            
            # Check if condition failed
            if isinstance(result, dict) and result.get("stop"):
                break
                
            # Move to next
            if current.next_nodes:
                next_id = current.next_nodes[0]
                current = workflow.nodes.get(next_id)
            else:
                break
                
        workflow.status = WorkflowStatus.COMPLETED
        self.running[workflow.id] = False
        
        return results
        
    async def _execute_node(self, node: WorkflowNode, context: dict) -> dict:
        """Execute single node"""
        if node.type == NodeType.TASK:
            # Simulate task execution
            return {"result": "done", "node": node.id}
        elif node.type == NodeType.CONDITION:
            return {"result": True, "node": node.id}
        elif node.type == NodeType.API:
            return {"result": "API called", "node": node.id}
        else:
            return {"result": "ok", "node": node.id}
            
    def stop(self, workflow_id: str):
        """Stop workflow"""
        self.running[workflow_id] = False


# ============================================================================
# WORKFLOW BUILDER
# ============================================================================

class WorkflowBuilder:
    """Build workflows visually"""
    
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        
    def create_workflow(self, name: str) -> Workflow:
        """Create workflow"""
        import uuid
        wf = Workflow(
            id=uuid.uuid4().hex[:16],
            name=name,
        )
        self.workflows[wf.id] = wf
        return wf
        
    def add_node(
        self,
        workflow: Workflow,
        node_type: NodeType,
        config: dict = None
    ) -> WorkflowNode:
        """Add node"""
        import uuid
        node = WorkflowNode(
            id=uuid.uuid4().hex[:8],
            type=node_type,
            config=config or {},
        )
        workflow.nodes[node.id] = node
        return node
        
    def connect(self, workflow: Workflow, from_id: str, to_id: str):
        """Connect nodes"""
        if from_id in workflow.nodes:
            workflow.nodes[from_id].next_nodes.append(to_id)
            
    def build_linear(self, name: str, tasks: List[str]) -> Workflow:
        """Build linear workflow"""
        wf = self.create_workflow(name)
        
        # Add start
        start = self.add_node(wf, NodeType.START)
        
        # Add tasks
        prev = start
        for task in tasks:
            task_node = self.add_node(wf, NodeType.TASK, {"task": task})
            self.connect(wf, prev.id, task_node.id)
            prev = task_node
            
        # Add end
        end = self.add_node(wf, NodeType.END)
        self.connect(wf, prev.id, end.id)
        
        return wf


# ============================================================================
# AUTOMATION
# ============================================================================

class AutomationEngine:
    """Automation engine"""
    
    def __init__(self):
        self.builder = WorkflowBuilder()
        self.runner = WorkflowRunner()
        self.automations: Dict[str, Callable] = {}
        
    def register_automation(
        self,
        name: str,
        trigger: str,
        workflow: Workflow
    ):
        """Register automation"""
        self.automations[name] = {
            "trigger": trigger,
            "workflow": workflow,
        }
        
    async def trigger(self, name: str) -> dict:
        """Trigger automation"""
        if name in self.automations:
            auto = self.automations[name]
            return await self.runner.run(auto["workflow"])
        return {"error": "Not found"}


# Global
_engine = None

def get_automation() -> AutomationEngine:
    global _engine
    if _engine is None:
        _engine = AutomationEngine()
    return _engine


__all__ = [
    "WorkflowStatus",
    "NodeType",
    "WorkflowNode",
    "Workflow",
    "WorkflowRunner",
    "WorkflowBuilder",
    "AutomationEngine",
    "get_automation",
]