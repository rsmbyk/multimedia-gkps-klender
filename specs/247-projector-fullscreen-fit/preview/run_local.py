#!/usr/bin/env python3
"""Run a command with DATABASE_URL taken from the compose web container at run time.

Never prints the credential. `db:5432` inside the container is translated to the
published host and port; GKPS_DB overrides only the database name, so a test run
gets a throwaway database a parallel session cannot lock.
"""
import os
import subprocess
import sys
from urllib.parse import unquote, urlsplit, urlunsplit

CONTAINER = "multimedia-gkps-klender-web-1"
HOST = "127.0.0.1"
PORT = os.environ.get("GKPS_DB_PORT", "59075")


def main():
    separator = sys.argv.index("--") if "--" in sys.argv else -1
    if separator < 0 or separator == len(sys.argv) - 1:
        print("usage: run_local.py [--] <command> [args...]", file=sys.stderr)
        return 2
    raw = subprocess.check_output(
        ["docker", "exec", CONTAINER, "python", "-c",
         "import os; print(os.environ['DATABASE_URL'])"],
        text=True,
    ).strip()
    parts = urlsplit(raw)
    user = unquote(parts.username or "")
    password = unquote(parts.password or "")
    database = os.environ.get("GKPS_DB") or parts.path.lstrip("/")
    netloc = f"{user}:{password}@{HOST}:{PORT}"
    path = "/" + database
    env = dict(os.environ, DATABASE_URL=urlunsplit(
        (parts.scheme, netloc, path, parts.query, parts.fragment)))
    return subprocess.call(sys.argv[separator + 1:], env=env)


if __name__ == "__main__":
    raise SystemExit(main())
