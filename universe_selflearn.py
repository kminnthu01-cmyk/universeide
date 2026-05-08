"""
Universe IDE - Self-Learning System

The platform that learns from its own performance and improves over time.

Features:
- Performance tracking
- Success/failure pattern learning
- Model adaptation
- Strategy optimization
- Caching with intelligence
"""

import json
import os
import time
from collections import defaultdict
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Optional
from threading import Lock


# ============================================================================
# PERFORMANCE TRACKING
# ============================================================================

@dataclass
class PerformanceRecord:
    """Record of a single execution"""
    task_id: str
    timestamp: datetime
    duration_ms: int
    success: bool
    model: str
    strategy: str
    tokens_used: int = 0
    error: Optional[str] = None


@dataclass
class ModelPerformance:
    """Performance metrics for a model"""
    model: str
    total_tasks: int = 0
    successful_tasks: int = 0
    total_duration_ms: int = 0
    total_tokens: int = 0
    
    @property
    def success_rate(self) -> float:
        return self.successful_tasks / max(1, self.total_tasks)
    
    @property
    def avg_duration(self) -> int:
        return self.total_duration_ms // max(1, self.total_tasks)


class PerformanceTracker:
    """
    Track performance and learn from success/failure patterns.
    
    This is the foundation of self-improvement.
    """
    
    def __init__(self, max_records: int = 10000):
        self.max_records = max_records
        self.records: list[PerformanceRecord] = []
        self.model_performance: dict[str, ModelPerformance] = {}
        self.strategy_performance: dict[str, dict] = defaultdict(lambda: {
            "success": 0, "fail": 0, "total_duration": 0
        })
        self.lock = Lock()
        
        # Load from disk if available
        self._load()
        
    def record(
        self, 
        task_id: str,
        duration_ms: int,
        success: bool,
        model: str,
        strategy: str,
        tokens_used: int = 0,
        error: Optional[str] = None
    ):
        """Record a performance observation"""
        with self.lock:
            record = PerformanceRecord(
                task_id=task_id,
                timestamp=datetime.now(),
                duration_ms=duration_ms,
                success=success,
                model=model,
                strategy=strategy,
                tokens_used=tokens_used,
                error=error,
            )
            
            self.records.append(record)
            
            # Update model performance
            if model not in self.model_performance:
                self.model_performance[model] = ModelPerformance(model)
                
            mp = self.model_performance[model]
            mp.total_tasks += 1
            if success:
                mp.successful_tasks += 1
            mp.total_duration_ms += duration_ms
            mp.total_tokens += tokens_used
            
            # Update strategy performance
            sp = self.strategy_performance[strategy]
            if success:
                sp["success"] += 1
            else:
                sp["fail"] += 1
            sp["total_duration"] += duration_ms
            
            # Trim old records
            if len(self.records) > self.max_records:
                self.records = self.records[-self.max_records:]
                
        # Save periodically
        if len(self.records) % 100 == 0:
            self._save()
            
    def get_best_model(self, task_type: str = "default") -> str:
        """Get the best model for a task type"""
        # For now, return best by success rate
        best = None
        best_rate = 0
        
        for model, perf in self.model_performance.items():
            if perf.total_tasks >= 5:  # Minimum sample size
                if perf.success_rate > best_rate:
                    best_rate = perf.success_rate
                    best = model
                    
        return best or "claude-sonnet-4-20250505"  # Default
        
    def get_best_strategy(self) -> str:
        """Get the best performing strategy"""
        best = None
        best_rate = 0
        
        for strategy, perf in self.strategy_performance.items():
            total = perf["success"] + perf["fail"]
            if total >= 5:
                rate = perf["success"] / total
                if rate > best_rate:
                    best_rate = rate
                    best = strategy
                    
        return best or "parallel"
        
    def get_stats(self) -> dict:
        """Get overall statistics"""
        return {
            "total_records": len(self.records),
            "models": {
                m: {
                    "success_rate": p.success_rate,
                    "avg_duration": p.avg_duration,
                    "total_tasks": p.total_tasks,
                }
                for m, p in self.model_performance.items()
            },
            "strategies": dict(self.strategy_performance),
        }
        
    def _save(self):
        """Persist to disk"""
        try:
            data = {
                "model_performance": [
                    {
                        "model": m,
                        "total_tasks": p.total_tasks,
                        "successful_tasks": p.successful_tasks,
                        "total_duration_ms": p.total_duration_ms,
                        "total_tokens": p.total_tokens,
                    }
                    for m, p in self.model_performance.items()
                ],
                "strategy_performance": dict(self.strategy_performance),
            }
            with open(".universe_performance.json", "w") as f:
                json.dump(data, f)
        except:
            pass
            
    def _load(self):
        """Load from disk"""
        try:
            with open(".universe_performance.json", "r") as f:
                data = json.load(f)
                
            for m in data.get("model_performance", []):
                mp = ModelPerformance(m["model"])
                mp.total_tasks = m["total_tasks"]
                mp.successful_tasks = m["successful_tasks"]
                mp.total_duration_ms = m["total_duration_ms"]
                mp.total_tokens = m["total_tokens"]
                self.model_performance[m["model"]] = mp
                
            for s, p in data.get("strategy_performance", {}).items():
                self.strategy_performance[s] = p
        except:
            pass


# ============================================================================
# INTELLIGENT CACHING
# ============================================================================

@dataclass
class CacheEntry:
    """A cached result"""
    key: str
    value: Any
    timestamp: datetime
    hits: int = 0
    ttl_seconds: int = 3600
    
    def is_expired(self) -> bool:
        return (datetime.now() - self.timestamp).total_seconds() > self.ttl_seconds


class IntelligentCache:
    """
    Cache with automatic optimization.
    
    Features:
    - TTL expiry
    - Hit counting
    - LRU eviction
    - Size limits
    """
    
    def __init__(self, max_entries: int = 1000, default_ttl: int = 3600):
        self.max_entries = max_entries
        self.default_ttl = default_ttl
        self.cache: dict[str, CacheEntry] = {}
        self.hits = 0
        self.misses = 0
        self.lock = Lock()
        
    def get(self, key: str) -> Optional[Any]:
        """Get a cached value"""
        with self.lock:
            entry = self.cache.get(key)
            if entry is None:
                self.misses += 1
                return None
                
            if entry.is_expired():
                del self.cache[key]
                self.misses += 1
                return None
                
            entry.hits += 1
            self.hits += 1
            return entry.value
            
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a cached value"""
        with self.lock:
            # Evict if full
            if len(self.cache) >= self.max_entries and key not in self.cache:
                self._evict_lru()
                
            self.cache[key] = CacheEntry(
                key=key,
                value=value,
                timestamp=datetime.now(),
                ttl_seconds=ttl or self.default_ttl,
            )
            
    def _evict_lru(self):
        """Evict least recently used"""
        if not self.cache:
            return
            
        # Find entry with lowest hits
        lru_key = min(self.cache.keys(), key=lambda k: self.cache[k].hits)
        del self.cache[lru_key]
        
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / max(1, total)
        
        return {
            "entries": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
        }
        
    def clear(self):
        """Clear the cache"""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0


# ============================================================================
# SELF-OPTIMIZING ORCHESTRATOR
# ============================================================================

class SelfOptimizingOrchestrator:
    """
    An orchestrator that learns and optimizes itself.
    
    This is the core of self-improvement:
    - Tracks what works
    - Adapts strategies
    - Picks best models
    - Caches results
    """
    
    def __init__(self, num_agents: int = 100):
        self.num_agents = num_agents
        self.tracker = PerformanceTracker()
        self.cache = IntelligentCache()
        
        # Learning parameters
        self.learning_rate = 0.1
        self.exploration_rate = 0.2  # Try new things 20% of time
        
    def optimize_task(self, task: str) -> dict:
        """
        Optimize task execution based on learned patterns.
        
        Returns:
        - best_model: Model to use
        - best_strategy: Strategy to use
        - cached_result: If available
        """
        # Check cache first
        cache_key = f"{task}:{hash(task) % 10000}"
        cached = self.cache.get(cache_key)
        
        if cached is not None:
            return {
                "strategy": "cache",
                "result": cached,
                "cached": True,
            }
            
        # Get best from learning
        best_model = self.tracker.get_best_model()
        best_strategy = self.tracker.get_best_strategy()
        
        # Exploration: sometimes try something new
        import random
        if random.random() < self.exploration_rate:
            # Try alternative strategy
            alternatives = ["parallel", "sequential", "swarm", "async"]
            best_strategy = random.choice(alternatives)
            
        return {
            "model": best_model,
            "strategy": best_strategy,
            "cached": False,
        }
        
    def record_result(
        self, 
        task: str,
        duration_ms: int,
        success: bool,
        model: str,
        strategy: str,
        result: Any = None
    ):
        """Record result for learning"""
        task_id = f"{task[:20]}:{hash(task) % 10000}"
        
        # Record for learning
        self.tracker.record(
            task_id=task_id,
            duration_ms=duration_ms,
            success=success,
            model=model,
            strategy=strategy,
        )
        
        # Cache successful results
        if success and result:
            cache_key = f"{task}:{hash(task) % 10000}"
            self.cache.set(cache_key, result)
            
    def get_optimization_stats(self) -> dict:
        """Get optimization statistics"""
        return {
            "performance": self.tracker.get_stats(),
            "cache": self.cache.get_stats(),
            "learning_rate": self.learning_rate,
            "exploration_rate": self.exploration_rate,
        }


# Global instance
_optimizer = None

def get_optimizer() -> SelfOptimizingOrchestrator:
    """Get or create global optimizer"""
    global _optimizer
    if _optimizer is None:
        _optimizer = SelfOptimizingOrchestrator()
    return _optimizer


__all__ = [
    "PerformanceTracker",
    "IntelligentCache",
    "SelfOptimizingOrchestrator",
    "get_optimizer",
    "PerformanceRecord",
    "ModelPerformance",
    "CacheEntry",
]