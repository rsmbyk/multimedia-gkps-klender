# Spec 248 probe — read the top-pin takeover boundary on a running dock.
# Usage: probe_boundary.py <base-url> [out-json]
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:63404'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'boundary.json')

STATE = """() => {
  const box = document.getElementById('runBody');
  const li = document.querySelector('.entryli[data-live=\"true\"]');
  const row = li && li.querySelector('.entryrow');
  const slot = document.querySelector('.topband-slot');
  const clone = slot && !slot.hidden ? slot.querySelector('.entryrow') : null;
  const b = box.getBoundingClientRect();
  const l = li ? li.getBoundingClientRect() : null;
  const r = row ? row.getBoundingClientRect() : null;
  const c = clone ? clone.getBoundingClientRect() : null;
  return {
    scrollTop: +box.scrollTop.toFixed(1),
    maxScroll: +(box.scrollHeight - box.clientHeight).toFixed(1),
    blockTop: l ? +(l.top - b.top).toFixed(2) : null,
    blockBottom: l ? +(l.bottom - b.top).toFixed(2) : null,
    headerTop: r ? +(r.top - b.top).toFixed(2) : null,
    headerBottom: r ? +(r.bottom - b.top).toFixed(2) : null,
    pinned: !!(clone),
    pinTop: c ? +(c.top - b.top).toFixed(2) : null,
    pinBottom: c ? +(c.bottom - b.top).toFixed(2) : null,
    pinLabel: clone ? clone.textContent.trim().replace(/\\s+/g, ' ') : null,
    headerLabel: row ? row.textContent.trim().replace(/\\s+/g, ' ') : null,
    stuck: !!(row && row.classList.contains('is-stuck')),
    headerVisibility: row ? getComputedStyle(row).visibility : null,
    headerCovered: !!(row && row.classList.contains('is-covered')),
    radiusTop: row ? getComputedStyle(row).borderTopLeftRadius : null
  };
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 420, 'height': 860},
                            color_scheme='dark', device_scale_factor=1)
    page.goto(BASE + '/obs/dock', wait_until='networkidle')
    page.wait_for_selector('#pickBody .servicerow', timeout=20000)
    page.locator('#pickBody .servicerow').nth(0).click()
    page.wait_for_selector('#dockPanel[data-view=\"run\"] .entryli', timeout=20000)
    page.wait_for_timeout(400)
    deep = page.evaluate("""() => {
      const lis = [...document.querySelectorAll('#entryList .entryli')];
      const hit = lis.find(li => parseInt(li.dataset.index, 10) >= 25 && li.querySelector('.screenerow'));
      return hit ? hit.dataset.index : null;
    }""")
    if deep is None:
        print('NO DEEP ENTRY IN FIRST SERVICE')
        sys.exit(1)
    page.evaluate("i => document.querySelector('.entryli[data-index=\"' + i + '\"] .entryrow').click()", deep)
    page.wait_for_timeout(350)
    page.evaluate("i => document.querySelector('.entryli[data-index=\"' + i + '\"] .screenerow').click()", deep)
    page.wait_for_timeout(500)
    # Open the live block and several below it so there is a real scroll range.
    page.evaluate("i => document.querySelector('.entryli[data-index=\"' + i + '\"] .entryrow').click()", deep)
    page.wait_for_timeout(400)
    max_scroll = page.evaluate("() => { const b = document.getElementById('runBody'); return b.scrollHeight - b.clientHeight; }")
    frames = []
    steps = 0
    while steps <= int(max_scroll) + 12:
        page.evaluate("v => { document.getElementById('runBody').scrollTop = v; }", steps)
        page.wait_for_timeout(24)
        frames.append(page.evaluate(STATE))
        steps += 4
    page.evaluate("() => { const b = document.getElementById('runBody'); b.scrollTop = b.scrollHeight; }")
    page.wait_for_timeout(250)
    frames.append(page.evaluate(STATE))
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    with open(OUT, 'w') as fh:
        fh.write('[\n')
        for i, frame in enumerate(frames):
            fh.write(json.dumps(frame, separators=(',', ':')))
            fh.write(',' if i < len(frames) - 1 else '')
            fh.write('\n')
        fh.write(']\n')
    changes = [f for i, f in enumerate(frames) if i == 0 or f['pinned'] != frames[i-1]['pinned']]
    first = next((f for f in frames if f['pinned']), None)
    straddle = [f for f in frames if f['pinned'] and f['blockBottom'] > 0.5]
    dup = [f['scrollTop'] for f in frames if f['pinned'] and f['headerVisibility'] != 'hidden']
    misalign = [f['scrollTop'] for f in straddle if abs((f['pinTop'] or 0) - (f['headerTop'] or 0)) > 0.5]
    boundary_bad = [f['scrollTop'] for f in frames if f['pinned'] != (f['blockTop'] <= 0.5)]
    print(json.dumps({'url': BASE, 'live_entry': deep, 'max_scroll': max_scroll,
                      'frames': len(frames), 'changes': changes,
                      'first_pin': first,
                      'straddle_frames': len(straddle),
                      'duplicate_header_frames': dup[:6],
                      'misaligned_takeover_frames': misalign[:6],
                      'boundary_mismatch_frames': boundary_bad[:6]}, indent=2))
    browser.close()
