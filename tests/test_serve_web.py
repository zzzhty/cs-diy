"""Local, temporary-fixture checks; never start a listener on an external interface."""
import http.client
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import shutil
import os
import socket
import subprocess
import time
import tempfile
import threading
import unittest
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("serve_web", ROOT / "scripts/serve_web.py")
web = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"}:
                self.links.append(value)


class CourseServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        self.entries = (self.root / 'scripts/web-files.txt').read_text().splitlines()

    def serve(self, url_root=''):
        pages = web.load_pages(self.root, self.entries, url_root)
        handler = web.make_handler(pages)
        handler.log_message = lambda *args: None
        server = web.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        def cleanup():
            server.shutdown()
            server.server_close()
            thread.join()
        self.addCleanup(cleanup)
        self.port = server.server_port
        return pages

    def request(self, path, method='GET'):
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=5)
        try:
            conn.request(method, path)
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def check_pages_and_links(self, prefix=''):
        pages = self.serve(prefix)
        for route, (body, mime) in pages.items():
            with self.subTest(route=route):
                status, headers, received = self.request(route)
                self.assertEqual(status, 200)
                self.assertEqual(body, received)
                self.assertEqual(headers['Content-Type'], mime)
                if route.endswith('.html'):
                    parser = Links()
                    parser.feed(body.decode())
                    for link in parser.links:
                        if not urlsplit(link).scheme:
                            self.assertFalse(link.startswith('/'), link)
                            target = urlsplit(urljoin(route, link)).path
                            self.assertEqual(self.request(target)[0], 200, (route, link))

    def test_all_root_pages_assets_and_relative_links(self):
        self.check_pages_and_links()

    def test_all_legacy_pages_assets_and_relative_links(self):
        self.check_pages_and_links('machine-learning')

    def test_home_documents_reachable_urls_for_both_launch_directories(self):
        track = 'deep-learning/language-modeling-from-scratch/'
        home = (self.root / 'machine-learning' / track / 'index.html').read_text()
        root_url = 'http://&lt;server-ip&gt;:8000/machine-learning/' + track
        legacy_url = 'http://&lt;server-ip&gt;:8000/' + track
        self.assertIn(root_url, home)
        self.assertIn(legacy_url, home)
        self.assertLess(home.index(root_url), home.index('cd machine-learning'))
        self.assertLess(home.index('cd machine-learning'), home.index(legacy_url))
        self.serve()
        self.assertEqual(self.request('/machine-learning/' + track)[0], 200)
        self.serve('machine-learning')
        self.assertEqual(self.request('/' + track)[0], 200)

    def test_private_files_outputs_and_directory_lists_denied(self):
        for path in ('.env', '.git/config', 'outputs/report.html', 'assets/private.js',
                     'machine-learning/deep-learning/language-modeling-from-scratch/lessons/private.html'):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('PRIVATE_MARKER')
        self.serve()
        for path in ('/.env', '/.git/config', '/outputs/report.html', '/assets/private.js', '/',
                     '/assets/', '/scripts/web-files.txt', '/README.md',
                     '/machine-learning/deep-learning/language-modeling-from-scratch/NOTES.md',
                     '/machine-learning/deep-learning/language-modeling-from-scratch/lessons/private.html'):
            for method in ('GET', 'HEAD'):
                with self.subTest(path=path, method=method):
                    status, _, body = self.request(path, method)
                    self.assertEqual(status, 404)
                    self.assertNotIn(b'PRIVATE_MARKER', body)

    def test_encoded_traversal_and_ambiguous_paths_denied(self):
        self.serve()
        for path in ('/../assets/course.css', '/%2e%2e/assets/course.css',
                     '/assets/%2e%2e/assets/course.css', '/%252e%252e/.env',
                     '/assets\\course.css', '/assets%5ccourse.css', '/assets//course.css',
                     '/assets/%00course.css', '/%ff', '/.git%2fconfig'):
            with self.subTest(path=path):
                self.assertEqual(self.request(path)[0], 404)

    def test_head_query_and_index_redirect(self):
        self.serve()
        status, headers, body = self.request('/assets/course.css?v=1', 'HEAD')
        self.assertEqual(status, 200)
        self.assertEqual(body, b'')
        self.assertGreater(int(headers['Content-Length']), 0)
        route = '/machine-learning/deep-learning/language-modeling-from-scratch'
        status, headers, _ = self.request(route + '?v=1')
        self.assertEqual(status, 301)
        self.assertEqual(headers['Location'], route + '/?v=1')
        self.assertEqual(self.request(headers['Location'])[0], 200)

    def test_file_symlink_fails_closed(self):
        target = self.root / 'assets/course.css'
        target.unlink()
        secret = Path(self.temp.name) / 'secret.css'
        secret.write_text('SECRET')
        target.symlink_to(secret)
        with self.assertRaises(OSError):
            web.load_pages(self.root, self.entries)

    def test_directory_symlink_fails_closed(self):
        target = self.root / 'assets'
        target.rename(self.root / 'original-assets')
        target.symlink_to(self.root / 'original-assets', target_is_directory=True)
        with self.assertRaises(OSError):
            web.load_pages(self.root, self.entries)

    def test_post_start_replacement_cannot_change_snapshot(self):
        self.serve()
        before = self.request('/assets/course.css')[2]
        target = self.root / 'assets/course.css'
        target.unlink()
        target.symlink_to(self.root / 'AGENTS.md')
        self.assertEqual(self.request('/assets/course.css')[2], before)

    def test_bad_manifest_entries_fail_closed(self):
        for entry in ('../secret.html', '.env', 'assets/../README.md', '/assets/course.css',
                      'assets//course.css', 'assets/*.css', 'outputs/private.bin'):
            with self.subTest(entry=entry), self.assertRaises((ValueError, OSError)):
                web.load_pages(self.root, [entry])

    def test_shell_entrypoints_and_argument_validation(self):
        for script, route in (
            ('scripts/serve-web.sh', '/machine-learning/deep-learning/language-modeling-from-scratch/'),
            ('machine-learning/scripts/serve-web.sh', '/deep-learning/language-modeling-from-scratch/')
        ):
            env = dict(os.environ, WEB_HOST='127.0.0.1')
            for args in (['--port', '0'], ['--port', '65536'], ['--port', 'bad'], ['--unknown']):
                result = subprocess.run(['sh', str(self.root / script)] + args,
                                        env=env, capture_output=True, timeout=5)
                self.assertEqual(result.returncode, 2)
            with socket.socket() as sock:
                sock.bind(('127.0.0.1', 0))
                self.port = sock.getsockname()[1]
            process = subprocess.Popen(['sh', str(self.root / script), '--port', str(self.port)],
                                       env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                deadline = time.monotonic() + 5
                while True:
                    try:
                        status, _, _ = self.request(route)
                        break
                    except OSError:
                        if process.poll() is not None or time.monotonic() > deadline:
                            self.fail('Server did not become ready')
                        time.sleep(0.02)
                self.assertEqual(status, 200)
                self.assertEqual(self.request('/.env')[0], 404)
            finally:
                process.terminate()
                process.communicate(timeout=5)

    def test_non_get_methods_cannot_mutate(self):
        self.serve()
        for method in ('POST', 'PUT', 'DELETE'):
            self.assertEqual(self.request('/assets/course.css', method)[0], 501)


if __name__ == '__main__':
    unittest.main()
