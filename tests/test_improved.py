"""
Universe IDE - Testing Improvements

Comprehensive test suite.
"""

import pytest
from universe_ide import cosmos
from universe_ai_assist import get_ai_assistant
from universe_self_training import get_self_training_ai
from universe_neural import get_neural_ai
from universe_multimodal import get_unified_ai
from universe_cloud import get_cloud
from universe_byok import get_byok
from universe_swarm import get_swarm
from universe_cache import get_cache


# ============================================================================
# CORE TESTS
# ============================================================================

class TestUniverseCore:
    """Test core functionality"""
    
    def test_cosmos(self):
        u = cosmos(100)
        assert u.num_agents == 100
        
    def test_ai_assistant(self):
        ai = get_ai_assistant()
        assert ai is not None
        
    def test_self_training_ai(self):
        ai = get_self_training_ai()
        result = ai.learn_and_predict("test")
        assert result is not None


class TestIntelligence:
    """Test AI features"""
    
    def test_neural(self):
        neural = get_neural_ai()
        assert neural is not None
        
    def test_unified_multi_modal(self):
        unified = get_unified_ai()
        result = unified.understand("hello", "text")
        assert result is not None


class TestInfrastructure:
    """Test infrastructure"""
    
    def test_cloud(self):
        cloud = get_cloud()
        assert cloud is not None
        
    def test_byok(self):
        byok = get_byok()
        assert byok is not None


class TestAdvanced:
    """Test advanced features"""
    
    def test_swarm(self):
        swarm = get_swarm()
        status = swarm.get_status()
        assert status["agents"] > 0
        
    def test_cache(self):
        cache = get_cache()
        cache.set("test", "value")
        value = cache.get("test")
        assert value == "value"


# ============================================================================
# ADDITIONAL TESTS
# ============================================================================

class TestEdgeCases:
    """Test edge cases"""
    
    def test_cosmos_zero(self):
        u = cosmos(0)
        assert u.num_agents == 0
        
    def test_cache_miss(self):
        cache = get_cache()
        value = cache.get("nonexistent")
        # None or None is acceptable


class TestIntegration:
    """Integration tests"""
    
    def test_full_stack(self):
        # Test full stack
        universe = cosmos(10)
        ai = get_ai_assistant()
        cloud = get_cloud()
        
        assert universe.num_agents == 10
        assert ai is not None
        assert cloud is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])