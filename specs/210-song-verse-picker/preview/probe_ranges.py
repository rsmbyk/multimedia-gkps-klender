"""Read the live page's printed verse references (modal summary + entry Bait lines)."""
import json
import os
from playwright.sync_api import sync_playwright

URL = os.environ.get('SLICE_URL', 'http://127.0.0.1:8765/tatib/151/')


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(URL)
        page.wait_for_load_state('networkidle')
        print('PAGE', json.dumps(page.evaluate("""() => ({
          rows: [...document.querySelectorAll('#chList .songrow__verses')].map(e => e.textContent),
          stage: [...document.querySelectorAll('.read__sub')].map(e => e.textContent),
        })"""), indent=1))
        page.evaluate("document.querySelector('[data-entry-open=\"song\"]').click()")
        page.wait_for_selector('dialog[open] #entry-song-search')
        page.locator('#entry-song-search').fill('HAL')
        page.wait_for_selector('#entry-song-options [data-song]')
        page.locator('#entry-song-options [data-song]').first.click()
        page.wait_for_selector('.editor__verse-tile')
        summary = page.locator('[data-verses-summary]')
        out = {'fresh': summary.inner_text()}
        page.locator('.editor__verse-tile').nth(1).click()
        out['pair'] = summary.inner_text()
        tiles = page.locator('.editor__verse-tile')
        a = tiles.nth(0).bounding_box()
        b = tiles.nth(2).bounding_box()
        page.mouse.move(a['x'] + a['width'] / 2, a['y'] + a['height'] / 2)
        page.mouse.down()
        page.mouse.move(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2)
        page.wait_for_timeout(120)
        out['drag_preview'] = summary.inner_text()
        page.mouse.up()
        page.wait_for_timeout(150)
        out['after_release'] = summary.inner_text()
        page.locator('[data-verse-all]').click()
        out['all'] = summary.inner_text()
        print('MODAL', json.dumps(out, indent=1))
        browser.close()


if __name__ == '__main__':
    main()
