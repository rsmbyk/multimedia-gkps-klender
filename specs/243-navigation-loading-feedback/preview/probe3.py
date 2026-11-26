"""Measure and shoot spec 243 v3: 3 treatments x 3 click sources."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
URL = (HERE / 'index.html').as_uri()

MEASURE = """() => {
  const shown = (s) => [...document.querySelectorAll(s)].filter((e) => {
    const b = e.getBoundingClientRect();
    return getComputedStyle(e).display !== 'none' && b.width > 0 && b.height > 0;
  });
  const where = (s) => shown(s).map((e) => e.closest('#panelBody,#chBody,.stage')?.id
    || (e.closest('.stage') ? 'stage' : 'unknown'));
  return {
    treatment: document.documentElement.dataset.treatment,
    scenario: document.documentElement.dataset.scenario,
    busy: document.documentElement.classList.contains('pv-busy'),
    strips: where('.pv-strip'), skeletons: where('.pv-skel'), placeholders: where('.pv-place'),
    sourceMarks: document.querySelectorAll('.pv-source').length,
    live: document.getElementById('pvLive').textContent
  };
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                    device_scale_factor=1)
            for treatment in ('quiet', 'skeleton', 'placeholder'):
                for scenario in ('rail', 'first', 'second'):
                    page.goto(URL)
                    page.wait_for_timeout(120)
                    page.click(f'.pv-bar button[data-treatment="{treatment}"]')
                    page.click(f'.pv-bar button[data-scenario="{scenario}"]')
                    page.wait_for_timeout(390)
                    print(f'=== {treatment}/{scenario} ===',
                          json.dumps(page.evaluate(MEASURE)))
                    page.screenshot(path=str(HERE / f'shot3-{treatment}-{scenario}.png'))
            # Timing guard: no busy state before 300ms, none after settlement.
            page.goto(URL)
            page.wait_for_timeout(120)
            page.click('.pv-bar button[data-scenario="first"]')
            page.wait_for_timeout(150)
            print('=== early (150 ms) ===', json.dumps(page.evaluate(MEASURE)))
            page.wait_for_timeout(2400)
            print('=== settled ===', json.dumps(page.evaluate(MEASURE)))
            page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
