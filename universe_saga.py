"""
Universe IDE - Saga Orchestration Module

Distributed transaction management.
"""

from typing import Any, Callable, Dict, List
import time


# ============================================================================
# SAGA STEP
# ============================================================================

class SagaStep:
    """Saga step"""
    
    def __init__(step_id: str, action: Callable, compensation: Callable):
        self.step_id = step_id
        self.action = action
        self.compensation = compensation
        self.executed = False
        self.compensated = False
        
    def execute(self) -> Any:
        self.executed = True
        return self.action()
        
    def compensate(self) -> Any:
        if self.executed and not self.compensated:
            self.compensated = True
            return self.compensation()


# ============================================================================
# SAGA ORCHESTRATOR
# ============================================================================

class SagaOrchestrator:
    """Saga orchestrator"""
    
    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps = []
        self.current_step = 0
        
    def add_step(self, step: SagaStep):
        self.steps.append(step)
        
    def execute(self) -> Dict:
        results = []
        for step in self.steps:
            try:
                result = step.execute()
                results.append({"step": step.step_id, "result": result})
            except Exception as e:
                # Compensate
                for s in reversed(self.steps[:self.current_step]):
                    s.compensate()
                return {"error": str(e)}
            self.current_step += 1
        return {"completed": True}


__all__ = ["SagaStep", "SagaOrchestrator"]