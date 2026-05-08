"""
Universe IDE - Windows Desktop App

Windows desktop GUI for Universe IDE.
"""

import sys

# Check if tkinter available
TKINTER_AVAILABLE = False
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    pass


def main():
    if not TKINTER_AVAILABLE:
        print("=" * 40)
        print("Universe IDE Desktop v2.8")
        print("=" * 40)
        print("")
        print("Desktop GUI requires tkinter")
        print("Install on Windows: pip install tk")
        print("Or use the CLI: python universe_ide.py")
        print("")
        return
    
    root = tk.Tk()
    root.title("Universe IDE")
    root.geometry("1000x700")
    
    # Menu
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=lambda: None)
    file_menu.add_command(label="Open", command=lambda: None)
    file_menu.add_command(label="Save", command=lambda: None)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Toolbar
    toolbar = ttk.Frame(root)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    ttk.Button(toolbar, text="New").pack(side=tk.LEFT, padx=2)
    ttk.Button(toolbar, text="Open").pack(side=tk.LEFT, padx=2)
    ttk.Button(toolbar, text="Save").pack(side=tk.LEFT, padx=2)
    
    # Main area
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Editor
    editor = scrolledtext.ScrolledText(main_frame, font=("Consolas", 11))
    editor.pack(fill=tk.BOTH, expand=True)
    
    # Status
    status = ttk.Label(root, text="Ready - Universe IDE v2.8")
    status.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()


if __name__ == "__main__":
    main()
