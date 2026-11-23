"""Run the focused template gate tests against a throwaway database name."""
import os
import subprocess
import sys
from urllib.parse import quote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PY = "/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python"

raw = subprocess.check_output(
    ["docker", "exec", "multimedia-gkps-klender-web-1", "python",
     "-c", "import os;print(os.environ['DATABASE_URL'])"], text=True).strip()
p = urlsplit(raw)
db_name = "gkps231"
path = "/%s" % db_name
os.environ["DATABASE_URL"] = "%s://%s:%s@127.0.0.1:59075%s" % (
    p.scheme, p.username, quote(p.password or "", safe=""), path)

cmd = [VENV_PY, "manage.py", "test"] + sys.argv[1:] + [
    "--keepdb", "--noinput"]
sys.stdout.write("$ manage.py %s\n" % " ".join(cmd[2:]))
sys.exit(subprocess.call(cmd, cwd=ROOT))
