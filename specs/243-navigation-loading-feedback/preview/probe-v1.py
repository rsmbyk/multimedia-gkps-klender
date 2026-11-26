"""Measure spec 243's four loading-sign candidates in the static preview.

Run with the project venv's Python (it has Playwright):
  ~/Projects/multimedia-gkps-klender/.venv/bin/python probe.py
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
URL = (HERE / 'index.html').as_uri()

MEASURE = """() => {
  const box = (s) => { const e = document.querySelector(s); if (!e) return null;
    const b = e.getBoundingClientRect(); return {x:+b.x.toFixed(1), y:+b.y.toFixed(1),
      w:+b.width.toFixed(1), h:+b.height.toFixed(1), shown:!e.hidden &&
      getComputedStyle(e).display !== 'none'}; };
  const style = (s, p) => { const e = document.querySelector(s); return e ?
    getComputedStyle(e)[p] : null; };
  const pseudo = (s, p, which) => { const e = document.querySelector(s); return e ?
    getComputedStyle(e, which)[p] : null; };
  return {
    viewport: {w: innerWidth, h: innerHeight},
    stage: box('.stage'),
    progress: box('#pvProgress'), progressBg: style('#pvProgress','backgroundColor'),
    progressAnim: pseudo('#pvProgress','animationName','::before'),
    row: box('.pv-row-target'), rowShadow: style('.pv-row-target','boxShadow'),
    rowLabelOpacity: style('.pv-row-target .book__n','opacity'),
    spin: box('.pv-row-spin'), spinAnim: style('.pv-row-spin','animationName'),
    veil: box('#pvVeil'), veilBg: style('#pvVeil','backgroundColor'),
    toast: box('#pvToast'), toastBorder: style('#pvToast','borderLeftColor'),
    live: document.getElementById('pvLive').textContent
  };
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={'width': 900, 'height': 760},
                                    device_scale_factor=1)
            for option in 'abcd':
                page.goto(URL)
                page.wait_for_timeout(300)
                page.click(f'.pv-bar button[data-pv="{option}"]')
                page.wait_for_timeout(120)
                print(f'=== option {option} ===')
                print(json.dumps(page.evaluate(MEASURE)))
                page.screenshot(path=str(HERE / f'shot-{option}.png'))
            page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
