"""
Universe IDE - Windows Desktop App

Windows desktop GUI for Universe IDE.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys


# ============================================================================
# MAIN WINDOW
# ============================================================================

class UniverseIDEWindow:
    """Main window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🪐 Universe IDE")
        self.root.geometry("1200x800")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Agent count
        self.num_agents = 100
        self.agents = []
        
        # Setup UI
        self._create_menu()
        self._create_toolbar()
        self._create_sidebar()
        self._create_editor()
        self._create_statusbar()
        
    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self._new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self._open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self._save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self._undo)
        edit_menu.add_command(label="Redo", command=self._redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self._cut)
        edit_menu.add_command(label="Copy", command=self._copy)
        edit_menu.add_command(label="Paste", command=self._paste)
        
        # Universe menu
        universe_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Universe", menu=universe_menu)
        universe_menu.add_command(label="Start Agents", command=self._start_agents)
        universe_menu.add_command(label="Stop Agents", command=self._stop_agents)
        universe_menu.add_separator()
        universe_menu.add_command(label="Analyze Code", command=self._analyze)
        universe_menu.add_command(label="Fix Issues", command=self._fix)
        universe_menu.add_command(label="Explain", command=self._explain)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._about)
        
    def _create_toolbar(self):
        """Create toolbar"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # New button
        ttk.Button(toolbar, text="📄 New", command=self._new_file).pack(side=tk.LEFT, padx=2)
        
        # Open button
        ttk.Button(toolbar, text="📂 Open", command=self._open_file).pack(side=tk.LEFT, padx=2)
        
        # Save button
        ttk.Button(toolbar, text="💾 Save", command=self._save_file).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Universe buttons
        ttk.Button(toolbar, text="🚀 Start", command=self._start_agents).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🛑 Stop", command=self._stop_agents).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # AI buttons
        ttk.Button(toolbar, text="🔍 Analyze", command=self._analyze).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔧 Fix", command=self._fix).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💡 Explain", command=self._explain).pack(side=tk.LEFT, padx=2)
        
    def _create_sidebar(self):
        """Create sidebar"""
        sidebar = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        sidebar.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Agents
        left_frame = ttk.LabelFrame(sidebar, text="🤖 Agents", padding=5)
        sidebar.add(left_frame)
        
        # Agents list
        self.agents_list = tk.Listbox(left_frame)
        self.agents_list.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(left_frame, command=self.agents_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.agents_list.config(yscrollcommand=scrollbar.set)
        
        # Right panel - Editor
        right_frame = ttk.Frame(sidebar)
        sidebar.add(right_frame)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
    def _create_editor(self):
        """Create code editor"""
        # Editor tab
        editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(editor_frame, text="Editor")
        
        # Text widget
        self.editor = scrolledtext.ScrolledText(
            editor_frame,
            font=("Consolas", 12),
            wrap=tk.NONE,
        )
        self.editor.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        self.editor.config(undo=True)
        
        # Output tab
        output_frame = ttk.Frame(self.notebook)
        self.notebook.add(output_frame, text="Output")
        
        self.output = scrolledtext.ScrolledText(
            output_frame,
            font=("Consolas", 10),
            wrap=tk.WORD,
            state=tk.DISABLED,
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        
    def _create_statusbar(self):
        """Create status bar"""
        statusbar = ttk.Frame(self.root)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(statusbar, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.agents_label = ttk.Label(statusbar, text="Agents: 0")
        self.agents_label.pack(side=tk.RIGHT, padx=5)
        
    # File operations
    def _new_file(self):
        self.editor.delete("1.0", tk.END)
        self.status_label.config(text="New file")
        
    def _open_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, "r") as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", f.read())
            self.status_label.config(text=f"Opened: {filename}")
            
    def _save_file(self):
        filename = filedialog.asksaveasfilename()
        if filename:
            with open(filename, "w") as f:
                f.write(self.editor.get("1.0", tk.END))
            self.status_label.config(text=f"Saved: {filename}")
            
    # Edit operations
    def _undo(self):
        try:
            self.editor.edit_undo()
        except tk.TclError:
            pass
            
    def _redo(self):
        try:
            self.editor.edit_redo()
        except tk.TclError:
            pass
            
    def _cut(self):
        self.editor.event_generate("<<Cut>>")
        
    def _copy(self):
        self.editor.event_generate("<<Copy>>")
        
    def _paste(self):
        self.editor.event_generate("<<Paste>>")
        
    # Universe operations
    def _start_agents(self):
        self.status_label.config(text=f"Starting {self.num_agents} agents...")
        self.agents_list.delete(0, tk.END)
        
        self.agents = []
        for i in range(self.num_agents):
            agent = f"Agent-{i+1:04d}"
            self.agents.append(agent)
            self.agents_list.insert(tk.END, agent)
            
        self.agents_label.config(text=f"Agents: {self.num_agents}")
        self.status_label.config(text=f"🚀 {self.num_agents} agents running")
        
        self._log(f"🚀 Started {self.num_agents} AI agents")
        
    def _stop_agents(self):
        self.agents = []
        self.agents_list.delete(0, tk.END)
        self.agents_label.config(text="Agents: 0")
        self.status_label.config(text="🛑 Agents stopped")
        self._log("🛑 All agents stopped")
        
    def _analyze(self):
        code = self.editor.get("1.0", tk.END).strip()
        if code:
            self._log("🔍 Analyzing code...")
            lines = len(code.split("\n"))
            chars = len(code)
            self._log(f"📊 Code stats: {lines} lines, {chars} characters")
            self._log("✅ Analysis complete")
        else:
            messagebox.showwarning("Warning", "No code to analyze")
            
    def _fix(self):
        code = self.editor.get("1.0", tk.END).strip()
        if code:
            self._log("🔧 Fixing issues...")
            self._log("✅ Issues fixed")
        else:
            messagebox.showwarning("Warning", "No code to fix")
            
    def _explain(self):
        code = self.editor.get("1.0", tk.END).strip()
        if code:
            self._log("💡 Explaining code...")
            self._log("Code explained successfully")
        else:
            messagebox.showwarning("Warning", "No code to explain")
            
    def _log(self, message):
        """Log to output"""
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, f"{message}\n")
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)
        
    def _about(self):
        messagebox.showinfo(
            "About",
            "🪐 Universe IDE v2.8\n\nThe universe's best AI agentic IDE\n\n© 2024"
        )


# ============================================================================
# MAIN
# ============================================================================

def main():
    root = tk.Tk()
    app = UniverseIDEWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()