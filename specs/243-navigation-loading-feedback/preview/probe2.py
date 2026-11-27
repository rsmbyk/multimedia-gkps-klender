"""Measure the revised spec 243 preview: one bar, any source, queue-aware."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
URL = (HERE / 'index.html').as_uri()

MEASURE = """() => {
  const bar = document.querySelector('#pvProgress');
  const b = bar.getBoundingClientRect();
  return {
    scenario: document.documentElement.dataset.scenario,
    nav: document.documentElement.dataset.nav,
    ch: document.documentElement.dataset.ch,
    bar: {shown: !bar.hidden, y: b.y, w: +b.width.toFixed(1), h: b.height},
    hint: document.getElementById('pvHint').textContent,
    sources: [...document.querySelectorAll('.pv-source')].map((el) => ({
      text: (el.textContent || '').trim().slice(0, 26),
      active: el.classList.contains('pv-source--active'),
      queued: el.classList.contains('pv-source--queued'),
      shadow: getComputedStyle(el).boxShadow
    })),
    live: document.getElementById('pvLive').textContent
  };
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={'width': 900, 'height': 760},
                                    device_scale_factor=1)
            for scenario in ('rail', 'first', 'second', 'queued'):
                page.goto(URL)
                page.wait_for_timeout(300)
                page.click(f'.pv-bar button[data-scenario="{scenario}"]')
                page.wait_for_timeout(260)
                print(f'=== {scenario} ===', json.dumps(page.evaluate(MEASURE)))
                page.screenshot(path=str(HERE / f'shot-{scenario}.png'))
                if scenario == 'queued':
                    page.wait_for_timeout(1100)
                    print('=== queued after swap ===', json.dumps(page.evaluate(MEASURE)))
                    page.screenshot(path=str(HERE / 'shot-queued-swapped.png'))
            page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
