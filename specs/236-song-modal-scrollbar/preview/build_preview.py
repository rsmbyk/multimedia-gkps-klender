#!/usr/bin/env python3
"""Assemble the spec-236 static preview from the project's real materials.

The dialog markup was captured from the running app's rendered #editorModal
(snippets/), and the CSS is copied verbatim from the slice worktree's
static/styles/design/. The only changed declaration lives in
css/after/components.css (`.editor { overflow: clip; }`). The before column
scopes that one declaration back to the base value so both states can be
measured on one page. `index.html` is generated SELF-CONTAINED: all four stylesheets
are inlined into one `<style>` block, because the chat's `srcdoc` frame is an opaque
origin where sibling files never resolve. Run the frame verifier before using
`::preview` with this page.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNIPPETS = HERE / "snippets"

TEMPLATE = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spec 236 — song entry modal scrollbar</title>
<style>
__STYLES__
</style>
</head>
<body>
<header class="pv-head">
  <div>
    <h1>Spec 236 — no scrollbar on the song entry modal</h1>
    <p>Real rendered <code>#editorModal</code> markup and the project's own CSS. The after column
       loads <code>css/after/components.css</code>, whose only change is <code>.editor { overflow: clip; }</code>.</p>
  </div>
  <button type="button" class="pv-theme" id="themeToggle">Switch to light</button>
</header>
<main class="pv-grid">
__COLUMNS__
</main>
<script>
(function () {
  document.querySelectorAll('.pv-panel').forEach(function (panel) {
    var d = panel.querySelector('.editor');
    var out = panel.querySelector('.pv-readout');
    if (!d || !out) return;
    var gutter = d.offsetWidth - d.clientWidth;
    out.textContent = 'dialog client ' + d.clientHeight + 'px · scroll ' + d.scrollHeight +
      'px · scrollbar gutter ' + gutter + 'px · overflow-y ' + getComputedStyle(d).overflowY;
  });
  var root = document.documentElement, btn = document.getElementById('themeToggle');
  btn.addEventListener('click', function () {
    var dark = root.getAttribute('data-theme') === 'dark';
    root.setAttribute('data-theme', dark ? 'light' : 'dark');
    btn.textContent = dark ? 'Switch to dark' : 'Switch to light';
  });
})();
</script>
</body>
</html>
"""

PANEL = """  <section class="pv-panel" data-panel="{key}">
    <h3>{variant}</h3>
    <div class="pv-stage">
{dialog}
    </div>
    <p class="pv-readout" data-readout></p>
  </section>"""

COLUMN = """<section class="pv-col pv-col--{side}">
  <h2>{heading}</h2>
  <p class="pv-note">{note}</p>
{panels}
</section>"""


def render(side, heading, note):
    panels = []
    for variant, name in (("new", "New song"), ("edit", "Edit song")):
        html = (SNIPPETS / f"{variant}-song-dialog.html").read_text().strip()
        html = html.replace('id="editorModal"', f'id="editorModal-{variant}-{side}"', 1)
        panels.append(PANEL.format(key=f"{variant}-{side}", variant=name, dialog=html))
    return COLUMN.format(side=side, heading=heading, note=note, panels="\n".join(panels))


STYLES = [
    ("tokens — base", "css/before/tokens.css"),
    ("components — after (one declaration changed)", "css/after/components.css"),
    ("generate — base", "css/before/generate.css"),
    ("preview scaffolding only", "preview.css"),
]
styles = "\n".join(
    "/* " + label + " */\n" + (HERE / path).read_text()
    for label, path in STYLES
)

html = TEMPLATE.replace("__COLUMNS__", "\n".join([
    render("before", "Before — develop", "UA dialog overflow (auto): the collapsed verse panel leaves 10px of overflow and the right-edge scrollbar."),
    render("after", "After — spec 236", "The dialog is not a scroll container; overflow is clipped at its rounded edge. The content wrapper still scrolls when content is taller."),
])).replace("__STYLES__", styles)
(HERE / "index.html").write_text(html)
print(f"wrote {HERE / 'index.html'} ({len(html)} chars)")
