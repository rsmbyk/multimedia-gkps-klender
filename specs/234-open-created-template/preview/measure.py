"""Measure the template stage the new create lands on (spec 234 preview)."""
import json
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8774/tatib/8/?mode=template'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900}, color_scheme='dark')
    page.goto(url, wait_until='networkidle')
    print(json.dumps(page.evaluate("""() => {
      const box = sel => { const e = document.querySelector(sel); if (!e) return null;
        const r = e.getBoundingClientRect();
        return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; };
      return {window: [innerWidth, innerHeight],
              readName: box('#readName'),
              eyebrow: box('.read__eyebrow'),
              empty: box('.entry__empty-title'),
              row: box('#panelBody .book[aria-current="true"]'),
              nav: document.documentElement.dataset.nav,
              ch: document.documentElement.dataset.ch,
              mode: document.getElementById('tatibMode')?.getAttribute('aria-pressed')};
    }"""), indent=2))
    browser.close()
