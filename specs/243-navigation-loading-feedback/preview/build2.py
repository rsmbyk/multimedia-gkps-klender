#!/usr/bin/env python3
"""Spec 243, revised preview: one pending state for every fetching click.

Reuses build.py's real-shell inlining. The four scenarios all go through the
same global bar and source mark: rail section, first-level row, second-level
row, and a queued second click. Writes index.html.
"""
import re

from build import HERE, catalogue_css, inline_images

PREVIEW_CSS = r'''
/* ---- Preview chrome: one global sign, any source ----------------------- */
:root { --pv-top: 44px; }
body { padding-top: var(--pv-top); }
.pv-bar {
  position: fixed; inset: 0 0 auto 0; height: var(--pv-top); z-index: 9000;
  display: flex; align-items: center; gap: 8px; padding: 0 12px;
  background: var(--rail-bg); border-bottom: 1px solid var(--divider);
  color: var(--ink); font: 12px/1.35 ui-sans-serif, system-ui, sans-serif;
}
.pv-bar__title { font-weight: 650; margin-right: 4px; white-space: nowrap; }
.pv-bar__hint { margin-left: auto; opacity: .72; white-space: nowrap; }
.pv-bar button {
  border: 1px solid var(--divider); border-radius: 6px; padding: 5px 9px;
  background: transparent; color: inherit; font: inherit; cursor: pointer;
}
.pv-bar button:hover { background: var(--icon-hover-bg); }
.pv-bar button[aria-pressed="true"] { background: var(--active-bg); color: var(--active-ink); border-color: transparent; }
.pv-bar button:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.pv-asset { display: inline-block; background-size: contain; background-repeat: no-repeat; background-position: center; }
.rail, .panel, .chapters, .topbar { top: var(--pv-top) !important; }

/* The one global sign. 3px at the window top, delayed 180ms, never clears
   between a fetch and its queued successor. */
.pv-progress {
  position: fixed; top: 0; left: 0; right: 0; height: 3px; z-index: 9500;
  overflow: hidden; background: color-mix(in srgb, var(--active-bg) 22%, transparent);
}
.pv-progress::before {
  content: ""; position: absolute; top: 0; bottom: 0; width: 28%;
  background: var(--active-bg); animation: pv-slide 1.05s var(--ease-timing) infinite;
}
@keyframes pv-slide { from { transform: translateX(-100%); } to { transform: translateX(460%); } }

/* The source mark is attached to whichever element was clicked: a rail
   button, a first-level row, or a chapter/song tile. Solid = fetching;
   dashed = queued. No selector here names a particular control type. */
.pv-source { position: relative; }
html.pv-loading .pv-source--active {
  box-shadow: inset 3px 0 var(--active-bg);
}
html.pv-loading .pv-source--active .book__n,
html.pv-loading .pv-source--active .book__a,
html.pv-loading .pv-source--active .book__s,
html.pv-loading .pv-source--active .rail__name { opacity: .58; }
html.pv-loading .pv-source--queued {
  box-shadow: inset 3px 0 color-mix(in srgb, var(--active-bg) 55%, transparent);
}
html.pv-loading .pv-source--queued .book__n,
html.pv-loading .pv-source--queued .book__a,
html.pv-loading .pv-source--queued .book__s { opacity: .78; }
html.pv-loading .pv-source--queued::after {
  content: ""; position: absolute; right: 9px; top: 50%; width: 5px; height: 5px;
  margin-top: -2.5px; border-radius: 50%; background: var(--active-bg); opacity: .65;
}
.pv-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.pv-progress[hidden] { display: none !important; }
@media (prefers-reduced-motion: reduce) { .pv-progress::before { animation: none; } }
'''

SCENARIO_JS = r'''
(function () {
  var root = document.documentElement;
  var bar = document.getElementById('pvProgress');
  var live = document.getElementById('pvLive');
  var hint = document.getElementById('pvHint');
  var buttons = [...document.querySelectorAll('.pv-bar button[data-scenario]')];
  var marked = [];
  var showTimer, swapTimer, settleTimer;

  var scenes = {
    rail: {
      nav: 'closed', ch: 'closed',
      hint: '180 ms delay · 2.4 s fetch · rail section switch',
      pick: function () { return [document.querySelector('.rail__btn[data-panel="kidung"]')]; }
    },
    first: {
      nav: 'open', ch: 'closed',
      hint: '180 ms delay · 2.4 s fetch · first-level row',
      pick: function () { return [document.querySelector('.book[data-name="Keluaran"]')]; }
    },
    second: {
      nav: 'open', ch: 'open',
      hint: '180 ms delay · 2.4 s fetch · second-level row',
      pick: function () {
        var tiles = document.querySelectorAll('.ch-num');
        return [tiles[1] || tiles[0]];
      }
    },
    queued: {
      nav: 'open', ch: 'closed',
      hint: 'solid = fetching · dashed = queued · one bar across both',
      pick: function () {
        return [document.querySelector('.book[data-name="Keluaran"]'),
                document.querySelector('.book[data-name="Imamat"]')];
      }
    }
  };

  function clearMarks() {
    marked.forEach(function (el) {
      if (!el) return;
      el.classList.remove('pv-source', 'pv-source--active', 'pv-source--queued');
    });
    marked = [];
  }
  function mark(el, state) {
    if (!el) return;
    el.classList.add('pv-source', 'pv-source--' + state);
    marked.push(el);
  }
  function paint() {
    var scene = scenes[root.dataset.scenario];
    clearMarks();
    var picked = scene.pick();
    mark(picked[0], 'active');
    if (picked[1]) mark(picked[1], 'queued');
    bar.hidden = false;
    live.textContent = root.dataset.scenario === 'queued'
      ? 'Loading page, one page queued' : 'Loading page';
  }
  function swapQueue() {
    if (root.dataset.scenario !== 'queued') return;
    var picked = scenes.queued.pick();
    if (picked[0]) picked[0].classList.remove('pv-source--active');
    if (picked[1]) {
      picked[1].classList.remove('pv-source--queued');
      picked[1].classList.add('pv-source--active');
    }
    live.textContent = 'Loading queued page';
  }
  function settle() {
    clearTimeout(showTimer); clearTimeout(swapTimer); clearTimeout(settleTimer);
    root.classList.remove('pv-loading');
    clearMarks();
    bar.hidden = true;
    live.textContent = 'Pages opened';
  }
  function replay() {
    clearTimeout(showTimer); clearTimeout(swapTimer); clearTimeout(settleTimer);
    root.classList.remove('pv-loading');
    clearMarks();
    bar.hidden = true;
    var scene = scenes[root.dataset.scenario];
    root.dataset.nav = scene.nav;
    root.dataset.ch = scene.ch;
    hint.textContent = scene.hint;
    root.classList.add('pv-loading');
    showTimer = setTimeout(paint, 180);
    swapTimer = setTimeout(swapQueue, 1200);
    settleTimer = setTimeout(settle, 2400);
  }
  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === button)); });
      root.dataset.scenario = button.dataset.scenario;
      replay();
    });
  });
  document.getElementById('pvReplay').addEventListener('click', replay);
  replay();
})();
'''


def main():
    raw = (HERE / 'source.html').read_text(encoding='utf-8')
    match = re.search(r'<body[^>]*>(.*)</body>', raw, re.S)
    if not match:
        raise ValueError('source.html has no <body>')
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', match.group(1), flags=re.S | re.I)
    body, _ = inline_images(body)
    body = re.sub(r'\b(?:href|src)="(?:/static/|/_static/)[^"]*"', 'href="#"', body)
    css, _ = catalogue_css(['tokens.css', 'components.css', 'generate.css'])

    doc = f'''<!doctype html>
<html lang="en" data-theme="dark" data-theme-mode="dark" data-nav="open"
      data-ch="closed" data-read="on" data-home="reading"
      data-section="alkitab" data-bible-edition="tb" data-ch-mode="chapter"
      data-scenario="first">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spec 243 — navigation pending, all sources</title>
<style>{css}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="pv-bar" role="toolbar" aria-label="Navigation sources">
  <span class="pv-bar__title">Fetching from</span>
  <button type="button" data-scenario="rail" aria-pressed="false">Rail</button>
  <button type="button" data-scenario="first" aria-pressed="true">First-level row</button>
  <button type="button" data-scenario="second" aria-pressed="false">Second-level row</button>
  <button type="button" data-scenario="queued" aria-pressed="false">Queued click</button>
  <button type="button" id="pvReplay">Replay</button>
  <span class="pv-bar__hint" id="pvHint"></span>
</div>
<div id="pvProgress" class="pv-progress" role="progressbar" aria-label="Loading page" hidden></div>
<div class="pv-app">
{body}
</div>
<div class="pv-sr" id="pvLive" role="status" aria-live="polite"></div>
<script>
{SCENARIO_JS}
</script>
</body>
</html>
'''
    (HERE / 'index.html').write_text(doc, encoding='utf-8')
    print(f'wrote {HERE / "index.html"} ({len(doc)} bytes)')


if __name__ == '__main__':
    main()
