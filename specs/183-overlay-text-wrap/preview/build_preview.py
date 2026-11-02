"""Build the slice-183 preview from the live overlay.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/183-overlay-text-wrap/preview/build_preview.py --service 3

For each state the script opens `/obs/source/overlay` on the slice's own `runserver`,
waits for the panel to settle, and captures the stage's DOM exactly as
`static/web/obs-overlay.js` built it. It measures the state twice — as the page paints
it, and with the one declaration this slice adds restored to `normal` — and writes
`index.html` with both, so the review page shows the product's own markup and the
product's own sheet, before and after.
"""

import argparse
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import screens  # noqa: E402  — the projector's own screen list

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent

STATES = [
    (0, 'text-long-word', 'in', 'Liturgy text · the report',
     'Body `a very <120-character run> untitled text` — the owner\'s screenshot.'),
    (1, 'text-pasted-url', 'in', 'Liturgy text · pasted link',
     'A speaker mark, then a 140-character URL: the mark keeps its column, the words wrap.'),
    (2, 'song-long-word', 'in', 'Song · the caption',
     'A lyric whose 66-character run is the caption, set at 72px with no panel to grow into.'),
    (3, 'passage-long-title', 'in', 'Passage · a long verse title',
     'The heading is a run with no space in it: the title wraps under the reference.'),
    (4, 'text-short', 'in', 'Control · a short liturgy',
     'Both lines fit: the same rows, the same box, the same place as before the slice.'),
    (5, 'text-untitled-short', 'in', 'Control · a short untitled text',
     'The smallest panel on the surface — unchanged by the rule.'),
    (6, 'text-long-kicker', 'in', 'Liturgy text · a 64-character entry title',
     'The plate\'s kicker is the entry\'s own title: the plate grows to hold it, one row.'),
]

MEASURE = """() => {
  const plate = document.querySelector('.obs-overlay__plate');
  const caption = document.querySelector('.obs-overlay__caption');
  const root = plate || caption;
  if (!root) return null;
  const box = root.getBoundingClientRect();
  const rows = (el) => { const range = document.createRange();
    range.selectNodeContents(el);
    return new Set([...range.getClientRects()].map(r => Math.round(r.top))).size; };
  const spill = (el) => { const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()];
    if (!rects.length) return 0;
    return Math.max(...rects.map(r => r.right)) - el.getBoundingClientRect().right; };
  const row = (name, scope, elements) => ({
    name: name, scope: scope,
    rows: elements.reduce((n, el) => n + rows(el), 0),
    spill: +Math.max(0, ...elements.map(spill)).toFixed(2)});
  const out = [];
  if (caption) {
    out.push(row('caption', 'in', [caption]));
  } else {
    const kicker = plate.querySelector('.obs-overlay__kicker');
    const title = plate.querySelector('.obs-overlay__title');
    const lines = [...plate.querySelectorAll('.obs-overlay__line')];
    if (kicker) out.push(row('kicker', 'in', [kicker]));
    if (title) out.push(row('title', 'in', [title]));
    out.push(row('body', 'in', lines));
  }
  return {w: +box.width.toFixed(2), h: +box.height.toFixed(2),
          font: getComputedStyle(plate || caption).fontSize, elements: out};
}"""



def capture(page, service, screen):
    page.evaluate("""([service, screen]) => localStorage.setItem('gkps-display',
        JSON.stringify({service: service, screen: screen, on: true, translation: null}))""",
                  [service, screen])
    page.reload()
    page.wait_for_selector('.obs-overlay__plate, .obs-overlay__caption')
    page.wait_for_timeout(400)
    after = page.evaluate(MEASURE)
    html = page.evaluate("() => document.querySelector('.obs-overlay__stage').innerHTML")
    kind = page.evaluate(
        "() => document.querySelector('.obs-overlay__caption') ? 'caption' : 'plate'")
    page.evaluate("""() => document
        .querySelectorAll('.obs-overlay__stage, .obs-overlay__stage *')
        .forEach(el => el.style.setProperty('overflow-wrap', 'normal', 'important'))""")
    page.wait_for_timeout(120)
    before = page.evaluate(MEASURE)
    return {'html': html, 'kind': kind, 'before': before, 'after': after}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='http://127.0.0.1:8816')
    parser.add_argument('--service', type=int, default=3)
    parser.add_argument('--out', default=str(HERE / 'index.html'))
    args = parser.parse_args()

    states = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_context(viewport={'width': 1920, 'height': 1080},
                                   device_scale_factor=1).new_page()
        page.goto(args.base + '/obs/source/overlay')
        screen_list = screens.screens(args.base, args.service)
        for entry_index, name, scope, title, note in STATES:
            screen = screens.first_screen_of(screen_list, entry_index)
            data = capture(page, args.service, screen)
            data.update({'id': name, 'scope': scope, 'title': title, 'note': note,
                         'screen': screen, 'entry': entry_index})
            states.append(data)
        browser.close()

    payload = json.dumps(states, indent=1)
    html = TEMPLATE.replace('/*__STATES__*/', payload)
    pathlib.Path(args.out).write_text(html)
    for state in states:
        cells = []
        for which in ('before', 'after'):
            body = [e for e in state[which]['elements'] if e['name'] == 'body']
            body = body[0] if body else {'rows': 0, 'spill': 0}
            cells.append(f"{which} {body['rows']}r spill {body['spill']:>8}")
        print(f"{state['id']:<20} {state['scope']:<4} " + '  '.join(cells) +
              f"  box {state['before']['w']}x{state['before']['h']}")
    print('wrote', args.out)


TEMPLATE = r"""<!doctype html>
<!-- Spec 183 — the overlay's text, before and after it wraps. A static review page:
     the DOM captured from the slice's own `/obs/source/overlay` (so it is the
     controller's own markup, class for class), the repo's own obs-overlay.css and
     bundled faces, over the 1920x1080 frame spec 180's preview already carries, captured
     from the church's own worship video. Each
     frame is laid out at 1920x1080 — container units resolve at the real size — and
     only the paint is scaled. "Before" is the same subtree with the one declaration
     this slice adds restored to `normal`. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Overlay text wrap — spec 183</title>
<link rel="stylesheet" href="../../../static/styles/design/fonts.css">
<link rel="stylesheet" href="../../../static/styles/design/tokens.css">
<link rel="stylesheet" href="../../../static/styles/design/obs-overlay.css">
<style>
  html, body.review { margin: 0; height: 100%; background: #0B0D10; color: #E8EAED;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  body.review { display: flex; flex-direction: column; overflow: hidden; }
  .review__bar { flex: 0 0 auto; display: flex; align-items: center; gap: 10px;
    padding: 10px 16px; border-bottom: 1px solid rgba(255,255,255,.08); }
  .review__title { margin: 0 auto 0 0; font-size: 13px; font-weight: 650; }
  .review__title span { color: rgba(255,255,255,.5); font-weight: 450; }
  .review__group { display: flex; gap: 2px; padding: 2px; border: 1px solid rgba(255,255,255,.1);
    border-radius: 8px; }
  .review__btn { appearance: none; border: 0; border-radius: 6px; padding: 5px 10px;
    background: transparent; color: rgba(255,255,255,.62); font: inherit; font-size: 12px;
    font-weight: 550; cursor: pointer; }
  .review__btn:hover { color: #fff; background: rgba(255,255,255,.07); }
  .review__btn[aria-pressed="true"] { background: #E8EAED; color: #0B0D10; }
  .review__count { min-width: 54px; text-align: center; font-size: 11.5px;
    color: rgba(255,255,255,.46); font-variant-numeric: tabular-nums; }
  .review__body { flex: 1 1 auto; display: grid; grid-template-columns: 236px 1fr;
    min-height: 0; }
  .review__index { overflow: auto; border-right: 1px solid rgba(255,255,255,.08);
    padding: 8px; }
  .review__item { display: block; width: 100%; text-align: left; border: 0; border-radius: 7px;
    background: transparent; color: rgba(255,255,255,.66); font: inherit; font-size: 12px;
    padding: 8px 9px; cursor: pointer; }
  .review__item:hover { background: rgba(255,255,255,.06); color: #fff; }
  .review__item[aria-current="true"] { background: rgba(255,255,255,.1); color: #fff; }
  .review__item b { display: block; font-weight: 600; font-size: 12px; }
  .review__item i { font-style: normal; color: rgba(255,255,255,.4); font-size: 11px; }
  .review__pane { position: relative; min-width: 0; overflow: auto; padding: 14px 18px 18px; }
  .review__note { margin: 0 0 12px; font-size: 12.5px; line-height: 1.5;
    color: rgba(255,255,255,.72); max-width: 78ch; }
  .shot { position: relative; margin: 0 0 14px; }
  .shot__label { position: absolute; top: -1px; left: 0; z-index: 3; padding: 3px 8px;
    font-size: 10.5px; font-weight: 650; letter-spacing: .08em; text-transform: uppercase;
    border-radius: 0 0 6px 0; }
  .shot--before .shot__label { background: rgba(190,60,60,.92); color: #fff; }
  .shot--after .shot__label { background: rgba(60,150,110,.92); color: #fff; }
  .shot__box { position: relative; overflow: hidden; border-radius: 6px;
    outline: 1px solid rgba(255,255,255,.09); }
  .shot__frame { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px;
    transform-origin: 0 0; }
  .shot__frame .obs-overlay__stage { position: absolute; inset: 0; }
  .shot__frame img { position: absolute; inset: 0; width: 1920px; height: 1080px;
    object-fit: cover; }
  /* The one declaration this slice adds, restored: the before state is the same tree
     with every text run back to the browser's default. */
  .is-before, .is-before * { overflow-wrap: normal !important; }
  .readout { display: flex; gap: 16px; flex-wrap: wrap; margin: 6px 0 18px; font-size: 12px;
    color: rgba(255,255,255,.6); font-variant-numeric: tabular-nums; }
  .readout b { color: #fff; font-weight: 600; }
  .readout i { font-style: normal; color: rgba(240,196,120,.92); }
  .readout .before { color: rgba(240,138,138,.9); }
  .readout .after { color: rgba(127,211,168,.95); }
  .readout .bad { color: #F08A8A; }
  .readout .good { color: #7FD3A8; }
  @media (max-width: 880px) { .review__body { grid-template-columns: 1fr; } }
</style>
</head>
<body class="review">
<header class="review__bar">
  <p class="review__title">OBS overlay · text that has no space in it
    <span>spec 183 · 1920×1080 frames</span></p>
  <div class="review__group" id="states"></div>
  <div class="review__group">
    <button class="review__btn" data-mode="before">Before</button>
    <button class="review__btn" data-mode="both">Both</button>
    <button class="review__btn" data-mode="after">After</button>
  </div>
  <div class="review__group">
    <button class="review__btn" data-scale="fit" id="scaleFit">Fit</button>
    <button class="review__btn" data-scale="one" id="scaleOne">1:1</button>
  </div>
  <span class="review__count" id="count"></span>
  <button class="review__btn" id="prev">◀</button>
  <button class="review__btn" id="next">▶</button>
</header>
<div class="review__body">
  <nav class="review__index" id="index"></nav>
  <main class="review__pane" id="pane">
    <p class="review__note" id="note"></p>
    <div id="frames"></div>
    <div class="readout" id="readout"></div>
  </main>
</div>
<script>
var STATES = /*__STATES__*/;
var mode = 'both', scaleMode = 'fit', at = 0;
var framePath = '../../180-overlay-text-styles/preview/frame.jpg';

function el(tag, className) { var n = document.createElement(tag);
  if (className) n.className = className; return n; }

function buildShots() {
  var frames = document.getElementById('frames');
  frames.replaceChildren();
  var state = STATES[at];
  var shots = [];
  if (mode !== 'after') shots.push('before');
  if (mode !== 'before') shots.push('after');
  shots.forEach(function (which) {
    var shot = el('figure', 'shot shot--' + which);
    shot.appendChild(el('figcaption', 'shot__label')).textContent =
      which + (which === 'before' ? ' · overflow-wrap: normal' : ' · overflow-wrap: break-word');
    var box = el('div', 'shot__box');
    var frame = el('div', 'shot__frame');
    var img = el('img'); img.src = framePath; img.alt = '';
    var stage = el('div', 'obs-overlay__stage' + (which === 'before' ? ' is-before' : ''));
    stage.setAttribute('aria-live', 'off');
    stage.innerHTML = state.html;
    frame.appendChild(img); frame.appendChild(stage);
    box.appendChild(frame);
    shot.appendChild(box);
    frames.appendChild(shot);
    shot._frame = frame; shot._box = box;
  });
  return shots;
}

function layout() {
  var pane = document.getElementById('pane');
  var shots = document.querySelectorAll('.shot');
  var width = Math.min(pane.clientWidth - 36, 1920);
  var scale = 1;
  if (scaleMode === 'fit') {
    var room = (pane.clientHeight - 140) / Math.max(1, shots.length) - 18;
    scale = Math.min(width / 1920, room / 1080);
    scale = Math.max(0.16, Math.min(scale, 1));
  }
  shots.forEach(function (shot) {
    shot._frame.style.transform = 'scale(' + scale + ')';
    shot._box.style.width = (1920 * scale) + 'px';
    shot._box.style.height = (1080 * scale) + 'px';
  });
}

function readout() {
  var state = STATES[at];
  var box = document.getElementById('readout');
  var parts = [];
  ['before', 'after'].forEach(function (which) {
    if (mode !== 'both' && mode !== which) return;
    var m = state[which];
    var cells = m.elements.map(function (e) {
      var tail;
      if (e.spill > 0) {
        tail = '<span class="bad">' + e.spill.toFixed(2) + 'px past</span>';
      } else {
        tail = '<span class="good">inside</span>';
      }
      var scope = e.scope === 'out' ? ' <i>out of scope</i>' : '';
      return e.name + ': <b>' + e.rows + '</b> r · ' + tail + scope;
    });
    parts.push('<span class="' + which + '">' + which + '</span> · <b>' + m.w + ' × ' + m.h +
      '</b> px at ' + m.font + ' — ' + cells.join(' · '));
  });
  box.innerHTML = parts.join('<br>');
}

function render() {
  var state = STATES[at];
  document.querySelectorAll('.review__item').forEach(function (node, i) {
    node.setAttribute('aria-current', i === at ? 'true' : 'false');
  });
  document.getElementById('count').textContent = (at + 1) + ' / ' + STATES.length;
  document.getElementById('note').textContent = state.title + ' — ' + state.note;
  document.querySelectorAll('[data-mode]').forEach(function (b) {
    b.setAttribute('aria-pressed', b.dataset.mode === mode ? 'true' : 'false');
  });
  document.getElementById('scaleFit').setAttribute('aria-pressed', scaleMode === 'fit');
  document.getElementById('scaleOne').setAttribute('aria-pressed', scaleMode === 'one');
  buildShots();
  layout();
  readout();
  location.hash = 'state=' + state.id + '&mode=' + mode + '&scale=' + scaleMode;
}

function go(delta) { at = (at + delta + STATES.length) % STATES.length; render(); }

document.getElementById('prev').onclick = function () { go(-1); };
document.getElementById('next').onclick = function () { go(1); };
document.querySelectorAll('[data-mode]').forEach(function (button) {
  button.onclick = function () { mode = button.dataset.mode; render(); };
});
document.getElementById('scaleFit').onclick = function () { scaleMode = 'fit'; render(); };
document.getElementById('scaleOne').onclick = function () { scaleMode = 'one'; render(); };

var statesBar = document.getElementById('states');
var index = document.getElementById('index');
STATES.forEach(function (state, i) {
  var bar = el('button', 'review__btn');
  bar.textContent = String(i + 1);
  bar.title = state.title;
  bar.onclick = function () { at = i; render(); };
  statesBar.appendChild(bar);
  var item = el('button', 'review__item');
  var name = el('b'); name.textContent = state.title;
  var sub = el('i');
  sub.textContent = 'screen ' + state.screen + ' · ' +
    (state.scope === 'out' ? 'out of scope' : 'in scope');
  item.appendChild(name); item.appendChild(sub);
  item.onclick = function () { at = i; render(); };
  index.appendChild(item);
});

document.addEventListener('keydown', function (event) {
  if (event.key === 'ArrowRight' || event.key === 'j' || event.key === 'J') go(1);
  else if (event.key === 'ArrowLeft' || event.key === 'k' || event.key === 'K') go(-1);
  else if (event.key === 'b' || event.key === 'B') {
    mode = mode === 'both' ? 'after' : mode === 'after' ? 'before' : 'both'; render();
  } else if (event.key >= '1' && event.key <= String(STATES.length)) {
    at = Number(event.key) - 1; render();
  }
});

var hash = new URLSearchParams(location.hash.slice(1));
if (hash.get('mode')) mode = hash.get('mode');
if (hash.get('scale')) scaleMode = hash.get('scale');
if (hash.get('state')) {
  var found = STATES.findIndex(function (s) { return s.id === hash.get('state'); });
  if (found >= 0) at = found;
}
window.addEventListener('resize', function () { layout(); });

/* A pasted deep link is a state: read the hash again when it changes, without a reload. */
window.addEventListener('hashchange', function () {
  var link = new URLSearchParams(location.hash.slice(1));
  if (link.get('mode')) mode = link.get('mode');
  if (link.get('scale')) scaleMode = link.get('scale');
  if (link.get('state')) {
    var found = STATES.findIndex(function (s) { return s.id === link.get('state'); });
    if (found >= 0) at = found;
  }
  render();
});
render();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    main()
