"""Measure the create-a-template destination on base and slice servers (spec 234).

    .venv/bin/python probe.py http://127.0.0.1:8775 http://127.0.0.1:8774

Both servers point at the same dedicated database, so the records they create are
equivalent. The probe drives the real sidebar create form in a 1440x900 Chromium tab.
"""
import json
import sys
import time
from playwright.sync_api import sync_playwright

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8775'
SLICE_URL = sys.argv[2] if len(sys.argv) > 2 else 'http://127.0.0.1:8774'

STATE_JS = """() => ({
  path: location.pathname + location.search,
  name: document.getElementById('readName')?.textContent || '',
  current: document.querySelector('#panelBody a.book[aria-current="true"]')
    ?.getAttribute('data-name') || null,
  nav: document.documentElement.dataset.nav || '',
  ch: document.documentElement.dataset.ch || '',
  mode_pressed: document.getElementById('tatibMode')?.getAttribute('aria-pressed') || '',
  empty: !!document.querySelector('.entry__empty-title'),
  marker: window.__gkps234 || null,
  timeOrigin: performance.timeOrigin,
  focus_name: document.activeElement?.getAttribute('data-name') || null,
  focus_class: document.activeElement?.className || ''
})"""


def state(page):
    return page.evaluate(STATE_JS)


def create(page, base, case, label, start='/tatib/'):
    suffix = str(int(time.time() * 1000))[-6:]
    name = f'Probe {label} {case} {suffix}'
    page.goto(base + start, wait_until='networkidle')
    page.evaluate("window.__gkps234 = 'alive'")
    before = state(page)
    page.click('#panelAdd')
    page.wait_for_selector('#editorContent .editor__form')
    if case.startswith('template'):
        page.click('#editorContent [data-tatib-kind="1"]')
        page.wait_for_function(
            "document.querySelector('#editorContent .editor__date-field')?.hidden === true")
    page.fill('#editorContent input[name="name"]', name)
    page.click('#editorContent .editor__save')
    page.wait_for_function("!document.querySelector('dialog[open]')", timeout=8000)
    page.wait_for_timeout(800)
    after = state(page)
    print(json.dumps({'server': label, 'case': case, 'start': start, 'name': name,
                      'before': before, 'after': after}))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for label, base in [('before', BASE_URL), ('after', SLICE_URL)]:
        page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                color_scheme='dark')
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        for case, start in [('template', '/tatib/'),
                            ('template_from_template_list', '/tatib/?mode=template'),
                            ('dated', '/tatib/')]:
            try:
                create(page, base, case, label, start)
            except Exception as exc:
                print(json.dumps({'server': label, 'case': case, 'error': str(exc)}))
        print(json.dumps({'server': label, 'page_errors': errors}))
        page.close()
    browser.close()
