"""The adopted badge (13px, glyph 10px) measured on the live slice page.

Writes shots/adopted-<theme>.png and shots/adopted.json, and prints the numbers the
spec's `## UI/UX` section carries.

Run: /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/213-slot-kind-badge/preview/probe_adopted.py
"""
import json
import pathlib
import subprocess

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'shots'
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:8777'
URL = BASE + '/tatib/151/'

MEASURE = """() => {
  const rows = [...document.querySelectorAll('#read .tatib__item--slot')];
  const box = el => { const b = el.getBoundingClientRect();
    return {x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1)}; };
  const lum = (c) => { const [r,g,b] = c.match(/[\\d.]+/g).slice(0,3).map(Number).map(v => v/255)
      .map(v => v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4));
    return 0.2126*r + 0.7152*g + 0.0722*b; };
  const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b);
    return +(((Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05))).toFixed(2); };
  return rows.map(row => {
    const mark = row.querySelector('.slot__mark');
    const frame = mark.querySelector(':scope > svg');
    const badge = row.querySelector('.slot__badge');
    const glyph = badge && badge.querySelector('svg');
    const label = row.querySelector('.slot__kind');
    const sec = row.querySelector(':scope > .read__sec');
    const shown = !!badge && getComputedStyle(badge).display !== 'none';
    const mb = mark.getBoundingClientRect();
    const bb = shown ? badge.getBoundingClientRect() : null;
    const lb = label.getBoundingClientRect();
    const bcs = shown ? getComputedStyle(badge) : null;
    return {
      anchor: row.dataset.anchor,
      kind: badge ? badge.dataset.kindBadge : null,
      label: label.textContent.trim(),
      row: box(row),
      titleX: sec ? +sec.getBoundingClientRect().x.toFixed(1) : null,
      mark: box(mark),
      frameStroke: getComputedStyle(frame).strokeDasharray,
      badge: shown ? box(badge) : null,
      glyph: shown && glyph ? box(glyph) : null,
      glyphStroke: shown && glyph ? getComputedStyle(glyph).strokeWidth : null,
      disc: bcs ? bcs.backgroundColor : null,
      ink: bcs ? bcs.color : null,
      contrastOnDisc: bcs ? ratio(bcs.color, bcs.backgroundColor) : null,
      gapBadgeToLabel: bb ? +(lb.left - bb.right).toFixed(1) : null,
      overhangX: bb ? +(bb.right - mb.right).toFixed(1) : null,
      overhangY: bb ? +(bb.bottom - mb.bottom).toFixed(1) : null,
      insideRow: bb ? bb.right <= row.getBoundingClientRect().right
                      && bb.bottom <= row.getBoundingClientRect().bottom : null,
    };
  });
}"""


def main():
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for theme in ('dark', 'light'):
            page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                    color_scheme=theme, device_scale_factor=1)
            page.goto(URL, wait_until='networkidle')
            page.wait_for_timeout(450)
            report[theme] = page.evaluate(MEASURE)
            report[f'{theme}_scroll'] = page.evaluate('() => document.documentElement.scrollHeight')

            # suppressed: what must not move
            page.add_style_tag(content='#read .slot__mark .slot__badge{display:none !important}')
            page.wait_for_timeout(200)
            report[f'{theme}_suppressed'] = page.evaluate(MEASURE)
            report[f'{theme}_suppressed_scroll'] = page.evaluate(
                '() => document.documentElement.scrollHeight')
            page.evaluate("""() => [...document.querySelectorAll('style')]
                .filter(e => e.textContent.includes('slot__badge{display:none'))
                .forEach(e => e.remove())""")
            page.wait_for_timeout(200)

            # the pointed-at state: does the disc still read as a hole?
            page.evaluate("""() => document.querySelector('#read [data-anchor="e36"]')
                .classList.add('is-modal-origin')""")
            page.wait_for_timeout(250)
            report[f'{theme}_tinted'] = page.evaluate("""() => {
              const row = document.querySelector('#read [data-anchor="e36"]');
              const d = getComputedStyle(row.querySelector('.slot__badge'));
              return {rowBg: getComputedStyle(row).backgroundColor,
                      discImage: d.backgroundImage.slice(0, 46),
                      ink: d.color};
            }""")
            page.screenshot(path=str(OUT / f'adopted-{theme}.png'),
                            clip={'x': 950, 'y': 300, 'width': 420, 'height': 420})
            for anchor in ('e36', 'e38', 'e56', 'e51'):
                el = page.locator(f'#read [data-anchor="{anchor}"] .slot__mark').first
                el.scroll_into_view_if_needed()
                page.wait_for_timeout(120)
                b = el.bounding_box()
                tmp = OUT / f'adopted-{theme}-{anchor}.png'
                page.screenshot(path=str(tmp),
                                clip={'x': b['x'] - 8, 'y': b['y'] - 8,
                                      'width': b['width'] + 26, 'height': b['height'] + 22})
                subprocess.run(['magick', str(tmp), '-filter', 'point', '-resize', '800%',
                                str(OUT / f'adopted-{theme}-{anchor}-8x.png')], check=True)
            page.close()
        browser.close()

    (OUT / 'adopted.json').write_text(json.dumps(report, indent=2))
    for theme in ('dark', 'light'):
        rows = report[theme]
        r = rows[0]
        same_rows = ([{k: v for k, v in x.items() if k in ('anchor', 'row', 'titleX')}
                      for x in rows]
                     == [{k: v for k, v in x.items() if k in ('anchor', 'row', 'titleX')}
                         for x in report[f'{theme}_suppressed']])
        print(f'--- {theme} ---')
        print(f'  badge {r["badge"]["w"]}x{r["badge"]["h"]}  glyph {r["glyph"]["w"]}px '
              f'stroke {r["glyphStroke"]}')
        print(f'  disc {r["disc"]}  ink {r["ink"]}  contrast {r["contrastOnDisc"]}:1')
        print(f'  overhang right {r["overhangX"]}px / bottom {r["overhangY"]}px; '
              f'gap to label {r["gapBadgeToLabel"]}px; inside row {r["insideRow"]}')
        print(f'  rows+scroll unchanged with badge suppressed: {same_rows} '
              f'({report[f"{theme}_scroll"]} vs {report[f"{theme}_suppressed_scroll"]})')
        print(f'  tinted: {report[f"{theme}_tinted"]}')
        print(f'  kinds: {[(x["kind"], x["label"]) for x in rows]}')


if __name__ == '__main__':
    main()
