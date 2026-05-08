"""
Universe IDE - Workflow Automation

Workflow engine for task automation.
"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# WORKFLOW STATES
# ============================================================================

class WorkflowState(Enum):
    """Workflow states"""
    PENDING = "pending"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ============================================================================
# STEP TYPES
# ============================================================================

class StepType(Enum):
    """Step types"""
    TASK = "task"
    CONDITION = "condition"
    PARALLEL = "parallel"
    LOOP = "loop"
    APPROVAL = "approval"
    DELAY = "delay"


# ============================================================================
# WORKFLOW STEP
# ============================================================================

@dataclass
class WorkflowStep:
    """A workflow step"""
    step_id: str
    name: str
    type: StepType
    config: dict = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    retries: int = 0
    
    def execute(self, context: dict) -> dict:
        """Execute step"""
        # Base implementation
        return {"status": "done", "output": {}}


# ============================================================================
# WORKFLOW
# ============================================================================

@dataclass
class Workflow:
    """A workflow"""
    workflow_id: str
    name: str
    steps: list[WorkflowStep] = field(default_factory=list)
    state: WorkflowState = WorkflowState.PENDING
    context: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def add_step(self, step: WorkflowStep):
        """Add step"""
        self.steps.append(step)
        
    def get_ready_steps(self) -> list[WorkflowStep]:
        """Get steps ready to run"""
        ready = []
        for step in self.steps:
            if step.depends_on:
                # Check dependencies
                deps_met = True
                for s in self.steps:
                    for dep in step.depends_on:
                        if s.step_id == dep and s.state != WorkflowState.COMPLETED:
                            deps_met = False
                            break
                if deps_met:
                    ready.append(step)
            else:
                # No dependencies
                ready.append(step)
        return ready


# ============================================================================
# SCHEDULE
# ============================================================================

@dataclass  
class Schedule:
    """Workflow schedule"""
    schedule_id: str
    workflow_id: str
    cron: str = ""
    interval_seconds: int = 0
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None


# ============================================================================
# WORKFLOW ENGINE
# ============================================================================

class WorkflowEngine:
    """
    Workflow execution engine.
    """
    
    def __init__(self):
        self.workflows: dict[str, Workflow] = {}
        self.schedules: dict[str, Schedule] = {}
        self.running: set[str] = set()
        
    def create_workflow(self, name: str, steps: list[dict]) -> str:
        """Create workflow"""
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        workflow = Workflow(workflow_id=workflow_id, name=name)
        
        for step_config in steps:
            step = WorkflowStep(
                step_id=f"step_{uuid.uuid4().hex[:8]}",
                name=step_config.get("name", "step"),
                type=StepType(step_config.get("type", "task")),
                config=step_config.get("config", {}),
                depends_on=step_config.get("depends_on", []),
            )
            workflow.add_step(step)
            
        self.workflows[workflow_id] = workflow
        return workflow_id
        
    def run_workflow(self, workflow_id: str) -> dict:
        """Run workflow"""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
            
        workflow = self.workflows[workflow_id]
        workflow.state = WorkflowState.RUNNING
        workflow.started_at = datetime.now()
        self.running.add(workflow_id)
        
        # Execute steps
        ready = workflow.get_ready_steps()
        for step in ready:
            try:
                result = step.execute(workflow.context)
                workflow.context[step.step_id] = result
            except Exception as e:
                workflow.state = WorkflowState.FAILED
                return {"error": str(e)}
            
        workflow.state = WorkflowState.COMPLETED
        workflow.completed_at = datetime.now()
        self.running.discard(workflow_id)
        
        return {"workflow_id": workflow_id, "status": workflow.state.value}
        
    def schedule_workflow(self, workflow_id: str, interval_seconds: int) -> str:
        """Schedule workflow"""
        schedule_id = f"sched_{uuid.uuid4().hex[:8]}"
        schedule = Schedule(
            schedule_id=schedule_id,
            workflow_id=workflow_id,
            interval_seconds=interval_seconds,
        )
        self.schedules[schedule_id] = schedule
        return schedule_id
        
    def get_status(self) -> dict:
        """Get engine status"""
        return {
            "workflows": len(self.workflows),
            "running": len(self.running),
            "schedules": len(self.schedules),
        }


# ============================================================================
# TEMPLATES
# ============================================================================

class WorkflowTemplates:
    """Built-in workflow templates"""
    
    @staticmethod
    def ci_cd() -> list[dict]:
        """CI/CD workflow"""
        return [
            {"name": "checkout", "type": "task", "config": {"action": "checkout"}},
            {"name": "test", "type": "task", "config": {"action": "test"}, "depends_on": ["checkout"]},
            {"name": "build", "type": "task", "config": {"action": "build"}, "depends_on": ["test"]},
            {"name": "deploy", "type": "task", "config": {"action": "deploy"}, "depends_on": ["build"]},
        ]
        
    @staticmethod
    def code_review() -> list[dict]:
        """Code review workflow"""
        return [
            {"name": "lint", "type": "task"},
            {"name": "test", "type": "task"},
            {"name": "security", "type": "task"},
            {"name": "approve", "type": "approval"},
        ]
        
    @staticmethod
    def data_pipeline() -> list[dict]:
        """Data pipeline workflow"""
        return [
            {"name": "extract", "type": "task"},
            {"name": "transform", "type": "task", "depends_on": ["extract"]},
            {"name": "load", "type": "task", "depends_on": ["transform"]},
            {"name": "validate", "type": "task", "depends_on": ["load"]},
        ]


# Global instance
_engine = None

def get_workflow_engine() -> WorkflowEngine:
    """Get workflow engine"""
    global _engine
    if _engine is None:
        _engine = WorkflowEngine()
    return _engine


__all__ = [
    "WorkflowState",
    "StepType",
    "WorkflowStep",
    "Workflow", 
    "Schedule",
    "WorkflowEngine",
    "WorkflowTemplates",
    "get_workflow_engine",
]