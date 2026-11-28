"""Measure the entry-kind marks on the live slice server.

Run with the project venv (the worktree shares the main checkout's venv):
  ~/Projects/multimedia-gkps-klender/.venv/bin/python preview/probe.py http://127.0.0.1:8771/obs/dock 144
"""

import json
import sys

from playwright.sync_api import sync_playwright

BOXES = """() => [...document.querySelectorAll('.entryli')].map(li => {
  const row = li.querySelector('.entryrow');
  const icon = row.querySelector('.entryicon');
  const chev = row.querySelector('.entrychev');
  const r = row.getBoundingClientRect();
  const i = icon && icon.getBoundingClientRect();
  const c = chev && chev.getBoundingClientRect();
  return {index: li.dataset.index, kind: icon && icon.dataset.kind,
          colour: icon && getComputedStyle(icon).color,
          glyphs: icon ? icon.querySelectorAll('svg > *').length : 0,
          icon: i ? [+i.left.toFixed(2), +i.right.toFixed(2)] : null,
          chevron: c ? [+c.left.toFixed(2), +c.right.toFixed(2)] : null,
          gap: i && c ? +(c.left - i.right).toFixed(2) : null,
          rowHeight: +r.height.toFixed(2)};
})"""


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8771/obs/dock'
    service = sys.argv[2] if len(sys.argv) > 2 else '144'
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={'width': 420, 'height': 800},
                                      device_scale_factor=1, color_scheme='dark')
        page = context.new_page()
        page.goto(url)
        page.locator(f'.servicerow[data-service="{service}"]').first.click()
        page.wait_for_selector('.entryrow')
        page.wait_for_timeout(250)
        print(json.dumps(page.evaluate(BOXES), indent=1))
        context.close()
        browser.close()


if __name__ == '__main__':
    main()
