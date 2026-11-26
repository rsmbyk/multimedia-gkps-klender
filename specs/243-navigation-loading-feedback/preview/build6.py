#!/usr/bin/env python3
"""Spec 243 preview v6: list-only fetches leave the reading page untouched.

Extends v5 with explicit rail-list and sidebar-list scenarios. The three row
variants, stage-changing cases, cancellation rules and v1-v5 references remain.
"""
import base64
import re

from build import HERE, catalogue_css, inline_images

PREVIEW_CSS = r'''
/* ---- Preview chrome ------------------------------------------------------ */
:root { --pv-top: 150px; }
body { padding-top: var(--pv-top); }
.pv-bar {
  position: fixed; inset: 0 0 auto 0; height: var(--pv-top); z-index: 9000;
  display: flex; flex-direction: column; justify-content: center; gap: 5px;
  padding: 6px 12px; background: var(--rail-bg);
  border-bottom: 1px solid var(--divider); color: var(--ink);
  font: 12px/1.3 ui-sans-serif, system-ui, sans-serif;
}
.pv-row { display: flex; align-items: center; gap: 6px; }
.pv-row__label { font-weight: 650; min-width: 78px; opacity: .85; }
.pv-row__hint { margin-left: auto; opacity: .75; white-space: nowrap; }
.pv-bar button {
  border: 1px solid var(--divider); border-radius: 6px; padding: 4px 8px;
  background: transparent; color: inherit; font: inherit; cursor: pointer;
}
.pv-bar button:hover { background: var(--icon-hover-bg); }
.pv-bar button[aria-pressed="true"] { background: var(--active-bg); color: var(--active-ink); border-color: transparent; }
.pv-bar button:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.pv-asset { display: inline-block; background-size: contain; background-repeat: no-repeat; background-position: center; }
.rail, .panel, .chapters, .topbar { top: var(--pv-top) !important; }
.pv-refs { display: flex; align-items: center; gap: 6px; }
.pv-ref { display: flex; align-items: center; gap: 6px; padding: 3px 6px 3px 3px; border: 1px solid var(--divider); border-radius: 6px; color: inherit; text-decoration: none; font: 11px/1.25 ui-sans-serif, system-ui, sans-serif; }
.pv-ref:hover { background: var(--icon-hover-bg); }
.pv-ref__shot { display: block; width: 76px; height: 43px; border-radius: 3px; background-size: cover; background-position: top left; border: 1px solid var(--divider); }
.pv-ref__name { font-weight: 600; }
.pv-ref__name small { display: block; font-weight: 400; opacity: .68; }

/* ---- R1: the clicked item locks ----------------------------------------- */
@keyframes pv-spin { to { transform: rotate(360deg); } }
.pv-spin {
  display: inline-block; width: 13px; height: 13px; flex: none;
  border: 2px solid var(--divider); border-top-color: var(--active-bg);
  border-radius: 50%; animation: pv-spin .8s linear infinite;
}
.pv-rail-busy > svg { display: none; }
.pv-rail-busy::after {
  content: ""; display: block; width: 18px; height: 18px;
  border: 2px solid var(--divider); border-top-color: var(--active-bg);
  border-radius: 50%; animation: pv-spin .8s linear infinite;
}
.pv-row-busy { pointer-events: none !important; opacity: .58; }
.pv-row-busy::after {
  content: ""; position: absolute; right: 9px; top: 50%; width: 12px; height: 12px;
  margin-top: -6px; border: 2px solid var(--divider);
  border-top-color: var(--active-bg); border-radius: 50%;
  animation: pv-spin .8s linear infinite;
}
html[data-rowstyle="b"] .pv-row-busy { opacity: 1; }
html[data-rowstyle="b"] .pv-row-busy .book__a,
html[data-rowstyle="b"] .pv-row-busy .ch-num__n { visibility: hidden; }
html[data-rowstyle="b"] .pv-row-busy::after { right: auto; left: 11px; }
html[data-rowstyle="c"] .pv-row-busy::after { display: none; }
.book, .ch-num { position: relative !important; }

/* ---- R2: reading page disabled, bar above it, prefilled placeholder ------ */
.stage { position: relative !important; }
.stage[aria-busy="true"] { pointer-events: none !important; }
.stage[aria-busy="true"] .read { visibility: hidden; }
.pv-stagebar {
  position: absolute; top: 0; left: 0; right: 0; height: 3px; z-index: 8;
  overflow: hidden; background: color-mix(in srgb, var(--active-bg) 20%, transparent);
}
.pv-stagebar[hidden] { display: none !important; }
.pv-stagebar::before {
  content: ""; position: absolute; top: 0; bottom: 0; width: 28%;
  background: var(--active-bg); animation: pv-slide 1.05s var(--ease-timing) infinite;
}
@keyframes pv-slide { from { transform: translateX(-100%); } to { transform: translateX(460%); } }
.pv-placeholder {
  position: absolute; inset: 0 0 auto 0; z-index: 7; padding: 30px 42px;
  background: var(--canvas); color: var(--ink);
  font: 16px/1.5 ui-sans-serif, system-ui, sans-serif;
}
.pv-placeholder[hidden] { display: none !important; }
.pv-ph__eyebrow { margin: 0 0 6px; font: 12px/1.3 ui-sans-serif, system-ui, sans-serif; color: var(--head-ink); letter-spacing: .04em; }
.pv-ph__title { margin: 0; font: 600 32px/1.2 var(--font-serif); }
.pv-ph__meta { margin: 8px 0 26px; font: 13px/1.4 ui-sans-serif, system-ui, sans-serif; color: var(--head-ink); }
.pv-ph__line { height: 12px; margin: 13px 0; border-radius: 4px; background: var(--divider); opacity: .55; }
.pv-ph__line:nth-of-type(1) { width: 88%; }
.pv-ph__line:nth-of-type(2) { width: 94%; }
.pv-ph__line:nth-of-type(3) { width: 67%; }
.pv-ph__line:nth-of-type(4) { width: 83%; }
.pv-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
@media (prefers-reduced-motion: reduce) {
  .pv-spin, .pv-rail-busy::after, .pv-row-busy::after, .pv-stagebar::before { animation: none; }
}
'''

JS = r'''
(function () {
  var root = document.documentElement;
  var status = document.getElementById('pvStatus');
  var bar = document.getElementById('pvStagebar');
  var ph = document.getElementById('pvPlaceholder');
  var title = document.getElementById('pvPhTitle');
  var meta = document.getElementById('pvPhMeta');
  var live = document.getElementById('pvLive');
  var styleButtons = [...document.querySelectorAll('.pv-bar button[data-rowstyle]')];
  var scenarioButtons = [...document.querySelectorAll('.pv-bar button[data-scenario]')];
  var timers = [];
  var locked = [];

  function el(sel, index) {
    var nodes = document.querySelectorAll(sel);
    return index === undefined ? nodes[0] : nodes[index];
  }
  function dataOf(node, kind) {
    if (kind === 'rail') return {t: node.querySelector('.rail__name').textContent.trim(), m: 'section'};
    if (kind === 'book') return {t: node.dataset.name, m: (node.querySelector('.book__a') || {}).textContent || ''};
    if (kind === 'chapter') return {t: el('.book[aria-current]') ? el('.book[aria-current]').dataset.name : 'Kejadian', m: 'chapter ' + node.textContent.trim()};
    return {t: 'Tata Ibadah mode', m: 'list only'};
  }
  function lock(node, kind) {
    if (!node) return;
    node.classList.add(kind === 'rail' ? 'pv-rail-busy' : 'pv-row-busy');
    node.setAttribute('aria-disabled', 'true');
    locked.push(node);
  }
  function unlock(node) {
    if (!node) return;
    node.classList.remove('pv-rail-busy', 'pv-row-busy');
    node.removeAttribute('aria-disabled');
    locked = locked.filter(function (n) { return n !== node; });
  }
  function stageOn(d) {
    title.textContent = d.t; meta.textContent = d.m;
    bar.hidden = false; ph.hidden = false;
    document.querySelector('.stage').setAttribute('aria-busy', 'true');
  }
  function stageOff() {
    bar.hidden = true; ph.hidden = true;
    document.querySelector('.stage').removeAttribute('aria-busy');
  }
  function later(fn, ms) { var id = setTimeout(fn, ms); timers.push(id); return id; }
  function reset() {
    timers.forEach(clearTimeout); timers = [];
    locked.forEach(unlock); locked = [];
    stageOff(); status.textContent = ''; live.textContent = '';
  }
  function replay() {
    reset();
    var s = root.dataset.scenario;
    var rail = el('.rail__btn[data-panel="kidung"]');
    var bookA = el('.book[data-name="Keluaran"]');
    var bookB = el('.book[data-name="Imamat"]');
    var chapter = el('.ch-num', 1);
    /* The already-current book toggles its chapter list in place (reading.js:820-826),
       so it is the real list-only sidebar item in this snapshot. */
    var listOnly = el('.book[data-name="Kejadian"]') || el('#tatibMode') || el('.panel__mode');
    var railList = el('.rail__btn[data-panel="alkitab"]');
    var railD = dataOf(rail, 'rail'), aD = dataOf(bookA, 'book');
    var bD = dataOf(bookB, 'book'), chD = dataOf(chapter, 'chapter');

    if (s === 'rail-stage') {
      lock(rail, 'rail'); stageOn(railD);
      status.textContent = 'Rail locked · reading page disabled · placeholder seeded from rail label';
      live.textContent = 'Opening ' + railD.t;
      later(function () { unlock(rail); stageOff(); status.textContent = 'Opened ' + railD.t; live.textContent = railD.t + ' opened'; }, 1800);
    } else if (s === 'sidebar-stage') {
      lock(bookA, 'book'); stageOn(aD);
      status.textContent = 'Row locked · reading page disabled · placeholder seeded from ' + aD.t;
      live.textContent = 'Opening ' + aD.t;
      later(function () { unlock(bookA); stageOff(); status.textContent = 'Opened ' + aD.t; live.textContent = aD.t + ' opened'; }, 1800);
    } else if (s === 'list-only' || s === 'sidebar-list') {
      lock(listOnly, 'book');
      status.textContent = 'Sidebar list fetching · reading page kept as displayed · no bar, no placeholder';
      live.textContent = 'Updating sidebar list';
      later(function () { unlock(listOnly); status.textContent = 'Sidebar list updated · reading page unchanged'; live.textContent = 'Sidebar list updated'; }, 1800);
    } else if (s === 'rail-list') {
      lock(railList, 'rail');
      status.textContent = 'Rail list fetching · reading page kept as displayed · no bar, no placeholder';
      live.textContent = 'Updating rail section';
      later(function () { unlock(railList); status.textContent = 'Rail list updated · reading page unchanged'; live.textContent = 'Rail list updated'; }, 1800);
    } else if (s === 'cancel-stage-stage') {
      lock(bookA, 'book'); stageOn(aD);
      status.textContent = aD.t + ' fetching';
      later(function () {
        unlock(bookA); lock(bookB, 'book'); stageOn(bD);
        status.textContent = aD.t + ' cancelled · ' + bD.t + ' fetching';
        live.textContent = 'Opening ' + bD.t;
      }, 700);
      later(function () { unlock(bookB); stageOff(); status.textContent = 'Opened ' + bD.t; live.textContent = bD.t + ' opened'; }, 1800);
    } else if (s === 'cancel-stage-list') {
      lock(bookA, 'book'); stageOn(aD);
      status.textContent = aD.t + ' fetching';
      later(function () {
        lock(listOnly, 'list');
        status.textContent = aD.t + ' continues (new click does not change the page) · list fetching';
      }, 700);
      later(function () {
        unlock(bookA); unlock(listOnly); stageOff();
        status.textContent = aD.t + ' opened · list updated';
        live.textContent = aD.t + ' opened';
      }, 1800);
    } else if (s === 'cancel-list-stage') {
      lock(listOnly, 'list');
      status.textContent = 'List fetching';
      later(function () {
        unlock(listOnly); lock(chapter, 'chapter'); stageOn(chD);
        status.textContent = 'List cancelled · chapter fetching · reading page disabled';
        live.textContent = 'Opening ' + chD.t;
      }, 700);
      later(function () { unlock(chapter); stageOff(); status.textContent = 'Opened ' + chD.t; live.textContent = chD.t + ' opened'; }, 1800);
    }
  }
  styleButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      styleButtons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      root.dataset.rowstyle = b.dataset.rowstyle; replay();
    });
  });
  scenarioButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      scenarioButtons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      root.dataset.scenario = b.dataset.scenario; replay();
    });
  });
  document.getElementById('pvReplay').addEventListener('click', replay);
  replay();
})();
'''


def thumb(filename):
    return 'data:image/png;base64,' + base64.b64encode((HERE / filename).read_bytes()).decode()


def main():
    raw = (HERE / 'source.html').read_text(encoding='utf-8')
    match = re.search(r'<body[^>]*>(.*)</body>', raw, re.S)
    if not match:
        raise ValueError('source.html has no <body>')
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', match.group(1), flags=re.S | re.I)
    body, _ = inline_images(body)
    body = re.sub(r'\b(?:href|src)="(?:/static/|/_static/)[^"]*"', 'href="#"', body)
    stage_insert = (
        '<div class="pv-stagebar" id="pvStagebar" hidden></div>'
        '<div class="pv-placeholder" id="pvPlaceholder" hidden>'
        '<p class="pv-ph__eyebrow">OPENING</p>'
        '<h2 class="pv-ph__title" id="pvPhTitle"></h2>'
        '<p class="pv-ph__meta" id="pvPhMeta"></p>'
        + ''.join('<div class="pv-ph__line"></div>' for _ in range(4))
        + '</div>')
    body = body.replace('<main class="stage">', '<main class="stage">' + stage_insert, 1)
    css, _ = catalogue_css(['tokens.css', 'components.css', 'generate.css'])

    refs = [
        ('index-v1.html', 'shot-a.png', 'v1', 'global bar'),
        ('index-v2.html', 'shot-queued.png', 'v2', 'source marks'),
        ('index-v3.html', 'shot3-skeleton-first.png', 'v3', 'skeleton / strip'),
        ('index-v4.html', 'shot4-slow-first.png', 'v4', 'optimistic'),
        ('index-v5.html', 'shot5-row-a.png', 'v5', 'lock + placeholder'),
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
      data-rowstyle="a" data-scenario="sidebar-list">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spec 243 — owner rules preview v5</title>
<style>{css}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="pv-bar" role="toolbar" aria-label="Navigation rules preview">
  <div class="pv-row">
    <span class="pv-row__label">Disabled row</span>
    <button type="button" data-rowstyle="a" aria-pressed="true">A · dim + spinner right</button>
    <button type="button" data-rowstyle="b" aria-pressed="false">B · leading mark → spinner</button>
    <button type="button" data-rowstyle="c" aria-pressed="false">C · dim only</button>
    <span class="pv-row__hint" id="pvStatus"></span>
  </div>
  <div class="pv-row">
    <span class="pv-row__label">Scenario</span>
    <button type="button" data-scenario="rail-stage" aria-pressed="false">Rail → page</button>
    <button type="button" data-scenario="sidebar-stage" aria-pressed="false">Row → page</button>
    <button type="button" data-scenario="rail-list" aria-pressed="false">Rail list only</button>
    <button type="button" data-scenario="sidebar-list" aria-pressed="true">Sidebar list only</button>
    <button type="button" data-scenario="cancel-stage-stage" aria-pressed="false">Cancel page → page</button>
    <button type="button" data-scenario="cancel-stage-list" aria-pressed="false">Cancel page → list</button>
    <button type="button" data-scenario="cancel-list-stage" aria-pressed="false">Cancel list → page</button>
    <button type="button" id="pvReplay">Replay</button>
  </div>
  <div class="pv-row pv-refs">
    <span class="pv-row__label">Previous</span>
    {ref_html}
    <span class="pv-row__hint">rules draft: rules-v5-draft.md</span>
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
