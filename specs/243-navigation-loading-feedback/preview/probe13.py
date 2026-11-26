"""Measure and shoot spec 243 v9: dim-only lock, all scenarios."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
URL = (HERE / 'index.html').as_uri()

MEASURE = """() => {
  const locked = [...document.querySelectorAll('.pv-locked')];
  const railSvg = document.querySelector('.pv-rail-busy svg');
  const row = document.querySelector('.pv-row-busy');
  return {
    lockstyle: document.documentElement.dataset.lockstyle,
    scenario: document.documentElement.dataset.scenario,
    locked: locked.map((e) => (e.textContent || '').trim().replace(/\\s+/g,' ').slice(0, 24)),
    markers: locked.map((e) => e.querySelectorAll('.pv-rail-spin,.pv-lock-label,.pv-lock-edge,.pv-lock-ring').length),
    railSvg: railSvg ? getComputedStyle(railSvg).display : null,
    railOpacity: railSvg ? getComputedStyle(railSvg).opacity : null,
    rowOpacity: row ? getComputedStyle(row).opacity : null,
    stageBusy: document.querySelector('.stage').getAttribute('aria-busy'),
    barShown: !document.getElementById('pvStagebar').hidden,
    panelBarShown: !document.getElementById('pvPanelBar').hidden,
    chBarShown: !document.getElementById('pvChBar').hidden,
    barTops: (() => {
      const out = {};
      for (const id of ['pvPanelBar','pvChBar','pvStagebar']) {
        const e = document.getElementById(id), p = e.parentElement;
        if (e.hidden) { out[id] = null; continue; }
        out[id] = +(e.getBoundingClientRect().top - p.getBoundingClientRect().top).toFixed(2);
      }
      return out;
    })(),
    placeholder: (() => {
      for (const k of ['bible','song','service']) {
        const e = document.getElementById('pvPh-' + k);
        if (e && !e.hidden) return {kind: k,
          head: !!e.querySelector('.read__head'), body: !!e.querySelector('.read__body'),
          verses: e.querySelectorAll('.v').length,
          entries: e.querySelectorAll('.tatib__item').length,
          title: e.querySelector('.pv-ph-name').textContent};
      }
      return null;
    })(),
    status: document.getElementById('pvStatus').textContent
  };
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                    device_scale_factor=1)
            for scenario in ('rail-list', 'chapter-list', 'songbook-list',
                             'song-page', 'verse-page', 'service-page',
                             'cancel-page-page', 'cancel-page-list', 'cancel-list-page'):
                page.goto(URL)
                page.wait_for_timeout(100)
                page.click(f'.pv-bar button[data-scenario="{scenario}"]')
                wait = 900 if scenario.startswith('cancel') else 420
                page.wait_for_timeout(wait)
                print(f'=== {scenario} ===', json.dumps(page.evaluate(MEASURE)))
                page.screenshot(path=str(HERE / f'shot9-{scenario}.png'))
            page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
