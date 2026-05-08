#!/usr/bin/env python3
"""
🪐 Universe IDE - Advanced Examples

Advanced use cases demonstrating the platform capabilities.
"""

import asyncio
import json
import random


# ============================================================================
# ADVANCED EXAMPLE 1: Auto-Healing System
# ============================================================================

async def example_auto_healing():
    """
    System that detects failures and auto-heals using resilience.
    """
    from universe import create_universe
    from universe_resilience import CircuitBreaker, RetryConfig
    
    print("=== Auto-Healing System ===")
    
    # Create universe with circuit breaker
    universe = await create_universe(num_agents=10)
    print(f"✓ Created {universe.num_agents} agents")
    
    # Configure circuit breaker
    circuit = CircuitBreaker("universe", config=CircuitConfig(
        failure_threshold=3,
        timeout_seconds=5.0
    ))
    
    # Simulate work with potential failures
    for i in range(10):
        try:
            result = circuit.call(lambda: f"task_{i}")
            print(f"  Task {i}: SUCCESS")
        except CircuitBreakerOpen:
            print(f"  Task {i}: CIRCUIT OPEN - Waiting...")
            await asyncio.sleep(1)
            
    print("✓ Auto-healing complete")


# ============================================================================
# ADVANCED EXAMPLE 2: Real-Time Monitoring Dashboard
# ============================================================================

def example_monitoring_dashboard():
    """
    Real-time monitoring with live metrics.
    """
    from universe_monitoring import MonitoringDashboard, AlertLevel
    
    print("=== Real-Time Monitoring ===")
    
    # Create dashboard
    dash = MonitoringDashboard()
    
    # Simulate metrics
    for i in range(5):
        dash.record_metric('cpu.usage', random.uniform(10, 90))
        dash.record_metric('memory.usage', random.uniform(20, 80))
        dash.record_metric('tasks.completed', random.randint(1, 10))
        
        if random.random() < 0.3:
            dash.alert(AlertLevel.WARNING, f"High load at {i}")
    
    # Get snapshot
    snapshot = dash.get_snapshot()
    
    print(f"  CPU: {snapshot['metrics'].get('cpu.usage', 0):.1f}%")
    print(f"  Memory: {snapshot['metrics'].get('memory.usage', 0):.1f}%")
    print(f"  Tasks: {snapshot['metrics'].get('tasks.completed', 0):.0f}")
    print(f"  Alerts: {snapshot['alerts']['total']}")
    
    print("✓ Dashboard working")


# ============================================================================
# ADVANCED EXAMPLE 3: Performance Optimization  
# ============================================================================

def example_performance_tuning():
    """
    Performance optimization with caching and parallelism.
    """
    from universe_optimize import PerformanceOptimizer
    import time
    
    print("=== Performance Optimization ===")
    
    opt = PerformanceOptimizer()
    
    # Simulate computation
    def slow_func(x):
        time.sleep(0.01)  # Simulate work
        return x ** 2
    
    # First call (slow)
    start = time.time()
    result1 = opt.cached_execute("square_9", slow_func, 9)
    time1 = time.time() - start
    
    # Second call (fast from cache)
    start = time.time()
    result2 = opt.cached_execute("square_9", slow_func, 9)
    time2 = time.time() - start
    
    print(f"  First call: {time1*1000:.1f}ms -> {result1}")
    print(f"  Cached call: {time2*1000:.2f}ms -> {result2}")
    print(f"  Speedup: {time1/max(0.0001, time2):.0f}x")
    
    # Parallel execution
    items = list(range(10))
    start = time.time()
    results = opt.parallel_map(lambda x: x**2, items)
    time_parallel = time.time() - start
    
    print(f"  Parallel: {time_parallel*1000:.1f}ms for {len(items)} items")
    print("✓ Performance optimized")


# ============================================================================
# ADVANCED EXAMPLE 4: Self-Learning Model Selection
# ============================================================================

def example_self_learning():
    """
    System that learns best models from experience.
    """
    from universe_selflearn import PerformanceTracker
    
    print("=== Self-Learning ===")
    
    tracker = PerformanceTracker()
    
    # Simulate task history
    models = ["claude-gpt", "openai-gpt", "gemini"]
    strategies = ["parallel", "sequential", "swarm"]
    
    for _ in range(20):
        model = random.choice(models)
        strategy = random.choice(strategies)
        duration = random.randint(100, 5000)
        success = random.random() > 0.2  # 80% success
        
        tracker.record(
            task_id=f"task_{_}",
            duration_ms=duration,
            success=success,
            model=model,
            strategy=strategy
        )
    
    # Get learned recommendations
    best_model = tracker.get_best_model()
    best_strategy = tracker.get_best_strategy()
    stats = tracker.get_stats()
    
    print(f"  Best model: {best_model}")
    print(f"  Best strategy: {best_strategy}")
    print(f"  Total records: {stats['total_records']}")
    
    print("✓ Self-learning working")


# ============================================================================
# ADVANCED EXAMPLE 5: Full Stack with All Features
# ============================================================================

async def example_full_stack():
    """
    Complete application using all features.
    """
    from universe import create_universe
    from universe_selflearn import get_optimizer
    from universe_selfupdate import get_health_monitor
    from universe_monitoring import get_monitoring
    from universe_resilience import get_resilience
    from universe_optimize import get_performance_optimizer
    
    print("=== Full Stack Application ===")
    
    # Initialize components
    universe = await create_universe(num_agents=50)
    optimizer = get_optimizer()
    health = get_health_monitor()
    monitoring = get_monitoring()
    resilience = get_resilience()
    performance = get_performance_optimizer()
    
    print(f"✓ Universe: {universe.num_agents} agents")
    
    # Track start
    monitoring.start_timer("task")
    
    # Deploy task with optimization
    result = await universe.deploy("Build API", "src/")
    
    # Track completion
    monitoring.stop_timer("task")
    monitoring.track_event("task_completed", {"task": "Build API", "result": result})
    
    # Get status
    snapshot = monitoring.get_snapshot()
    perf_stats = performance.get_stats()
    
    print(f"  Task: {result['status']}")
    print(f"  Duration: {snapshot['performance']}")
    print(f"  Cache: {perf_stats['cache']['hit_rate']:.1%}")
    
    # Health check
    health_status = health.run_full_check()
    print(f"  Health: {'✓' if health_status.healthy else '✗'}")
    
    print("✓ Full stack working")


# ============================================================================
# ADVANCED EXAMPLE 6: Web API Server
# ============================================================================

def example_api_server():
    """
    Example FastAPI server using Universe IDE.
    """
    print("=== API Server Example ===")
    
    # This would be the code for a FastAPI server
    code = '''
from fastapi import FastAPI
from universe_ide import cosmos
from universe_monitoring import get_monitoring

app = FastAPI()
monitoring = get_monitoring()

@app.post("/cosmos")
async def create_universe(agents: int):
    universe = cosmos(agents)
    monitoring.track_event("universe_created", {"agents": agents})
    return {"agents": agents, "status": "created"}

@app.get("/monitoring")
async def get_stats():
    return monitoring.get_snapshot()
'''
    
    print("  FastAPI setup:")
    for line in code.split('\n')[:5]:
        print(f"    {line}")
    print("  ...")
    
    print("✓ API example ready")


# ============================================================================
# ADVANCED EXAMPLE 7: Kubernetes Deployment
# ============================================================================

def example_k8s_deployment():
    """
    Example Kubernetes deployment.
    """
    print("=== Kubernetes Deployment ===")
    
    yaml = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: universe-ide
spec:
  replicas: 3
  selector:
    matchLabels:
      app: universe-ide
  template:
    metadata:
      labels:
        app: universe-ide
    spec:
      containers:
      - name: universe
        image: universe-ide:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            nvidia.com/gpu: 1
          requests:
            cpu: "2"
            memory: "4Gi"
'''
    print("  Deployment config:")
    for line in yaml.split('\n')[:8]:
        print(f"    {line}")
    print("  ...")
    
    print("✓ K8s example ready")


# ============================================================================
# RUN ALL ADVANCED EXAMPLES
# ============================================================================

async def run_all():
    """Run all advanced examples"""
    print("=" * 60)
    print("🪐 UNIVERSE IDE - ADVANCED EXAMPLES")
    print("=" * 60)
    
    # Example 1
    print()
    example_monitoring_dashboard()
    
    # Example 2
    print()
    example_performance_tuning()
    
    # Example 3
    print()
    example_self_learning()
    
    # Example 4 (async)
    print()
    await example_full_stack()
    
    # Example 5
    print()
    example_api_server()
    
    # Example 6
    print()
    example_k8s_deployment()
    
    print()
    print("=" * 60)
    print("✓ ALL ADVANCED EXAMPLES COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all())