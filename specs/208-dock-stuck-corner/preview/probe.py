# Spec 208 probe — the pinned/flat-top desync, before and after.
# Usage: probe.py <base-url> <out-dir>
# Drives the real dock: open a service with a long song, project its first
# screen, advance deep (header pins), hand-scroll (control), Ctrl+Home back
# (header lands in flow). Measures geometry vs .is-stuck vs painted radius,
# and samples class-vs-geometry per frame during the advance.
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:63404'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__)) + '/shots'
os.makedirs(OUT, exist_ok=True)

MEASURE = """() => {
  const box = document.getElementById('runBody');
  const li = document.querySelector('.entryli[data-live="true"]');
  if (!box || !li) return {error: 'no live entry'};
  const row = li.querySelector('.entryrow');
  const b = box.getBoundingClientRect(), r = row.getBoundingClientRect();
  const l = li.getBoundingClientRect();
  const cs = getComputedStyle(row);
  const cur = li.querySelector('.screenerow[aria-current="true"]');
  return {
    index: li.dataset.index,
    label: row.textContent.trim().replace(/\\s+/g, ' ').slice(0, 48),
    delta: +(r.top - b.top).toFixed(2),
    liBottom: +(l.bottom - b.top).toFixed(2),
    stuckClass: row.classList.contains('is-stuck'),
    radius: cs.borderTopLeftRadius,
    scrollTop: +box.scrollTop.toFixed(1),
    screen: cur ? cur.dataset.screen : null
  };
}"""

ENTRIES = """() => Array.from(document.querySelectorAll('#entryList .entryli')).map(li => ({
  index: li.dataset.index,
  label: li.querySelector('.entryrow').textContent.trim().replace(/\\s+/g, ' ').slice(0, 48),
  screens: li.querySelectorAll('.screenerow').length
}))"""

SAMPLER = """() => {
  window.__frames = []; window.__stop = false;
  (function sample() {
    if (window.__stop) return;
    const box = document.getElementById('runBody');
    const li = document.querySelector('.entryli[data-live="true"]');
    if (box && li) {
      const row = li.querySelector('.entryrow');
      const b = box.getBoundingClientRect(), r = row.getBoundingClientRect();
      const l = li.getBoundingClientRect();
      window.__frames.push({d: r.top - b.top, lb: l.bottom - b.top,
                            c: row.classList.contains('is-stuck')});
    }
    requestAnimationFrame(sample);
  })();
}"""

def measure(page, tag):
    m = page.evaluate(MEASURE)
    m['tag'] = tag
    print(json.dumps(m), flush=True)
    return m

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={'width': 420, 'height': 860},
                    color_scheme='dark', device_scale_factor=1)
    pg.goto(BASE + '/obs/dock', wait_until='networkidle')
    pg.wait_for_selector('#pickBody .servicerow', timeout=15000)

    rows = pg.query_selector_all('#pickBody .servicerow')
    chosen = None
    for i, r in enumerate(rows[:6]):
        r.click()
        pg.wait_for_selector('#dockPanel[data-view="run"] .entryli', timeout=15000)
        pg.wait_for_timeout(400)
        es = pg.evaluate(ENTRIES)
        cands = [e for e in es if e['screens'] >= 12 and int(e['index']) >= 3]
        if cands:
            chosen = max(cands, key=lambda e: e['screens'])
            print(json.dumps({'base': BASE, 'service_try': i, 'chosen': chosen}), flush=True)
            break
        pg.click('#switchBtn')
        pg.wait_for_selector('#dockPanel[data-view="pick"]', timeout=10000)
    if not chosen:
        print('NO LONG SONG FOUND'); sys.exit(1)

    idx = chosen['index']
    pg.click(f'.entryli[data-index="{idx}"] .entryrow')     # open the block
    pg.wait_for_timeout(450)
    pg.click(f'.entryli[data-index="{idx}"] .screenerow')   # project first screen
    pg.wait_for_timeout(700)
    measure(pg, 'live at first screen (in flow)')
    pg.evaluate("document.getElementById('dockPanel').focus()")
    pg.evaluate(SAMPLER)

    # A: advance deep — the header lands pinned; sample class-vs-geometry per frame
    for _ in range(chosen['screens'] - 4):
        pg.keyboard.press('ArrowRight')
        pg.wait_for_timeout(330)
    pg.wait_for_timeout(900)
    pg.evaluate('window.__stop = true')
    frames = pg.evaluate('window.__frames')
    bad = [f for f in frames if f['c'] != (f['d'] <= 0.5 and f['lb'] > 0.5)]
    pinned = [f for f in frames if f['d'] <= 0.5 and f['lb'] > 0.5]
    print(json.dumps({'tag': 'per-frame during advance', 'frames': len(frames),
                      'pinned_frames': len(pinned), 'mismatched_frames': len(bad)}), flush=True)
    a = measure(pg, 'A after advance, at rest')
    pg.screenshot(path=OUT + '/a-pinned.png')

    # control: one hand scroll reconciles on any build
    pg.evaluate("document.getElementById('runBody').scrollTop -= 24")
    pg.wait_for_timeout(200)
    measure(pg, 'control after hand scroll')
    pg.screenshot(path=OUT + '/control-pinned.png')

    # B: Ctrl+Home crosses to the first entry; its header lands in flow
    pg.keyboard.press('Control+Home')
    pg.wait_for_timeout(900)
    bb = measure(pg, 'B after Ctrl+Home, at rest')
    pg.screenshot(path=OUT + '/b-inflow.png')

    b.close()
