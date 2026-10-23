"""Serve an in-memory snapshot of explicitly approved course files (POSIX/Python 3)."""
import argparse
import mimetypes
import os
from pathlib import Path
import stat
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "scripts/web-files.txt"


def safe_parts(path):
    parts = path.split("/")
    if any(not part or part.startswith(".") or "\\" in part for part in parts):
        raise ValueError("Only explicit, non-hidden relative paths are allowed")
    return parts


def read_regular_file(root, relative):
    """Walk directory descriptors without following any symlink, including ancestors."""
    parts = safe_parts(relative)
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                     dir_fd=descriptor)
        with os.fdopen(fd, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise ValueError("Course assets must be regular files")
            return stream.read()
    finally:
        os.close(descriptor)


def load_pages(root, entries, url_root=""):
    """No live checkout reads occur after this snapshot is created."""
    pages = {}
    prefix = url_root + "/" if url_root else ""
    for entry in entries:
        relative = entry.strip()
        if not relative or relative.startswith("#"):
            continue
        safe_parts(relative)
        if Path(relative).suffix not in {".html", ".css", ".js", ".md"}:
            raise ValueError("Only course HTML, CSS, JavaScript and reviewed Markdown may be published")
        if not relative.startswith(prefix):
            continue
        content = read_regular_file(root, relative)
        route = "/" + relative[len(prefix):]
        if route in pages:
            raise ValueError("Duplicate course file: " + relative)
        mime = mimetypes.guess_type(relative)[0] or "application/octet-stream"
        pages[route] = (content, mime + "; charset=utf-8")
    return pages


def make_handler(pages):
    class CourseHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.serve_page(send_body=True)

        def do_HEAD(self):
            self.serve_page(send_body=False)

        def serve_page(self, send_body):
            try:
                parsed = urlsplit(self.path)
                path = unquote(parsed.path, errors="strict")
                # Reject traversal rather than normalizing it into an approved URL.
                if parsed.scheme or parsed.netloc or not path.startswith("/"):
                    raise ValueError("Invalid request target")
                safe_parts(path[1:-1] if path.endswith("/") else path[1:])
            except (ValueError, UnicodeError):
                self.send_error(404)
                return
            if path.endswith("/"):
                path += "index.html"
            if path not in pages and path + "/index.html" in pages:
                self.send_response(301)
                self.send_header("Location", path + "/" +
                                 ("?" + parsed.query if parsed.query else ""))
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            page = pages.get(path)
            if page is None:
                self.send_error(404)
                return
            content, mime = page
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if send_body:
                self.wfile.write(content)
    return CourseHandler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--url-root", choices=("", "machine-learning"), default="")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    try:
        pages = load_pages(ROOT, MANIFEST.read_text().splitlines(), args.url_root)
        with ThreadingHTTPServer((args.host, args.port), make_handler(pages)) as server:
            print(f"Serving {len(pages)} approved course files on {args.host}:{args.port}; "
                  "restart to load edits.", flush=True)
            server.serve_forever()
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot serve approved course files: {error}\n")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
