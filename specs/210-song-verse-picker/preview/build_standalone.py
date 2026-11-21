"""Inline the product CSS and preview JS into one portable HTML file."""
from pathlib import Path

base = Path(__file__).resolve().parent
out = base / 'song-verse-picker-preview.html'
html = (base / 'index.html').read_text()

for href in (
    '../../../static/styles/design/tokens.css',
    '../../../static/styles/design/components.css',
    'preview.css',
):
    tag = '<link rel="stylesheet" href="' + href + '">'
    css = (base / href).resolve().read_text()
    html = html.replace(tag, '<style>\n' + css + '\n</style>')

script = '<script src="preview.js"></script>'
js = (base / 'preview.js').read_text()
html = html.replace(script, '<script>\n' + js + '\n</script>')

assert '<link rel="stylesheet"' not in html, 'a stylesheet link survived'
assert '<script src=' not in html, 'a script src survived'
out.write_text(html)
print(out, out.stat().st_size, 'bytes')
