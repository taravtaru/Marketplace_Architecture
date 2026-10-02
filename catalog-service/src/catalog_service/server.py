"""A dependency-free HTTP health endpoint.

Business behavior is intentionally absent at this stage of the assignment.
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


class HealthHandler(BaseHTTPRequestHandler):
    """Serve the technical liveness endpoint and reject all other routes."""

    server_version = "catalog-service"

    def do_GET(self) -> None:  # noqa: N802 - method name is defined by stdlib
        if urlsplit(self.path).path == "/health":
            self._write_json(200, {"status": "ok", "service": "catalog-service"})
            return

        self._write_json(404, {"error": "not_found"})

    def _write_json(self, status: int, payload: dict[str, str]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def create_server(host: str = "0.0.0.0", port: int = 8080) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), HealthHandler)


def run() -> None:
    port = int(os.environ.get("PORT", "8080"))
    server = create_server(port=port)
    print(f"catalog-service listening on 0.0.0.0:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
