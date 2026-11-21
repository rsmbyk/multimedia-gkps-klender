"""Inspect the Add song modal after a Save with no verses ticked.

Run: ~/Projects/multimedia-gkps-klender/.venv/bin/python probe_error.py
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
        page.locator('[data-verse-clear]').click()
        page.wait_for_timeout(300)
        page.screenshot(path=str(SHOTS / 'error-before-save.png'), full_page=False)
        page.get_by_role('button', name='Save', exact=True).click()
        page.wait_for_timeout(2500)
        page.screenshot(path=str(SHOTS / 'error-after-save.png'), full_page=False)
        result = page.evaluate("""() => {
          const r = el => { const b = el.getBoundingClientRect();
            return { top: Math.round(b.top), bottom: Math.round(b.bottom),
                     left: Math.round(b.left), width: Math.round(b.width),
                     height: Math.round(b.height) }; };
          const dialog = document.querySelector('dialog[open]');
          const panel = dialog && dialog.querySelector('[data-verse-panel]');
          const inner = dialog && dialog.querySelector('.editor__verse-panel-inner');
          const tiles = [...(dialog ? dialog.querySelectorAll('.editor__verse-tile') : [])];
          const summary = dialog && dialog.querySelector('[data-verses-summary]');
          const errors = [...(dialog ? dialog.querySelectorAll('.editor__error') : [])];
          return {
            dialogOpen: !!dialog,
            panelDisplay: panel ? getComputedStyle(panel).display : null,
            panel: panel ? r(panel) : null,
            settled: panel ? panel.dataset.settled : null,
            hidden: panel ? panel.hidden : null,
            inner: inner ? r(inner) : null,
            innerOverflow: inner ? getComputedStyle(inner).overflow : null,
            tiles: tiles.map(r),
            summary: summary ? { tag: summary.tagName, text: summary.textContent,
                                 colour: getComputedStyle(summary).color } : null,
            errors: errors.map(e => ({ text: e.textContent.trim(), box: r(e),
                                       parent: e.parentElement.className })),
            copyCount: (dialog ? dialog.innerText : '').split('keep at least one').length - 1,
            contentScrollTop: dialog ? dialog.querySelector('.editor__content').scrollTop : null,
            contentScrollHeight: dialog ? dialog.querySelector('.editor__content').scrollHeight : null,
            contentHeight: dialog ? dialog.querySelector('.editor__content').clientHeight : null,
          };
        }""")
        html = page.evaluate("""() => document.querySelector('dialog[open] .editor__verse-panel').outerHTML""")
        result['panel_html'] = html[:1200]
        print(json.dumps(result, indent=1))
        browser.close()


if __name__ == '__main__':
    main()
