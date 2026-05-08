#!/usr/bin/env python3
"""
🪐 Universe IDE - Enhanced CLI

The ultimate CLI experience for the Universe AI Platform.

Features:
- Rich colorful output with gradients
- Interactive prompts  
- Progress visualization
- Agent swarm visualization
- Auto-completion
- Real-time metrics display
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from typing import Optional

# Rich for colorful output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.table import Table
    from rich.live import Live
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None


# ANSI Colors (fallback)
class Colors:
    """ANSI color codes"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class UniverseCLI:
    """
    Enhanced CLI for Universe AI Platform
    
    The professional developer's experience.
    """
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.running = True
        self.metrics = {
            "tasks_completed": 0,
            "active_agents": 0,
            "total_agents": 0,
        }
        
    def print_banner(self):
        """Print the universe banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════════════╗
║                                                           ║
║        🪐 U N I V E R S E   I D E                    ║
║                                                           ║
║        The Ultimate AI Agentic Development Platform       ║
║        • Quantum Parallelism • Entangled State •           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════════════════╝
"""
        if self.console:
            self.console.print(banner, style="cyan")
        else:
            print(banner)
            
    def print_status(self, universe):
        """Print universe status with rich table"""
        status_text = f"""
╔══════════════════════════╗
║ 🪐 Universe Status      ║
╠══════════════════════════╣
║ Agents:    {universe.num_agents:>6}   ║
║ Provider: {universe.provider:>6}    ║
║ Model:    {universe.model[:10]:>6}    ║
║ Status:   Running        ║
╚══════════════════════════╝
"""
        if self.console:
            self.console.print(status_text, style="green")
        else:
            print(status_text)
            
    def visualize_agents(self, count: int = 10):
        """Visualize the agent swarm"""
        dots = "● " * min(count, 20)
        print(f"Agent Swarm: {dots}")
            
    def print_progress_bar(self, label: str, current: int, total: int):
        """Print progress bar"""
        percent = int(current / total * 20)
        bar = "█" * percent + "░" * (20 - percent)
        print(f"{label}: [{bar}] {percent*5}%")
            
    def run_interactive(self):
        """Run interactive mode"""
        self.print_banner()
        
        print("\n[?] How many agents? (default: 100)")
        try:
            user_input = input("> ").strip()
            agent_count = int(user_input) if user_input else 100
        except ValueError:
            agent_count = 100
            
        print(f"\n[+] Creating {agent_count} parallel universes...")
        
        # Create universe
        from universe_ide import cosmos
        universe = cosmos(agent_count)
        
        # Show status
        self.print_status(universe)
        
        # Visualize
        self.visualize_agents(agent_count)
        
        print("\n[✓] Universe ready!")
        print("[i] Use universe.deploy('task') to deploy work")
        print("[i] Use universe.get_status() for metrics")
        
        return universe
        
    def run_demo(self, duration: int = 10):
        """Run a demo showing agents in action"""
        from universe_ide import cosmos
        
        print("\n🪐 Running Universe Demo...\n")
        
        # Create universe 
        universe = cosmos(10)
        
        self.print_banner()
        self.print_status(universe)
        
        # Simulate activity
        print("\n[→] Deploying tasks to agent swarm...\n")
        
        # Progress simulation
        for i in range(5):
            self.print_progress_bar("Processing", i, 5)
            time.sleep(0.3)
            
        self.visualize_agents(10)
        
        print("\n[✓] Demo complete!")
        print(f"[i] Created universe with {universe.num_agents} agents")
        
    def print_help(self):
        """Print help message"""
        help_text = """
🪐 Universe IDE Commands

Usage:
    cosmos(n)              Create n parallel agents
    universe.deploy(task)    Deploy task to swarm
    universe.get_status()  Get metrics
    universe.tools.*       Use tools

Examples:
    # Quick start
    from universe_ide import cosmos
    u = cosmos(100)
    
    # Deploy work
    result = await u.deploy("Build API", "src/")
    
    # Use tools
    await u.tools.search.grep("pattern")

Commands:
    help     - Show this help
    status   - Show universe status
    demo     - Run demo
    quit/exit - Exit
"""
        print(help_text)


def main():
    """Main CLI entry point"""
    cli = UniverseCLI()
    
    if len(sys.argv) > 1:
        # Process commands
        cmd = sys.argv[1]
        
        if cmd == "demo":
            cli.run_demo()
        elif cmd == "status":
            from universe_ide import cosmos
            universe = cosmos(10)
            cli.print_status(universe)
        elif cmd == "help":
            cli.print_help()
        else:
            print(f"[?] Unknown command: {cmd}")
            print("[i] Run 'python universe_cli.py help' for help")
    else:
        # Interactive mode
        try:
            cli.run_interactive()
        except KeyboardInterrupt:
            print("\n\n🪐 Goodbye, space traveler!")
        except EOFError:
            print("\n\n🪐 Goodbye!")


if __name__ == "__main__":
    main()
