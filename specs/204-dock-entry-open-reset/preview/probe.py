"""Exercise every state of the spec 204 preview and read back what is PAINTED.

One run walks both behaviours (drafted / today) through the reported sequence and the
states the slice must not disturb, writes shots/ and measurements.json, and prints a
table. Nothing is asserted from a state variable: every number is the DOM's own
(aria-expanded, is-open, the inner's measured box height).

    .venv/bin/python specs/204-dock-entry-open-reset/preview/probe.py [url]

`url` defaults to the built index.html over file://. Pass an http:// URL (any static
file server) to compare the browser's cookie behaviour for the reload state.
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[1] if len(sys.argv) > 1 else 'file://' + os.path.join(HERE, 'index.html')
SHOTS = os.path.join(HERE, 'shots')
os.makedirs(SHOTS, exist_ok=True)

ROWS_JS = """() => [...document.querySelectorAll('#entryList .entryli')].map(li => {
    const row = li.querySelector('.entryrow');
    const inner = li.querySelector('.entryinner');
    const title = row && row.querySelector('.entryrow__t');
    return {index: Number(li.dataset.index),
            label: ((title ? title.textContent : (row ? row.textContent : '')) || '')
                     .trim().replace(/\\s+/g, ' ').slice(0, 28),
            expanded: row ? row.getAttribute('aria-expanded') : null,
            live: li.dataset.live === 'true',
            open: inner ? inner.classList.contains('is-open') : null,
            h: inner ? Math.round(inner.getBoundingClientRect().height) : null,
            chev: [...li.querySelectorAll('.entrychev')].filter(c => c.getClientRects().length).length};
})"""
STATE_JS = "() => localStorage.getItem('gkps-display') || 'null'"
VIEW_JS = "() => document.getElementById('dockPanel').dataset.view"
SCROLL_JS = "() => Math.round(document.getElementById('runBody').scrollTop)"

results = []


def settle(page, ms=480):
    page.wait_for_timeout(ms)


def rows(page):
    return page.evaluate(ROWS_JS)


def opens(page):
    return [r['index'] for r in rows(page) if r['open']]


def non_live_opens(page):
    return [r['index'] for r in rows(page) if r['open'] and not r['live']]


def record(page, name, note=''):
    data = {'state': name, 'view': page.evaluate(VIEW_JS), 'open': opens(page),
            'non_live_open': non_live_opens(page),
            'live': [r['index'] for r in rows(page) if r['live']],
            'scrollTop': page.evaluate(SCROLL_JS),
            'display': json.loads(page.evaluate(STATE_JS)),
            'verdict': page.evaluate(
                "() => {const v = document.getElementById('verdict');"
                " return v.hidden ? null : {ok: v.dataset.ok, text: v.textContent};}"),
            'rows': rows(page), 'note': note}
    results.append(data)
    print(f'{name:38s} view={data["view"]:4s} open={str(data["open"]):12s} '
          f'live={str(data["live"]):8s} non-live-open={data["non_live_open"]}')
    return data


def shot(page, name):
    page.screenshot(path=os.path.join(SHOTS, name + '.png'))


async def noop():
    pass


def open_service(page, sid):
    if page.evaluate(VIEW_JS) != 'pick':
        page.locator('#switchBtn').click()
        page.wait_for_selector('#viewPick.is-active')
        settle(page, 280)
    page.locator(f'.servicerow[data-service="{sid}"]').first.click()
    page.wait_for_function("() => document.getElementById('dockPanel').dataset.view === 'run'")
    settle(page, 800)


def header(page, index):
    page.locator(f'.entryli[data-index="{index}"] .entryrow').click()
    settle(page)


def ensure_open(page, index):
    inner = page.locator(f'#entryinner-{index}')
    if inner.count() and not inner.evaluate("el => el.classList.contains('is-open')"):
        header(page, index)


def project(page, index):
    ensure_open(page, index)
    row = page.locator(f'.entryli[data-index="{index}"] .screenerow').first
    row.scroll_into_view_if_needed()
    settle(page, 140)
    row.click()
    settle(page, 750)


def reread(page):
    """A saved change, not an open: bump the served payload so the rebuild is real."""
    page.evaluate(
        """() => {window.__rebuilds = 0;
            new MutationObserver(ms => ms.forEach(m => {
                if (m.type === 'childList') window.__rebuilds++;
            })).observe(document.getElementById('entryList'), {childList: true});
            window.__previewRevision = (window.__previewRevision || 0) + 1;
            const c = new BroadcastChannel('gkps-service-display');
            c.postMessage({type: 'update'}); c.close();}""")
    settle(page, 900)
    return page.evaluate("() => window.__rebuilds")


def run_behaviour(browser, behaviour, reduced=False, width=1280, height=900, tag=''):
    ctx = browser.new_context(viewport={'width': width, 'height': height},
                              color_scheme='dark', device_scale_factor=1,
                              reduced_motion='reduce' if reduced else 'no-preference')
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: errors.append('console: ' + m.text) if m.type == 'error' else None)
    url = URL + ('&' if '?' in URL else '?') + 'behaviour=' + behaviour
    page.goto(url)
    page.wait_for_selector('.servicerow')
    settle(page, 300)
    prefix = f'{behaviour}{tag}'
    print(f'\n===== {prefix} (reduced={reduced}, {width}x{height}) =====')
    record(page, f'{prefix}: picker at rest')
    shot(page, f'{prefix}-01-picker')

    # the reported sequence
    open_service(page, '155')
    record(page, f'{prefix}: 155 opened')
    shot(page, f'{prefix}-02-155-rest')
    header(page, 3)
    record(page, f'{prefix}: position 4 expanded')
    shot(page, f'{prefix}-03-155-expanded')
    open_service(page, '149')
    record(page, f'{prefix}: 149 opened after 4 was expanded')
    shot(page, f'{prefix}-04-149-after-open')
    open_service(page, '155')
    record(page, f'{prefix}: 155 re-opened')
    shot(page, f'{prefix}-05-155-reopened')

    # multi-open
    for i in (1, 3, 8):
        ensure_open(page, i)
    record(page, f'{prefix}: three blocks open by hand')
    open_service(page, '149')
    record(page, f'{prefix}: 149 after three hand-opens')
    shot(page, f'{prefix}-06-multi-leak')

    # the live-entry exception
    open_service(page, '155')
    project(page, 3)
    record(page, f'{prefix}: position 4 live')
    shot(page, f'{prefix}-07-live')
    open_service(page, '149')
    record(page, f'{prefix}: 149 while 155 is on air')
    open_service(page, '155')
    record(page, f'{prefix}: back on the on-air service')
    shot(page, f'{prefix}-08-live-return')

    # a crossing inside one service (spec 198's rule, unchanged)
    ensure_open(page, 6)
    project(page, 0)
    record(page, f'{prefix}: crossed to 1 with 6 hand-open')
    shot(page, f'{prefix}-09-crossing')

    # a re-read is not an open
    ensure_open(page, 9)
    before = opens(page)
    rebuilds = reread(page)
    record(page, f'{prefix}: after a re-read', note=f'before={before} rebuilds={rebuilds}')
    shot(page, f'{prefix}-10-reread')

    # reload forgets page memory
    page.reload()
    page.wait_for_selector('#dockPanel')
    settle(page, 900)
    record(page, f'{prefix}: after reload')
    shot(page, f'{prefix}-11-reload')

    # the long service with section breaks, and the empty one
    open_service(page, '142')
    record(page, f'{prefix}: 142 (27 entries, 3 breaks)')
    shot(page, f'{prefix}-12-long')
    header(page, 4)
    open_service(page, '145')
    record(page, f'{prefix}: 145 (empty service)')
    shot(page, f'{prefix}-13-empty')

    # light theme, through the dock's own control (it lives in the picker's head)
    open_service(page, '155')
    page.locator('#switchBtn').click()
    page.wait_for_selector('#viewPick.is-active')
    settle(page, 280)
    page.locator('#themeBtn').click()
    settle(page, 300)
    record(page, f'{prefix}: light theme')
    shot(page, f'{prefix}-14-light')

    print('page errors:', errors[:6] if errors else 'none')
    ctx.close()
    return errors


with sync_playwright() as p:
    browser = p.chromium.launch()
    errs = []
    errs += run_behaviour(browser, 'drafted')
    errs += run_behaviour(browser, 'today')
    errs += run_behaviour(browser, 'drafted', reduced=True, tag='-reduce')
    errs += run_behaviour(browser, 'drafted', width=700, height=900, tag='-narrow')
    browser.close()

with open(os.path.join(HERE, 'measurements.json'), 'w', encoding='utf-8') as handle:
    json.dump({'url': URL, 'results': results, 'page_errors': errs}, handle,
              ensure_ascii=False, indent=1)
print('\nwrote measurements.json with', len(results), 'states;', len(errs), 'page errors')
