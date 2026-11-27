"""Measure and shoot spec 243 v5: locks, stage placeholder, cancellations."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
URL = (HERE / 'index.html').as_uri()

MEASURE = """() => {
  const stage = document.querySelector('.stage');
  const bar = document.getElementById('pvStagebar');
  const ph = document.getElementById('pvPlaceholder');
  const after = (s) => { const e = document.querySelector(s); return e ?
    getComputedStyle(e, '::after').content : null; };
  return {
    rowstyle: document.documentElement.dataset.rowstyle,
    scenario: document.documentElement.dataset.scenario,
    locked: [...document.querySelectorAll('.pv-row-busy, .pv-rail-busy')]
      .map((e) => (e.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 20)),
    rowOpacity: (document.querySelector('.pv-row-busy') ?
      getComputedStyle(document.querySelector('.pv-row-busy')).opacity : null),
    rowAfter: after('.pv-row-busy'), railAfter: after('.pv-rail-busy'),
    stageBusy: stage.getAttribute('aria-busy'),
    barShown: !bar.hidden, placeholderShown: !ph.hidden,
    placeholder: document.getElementById('pvPhTitle').textContent + ' / '
      + document.getElementById('pvPhMeta').textContent,
    status: document.getElementById('pvStatus').textContent,
    live: document.getElementById('pvLive').textContent
  };
}"""


def shot(page, name):
    print(name, json.dumps(page.evaluate(MEASURE)))
    page.screenshot(path=str(HERE / name))


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                    device_scale_factor=1)
            for style in ('a', 'b', 'c'):
                page.goto(URL)
                page.wait_for_timeout(100)
                page.click(f'.pv-bar button[data-rowstyle="{style}"]')
                page.wait_for_timeout(420)
                shot(page, f'shot5-row-{style}.png')
            for scenario, wait in (
                ('rail-stage', 420), ('sidebar-stage', 420),
                ('rail-list', 420), ('sidebar-list', 420),
                ('cancel-stage-stage', 900), ('cancel-stage-list', 900),
                ('cancel-list-stage', 900),
            ):
                page.goto(URL)
                page.wait_for_timeout(100)
                page.click(f'.pv-bar button[data-scenario="{scenario}"]')
                page.wait_for_timeout(wait)
                shot(page, f'shot5-{scenario}.png')
            page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
