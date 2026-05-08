"""
Universe IDE - Task Queue System

Distributed async task queue.
"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# TASK PRIORITY
# ============================================================================

class TaskPriority(Enum):
    """Task priorities"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


# ============================================================================
# TASK STATUS
# ============================================================================

class TaskStatus(Enum):
    """Task status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ============================================================================
# TASK
# ============================================================================

@dataclass
class Task:
    """Async task"""
    task_id: str
    func_name: str
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


# ============================================================================
# TASK QUEUE
# ============================================================================

class TaskQueue:
    """
    Distributed task queue.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.queue: list[Task] = []
        self.running: dict[str, Task] = {}
        self.completed: dict[str, Task] = {}
        self.functions: dict[str, Callable] = {}
        self._running = False
        
    def register(self, name: str, func: Callable):
        """Register function"""
        self.functions[name] = func
        
    def enqueue(
        self, 
        func_name: str, 
        *args, 
        priority: TaskPriority = TaskPriority.NORMAL,
        **kwargs
    ) -> str:
        """Add task to queue"""
        task = Task(
            task_id=f"task_{uuid.uuid4().hex[:8]}",
            func_name=func_name,
            args=args,
            kwargs=kwargs,
            priority=priority,
        )
        
        # Insert by priority
        inserted = False
        for i, t in enumerate(self.queue):
            if priority.value > t.priority.value:
                self.queue.insert(i, task)
                inserted = True
                break
                
        if not inserted:
            self.queue.append(task)
            
        return task.task_id
        
    async def execute(self, task: Task) -> Any:
        """Execute single task"""
        if task.func_name not in self.functions:
            task.status = TaskStatus.FAILED
            task.error = f"Function {task.func_name} not found"
            return None
            
        func = self.functions[task.func_name]
        
        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            
            if asyncio.iscoroutinefunction(func):
                task.result = await func(*task.args, **task.kwargs)
            else:
                task.result = func(*task.args, **task.kwargs)
                
            task.status = TaskStatus.COMPLETED
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            
        task.completed_at = datetime.now()
        
        return task.result
        
    async def worker(self, worker_id: str):
        """Worker coroutine"""
        while self._running:
            # Get task from queue
            if not self.queue:
                await asyncio.sleep(0.1)
                continue
                
            task = self.queue.pop(0)
            self.running[task.task_id] = task
            
            # Execute
            await self.execute(task)
            
            # Move to completed
            self.completed[task.task_id] = task
            if task.task_id in self.running:
                del self.running[task.task_id]
                
    async def run(self):
        """Run task queue"""
        self._running = True
        
        # Start workers
        workers = [
            asyncio.create_task(self.worker(f"worker_{i}"))
            for i in range(self.max_workers)
        ]
        
        # Wait for all work done and queue empty
        while self.queue or self.running:
            await asyncio.sleep(0.1)
            
        # Cancel workers
        self._running = False
        for w in workers:
            w.cancel()
            
    def cancel(self, task_id: str):
        """Cancel task"""
        for task in self.queue:
            if task.task_id == task_id:
                task.status = TaskStatus.CANCELLED
                return True
                
        if task_id in self.running:
            self.running[task_id].status = TaskStatus.CANCELLED
            return True
            
        return False
        
    def get_status(self) -> dict:
        """Get queue status"""
        return {
            "pending": len(self.queue),
            "running": len(self.running),
            "completed": len(self.completed),
            "workers": self.max_workers,
        }


# ============================================================================
# TASK SCHEDULER
# ============================================================================

class TaskScheduler:
    """Schedule recurring tasks"""
    
    def __init__(self):
        self.tasks: dict[str, dict] = {}
        self._running = False
        
    def schedule_interval(
        self, 
        name: str, 
        func: Callable, 
        interval_seconds: int
    ):
        """Schedule recurring task"""
        self.tasks[name] = {
            "func": func,
            "interval": interval_seconds,
            "last_run": None,
        }
        
    async def run(self):
        """Run scheduler"""
        self._running = True
        last_runs: dict[str, float] = {}
        
        while self._running:
            now = datetime.now().timestamp()
            
            for name, task in self.tasks.items():
                last = last_runs.get(name, 0)
                interval = task["interval"]
                
                if now - last >= interval:
                    try:
                        if asyncio.iscoroutinefunction(task["func"]):
                            await task["func"]()
                        else:
                            task["func"]()
                    except:
                        pass
                        
                    last_runs[name] = now
                    
            await asyncio.sleep(1)
            
    def stop(self):
        """Stop scheduler"""
        self._running = False


# Global
_queue = None

def get_task_queue() -> TaskQueue:
    """Get global task queue"""
    global _queue
    if _queue is None:
        _queue = TaskQueue()
    return _queue


__all__ = [
    "TaskPriority",
    "TaskStatus",
    "Task",
    "TaskQueue",
    "TaskScheduler",
    "get_task_queue",
]