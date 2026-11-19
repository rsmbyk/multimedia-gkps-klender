"""SC-006 / FR-005: an open writes nothing and animates nothing.

Three read-backs per open, on both behaviours:
  * the stored display state's BYTES before and after the open (must be identical),
  * the display channel's messages during the open (must be none),
  * `.entryinner.is-morph` in the new list and `runBody.scrollTop` sampled across it
    (the list paints shut; no collapse morph, no scroll jump).

    .venv/bin/python specs/204-dock-entry-open-reset/preview/probe_open_write.py [url]
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8899/index.html'
RAW = "() => localStorage.getItem('gkps-display') || 'null'"
MORPH = "() => [...document.querySelectorAll('#entryList .entryinner.is-morph')].map(e => e.id)"
OPEN_BLOCKS = """() => [...document.querySelectorAll('#entryList .entryli')]
    .filter(li => {const i = li.querySelector('.entryinner');
                   return i && i.classList.contains('is-open');})
    .map(li => Number(li.dataset.index))"""

out = []


def settle(p, ms=800):
    p.wait_for_timeout(ms)


def open_service(p, sid):
    if p.evaluate("() => document.getElementById('dockPanel').dataset.view") != 'pick':
        p.locator('#switchBtn').click()
        p.wait_for_selector('#viewPick.is-active')
        settle(p, 300)
    before = p.evaluate(RAW)
    p.evaluate("() => {window.__msgs = [];}")
    p.locator(f'.servicerow[data-service="{sid}"]').first.click()
    p.wait_for_function("() => document.getElementById('dockPanel').dataset.view === 'run'")
    samples = p.evaluate("""() => new Promise(res => {
        const out = []; const t0 = performance.now();
        const body = document.getElementById('runBody');
        function tick() {
            out.push([Math.round(performance.now() - t0), Math.round(body.scrollTop),
                      document.querySelectorAll('#entryList .entryinner.is-morph').length]);
            if (performance.now() - t0 < 700) requestAnimationFrame(tick); else res(out);
        }
        requestAnimationFrame(tick);
    })""")
    settle(p, 300)
    after = p.evaluate(RAW)
    msgs = p.evaluate("() => window.__msgs")
    record = {'opened': sid, 'bytes_before': before, 'bytes_after': after,
              'bytes_identical': before == after, 'channel_messages': msgs,
              'morph_ids': p.evaluate(MORPH), 'open_blocks': p.evaluate(OPEN_BLOCKS),
              'scroll_samples': samples[::6],
              'scroll_max': max(s[1] for s in samples),
              'morph_frames': sum(1 for s in samples if s[2] > 0)}
    out.append(record)
    print(f'open {sid}: bytes identical={record["bytes_identical"]} '
          f'channel msgs={len(msgs)} morph ids={record["morph_ids"]} '
          f'morph frames={record["morph_frames"]} scroll max={record["scroll_max"]} '
          f'open blocks={record["open_blocks"]}')
    return record


with sync_playwright() as p:
    browser = p.chromium.launch()
    for behaviour in ('drafted', 'today'):
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900},
                                  color_scheme='dark', device_scale_factor=1)
        page = ctx.new_page()
        page.goto(URL + '?behaviour=' + behaviour)
        page.wait_for_selector('.servicerow')
        page.evaluate("""() => {
            window.__msgs = [];
            const c = new BroadcastChannel('gkps-service-display');
            c.onmessage = e => window.__msgs.push(e.data);
        }""")
        settle(page, 300)
        print(f'\n===== {behaviour} =====')
        open_service(page, '155')
        page.locator('.entryli[data-index="3"] .entryrow').click()
        settle(page)
        open_service(page, '149')                     # the reported leak, measured for writes
        open_service(page, '155')
        # put an entry on air, then open services: the open must not touch the state
        inner = page.locator('#entryinner-3')
        if not inner.evaluate("el => el.classList.contains('is-open')"):
            page.locator('.entryli[data-index="3"] .entryrow').click()
            settle(page)
        row = page.locator('.entryli[data-index="3"] .screenerow').first
        row.scroll_into_view_if_needed()
        settle(page, 150)
        row.click()
        settle(page, 900)
        print('on air:', page.evaluate(RAW))
        open_service(page, '149')
        open_service(page, '155')
        ctx.close()
    browser.close()

path = os.path.join(HERE, 'measurements-open-write.json')
with open(path, 'w', encoding='utf-8') as handle:
    json.dump({'url': URL, 'opens': out}, handle, ensure_ascii=False, indent=1)
print('\nwrote', path, 'with', len(out), 'opens')
