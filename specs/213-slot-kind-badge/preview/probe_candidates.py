"""Measure every badge candidate on the preview page (spec 213).

Writes shots/cand-<option>-<theme>.png and shots/cand-<option>@4x.png, plus
shots/candidates.json with each candidate's measured box and contrast.

Run: /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/213-slot-kind-badge/preview/probe_candidates.py
"""
import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'shots'
OUT.mkdir(exist_ok=True)
PAGE = (HERE / 'index.html').as_uri()

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
    const badge = row.querySelector('.slot__badge');
    const glyph = badge && badge.querySelector('svg');
    const bcs = badge && getComputedStyle(badge);
    const show = bcs && bcs.display !== 'none';
    return {
      anchor: row.dataset.anchor,
      kind: badge ? badge.dataset.kindBadge : null,
      row: box(row),
      titleX: row.querySelector(':scope > .read__sec')
        ? +row.querySelector(':scope > .read__sec').getBoundingClientRect().x.toFixed(1) : null,
      badge: show ? box(badge) : null,
      glyph: show && glyph ? box(glyph) : null,
      disc: show ? bcs.backgroundColor : null,
      ink: show ? bcs.color : null,
      glyphStroke: show && glyph ? getComputedStyle(glyph).strokeWidth : null,
      contrast: show ? ratio(bcs.color, bcs.backgroundColor) : null,
    };
  });
}"""


def main():
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 900, 'height': 1000}, device_scale_factor=1)
        page.goto(PAGE)
        page.wait_for_timeout(300)

        for opt in ('now', 's11', 's13', 's15'):
            for theme in ('dark', 'light'):
                page.evaluate(f"""() => {{
                  document.documentElement.dataset.option = '{opt}';
                  document.documentElement.dataset.theme = '{theme}';
                }}""")
                page.wait_for_timeout(120)
                key = f'{opt}-{theme}'
                report[key] = page.evaluate(MEASURE)
                page.screenshot(path=str(OUT / f'cand-{key}.png'),
                                clip={'x': 0, 'y': 60, 'width': 900, 'height': 620})

        # 4x crops of one fill-in mark (song) and one choice mark (passage)
        page4 = browser.new_page(viewport={'width': 900, 'height': 1000}, device_scale_factor=4)
        page4.goto(PAGE)
        page4.wait_for_timeout(300)
        page4.evaluate("() => { document.documentElement.dataset.theme = 'dark'; }")
        for opt in ('s11', 's13', 's15'):
            page4.evaluate(f"() => {{ document.documentElement.dataset.option = '{opt}'; }}")
            page4.wait_for_timeout(120)
            for anchor in ('e36', 'e38'):
                el = page4.locator(f'#read [data-anchor="{anchor}"] .slot__mark')
                el.first.scroll_into_view_if_needed()
                page4.wait_for_timeout(100)
                b = el.first.bounding_box()
                page4.screenshot(path=str(OUT / f'cand-{opt}-{anchor}@4x.png'),
                                 clip={'x': b['x'] - 6, 'y': b['y'] - 6,
                                       'width': b['width'] + 18, 'height': b['height'] + 16})
        browser.close()

    (OUT / 'candidates.json').write_text(json.dumps(report, indent=2))
    for key in ('s11-dark', 's13-dark', 's15-dark'):
        rows = [r for r in report[key] if r['badge']]
        first = rows[0]
        print(f"{key}: badge {first['badge']['w']}x{first['badge']['h']} "
              f"glyph {first['glyph']['w']}x{first['glyph']['h']} "
              f"stroke {first['glyphStroke']} contrast {first['contrast']} "
              f"| badges {len(rows)}")
    print('now-dark badges:', len([r for r in report['now-dark'] if r['badge']]))


if __name__ == '__main__':
    main()
