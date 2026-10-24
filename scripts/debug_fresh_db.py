"""One-off diagnostic: build a fresh database from migrations only (like the test
harness does, since db.sqlite3 is gitignored) and check whether the catalogue loads.

Run from the repo root:  .venv/bin/python scripts/debug_fresh_db.py
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

sys.path.insert(0, ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pattipot.settings")
os.environ["ALLOWED_HOSTS"] = "testserver"

import django  # noqa: E402

django.setup()

from django.core.management import call_command  # noqa: E402
from django.test import Client  # noqa: E402

DB = os.path.join(ROOT, "db.sqlite3")
BACKUP = DB + ".bak"
if os.path.exists(BACKUP):
    os.remove(BACKUP)
if os.path.exists(DB):
    os.rename(DB, BACKUP)

try:
    call_command("migrate", verbosity=0)
    c = Client()
    r = c.get("/sitemap.xml")
    print("sitemap:", r.status_code, "product urls:", r.content.decode().count("/tea/"))
    r = c.get("/")
    print("home:", r.status_code, "product links:", r.content.decode().count("/tea/"))
    r = c.get("/tea/assam-breakfast-ctc/")
    print("product page:", r.status_code)
finally:
    # restore the original db
    if os.path.exists(DB):
        os.remove(DB)
    if os.path.exists(BACKUP):
        os.rename(BACKUP, DB)
