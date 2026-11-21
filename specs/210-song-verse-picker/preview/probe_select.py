"""Check select-on-focus on the live song search."""
import json
import os
from playwright.sync_api import sync_playwright

URL = os.environ.get('SLICE_URL', 'http://127.0.0.1:8765/tatib/151/')


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
        search = page.locator('#entry-song-search')
        before = search.input_value()
        page.locator('#editorTitle').click()
        search.click()
        page.wait_for_timeout(150)
        sel = search.evaluate("el => ({s: el.selectionStart, e: el.selectionEnd, n: el.value.length})")
        page.keyboard.type('HAL 4')
        typed = search.input_value()
        # a second click while already focused must not re-select everything
        search.click()
        page.keyboard.press('End')
        page.keyboard.type('x')
        appended = search.input_value()
        print(json.dumps({'before': before, 'selection': sel, 'typed': typed,
                          'after_caret_type': appended}, indent=1))
        browser.close()


if __name__ == '__main__':
    main()
