"""Measure and shoot spec 243 v4: optimistic selection, fast vs slow path."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
URL = (HERE / 'index.html').as_uri()

MEASURE = """() => {
  const cur = [...document.querySelectorAll('[aria-current]')]
    .filter((e) => e.matches('.rail__btn, .book, .ch-num'))
    .map((e) => (e.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 24));
  const opening = document.getElementById('pvOpening');
  return {
    net: document.documentElement.dataset.net,
    scenario: document.documentElement.dataset.scenario,
    current: cur,
    title: document.getElementById('readName').textContent + ' '
      + (document.getElementById('readNo').hidden ? '' : document.getElementById('readNo').textContent),
    opening: !opening.hidden,
    live: document.getElementById('pvLive').textContent
  };
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                    device_scale_factor=1)
            for net in ('slow', 'fast'):
                for scenario in ('rail', 'first', 'second'):
                    page.goto(URL)
                    page.wait_for_timeout(120)
                    page.click(f'.pv-bar button[data-net="{net}"]')
                    page.click(f'.pv-bar button[data-scenario="{scenario}"]')
                    page.wait_for_timeout(80)
                    print(f'=== {net}/{scenario} @80ms ===', json.dumps(page.evaluate(MEASURE)))
                    page.wait_for_timeout(360)
                    m = page.evaluate(MEASURE)
                    print(f'=== {net}/{scenario} @440ms ===', json.dumps(m))
                    page.screenshot(path=str(HERE / f'shot4-{net}-{scenario}.png'))
                    page.wait_for_timeout(2200)
                    print(f'=== {net}/{scenario} settled ===', json.dumps(page.evaluate(MEASURE)))
            page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
