import json
import subprocess
import sys
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"
BASE_URL = "http://127.0.0.1:18080"


class PortfolioAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import os
        env = os.environ.copy()
        # Run the application on a dedicated test port.
        source = APP.read_text()
        source = source.replace(
            'HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()',
            'HTTPServer(("127.0.0.1", 18080), Handler).serve_forever()'
        )
        cls.temp_app = APP.parent / ".test_app_temp.py"
        cls.temp_app.write_text(source)
        cls.process = subprocess.Popen(
            [sys.executable, str(cls.temp_app)],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        for _ in range(50):
            try:
                urllib.request.urlopen(BASE_URL + "/health", timeout=1)
                break
            except Exception:
                if cls.process.poll() is not None:
                    raise RuntimeError("Application exited during startup")
                time.sleep(0.1)
        else:
            cls.process.terminate()
            raise RuntimeError("Application did not start in time")

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        try:
            cls.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            cls.process.kill()
            cls.process.wait()
        cls.temp_app.unlink(missing_ok=True)

    def get_json(self, path):
        with urllib.request.urlopen(BASE_URL + path, timeout=3) as response:
            return response.status, json.loads(response.read())

    def test_health_endpoint(self):
        status, body = self.get_json("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "healthy")
        self.assertEqual(body["service"], "portfolio-demo")

    def test_home_endpoint(self):
        status, body = self.get_json("/")
        self.assertEqual(status, 200)
        self.assertEqual(body["version"], "1.0.0")
        self.assertIn("architecture", body)

    def test_unknown_endpoint_returns_404(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(BASE_URL + "/missing", timeout=3)
        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
