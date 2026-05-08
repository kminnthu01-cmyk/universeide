"""
Universe IDE - API Server

HTTP server with API endpoints for the UI.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys


# ============================================================================
# TRY IMPORTS
# ============================================================================

try:
    from universe_ide import cosmos
except ImportError:
    cosmos = lambda n: type('U', (), {'num_agents': n})()

try:
    from universe_swarm import get_swarm
except ImportError:
    def get_swarm():
        return type('S', (), {'get_status': lambda: {'agents': 100}})()


# ============================================================================
# HANDLER
# ============================================================================

class UniverseHandler(BaseHTTPRequestHandler):
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        if isinstance(html, str):
            html = html.encode()
        self.wfile.write(html)
    
    def do_GET(self):
        path = self.path
        
        if path == "/" or path == "/index.html":
            try:
                with open("index.html", "rb") as f:
                    self.send_html(f.read())
            except FileNotFoundError:
                self.send_html("<h1>404 Not Found</h1>", 404)
            return
        
        # API endpoints
        if path == "/api/health":
            self.send_json({"status": "healthy", "service": "universe-ide", "version": "v5.3"})
            return
        
        if path == "/api/status":
            self.send_json({
                "version": "v5.3",
                "status": "running"
            })
            return
        
        if path == "/api/cosmos":
            u = cosmos(1000)
            self.send_json({"agents": u.num_agents, "max": 10000})
            return
        
        if path == "/api/swarm":
            try:
                s = get_swarm()
                self.send_json(s.get_status())
            except Exception as e:
                self.send_json({"agents": 100, "error": str(e)})
            return
        
        # AI Query endpoint
        if path == "/api/ai/query":
            try:
                from universe_ai_assist import aiassist
                # Simple response
                self.send_json({"response": "AI query processed", "status": "ok"})
            except Exception as e:
                self.send_json({"error": str(e)})
            return
        
        # Try static files for other paths
        try:
            filepath = path.lstrip("/")
            with open(filepath, "rb") as f:
                ext = filepath.rsplit(".", 1)[-1] if "." in filepath else ""
                content_types = {"html": "text/html", "css": "text/css", "js": "application/javascript", "json": "application/json"}
                self.send_response(200)
                self.send_header("Content-Type", content_types.get(ext, "text/plain"))
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_json({"error": "Not found"}, 404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        
    def log_message(self, format, *args):
        print(f"[SERVER] {args[0]}")


# ============================================================================
# MAIN
# ============================================================================

def run_server(port=8080):
    server = HTTPServer(("0.0.0.0", port), UniverseHandler)
    print(f"Universe IDE running on http://0.0.0.0:{port}")
    print(f"   API: http://0.0.0.0:{port}/api/*")
    sys.stdout.flush()
    server.serve_forever()


if __name__ == "__main__":
    run_server()
