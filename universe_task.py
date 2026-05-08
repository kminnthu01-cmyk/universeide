"""
Universe IDE - Task Module

Task execution.
"""

from typing import Any, Callable, Dict


# ============================================================================
# TASK
# ============================================================================

class Task:
    """Task"""
    
    def __init__(self, task_id: str, handler: Callable):
        self.task_id = task_id
        self.handler = handler
        self.status = "pending"
        self.result = None
        
    def execute(self, *args, **kwargs):
        self.status = "running"
        self.result = self.handler(*args, **kwargs)
        self.status = "completed"
        return self.result


# ============================================================================
# TASK RUNNER
# ============================================================================

class TaskRunner:
    """Task runner"""
    
    def __init__(self):
        self.tasks = {}
        
    def register(self, task: Task):
        self.tasks[task.task_id] = task
        
    def run(self, task_id: str, *args, **kwargs):
        if task_id in self.tasks:
            return self.tasks[task_id].execute(*args, **kwargs)


__all__ = ["Task", "TaskRunner"]