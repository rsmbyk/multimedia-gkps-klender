"""Assemble a self-contained preview from the product's own CSS.

The chat preview frame loads local files with an opaque origin, so relative
<link> tags never resolve: tokens and the real editor rules are inlined.
Only the state switcher and the proposed empty-state rules are preview-only;
everything else is copied verbatim from the repository's stylesheets.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

tokens = (REPO / "static/styles/design/tokens.css").read_text()
lines = (REPO / "static/styles/design/components.css").read_text().splitlines()
# 1-indexed and inclusive: the editor dialog frame, the head/field/control rules,
# the search field, and the whole verse picker block.
ranges = [(513, 553), (689, 745), (746, 754), (819, 834), (843, 850), (2720, 2788)]
editor_css = "\n".join(
    "\n".join(lines[start - 1:end]) for start, end in ranges
)

html = (HERE / "template.html").read_text()
html = html.replace("/*__TOKENS__*/", tokens).replace("/*__EDITOR_CSS__*/", editor_css)
(HERE / "index.html").write_text(html)
print(f"wrote {HERE / 'index.html'} ({len(html)} bytes; {len(editor_css.splitlines())} product CSS lines inlined)")
