#!/usr/bin/env python3
"""Assemble the scroll-tuning harness into one self-contained page."""
from __future__ import annotations

import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
SHEETS = [REPO / "static/styles/design/tokens.css",
          REPO / "static/styles/design/obs-dock.css",
          HERE / "tune.css"]


def main() -> int:
    page = (HERE / "tune.html").read_text(encoding="utf-8")
    css = "\n".join(f"/* ===== {p.relative_to(REPO)} ===== */\n{p.read_text(encoding='utf-8')}"
                    for p in SHEETS)
    js = (HERE / "tune.js").read_text(encoding="utf-8")
    for marker, payload in (("/*__STYLES__*/", css), ("/*__SCRIPT__*/", js)):
        if marker not in page:
            raise SystemExit(f"marker {marker} missing from tune.html")
        page = page.replace(marker, payload)
    external = sorted(set(re.findall(r"url\((['\"]?)(?!data:)([^)'\"]+)\1\)", css)))
    out = HERE / "tune-built.html"
    out.write_text(page, encoding="utf-8")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    print(f"wrote {out.relative_to(REPO)} ({out.stat().st_size} bytes) at {commit}")
    print("external assets:", external or "none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
