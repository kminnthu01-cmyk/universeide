# 🪐 Universe IDE

## The Universe's Best Open Source AI Agentic IDE Platform

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Core Features](#core-features)
4. [AI Agents](#ai-agents)
5. [IDE Interface](#ide-interface)
6. [Cloud Deployment](#cloud-deployment)
7. [Security](#security)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Run in 5 Seconds

```bash
# Clone and run
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide

# Create universe with 1000 AI agents
python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

### Open UI

```bash
# Open in browser
open universe_ide_ui.html
```

---

## Installation

### Requirements

- Python 3.13+
- Git

### Install from Source

```bash
# Clone
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide

# Virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Run tests
pytest tests/ -v
```

### Install from PyPI (Coming Soon)

```bash
pip install universe-ide
```

---

## Core Features

### 1000 Parallel AI Agents

```python
from universe_ide import cosmos

# Create universe with 1000 agents
universe = cosmos(1000)
print(universe.num_agents)  # 1000
```

### Self-Training AI

```python
from universe_self_training import get_self_training_ai

ai = get_self_training_ai()

# Learn and predict
result = ai.learn_and_predict("test input")
print(result)
```

### Neural Code Understanding

```python
from universe_neural import get_neural_ai

neural = get_neural_ai()

# Analyze code
result = neural.analyze("def test(): return 42")
print(result)
```

### Multi-Modal Processing

```python
from universe_multimodal import get_unified_ai

unified = get_unified_ai()

# Process any input type
result = unified.understand("hello", "text")
print(result)
```

---

## AI Agents

### Creating Agents

```python
from universe_ide import cosmos

# 1000 parallel agents
universe = cosmos(1000)
```

### Agent Communication

```python
from universe_messaging import get_message_bus

bus = get_message_bus()
bus.send("Hello!", recipient="agent-1")
```

### Knowledge

```python
from universe_memory import get_knowledge_base

kb = get_knowledge_base()
kb.learn("key", "value")
value = kb.recall("key")
```

---

## IDE Interface

### Open Web UI

```bash
open universe_ide_ui.html
```

### Features

- **Sidebar**: File explorer with folder tree
- **Code Editor**: Syntax highlighting, line numbers
- **Terminal**: Integrated terminal
- **Tabs**: Multiple files
- **Status Bar**: Version, agents, encoding
- **Command Palette**: Ctrl+P

### Keyboard Shortcuts

| Shortcut | Action |
|---------|--------|
| Ctrl+P | Command Palette |
| Ctrl+S | Save |
| Ctrl+B | Toggle Sidebar |
| Ctrl+J | Toggle Terminal |

---

## Cloud Deployment

### AWS

```python
from universe_cloud import get_cloud

cloud = get_cloud()

# Deploy to AWS
cloud.deploy_aws("my-app", {"region": "us-east-1"})
```

### GCP

```python
# Deploy to GCP
cloud.deploy_gcp("my-app", {"region": "us-central1"})
```

### Vercel

```python
# Deploy to Vercel
cloud.deploy_vercel("my-app", {})
```

---

## Security

### BYOK (Bring Your Own Key)

```python
from universe_byok import get_byok, KeyType

vault = get_byok()

# Add your own key
key_id = vault.add_key("my-key", "secret-value", KeyType.ENCRYPTION)
```

### Generate Key

```python
from universe_byok import BYOKEncryption

# Generate secure key
key = BYOKEncryption.generate_key()
```

---

## API Reference

### Core Modules

| Module | Description |
|--------|-------------|
| `universe_ide.py` | Core: 1000 parallel agents |
| `universe_ai_assist.py` | AI Assistant |
| `universe_self_training.py` | Self-training AI |
| `universe_neural.py` | Neural code understanding |
| `universe_multimodal.py` | Multi-modal processing |
| `universe_cloud.py` | Cloud deployment |
| `universe_byok.py` | Security (BYOK) |
| `universe_quantum.py` | Quantum efficiency |

### Quick Import

```python
# All main modules
from universe_ide import cosmos
from universe_ai_assist import get_ai_assistant
from universe_self_training import get_self_training_ai
from universe_neural import get_neural_ai
from universe_multimodal import get_unified_ai
from universe_cloud import get_cloud
from universe_byok import get_byok
```

---

## Troubleshooting

### Tests Failing

```bash
# Run with verbose
pytest tests/ -v

# Run specific test
pytest tests/test_universe.py -v
```

### Import Errors

```bash
# Clean and reinstall
rm -rf __pycache__ .venv
pip install -e .
```

### Performance Issues

```bash
# Check Python version
python --version  # Should be 3.13+
```

---

## License

MIT License

**🪐 Universe IDE - The Universe's Best Open Source AI Agentic IDE Platform**