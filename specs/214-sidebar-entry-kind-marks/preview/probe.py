"""Measure the static preview. Needs Playwright's Python package and a local Chrome.

    python specs/214-sidebar-entry-kind-marks/preview/probe.py
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent

MEASURE = """() => {
  const box = e => { const r = e.getBoundingClientRect();
    return {x: +r.x.toFixed(2), y: +r.y.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2)}; };
  const panes = [...document.querySelectorAll('.pane')].map(p => {
    const rows = [...p.querySelectorAll('#chList > li')].map(li => {
      const row = li.querySelector('a.songrow');
      const num = li.querySelector('.songrow__c');
      const mark = li.querySelector('.songrow__mark');
      const text = li.querySelector('.songrow__t');
      const line = text ? getComputedStyle(text).lineHeight : null;
      return {kind: mark ? mark.dataset.mark : 'break(no mark)',
              n: num ? num.textContent.trim() : null,
              row: row ? box(row) : box(li),
              num: num ? box(num) : null,
              mark: mark ? box(mark) : null,
              text: text ? box(text) : null,
              lines: text && line ? +(text.getBoundingClientRect().height / parseFloat(line)).toFixed(2) : null};
    });
    return {pane: ['0', 'A', 'B'].find(s => p.classList.contains('pane--' + s)) || '?',
            list: box(p.querySelector('#chList')), rows};
  });
  const cs = getComputedStyle(document.documentElement);
  return {panes, tokens: {canvas: cs.getPropertyValue('--canvas').trim(),
                          headInk: cs.getPropertyValue('--head-ink').trim()}};
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/google-chrome',
                                    args=['--no-sandbox'])
        try:
            for theme in ('light', 'dark'):
                page = browser.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)
                page.goto((HERE / 'index.html').as_uri())
                page.evaluate('(t) => document.documentElement.dataset.theme = t', theme)
                page.wait_for_timeout(50)
                print(f'=== theme {theme} ===')
                print(json.dumps(page.evaluate(MEASURE), indent=2))
                page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
