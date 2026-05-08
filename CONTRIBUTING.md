# 🪐 Universe IDE - Contributing Guide

> "Think as super-intelligent aliens using universe physics"

This guide covers everything developers need to contribute to Universe IDE.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Module Structure](#module-structure)
6. [Adding New Features](#adding-new-features)
7. [Testing](#testing)
8. [Pull Requests](#pull-requests)

---

## Project Overview

### What is Universe IDE?

**Universe IDE** is the world's most advanced AI agentic IDE platform built on OpenHands SDK. It features:

- **1000+ parallel AI agents** - Quantum-scale processing
- **Self-Learning** - Learns from code patterns
- **Self-Updating** - Auto-health monitoring
- **Enterprise-ready** - Plugin system, RBAC, events
- **Cross-platform** - Windows, Mobile, Cloud

### Mission

Build the ultimate IDE that transcends human cognitive limitations using principles from quantum mechanics and universal computation.

---

## Architecture

### Core Layers

```
┌─────────────────────────────────────────────┐
│            UNIVERSE IDE 2.1                  │
├─────────────────────────────────────────────┤
│  APPLICATION LAYER                         │
│  ├── universe_unified.py    (IDE)           │
│  ├── universe_dashboard.py (Web UI)        │
│  └── universe_cli.py       (CLI)           │
├─────────────────────────────────────────────┤
│  AI & INTELLIGENCE LAYER                    │
│  ├── universe_ai_assist.py   (AI)           │
│  ├── universe_debug2.py     (Debugger)     │
│  └── universe_intelligent.py (Analysis)    │
├─────────────────────────────────────────────┤
│  CORE LAYER                                │
│  ├── universe_ide.py        (1000 agents)  │
│  ├── universe_messaging.py  (Comm)        │
│  ├── universe_memory.py    (Storage)      │
│  └── universe_streaming.py  (Streaming)    │
├─────────────────────────────────────────────┤
│  ENTERPRISE LAYER                          │
│  ├── universe_plugins.py   (Plugins)       │
│  ├── universe_security.py  (Auth)        │
│  ├── universe_events.py    (Webhooks)     │
│  └── universe_workflow.py  (Automation)  │
├─────────────────────────────────────────────┤
│  DEPLOYMENT LAYER                          │
│  ├── universe_cloud.py     (Multi-cloud)  │
│  ├── universe_deploy2.py   (Docker/K8s)   │
│  └── universe_server.py     (FastAPI)       │
└─────────────────────────────────────────────┘
```

### Data Flow

```python
# Typical data flow
User Input → CLI/API → Universe Core → AI Agents → Tools → Output
                    ↓
            Memory (disk + cache)
                    ↓
            Events → Plugins + Webhooks
```

---

## Development Setup

### Prerequisites

- **Python 3.13+**
- **Git**
- **uv** (package manager)

### Clone & Install

```bash
# Clone repository
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide

# Install dependencies
uv sync

# Run development
uv run python -c "from universe_ide import cosmos; print(cosmos(100))"
```

### Environment Variables

```bash
# .env file (not committed)
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
```

---

## Coding Standards

### File Naming

```
universe_<feature>.py       # Main modules
universe_<feature>2.py     # v2 of module
test_universe.py           # Tests in tests/
```

### Module Template

```python
"""
Module Title - Brief Description

Extended description of what this module does.

Usage:
    from universe_example import get_example
    ex = get_example()
"""

import asyncio
from typing import Any
from dataclasses import dataclass


# ============================================================================
# CLASSES
# ============================================================================

@dataclass
class ExampleConfig:
    """Configuration for example"""
    value: str = "default"
    enabled: bool = True


class ExampleClass:
    """
    Main class description.
    
    Args:
        config: Configuration instance
    """
    
    def __init__(self, config: ExampleConfig = None):
        self.config = config or ExampleConfig()
        self._initialized = False
        
    def process(self, data: Any) -> Any:
        """Process data"""
        return data


# ============================================================================
# GLOBALS
# ============================================================================

_instance = None


def get_example() -> ExampleClass:
    """Get singleton instance"""
    global _instance
    if _instance is None:
        _instance = ExampleClass()
    return _instance


__all__ = [
    "ExampleClass",
    "ExampleConfig", 
    "get_example",
]
```

### Docstring Style

```python
def function(param: str, option: int = 0) -> dict:
    """
    Short description.
    
    Extended description of what the function does.
    
    Args:
        param: Description of param
        option: Description of option (default: 0)
    
    Returns:
        Description of return value
    
    Example:
        >>> result = function("test")
        >>> print(result)
        {'status': 'ok'}
    """
    pass
```

---

## Module Structure

### Required Exports

Every module should export:

```python
__all__ = [
    "MainClass",      # Required: main class
    "get_xxx()",     # Required: singleton/getter
]
```

### Singleton Pattern

```python
# Use singletons for shared state
_instance = None

def get_manager() -> ManagerClass:
    """Get global manager instance"""
    global _instance
    if _instance is None:
        _instance = ManagerClass()
    return _instance
```

### Error Handling

```python
# Always handle gracefully
try:
    result = risky_operation()
except ValueError as e:
    logger.warning(f"Value error: {e}")
    return {"error": str(e)}
except Exception as e:
    logger.error(f"Unexpected: {e}")
    raise
```

### Type Hints

```python
# Always use type hints
def process(items: list[str]) -> dict[str, int]:
    """Return mapping"""
    return {item: len(item) for item in items}
```

---

## Adding New Features

### Step 1: Create Module

```bash
# universe_newfeature.py
touch universe_newfeature.py
```

### Step 2: Implement

```python
"""Universe IDE - New Feature

Description of new feature.
"""

from dataclasses import dataclass


@dataclass
class NewFeatureConfig:
    """Configuration"""
    enabled: bool = True


class NewFeature:
    """Main feature class"""
    
    def __init__(self, config: NewFeatureConfig = None):
        self.config = config or NewFeatureConfig()


_instance = None


def get_new_feature() -> NewFeature:
    """Get feature instance"""
    global _instance
    if _instance is None:
        _instance = NewFeature()
    return _instance


__all__ = ["NewFeature", "NewFeatureConfig", "get_new_feature"]
```

### Step 3: Add Tests

```python
# tests/test_newfeature.py
import pytest
from universe_newfeature import NewFeature, get_new_feature


class TestNewFeature:
    """Test new feature"""
    
    def test_basic(self):
        """Basic test"""
        feature = get_new_feature()
        assert feature is not None
        
    def test_process(self):
        """Test process"""
        feature = NewFeature()
        result = feature.process("test")
        assert result is not None
```

### Step 4: Document

Update README with new module description.

---

## Testing

### Run Tests

```bash
# All tests
uv run pytest tests/ -v

# Specific file
uv run pytest tests/test_universe.py -v

# With coverage
uv run pytest tests/ --cov=universe_ --cov-report=html
```

### Write Tests

```python
# tests/test_module.py
import pytest


class TestModuleName:
    """Test suite"""
    
    def test_something(self):
        """Test something"""
        # Arrange
        expected = "value"
        
        # Act
        actual = "value"
        
        # Assert
        assert actual == expected
        
    @pytest.mark.asyncio
    async def test_async(self):
        """Test async"""
        result = await async_function()
        assert result is not None
```

### Test Fixtures

```python
# Use fixtures from universe_testing2
from universe_testing2 import TestFixtures

@pytest.fixture
def universe():
    """Universe fixture"""
    return TestFixtures.universe_100()


def test_with_fixture(universe):
    """Test with fixture"""
    assert universe is not None
```

---

## Pull Requests

### PR Guidelines

1. **Branch naming**: `feature/description` or `fix/description`
2. **Commits**: Clear, descriptive messages
3. **Tests**: All tests pass (8/8)
4. **Documentation**: Update README if needed

### Commit Message Format

```
type: description

- detail 1
- detail 2

[Co-authored-by: name <email>]
```

Types: `feat`, `fix`, `enhance`, `docs`, `test`, `refactor`

### Example

```bash
# Create branch
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "feat: add new feature

- NewFeature class added
- Tests included
- Documentation updated

[Co-authored-by: openhands <openhands@all-hands.dev>]"

# Push and PR
git push origin feature/new-feature
# Then create PR on GitHub
```

### Review Checklist

- [ ] Tests pass (8/8)
- [ ] Code follows standards
- [ ] Documentation updated
- [ ] No secrets committed
- [ ] `__all__` exports correct

---

## Help

### Common Issues

```bash
# Import error
uv sync

# Test fails
uv run pytest tests/test_universe.py -v

# Type errors
uv run mypy universe_/
```

### Resources

- [GitHub](https://github.com/kminnthu01-cmyk/universeide)
- [Issues](https://github.com/kminnthu01-cmyk/universeide/issues)
- [OpenHands SDK](https://docs.openhands.dev/)

---

**🪐 Contributing to the Ultimate AI Agentic IDE**