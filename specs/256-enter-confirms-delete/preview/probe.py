"""Probe the spec-256 live preview: what does Enter do on each delete confirm?

Usage: python probe.py <tag>
Writes one compact JSON object per surface to probe-results-<tag>.jsonl.
Each case opens the real confirmation on the live worktree, moves focus away
from the destructive control, presses Enter once and records what happened.
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8768'
HERE = Path(__file__).resolve().parent
TAG = sys.argv[1] if len(sys.argv) > 1 else 'before'


def record(page, surface, extra):
    row = {
        'surface': surface,
        'tag': TAG,
        'requests': page._gkps_requests,
    }
    row.update(extra)
    with (HERE / f'probe-results-{TAG}.jsonl').open('a') as handle:
        handle.write(json.dumps(row, separators=(',', ':')) + '\n')
    print(json.dumps(row, separators=(',', ':')))


def watch(page):
    page._gkps_requests = []
    def on_request(request):
        if request.method != 'GET':
            page._gkps_requests.append(
                {'method': request.method, 'url': request.url.replace(BASE, '')})
    if getattr(page, '_gkps_watcher', None):
        page.remove_listener('request', page._gkps_watcher)
    page._gkps_watcher = on_request
    page.on('request', on_request)


def press_with_focus_away(page):
    active_before = page.evaluate(
        "() => document.activeElement ? document.activeElement.tagName + '#' + document.activeElement.id : 'none'")
    page.evaluate('() => { if (document.activeElement) document.activeElement.blur(); }')
    page.keyboard.press('Enter')
    page.wait_for_timeout(700)
    return active_before


def probe_entry(page):
    page.goto(BASE + '/')
    page.locator('[data-panel="tatib"]').click()
    page.wait_for_selector('.book[href*="/tatib/"]')
    page.locator('.book[href*="/tatib/"]').first.click()
    page.wait_for_selector('.tatib__item')
    before = page.locator('.tatib__item').count()
    page.locator('.tatib__item').first.hover()
    page.locator('[data-entry-delete]').first.click(force=True)
    page.wait_for_selector('#editorModal [data-confirm-delete]')
    watch(page)
    active_before = press_with_focus_away(page)
    record(page, 'entry-delete', {
        'active_before': active_before,
        'dialog_open': page.evaluate("() => !!document.querySelector('dialog[open]')"),
        'confirm_visible': page.locator('#editorModal [data-confirm-delete]').count() > 0,
        'rows_before': before,
        'rows_after': page.locator('.tatib__item').count(),
    })


def probe_sidebar(page):
    page.goto(BASE + '/')
    page.locator('[data-panel="tatib"]').click()
    page.locator('.book[href*="/tatib/"]').first.hover()
    page.locator('[data-editor-delete="tatib"]').first.click()
    page.wait_for_selector('#editorModal [data-editor-delete-form]')
    watch(page)
    active_before = press_with_focus_away(page)
    record(page, 'sidebar-delete', {
        'active_before': active_before,
        'confirm_visible': page.locator('#editorModal [data-editor-delete-form]').count() > 0,
        'dialog_open': page.locator('#editorModal').evaluate('e => e.open'),
    })


def probe_verse(page):
    page.goto(BASE + '/')
    page.locator('[data-panel="kidung"]').click()
    page.locator('.book[data-name]', has_text='Lagu Lain').click()
    page.locator('.songrow', has_text='Editable song').click()
    page.wait_for_selector('[data-verse-edit]')
    page.locator('[data-verse-edit]').first.dispatch_event('click')
    page.wait_for_selector('#editorContent [data-verse-delete]')
    page.locator('#editorContent [data-verse-delete]').first.dispatch_event('click')
    page.wait_for_selector('#editorModal [data-confirm-delete]')
    watch(page)
    active_before = press_with_focus_away(page)
    record(page, 'verse-delete', {
        'active_before': active_before,
        'confirm_visible': page.locator('#editorModal [data-confirm-delete]').count() > 0,
        'dialog_open': page.locator('#editorModal').evaluate('e => e.open'),
    })


def probe_media_remove(page):
    page.goto(BASE + '/media-library/')
    page.evaluate("""() => {
        window.__removeClicks = 0;
        document.getElementById('mediaConfirmRemove')
          .addEventListener('click', () => { window.__removeClicks += 1; });
        document.getElementById('mediaRemoveDialog').showModal();
    }""")
    watch(page)
    active_before = press_with_focus_away(page)
    record(page, 'media-remove', {
        'active_before': active_before,
        'remove_clicks': page.evaluate('() => window.__removeClicks'),
        'dialog_open': page.locator('#mediaRemoveDialog').evaluate('e => e.open'),
    })


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                color_scheme='dark', device_scale_factor=1)
        for name, fn in (
            ('entry-delete', probe_entry),
            ('sidebar-delete', probe_sidebar),
            ('verse-delete', probe_verse),
            ('media-remove', probe_media_remove),
        ):
            try:
                fn(page)
            except Exception as error:
                with (HERE / f'probe-results-{TAG}.jsonl').open('a') as handle:
                    handle.write(json.dumps(
                        {'surface': name, 'tag': TAG, 'error': str(error)},
                        separators=(',', ':')) + '\n')
                print(name, 'ERROR', error)
        browser.close()


if __name__ == '__main__':
    main()
