# 🪐 Universe IDE - API Reference

> Complete API documentation for all modules.

---

## Core

### universe_ide

Main entry point with 1000 parallel AI agents.

```python
from universe_ide import cosmos, UniverseAI, create_universe
```

#### cosmos(num_agents: int = 100) -> UniverseAI

Create universe with N parallel agents.

```python
# Basic
universe = cosmos(1000)

# With config
universe = cosmos(100, provider="openai", model="gpt-4")
```

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| num_agents | int | 100 | Number of parallel agents |
| provider | str | "anthropic" | LLM provider |
| model | str | "claude-sonnet-4-20250505" | Model name |

**Returns:** `UniverseAI` instance

#### UniverseAI class

Main universe class.

```python
universe = cosmos(1000)
print(universe.num_agents)    # 1000
print(universe.provider)       # anthropic
print(universe.model)         # claude-sonnet-4-20250505
```

**Attributes:**

| Attr | Type | Description |
|------|------|-------------|
| num_agents | int | Number of agents |
| provider | str | LLM provider |
| model | str | Model name |

---

## Messaging

### universe_messaging

Inter-agent communication.

```python
from universe_messaging import MessageBus, get_message_bus
```

#### MessageBus

Message bus for agent communication.

```python
bus = get_message_bus()

# Create message
msg = bus.create_message("Hello agents!", recipient="agent-2")

# Send
bus.send(msg)

# Receive
inbox = bus.get_inbox()
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `create_message(content, recipient)` | Message | Create message |
| `send(message)` | None | Send message |
| `get_inbox(agent_id)` | list | Get inbox |
| `get_outbox(agent_id)` | list | Get outbox |

#### Message

```python
@dataclass
class Message:
    id: str
    content: str
    sender: str
    recipient: str
    timestamp: datetime
    read: bool = False
```

---

### universe_memory

Persistent knowledge base.

```python
from universe_memory import KnowledgeBase, get_knowledge_base
```

#### KnowledgeBase

```python
kb = get_knowledge_base()

# Store
kb.store("key", {"data": "value"})

# Retrieve
data = kb.retrieve("key")

# Search
results = kb.search("query")
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `store(key, value)` | None | Store value |
| `retrieve(key)` | Any | Retrieve value |
| `delete(key)` | None | Delete key |
| `search(query)` | list | Search |
| `list_keys()` | list | List all keys |

---

### universe_streaming

Real-time token streaming.

```python
from universe_streaming import StreamManager, get_stream_manager
```

#### StreamManager

```python
sm = get_stream_manager()

# Connect to stream
async for token in sm.stream("prompt"):
    print(token, end="", flush=True)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `stream(prompt)` | AsyncIterator | Stream tokens |
| `subscribe(handler)` | None | Subscribe to stream |

---

### universe_queue

Async task queue.

```python
from universe_queue import TaskQueue, get_task_queue
```

#### TaskQueue

```python
queue = get_task_queue()

# Enqueue task
await queue.enqueue(task_function, args)

# Get status
status = await queue.get_status(task_id)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `enqueue(fn, args)` | str | Enqueue task |
| `get_status(task_id)` | dict | Get status |
| `cancel(task_id)` | None | Cancel task |

---

## AI & Intelligence

### universe_ai_assist

AI-powered code assistance.

```python
from universe_ai_assist import AIAssistant, get_ai_assistant
```

#### AIAssistant

```python
ai = get_ai_assistant()

# Analyze code
result = ai.analyze("def test(): pass")

# Fix code
result = ai.fix(code)

# Optimize
result = ai.optimize(code)

# Document
result = ai.document(code)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `analyze(code)` | AIResponse | Analyze complexity/quality |
| `fix(code)` | AIResponse | Auto-fix issues |
| `explain(code)` | AIResponse | Explain code |
| `optimize(code)` | AIResponse | Optimize |
| `document(code)` | AIResponse | Generate docs |

#### AIResponse

```python
@dataclass
class AIResponse:
    mode: AIMode
    content: Any
    confidence: float
```

---

### universe_debug2

Intelligent debugger.

```python
from universe_debug2 import (
    BreakpointManager,
    ExceptionIntelligence,
    ErrorPredictor,
    get_intelligent_debugger,
)
```

#### BreakpointManager

```python
bp = BreakpointManager()

# Add breakpoint
bp.add("file.py", 10, condition="x > 5")

# Get suggestions
sugs = bp.suggest_breakpoints(code)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `add(file, line, condition)` | str | Add breakpoint |
| `remove(bp_id)` | None | Remove |
| `suggest_breakpoints(code)` | list | AI suggestions |

#### ExceptionIntelligence

```python
# Analyze exception
analysis = ExceptionIntelligence.analyze(error)

# Get suggestions
fixes = ExceptionIntelligence.suggests_fix(error)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `analyze(exception)` | dict | Full analysis |
| `suggests_fix(exception)` | list | Fix suggestions |

#### ErrorPredictor

```python
# Predict potential errors
predictions = ErrorPredictor.predict(code)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `predict(code)` | list | Predicted errors |

---

## IDE Components

### universe_editor

Code editor with syntax highlighting.

```python
from universe_editor import get_editor, SyntaxTheme
```

#### CodeEditor

```python
editor = get_editor()

# Set code
editor.set_code("def hello(): print('hi')")

# Get tokens
tokens = editor.get_tokens()

# Get highlighted HTML
html = editor.get_html()
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `set_code(code)` | None | Set code |
| `get_code()` | str | Get code |
| `get_tokens()` | list | Get syntax tokens |
| `get_html()` | str | Highlighted HTML |
| `undo()` | None | Undo |
| `redo()` | None | Redo |

---

### universe_terminal

Terminal emulator.

```python
from universe_terminal import get_terminal, TerminalType
```

#### TerminalEmulator

```python
term = get_terminal()

# Start
term.start()

# Run command
term.send_command("ls -la")

# Read output
output = term.read_output()
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `start(cwd)` | None | Start shell |
| `send_command(cmd)` | None | Run command |
| `read_output()` | str | Read output |
| `resize(rows, cols)` | None | Resize terminal |

---

### universe_unified

Unified IDE experience.

```python
from universe_unified import get_unified_ide
```

#### UnifiedIDE

```python
ide = get_unified_ide()

# New project
project = ide.new_project("myapp")

# Get AI help
help_text = ide.get_ai_assistance("How do I...")

# Code completion
completions = ide.code_completion("imp")
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `new_project(name)` | Project | Create project |
| `get_ai_assistance(prompt)` | str | AI help |
| `code_completion(prefix)` | list | Autocomplete |
| `run_terminal(cmd)` | str | Run command |

---

### universe_intelligent

Code analysis and metrics.

```python
from universe_intelligent import get_intelligence
```

#### CodeIntelligence

```python
ci = get_intelligence()

# Analyze
suggestions = ci.analyze(code)

# Predict imports
imports = ci.predict_imports(code)

# Code metrics
mi = ci.maintainability_index(code)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `analyze(code)` | list | Suggestions |
| `predict_imports(code)` | list | Required imports |
| `suggest_tests(code)` | list | Test suggestions |

#### CodeMetrics

```python
from universe_intelligent import CodeMetrics

# Cyclomatic complexity
complexity = CodeMetrics.cyclomatic_complexity(code)

# Maintainability index (0-100)
mi = CodeMetrics.maintainability_index(code)
```

---

## Deployment

### universe_deploy2

Docker and Kubernetes.

```python
from universe_deploy2 import get_docker, get_k8s, Orchestrator
```

#### DockerManager

```python
docker = get_docker()

# Build image
docker.build("myapp:latest", path=".")

# Run container
docker.run("myapp:latest", name="myapp", ports=["8080:8080"])

# List containers
containers = docker.ps()
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `build(tag, path)` | dict | Build image |
| `run(image, name, ports)` | dict | Run container |
| `ps(all)` | list | List containers |
| `stop(id)` | dict | Stop container |
| `rm(id)` | dict | Remove container |

#### K8sManager

```python
k8s = get_k8s()

# Apply manifest
k8s.apply(manifest_yaml)

# Get resource
k8s.get("pod", "name")

# Logs
logs = k8s.logs("pod")
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `apply(manifest)` | dict | Apply YAML |
| `delete(kind, name)` | dict | Delete |
| `get(kind, name)` | dict | Get |
| `logs(pod)` | str | Pod logs |

---

### universe_cloud

Multi-cloud deployment.

```python
from universe_cloud import CloudManager, get_cloud
```

#### CloudManager

```python
cloud = get_cloud()

# Deploy
cloud.deploy("aws", "myapp")

# Scale
cloud.scale("aws", "myapp", replicas=5)

# Status
cloud.status("aws", "myapp")
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `deploy(provider, app)` | dict | Deploy |
| `scale(provider, app, n)` | dict | Scale |
| `status(provider, app)` | dict | Status |

---

## Platform

### universe_windows

Windows integration.

```python
from universe_windows import WindowsManager, get_windows
```

### universe_mobile

Mobile wrapper.

```python
from universe_mobile import MobileWrapper
```

---

## Testing

### universe_testing2

Advanced testing utilities.

```python
from universe_testing2 import TestFixtures, Fuzzer, TestRunner
```

#### TestFixtures

```python
# Get fixtures
universe = TestFixtures.universe_100()
memory = TestFixtures.memory_store()
queue = TestFixtures.task_queue()
```

#### Fuzzer

```python
fuzzer = Fuzzer(my_function)
fuzzer.fuzz(iterations=100)
```

---

## Version

Current: **2.1**

```python
from universe_ide import __version__
print(__version__)  # 2.1
```

---

**🪐 Complete API Reference**