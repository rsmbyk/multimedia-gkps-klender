"""Assemble a self-contained preview from the product's own CSS.

The desktop chat preview frame loads a local file through a sandboxed iframe with
an opaque origin, so relative <link> tags never resolve: everything is inlined.
The editor rules are copied verbatim out of the repo's stylesheets; only the
toolbar and the proposed notice variants are preview-only CSS.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

tokens = (REPO / "static/styles/design/tokens.css").read_text()
lines = (REPO / "static/styles/design/components.css").read_text().splitlines()
# 1-indexed, inclusive: dialog + large frame, narrow-width adjustments,
# head/field/control rules, help/actions/buttons.
ranges = [(513, 553), (680, 680), (689, 748), (845, 870)]
editor_css = "\n".join(
    "\n".join(lines[start - 1:end]) for start, end in ranges
)

html = (HERE / "template.html").read_text()
html = html.replace("/*__TOKENS__*/", tokens).replace("/*__EDITOR_CSS__*/", editor_css)
(HERE / "index.html").write_text(html)
print(f"wrote {HERE / 'index.html'} ({len(html)} bytes; {len(editor_css.splitlines())} product CSS lines inlined)")
