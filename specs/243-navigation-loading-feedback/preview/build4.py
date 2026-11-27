#!/usr/bin/env python3
"""Spec 243 preview v4: optimistic selection instead of loading chrome.

The click moves the existing selection immediately. On a fast (prefetched)
path the title follows at once; on a slow miss a quiet "Opening…" appears in
the existing title band while the old body stays. Earlier approaches stay on
the page as reference thumbnails linking to their own files.
"""
import base64
import re

from build import HERE, catalogue_css, inline_images

PREVIEW_CSS = r'''
/* ---- Preview chrome ------------------------------------------------------ */
:root { --pv-top: 152px; }
body { padding-top: var(--pv-top); }
.pv-bar {
  position: fixed; inset: 0 0 auto 0; height: var(--pv-top); z-index: 9000;
  display: flex; flex-direction: column; justify-content: center; gap: 5px;
  padding: 6px 12px; background: var(--rail-bg);
  border-bottom: 1px solid var(--divider); color: var(--ink);
  font: 12px/1.3 ui-sans-serif, system-ui, sans-serif;
}
.pv-row { display: flex; align-items: center; gap: 7px; }
.pv-row__label { font-weight: 650; min-width: 72px; opacity: .85; }
.pv-row__hint { margin-left: auto; opacity: .72; white-space: nowrap; }
.pv-bar button {
  border: 1px solid var(--divider); border-radius: 6px; padding: 4px 9px;
  background: transparent; color: inherit; font: inherit; cursor: pointer;
}
.pv-bar button:hover { background: var(--icon-hover-bg); }
.pv-bar button[aria-pressed="true"] { background: var(--active-bg); color: var(--active-ink); border-color: transparent; }
.pv-bar button:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.pv-asset { display: inline-block; background-size: contain; background-repeat: no-repeat; background-position: center; }
.rail, .panel, .chapters, .topbar { top: var(--pv-top) !important; }

/* The reference strip: earlier approaches remain visible and openable. */
.pv-refs { display: flex; align-items: center; gap: 7px; }
.pv-ref {
  display: flex; align-items: center; gap: 6px; padding: 3px 6px 3px 3px;
  border: 1px solid var(--divider); border-radius: 6px; color: inherit;
  text-decoration: none; font: 11px/1.25 ui-sans-serif, system-ui, sans-serif;
}
.pv-ref:hover { background: var(--icon-hover-bg); }
.pv-ref__shot {
  display: block; width: 82px; height: 46px; border-radius: 3px;
  background-size: cover; background-position: top left;
  border: 1px solid var(--divider);
}
.pv-ref__name { font-weight: 600; }
.pv-ref__name small { display: block; font-weight: 400; opacity: .68; }

/* ---- Treatment D: optimistic selection, no loading chrome --------------- */
.pv-opening {
  margin-left: 12px; font: 12px/1.3 ui-sans-serif, system-ui, sans-serif;
  color: var(--head-ink); vertical-align: middle;
}
.pv-opening[hidden] { display: none !important; }
.pv-opening::before {
  content: ""; display: inline-block; width: 6px; height: 6px; margin-right: 6px;
  border-radius: 50%; background: var(--active-bg); vertical-align: 1px;
}
.pv-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
'''

JS = r'''
(function () {
  var root = document.documentElement;
  var hint = document.getElementById('pvHint');
  var name = document.getElementById('readName');
  var number = document.getElementById('readNo');
  var opening = document.getElementById('pvOpening');
  var live = document.getElementById('pvLive');
  var scenarioButtons = [...document.querySelectorAll('.pv-bar button[data-scenario]')];
  var netButtons = [...document.querySelectorAll('.pv-bar button[data-net]')];
  var settleTimer, showTimer;

  var targets = {
    rail:   {sel: '.rail__btn[data-panel="kidung"]', name: 'Kidung', no: ''},
    first:  {sel: '.book[data-name="Keluaran"]', name: 'Keluaran', no: '1'},
    second: {sel: '.ch-num', index: 1, name: 'Kejadian', no: '2'}
  };

  function resetSelection() {
    document.querySelectorAll('.rail__btn[aria-current="page"], .book[aria-current="true"], .ch-num[aria-current="true"]')
      .forEach(function (el) { el.removeAttribute('aria-current'); });
    var rail = document.querySelector('.rail__btn[data-panel="alkitab"]');
    if (rail) rail.setAttribute('aria-current', 'page');
    var book = document.querySelector('.book[data-name="Kejadian"]');
    if (book) book.setAttribute('aria-current', 'true');
    var chapters = document.querySelectorAll('.ch-num');
    if (chapters[0]) chapters[0].setAttribute('aria-current', 'true');
    name.textContent = 'Kejadian';
    number.textContent = '1';
    number.hidden = false;
    opening.hidden = true;
  }
  function targetElement(t) {
    if (t.index === undefined) return document.querySelector(t.sel);
    return document.querySelectorAll(t.sel)[t.index];
  }
  function replay() {
    clearTimeout(settleTimer); clearTimeout(showTimer);
    resetSelection();
    var scenario = root.dataset.scenario;
    var t = targets[scenario];
    var el = targetElement(t);
    /* 0 ms: the existing selection moves to the target — this is the feedback.
       Only one item per list carries aria-current; the base mark is replaced. */
    var group = scenario === 'rail' ? '.rail__btn'
      : scenario === 'first' ? '.book' : '.ch-num';
    document.querySelectorAll(group + '[aria-current]').forEach(function (x) {
      x.removeAttribute('aria-current');
    });
    if (el) el.setAttribute('aria-current',
      el.classList.contains('rail__btn') ? 'page' : 'true');
    root.dataset.nav = 'open';
    root.dataset.ch = scenario === 'second' ? 'open' : 'closed';
    hint.textContent = root.dataset.net === 'fast'
      ? 'prefetched hit · selection moves now · title follows immediately'
      : 'cache miss · selection moves now · 300 ms title notice';
    live.textContent = 'Opening ' + t.name;
    var settle = function () {
      name.textContent = t.name;
      if (t.no) { number.textContent = t.no; number.hidden = false; }
      else number.hidden = true;
      opening.hidden = true;
      live.textContent = t.name + ' opened';
    };
    if (root.dataset.net === 'slow') {
      showTimer = setTimeout(function () { opening.hidden = false; }, 300);
      settleTimer = setTimeout(settle, 2400);
    } else {
      settleTimer = setTimeout(settle, 200);
    }
  }
  scenarioButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      scenarioButtons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      root.dataset.scenario = b.dataset.scenario;
      replay();
    });
  });
  netButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      netButtons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      root.dataset.net = b.dataset.net;
      replay();
    });
  });
  document.getElementById('pvReplay').addEventListener('click', replay);
  /* Clicking the real shell works too: the delegated handlers own the click. */
  document.addEventListener('click', function (event) {
    if (event.target.closest('.pv-bar, .pv-refs')) return;
    var scenario = null;
    if (event.target.closest('.rail__btn[data-panel]')) scenario = 'rail';
    else if (event.target.closest('.book')) scenario = 'first';
    else if (event.target.closest('.ch-num')) scenario = 'second';
    if (!scenario) return;
    event.preventDefault();
    root.dataset.scenario = scenario;
    scenarioButtons.forEach(function (x) {
      x.setAttribute('aria-pressed', String(x.dataset.scenario === scenario));
    });
    replay();
  });
  replay();
})();
'''


def thumb(filename):
    data = (HERE / filename).read_bytes()
    return 'data:image/png;base64,' + base64.b64encode(data).decode()


def main():
    raw = (HERE / 'source.html').read_text(encoding='utf-8')
    match = re.search(r'<body[^>]*>(.*)</body>', raw, re.S)
    if not match:
        raise ValueError('source.html has no <body>')
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', match.group(1), flags=re.S | re.I)
    body, _ = inline_images(body)
    body = re.sub(r'\b(?:href|src)="(?:/static/|/_static/)[^"]*"', 'href="#"', body)
    body = body.replace('<span class="read__no" id="readNo">1</span>',
                        '<span class="read__no" id="readNo">1</span>'
                        '<span class="pv-opening" id="pvOpening" hidden>Opening…</span>', 1)
    css, _ = catalogue_css(['tokens.css', 'components.css', 'generate.css'])

    refs = [
        ('index-v1.html', 'shot-a.png', 'v1', 'global bar + row'),
        ('index-v2.html', 'shot-queued.png', 'v2', 'source marks + queue'),
        ('index-v3.html', 'shot3-skeleton-first.png', 'v3', 'skeleton / strip'),
    ]
    ref_html = ''.join(
        f'<a class="pv-ref" href="{href}">'
        f'<span class="pv-ref__shot" style="background-image:url({thumb(shot)})"></span>'
        f'<span class="pv-ref__name">{label}<small>{sub}</small></span></a>'
        for href, shot, label, sub in refs)

    doc = f'''<!doctype html>
<html lang="en" data-theme="dark" data-theme-mode="dark" data-nav="open"
      data-ch="closed" data-read="on" data-home="reading"
      data-section="alkitab" data-bible-edition="tb" data-ch-mode="chapter"
      data-scenario="first" data-net="slow">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spec 243 — optimistic selection (v4)</title>
<style>{css}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="pv-bar" role="toolbar" aria-label="Loading approach options">
  <div class="pv-row">
    <span class="pv-row__label">Approach</span>
    <button type="button" aria-pressed="true">D · Optimistic selection</button>
    <button type="button" data-net="slow" aria-pressed="true">Slow miss</button>
    <button type="button" data-net="fast" aria-pressed="false">Prefetched hit</button>
    <span class="pv-row__hint" id="pvHint"></span>
  </div>
  <div class="pv-row">
    <span class="pv-row__label">Clicked from</span>
    <button type="button" data-scenario="rail" aria-pressed="false">Rail</button>
    <button type="button" data-scenario="first" aria-pressed="true">First-level row</button>
    <button type="button" data-scenario="second" aria-pressed="false">Second-level row</button>
    <button type="button" id="pvReplay">Replay</button>
    <span class="pv-row__hint">no bar, no spinner, no dim · the selection itself moves</span>
  </div>
  <div class="pv-row pv-refs">
    <span class="pv-row__label">Previous</span>
    {ref_html}
    <span class="pv-row__hint">thumbnails link to their full preview files</span>
  </div>
</div>
<div class="pv-app">
{body}
</div>
<div class="pv-sr" id="pvLive" role="status" aria-live="polite"></div>
<script>
{JS}
</script>
</body>
</html>
'''
    (HERE / 'index.html').write_text(doc, encoding='utf-8')
    print(f'wrote {HERE / "index.html"} ({len(doc)} bytes)')


if __name__ == '__main__':
    main()
