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
:root { --pv-top: 178px; }
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
.pv-rail-spin {
  display: block; width: 18px; height: 18px; box-sizing: border-box;
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
.book, .ch-num, .songrow { position: relative !important; }

/* ---- Alternatives to the rotating spinner -------------------------------- */
.pv-lock-label {
  font: 600 11px/1.2 ui-sans-serif, system-ui, sans-serif;
  color: var(--active-bg); white-space: nowrap;
}
.pv-lock-edge {
  position: absolute; left: 0; right: 0; bottom: 0; height: 2px;
  background: var(--active-bg); transform-origin: left center;
  animation: pv-edge 1.2s var(--ease-timing) infinite;
}
@keyframes pv-edge { from { transform: scaleX(.04); opacity: .95; } to { transform: scaleX(1); opacity: .25; } }
@property --pv-fill { syntax: "<angle>"; inherits: false; initial-value: 0deg; }
.pv-lock-ring {
  width: 18px; height: 18px; box-sizing: border-box; border-radius: 50%;
  background: conic-gradient(var(--active-bg) var(--pv-fill), var(--divider) 0);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #000 0);
  mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #000 0);
  animation: pv-fill 1.4s linear infinite;
}
@keyframes pv-fill { to { --pv-fill: 360deg; } }
html[data-lockstyle="label"] .pv-row-busy,
html[data-lockstyle="edge"] .pv-row-busy,
html[data-lockstyle="ring"] .pv-row-busy { opacity: 1; }
html[data-lockstyle="label"] .pv-rail-spin,
html[data-lockstyle="edge"] .pv-rail-spin,
html[data-lockstyle="ring"] .pv-rail-spin,
html[data-lockstyle="dim"] .pv-rail-spin { display: none; }
html[data-lockstyle="label"] .pv-row-busy::after,
html[data-lockstyle="edge"] .pv-row-busy::after,
html[data-lockstyle="ring"] .pv-row-busy::after,
html[data-lockstyle="dim"] .pv-row-busy::after { display: none; }
html[data-lockstyle="label"] .pv-locked .rail__name,
html[data-lockstyle="label"] .pv-locked .book__a,
html[data-lockstyle="label"] .pv-locked .ch-num__n { visibility: hidden; }
html[data-lockstyle="dim"] .pv-locked > svg { opacity: .45; }
html[data-lockstyle="label"] .pv-rail-busy > svg,
html[data-lockstyle="edge"] .pv-rail-busy > svg,
html[data-lockstyle="ring"] .pv-rail-busy > svg,
html[data-lockstyle="dim"] .pv-rail-busy > svg { display: block; }
html[data-lockstyle="label"] .pv-rail-busy .pv-lock-label {
  position: absolute; left: 50%; bottom: 1px; transform: translateX(-50%);
  padding: 0 4px; border-radius: 6px; font-size: 12px; line-height: 13px;
  background: var(--tip-bg); color: var(--tip-ink);
}

/* ---- R2: reading page disabled, bar above it, prefilled placeholder ------ */
.stage { position: relative !important; }
#panelBody, #chBody { position: relative !important; }
.pv-section-bar {
  position: absolute; top: 0; left: 0; right: 0; height: 3px; z-index: 8;
  overflow: hidden; background: color-mix(in srgb, var(--active-bg) 20%, transparent);
}
.pv-section-bar[hidden] { display: none !important; }
.pv-section-bar::before {
  content: ""; position: absolute; top: 0; bottom: 0; width: 28%;
  background: var(--active-bg); animation: pv-slide 1.05s var(--ease-timing) infinite;
}
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
/* Placeholder uses the real article anatomy: read__head / read__row /
   read__title / read__body with the product's own verse and entry classes. */
.stage[aria-busy="true"] > .pv-placeholder .read { visibility: visible !important; }
.pv-placeholder {
  position: absolute; inset: 0 0 auto 0; z-index: 7;
  /* Same offsets as the real .read inside .stage: top --pad-top, horizontal
     clamp(24px, 5vw, 64px). Without this the skeleton hugs the stage corner. */
  padding: var(--stage-pad-top) clamp(24px, 5vw, 64px) 0;
  background: var(--canvas); color: var(--ink);
}
.pv-placeholder[hidden] { display: none !important; }
@media (max-width: 720px) {
  .pv-placeholder { padding-left: 18px; padding-right: 18px; }
}
.pv-placeholder .read { pointer-events: none; }
.pv-ph-bar {
  display: block; height: 12px; border-radius: 4px;
  background: var(--divider); opacity: .55;
}
.pv-ph-bar--title { height: 24px; width: 62%; }
.pv-ph-bar--sec { height: 18px; width: 78%; margin: 0 0 6px; }
.pv-ph-bar--sub { height: 10px; width: 28%; }
.pv-ph-bar--verse { height: 12px; width: 88%; }
.pv-ph-bar--line { height: 11px; width: 94%; margin-top: 7px; }
.pv-ph-bar--line:nth-child(2) { width: 82%; }
.pv-ph-bar--line:nth-child(3) { width: 67%; }
.pv-ph-bar--wide { width: 96%; }
.pv-ph-bar--mid { width: 74%; }
.pv-ph-bar--short { width: 53%; }
.pv-ph-bar--entry { height: 20px; width: 58%; }
/* ---- Leaf items used as stage-writing examples --------------------------- */
.pv-leaf { display: none !important; }
html[data-scenario="song-page"] .pv-leaf--song,
html[data-scenario="verse-page"] .pv-leaf--verse,
html[data-scenario="service-page"] .pv-leaf--service,
html[data-scenario="cancel-page-page"] .pv-leaf--song,
html[data-scenario="cancel-page-list"] .pv-leaf--song,
html[data-scenario="cancel-list-page"] .pv-leaf--service { display: flex !important; }
.pv-leaf--verse {
  align-items: center; gap: 9px; margin: 0; padding: 0 11px; height: 38px;
  border-bottom: 1px solid var(--divider); font: 14px/1.3 var(--font-serif);
}
.pv-leaf--verse .v__n { color: var(--head-ink); font-size: 12px; }
.pv-sources { margin-top: 1px; }
.pv-sources .pv-leaf {
  align-items: center; gap: 6px; margin: 0; padding: 2px 7px; height: 22px;
  border: 1px solid var(--divider); border-radius: 5px;
  font: 11px/1.2 ui-sans-serif, system-ui, sans-serif; white-space: nowrap;
}
.pv-sources .songrow__c, .pv-sources .v__n { color: var(--head-ink); font-size: 10px; }
.pv-sources .songrow__t { font-weight: 600; }
.pv-sources .pv-row__hint { font-size: 11px; }
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
  var panelBar = document.getElementById('pvPanelBar');
  var chBar = document.getElementById('pvChBar');
  var placeholders = {
    bible: document.getElementById('pvPh-bible'),
    song: document.getElementById('pvPh-song'),
    service: document.getElementById('pvPh-service')
  };
  var live = document.getElementById('pvLive');
  var styleButtons = [...document.querySelectorAll('.pv-bar button[data-lockstyle]')];
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
    var rail = kind === 'rail';
    node.classList.add('pv-locked', rail ? 'pv-rail-busy' : 'pv-row-busy');
    var style = root.dataset.lockstyle;
    var cls = style === 'spinner' ? (rail ? 'pv-rail-spin' : null)
      : style === 'label' ? 'pv-lock-label'
      : style === 'edge' ? 'pv-lock-edge'
      : style === 'ring' ? 'pv-lock-ring' : null;
    if (cls) {
      var mark = document.createElement('span');
      mark.className = cls;
      if (cls === 'pv-lock-label') mark.textContent = rail ? '…' : 'Opening…';
      mark.setAttribute('aria-hidden', 'true');
      node.appendChild(mark);
    }
    node.setAttribute('aria-disabled', 'true');
    locked.push(node);
  }
  function unlock(node) {
    if (!node) return;
    node.classList.remove('pv-locked', 'pv-rail-busy', 'pv-row-busy');
    node.querySelectorAll('.pv-rail-spin, .pv-lock-label, .pv-lock-edge, .pv-lock-ring')
      .forEach(function (m) { m.remove(); });
    node.removeAttribute('aria-disabled');
    locked = locked.filter(function (n) { return n !== node; });
  }
  function stageOn(d) {
    Object.keys(placeholders).forEach(function (k) { placeholders[k].hidden = k !== d.kind; });
    var ph = placeholders[d.kind];
    ph.querySelector('.pv-ph-name').textContent = d.t;
    var no = ph.querySelector('.pv-ph-no');
    if (no) { no.textContent = d.no || ''; no.hidden = !d.no; }
    var eyebrow = ph.querySelector('.pv-ph-eyebrow');
    if (eyebrow) { eyebrow.textContent = d.eyebrow || ''; eyebrow.hidden = !d.eyebrow; }
    bar.hidden = false;
    document.querySelector('.stage').setAttribute('aria-busy', 'true');
  }
  function stageOff() {
    bar.hidden = true;
    Object.keys(placeholders).forEach(function (k) { placeholders[k].hidden = true; });
    document.querySelector('.stage').removeAttribute('aria-busy');
  }
  function barsOn(which) {
    panelBar.hidden = which.indexOf('panel') < 0;
    chBar.hidden = which.indexOf('ch') < 0;
  }
  function later(fn, ms) { var id = setTimeout(fn, ms); timers.push(id); return id; }
  function reset() {
    timers.forEach(clearTimeout); timers = [];
    locked.forEach(unlock); locked = [];
    stageOff(); barsOn([]); status.textContent = ''; live.textContent = '';
  }
  function replay() {
    reset();
    root.dataset.nav = 'open';
    root.dataset.ch = 'open';
    var s = root.dataset.scenario;
    var rail = el('.rail__btn[data-panel="kidung"]');
    var bookA = el('.book[data-name="Keluaran"]');
    var bookB = el('.book[data-name="Imamat"]');
    var chapter = el('.ch-num', 1);
    /* The already-current book toggles its chapter list in place (reading.js:820-826),
       so it is the real list-only sidebar item in this snapshot. */
    var listOnly = el('.book[data-name="Kejadian"]') || el('#tatibMode') || el('.panel__mode');
    var railList = el('.rail__btn[data-panel="alkitab"]');
    var railD = dataOf(rail, 'rail');
    var songD = {t: 'Jahowa Sihol Pujionku', no: '', eyebrow: 'HAL 1', kind: 'song'};
    var verseD = {t: 'Kejadian', no: '1', eyebrow: '', kind: 'bible'};
    var serviceD = {t: 'Service 111ojo', no: '', eyebrow: 'Tata Ibadah', kind: 'service'};

    if (s === 'rail-list') {
      lock(railList, 'rail'); barsOn(['panel', 'ch']);
      status.textContent = 'Rail list fetching · bars on first- and second-level · reading page kept';
      live.textContent = 'Updating rail section';
      later(function () { unlock(railList); barsOn([]); status.textContent = 'Rail list updated · reading page unchanged'; live.textContent = 'Rail list updated'; }, 1800);
    } else if (s === 'chapter-list') {
      lock(chapter, 'chapter'); barsOn(['ch']);
      status.textContent = 'Chapter list fetching · bar on second-level · reading page kept';
      live.textContent = 'Updating chapter list';
      later(function () { unlock(chapter); barsOn([]); status.textContent = 'Chapter list updated · reading page unchanged'; live.textContent = 'Chapter list updated'; }, 1800);
    } else if (s === 'songbook-list') {
      lock(bookA, 'book'); barsOn(['ch']);
      status.textContent = 'Songbook list fetching · bar on second-level · reading page kept';
      live.textContent = 'Updating songbook list';
      later(function () { unlock(bookA); barsOn([]); status.textContent = 'Songbook list updated · reading page unchanged'; live.textContent = 'Songbook list updated'; }, 1800);
    } else if (s === 'song-page' || s === 'verse-page' || s === 'service-page') {
      var leaf = s === 'song-page' ? el('.pv-leaf--song')
        : s === 'verse-page' ? el('.pv-leaf--verse') : el('.pv-leaf--service');
      var d = s === 'song-page' ? songD : s === 'verse-page' ? verseD : serviceD;
      lock(leaf, 'book'); stageOn(d); barsOn([]);
      status.textContent = d.t + ' writes to the reading page · page disabled · bar + seeded placeholder';
      live.textContent = 'Opening ' + d.t;
      later(function () { unlock(leaf); stageOff(); status.textContent = 'Opened ' + d.t; live.textContent = d.t + ' opened'; }, 1800);
    } else if (s === 'cancel-page-page') {
      var songLeaf = el('.pv-leaf--song'), verseLeaf = el('.pv-leaf--verse');
      lock(songLeaf, 'book'); stageOn(songD); barsOn([]);
      status.textContent = songD.t + ' writing';
      later(function () {
        unlock(songLeaf); lock(verseLeaf, 'book'); stageOn(verseD); barsOn([]);
        status.textContent = songD.t + ' cancelled · ' + verseD.t + ' writing';
        live.textContent = 'Opening ' + verseD.t;
      }, 700);
      later(function () { unlock(verseLeaf); stageOff(); status.textContent = 'Opened ' + verseD.t; live.textContent = verseD.t + ' opened'; }, 1800);
    } else if (s === 'cancel-page-list') {
      var song2 = el('.pv-leaf--song');
      lock(song2, 'book'); stageOn(songD); barsOn([]);
      status.textContent = songD.t + ' writing';
      later(function () {
        lock(bookA, 'book'); barsOn(['ch']);
        status.textContent = songD.t + ' continues · songbook fetch adds second-level bar';
      }, 700);
      later(function () {
        unlock(song2); unlock(bookA); stageOff(); barsOn([]);
        status.textContent = songD.t + ' opened · songbook list updated';
        live.textContent = songD.t + ' opened';
      }, 1800);
    } else if (s === 'cancel-list-page') {
      var chapter2 = el('.ch-num', 1), service2 = el('.pv-leaf--service');
      lock(chapter2, 'chapter'); barsOn(['ch']);
      status.textContent = 'Chapter list fetching · bar on second-level';
      later(function () {
        unlock(chapter2); lock(service2, 'book'); stageOn(serviceD); barsOn([]);
        status.textContent = 'Chapter list cancelled · service writes to the reading page';
        live.textContent = 'Opening ' + serviceD.t;
      }, 700);
      later(function () { unlock(service2); stageOff(); barsOn([]); status.textContent = 'Opened ' + serviceD.t; live.textContent = serviceD.t + ' opened'; }, 1800);
    }
  }
  styleButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      styleButtons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      root.dataset.lockstyle = b.dataset.lockstyle; replay();
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
    def verse_rows(count, lines=1):
        out = []
        for n in range(1, count + 1):
            bars = ''.join('<span class="pv-ph-bar pv-ph-bar--line"></span>'
                           for _ in range(lines))
            out.append(f'<p class="v"><span class="v__n">{n}</span>'
                       f'<span class="v__text">{bars}</span></p>')
        return ''.join(out)

    def service_rows(count):
        return ''.join(
            '<section class="tatib__item">'
            '<h2 class="read__sec"><span class="pv-ph-bar pv-ph-bar--entry '
            + ('pv-ph-bar--wide' if i == 0 else 'pv-ph-bar--mid') + '"></span></h2>'
            '<p class="read__sub"><span class="pv-ph-bar pv-ph-bar--sub"></span></p>'
            '</section>' for i in range(count))

    stage_insert = (
        '<div class="pv-stagebar" id="pvStagebar" hidden></div>'
        '<div class="pv-placeholder" id="pvPh-bible" hidden>'
        '<article class="read" data-kind="bible" lang="tb">'
        '<header class="read__head"><div class="read__head-top">'
        '<p class="read__eyebrow" hidden></p></div><div class="read__row">'
        '<h1 class="read__title"><span class="pv-ph-name">Kejadian</span> '
        '<span class="read__no pv-ph-no">1</span></h1>'
        '<div class="read__lang" role="group" aria-label="Choose reading translation" '
        'data-edition="tb"><span class="read__lang-thumb" aria-hidden="true"></span>'
        '<a aria-pressed="true">TB</a><a aria-pressed="false">SIM</a></div>'
        '<div class="read__project"><button type="button" class="read__project-btn" '
        'aria-label="Project">Project</button></div>'
        '</div></header><div class="read__body"><div class="read__ed" data-ed="tb">'
        '<h2 class="read__sec"><span class="pv-ph-bar pv-ph-bar--sec '
        'pv-ph-bar--mid"></span></h2>' + verse_rows(5) +
        '</div></div></article></div>'
        '<div class="pv-placeholder" id="pvPh-song" hidden>'
        '<article class="read" data-kind="song" lang="id">'
        '<header class="read__head"><div class="read__head-top">'
        '<p class="read__eyebrow pv-ph-eyebrow">HAL 1</p>'
        '<div class="read__project"><button type="button" class="read__project-btn" '
        'aria-label="Project">Project</button></div></div><div class="read__row">'
        '<h1 class="read__title"><span class="pv-ph-name">HAL 1</span> '
        '<span class="read__no pv-ph-no" hidden></span></h1>'
        '</div></header><div class="read__body">' + verse_rows(3, 3) +
        '</div></article></div>'
        '<div class="pv-placeholder" id="pvPh-service" hidden>'
        '<article class="read" data-kind="tatib" lang="id">'
        '<header class="read__head"><div class="read__head-top">'
        '<p class="read__eyebrow pv-ph-eyebrow">Tata Ibadah</p>'
        '<div class="read__project">'
        '<button type="button" class="read__project-btn">Media files</button>'
        '<button type="button" class="read__project-btn read__project-btn--primary">'
        'Use template</button></div></div><div class="read__row">'
        '<h1 class="read__title"><span class="pv-ph-name">Service</span> '
        '<span class="read__no pv-ph-no" hidden></span></h1>'
        '</div></header><div class="read__body">'
        '<div class="entry__start"><span class="entry__start-inner">'
        '<button type="button" class="entry__add-btn">+ Text</button>'
        '<button type="button" class="entry__add-btn">+ Song</button>'
        '<button type="button" class="entry__add-btn">+ Passage</button>'
        '</span></div>' + service_rows(3) +
        '</div></article></div>')
    body = body.replace('<main class="stage">', '<main class="stage">' + stage_insert, 1)
    leaves = (
        '<a class="songrow pv-leaf pv-leaf--song" href="#" data-num="HAL 1">'
        '<span class="songrow__c">HAL 1</span>'
        '<span class="songrow__t">Jahowa Sihol Pujionku</span></a>'
        '<p class="v pv-leaf pv-leaf--verse"><span class="v__n">1</span>'
        '<span>Pada mulanya Allah menciptakan langit dan bumi.</span></p>'
        '<a class="songrow pv-leaf pv-leaf--service" href="#" data-num="6">'
        '<span class="songrow__c">6</span><span class="songrow__t">Service entry</span></a>'
    )
    body = re.sub(r'(<aside class="panel"[^>]*>)',
                  r'\1<div class="pv-section-bar" id="pvPanelBar" hidden></div>',
                  body, count=1)
    body = re.sub(r'(<aside class="chapters"[^>]*>)',
                  r'\1<div class="pv-section-bar" id="pvChBar" hidden></div>',
                  body, count=1)
    css, _ = catalogue_css(['tokens.css', 'components.css', 'generate.css'])

    refs = [
        ('index-v1.html', 'shot-a.png', 'v1', 'global bar'),
        ('index-v2.html', 'shot-queued.png', 'v2', 'source marks'),
        ('index-v3.html', 'shot3-skeleton-first.png', 'v3', 'skeleton / strip'),
        ('index-v4.html', 'shot4-slow-first.png', 'v4', 'optimistic'),
        ('index-v5.html', 'shot5-row-a.png', 'v5', 'lock + placeholder'),
        ('index-v6.html', 'shot5-sidebar-list.png', 'v6', 'list-only'),
        ('index-v7.html', 'shot5-verse-page.png', 'v7', 'write classes'),
        ('index-v8.html', 'shot8-dim-verse-page.png', 'v8', 'spinner alternatives'),
        ('index-v9.html', 'shot9-verse-page.png', 'v9', 'dim only'),
        ('index-v10.html', 'shot9-rail-list.png', 'v10', 'section bars'),
        ('index-v11.html', 'shot9-chapter-list.png', 'v11', 'top-edge bars'),
        ('index-v12.html', 'shot9-verse-page.png', 'v12', 'clean sidebar'),
        ('index-v13.html', 'shot9-service-page.png', 'v13', 'layout placeholders'),
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
      data-lockstyle="dim" data-scenario="verse-page">
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
    <span class="pv-row__label">Lock style</span>
    <span class="pv-row__hint" style="margin-left:0">Dim only — rail icon stays, row dims</span>
    <span class="pv-row__hint" id="pvStatus"></span>
  </div>
  <div class="pv-row">
    <span class="pv-row__label">Scenario</span>
    <button type="button" data-scenario="rail-list" aria-pressed="false">Rail list</button>
    <button type="button" data-scenario="chapter-list" aria-pressed="false">Chapter list</button>
    <button type="button" data-scenario="songbook-list" aria-pressed="false">Songbook list</button>
    <button type="button" data-scenario="song-page" aria-pressed="false">Song → page</button>
    <button type="button" data-scenario="verse-page" aria-pressed="true">Verse → page</button>
    <button type="button" data-scenario="service-page" aria-pressed="false">Service → page</button>
    <button type="button" data-scenario="cancel-page-page" aria-pressed="false">Cancel page → page</button>
    <button type="button" data-scenario="cancel-page-list" aria-pressed="false">Cancel page → list</button>
    <button type="button" data-scenario="cancel-list-page" aria-pressed="false">Cancel list → page</button>
    <button type="button" id="pvReplay">Replay</button>
  </div>
  <div class="pv-row pv-sources">
    <span class="pv-row__label">Clicked leaf</span>
    {leaves}
    <span class="pv-row__hint">stand-ins for song / verse / service writes</span>
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
