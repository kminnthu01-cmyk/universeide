"""
Universe IDE - Advanced Agent Orchestration

High-performance parallel agent execution with smart batching.
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# AGENT TYPES
# ============================================================================

class AgentState(Enum):
    """Agent state"""
    IDLE = "idle"
    WORKING = "working"
    COMPLETE = "complete"
    ERROR = "error"


class AgentPriority(Enum):
    """Agent priority"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class AgentTask:
    """Agent task"""
    id: str
    description: str
    priority: AgentPriority = AgentPriority.NORMAL
    timeout: int = 60
    retries: int = 0
    result: Any = None
    error: str = ""
    started_at: datetime = None
    completed_at: datetime = None


@dataclass
class AgentResult:
    """Agent execution result"""
    task_id: str
    success: bool
    result: Any = None
    error: str = ""
    duration_ms: int = 0
    tokens: int = 0


# ============================================================================
# SMART BATCHER
# ============================================================================

class SmartBatcher:
    """Batch similar tasks for efficiency"""
    
    def __init__(self, max_batch_size: int = 10, max_wait_ms: int = 100):
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.pending: List[AgentTask] = []
        self.batch_history: List[dict] = []
        
    async def add_task(self, task: AgentTask):
        """Add task to batch queue"""
        self.pending.append(task)
        
    async def get_batch(self) -> List[AgentTask]:
        """Get optimized batch"""
        # Group by priority
        high_priority = [t for t in self.pending if t.priority == AgentPriority.HIGH]
        normal = [t for t in self.pending if t.priority == AgentPriority.NORMAL]
        
        batch = high_priority[:self.max_batch_size]
        
        remaining = self.max_batch_size - len(batch)
        if remaining > 0:
            batch.extend(normal[:remaining])
            
        return batch[:self.max_batch_size]
        
    def estimate_time(self, tasks: List[AgentTask]) -> int:
        """Estimate batch execution time"""
        # Based on priority and timeout
        total = 0
        for task in tasks:
            if task.priority == AgentPriority.HIGH:
                total += task.timeout // 2
            else:
                total += task.timeout
                
        return total // len(tasks) if tasks else 0


# ============================================================================
# RESULT CACHE
# ============================================================================

class ResultCache:
    """Smart cache for agent results"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.cache: Dict[str, dict] = {}
        self.hits = 0
        self.misses = 0
        
    def _hash(self, key: str) -> str:
        """Create cache key hash"""
        import hashlib
        return hashlib.md5(key.encode()).hexdigest()[:16]
        
    def get(self, key: str) -> Optional[Any]:
        """Get cached result"""
        hash_key = self._hash(key)
        
        if hash_key in self.cache:
            entry = self.cache[hash_key]
            
            # Check TTL
            age = (datetime.now() - entry["created_at"]).total_seconds()
            
            if age < self.ttl:
                self.hits += 1
                return entry["result"]
            else:
                # Expired
                del self.cache[hash_key]
                
        self.misses += 1
        return None
        
    def set(self, key: str, value: Any):
        """Cache result"""
        hash_key = self._hash(key)
        
        # Evict oldest if full
        if len(self.cache) >= self.max_size:
            oldest = min(self.cache.items(), key=lambda x: x[1]["created_at"])
            del self.cache[oldest[0]]
            
        self.cache[hash_key] = {
            "key": key,
            "result": value,
            "created_at": datetime.now(),
        }
        
    def invalidate(self, key: str = None):
        """Invalidate cache"""
        if key:
            hash_key = self._hash(key)
            if hash_key in self.cache:
                del self.cache[hash_key]
        else:
            self.cache.clear()
            
    def stats(self) -> dict:
        """Cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
        }


# ============================================================================
# ADAPTIVE ORCHESTRATOR
# ============================================================================

class AdaptiveOrchestrator:
    """Adaptive agent orchestration with learning"""
    
    def __init__(self, max_agents: int = 100):
        self.max_agents = max_agents
        self.active_agents: Dict[str, AgentState] = {}
        self.metrics: Dict[str, list] = {}
        self.batcher = SmartBatcher()
        self.cache = ResultCache()
        
    def get_optimal_count(self, task_complexity: float) -> int:
        """Dynamically determine optimal agent count"""
        # Adjust based on complexity and available resources
        base = min(self.max_agents, 10)
        
        if task_complexity > 0.8:
            return base * 2  # More agents for complex tasks
        elif task_complexity < 0.3:
            return max(1, base // 4)  # Fewer for simple
        else:
            return base
            
    def estimate_complexity(self, task: AgentTask) -> float:
        """Estimate task complexity (0-1)"""
        # Based on description length and keywords
        complexity = 0.3
        
        # Length factor
        if len(task.description) > 500:
            complexity += 0.3
            
        # Keywords indicating complexity
        complex_keywords = ["analyze", "process", "generate", "multi"]
        simple_keywords = ["get", "list", "check", "find"]
        
        for kw in complex_keywords:
            if kw in task.description.lower():
                complexity += 0.1
                
        for kw in simple_keywords:
            if kw in task.description.lower():
                complexity -= 0.1
                
        return max(0.1, min(1.0, complexity))
        
    def rank_tasks(self, tasks: List[AgentTask]) -> List[AgentTask]:
        """Rank tasks by priority and efficiency"""
        ranked = []
        
        for task in tasks:
            # Calculate priority score
            score = task.priority.value
            
            # Boost by cache potential
            if not self.cache.get(task.description):
                score += 1  # Boost uncached tasks
                
            # Adjust by complexity (simpler = higher priority for throughput)
            complexity = self.estimate_complexity(task)
            score += (1 - complexity)
            
            ranked.append((score, task))
            
        # Sort by score descending
        ranked.sort(key=lambda x: x[0], reverse=True)
        
        return [t for _, t in ranked]
        
    def get_metrics(self) -> dict:
        """Get orchestrator metrics"""
        return {
            "active_agents": len(self.active_agents),
            "max_agents": self.max_agents,
            "batched": len(self.batcher.pending),
            "cache": self.cache.stats(),
        }


# ============================================================================
# PARALLEL EXECUTOR
# ============================================================================

class ParallelExecutor:
    """High-performance parallel task execution"""
    
    def __init__(self, max_concurrent: int = 50):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.running = 0
        self.completed = 0
        self.errors = 0
        
    async def execute(
        self, 
        func: Callable, 
        args: tuple = None,
        kwargs: dict = None
    ) -> Any:
        """Execute with concurrency limit"""
        args = args or ()
        kwargs = kwargs or {}
        
        async with self.semaphore:
            self.running += 1
            try:
                result = await func(*args, **kwargs)
                self.completed += 1
                return result
            except Exception as e:
                self.errors += 1
                raise
            finally:
                self.running -= 1
                
    async def execute_batch(
        self, 
        tasks: List[tuple]
    ) -> List[Any]:
        """Execute batch of tasks"""
        results = await asyncio.gather(
            *[self.execute(f, args, kwargs) for f, args, kwargs in tasks],
            return_exceptions=True
        )
        
        return results
        
    def get_stats(self) -> dict:
        """Get execution statistics"""
        return {
            "running": self.running,
            "completed": self.completed,
            "errors": self.errors,
            "max_concurrent": self.max_concurrent,
        }


# ============================================================================
# ERROR RECOVERY
# ============================================================================

class ErrorRecovery:
    """Intelligent error handling and retry"""
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.error_counts: Dict[str, int] = {}
        
    def should_retry(self, error: Exception, context: str) -> bool:
        """Decide if should retry"""
        error_type = type(error).__name__
        
        # Don't retry these
        no_retry = ["KeyboardInterrupt", "SystemExit"]
        if error_type in no_retry:
            return False
            
        # Check count
        count = self.error_counts.get(context, 0)
        return count < self.max_retries
        
    def record_error(self, error: Exception, context: str):
        """Record error for analysis"""
        error_type = type(error).__name__
        key = f"{context}:{error_type}"
        
        self.error_counts[key] = self.error_counts.get(key, 0) + 1
        
    def get_retry_delay(self, attempt: int) -> float:
        """Exponential backoff"""
        # 1s, 2s, 4s, 8s...
        return min(2 ** attempt, 30)


# ============================================================================
# PERFORMANCE MONITOR
# ============================================================================

class PerformanceMonitor:
    """Monitor agent performance"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.durations: List[float] = []
        self.tokens_used: List[int] = []
        
    def record(self, duration_ms: int, tokens: int = 0):
        """Record execution"""
        self.durations.append(duration_ms)
        self.tokens_used.append(tokens)
        
        # Keep window
        self.durations = self.durations[-self.window_size:]
        self.tokens_used = self.tokens_used[-self.window_size:]
        
    def get_stats(self) -> dict:
        """Get statistics"""
        if not self.durations:
            return {"count": 0}
            
        sorted_durations = sorted(self.durations)
        
        return {
            "count": len(self.durations),
            "avg_ms": sum(self.durations) / len(self.durations),
            "p50_ms": sorted_durations[len(sorted_durations) // 2],
            "p95_ms": sorted_durations[int(len(sorted_durations) * 0.95)],
            "p99_ms": sorted_durations[int(len(sorted_durations) * 0.99)],
            "total_tokens": sum(self.tokens_used),
        }


# Global
_orchestrator = None

def get_orchestrator() -> AdaptiveOrchestrator:
    """Get orchestrator"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AdaptiveOrchestrator()
    return _orchestrator


__all__ = [
    "AgentState",
    "AgentPriority",
    "AgentTask",
    "AgentResult",
    "SmartBatcher",
    "ResultCache",
    "AdaptiveOrchestrator",
    "ParallelExecutor",
    "ErrorRecovery",
    "PerformanceMonitor",
    "get_orchestrator",
]