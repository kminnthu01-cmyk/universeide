"""
Universe IDE - Dashboard

Web-based real-time dashboard.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ============================================================================
# DASHBOARD COMPONENTS
# ============================================================================

@dataclass
class DashboardCard:
    """Dashboard card"""
    title: str
    content: str
    type: str = "info"  # info, success, warning, error
    value: Any = None


# ============================================================================
# DASHBOARD DATA
# ============================================================================

class DashboardData:
    """Dashboard data aggregator"""
    
    def __init__(self):
        self.cards: list[DashboardCard] = []
        self.metrics: dict = {}
        
    def add_card(self, card: DashboardCard):
        """Add card"""
        self.cards.append(card)
        
    def set_metric(self, name: str, value: Any):
        """Set metric"""
        self.metrics[name] = value
        
    def to_dict(self) -> dict:
        """Convert to dict"""
        return {
            "cards": [
                {
                    "title": c.title,
                    "content": c.content,
                    "type": c.type,
                    "value": c.value,
                }
                for c in self.cards
            ],
            "metrics": self.metrics,
            "timestamp": datetime.now().isoformat(),
        }


# ============================================================================
# DASHBOARD HTML
# ============================================================================

DASHBOARD_HTML = '''<!DOCTYPE html>
<html>
<head>
    <title>Universe IDE Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui; background: #0a0a1a; color: #e0e7ff; }
        .header { background: #1a1a2e; padding: 20px; border-bottom: 2px solid #6366f1; }
        .header h1 { color: #8b5cf6; font-size: 28px; }
        .header .version { color: #6366f1; font-size: 14px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; padding: 20px; }
        .card { background: #1a1a2e; border-radius: 12px; padding: 20px; border: 1px solid #2a2a4e; }
        .card.info { border-left: 4px solid #6366f1; }
        .card.success { border-left: 4px solid #22c55e; }
        .card.warning { border-left: 4px solid #f59e0b; }
        .card.error { border-left: 4px solid #ef4444; }
        .card h3 { color: #a5b4fc; font-size: 14px; margin-bottom: 10px; }
        .card .value { font-size: 32px; font-weight: bold; color: #fff; }
        .card .content { font-size: 14px; color: #94a3b8; margin-top: 10px; }
        .agents { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
        .agent { background: #2a2a4e; padding: 8px 16px; border-radius: 8px; font-size: 12px; }
        .agent.active { border: 1px solid #22c55e; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🪐 Universe IDE Dashboard</h1>
        <div class="version">v1.8.0 - Real-time</div>
    </div>
    <div class="grid" id="dashboard">
        <div class="card info">
            <h3>Total Agents</h3>
            <div class="value" id="agents">{agents}</div>
            <div class="content">Parallel AI agents running</div>
        </div>
        <div class="card success">
            <h3>Status</h3>
            <div class="value" id="status">{status}</div>
            <div class="content">System operational</div>
        </div>
        <div class="card info">
            <h3>Provider</h3>
            <div class="value" id="provider">{provider}</div>
            <div class="content">AI backend</div>
        </div>
        <div class="card info">
            <h3>Model</h3>
            <div class="value" id="model">{model}</div>
            <div class="content">Current model</div>
        </div>
    </div>
    <div style="padding: 20px;">
        <h3 style="color: #a5b4fc; margin-bottom: 10px;">Active Agents</h3>
        <div class="agents" id="agentList"></div>
    </div>
    <script>
        async function update() {
            try {
                const res = await fetch('/api/dashboard');
                const data = await res.json();
                
                document.getElementById('agents').textContent = data.agents;
                document.getElementById('status').textContent = data.status;
                document.getElementById('provider').textContent = data.provider;
                document.getElementById('model').textContent = data.model.substring(0, 20);
            } catch(e) { console.error(e); }
        }
        setInterval(update, 2000);
        update();
    </script>
</body>
</html>'''


# ============================================================================
# DASHBOARD SERVER
# ============================================================================

def create_dashboard_routes(app):
    """Create dashboard routes"""
    
    @app.get("/dashboard")
    async def dashboard():
        """Dashboard page"""
        return {"html": DASHBOARD_HTML}
        
    @app.get("/api/dashboard")
    async def dashboard_data():
        """Dashboard data"""
        from universe_ide import cosmos
        u = cosmos(10)
        
        return {
            "agents": u.num_agents,
            "status": "Running",
            "provider": u.provider,
            "model": u.model,
        }


# ============================================================================
# REAL-TIME UPDATES
# ============================================================================

async def stream_dashboard():
    """Stream dashboard updates"""
    while True:
        from universe_ide import cosmos
        u = cosmos(10)
        
        yield {
            "agents": u.num_agents,
            "status": "running",
            "timestamp": datetime.now().isoformat(),
        }
        
        await asyncio.sleep(2)


# Global
_dashboard = None

def get_dashboard():
    """Get dashboard data"""
    global _dashboard
    if _dashboard is None:
        _dashboard = DashboardData()
    return _dashboard


__all__ = [
    "DashboardCard",
    "DashboardData",
    "DASHBOARD_HTML",
    "create_dashboard_routes",
    "stream_dashboard",
    "get_dashboard",
]