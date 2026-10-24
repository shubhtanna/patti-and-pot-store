import subprocess, os
code = r'''
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pattipot.settings")
os.environ["ALLOWED_HOSTS"] = "testserver"
django.setup()
from django.test import Client
c = Client()
r = c.get("/sitemap.xml")
print(r.status_code)
print(r.content.decode()[:1500])
r = c.get("/llms.txt")
print(r.status_code)
print(r.content.decode()[:800])
r = c.get("/")
html = r.content.decode()
print("product links on home:", html.count("/tea/"))
r = c.get("/shop/assam/")
html = r.content.decode()
print("product links on category:", html.count("/tea/"))
import re
print(re.findall(r'href="(/tea/[^"]+)"', html)[:5])
'''
out = subprocess.run([os.path.join(".venv", "bin", "python"), "-c", code], capture_output=True, text=True)
print(out.stdout)
print(out.stderr[-2000:])
