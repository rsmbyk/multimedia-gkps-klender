#!/usr/bin/env python3
"""Build the three option previews from spec 243's accepted static shell.

The shell markup, tokens, components and pending-state classes come from the
repo. This script only swaps the preview toolbar and drives the two rail tiles
with a simulated delayed response; it does not modify application code.
"""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent / '243-navigation-loading-feedback' / 'preview' / 'index.html'
raw = BASE.read_text(encoding='utf-8')
style = re.search(r'<style>(.*?)</style>', raw, re.S).group(1)
body = re.search(r'<body[^>]*>(.*)</body>', raw, re.S).group(1)
body = body[body.index('<div class="pv-app">'):]

EXTRA_CSS = r'''
/* ---- Option previews: chrome, two target placeholders, landed pages ------ */
:root { --pv-top: 152px; }
html { color-scheme: dark; }
body { padding-top: var(--pv-top); }
.pv-bar {
  position: fixed; inset: 0 0 auto 0; height: var(--pv-top); z-index: 9600;
  display: flex; flex-direction: column; justify-content: center; gap: 5px;
  padding: 6px 12px; background: var(--rail-bg);
  border-bottom: 1px solid var(--divider); color: var(--ink);
  font: 12px/1.3 ui-sans-serif, system-ui, sans-serif;
}
.pv-row { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.pv-row__label { font-weight: 650; min-width: 62px; opacity: .85; }
.pv-row__title { font-weight: 700; font-size: 13px; margin-right: 8px; }
.pv-row__hint { margin-left: auto; opacity: .78; }
.pv-bar button, .pv-bar a {
  border: 1px solid var(--divider); border-radius: 6px; padding: 4px 8px;
  background: transparent; color: inherit; font: inherit; cursor: pointer;
  text-decoration: none;
}
.pv-bar button:hover, .pv-bar a:hover { background: var(--icon-hover-bg); }
.pv-bar button[aria-pressed="true"] {
  background: var(--active-bg); color: var(--active-ink); border-color: transparent;
}
.pv-bar button:focus-visible, .pv-bar a:focus-visible {
  outline: 2px solid var(--focus); outline-offset: 2px;
}
#pvReadout { font-family: ui-monospace, SFMono-Regular, monospace; font-size: 11.5px; }
.pv-windowbar {
  position: fixed; top: 0; left: 0; right: 0; height: 3px; z-index: 9800;
  overflow: hidden; background: color-mix(in srgb, var(--active-bg) 22%, transparent);
}
.pv-windowbar[hidden] { display: none !important; }
.pv-windowbar::before, .pv-stagebar::before {
  content: ""; position: absolute; top: 0; bottom: 0; width: 28%;
  background: var(--active-bg); animation: pv-slide 1.05s var(--ease-timing) infinite;
}
.rail, .panel, .chapters, .topbar { top: var(--pv-top) !important; }
.stage[aria-busy="true"] > .search-home,
.stage[aria-busy="true"] > .search-results { visibility: hidden !important; }

/* Placeholder anatomy for the two destinations (real classes inside). */
.pv-placeholder--search .result-group__head,
.pv-placeholder--media .media-library__intro { margin: 0 0 14px; }
.pv-placeholder .result-row { display: block; padding: 11px 0; }
.pv-placeholder .result-row__title,
.pv-placeholder .result-row__meta { display: block; }
.pv-ph-file {
  display: flex; align-items: center; gap: 14px;
  padding: 13px 2px; border-bottom: 1px solid var(--divider);
}
.pv-ph-file__icon {
  width: 34px; height: 34px; flex: none; border-radius: 8px;
  background: var(--icon-hover-bg);
}
.pv-ph-file__lines { flex: 1; display: flex; flex-direction: column; gap: 7px; }
.pv-landed {
  position: absolute; inset: 0; z-index: 9; overflow: auto;
  padding: 40px clamp(24px, 5vw, 64px); background: var(--canvas); color: var(--ink);
}
.pv-landed[hidden], .pv-placeholder[hidden] { display: none !important; }
/* The shell hides search/media surfaces on the reading home state; the
   placeholder and the landed page must override that for this preview. */
.stage[aria-busy="true"] > .pv-placeholder .search-results,
.stage[aria-busy="true"] > .pv-placeholder .media-library,
.pv-landed .search-results, .pv-landed .search-home, .pv-landed .media-library {
  display: block !important; visibility: visible !important;
}
/* Search home keeps its grid; block would stack the form at the top edge. */
.stage[aria-busy="true"] > .pv-placeholder .search-home {
  display: grid !important; visibility: visible !important;
}
.pv-ph-logo {
  display: block; width: 96px; height: 96px; border-radius: 14px;
  background: var(--icon-hover-bg);
}
.pv-ph-bar--icon { width: 23px; height: 23px; border-radius: 6px; }
.pv-ph-bar--unused { height: 18px; width: 53%; }
.pv-ph-bar--button { width: 36px; height: 36px; border-radius: 9px; }
.pv-ph-bar--input {
  position: absolute; left: 22px; top: 50%; transform: translateY(-50%);
  width: 58%; height: 12px; pointer-events: none;
}
.pv-media-count { margin: 0 auto; color: var(--head-ink); font-size: 12px; }
/* Skeleton controls and hidden header actions, mirrored from the product. */
.pv-placeholder--media .media-library__head-actions { visibility: hidden; }
.pv-placeholder--media .media-library__intro,
.pv-placeholder--media .media-library__chips button,
.pv-placeholder--media .pv-media-count,
.pv-placeholder--media .media-library__sort button span { position: relative; color: transparent; }
.pv-placeholder--media .media-library__sort button svg { visibility: hidden; }
.pv-placeholder--media .media-library__intro::after,
.pv-placeholder--media .media-library__chips button::after,
.pv-placeholder--media .pv-media-count::after,
.pv-placeholder--media .media-library__sort button span::after {
  content: ""; position: absolute; border-radius: 4px; background: var(--divider); opacity: .55;
}
.pv-placeholder--media .media-library__intro::after { left: 0; top: 2px; width: 72%; height: 18px; }
.pv-placeholder--media .media-library__chips button::after {
  left: 11px; right: 11px; top: 50%; height: 10px; transform: translateY(-50%);
}
.pv-placeholder--media .pv-media-count::after { left: 0; right: 0; top: 3px; height: 12px; }
.pv-placeholder--media .media-library__sort button span::after {
  left: 0; right: 0; top: 50%; height: 10px; transform: translateY(-50%);
}
.pv-placeholder .search-home__input { pointer-events: none; }
.pv-landed .read__title { font-size: 30px; }
.pv-landed .result-row { cursor: default; }
.pv-landed .media-library__intro { margin-bottom: 18px; }
.pv-landed .pv-ph-file .pv-ph-bar { background: var(--divider); }
@media (prefers-reduced-motion: reduce) {
  .pv-windowbar::before, .pv-stagebar::before { animation: none; }
}
'''

TOOLBAR = r'''
<div class="pv-bar" role="toolbar" aria-label="Option preview controls">
  <div class="pv-row">
    <span class="pv-row__title" id="pvTitle"></span>
    <span class="pv-row__hint" id="pvStatus">Idle — click a rail tile below or in the rail.</span>
  </div>
  <div class="pv-row">
    <span class="pv-row__label">Fetch</span>
    <button type="button" data-delay="0">Instant</button>
    <button type="button" data-delay="1200" aria-pressed="true">Slow 1.2s</button>
    <button type="button" data-delay="2500">Very slow 2.5s</button>
    <button type="button" id="pvSearchBtn">Click Search rail</button>
    <button type="button" id="pvMediaBtn">Click Media Library rail</button>
    <button type="button" id="pvReplay">Replay</button>
    <span class="pv-row__label">Search to</span>
    <button type="button" data-search-dest="results" aria-pressed="true">results</button>
    <button type="button" data-search-dest="home" aria-pressed="false">home</button>
  </div>
  <div class="pv-row">
    <span class="pv-row__label">Measure</span>
    <span id="pvReadout">tile svg opacity — · aria-disabled — · stage aria-busy — · bar — · placeholder —</span>
    <a id="pvPrev" href="#">← Prev</a>
    <a href="index.html">Index</a>
    <a id="pvNext" href="#">Next →</a>
  </div>
</div>
<div class="pv-windowbar" id="pvWindowBar" hidden></div>
'''

PLACEHOLDERS = r'''
<div class="pv-placeholder pv-placeholder--search" id="pvPh-search" hidden>
  <div class="search-results">
    <p class="search-results__intro" role="status">Results for “Yoh 3:16”</p>
    <section class="result-group" data-kind="passage">
      <div class="result-group__head">
        <h2 class="result-group__title">Passage</h2><span class="result-group__count">3 results</span>
      </div>
      <ul class="result-list">
        <li><a class="result-row" data-kind="passage" href="#">
          <span class="result-row__title">Yohanes 3:16</span>
          <span class="result-row__meta">Yohanes · 3</span>
          <span class="result-row__excerpt">Karena demikianlah Allah mengasihi isi dunia…</span>
        </a></li>
        <li><a class="result-row" data-kind="passage" href="#">
          <span class="result-row__title"><span class="pv-ph-bar pv-ph-bar--title"></span></span>
          <span class="result-row__meta"><span class="pv-ph-bar pv-ph-bar--sub"></span></span>
          <span class="result-row__excerpt"><span class="pv-ph-bar pv-ph-bar--verse"></span></span>
        </a></li>
        <li><a class="result-row" data-kind="passage" href="#">
          <span class="result-row__title"><span class="pv-ph-bar pv-ph-bar--title"></span></span>
          <span class="result-row__meta"><span class="pv-ph-bar pv-ph-bar--sub"></span></span>
          <span class="result-row__excerpt"><span class="pv-ph-bar pv-ph-bar--verse"></span></span>
        </a></li>
      </ul>
      <a class="result-more" href="#">Show more</a>
    </section>
    <section class="result-group" data-kind="song">
      <div class="result-group__head">
        <h2 class="result-group__title">Song</h2><span class="result-group__count">2 results</span>
      </div>
      <ul class="result-list">
        <li><a class="result-row" data-kind="song" href="#">
          <span class="result-row__title"><span class="pv-ph-bar pv-ph-bar--title"></span></span>
          <span class="result-row__meta"><span class="pv-ph-bar pv-ph-bar--sub"></span></span>
        </a></li>
        <li><a class="result-row" data-kind="song" href="#">
          <span class="result-row__title"><span class="pv-ph-bar pv-ph-bar--title"></span></span>
          <span class="result-row__meta"><span class="pv-ph-bar pv-ph-bar--sub"></span></span>
        </a></li>
      </ul>
    </section>
  </div>
</div>
<div class="pv-placeholder pv-placeholder--search-home" id="pvPh-search-home" hidden>
  <section class="search-home" aria-label="Search GKPS Klender">
    <div class="search-home__inner">
      <span class="search-home__logo pv-ph-logo" aria-hidden="true"></span>
      <form class="search-home__form" role="search" action="#">
        <input class="search-home__input" type="search" value="" placeholder="" readonly>
        <span class="pv-ph-bar pv-ph-bar--input" aria-hidden="true"></span>
        <button class="search-home__submit" type="button" aria-label="Search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
               stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>
        </button>
      </form>
    </div>
  </section>
</div>
<div class="pv-placeholder pv-placeholder--media" id="pvPh-media" hidden>
  <article class="read" data-kind="media-library">
    <header class="read__head"><div class="read__head-top">
      <div class="media-library__head-actions">
        <button type="button" class="media-library__icon-btn"></button>
        <button type="button" class="media-library__icon-btn"></button>
        <button type="button" class="media-library__icon-btn"></button>
      </div>
    </div><div class="read__row"><h1 class="read__title">Media Library</h1></div></header>
    <div class="read__body">
    <div class="media-library">
    <p class="media-library__intro">Files available on this computer. Add a file while editing a Tata Ibadah entry, or choose one already in this library.</p>
    <div class="media-library__filters"><div class="media-library__chips" role="group" aria-label="File type filters">
      <button type="button" aria-pressed="false">Images</button><button type="button" aria-pressed="false">Audio</button>
      <button type="button" aria-pressed="false">Video</button><button type="button" aria-pressed="false">PDF</button>
      <button type="button" aria-pressed="false">Slides</button><span aria-hidden="true">·</span>
      <button type="button" aria-pressed="false">Unused</button>
    </div>
    <p class="pv-media-count">Loading files…</p>
    <div class="media-library__sort"><button type="button" aria-label="Sort files: Upload date, newest" aria-expanded="false">
      <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5.5 3.5v13m0-13-2.5 2.5m2.5-2.5L8 6m6.5 10.5v-13m0 13-2.5-2.5m2.5 2.5L17 14"/></svg>
      <span>Upload date · newest</span></button></div></div>
    <div class="media-library__file"><div class="media-library__file-icon"><span class="pv-ph-bar pv-ph-bar--icon"></span></div>
      <div class="media-library__file-main"><div class="media-library__filename"><span class="pv-ph-bar pv-ph-bar--title"></span></div>
      <div class="media-library__meta"><span class="pv-ph-bar pv-ph-bar--sub"></span></div>
      <div class="media-library__unused"><span class="pv-ph-bar pv-ph-bar--unused"></span></div></div>
      <div class="media-library__cloud"><span class="pv-ph-bar pv-ph-bar--button" aria-hidden="true"></span></div>
      <span class="pv-ph-bar pv-ph-bar--button" aria-hidden="true"></span></div>
    <div class="media-library__file"><div class="media-library__file-icon"><span class="pv-ph-bar pv-ph-bar--icon"></span></div>
      <div class="media-library__file-main"><div class="media-library__filename"><span class="pv-ph-bar pv-ph-bar--title"></span></div>
      <div class="media-library__meta"><span class="pv-ph-bar pv-ph-bar--sub"></span></div>
      <div class="media-library__unused"><span class="pv-ph-bar pv-ph-bar--unused"></span></div></div>
      <div class="media-library__cloud"><span class="pv-ph-bar pv-ph-bar--button" aria-hidden="true"></span></div>
      <span class="pv-ph-bar pv-ph-bar--button" aria-hidden="true"></span></div>
    <div class="media-library__file"><div class="media-library__file-icon"><span class="pv-ph-bar pv-ph-bar--icon"></span></div>
      <div class="media-library__file-main"><div class="media-library__filename"><span class="pv-ph-bar pv-ph-bar--title"></span></div>
      <div class="media-library__meta"><span class="pv-ph-bar pv-ph-bar--sub"></span></div>
      <div class="media-library__unused"><span class="pv-ph-bar pv-ph-bar--unused"></span></div></div>
      <div class="media-library__cloud"><span class="pv-ph-bar pv-ph-bar--button" aria-hidden="true"></span></div>
      <span class="pv-ph-bar pv-ph-bar--button" aria-hidden="true"></span></div>
    </div></div></article>
</div>
<div class="pv-landed" id="pvLanded" hidden></div>
'''

JS = r'''
(function () {
  var root = document.documentElement;
  var option = root.dataset.option;
  var titles = {
    a: 'A · full-page lock + viewport bar',
    b: 'B · in-page parity: lock + stage bar + seeded placeholder',
    c: 'C · placeholder only, keep today\'s lock/bar',
    d: 'Combined · rail lock + stage bar + real-layout placeholder'
  };
  document.getElementById('pvTitle').textContent = titles[option];
  var files = {a: 'option-a.html', b: 'option-b.html', c: 'option-c.html', d: 'combined.html'};
  var order = ['d', 'a', 'b', 'c'];
  var at = order.indexOf(option);
  document.getElementById('pvPrev').href = order[at - 1] ? files[order[at - 1]] : 'index.html';
  document.getElementById('pvNext').href = order[at + 1] ? files[order[at + 1]] : 'index.html';
  document.addEventListener('keydown', function (event) {
    if (event.target.matches('input, textarea')) return;
    if (event.key === 'ArrowLeft') location.href = document.getElementById('pvPrev').href;
    if (event.key === 'ArrowRight') location.href = document.getElementById('pvNext').href;
  });

  var status = document.getElementById('pvStatus');
  var readout = document.getElementById('pvReadout');
  var stage = document.querySelector('.stage');
  var stageBar = document.getElementById('pvStagebar');
  var windowBar = document.getElementById('pvWindowBar');
  var landed = document.getElementById('pvLanded');
  var placeholders = {
    search: document.getElementById('pvPh-search'),
    'search-home': document.getElementById('pvPh-search-home'),
    media: document.getElementById('pvPh-media')
  };
  function phKey(which) {
    return which === 'search' && root.dataset.searchDest === 'home' ? 'search-home' : which;
  }
  function phSet(which, show) {
    Object.keys(placeholders).forEach(function (key) { placeholders[key].hidden = true; });
    if (show) placeholders[phKey(which)].hidden = false;
  }
  function phShown(which) { return !placeholders[phKey(which)].hidden; }
  var searchTile = document.getElementById('railSearch');
  var mediaTile = document.getElementById('railMediaLibrary');
  var delay = 1200;
  var last = null;
  var timers = [];

  var landedHtml = {
    search: '<div class="search-results"><p class="search-results__intro">3 results for <b>Yoh 3:16</b></p>'
      + '<section class="result-group"><h2 class="result-group__head">Passage</h2>'
      + '<ul class="result-list"><li class="result-row"><a class="result-row__title">Yohanes 3:16</a>'
      + '<span class="result-row__meta">Yohanes · 3</span>'
      + '<span class="result-row__excerpt">Karena demikianlah Allah mengasihi isi dunia…</span></li></ul></section></div>',
    'search-home': '<section class="search-home" aria-label="Search GKPS Klender"><div class="search-home__inner">'
      + '<span class="search-home__logo pv-ph-logo" aria-hidden="true"></span>'
      + '<form class="search-home__form" role="search"><input class="search-home__input" type="search" '
      + 'placeholder="Search Alkitab, Kidung, Tata Ibadah..." value=""></form></div></section>',
    media: '<div class="media-library"><p class="media-library__intro">Files available on this computer.</p>'
      + '<div class="media-library__filters"><div class="media-library__chips">'
      + '<button type="button">Images</button><button type="button">Audio</button>'
      + '<button type="button">Video</button><button type="button">PDF</button></div></div>'
      + '<div class="pv-ph-file"><span class="pv-ph-file__icon"></span><span class="pv-ph-file__lines">'
      + '<span>gereja.jpg</span><span>Image · 2.4 MB</span></span></div>'
      + '<div class="pv-ph-file"><span class="pv-ph-file__icon"></span><span class="pv-ph-file__lines">'
      + '<span>kidung.mp3</span><span>Audio · 5.1 MB</span></span></div></div>'
  };

  function later(fn, ms) { timers.push(setTimeout(fn, ms)); }
  function clearAll() {
    timers.forEach(clearTimeout); timers = [];
    [searchTile, mediaTile].forEach(function (tile) {
      tile.classList.remove('pv-locked', 'pv-rail-busy');
      tile.removeAttribute('aria-disabled');
      tile.removeAttribute('data-pending');
    });
    stageBar.hidden = true; windowBar.hidden = true;
    stage.removeAttribute('aria-busy');
    Object.keys(placeholders).forEach(function (key) { placeholders[key].hidden = true; });
    landed.hidden = true;
  }
  function parts(which) {
    if (option === 'a') return {lock: true, bar: 'window', placeholder: false, inPage: false};
    if (option === 'b') return {lock: true, bar: 'stage', placeholder: true, inPage: true};
    if (option === 'd') return {lock: true, bar: 'stage', placeholder: true, inPage: true};
    return {lock: true, bar: which === 'media' ? 'window' : 'stage',
            placeholder: true, inPage: which === 'search'};
  }
  function measure(tile, p) {
    var svg = tile.querySelector('svg');
    var bar = p.bar === 'window' ? windowBar : stageBar;
    var ph = p.placeholder ? phShown(last) : false;
    var box = bar.getBoundingClientRect();
    readout.textContent = 'tile svg opacity ' + getComputedStyle(svg).opacity
      + ' · aria-disabled ' + (tile.getAttribute('aria-disabled') || 'none')
      + ' · stage aria-busy ' + (stage.getAttribute('aria-busy') || 'none')
      + ' · bar ' + getComputedStyle(bar).height + ' at y=' + Math.round(box.top - stage.getBoundingClientRect().top)
      + ' · placeholder ' + (ph ? 'present' : 'none')
      + ' · destination ' + (last === 'search'
        ? (root.dataset.searchDest === 'home' ? 'home' : 'results') : 'media library')
      + ' · fetch ' + (p.inPage ? 'in-page' : 'full page');
  }
  function start(which) {
    last = which;
    clearAll();
    var tile = which === 'search' ? searchTile : mediaTile;
    var p = parts(which);
    if (p.lock) {
      tile.classList.add('pv-locked', 'pv-rail-busy');
      tile.setAttribute('aria-disabled', 'true');
      tile.setAttribute('data-pending', 'true');
    }
    if (p.bar === 'window') windowBar.hidden = false;
    if (p.bar === 'stage') { stageBar.hidden = false; stage.setAttribute('aria-busy', 'true'); }
    if (p.placeholder) phSet(which, true);
    status.textContent = 'Fetching ' + (which === 'search' ? 'Search' : 'Media Library')
      + ' — tile locked, ' + (p.bar === 'window' ? 'viewport' : 'stage') + ' bar'
      + (p.placeholder ? ', seeded placeholder' : ', no placeholder');
    requestAnimationFrame(function () { measure(tile, p); });
    later(function () {
      clearAll();
      landed.innerHTML = landedHtml[phKey(which)];
      landed.hidden = false;
      var arrived = which === 'search'
        ? (root.dataset.searchDest === 'home' ? 'home search' : 'search results')
        : 'Media Library';
      status.textContent = 'Arrived at ' + arrived
        + ' via ' + (p.inPage ? 'in-page swap' : 'full page load') + '.';
      readout.textContent = 'settled · tile unlocked · bar cleared · placeholder replaced by page';
    }, delay);
  }

  document.querySelectorAll('[data-delay]').forEach(function (button) {
    button.addEventListener('click', function () {
      document.querySelectorAll('[data-delay]').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === button));
      });
      delay = Number(button.dataset.delay);
      if (last) start(last);
    });
  });
  searchTile.addEventListener('click', function (event) { event.preventDefault(); start('search'); });
  mediaTile.addEventListener('click', function (event) { event.preventDefault(); start('media'); });
  document.getElementById('pvSearchBtn').addEventListener('click', function () { start('search'); });
  document.getElementById('pvMediaBtn').addEventListener('click', function () { start('media'); });
  document.getElementById('pvReplay').addEventListener('click', function () { start(last || 'search'); });
  document.querySelectorAll('[data-search-dest]').forEach(function (button) {
    button.addEventListener('click', function () {
      document.querySelectorAll('[data-search-dest]').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === button));
      });
      root.dataset.searchDest = button.dataset.searchDest;
      if (last === 'search') start('search');
    });
  });
})();
'''

INDEX = r'''<!doctype html>
<html lang="en" data-theme="dark">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rail fetch feedback — choose an option</title>
<style>
body { margin: 0; padding: 36px 28px; background: #171816; color: #F7F5F1;
  font: 15px/1.55 ui-sans-serif, system-ui, sans-serif; }
h1 { font-size: 26px; margin: 0 0 8px; }
p { max-width: 760px; color: #B9B8B2; }
ol { padding-left: 20px; max-width: 860px; }
li { margin: 18px 0; }
a { color: #8FD0AC; }
b { color: #F7F5F1; }
code { font-size: 13px; color: #D7D4CC; }
</style></head>
<body>
<h1>Rail fetch feedback — three options</h1>
<p>Each page is the real reading shell from spec 243's accepted preview, in dark mode, with
a simulated delayed response. Click the actual Search or Media Library rail tile, or the
buttons in the top bar. Use the delay buttons to watch the pending state at 0 ms / 1.2 s /
2.5 s; the readout shows computed values. Arrow keys and the links move between options.</p>
<ol>
<li><a href="combined.html">Combined — rail lock + reading-page bar + a little placeholder</a><br>
The chosen shape: the clicked Search or Media Library tile dims and locks, a 3px bar runs
at the top edge of the reading stage, and the stage carries a placeholder built from the
destination's own markup — result groups and rows for Search results (or the centred logo
and input when Search opens home), intro, filter chips, grouped file rows and cloud/remove
controls for Media Library. Both tiles fetch in place, so the rail and sidebars stay usable.</li>
<li><a href="option-a.html">Option A — full-page lock + viewport bar</a><br>
The clicked tile dims and locks; a 3px bar runs at the very top of the window for the whole
document load. The reading stage keeps whatever it showed. No placeholder.</li>
<li><a href="option-b.html">Option B — in-page parity</a><br>
Both rail tiles become in-page fetches through the shell's navigation. The tile locks, a 3px
bar runs at the stage's top edge, `aria-busy` is set and a seeded Search / Media Library
placeholder appears in the real page layout.</li>
<li><a href="option-c.html">Option C — placeholder only</a><br>
Keep today's lock and bar rules untouched (Search has a stage bar; Media Library is still a
full page load with a viewport bar) and add only the seeded placeholder while the page is
fetched.</li>
</ol>
</body></html>
'''

OPTIONS = {
    'a': 'A · full-page lock + viewport bar (no placeholder)',
    'b': 'B · in-page parity (lock + stage bar + seeded placeholder)',
    'c': 'C · placeholder only (today\'s lock/bar + seeded placeholder)',
    'd': 'Combined · rail lock + stage bar + real-layout placeholder',
}


def build(code, title):
    doc = raw
    doc = doc.replace('<html lang="en" data-theme="dark" data-theme-mode="dark"',
                      '<html lang="en" data-option="' + code + '" data-search-dest="results" data-theme="dark" data-theme-mode="dark"', 1)
    doc = doc.replace('data-lockstyle="dim"', 'data-lockstyle="dim"', 1)
    doc = doc.replace('</head>', '<style>' + EXTRA_CSS + '</style>\n</head>', 1)
    start = body.index('<div class="pv-app">')
    newbody = TOOLBAR + body[start:]
    newbody = newbody.replace('<main class="stage">', '<main class="stage">' + PLACEHOLDERS, 1)
    newbody = newbody.replace('<script>', '<script>', 1)  # keep head theme script untouched
    # The last script tag in the body is the old scenario driver.
    tail_pos = newbody.rfind('<script>')
    if tail_pos >= 0:
        end = newbody.find('</script>', tail_pos)
        newbody = newbody[:tail_pos] + '<script>' + JS + '</script>' + newbody[end + len('</script>'):]
    doc = re.sub(r'<body[^>]*>.*</body>', lambda m: '<body>\n' + newbody + '\n</body>', doc, count=1, flags=re.S)
    doc = doc.replace('<title>Spec 243 — owner rules preview v5</title>', '<title>' + title + '</title>', 1)
    out = HERE / ('combined.html' if code == 'd' else 'option-' + code + '.html')
    out.write_text(doc, encoding='utf-8')
    print(out.name, len(doc))


def main():
    (HERE / 'index.html').write_text(INDEX, encoding='utf-8')
    for code, title in OPTIONS.items():
        build(code, title)


if __name__ == '__main__':
    main()
