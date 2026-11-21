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
        opened = page.evaluate("""() => {
          const row = document.querySelector('.tatib__item--entry[data-entry-kind="song"]')
            || [...document.querySelectorAll('.tatib__item--entry')].find(el => el.dataset.entryKind === 'song');
          if (!row) return false;
          const edit = row.querySelector('[data-entry-edit]') || row.querySelector('.row-edit');
          if (!edit) return false;
          edit.click();
          return true;
        }""")
        page.wait_for_timeout(1800)
        result = page.evaluate("""() => {
          const box = document.querySelector('dialog[open] #entry-verses');
          if (!box) return { noBox: true };
          const kids = [...box.children];
          return {
            opened: true,
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
