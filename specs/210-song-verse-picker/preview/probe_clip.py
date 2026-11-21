"""Measure the Verses panel for clipping on the live slice server.

Run: ~/Projects/multimedia-gkps-klender/.venv/bin/python probe_clip.py
"""
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get('SLICE_URL', 'http://127.0.0.1:8765/tatib/151/')
SHOTS = Path(__file__).resolve().parent / 'shots'
SHOTS.mkdir(exist_ok=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 801, 'height': 1044})
        page.goto(URL)
        page.wait_for_load_state('networkidle')
        page.evaluate("document.querySelector('[data-entry-open=\"song\"]').click()")
        page.wait_for_selector('dialog[open] #entry-song-search')
        page.locator('#entry-song-search').fill('HAL 2')
        page.wait_for_selector('#entry-song-options [data-song]')
        page.locator('#entry-song-options [data-song]').first.click()
        page.wait_for_selector('.editor__verse-tile')
        page.wait_for_timeout(500)
        page.screenshot(path=str(SHOTS / 'clip-801.png'), full_page=False)
        result = page.evaluate("""() => {
          const q = s => document.querySelector(s);
          const inner = q('.editor__verse-panel-inner');
          const panel = q('[data-verse-panel]');
          const tiles = [...document.querySelectorAll('.editor__verse-tile')];
          const last = tiles[tiles.length - 1].getBoundingClientRect();
          return {
            count: tiles.length,
            settled: panel.dataset.settled,
            display: getComputedStyle(panel).display,
            overflow: getComputedStyle(inner).overflow,
            cut: Math.round((last.bottom - inner.getBoundingClientRect().bottom) * 10) / 10,
            tileH: Math.round(tiles[0].getBoundingClientRect().height),
            panelH: Math.round(panel.getBoundingClientRect().height),
            innerH: Math.round(inner.getBoundingClientRect().height),
          };
        }""")
        print(json.dumps(result))
        browser.close()


if __name__ == '__main__':
    main()
