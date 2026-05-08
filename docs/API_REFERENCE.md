# Universe IDE - API Reference

## All Modules

### Core

```python
from universe_ide import cosmos
```

```python
universe = cosmos(1000)  # Create 1000 agents
universe.num_agents    # int: Number of agents
universe.agents      # list: Agent list
```

### AI Assistant

```python
from universe_ai_assist import get_ai_assistant
```

```python
ai = get_ai_assistant()
ai.analyze(code)   # Analyze code
ai.explain(code)   # Explain code
ai.fix(code)      # Fix code issues
```

### Self-Training AI

```python
from universe_self_training import get_self_training_ai

ai = get_self_training_ai()
result = ai.learn_and_predict("input")
ai.auto_improve()
```

### Neural Code

```python
from universe_neural import get_neural_ai

neural = get_neural_ai()
result = neural.analyze(code)
```

### Multi-Modal

```python
from universe_multimodal import get_unified_ai

unified = get_unified_ai()
result = unified.understand(content, modality)
```

### Quantum Efficiency

```python
from universe_quantum import get_efficiency_engine

engine = get_efficiency_engine()
result = engine.process(data, operation)
```

### Cloud

```python
from universe_cloud import get_cloud

cloud = get_cloud()
cloud.deploy_aws("app", config)
cloud.deploy_gcp("app", config)
cloud.deploy_vercel("app", config)
```

### BYOK Security

```python
from universe_byok import get_byok

vault = get_byok()
vault.add_key(name, key, key_type)
```

### Database

```python
from universe_database import get_database

db = get_database()
db.save(key, value)
value = db.get(key)
```

### Messaging

```python
from universe_messaging import get_message_bus

bus = get_message_bus()
bus.send(message, recipient)
inbox = bus.inbox(recipient)
```

### Memory

```python
from universe_memory import get_knowledge_base

kb = get_knowledge_base()
kb.learn(key, value)
value = kb.recall(key)
```

### Events

```python
from universe_events2 import get_event_system

events = get_event_system()
events.emit("event", data)
events.on("event", handler)
```

### Editor

```python
from universe_editor import get_editor

editor = get_editor()
editor.open(file)
editor.save()
```

### Terminal

```python
from universe_terminal import get_terminal

terminal = get_terminal()
terminal.run(command)
```

### Workflow

```python
from universe_workflow2 import get_automation

workflow = get_automation()
workflow.run(name)
```

### REST API

```python
from universe_api2 import get_api

api = get_api()
response = api.handle(method, path, data)
```

### Server

```python
from universe_server import Server

server = Server(host="0.0.0.0", port=8000)
server.start()
server.stop()
```

### Graph Algorithms

```python
from universe_graphs import Graph

graph = Graph()
graph.add_edge(u, v)
graph.bfs(start)
graph.dfs(start)
```

### Real-time

```python
from universe_realtime import get_realtime

rt = get_realtime()
rt.add(data)
stats = rt.get_stats()
```

### UI Components

```python
from universe_ui import Theme, Button, Input, Card

# Theme
theme = Theme.UNIVERSE  # Dark Universe theme

# Button
Button.render(label, variant, size)

# Input
Input.render(placeholder, type)

# Card
Card.render(title, content)
```

### UX Features

```python
from universe_ux2 import (
    CommandPalette,
    KeyboardManager,
    Toast,
    Autocomplete,
)

# Command palette
palette = CommandPalette()
palette.register("command", action, shortcut)
palette.search(query)

# Keyboard
kb = KeyboardManager()
kb.register("ctrl+s", save_action)

# Toast
toast = get_toast()
toast.show(message, type)

# Autocomplete
auto = Autocomplete()
completions = auto.get_completions(prefix)
```

---

## Function Summary

| Module | Function | Description |
|--------|----------|-------------|
| universe_ide | cosmos(n) | Create universe |
| universe_ai | get_ai_assistant() | AI assistant |
| universe_self_training | get_self_training_ai() | Self-training |
| universe_neural | get_neural_ai() | Neural code |
| universe_multimodal | get_unified_ai() | Multi-modal |
| universe_quantum | get_efficiency_engine() | Quantum |
| universe_cloud | get_cloud() | Cloud |
| universe_byok | get_byok() | BYOK |
| universe_database | get_database() | Database |
| universe_messaging | get_message_bus() | Messaging |
| universe_memory | get_knowledge_base() | Memory |
| universe_events2 | get_event_system() | Events |
| universe_editor | get_editor() | Editor |
| universe_terminal | get_terminal() | Terminal |
| universe_workflow2 | get_automation() | Workflow |
| universe_api2 | get_api() | REST API |
| universe_server | Server | Server |
| universe_graphs | Graph | Graph algo |
| universe_realtime | get_realtime() | Real-time |
| universe_ui | Theme | UI theme |
| universe_ux2 | CommandPalette | UX |

**🪐 Universe IDE API Reference**