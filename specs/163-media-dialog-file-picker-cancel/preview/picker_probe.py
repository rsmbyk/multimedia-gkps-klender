"""Probe the New media dialog's dismissal behaviour on a running server (spec 163).

    ../multimedia-gkps-klender/.venv/bin/python specs/163-media-dialog-file-picker-cancel/preview/picker_probe.py \
        --url http://localhost:8814/tatib/149/

Send what a browser sends at the file input when the person closes the picker without choosing
(`cancel`, bubbling, not cancelable) and report whether the dialog survives it. Exits 0 when the
dialog stays open and its own Escape still closes it; exits 1 otherwise.

`--url` must name a port the media companion admits (`GKPS_MEDIA_ALLOWED_ORIGINS`); `8814` is in the
local list, `8768` is not.
"""
import argparse
import os
import struct
import sys
import tempfile
import zlib

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sys.exit('playwright is not installed in the interpreter this script runs on')

OPEN_MEDIA = """() => {
  const all = [...document.querySelectorAll('[data-entry-open="media"]')];
  const visible = all.find(el => { const r = el.getBoundingClientRect(); return r.width > 4 && r.height > 4; });
  (visible || all[0]).click();
}"""


def write_png(path):
    """A real 4x4 PNG — the companion sniffs magic bytes when a file is chosen."""
    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data
                + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF))
    raw = b''.join(b'\x00' + bytes([200, 60, 40]) * 4 for _ in range(4))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'
                     + chunk(b'IHDR', struct.pack('>IIBBBBB', 4, 4, 8, 2, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(raw))
                     + chunk(b'IEND', b''))


def open_media_form(page):
    page.evaluate(OPEN_MEDIA)
    page.wait_for_selector('#editorModal form[data-entry-form="media"]', timeout=10000)
    page.wait_for_timeout(300)


def dialog_state(page):
    return page.evaluate("""() => {
      const dialog = document.getElementById('editorModal');
      const form = dialog.querySelector('form[data-media-create]');
      return {
        open: dialog.open,
        formInPage: !!form,
        title: form ? form.querySelector('[name="title"]').value : null,
        saveDisabled: form ? form.querySelector('.editor__save').disabled : null,
        shownName: form ? form.querySelector('[data-media-selected-name]').textContent : null,
      };
    }""")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://localhost:8814/tatib/149/')
    parser.add_argument('--png')
    options = parser.parse_args()
    if not options.png:
        options.png = os.path.join(tempfile.mkdtemp(), 'swatch.png')
    write_png(__import__('pathlib').Path(options.png))
    failures = []

    with sync_playwright() as play:
        browser = play.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(options.url, wait_until='load')

        # 1 — the picker dismissed, nothing chosen
        open_media_form(page)
        page.evaluate("""() => {
          document.querySelector('#editorModal form[data-media-create] [name="title"]').value = 'Closing hymn';
          document.querySelector('#editorModal input[type=file]')
            .dispatchEvent(new Event('cancel', { bubbles: true }));
        }""")
        page.wait_for_timeout(400)
        state = dialog_state(page)
        print('picker dismissed, nothing chosen:', state)
        if not (state['open'] and state['formInPage'] and state['title'] == 'Closing hymn'
                and state['saveDisabled']):
            failures.append('the dialog did not keep its form, title and Save state')

        # 2 — a file chosen, then the picker dismissed again
        if not page.locator('#editorModal').evaluate('dialog => dialog.open'):
            open_media_form(page)      # a build that fails case 1 left no form to work with
        page.set_input_files('input[data-media-file]', options.png)
        page.wait_for_timeout(1200)
        chosen = dialog_state(page)
        print('a file chosen:', chosen)
        page.evaluate("""() => document.querySelector('#editorModal input[type=file]')
            .dispatchEvent(new Event('cancel', { bubbles: true }))""")
        page.wait_for_timeout(400)
        kept = dialog_state(page)
        print('picker dismissed with a file chosen:', kept)
        if not (kept['open'] and kept['shownName'] == chosen['shownName']
                and kept['saveDisabled'] == chosen['saveDisabled']):
            failures.append('the chosen file did not survive the dismissal')

        # 3 — the dialog's own Escape must still close it
        page.locator('#editorModal').press('Escape')
        page.wait_for_timeout(400)
        closed = dialog_state(page)
        print('Escape on the dialog itself:', closed)
        if closed['open']:
            failures.append('Escape no longer closes the dialog')

        browser.close()

    if failures:
        print('FAIL — ' + '; '.join(failures))
        return 1
    print('OK — a dismissed picker leaves the dialog, its title and its file; Escape still closes it')
    return 0


if __name__ == '__main__':
    sys.exit(main())
