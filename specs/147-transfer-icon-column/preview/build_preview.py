#!/usr/bin/env python3
"""Regenerate the transfer-row comparison preview.

The markup is the real dialog's own — captured from a running page after its own script has
drawn the rows, so the names, the glyph and the status labels are the companion's, not a
transcription. The stylesheets are FROZEN at the commit before this slice, because the
comparison has to keep showing the shipped rows as its "Now" column after the fix is in the
working tree; linking the live stylesheet would turn Now into a second Fixed.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/147-transfer-icon-column/preview/build_preview.py [url]

Reads   http://127.0.0.1:63404/media-library/ by default (a server whose Transfers dialog holds
        both short and long names), or the URL given as the first argument
Writes  preview.html + assets/{tokens,components,fonts}.css next to this file
"""
import pathlib
import subprocess
import sys

from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:63404/media-library/"
FROZEN_AT = "05379336"  # develop, immediately before this slice

for name in ("tokens.css", "components.css", "fonts.css"):
    blob = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{FROZEN_AT}:static/styles/design/{name}"],
        capture_output=True, check=True,
    ).stdout
    (HERE / "assets").mkdir(exist_ok=True)
    (HERE / "assets" / name).write_bytes(blob)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1200})
    page.goto(URL, wait_until="networkidle")
    page.click("#mediaTransfersButton")
    page.wait_for_selector(".media-transfers__row", timeout=15000)
    page.wait_for_timeout(600)
    rows = page.inner_html("#mediaTransfersList")
    browser.close()

# The rows are the list's own children; the dialog's heading is the only other thing drawn.

PANELS = [
    ("now", "wide", "Now — as shipped", "the mark is a shrinkable flex item: the long names pay for their own overflow"),
    ("fixed", "wide", "Fixed — the mark column pinned", "`flex: none` on the mark: the name ellipsizes, the column holds"),
    ("now", "narrow", "Now — as shipped, 382px dialog", "the window is 420px; the UA caps min(580px, 100vw - 32px) at 382px"),
    ("fixed", "narrow", "Fixed — the mark column pinned, 382px dialog", "same width, same rows, same column"),
]

panels = "\n".join(
    f'''<section class="panel" data-option="{option}" data-width="{width}">
  <header><b>{title}</b><small>{note}</small></header>
  <dialog open class="media-library__dialog media-transfers__dialog">
    <h2>Transfers</h2><div id="list-{option}-{width}" class="panel__list">{rows}</div>
  </dialog>
  <p class="readout" data-readout>measuring…</p>
</section>'''
    for option, width, title, note in PANELS
)

HTML = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Transfer rows — the icon column, before and after</title>
<link rel="stylesheet" href="assets/tokens.css">
<link rel="stylesheet" href="assets/components.css">
<style>
  /* Preview chrome only — nothing here ships. */
  html, body {{ margin: 0; }}
  body {{ background: var(--canvas); color: var(--ink); font-family: var(--font-sans); padding: 28px 24px 120px; }}
  h1 {{ margin: 0 0 6px; font-size: 20px; }}
  .lede {{ margin: 0 0 24px; max-width: 780px; color: var(--head-ink); font-size: 13.5px; line-height: 1.5; }}
  .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 26px 30px; align-items: start; }}
  .panel > header {{ display: flex; flex-direction: column; gap: 2px; margin-bottom: 10px; }}
  .panel > header b {{ font-size: 13.5px; }}
  .panel > header small {{ color: var(--head-ink); font-size: 12px; }}
  /* the dialog's own 190ms scale-in would be measured mid-flight: 32px of column reads 31.04 */
  dialog[open] {{ position: static; margin: 0; max-height: none; animation: none !important; }}
  /* a 420px window: min(580px, 100vw - 32px) = 388px, then Chrome's own
     dialog max-width calc(100% - 6px - 2em) caps the rendered box at 382px */
  .panel[data-width="narrow"] dialog {{ width: 382px; }}
  .readout {{ margin: 10px 0 0; font: 500 12px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--head-ink); white-space: pre-line; }}
  .readout b {{ color: var(--ink); }}
  .readout .off {{ color: var(--danger); }}
  .readout .ok {{ color: var(--focus); }}
</style>
<style>
  /* THE PROPOSED CHANGE, and nothing else. The implementation writes this same declaration on
     .media-transfers__mark itself; it is scoped here so the Now column keeps the shipped rule. */
  [data-option="fixed"] .media-transfers__mark {{ flex: none; }}
</style>
</head>
<body>
<h1>The Transfers dialog — one icon column, or one per row</h1>
<p class="lede">Real dialog markup, captured from the running page; real stylesheets, frozen at
{FROZEN_AT}. The rows are the companion's own nine jobs. Below each dialog: the smallest and largest left
edge of the glyph, of the name and of the status label, and how many names truncate.</p>
<div class="grid">
{panels}
</div>
<script>
for (const panel of document.querySelectorAll('.panel')) {{
  const list = panel.querySelector('.panel__list');
  const rows = [...list.querySelectorAll('.media-transfers__row')];
  const spread = (nodes) => {{
    const xs = nodes.map(n => n.getBoundingClientRect().left);
    return {{ min: Math.min(...xs), max: Math.max(...xs), spread: Math.max(...xs) - Math.min(...xs) }};
  }};
  const glyph = spread(rows.map(r => r.querySelector('.media-transfers__mark svg')));
  const name  = spread(rows.map(r => r.querySelector('.media-transfers__main strong')));
  const label = spread(rows.map(r => r.querySelector('.media-transfers__main span')));
  const truncated = rows.filter(r => {{ const s = r.querySelector('strong'); return s.scrollWidth > s.clientWidth; }}).length;
  const marks = [...new Set(rows.map(r => +r.querySelector('.media-transfers__mark').getBoundingClientRect().width.toFixed(2)))];
  const out = panel.querySelector('[data-readout]');
  const cls = (v) => v === 0 ? 'ok' : 'off';
  out.innerHTML =
    `${{rows.length}} rows · ${{truncated}} truncating · mark column ${{marks.join(' / ')}}px\\n` +
    `glyph x   ${{glyph.min.toFixed(1)}} .. ${{glyph.max.toFixed(1)}}   spread <b class="${{cls(glyph.spread)}}">${{glyph.spread.toFixed(1)}}px</b>\\n` +
    `name  x   ${{name.min.toFixed(1)}} .. ${{name.max.toFixed(1)}}   spread <b class="${{cls(name.spread)}}">${{name.spread.toFixed(1)}}px</b>\\n` +
    `label x   ${{label.min.toFixed(1)}} .. ${{label.max.toFixed(1)}}   spread <b class="${{cls(label.spread)}}">${{label.spread.toFixed(1)}}px</b>`;
}}
</script>
</body>
</html>
"""

(HERE / "preview.html").write_text(HTML, encoding="utf-8")
print(f"wrote {HERE / 'preview.html'} — {len(rows.splitlines())} lines of row markup from {URL}")
