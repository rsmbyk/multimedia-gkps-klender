"""Measure the Add/Edit verse handlers after a sidebar navigation (spec 230).

Run from any checkout with the two servers up:
    .venv/bin/python specs/230-song-verse-script-boot/preview/probe.py

The before server is the unmodified app; the after server is this slice's worktree.
Both URLs are arguments so the probe stays useful after the ports move.
"""
import sys
from playwright.sync_api import sync_playwright

CASES = [
    ('before', sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:63404'),
    ('after', sys.argv[2] if len(sys.argv) > 2 else 'http://127.0.0.1:8771'),
]
SONG = '/songs/1387/'
BOOK = '/songs/book/18/'
SONG_LINK = '/songs/1387/'


def title(page):
    locator = page.locator('#editorContent .editor__title')
    return locator.inner_text() if locator.count() else '-'


def run(page, base, label):
    page.goto(base + '/', wait_until='networkidle')
    home_scripts = page.evaluate(
        "document.querySelectorAll('script[src*=songs_verse]').length")
    page.locator('a[href="/songs/"]').first.click()
    page.wait_for_timeout(600)
    page.locator('#panelBody a[href="%s"]' % BOOK).first.click()
    page.wait_for_timeout(600)
    page.locator('#chList a[href="%s"]' % SONG_LINK).first.click()
    page.wait_for_timeout(800)
    url = page.url
    btn = page.locator('[data-add-verse]').first
    box = btn.bounding_box()
    scripts = page.evaluate(
        "document.querySelectorAll('script[src*=songs_verse]').length")
    btn.click()
    opened = False
    try:
        page.wait_for_selector('#editorModal[open]', timeout=3000)
        opened = True
    except Exception:
        pass
    resources = page.evaluate(
        "performance.getEntriesByType('resource')"
        ".filter(e => e.name.indexOf('songs_verse.js') !== -1)"
        ".map(e => Math.round(e.responseEnd))")
    print(f'{label}: url={url} home_script_tags={home_scripts} '
          f'page_script_tags={scripts} button={box}')
    print(f'{label}: add_dialog_open={opened} title={title(page)!r} '
          f'song_js_loaded_at_ms={resources}')

    page.evaluate('document.getElementById("editorModal").close()')
    page.locator('[data-verse-edit]').first.evaluate('el => el.click()')
    edit_open = False
    try:
        page.wait_for_selector('#editorModal[open]', timeout=3000)
        edit_open = True
    except Exception:
        pass
    print(f'{label}: edit_dialog_open={edit_open} title={title(page)!r}')

    page.goto(base + SONG, wait_until='networkidle')
    page.locator('[data-add-verse]').first.click()
    page.wait_for_timeout(700)
    print(f'{label}: direct_load_dialog_open='
          f'{page.locator("#editorModal").evaluate("el => el.open")}')


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for label, base in CASES:
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        run(page, base, label)
        print(f'{label}: page_errors={errors}')
        page.close()
    browser.close()
