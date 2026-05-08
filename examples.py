#!/usr/bin/env python3
"""
🪐 Universe IDE - Example Scripts

Ready-to-run examples showing what's possible.
"""

import asyncio

# ============================================================================
# EXAMPLE 1: Quick Start - One Line
# ============================================================================

def example_quick_start():
    """
    The simplest possible usage.
    
    Result: Creates 100 parallel AI agents ready to work
    """
    from universe_ide import cosmos
    
    # ONE LINE - creates 100 parallel agents!
    universe = cosmos(100)
    
    print(f"✓ Created {universe.num_agents} agents")
    print(f"  Provider: {universe.provider}")
    print(f"  Model: {universe.model}")
    return universe


# ============================================================================
# EXAMPLE 2: Deploy Task
# ============================================================================

async def example_deploy_task():
    """
    Deploy a task to the agent swarm.
    
    Result: All agents work on the task in parallel
    """
    from universe_ide import create_universe
    
    # Create universe
    universe = await create_universe(num_agents=50)
    
    # Deploy work
    result = await universe.deploy(
        task="Build a REST API with FastAPI",
        target="src/api/"
    )
    
    print(f"✓ Task deployed: {result['status']}")
    print(f"  Agents: {universe.num_agents}")
    return result


# ============================================================================
# EXAMPLE 3: Code Analysis
# ============================================================================

def example_code_analysis():
    """
    Analyze code for security issues.
    
    Result: Detailed report with vulnerabilities
    """
    from universe_ide import quick_analyze
    
    if quick_analyze is None:
        print("⚠ Analysis not available")
        return {"issues": 0}
    
    # Code to analyze
    code = '''
import os
import sqlite3

def login(username, password):
    # SQL injection vulnerability!
    query = f"SELECT * FROM users WHERE name = '{username}'"
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    return cursor.execute(query)
    
def run_command():
    os.system(input())  # Command injection!
'''

    # Analyze
    result = quick_analyze(code)
    
    print(f"✓ Code Score: {result['score']}/100")
    print(f"  Issues Found: {result['issues']}")
    print(f"  Critical: {result.get('critical', 0)}")
    print(f"  High: {result.get('high', 0)}")
    
    for issue in result.get('issues_detail', [])[:5]:
        print(f"  [{issue['severity']}] Line {issue['line']}: {issue['message'][:50]}...")
    
    return result


# ============================================================================
# EXAMPLE 4: Security Scanner
# ============================================================================

def example_security_scanner():
    """
    Scan a repository for security issues.
    
    Result: List of all security vulnerabilities
    """
    from universe_ide import cosmos, quick_analyze
    
    universe = cosmos(10)
    
    if quick_analyze is None:
        print("⚠ Analysis not available")
        return []
    
    # Analyze files
    results = []
    for path in ['src/auth.py', 'src/api.py', 'src/db.py']:
        try:
            with open(path) as f:
                code = f.read()
            result = quick_analyze(code)
            results.append((path, result))
        except FileNotFoundError:
            pass
            
    print(f"✓ Scanned {len(results)} files")
    return results


# ============================================================================
# EXAMPLE 5: Parallel File Operations
# ============================================================================

async def example_parallel_files():
    """
    Use multiple agents to work on files in parallel.
    
    Result: Fast batch processing
    """
    from universe_ide import create_universe
    
    universe = await create_universe(num_agents=100)
    
    # Files to process
    files = [
        "src/module1.py",
        "src/module2.py", 
        "src/module3.py",
        "tests/test1.py",
        "tests/test2.py",
    ]
    
    # Each agent works on one file
    tasks = [f"Optimize {f}" for f in files]
    
    # Execute in parallel
    results = await universe.execute_parallel(tasks)
    
    print(f"✓ Processed {len(results)} files in parallel")
    return results


# ============================================================================
# EXAMPLE 6: Full IDE Setup
# ============================================================================

def example_full_ide():
    """
    Full IDE with all features.
    
    Result: Complete development environment
    """
    from universe_ide import UniverseIDEPackage
    
    # Create full IDE
    ide = UniverseIDEPackage(num_agents=100)
    
    print(f"✓ Universe IDE ready")
    print(f"  Agents: {ide.num_agents}")
    
    # Get metrics
    metrics = ide.get_metrics()
    print(f"  Specializations: {metrics.get('swarm_specializations', 8)}")
    print(f"  Security Rules: {metrics.get('security_rules', 25)}")
    
    return ide


# ============================================================================
# EXAMPLE 7: Swarm Orchestration
# ============================================================================

def example_swarm_orchestration():
    """
    Advanced multi-agent orchestration.
    
    Result: Task decomposition and parallel execution
    """
    from universe_ide import cosmos
    
    universe = cosmos(10)
    
    # Decompose complex task
    task = "Build a complete e-commerce platform"
    
    print(f"✓ Universe with 10 agents ready")
    print(f"  Provider: {universe.provider}")
    print(f"  Model: {universe.model}")
    print(f"  Task: {task}")
    print(f"\n  Each agent specializes in:")
    print(f"  - architect (system design)")
    print(f"  - coder (implementation)")
    print(f"  - prover (testing)")
    print(f"  - debugger (bug fixing)")
    print(f"  - optimizer (performance)")
    print(f"  - security (vulnerability scanning)")
    print(f"  - reviewer (code review)")
    print(f"  - documenter (docs)")
    
    return universe


# ============================================================================
# EXAMPLE 8: Custom Tool Creation
# ============================================================================

def example_custom_tools():
    """
    Create custom tools for agents.
    
    Result: Extended agent capabilities
    """
    from universe_ide import cosmos
    
    universe = cosmos(10)
    
    print(f"✓ Universe IDE ready")
    print(f"  Agents: {universe.num_agents}")
    print(f"  Built-in Tools:")
    print(f"    - FileEditor (read/write files)")
    print(f"    - Terminal (run commands)")
    print(f"    - Browser (web interaction)")
    print(f"    - Git (version control)")
    print(f"    - Docker (containers)")
    print(f"    - Search (grep, web search)")
    
    return universe


# ============================================================================
# RUN ALL EXAMPLES
# ============================================================================

async def run_all_examples():
    """Run all examples"""
    import asyncio
    
    print("=" * 60)
    print("🪐 UNIVERSE IDE EXAMPLES")
    print("=" * 60)
    
    # Example 1
    print("\n" + "=" * 40)
    print("Example 1: Quick Start")
    print("=" * 40)
    example_quick_start()
    
    # Example 2
    print("\n" + "=" * 40)
    print("Example 2: Deploy Task")
    print("=" * 40)
    await example_deploy_task()
    
    # Example 3
    print("\n" + "=" * 40)
    print("Example 3: Code Analysis")
    print("=" * 40)
    example_code_analysis()
    
    # Example 4
    print("\n" + "=" * 40)
    print("Example 4: Full IDE")
    print("=" * 40)
    example_full_ide()
    
    # Example 5
    print("\n" + "=" * 40)
    print("Example 5: Swarm Orchestration")
    print("=" * 40)
    example_swarm_orchestration()
    
    print("\n" + "=" * 60)
    print("✓ ALL EXAMPLES COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_examples())