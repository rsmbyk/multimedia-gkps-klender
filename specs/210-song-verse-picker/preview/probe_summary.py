"""Check that the verse summary row is display text on the live slice server.

Run: ~/Projects/multimedia-gkps-klender/.venv/bin/python probe_summary.py
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
        page.wait_for_timeout(350)
        summary = page.locator('[data-verses-summary]')
        before = summary.inner_text()
        summary.click()
        page.wait_for_timeout(250)
        page.screenshot(path=str(SHOTS / 'summary-801.png'), full_page=False)
        result = {
            'tag': summary.evaluate('el => el.tagName'),
            'cursor': summary.evaluate("el => getComputedStyle(el).cursor"),
            'tabindex': summary.evaluate('el => el.getAttribute("tabindex")'),
            'text_before': before,
            'text_after': summary.inner_text(),
            'tiles_visible_after_click': page.locator('[data-verse-tiles]').is_visible(),
            'buttons_in_summary': summary.evaluate('el => el.querySelectorAll("button,a,input").length'),
        }
        # a drag still writes the preview into the summary line
        tiles = page.locator('.editor__verse-tile')
        box = tiles.nth(0).bounding_box()
        page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        page.mouse.down()
        third = tiles.nth(2).bounding_box()
        page.mouse.move(third['x'] + third['width'] / 2, third['y'] + third['height'] / 2)
        page.wait_for_timeout(120)
        result['drag_preview'] = summary.inner_text()
        page.mouse.up()
        page.wait_for_timeout(120)
        result['after_release'] = summary.inner_text()
        print(json.dumps(result))
        browser.close()


if __name__ == '__main__':
    main()
