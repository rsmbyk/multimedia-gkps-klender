"""Measure and shoot spec 243 v8: alternatives to the spinner."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
URL = (HERE / 'index.html').as_uri()

MEASURE = """() => {
  const locked = [...document.querySelectorAll('.pv-locked')];
  return {
    lockstyle: document.documentElement.dataset.lockstyle,
    scenario: document.documentElement.dataset.scenario,
    locked: locked.map((e) => (e.textContent || '').trim().replace(/\\s+/g,' ').slice(0, 24)),
    markers: locked.map((e) => [...e.children].filter((c) =>
      /^pv-(rail-spin|lock-label|lock-edge|lock-ring)$/.test(c.className))
      .map((c) => c.className)),
    rowOpacity: locked[0] ? getComputedStyle(locked[0]).opacity : null,
    stageBusy: document.querySelector('.stage').getAttribute('aria-busy'),
    barShown: !document.getElementById('pvStagebar').hidden,
    status: document.getElementById('pvStatus').textContent
  };
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                    device_scale_factor=1)
            for scenario in ('verse-page', 'rail-list'):
                for style in ('spinner', 'label', 'edge', 'ring', 'dim'):
                    page.goto(URL)
                    page.wait_for_timeout(100)
                    page.click(f'.pv-bar button[data-lockstyle="{style}"]')
                    page.click(f'.pv-bar button[data-scenario="{scenario}"]')
                    page.wait_for_timeout(420)
                    print(f'=== {scenario}/{style} ===', json.dumps(page.evaluate(MEASURE)))
                    page.screenshot(path=str(HERE / f'shot8-{style}-{scenario}.png'))
            page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
