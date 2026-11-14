#!/usr/bin/env python3
"""Copy the stylesheets this preview draws with, frozen at the slice's base commit.

The page links copies rather than the working tree's files, so the **Today** column keeps
drawing develop's rules after this slice's rules land. Nothing here generates markup:
`preview.html` is authored, and carries the preview dialog's real markup with the song the
report was taken from.

    python3 specs/153-preview-tabs-row/preview/build_preview.py
"""
import pathlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
FROZEN_AT = "24a6d6d2"          # develop, the base commit this slice is cut from

for name in ("fonts.css", "tokens.css", "components.css"):
    blob = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{FROZEN_AT}:static/styles/design/{name}"],
        capture_output=True, check=True,
    ).stdout
    (HERE / "assets").mkdir(exist_ok=True)
    (HERE / "assets" / name).write_bytes(blob)
    print(f"assets/{name}  {len(blob)} bytes  from {FROZEN_AT}")
