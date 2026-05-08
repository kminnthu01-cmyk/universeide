"""
Universe IDE - Workflow Engine Module

Workflow orchestration.
"""

from typing import Any, Callable, Dict, List, Optional
from collections import deque


# ============================================================================
# TASK
# ============================================================================

class WorkflowTask:
    """Workflow task"""
    
    def __init__(self, task_id: str, name: str, handler: Callable):
        self.task_id = task_id
        self.name = name
        self.handler = handler
        self.status = "pending"
        self.result = None
        
    def execute(self, input_data: Any) -> Any:
        self.status = "running"
        self.result = self.handler(input_data)
        self.status = "completed"
        return self.result


# ============================================================================
# WORKFLOW
# ============================================================================

class Workflow:
    """Workflow definition"""
    
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.tasks = {}
        self.edges = []
        
    def add_task(self, task: WorkflowTask):
        self.tasks[task.task_id] = task
        
    def add_edge(self, from_id: str, to_id: str):
        self.edges.append((from_id, to_id))
        
    def execute(self, input_data: Any) -> Dict:
        results = {}
        # Simple sequential execution
        for task in self.tasks.values():
            input_data = task.execute(input_data)
            results[task.task_id] = task.result
        return results


# ============================================================================
# WORKFLOW ENGINE
# ============================================================================

class WorkflowEngine:
    """Execute workflows"""
    
    def __init__(self):
        self.workflows = {}
        
    def register(self, workflow: Workflow):
        self.workflows[workflow.workflow_id] = workflow
        
    def execute(self, workflow_id: str, input_data: Any) -> Optional[Dict]:
        if workflow_id in self.workflows:
            return self.workflows[workflow_id].execute(input_data)
        return None
        
    def list_workflows(self) -> List[str]:
        return list(self.workflows.keys())


# Global
_engine = None

def get_workflow_engine() -> WorkflowEngine:
    global _engine
    if _engine is None:
        _engine = WorkflowEngine()
    return _engine


__all__ = ["WorkflowTask", "Workflow", "WorkflowEngine", "get_workflow_engine"]