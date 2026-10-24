"""One-off generator: writes a simple SVG tin image per product into static/img/tins/.

Run from the repo root:  .venv/bin/python scripts/gen_tin_images.py
The generated files are committed with the change; the JSON-LD on each product
page points at its tin image.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python")

try:
    import django  # noqa: F401
except ModuleNotFoundError:
    # The tool runner's Python has no Django; re-exec with the repo's venv.
    raise SystemExit(subprocess.run([VENV_PY, __file__], cwd=ROOT).returncode)

sys.path.insert(0, ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pattipot.settings")

django = __import__("django")
django.setup()

from shop.models import Product  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "img", "tins")
os.makedirs(OUT, exist_ok=True)

TPL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 240" role="img" aria-label="{name} tin">
  <rect width="200" height="240" fill="#f6f1e7"/>
  <rect x="40" y="30" width="120" height="180" rx="10" fill="{colour}"/>
  <rect x="40" y="18" width="120" height="22" rx="8" fill="#d9c9a8"/>
  <rect x="58" y="70" width="84" height="100" rx="6" fill="#f6f1e7" opacity="0.92"/>
  <text x="100" y="105" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="bold" fill="#3a2a1a">{name}</text>
  <text x="100" y="128" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="#6b543a">{weight}</text>
  <text x="100" y="152" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="#6b543a">Patti &amp; Pot</text>
</svg>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


for p in Product.objects.all():
    svg = TPL.format(name=esc(p.name), weight=esc(p.weight), colour=p.colour)
    with open(os.path.join(OUT, f"{p.slug}.svg"), "w") as f:
        f.write(svg)
    print("wrote", p.slug + ".svg")
