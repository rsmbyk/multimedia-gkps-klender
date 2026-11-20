"""Gate-1 reproduction for spec 209: a sidebar create leaves the stage where it was.

Run with the repository's venv and the compose web service on 127.0.0.1:63404:
    .venv/bin/python specs/209-open-created-service/reproduce.py

The script creates one dated service, reads the stage before the save, after the save and after a
manual click of the new row, then prints the three snapshots as JSON. On the base commit the
"after_save" snapshot still has url=/tatib/, an empty #readName and no aria-current row; the
"after_click" snapshot is the state the slice wants immediately after the save.
"""
import json
import sys
import time
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:63404'
NAME = 'Spec 209 reproduce %s' % int(time.time())

SNAPSHOT = """() => ({
  url: location.pathname + location.search,
  stage: document.getElementById('readName')?.textContent,
  current: document.querySelector('#panelBody .book[aria-current="true"]')?.getAttribute('data-name'),
  nav: document.documentElement.dataset.nav,
  ch: document.documentElement.dataset.ch,
  marker: window.__reproduceMarker || null,
  createdHref: Array.from(document.querySelectorAll('#panelBody .book'))
    .find(a => a.textContent.includes(NAME))?.getAttribute('href') || null,
  empty: !!document.querySelector('.entry__empty-title')
})"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(BASE + '/tatib/', wait_until='networkidle')
    page.evaluate("name => { window.__reproduceMarker = 'set-before-save'; window.__name = name; }", NAME)
    before = page.evaluate(SNAPSHOT.replace('NAME', 'window.__name'))
    page.click('#panelAdd')
    page.wait_for_selector('#editorContent input[name="name"]')
    page.fill('#editorContent input[name="name"]', NAME)
    page.click('#editorContent .editor__save')
    page.wait_for_function(
        "name => !!Array.from(document.querySelectorAll('#panelBody .book'))"
        ".find(a => a.textContent.includes(name))", arg=NAME)
    page.wait_for_timeout(700)
    after_save = page.evaluate(SNAPSHOT.replace('NAME', 'window.__name'))
    page.click('#panelBody .book:has-text("%s")' % NAME)
    page.wait_for_timeout(700)
    after_click = page.evaluate(SNAPSHOT.replace('NAME', 'window.__name'))
    print(json.dumps({'before': before, 'after_save': after_save,
                      'after_click': after_click}, indent=2))
    browser.close()
