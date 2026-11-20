"""FR-003 / US1-AC6: the keyboard open path resets too.

The picker's `Enter` opens the marked row through the same `openService` path a click uses.
This drives it with real keys: mark a row, Enter, expand a block by hand, back to the picker,
mark another row, Enter — and reads back what is painted.

    .venv/bin/python specs/204-dock-entry-open-reset/preview/probe_enter_path.py [url]
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8899/index.html'
OPEN_BLOCKS = """() => [...document.querySelectorAll('#entryList .entryli')]
    .filter(li => {const i = li.querySelector('.entryinner');
                   return i && i.classList.contains('is-open');})
    .map(li => Number(li.dataset.index))"""
CURSOR = "() => (document.querySelector('.servicerow.is-cursor') || {}).dataset?.service || null"
VIEW = "() => document.getElementById('dockPanel').dataset.view"

out = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for behaviour in ('drafted', 'today'):
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900},
                                  color_scheme='dark', device_scale_factor=1)
        page = ctx.new_page()
        page.goto(URL + '?behaviour=' + behaviour)
        page.wait_for_selector('.servicerow.is-cursor')
        page.wait_for_timeout(300)
        # walk the picker to service 155 with the dock's own keys, then Enter
        for _ in range(12):
            if page.evaluate(CURSOR) == '155':
                break
            page.keyboard.press('ArrowDown')
            page.wait_for_timeout(120)
        marked = page.evaluate(CURSOR)
        page.keyboard.press('Enter')
        page.wait_for_function("() => document.getElementById('dockPanel').dataset.view === 'run'")
        page.wait_for_timeout(800)
        page.locator('.entryli[data-index="3"] .entryrow').click()
        page.wait_for_timeout(500)
        after_expand = page.evaluate(OPEN_BLOCKS)
        # back to the picker (Esc hold is the dock's own exit; the head control is the pointer one)
        page.locator('#switchBtn').click()
        page.wait_for_selector('#viewPick.is-active')
        page.wait_for_timeout(300)
        for _ in range(12):
            if page.evaluate(CURSOR) == '149':
                break
            page.keyboard.press('ArrowDown')
            page.wait_for_timeout(120)
        page.keyboard.press('Enter')
        page.wait_for_function("() => document.getElementById('dockPanel').dataset.view === 'run'")
        page.wait_for_timeout(800)
        record = {'behaviour': behaviour, 'marked_first': marked,
                  'open_after_expand': after_expand,
                  'open_after_enter_on_149': page.evaluate(OPEN_BLOCKS)}
        out.append(record)
        print(behaviour, json.dumps(record))
        page.screenshot(path=os.path.join(HERE, 'shots', f'{behaviour}-15-enter-path.png'))
        ctx.close()
    browser.close()

with open(os.path.join(HERE, 'measurements-enter.json'), 'w', encoding='utf-8') as handle:
    json.dump({'url': URL, 'results': out}, handle, indent=1)
print('wrote measurements-enter.json')
