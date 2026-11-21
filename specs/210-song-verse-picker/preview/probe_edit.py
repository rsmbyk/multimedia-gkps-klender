"""Check how an existing song entry's Edit form renders its verse tiles."""
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
        rows = page.locator('.tatib__item--entry')
        print('rows', rows.count())
        for index in range(rows.count()):
            row = rows.nth(index)
            row.hover()
            control = row.locator('[data-entry-edit]')
            if control.count():
                control.first.click(force=True)
                break
        page.wait_for_selector('dialog[open]', timeout=5000)
        page.wait_for_timeout(1200)
        result = page.evaluate("""() => {
          const box = document.querySelector('dialog[open] #entry-verses');
          if (!box) return { noBox: true };
          const kids = [...box.children];
          return {
            opened: true,
            title: document.querySelector('dialog[open] #editorTitle').textContent.trim(),
            mode: document.querySelector('dialog[open] .editor__form').dataset.entryMode,
            active: document.activeElement ? (document.activeElement.id || document.activeElement.className) : null,
            menuHidden: document.querySelector('dialog[open] #entry-song-menu').hidden,
            numbers: [...box.querySelectorAll('.editor__verse-tile')].map(t => t.textContent.trim()),
            checked: [...box.querySelectorAll('.editor__verse-tile')]
              .filter(t => t.querySelector('input:checked')).map(t => t.textContent.trim()),
            kidTags: kids.map(k => k.tagName + (k.id ? '#' + k.id : '')),
            optionDivs: box.querySelectorAll('div > div').length,
            labelledTiles: box.querySelectorAll('label.editor__verse-tile').length,
            plainLabels: box.querySelectorAll('label:not(.editor__verse-tile)').length,
            checks: box.querySelectorAll('input[type=checkbox]').length,
            gridColumns: getComputedStyle(box).gridTemplateColumns,
            firstLabelWidth: box.querySelector('label') ? Math.round(box.querySelector('label').getBoundingClientRect().width) : null,
          };
        }""")
        print(json.dumps(result))
        browser.close()


if __name__ == '__main__':
    main()
