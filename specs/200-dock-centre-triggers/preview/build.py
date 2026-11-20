#!/usr/bin/env python3
"""Assemble the preview into ONE self-contained page.

The dock's own face is copied verbatim from the product's stylesheets, so the page
cannot drift from them silently; re-run this after touching either file. Self-contained
because the desktop chat's preview pane loads a page as `srcdoc` in a sandboxed frame,
where a relative <link>/<script> never resolves.

    python3 build.py
"""

from __future__ import annotations

import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]

STYLESHEETS = [
    REPO / "static/styles/design/tokens.css",
    REPO / "static/styles/design/obs-dock.css",
    HERE / "preview.css",
]
SOURCES = [HERE / "panel.html", HERE / "preview.js"]


def main() -> int:
    page = (HERE / "panel.html").read_text(encoding="utf-8")
    css = "\n".join(
        f"/* ===== {sheet.relative_to(REPO)} ===== */\n{sheet.read_text(encoding='utf-8')}"
        for sheet in STYLESHEETS
    )
    js = (HERE / "preview.js").read_text(encoding="utf-8")

    for marker, payload in (("/*__STYLES__*/", css), ("/*__SCRIPT__*/", js)):
        if marker not in page:
            raise SystemExit(f"marker {marker} missing from panel.html")
        page = page.replace(marker, payload)

    external = sorted(set(re.findall(r"url\((['\"]?)(?!data:)([^)'\"]+)\1\)", css)))
    commit = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True
    ).stdout.strip()

    out = HERE / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(REPO)} ({out.stat().st_size} bytes) at {commit}")
    if external:
        print("NOTE: stylesheets reference external assets (would 404 in a sandboxed frame):")
        for _, url in external:
            print(f"  {url}")
    else:
        print("no external url() in the stylesheets — the page is fully self-contained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
