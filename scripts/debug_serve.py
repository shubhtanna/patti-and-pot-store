import os, subprocess, sys, time, urllib.request
ROOT = os.getcwd()
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python")
env = dict(os.environ, DJANGO_SETTINGS_MODULE="pattipot.settings", ALLOWED_HOSTS="127.0.0.1,localhost")
log = open("server_debug.log", "w")
proc = subprocess.Popen([VENV_PY, "manage.py", "runserver", "127.0.0.1:8010", "--noreload"],
                        cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
time.sleep(4)
print("poll:", proc.poll())
for path in ["/", "/sitemap.xml", "/llms.txt", "/robots.txt", "/tea/assam-breakfast-ctc/"]:
    try:
        with urllib.request.urlopen("http://127.0.0.1:8010" + path, timeout=10) as r:
            body = r.read().decode("utf-8", "replace")
            print(path, r.status, "len", len(body), "| tea links:", body.count("/tea/"),
                  "| jsonld:", "application/ld+json" in body)
    except Exception as e:
        print(path, "ERROR", repr(e))
log.close()
print("--- server log ---")
print(open("server_debug.log").read()[-3000:])
