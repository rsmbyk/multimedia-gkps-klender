#!/usr/bin/env python3
"""Copy the stylesheets this preview draws with, frozen at the slice's base commit.

The page links copies rather than the working tree's files, so the **Today** column keeps
showing develop's rules after this slice's change lands. Nothing here generates markup:
`preview.html` is authored, and carries the projector's real stage markup — the stage, a detour
screen and the `projector__empty` paragraph — at the screen's own 1920×1080.

The one edit to a copied sheet is the font path: `static/styles/design/fonts.css` points at
`../../assets/fonts/`, which from this pack would be a folder that does not exist. It is re-pointed
at the repository's committed faces (`static/assets/fonts/`) so the fitting measures the display's
real type, not a fallback.

    python3 specs/161-projector-empty-notice/preview/build_preview.py
"""
import pathlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
FROZEN_AT = "24a6d6d2"          # develop, the base commit this slice is cut from

for name in ("fonts.css", "tokens.css", "projector.css"):
    blob = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{FROZEN_AT}:static/styles/design/{name}"],
        capture_output=True, check=True,
    ).stdout
    if name == "fonts.css":
        blob = blob.replace(b"../../assets/fonts/", b"../../../../static/assets/fonts/")
    (HERE / "assets").mkdir(exist_ok=True)
    (HERE / "assets" / name).write_bytes(blob)
    print(f"assets/{name}  {len(blob)} bytes  from {FROZEN_AT}")
