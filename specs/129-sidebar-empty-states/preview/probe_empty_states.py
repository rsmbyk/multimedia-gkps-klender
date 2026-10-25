"""Probe spec 129's sidebar empty states in a real browser and print measurements.

Read-only: opens pages on the dev server, forces each state, and reports the
state text, the glyph shown, and how far the block's ink sits from the centre
of the list area it belongs to.
"""

import json
import sys

from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8801'
OUT = '/tmp'


def measure(page, selector):
    return page.evaluate(
        """(selector) => {
        const el = document.querySelector(selector);
        if (!el || el.hidden) return null;
        const box = el.getBoundingClientRect();
        const kids = Array.from(el.children)
          .filter((child) => child.getBoundingClientRect().height > 0);
        const rects = kids.map((child) => child.getBoundingClientRect());
        const top = Math.min(...rects.map((r) => r.top));
        const bottom = Math.max(...rects.map((r) => r.bottom));
        const left = Math.min(...rects.map((r) => r.left));
        const right = Math.max(...rects.map((r) => r.right));
        const glyph = el.querySelector('.listempty__icon:not([style*="none"])');
        const shownIcon = Array.from(el.querySelectorAll('.listempty__icon'))
          .find((node) => getComputedStyle(node).display !== 'none');
        return {
          state: el.dataset.state,
          title: el.querySelector('.listempty__title').textContent,
          hint: el.querySelector('.listempty__hint').textContent,
          iconFor: shownIcon ? shownIcon.dataset.when : null,
          iconPx: shownIcon ? Math.round(shownIcon.getBoundingClientRect().width) : 0,
          sidePx: Math.round(box.height),
          dvCenter: Math.round(((top + bottom) / 2 - (box.top + box.bottom) / 2) * 10) / 10,
          dhCenter: Math.round(((left + right) / 2 - (box.left + box.right) / 2) * 10) / 10,
          boxCenter: Math.round((box.top + box.bottom) / 2),
          inkTop: Math.round(top),
          inkBottom: Math.round(bottom)
        };
      }""", selector)


def report(name, page, selectors):
    print(f'\n== {name}')
    for selector in selectors:
        data = measure(page, selector)
        print(f'  {selector}: {json.dumps(data)}')


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})

        # 1. a Tata Ibadah with no sections at all
        page.goto(BASE + '/tatib/148/')
        page.wait_for_selector('#chapters')
        page.wait_for_timeout(250)
        report('tatib 148 — empty service', page, ['#chEmpty'])
        page.screenshot(path=f'{OUT}/gkps129-empty-sections.png')

        # 2. the same list, filtered to nothing (service 143 has entries)
        page.goto(BASE + '/tatib/143/')
        page.wait_for_selector('#chapters')
        page.fill('#songFilter', 'zzz')
        page.wait_for_timeout(200)
        report('tatib 143 — sections filter miss', page, ['#chEmpty'])
        page.screenshot(path=f'{OUT}/gkps129-filtered-sections.png')

        # 3. the first column filtered to nothing
        page.fill('#bookFilter', 'zzz')
        page.wait_for_timeout(200)
        report('tatib 143 — panel filter miss', page, ['#panelEmpty'])
        page.screenshot(path=f'{OUT}/gkps129-filtered-panel.png')

        # 4. a songbook with no songs
        page.goto(BASE + '/songs/book/36/')
        page.wait_for_selector('#chapters')
        page.wait_for_timeout(250)
        report('songbook 36 — no songs', page, ['#chEmpty'])
        page.screenshot(path=f'{OUT}/gkps129-empty-songs.png')

        # 5. a hymn songbook filtered to nothing
        page.goto(BASE + '/songs/book/1/')
        page.wait_for_selector('#chapters')
        page.fill('#songFilter', 'zzz')
        page.wait_for_timeout(200)
        report('songbook 1 — songs filter miss', page, ['#chEmpty'])
        page.screenshot(path=f'{OUT}/gkps129-filtered-songs.png')

        # 6. the collapsed panel keeps the rail clean
        page.goto(BASE + '/bible/')
        page.wait_for_selector('#panelBody')
        page.fill('#bookFilter', 'zzz')
        page.locator('#panelCollapse').click()
        page.wait_for_timeout(300)
        print('\n== mini panel')
        print('  collapsed empty visible:', page.evaluate(
            "getComputedStyle(document.getElementById('panelEmpty')).display"))

        browser.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
