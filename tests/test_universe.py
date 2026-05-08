"""
Universe IDE - Test Suite

Tests for the Universe IDE Platform.
Run with: pytest tests/test_universe.py -v
"""

import pytest
import asyncio
from universe_ide import cosmos, UniverseAI
from universe_ide import FileEditorTool, TerminalTool


class TestUniverseCore:
    """Test core Universe AI functionality"""
    
    def test_cosmos_creation(self):
        """Test cosmos() creation"""
        u = cosmos(100)
        assert u.num_agents == 100
        
    def test_cosmos_defaults(self):
        """Test cosmos defaults"""
        u = cosmos()
        assert u.num_agents == 100
        assert u.provider == "anthropic"
        
    def test_universe_attributes(self):
        """Test universe attributes"""
        u = cosmos(10)
        assert u.num_agents == 10
        assert u.model is not None
        assert u.provider is not None


@pytest.mark.asyncio
class TestAsync:
    """Test async functionality"""
    
    async def test_create_universe(self):
        """Test async universe creation"""
        from universe_ide import create_universe
        u = await create_universe(10)
        assert u.num_agents == 10
        
    async def test_deploy(self):
        """Test deploy"""
        from universe_ide import create_universe
        u = await create_universe(10)
        result = await u.deploy("test task", ".")
        assert result["status"] == "deployed"


class TestTools:
    """Test tools"""
    
    def test_file_editor(self):
        """Test file editor tool"""
        tool = FileEditorTool(".")
        assert tool is not None
        
    def test_terminal(self):
        """Test terminal tool"""
        tool = TerminalTool()
        assert tool is not None


class TestSecurity:
    """Test security features"""
    
    def test_analysis_available(self):
        """Test analysis is available"""
        from universe_ide import quick_analyze
        assert quick_analyze is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])