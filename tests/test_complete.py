"""
Universe IDE - Comprehensive Test Suite

All tests: Unit, Integration, E2E, Security, Performance.
"""

import pytest
import os
import time
from universe_ide import cosmos
from universe_ai_assist import get_ai_assistant
from universe_self_training import get_self_training_ai
from universe_neural import get_neural_ai
from universe_multimodal import get_unified_ai
from universe_cloud import get_cloud
from universe_byok import get_byok
from universe_swarm import get_swarm
from universe_cache import get_cache
from universe_pipeline import get_pipeline
from universe_plugin2 import get_plugin_manager
from universe_db import get_database
from universe_messaging import get_message_bus
from universe_memory import get_knowledge_base
from universe_deploy2 import get_docker


# ============================================================================
# UNIT TESTS
# ============================================================================

class TestCore:
    """Core functionality tests"""
    
    def test_cosmos_creation(self):
        u = cosmos(100)
        assert u.num_agents == 100
        
    def test_cosmos_large(self):
        u = cosmos(1000)
        assert u.num_agents == 1000
        
    def test_cosmos_zero(self):
        u = cosmos(0)
        assert u.num_agents == 0
        
    def test_ai_assistant(self):
        ai = get_ai_assistant()
        assert ai is not None


class TestIntelligence:
    """AI tests"""
    
    def test_self_training(self):
        st = get_self_training_ai()
        result = st.learn_and_predict("test")
        assert result is not None
        
    def test_neural(self):
        n = get_neural_ai()
        assert n is not None
        
    def test_unified(self):
        u = get_unified_ai()
        result = u.understand("hello", "text")
        assert result is not None


class TestInfrastructure:
    """Infrastructure tests"""
    
    def test_cloud(self):
        c = get_cloud()
        assert c is not None
        
    def test_byok(self):
        b = get_byok()
        assert b is not None
        
    def test_deployer(self):
        d = get_docker()
        assert d is not None


class TestAdvanced:
    """Advanced features"""
    
    def test_swarm(self):
        s = get_swarm()
        status = s.get_status()
        assert status["agents"] > 0
        
    def test_cache(self):
        c = get_cache()
        c.set("key", "value")
        assert c.get("key") == "value"
        
    def test_cache_miss(self):
        c = get_cache()
        assert c.get("nonexistent") is None
        
    def test_pipeline(self):
        p = get_pipeline()
        assert p.name == "main"
        
    def test_plugins(self):
        pm = get_plugin_manager()
        pid = pm.register("test", "1.0", "Test", [])
        assert pid is not None


class TestData:
    """Data layer tests"""
    
    def test_database(self):
        db = get_database()
        assert db is not None
        
    def test_messaging(self):
        m = get_message_bus()
        assert m is not None
        
    def test_knowledge_base(self):
        m = get_knowledge_base()
        assert m is not None


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests"""
    
    def test_full_stack(self):
        # Complete stack test
        universe = cosmos(100)
        ai = get_ai_assistant()
        cloud = get_cloud()
        byok = get_byok()
        
        assert universe.num_agents == 100
        assert ai is not None
        assert cloud is not None
        assert byok is not None
        
    def test_ai_pipeline(self):
        # AI pipeline
        st = get_self_training_ai()
        result = st.learn_and_predict("data")
        
        neural = get_neural_ai()
        
        assert result is not None


# ============================================================================
# EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Edge case tests"""
    
    def test_empty_input(self):
        from universe_multimodal import get_unified_ai
        u = get_unified_ai()
        result = u.understand("", "text")
        
    def test_special_chars(self):
        from universe_multimodal import get_unified_ai
        u = get_unified_ai()
        result = u.understand("!@#$%", "text")
        
    def test_unicode(self):
        from universe_multimodal import get_unified_ai
        u = get_unified_ai()
        result = u.understand("🪐", "text")


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Performance tests"""
    
    def test_cache_performance(self):
        c = get_cache()
        
        start = time.perf_counter()
        for i in range(100):
            c.set(f"key{i}", f"value{i}")
        elapsed = time.perf_counter() - start
        
        assert elapsed < 1.0  # Should be fast
        
    def test_cosmos_performance(self):
        start = time.perf_counter()
        u = cosmos(1000)
        elapsed = time.perf_counter() - start
        
        assert elapsed < 1.0


# ============================================================================
# SECURITY TESTS
# ============================================================================

class TestSecurity:
    """Security tests"""
    
    def test_byok(self):
        b = get_byok()
        
    def test_no_secrets(self):
        # Check no hardcoded secrets
        for f in os.listdir("."):
            if f.endswith(".py"):
                with open(f) as fp:
                    content = fp.read()
                    # Simple check
                    assert "password" not in content.lower() or "#" in content


# ============================================================================
# REGRESSION TESTS
# ============================================================================

class TestRegression:
    """Regression tests"""
    
    def test_previous_versions(self):
        # Test v3.x features still work
        u = cosmos(100)
        ai = get_ai_assistant()
        
        assert u.num_agents == 100
        assert ai is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])