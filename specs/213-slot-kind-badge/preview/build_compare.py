"""Build the three-candidate comparison page (spec 213).

Three columns, each the real `/tatib/151/` slot rows at 1x, plus the same badge at 1x
pixels magnified 8x so the glyph itself can be judged. Re-run after any template or
stylesheet change:

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/213-slot-kind-badge/preview/build_compare.py
"""
import base64
import pathlib
import subprocess
import tempfile

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
SRC = REPO / 'static' / 'styles' / 'design'
BASE = 'http://127.0.0.1:8777'

COLS = [
    ('s11', 'A', '11px', 'glyph 8.5px', 'inside the corner', ''),
    ('s13', 'B', '13px', 'glyph 10px', 'overhanging 4px', 'adopted'),
    ('s15', 'C', '15px', 'glyph 11.5px', 'overhanging 5px', ''),
]

BADGE_CSS = """
#read .slot__mark .slot__badge {
  position: absolute; border-radius: 50%; display: grid; place-items: center;
  background: var(--canvas); color: var(--head-ink);
}
#read .slot__mark .slot__badge svg {
  width: 100%; height: 100%; fill: none; stroke: currentColor;
  stroke-linecap: round; stroke-linejoin: round;
}
[data-cand="s11"] #read .slot__mark .slot__badge { right:-2px; bottom:-2px; width:11px; height:11px; }
[data-cand="s11"] #read .slot__mark .slot__badge svg { width:8.5px; height:8.5px; stroke-width:1.7; }
[data-cand="s13"] #read .slot__mark .slot__badge { right:-4px; bottom:-3px; width:13px; height:13px; }
[data-cand="s13"] #read .slot__mark .slot__badge svg { width:10px; height:10px; stroke-width:1.6; }
[data-cand="s15"] #read .slot__mark .slot__badge { right:-5px; bottom:-4px; width:15px; height:15px; }
[data-cand="s15"] #read .slot__mark .slot__badge svg { width:11.5px; height:11.5px; stroke-width:1.5; }
"""

PAGE_CSS = """
html, body { margin: 0; }
/* the product's shell makes body a flex row; this page is a document, so say so */
body { display: block; background: var(--canvas); color: var(--ink); font-family: var(--font-sans); }
.bar { position: sticky; top: 0; z-index: 40; display: flex; flex-wrap: wrap;
  align-items: center; gap: 8px; padding: 9px 14px;
  background: color-mix(in srgb, var(--rail-bg) 92%, var(--canvas));
  border-bottom: 1px solid var(--divider); }
.bar button { padding: 6px 11px; border: 1px solid var(--divider); border-radius: 8px;
  background: var(--canvas); color: var(--ink); font: 600 12px/1 var(--font-sans); cursor: pointer; }
.bar .note { font: 500 11.5px/1.3 var(--font-sans); color: var(--head-ink); }
.cmp { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px;
  padding: 12px 14px 40px; align-items: start; }
.col { min-width: 0; }
.col > h2 { margin: 0 0 4px; font: 700 12.5px/1.2 var(--font-sans); letter-spacing: .02em; }
.col > h2 em { margin-left: 4px; padding: 1px 6px; border-radius: 999px;
  background: var(--active-bg); color: var(--active-ink);
  font: 700 10px/1.6 var(--font-sans); letter-spacing: .06em; text-transform: uppercase;
  font-style: normal; vertical-align: 1px; }
.col > h2 small { display: block; margin-top: 2px; font: 500 11px/1.3 var(--font-sans);
  color: var(--head-ink); letter-spacing: 0; }
.clip { width: 100%; overflow: hidden; }
.read { display: block; }
.read__body { container: stage-pane / inline-size; width: 400px; }
.clip .tatib__item { margin-left: 0; margin-right: 0; }
/* The comparison is the mark, so each row is cut back to its mark and its kind label:
   at three columns the full rows clip their titles mid-word, which reads as breakage. */
.clip .read__sec, .clip .choice__options, .clip .slot__add-row, .clip .entry__acts,
.clip .slot__state, .clip .read__sub { display: none; }
.zoom { margin-top: 10px; padding-top: 9px; border-top: 1px solid var(--divider); }
.zoom img { display: block; width: 100%; max-width: 220px; image-rendering: pixelated; }
.zoom p { margin: 4px 0 0; font: 500 10.5px/1.35 var(--font-sans); color: var(--head-ink); }
/* the forced hover, for looking at the fill without holding the pointer still */
#read .tatib__item--slot.is-forced-hover { background: var(--icon-hover-bg); }
#read .tatib__item--slot.is-forced-hover .slot__mark .slot__badge {
  background-image: linear-gradient(var(--icon-hover-bg), var(--icon-hover-bg)); }
"""

SCRIPT = """
(() => {
  const theme = document.getElementById('theme');
  theme.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme === 'dark';
    document.documentElement.dataset.theme = dark ? 'light' : 'dark';
    theme.textContent = dark ? 'Dark' : 'Light';
  });
  const hover = document.getElementById('hover');
  hover.addEventListener('click', () => {
    const on = hover.getAttribute('aria-pressed') !== 'true';
    hover.setAttribute('aria-pressed', String(on));
    document.querySelectorAll('#read .tatib__item--slot').forEach((row, i) => {
      if (i % 6 === 0) row.classList.toggle('is-forced-hover', on);
    });
  });
})();
"""


def strips():
    """1x pixels of one song slot and one passage slot, magnified 8x per candidate."""
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 900, 'height': 1000}, device_scale_factor=1)
        page.goto((HERE / 'index.html').as_uri())
        page.wait_for_timeout(300)
        page.evaluate("() => document.documentElement.dataset.theme = 'dark'")
        for opt, *_ in COLS:
            page.evaluate(f"() => document.documentElement.dataset.option = '{opt}'")
            page.wait_for_timeout(120)
            for anchor, label in (('e36', 'song'), ('e38', 'passage')):
                el = page.locator(f'#read [data-anchor="{anchor}"] .slot__mark').first
                el.scroll_into_view_if_needed()
                page.wait_for_timeout(100)
                b = el.bounding_box()
                tmp = pathlib.Path(tempfile.mkdtemp()) / f'{opt}-{label}.png'
                page.screenshot(path=str(tmp),
                                clip={'x': b['x'] - 4, 'y': b['y'] - 4,
                                      'width': b['width'] + 16, 'height': b['height'] + 14})
                big = tmp.with_name(tmp.stem + '-8x.png')
                subprocess.run(['magick', str(tmp), '-filter', 'point', '-resize', '800%',
                                str(big)], check=True)
                out[(opt, label)] = base64.b64encode(big.read_bytes()).decode()
        browser.close()
    return out


def rows():
    """The real slot rows, cloned once per column by the page's own script."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(BASE + '/tatib/151/', wait_until='networkidle')
        page.wait_for_timeout(400)
        html = page.evaluate("""() => [...document.querySelectorAll('#read .tatib__item--slot')]
            .map(el => el.outerHTML.replace(/\\sid="[^"]*"/g, '')).join('\\n')""")
        browser.close()
    return html


def main():
    sheets = {n: (SRC / n).read_text() for n in
              ('tokens.css', 'components.css', 'generate.css')}
    imgs = strips()
    body_rows = rows()

    cols = []
    for opt, letter, size, glyph, seat, state in COLS:
        zoom = ''
        for label in ('song', 'passage'):
            src = imgs[(opt, label)]
            zoom += (f'<div class="zoom"><img alt="the {label} badge at 1x, magnified 8x" '
                     f'src="data:image/png;base64,{src}">'
                     f'<p>{label} slot · {letter} · {size}, 1× pixels at 8×</p></div>')
        cols.append(f"""<section class="col" data-cand="{opt}">
  <h2>{letter} · {size}{' <em>adopted</em>' if state else ''}<small>{glyph} · {seat}</small></h2>
  <div class="clip"><article class="read" id="read" data-kind="tatib">
    <div class="read__body">{body_rows}</div>
  </article></div>
  {zoom}
</section>""")

    page = ('<!doctype html>\n<html lang="id" data-read="on" data-theme="dark">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>Slot kind badge — A, B and C side by side</title>\n'
            + '<style>\n' + sheets['tokens.css'] + '\n</style>\n'
            + '<style>\n' + sheets['components.css'] + '\n</style>\n'
            + '<style>\n' + sheets['generate.css'] + '\n</style>\n'
            + '<style>' + PAGE_CSS + '</style>\n'
            + '<style>' + BADGE_CSS + '</style>\n'
            + '</head>\n<body>\n'
            '<div class="bar"><span class="note">The same six slot rows, three badge sizes. '
            'Each column is clipped at the same width so the marks sit side by side.</span>'
            '<button type="button" id="hover" aria-pressed="false">Hover the first row</button>'
            '<button type="button" id="theme">Light</button></div>\n'
            '<div class="cmp">' + '\n'.join(cols) + '</div>\n'
            '<script>' + SCRIPT + '</script>\n</body>\n</html>\n')
    (HERE / 'compare.html').write_text(page)
    print('wrote', HERE / 'compare.html', len(page), 'bytes')


if __name__ == '__main__':
    main()
