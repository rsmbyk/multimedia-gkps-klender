"""Check that a clicked verse tile keeps no ring on the live slice server.

Run: ~/Projects/multimedia-gkps-klender/.venv/bin/python probe_ring.py
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
        page.locator('#entry-song-search').fill('HAL 3')
        page.wait_for_selector('#entry-song-options [data-song]')
        page.locator('#entry-song-options [data-song]').first.click()
        page.wait_for_selector('.editor__verse-tile')
        page.locator('.editor__verse-tile').nth(1).click()
        page.wait_for_timeout(350)
        page.screenshot(path=str(SHOTS / 'ring-801.png'), full_page=False)
        result = page.evaluate("""() => {
          const tile = document.querySelectorAll('.editor__verse-tile')[1];
          const s = getComputedStyle(tile);
          return {
            clickedOutlined: s.outlineWidth,
            checked: !!tile.querySelector('input:checked'),
            activeIsCheckbox: !!(document.activeElement && document.activeElement.type === 'checkbox'),
          };
        }""")
        print(json.dumps(result))
        browser.close()


if __name__ == '__main__':
    main()
