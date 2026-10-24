import os, sys, subprocess, shutil
print("executable:", sys.executable)
print("version:", sys.version)
for p in [".venv/bin/python", "venv/bin/python", ".venv/Scripts/python.exe", "venv/Scripts/python.exe"]:
    print(p, os.path.exists(p))
print("python3:", shutil.which("python3"))
print("pip:", shutil.which("pip"))
try:
    import django
    print("django", django.get_version())
except Exception as e:
    print("no django:", e)
