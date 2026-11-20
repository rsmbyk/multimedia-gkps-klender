# Spec 208 US4 probe — the bottom pin on the real dock.
# Usage: probe_bottom.py <base-url> <out-dir>
# Scenario A: the 60-entry service — a song deep in the list goes live; at
# scrollTop 0 its header is far below the view (fully-off strip), then the
# partial-cut stack (band at the edge, strip above), then the strip-click glide
# home (per-frame tracking + the centre act).
# Scenario B: the 1 Nov service — the LAST entry live with a hand-opened block
# above: no NEXT entry exists, so the strip holds the edge alone; the click
# glides to the list's end clamp (correct physics, R15).
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8767'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__)) + '/shots/bottom'
os.makedirs(OUT, exist_ok=True)

STATE = """() => {
  const box = document.getElementById('runBody');
  const li = document.querySelector('.entryli[data-live="true"]');
  const row = li && li.querySelector('.entryrow');
  const strip = document.querySelector('.liveband');
  const slot = document.querySelector('.liveband-slot');
  const band = document.querySelector('.nextband');
  const b = box.getBoundingClientRect();
  const s = strip && slot && !slot.hidden ? strip.getBoundingClientRect() : null;
  const n = band && !band.hidden ? band.getBoundingClientRect() : null;
  const r = row ? row.getBoundingClientRect() : null;
  return {
    live: li ? li.dataset.index : null,
    stripVisible: !!s,
    stripBottom: s ? +(s.bottom - b.bottom).toFixed(2) : null,
    stripRadius: strip ? getComputedStyle(strip).borderBottomLeftRadius : null,
    stripLabel: strip ? strip.textContent.trim().replace(/\\s+/g, ' ') : null,
    bandVisible: !!n,
    bandTop: n ? +(n.top - b.bottom).toFixed(2) : null,
    bandBottom: n ? +(n.bottom - b.bottom).toFixed(2) : null,
    headerTop: r ? +(r.top - b.top).toFixed(2) : null,
    headerBottom: r ? +(r.bottom - b.top).toFixed(2) : null,
    viewportH: +b.height.toFixed(2), scrollTop: +box.scrollTop.toFixed(1)
  };
}"""

SAMPLER = """() => {
  window.__bframes = []; window.__bstop = false;
  (function sample() {
    if (window.__bstop) return;
    const box = document.getElementById('runBody');
    const li = document.querySelector('.entryli[data-live="true"]');
    const slot = document.querySelector('.liveband-slot');
    if (box && li && slot) {
      const r = li.querySelector('.entryrow').getBoundingClientRect();
      const b = box.getBoundingClientRect();
      window.__bframes.push({hb: r.bottom - b.bottom, v: !slot.hidden});
    }
    requestAnimationFrame(sample);
  })();
}"""

def show(page, tag):
    s = page.evaluate(STATE)
    s['tag'] = tag
    print(json.dumps(s), flush=True)
    return s

def click_row(page, i):
    page.evaluate("i => document.querySelector('.entryli[data-index=\"' + i + '\"] .entryrow').click()", i)

def click_screen(page, i):
    page.evaluate("i => document.querySelector('.entryli[data-index=\"' + i + '\"] .screenerow').click()", i)

def glide_report(page, tag):
    before = page.evaluate("() => localStorage.getItem('gkps-display')")
    page.evaluate(SAMPLER)
    page.evaluate("document.querySelector('.liveband').click()")
    page.wait_for_timeout(750)
    page.evaluate('window.__bstop = true')
    frames = page.evaluate('window.__bframes')
    bad = [f for f in frames if f['v'] != (f['hb'] > 0.5)]
    after = page.evaluate("() => localStorage.getItem('gkps-display')")
    off = page.evaluate("""() => { const box = document.getElementById('runBody');
        const row = document.querySelector('.screenerow[aria-current="true"]');
        const b = box.getBoundingClientRect(), r = row.getBoundingClientRect();
        return +(((r.top + r.bottom) / 2) - ((b.top + b.bottom) / 2)).toFixed(2); }""")
    following = page.evaluate("document.getElementById('centreBtn').getAttribute('aria-pressed')")
    print(json.dumps({'tag': tag, 'frames': len(frames), 'mismatched_frames': len(bad),
                      'state_unchanged': before == after,
                      'live_row_offset_from_centre': off, 'following': following}), flush=True)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={'width': 420, 'height': 860},
                    color_scheme='dark', device_scale_factor=1)
    pg.goto(BASE + '/obs/dock', wait_until='networkidle')
    pg.wait_for_selector('#pickBody .servicerow', timeout=15000)

    # ---- Scenario A: a deep entry in the 60-entry service ----
    pg.locator('#pickBody .servicerow').nth(0).click()
    pg.wait_for_selector('#dockPanel[data-view="run"] .entryli', timeout=15000)
    pg.wait_for_timeout(400)
    song = pg.evaluate("""() => {
        const lis = [...document.querySelectorAll('#entryList .entryli')];
        const hit = lis.find(li => parseInt(li.dataset.index, 10) >= 25 &&
            li.querySelector('.screenerow'));
        return hit ? hit.dataset.index : null;
    }""")
    if song is None:
        print('NO DEEP ENTRY IN SERVICE A'); sys.exit(1)
    click_row(pg, song); pg.wait_for_timeout(400)
    click_screen(pg, song); pg.wait_for_timeout(600)
    s = show(pg, 'A fully off below (deep entry live, list at the top)')
    pg.screenshot(path=OUT + '/a-fully-off.png')
    pg.evaluate("s => document.getElementById('runBody').scrollTop += s",
                s['headerTop'] - (s['viewportH'] - 20))
    pg.wait_for_timeout(250)
    s = show(pg, 'A partial cut — strip above the band (band caged by its li top)')
    pg.screenshot(path=OUT + '/a-stack.png')
    glide_report(pg, 'A strip click: glide home')
    show(pg, 'A after the click')
    pg.screenshot(path=OUT + '/a-after-click.png')

    # ---- Scenario B: the last entry live, no NEXT band ----
    pg.evaluate("document.getElementById('switchBtn').click()")
    pg.wait_for_selector('#dockPanel[data-view="pick"]', timeout=10000)
    pg.locator('#pickBody .servicerow').nth(1).click()
    pg.wait_for_selector('#dockPanel[data-view="run"] .entryli', timeout=15000)
    pg.wait_for_timeout(400)
    last = pg.evaluate("""() => {
        const lis = [...document.querySelectorAll('#entryList .entryli')];
        const withBlock = lis.filter(li => li.querySelector('.screenerow'));
        return withBlock[withBlock.length - 1].dataset.index;
    }""")
    click_row(pg, last); pg.wait_for_timeout(400)
    click_screen(pg, last); pg.wait_for_timeout(500)
    click_row(pg, '4'); pg.wait_for_timeout(500)     # HAL 1's block open above
    s = show(pg, 'B fully off below, no NEXT entry (strip alone at the edge)')
    pg.screenshot(path=OUT + '/b-fully-off-no-band.png')
    glide_report(pg, 'B strip click: glide to the end clamp')
    show(pg, 'B after the click')
    b.close()
