"""The four badge glyphs, read as pixels (spec 213).

For each kind, captures the badge element itself (an element screenshot, which is immune
to the bounding-box / clip coordinate mismatch: `bounding_box()` is viewport-relative and
`page.screenshot(clip=…)` is document-relative, so a scrolled page silently captures empty
background), prints its 13px pixel map as text, and compares every pair.

Run: /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/213-slot-kind-badge/preview/probe_glyphs.py
"""
import itertools
import pathlib
import subprocess

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'shots'
OUT.mkdir(exist_ok=True)
URL = 'http://127.0.0.1:8777/tatib/151/'
KINDS = ('song', 'scripture', 'media', 'text')
RAMP = ' .:-=+*#%@'


def gray(path):
    txt = subprocess.run(['magick', str(path), '-colorspace', 'gray', '-depth', '8', 'txt:-'],
                         capture_output=True, text=True, check=True).stdout
    px = {}
    for line in txt.splitlines()[1:]:
        coord, rest = line.split(':', 1)
        x, y = map(int, coord.split(','))
        px[(x, y)] = int(rest.split('(')[1].split(',')[0].split(')')[0])
    return px


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                color_scheme='dark', device_scale_factor=1)
        page.goto(URL, wait_until='networkidle')
        page.wait_for_timeout(400)
        paint = page.evaluate("""() => {
          const s = getComputedStyle(document.querySelector('#read .slot__badge svg'));
          return {fill: s.fill, stroke: s.stroke, width: s.width};
        }""")
        print(f"paint: fill={paint['fill']} stroke={paint['stroke']} width={paint['width']}")
        assert paint['fill'] == 'none', 'the glyph is filled, not stroked: it will paint as a blob'
        assert paint['stroke'] != 'none', 'the glyph has no stroke: it will not paint at all'
        for kind in KINDS:
            el = page.locator(f'#read .slot__badge[data-kind-badge="{kind}"]').first
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(150)
            el.screenshot(path=str(OUT / f'glyph-{kind}.png'))
        browser.close()

    maps = {}
    for kind in KINDS:
        px = gray(OUT / f'glyph-{kind}.png')
        maps[kind] = px
        w, h = max(x for x, y in px) + 1, max(y for x, y in px) + 1
        print(f'--- {kind} ({w}x{h}) levels {min(px.values())}..{max(px.values())} ---')
        for y in range(h):
            print(''.join(RAMP[min(9, px[(x, y)] * 10 // 256)] for x in range(w)))

    print('\nmean absolute difference, normalised (a distinct glyph scores well above 0.05):')
    worst = 1.0
    for a, b in itertools.combinations(KINDS, 2):
        lo = min(min(maps[a].values()), min(maps[b].values()))
        span = max(max(maps[a].values()), max(maps[b].values())) - lo or 1
        d = sum(abs(maps[a][k] - maps[b][k]) for k in maps[a]) / (len(maps[a]) * span)
        worst = min(worst, d)
        print(f'  {a:10s} vs {b:10s} {d:.3f}')
    print(f'\nclosest pair: {worst:.3f}')

    tiles = []
    for kind in KINDS:
        big = OUT / f'glyph-{kind}-8x.png'
        subprocess.run(['magick', str(OUT / f'glyph-{kind}.png'), '-filter', 'point',
                        '-resize', '800%', '-bordercolor', '#14130F', '-border', '12',
                        str(big)], check=True)
        tiles.append(str(big))
    subprocess.run(['magick'] + tiles + ['+append', str(OUT / 'glyph-sheet-8x.png')], check=True)
    print('wrote', OUT / 'glyph-sheet-8x.png')


if __name__ == '__main__':
    main()
