"""
Universe IDE - Testing Utilities

Test helpers and utilities.
"""

import asyncio
import unittest
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================================
# TEST HELPERS
# ============================================================================

class AsyncTestCase(unittest.TestCase):
    """Base async test case"""
    
    def asyncSetUp(self):
        """Setup async"""
        pass
        
    def asyncTearDown(self):
        """Teardown async"""
        pass


# ============================================================================
# MOCKS
# ============================================================================

class MockUniverse:
    """Mock universe for testing"""
    
    def __init__(self, num_agents: int = 10):
        self.num_agents = num_agents
        self.provider = "mock"
        self.model = "mock-model"
        self.deployed = False
        
    def deploy(self, task: str) -> dict:
        """Mock deploy"""
        self.deployed = True
        return {"status": "deployed", "task": task}


class MockAgent:
    """Mock agent for testing"""
    
    def __init__(self, agent_id: str = "test"):
        self.agent_id = agent_id
        self.messages = []
        
    def send(self, message: str):
        """Mock send"""
        self.messages.append(message)


# ============================================================================
# FIXTURES
# ============================================================================

@dataclass
class TestFixture:
    """Test fixture"""
    name: str
    setup_fn: Callable
    teardown_fn: Callable = None


class FixtureManager:
    """Manage test fixtures"""
    
    def __init__(self):
        self.fixtures: dict[str, TestFixture] = {}
        
    def register(self, name: str, setup: Callable, teardown: Callable = None):
        """Register fixture"""
        self.fixtures[name] = TestFixture(name, setup, teardown)
        
    def setup(self, name: str) -> Any:
        """Setup fixture"""
        if name in self.fixtures:
            return self.fixtures[name].setup_fn()
        return None
        
    def teardown(self, name: str):
        """Teardown fixture"""
        if name in self.fixtures and self.fixtures[name].teardown_fn:
            self.fixtures[name].teardown_fn()


# ============================================================================
# ASSERTIONS
# ============================================================================

def assert_universe_healthy(universe) -> bool:
    """Assert universe is healthy"""
    return (
        universe is not None and 
        hasattr(universe, 'num_agents') and
        universe.num_agents > 0
    )


def assert_agent_valid(agent) -> bool:
    """Assert agent is valid"""
    return (
        agent is not None and
        hasattr(agent, 'agent_id')
    )


# ============================================================================
# TEST RUNNER
# ============================================================================

class TestRunner:
    """Test runner utilities"""
    
    def __init__(self):
        self.results: list = []
        
    def run_sync(self, test_fn: Callable):
        """Run sync test"""
        try:
            test_fn()
            self.results.append({"test": test_fn.__name__, "passed": True})
            return True
        except Exception as e:
            self.results.append({"test": test_fn.__name__, "passed": False, "error": str(e)})
            return False
            
    def run_async(self, test_fn: Callable):
        """Run async test"""
        try:
            result = asyncio.run(test_fn())
            self.results.append({"test": test_fn.__name__, "passed": True})
            return True
        except Exception as e:
            self.results.append({"test": test_fn.__name__, "passed": False, "error": str(e)})
            return False
            
    def get_results(self) -> dict:
        """Get results"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get("passed"))
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / max(1, total),
        }


# ============================================================================
# TEST UTILS
# ============================================================================

def create_test_universe(n: int = 10):
    """Create test universe"""
    from universe_ide import cosmos
    return cosmos(n)


def cleanup_test_universe(universe):
    """Cleanup test universe"""
    if universe:
        universe = None


__all__ = [
    "AsyncTestCase",
    "MockUniverse",
    "MockAgent",
    "TestFixture", 
    "FixtureManager",
    "assert_universe_healthy",
    "assert_agent_valid",
    "TestRunner",
    "create_test_universe",
    "cleanup_test_universe",
]