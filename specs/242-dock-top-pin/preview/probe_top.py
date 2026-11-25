# Spec 242 probe — the live header's off-screen top pin on the real dock.
# Usage: probe_top.py <base-url> <out-dir>
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8793'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__)) + '/shots'
os.makedirs(OUT, exist_ok=True)

STATE = """() => {
  const box = document.getElementById('runBody');
  const li = document.querySelector('.entryli[data-live="true"]');
  const row = li && li.querySelector('.entryrow');
  const topSlot = document.querySelector('.topband-slot');
  const botSlot = document.querySelector('.liveband-slot');
  const clone = topSlot && topSlot.querySelector('.entryrow');
  const b = box.getBoundingClientRect(), r = row && row.getBoundingClientRect();
  const c = clone && !topSlot.hidden ? clone.getBoundingClientRect() : null;
  const cs = clone ? getComputedStyle(clone) : null;
  return {
    live: li ? li.dataset.index : null,
    viewportTop: +b.top.toFixed(2), scrollTop: +box.scrollTop.toFixed(1),
    headerTop: r ? +(r.top - b.top).toFixed(2) : null,
    headerBottom: r ? +(r.bottom - b.top).toFixed(2) : null,
    liveBlockBottom: li ? +(li.getBoundingClientRect().bottom - b.top).toFixed(2) : null,
    topPinVisible: !!(topSlot && !topSlot.hidden),
    topPinTop: c ? +(c.top - b.top).toFixed(2) : null,
    topPinBottom: c ? +(c.bottom - b.top).toFixed(2) : null,
    topRadius: cs ? cs.borderTopLeftRadius : null,
    bottomRadius: cs ? cs.borderBottomLeftRadius : null,
    topPinLabel: clone ? clone.textContent.trim().replace(/\\s+/g, ' ') : null,
    headerLabel: row ? row.textContent.trim().replace(/\\s+/g, ' ') : null,
    bottomPinVisible: !!(botSlot && !botSlot.hidden),
    following: document.getElementById('centreBtn').getAttribute('aria-pressed')
  };
}"""

SAMPLER = """() => {
  window.__tframes = []; window.__tstop = false;
  (function sample() {
    if (window.__tstop) return;
    const box = document.getElementById('runBody');
    const li = document.querySelector('.entryli[data-live="true"]');
    const slot = document.querySelector('.topband-slot');
    if (box && li && slot) {
      window.__tframes.push({
        blockBottom: li.getBoundingClientRect().bottom - box.getBoundingClientRect().top,
        visible: !slot.hidden
      });
    }
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { setTimeout(sample, 2); });
    });
  })();
}"""


def show(page, tag):
    s = page.evaluate(STATE)
    s['tag'] = tag
    print(json.dumps(s), flush=True)
    return s


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 420, 'height': 860},
                            color_scheme='dark', device_scale_factor=1)
    page.goto(BASE + '/obs/dock', wait_until='networkidle')
    page.wait_for_selector('#pickBody .servicerow', timeout=15000)
    page.locator('#pickBody .servicerow').nth(0).click()
    page.wait_for_selector('#dockPanel[data-view="run"] .entryli', timeout=15000)
    page.wait_for_timeout(400)
    deep = page.evaluate("""() => {
      const lis = [...document.querySelectorAll('#entryList .entryli')];
      const hit = lis.find(li => parseInt(li.dataset.index, 10) >= 25 && li.querySelector('.screenerow'));
      return hit ? hit.dataset.index : null;
    }""")
    if deep is None:
        print('NO DEEP ENTRY IN FIRST SERVICE'); sys.exit(1)
    page.evaluate("i => document.querySelector('.entryli[data-index=\"' + i + '\"] .entryrow').click()", deep)
    page.wait_for_timeout(400)
    page.evaluate("i => document.querySelector('.entryli[data-index=\"' + i + '\"] .screenerow').click()", deep)
    page.wait_for_timeout(600)
    show(page, 'live entry, header in view')
    page.evaluate("() => { const b = document.getElementById('runBody'); b.scrollTop = b.scrollHeight; }")
    page.wait_for_timeout(350)
    s = show(page, 'live entry entirely above the scrollport')
    page.screenshot(path=OUT + '/top-pin.png')

    before = page.evaluate("() => localStorage.getItem('gkps-display')")
    page.evaluate(SAMPLER)
    if s['topPinVisible']:
        page.evaluate("document.querySelector('.topband-slot').click()")
    else:
        page.evaluate("document.getElementById('centreBtn').click()")
    page.wait_for_timeout(800)
    page.evaluate('window.__tstop = true')
    frames = page.evaluate('window.__tframes')
    bad = [f for f in frames if f['visible'] != (f['blockBottom'] <= 0.5)]
    if bad:
        print(json.dumps({'tag': 'mismatch detail', 'bad': bad[:8]}), flush=True)
    after = page.evaluate("() => localStorage.getItem('gkps-display')")
    landing = page.evaluate("""() => {
      const b = document.getElementById('runBody').getBoundingClientRect();
      const r = document.querySelector('.screenerow[aria-current="true"]').getBoundingClientRect();
      return +(((r.top + r.bottom) / 2) - ((b.top + b.bottom) / 2)).toFixed(2);
    }""")
    print(json.dumps({'tag': 'click', 'frames': len(frames), 'mismatched_frames': len(bad),
                      'state_unchanged': before == after,
                      'live_row_offset_from_centre': landing,
                      'following': page.evaluate("document.getElementById('centreBtn').getAttribute('aria-pressed')")}), flush=True)
    show(page, 'after the click')
    page.screenshot(path=OUT + '/after-click.png')
    browser.close()
