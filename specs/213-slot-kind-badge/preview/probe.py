"""Measure the slot kind badge (spec 213) on the live slice server.

Run: /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python specs/213-slot-kind-badge/preview/probe.py
Writes shots/ beside this file (gitignored).
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8777'
OUT = pathlib.Path(__file__).resolve().parent / 'shots'
OUT.mkdir(exist_ok=True)

MEASURE = """() => {
  const rows = [...document.querySelectorAll('#read .tatib__item--slot')];
  const box = el => { const b = el.getBoundingClientRect();
    return {x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1)}; };
  return rows.map(row => {
    const mark = row.querySelector('.slot__mark');
    const badge = row.querySelector('.slot__badge');
    const glyph = badge && badge.querySelector('svg');
    const title = row.querySelector('.read__sec');
    const label = row.querySelector('.slot__kind');
    const cs = el => el ? getComputedStyle(el) : null;
    const frame = mark && mark.querySelector(':scope > svg');
    return {
      anchor: row.dataset.anchor,
      slotKind: row.dataset.slotKind,
      resolvesTo: row.dataset.slot,
      label: label ? label.textContent.trim() : null,
      row: box(row),
      titleX: title ? +title.getBoundingClientRect().x.toFixed(1) : null,
      mark: mark ? box(mark) : null,
      markDash: frame ? cs(frame).strokeDasharray : null,
      markColor: mark ? cs(mark).color : null,
      badge: badge ? box(badge) : null,
      badgeKind: badge ? badge.dataset.kindBadge : null,
      badgeBg: badge ? cs(badge).backgroundColor : null,
      badgeColor: badge ? cs(badge).color : null,
      badgeGlyph: glyph ? box(glyph) : null,
      badgeStroke: glyph ? cs(glyph).strokeWidth : null,
      badgePath: glyph ? [...glyph.querySelectorAll('path,rect,circle')]
        .map(n => n.getAttribute('d') || n.tagName).join('|') : null,
    };
  });
}"""

GUTTER = """() => {
  const rows = [...document.querySelectorAll('#read .tatib__item--slot')];
  return rows.map(r => {
    const b = r.getBoundingClientRect();
    return {anchor: r.dataset.anchor, y: Math.round(b.y + window.scrollY), h: Math.round(b.height)};
  });
}"""


def main():
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                color_scheme='dark', device_scale_factor=1)
        page.goto(BASE + '/tatib/151/', wait_until='networkidle')
        page.wait_for_timeout(500)

        # ---- with the badge (the slice's change) ----
        report['with'] = page.evaluate(MEASURE)
        report['rows_with'] = page.evaluate(GUTTER)
        report['scroll_with'] = page.evaluate('() => document.documentElement.scrollHeight')

        # ---- the same page with the badge suppressed: what must not move ----
        page.add_style_tag(content='#read .slot__mark .slot__badge{display:none !important}')
        page.wait_for_timeout(200)
        report['rows_without'] = page.evaluate(GUTTER)
        report['scroll_without'] = page.evaluate('() => document.documentElement.scrollHeight')
        page.evaluate("""() => { const s = [...document.querySelectorAll('style')]
            .filter(e => e.textContent.includes('slot__badge{display:none'));
            s.forEach(e => e.remove()); }""")
        page.wait_for_timeout(200)

        # ---- screenshots: the gutter at 1x and 3x ----
        page.screenshot(path=str(OUT / 'page-dark.png'))
        first = page.locator('#read .tatib__item--slot').first
        first.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        page.screenshot(path=str(OUT / 'gutter-dark.png'),
                        clip={'x': 940, 'y': 0, 'width': 460, 'height': 620})

        # a crop of one song slot and one passage slot for the glyph itself
        for anchor in ('e36', 'e38'):
            el = page.locator(f'#read [data-anchor="{anchor}"]')
            if el.count():
                el.first.scroll_into_view_if_needed()
                page.wait_for_timeout(150)
                el.first.screenshot(path=str(OUT / f'row-{anchor}.png'))

        # ---- light theme ----
        page2 = browser.new_page(viewport={'width': 1440, 'height': 900},
                                 color_scheme='light', device_scale_factor=1)
        page2.goto(BASE + '/tatib/151/', wait_until='networkidle')
        page2.wait_for_timeout(500)
        report['light'] = page2.evaluate(MEASURE)
        page2.screenshot(path=str(OUT / 'gutter-light.png'),
                         clip={'x': 940, 'y': 0, 'width': 460, 'height': 620})

        # ---- the hover fill: does the disc read as a patch? ----
        page.locator('#read .tatib__item--slot').first.hover()
        page.wait_for_timeout(300)
        report['hover'] = page.evaluate("""() => {
          const row = document.querySelector('#read .tatib__item--slot');
          const badge = row.querySelector('.slot__badge');
          return {rowBg: getComputedStyle(row).backgroundColor,
                  badgeBg: getComputedStyle(badge).backgroundColor,
                  badgeColor: getComputedStyle(badge).color};
        }""")
        page.screenshot(path=str(OUT / 'gutter-hover-dark.png'),
                        clip={'x': 940, 'y': 0, 'width': 460, 'height': 620})

        # ---- the 400px pane: 1440 window with both sidebars open is the default here ----
        report['pane'] = page.evaluate("""() => {
          const read = document.querySelector('#read');
          return read ? Math.round(read.getBoundingClientRect().width) : null;
        }""")
        browser.close()

    (OUT / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2)[:6000])


if __name__ == '__main__':
    sys.exit(main())
