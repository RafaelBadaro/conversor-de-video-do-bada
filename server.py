#!/usr/bin/env python3
"""Servidor local: serve a página e roda yt-dlp -x --audio-format mp3 <link>."""
import json
import os
import signal
import subprocess
import threading
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import urlopen

HOST, PORT = "127.0.0.1", 8765
ROOT = Path(__file__).parent
OUT_DIR = Path.home() / "Music" / "yt-mp3"

# Processos do yt-dlp em andamento, para o botão Cancelar.
running = set()
running_lock = threading.Lock()


def kill(proc):
    """Mata o yt-dlp e os filhos dele (ffmpeg) de uma vez."""
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = (ROOT / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path.startswith("/info?"):
            self.send_info()
        else:
            self.send_error(404)

    def send_info(self):
        """Título, canal e capa do vídeo, pelo oEmbed do YouTube."""
        url = parse_qs(urlparse(self.path).query).get("url", [""])[0]
        try:
            with urlopen("https://www.youtube.com/oembed?format=json&url=" + quote(url, safe=""),
                         timeout=5) as res:
                data = json.load(res)
            body = json.dumps({k: data.get(k) for k in ("title", "author_name", "thumbnail_url")}).encode()
        except Exception:
            return self.send_error(404)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path == "/cancel":
            with running_lock:
                procs = list(running)
            for proc in procs:
                kill(proc)
            self.send_response(204)
            self.end_headers()
            return
        if self.path != "/convert":
            return self.send_error(404)
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length) or b"{}")
        url = data.get("url", "").strip()
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc or url.startswith("-"):
            return self.send_error(400, "Link inválido")

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        playlist = "--yes-playlist" if data.get("playlist", True) else "--no-playlist"
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--newline", playlist,
               "-P", str(OUT_DIR), "--", url]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, start_new_session=True)
        with running_lock:
            running.add(proc)
        try:
            for line in proc.stdout:
                self.wfile.write(line.encode())
                self.wfile.flush()
            code = proc.wait()
            self.wfile.write(f"\n__EXIT__{code}".encode())
        except (BrokenPipeError, ConnectionResetError):
            kill(proc)
        finally:
            with running_lock:
                running.discard(proc)

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
