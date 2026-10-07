#!/usr/bin/env python3
"""Servidor local: serve a página e roda yt-dlp -x --audio-format mp3 <link>."""
import json
import subprocess
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HOST, PORT = "127.0.0.1", 8765
ROOT = Path(__file__).parent
OUT_DIR = Path.home() / "Music" / "yt-mp3"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = (ROOT / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/convert":
            return self.send_error(404)
        length = int(self.headers.get("Content-Length", 0))
        url = json.loads(self.rfile.read(length) or b"{}").get("url", "").strip()
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc or url.startswith("-"):
            return self.send_error(400, "Link inválido")

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--newline",
               "-P", str(OUT_DIR), "--", url]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                self.wfile.write(line.encode())
                self.wfile.flush()
            code = proc.wait()
            self.wfile.write(f"\n__EXIT__{code}".encode())
        except (BrokenPipeError, ConnectionResetError):
            proc.kill()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"Rodando em http://{HOST}:{PORT}  (arquivos em {OUT_DIR})")
    try:
        server = ThreadingHTTPServer((HOST, PORT), Handler)
        webbrowser.open(f"http://{HOST}:{PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
