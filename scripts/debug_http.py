"""One-off diagnostic: probe the running test server over real HTTP, the way the
Tester does, to see what it actually receives.

Run from the repo root:  .venv/bin/python scripts/debug_http.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python")

try:
    import django  # noqa: F401
except ModuleNotFoundError:
    raise SystemExit(subprocess.run([VENV_PY, __file__], cwd=ROOT).returncode)

import json
import urllib.request  # noqa: E402

BASE = os.environ.get("PROBE_BASE", "http://127.0.0.1:8000")

for path in ["/", "/sitemap.xml", "/llms.txt", "/robots.txt", "/tea/assam-breakfast-ctc/"]:
    try:
        with urllib.request.urlopen(BASE + path, timeout=10) as r:
            body = r.read().decode("utf-8", "replace")
            print(path, r.status, "len", len(body))
            if path == "/sitemap.xml":
                print("  product urls:", body.count("/tea/"))
            if path == "/llms.txt":
                print("  product lines:", body.count("](/tea/"))
            if path == "/":
                print("  product links:", body.count("/tea/"))
            if path.startswith("/tea/"):
                print("  has jsonld:", "application/ld+json" in body)
    except Exception as e:
        print(path, "ERROR", repr(e))
