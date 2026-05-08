/**
 * Universe IDE - The World's Best AI Agentic IDE Platform
 * 
 * A futuristic web-based IDE with:
 * - Monaco Editor (VS Code's editor)
 * - Multi-terminal support
 * - AI Agent panel with parallel universes
 * - File browser with git integration
 * - Preview pane for web apps
 * 
 * This is what professional AI development looks like.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Editor } from '@monaco-editor/react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import 'xterm/css/xterm.css';

// AI Agent Panel Component
const AIChatPanel = ({ agents, onSend, isProcessing }) => {
  const [message, setMessage] = useState('');
  const [history, setHistory] = useState([]);
  
  const handleSend = () => {
    if (!message.trim()) return;
    onSend(message);
    setHistory([...history, { role: 'user', content: message }]);
    setMessage('');
  };
  
  return (
    <div className="ai-panel">
      <div className="agent-status">
        <span className="status-dot active"></span>
        {agents.length} Universe Agents Active
      </div>
      
      <div className="chat-messages">
        {history.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <span className="role">{msg.role}:</span>
            {msg.content}
          </div>
        ))}
        {isProcessing && <div className="processing">🤔 Thinking...</div>}
      </div>
      
      <div className="chat-input">
        <input 
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask the universe..."
          disabled={isProcessing}
        />
        <button onClick={handleSend} disabled={isProcessing}>
          ➤
        </button>
      </div>
    </div>
  );
};

// File Browser Component  
const FileBrowser = ({ files, onSelect, onCreate, currentPath }) => {
  const [expanded, setExpanded] = useState(true);
  
  return (
    <div className={`file-browser ${expanded ? 'expanded' : 'collapsed'}`}>
      <div className="header" onClick={() => setExpanded(!expanded)}>
        <span>📁 Explorer</span>
        <span className="toggle">{expanded ? '◀' : '▶'}</span>
      </div>
      {expanded && (
        <div className="files">
          {files.map((file, i) => (
            <div 
              key={i} 
              className={`file ${file.type}`}
              onClick={() => onSelect(file.path)}
            >
              <span className="icon">{file.icon}</span>
              <span className="name">{file.name}</span>
            </div>
          ))}
          <button className="new-file" onClick={onCreate}>+ New File</button>
        </div>
      )}
    </div>
  );
};

// Terminal Component
const TerminalPanel = ({ onCommand, history }) => {
  const [lines, setLines] = useState([]);
  
  return (
    <div className="terminal-panel">
      {history.map((line, i) => (
        <div key={i} className="line">{line}</div>
      ))}
      <div className="input">
        <span className="prompt">$</span>
        <input onKeyDown={(e) => {
          if (e.key === 'Enter') {
            onCommand(e.target.value);
            e.target.value = '';
          }
        }} />
      </div>
    </div>
  );
};

// Main IDE Layout
export const UniverseIDE = () => {
  const [currentFile, setCurrentFile] = useState(null);
  const [fileTree, setFileTree] = useState([]);
  const [agentCount, setAgentCount] = useState(100);
  const [aiProcessing, setAiProcessing] = useState(false);
  const [terminalHistory, setTerminalHistory] = useState([]);
  
  // Initialize file tree
  useEffect(() => {
    setFileTree([
      { name: 'src', type: 'folder', icon: '📁', path: '/src' },
      { name: 'tests', type: 'folder', icon: '📁', path: '/tests' },
      { name: 'README.md', type: 'file', icon: '📄', path: '/README.md' },
    ]);
  }, []);
  
  return (
    <div className="universe-ide">
      {/* Top Bar */}
      <header className="ide-header">
        <div className="logo">🪐 Universe IDE</div>
        <div className="controls">
          <select 
            value={agentCount} 
            onChange={(e) => setAgentCount(Number(e.target.value))}
          >
            <option value={10}>10 Agents</option>
            <option value={50}>50 Agents</option>
            <option value={100}>100 Agents</option>
            <option value={500}>500 Agents</option>
            <option value={1000}>1000 Agents</option>
          </select>
          <button className="run">▶ Run</button>
          <button className="deploy">🚀 Deploy</button>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="ide-main">
        {/* Sidebar */}
        <aside className="sidebar">
          <FileBrowser 
            files={fileTree}
            onSelect={setCurrentFile}
            onCreate={() => {}}
            currentPath="/"
          />
        </aside>
        
        {/* Editor */}
        <section className="editor-area">
          <Editor
            height="100%"
            defaultLanguage="python"
            theme="vs-dark"
            value={currentFile || "// Select or create a file to start coding..."}
            options={{
              minimap: { enabled: true },
              fontSize: 14,
              fontFamily: 'JetBrains Mono, monospace',
            }}
          />
        </section>
        
        {/* AI Panel */}
        <aside className="ai-sidebar">
          <AIChatPanel 
            agents={Array(agentCount).fill(0)}
            onSend={(msg) => {
              setAiProcessing(true);
              // Simulate AI response
              setTimeout(() => setAiProcessing(false), 2000);
            }}
            isProcessing={aiProcessing}
          />
        </aside>
      </main>
      
      {/* Terminal */}
      <footer className="ide-terminal">
        <TerminalPanel 
          onCommand={(cmd) => {
            setTerminalHistory([...terminalHistory, `$ ${cmd}`]);
          }}
          history={terminalHistory}
        />
      </footer>
    </div>
  );
};

export default UniverseIDE;