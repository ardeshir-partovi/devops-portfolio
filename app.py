from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import platform
from datetime import datetime, timezone

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status = 200
            body = {
                "status": "healthy",
                "service": "portfolio-demo",
                "architecture": platform.machine(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        elif self.path == "/":
            status = 200
            body = {
                "message": "DevOps demo service is running",
                "service": "portfolio-demo",
                "version": os.getenv("APP_VERSION", "1.0.0"),
                "architecture": platform.machine(),
                "health": "/health"
            }
        else:
            status = 404
            body = {"error": "not found"}

        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
