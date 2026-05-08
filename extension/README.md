# Universe IDE VSCode Extension

The universe's best AI agentic IDE - now in VSCode!

## Features

- 🚀 **1000 Parallel AI Agents** - Create universes of AI agents
- 🤖 **AI Code Analysis** - Analyze, fix, and explain code
- 💡 **Smart Autocomplete** - AI-powered suggestions
- ⚡ **Inline Suggestions** - Real-time code completion
- 📖 **Hover Explanations** - Hover for code info
- ⌨️ **Keyboard Shortcuts** - Quick access commands

## Commands

| Command | Shortcut | Description |
|---------|----------|------------|
| `Universe IDE: Start` | `Ctrl+Shift+U` | Start Universe IDE |
| `Universe IDE: Analyze` | `Ctrl+Shift+A` | Analyze code |
| `Universe IDE: Explain` | `Ctrl+Shift+E` | Explain code |

## Configuration

```json
{
  "universe.ide.provider": "anthropic",
  "universe.ide.model": "claude-sonnet-4-20250505",
  "universe.ide.maxAgents": 100,
  "universe.ide.autocomplete": true,
  "universe.ide.inlineSuggest": true
}
```

## Snippets

| Prefix | Description |
|--------|-------------|
| `cosmos` | Create universe |
| `uai` | AI assistant |
| `uanalyze` | Analyze code |

## Installation

1. Open VSCode
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search "Universe IDE"
4. Click Install

Or install from `.vsix`:

```bash
code --install-extension universe-ide-2.8.0.vsix
```

## Development

```bash
# Install dependencies
npm install

# Package
npx vsce package

# Publish
npx vsce publish
```

## License

MIT

**The universe's best AI agentic IDE** 🪐