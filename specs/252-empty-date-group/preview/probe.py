"""Measure the spec-252 preview against the real served code path.

Run with the project venv while serve.py is running on port 8776. Every state is
reached by hand-equivalent clicks on the live Django page; output is one compact
JSON object per line beside this script.
"""

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import serve  # noqa: E402  (path prepared above)

serve.prepare_env()

# Seeding runs in its own process so Playwright's event loop never touches the ORM.
def reseed():
    subprocess.check_call([sys.executable, str(HERE / 'reseed.py')])

from playwright.sync_api import sync_playwright  # noqa: E402

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8776'
OUT = HERE / ('probe-results-base.jsonl' if ':8777' in BASE else 'probe-results.jsonl')
ROWS = []


def record(case, state, values):
    row = {'case': case, 'state': state, **values}
    ROWS.append(row)
    print(json.dumps(row, separators=(',', ':')))


def counts(page):
    return page.evaluate("""() => ({
      recent: document.querySelectorAll('#panelBody section.group[data-bucket="last-30-days"]').length,
      older: document.querySelectorAll('#panelBody section.group[data-bucket="earlier-this-year"]').length,
      allGroups: document.querySelectorAll('#panelBody section.group').length,
      headings: [...document.querySelectorAll('#panelBody .group__head')].map(h => h.textContent.trim()),
      visibleBooks: [...document.querySelectorAll('#panelBody .book')].filter(
        a => getComputedStyle(a.closest('li')).display !== 'none' && !a.closest('.is-hidden')).length
    })""")


def delete(page, scope, kind, pk):
    button = page.locator(
        f'{scope} button[data-editor-delete="{kind}"][data-editor-id="{pk}"]')
    button.locator('xpath=..').hover()
    button.click()
    page.locator('#editorModal [data-editor-delete-form] button[type="submit"]').click()
    page.wait_for_function("!document.querySelector('dialog[open]')", timeout=10000)
    page.wait_for_timeout(120)


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                device_scale_factor=1, color_scheme='dark')

        # Case 1 — services sidebar date bucket.
        reseed()
        page.goto(BASE + '/tatib/', wait_until='networkidle')
        record('date-bucket', 'before', counts(page))
        for pk in page.evaluate("""() => [...document.querySelectorAll(
          '#panelBody section.group[data-bucket="last-30-days"] .book')].map(a => a.dataset.name)"""):
            delete(page, '#panelBody section.group[data-bucket="last-30-days"]', 'tatib', pk)
        record('date-bucket', 'after-last-delete', counts(page))
        page.reload(wait_until='networkidle')
        record('date-bucket', 'after-reload', counts(page))

        # Case 2 — template group.
        reseed()
        page.goto(BASE + '/tatib/?mode=template', wait_until='networkidle')
        record('templates', 'before', counts(page))
        for pk in page.evaluate("""() => [...document.querySelectorAll(
          '#panelBody .book')].map(a => a.dataset.name)"""):
            delete(page, '#panelBody', 'template', pk)
        record('templates', 'after-last-delete', counts(page))
        page.reload(wait_until='networkidle')
        record('templates', 'after-reload', counts(page))

        # Case 3 — unheaded songbook groups.
        reseed()
        page.goto(BASE + '/songs/', wait_until='networkidle')
        record('songbooks', 'before', counts(page))
        ordinary = page.evaluate("""() => {
          const li = [...document.querySelectorAll('#panelBody li')].find(
            li => li.querySelector('button[data-editor-delete="songbook"]'));
          return li ? li.querySelector('.book').dataset.name : null;
        }""")
        delete(page, '#panelBody', 'songbook', ordinary)
        record('songbooks', 'after-last-delete', counts(page))

        # Case 4 — filter hides the surviving rows of a bucket.
        reseed()
        page.goto(BASE + '/tatib/', wait_until='networkidle')
        page.fill('#bookFilter', 'Alpha')
        page.wait_for_timeout(120)
        record('filtered', 'filter-on', counts(page) | {
            'bucketHidden': page.evaluate("""() => document.querySelector(
              '#panelBody section.group[data-bucket="last-30-days"]').classList.contains('is-hidden')""")})
        first = page.evaluate("""() => [...document.querySelectorAll(
          '#panelBody section.group[data-bucket="last-30-days"] .book')].find(
          a => a.dataset.name && a.textContent.includes('Alpha')).dataset.name""")
        delete(page, '#panelBody section.group[data-bucket="last-30-days"]', 'tatib', first)
        record('filtered', 'after-visible-delete', counts(page) | {
            'bucketHidden': page.evaluate("""() => document.querySelector(
              '#panelBody section.group[data-bucket="last-30-days"]').classList.contains('is-hidden')""")})
        page.fill('#bookFilter', '')
        page.wait_for_timeout(120)
        record('filtered', 'filter-cleared', counts(page) | {
            'bucketHidden': page.evaluate("""() => document.querySelector(
              '#panelBody section.group[data-bucket="last-30-days"]').classList.contains('is-hidden')""")})
        browser.close()

    OUT.write_text('\n'.join(json.dumps(row, separators=(',', ':')) for row in ROWS) + '\n')


if __name__ == '__main__':
    main()
