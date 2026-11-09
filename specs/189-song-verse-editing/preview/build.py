"""Assemble the spec-189 preview from the app's own page, stylesheets and tokens.

    python3 specs/189-song-verse-editing/preview/build.py

Reads `shell.html` — a snapshot of `/songs/1825/` taken from the local stack on
2026-11-05 (song "BN. HKBP 730: Berdayakan Diriku", songbook "Lagu") — and writes
`index.html`: the same shell, the same stylesheets, the same verse text, with this
slice's verse controls drawn over it.

The page is SELF-CONTAINED on purpose. The desktop chat's `::preview{file=…}` frame
loads a page through `srcdoc` in a sandboxed iframe with an opaque origin, so a
relative `<link>` or `<script src>` never resolves there; every stylesheet, script
and font is inlined. The `.css` / `.js` files beside this one stay the authors.
"""

import base64
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]

# fonts.css is left out on purpose: its two faces (CMG Sans, the projector's display
# face; Source Sans 3, the caption overlay's) are not used by one pixel of the reading
# shell, and inlining 1.2 MB of TTF would make the page 2 MB for nothing.
CSS_FILES = (
    "static/styles/design/tokens.css",
    "static/styles/design/components.css",
    "static/styles/design/generate.css",
    "specs/189-song-verse-editing/preview/preview.css",
)

GRIP = (
    '<button type="button" class="v__grip" aria-label="Drag to reorder verse {n}"'
    ' title="Drag to reorder">'
    '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7"'
    ' stroke-linecap="round" aria-hidden="true">'
    '<path d="M7 5.5h.01M13 5.5h.01M7 10h.01M13 10h.01M7 14.5h.01M13 14.5h.01"/></svg>'
    '</button>'
)
EDIT = (
    '<button type="button" class="v__edit" aria-label="Edit verse {n}" title="Edit verse {n}">'
    '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7"'
    ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M12.5 4.5l3 3-8 8H4.5v-3z"/></svg>'
    '</button>'
)

ADD = """<div class="verse-add">
  <button type="button" class="verse-add__btn" data-add-verse>
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9"
         stroke-linecap="round" aria-hidden="true"><path d="M10 4.5v11M4.5 10h11"/></svg>
    <span>Add verse</span>
  </button>
</div>
"""

EMPTY = """<template id="emptyState">
<div class="entry__empty">
  <p class="entry__empty-title">This song has no verses yet.</p>
  <p class="entry__empty-hint">Add the first verse to give this song its lyrics.</p>
  <div class="entry__empty-actions">
    <button type="button" class="verse-add__btn" data-add-verse>
      <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9"
           stroke-linecap="round" aria-hidden="true"><path d="M10 4.5v11M4.5 10h11"/></svg>
      <span>Add verse</span>
    </button>
  </div>
</div>
</template>
"""


def read_css(rel: str) -> str:
    """A stylesheet's text, with its font files embedded as data URIs."""
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")

    def embed(match):
        target = match.group(1)
        asset = (path.parent / target).resolve()
        if asset.suffix in (".ttf", ".woff2"):
            return ("data:font/" + asset.suffix.lstrip(".") + ";base64,"
                    + base64.b64encode(asset.read_bytes()).decode())
        return match.group(0)

    return re.sub(r'url\("([^"]+)"\)', embed, text)


def verse_markup(number: str, lyric: str) -> str:
    return (
        f'<p class="v" data-verse="{number}">'
        f'<span class="v__n">{number}</span>'
        f'<span class="v__text">{lyric}</span>'
        f'<span class="v__acts" role="group" aria-label="Verse {number}">'
        + GRIP.format(n=number) + EDIT.format(n=number) +
        '</span></p>\n'
    )


def main() -> None:
    shell = (HERE / "shell.html").read_text(encoding="utf-8")
    html_open = re.search(r"<html[^>]*>", shell).group(0)
    body_open = re.search(r"<body[^>]*>", shell).group(0)
    body = shell.split(body_open, 1)[1]
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)

    match = re.search(
        r'(<div class="read__body" id="readBody">)(.*?)(</div>\s*</article>)',
        body, re.S)
    if not match:
        raise SystemExit("read body not found in shell.html")
    inner = match.group(2)
    found = re.findall(
        r'<p class="v"><span class="v__n">(\d+)</span><span>(.*?)</span></p>',
        inner, re.S)
    if not found:
        raise SystemExit("no verses found in shell.html")

    verses = "".join(verse_markup(number, lyric) for number, lyric in found)
    body = body.replace(match.group(0), match.group(1) + verses + ADD + match.group(3), 1)

    style = "\n".join(read_css(rel) for rel in CSS_FILES)
    long_song = (HERE / "long_song.json").read_text(encoding="utf-8")
    data = "<script>window.__LONG_SONG = " + long_song + ";</script>"
    script = (HERE / "preview.js").read_text(encoding="utf-8")

    page = f"""<!doctype html>
{html_open}
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verse editing — preview (spec 189)</title>
<style>
{style}
</style>
</head>
{body_open}
{body}
{EMPTY}
{data}
<script>
{script}
</script>
</body>
</html>
"""
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {HERE / 'index.html'} ({len(page):,} bytes, {len(found)} verses)")


if __name__ == "__main__":
    main()
