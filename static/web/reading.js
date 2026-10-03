/*
 * Shell behavior for the public reading pages (spec 004).
 *
 * Ported from the accepted mockup (scratch/revamp-mockup/
 * index-search-indonesian-terms.html): the open / mini / closed state
 * machine, content-based restoration, filters, tooltips, theme, and the
 * search keeping its last result set. Content and sidebars are
 * server-rendered; this file only moves and marks them.
 */
(function () {
  'use strict';

  var root = document.documentElement;
  var HOVER_DELAY = 600;                 /* ms before a rail tooltip appears */
  var SECTION_NAMES = { alkitab: 'Alkitab', kidung: 'Kidung', tatib: 'Tata Ibadah' };
  var mqNarrow = window.matchMedia('(max-width: 720px)');
  var mqSongNarrow = window.matchMedia('(max-width: 1272px)');

  var themeBtn = document.getElementById('themeBtn');
  var panel = document.getElementById('panel');
  var panelCollapse = document.getElementById('panelCollapse');
  var panelExpand = document.getElementById('panelExpand');
  var panelBody = document.getElementById('panelBody');
  var panelEmpty = document.getElementById('panelEmpty');
  var indUp = document.getElementById('indUp');
  var indDown = document.getElementById('indDown');
  var filter = document.getElementById('bookFilter');
  var rail = document.querySelector('.rail');
  var railSearch = document.getElementById('railSearch');
  var alkBtn = rail.querySelector('[data-panel="alkitab"]');
  var kidBtn = rail.querySelector('[data-panel="kidung"]');
  var tatBtn = rail.querySelector('[data-panel="tatib"]');
  var chaptersEl = document.getElementById('chapters');
  var chList = document.getElementById('chList');
  var chBody = document.getElementById('chBody');
  var chCollapse = document.getElementById('chCollapse');
  var chUp = document.getElementById('chUp');
  var chDown = document.getElementById('chDown');
  var songFilterEl = document.getElementById('songFilter');
  var songEmpty = document.getElementById('chEmpty');
  var searchForm = document.getElementById('globalSearch');
  var searchQuery = document.getElementById('searchQuery');
  var searchValidation = document.getElementById('searchValidation');
  var readEl = document.getElementById('read');
  var readBody = document.getElementById('readBody');
  var langTb = document.getElementById('langTb');
  var langSim = document.getElementById('langSim');

  var activeSection = root.dataset.section || 'alkitab';
  var navBeforeCh = null;
  var pendingAnchor = null;
  var railCloseTimer = null;
  var railCloseListener = null;

  /* What the server marked as this page's own content; restoration uses it. */
  var pageState = (function () {
    var tile = panelBody.querySelector('.book[aria-current="true"]');
    var row = chList.querySelector('.songrow[aria-current="true"]');
    var chapterTile = chList.querySelector('.ch-num[aria-current="true"]');
    return {
      tileName: tile ? tile.dataset.name : null,
      songId: row ? row.dataset.i : null,
      chapter: chapterTile ? chapterTile.dataset.n : null
    };
  })();

  function panelOwner() {
    return activeSection === 'kidung' ? kidBtn
         : activeSection === 'tatib' ? tatBtn : alkBtn;
  }

  function cancelPendingRailClose() {
    if (railCloseTimer !== null) window.clearTimeout(railCloseTimer);
    railCloseTimer = null;
    if (railCloseListener) chaptersEl.removeEventListener('transitionend', railCloseListener);
    railCloseListener = null;
  }

  function transitionDurationMs() {
    var ease = getComputedStyle(root).getPropertyValue('--ease').trim();
    var amount = parseFloat(ease);
    if (isNaN(amount)) return 200;
    return ease.indexOf('ms') !== -1 ? amount : amount * 1000;
  }

  /* ---------- tooltips: rail buttons get a delayed tip, instantly on focus ---------- */
  var tipTimer = null;
  var tipTarget = null;
  function showTip(btn) {
    hideTip();
    tipTarget = btn;
    btn.setAttribute('data-tip-open', 'true');
    btn.setAttribute('aria-describedby', 'tip-' + (btn.dataset.tip || '').replace(/\s+/g, '-'));
  }
  function hideTip() {
    if (tipTarget) {
      tipTarget.removeAttribute('data-tip-open');
      tipTarget.removeAttribute('aria-describedby');
    }
    tipTarget = null;
    if (tipTimer) { window.clearTimeout(tipTimer); tipTimer = null; }
  }
  function bindTip(el) {
    el.addEventListener('pointerenter', function (event) {
      if (event.pointerType === 'touch') return;      /* no hover tooltips on touch */
      window.clearTimeout(tipTimer);
      tipTimer = window.setTimeout(function () { showTip(el); }, HOVER_DELAY);
    });
    el.addEventListener('pointerleave', hideTip);
    el.addEventListener('focus', function () { showTip(el); });
    el.addEventListener('blur', hideTip);
  }
  rail.querySelectorAll('.rail__btn[data-tip]').forEach(function (btn) {
    bindTip(btn);
    btn.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && btn.getAttribute('data-tip-open') === 'true') {
        event.stopPropagation();
        hideTip();
      }
    });
  });

  /* floating tooltip for mini book tiles; lives outside the clip-wiped panel */
  var ftip = document.createElement('div');
  ftip.className = 'ftip';
  ftip.id = 'ftip';
  ftip.setAttribute('role', 'tooltip');
  document.body.appendChild(ftip);
  var ftimer = null;
  function showTileTip(tile) {
    if (root.dataset.nav !== 'mini') return;
    ftip.textContent = tile.dataset.tip;
    var r = tile.getBoundingClientRect();
    var pr = panel.getBoundingClientRect();
    ftip.style.left = (pr.right + 10) + 'px';
    ftip.style.top = (r.top + r.height / 2) + 'px';
    ftip.classList.add('show');
    tile.setAttribute('aria-describedby', 'ftip');
  }
  function hideTileTip() {
    ftip.classList.remove('show');
    if (ftimer) { window.clearTimeout(ftimer); ftimer = null; }
    var held = document.querySelector('[aria-describedby="ftip"]');
    if (held) held.removeAttribute('aria-describedby');
  }
  function bindFloatTip(el) {
    el.addEventListener('pointerenter', function (event) {
      if (root.dataset.nav !== 'mini' || event.pointerType === 'touch') return;
      window.clearTimeout(ftimer);
      ftimer = window.setTimeout(function () { showTileTip(el); }, HOVER_DELAY);
    });
    el.addEventListener('pointerleave', hideTileTip);
    el.addEventListener('focus', function () {
      if (root.dataset.nav === 'mini') showTileTip(el);
    });
    el.addEventListener('blur', hideTileTip);
  }
  panelBody.querySelectorAll('.book').forEach(bindFloatTip);
  bindFloatTip(panelExpand);

  /* ---------- theme ---------- */
  function applyTheme(theme, persist) {
    root.dataset.theme = theme;
    var dark = theme === 'dark';
    themeBtn.setAttribute('aria-pressed', String(dark));
    var label = dark ? 'Switch to light mode' : 'Switch to dark mode';
    themeBtn.setAttribute('aria-label', label);
    themeBtn.setAttribute('data-tip', label);
    if (persist) { try { localStorage.setItem('gkps-theme', theme); } catch (e) {} }
  }
  themeBtn.addEventListener('click', function () {
    applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true);
  });

  /* ---------- reading edition (TB / SIM) ---------- */
  var editionBlocks = [];
  if (readBody) {
    readBody.querySelectorAll('.read__ed').forEach(function (el) {
      editionBlocks.push({ ed: el.dataset.ed, el: el });
    });
  }
  function currentEdition() {
    return readEl && readEl.getAttribute('lang') === 'sim' ? 'sim' : 'tb';
  }
  function editionBlock(ed) {
    var found = null;
    editionBlocks.forEach(function (block) { if (block.ed === ed) found = block; });
    return found;
  }
  function decorateChapters() {
    if (activeSection !== 'alkitab') return;
    var ed = currentEdition();
    chList.querySelectorAll('.ch-num').forEach(function (a) {
      var ok = ed === 'sim' ? a.dataset.sim === 'true' : a.dataset.tb === 'true';
      a.classList.toggle('no-data', !ok);
      if (ok) a.removeAttribute('aria-disabled');
      else a.setAttribute('aria-disabled', 'true');
    });
  }
  function setEdition(ed, persist) {
    if (!editionBlocks.length) return;
    editionBlocks.forEach(function (block) { block.el.hidden = block.ed !== ed; });
    if (readEl) readEl.setAttribute('lang', ed === 'tb' ? 'id' : 'sim');
    if (langTb) langTb.setAttribute('aria-pressed', String(ed !== 'sim'));
    if (langSim) langSim.setAttribute('aria-pressed', String(ed === 'sim'));
    if (persist) { try { localStorage.setItem('gkps-lang', ed); } catch (e) {} }
    decorateChapters();
  }
  [langTb, langSim].forEach(function (link) {
    if (!link) return;
    link.addEventListener('click', function (event) {
      var want = link === langSim ? 'sim' : 'tb';
      /* no text in the other edition: keep the last good view */
      if (!editionBlock(want) || want === currentEdition()) { event.preventDefault(); return; }
      event.preventDefault();
      setEdition(want, true);
    });
  });
  try {
    var savedLang = localStorage.getItem('gkps-lang');
    if ((savedLang === 'tb' || savedLang === 'sim') && savedLang !== currentEdition()
        && editionBlock(savedLang)) {
      setEdition(savedLang, false);
    }
  } catch (e) {}

  /* ---------- shared helpers ---------- */
  function revealInSidebar(row, body) {
    if (!row) return;
    var r = row.getBoundingClientRect();
    var b = body.getBoundingClientRect();
    if (r.top < b.top || r.bottom > b.bottom) {
      body.scrollTop += (r.top + r.height / 2) - (b.top + b.height / 2);
    }
  }
  function markBookTile(name) {
    var key = name == null ? null : String(name);
    panelBody.querySelectorAll('.book').forEach(function (book) {
      if (key !== null && String(book.dataset.name) === key) book.setAttribute('aria-current', 'true');
      else book.removeAttribute('aria-current');
    });
  }
  function markRailTile() {
    if (activeSection === 'alkitab') {
      chList.querySelectorAll('.ch-num').forEach(function (x) {
        var on = !!pageState.chapter && x.dataset.n === pageState.chapter;
        if (on) x.setAttribute('aria-current', 'true');
        else x.removeAttribute('aria-current');
      });
      revealInSidebar(chList.querySelector('.ch-num[aria-current="true"]'), chBody);
      return;
    }
    if (activeSection === 'kidung') {
      chList.querySelectorAll('.songrow').forEach(function (x) {
        var on = !!pageState.songId && x.dataset.i === String(pageState.songId);
        if (on) x.setAttribute('aria-current', 'true');
        else x.removeAttribute('aria-current');
      });
      revealInSidebar(chList.querySelector('.songrow[aria-current="true"]'), chBody);
      return;
    }
    /* Tata Ibadah contents rows are quicklinks, never a current destination. */
    chList.querySelectorAll('.songrow[aria-current]').forEach(function (row) {
      row.removeAttribute('aria-current');
    });
  }

  /* ---------- chapters rail ---------- */
  function updateChInds() {
    if (root.dataset.ch !== 'open') {
      chUp.classList.remove('show');
      chDown.classList.remove('show');
      return;
    }
    var top = chBody.scrollTop;
    var rest = chBody.scrollHeight - top - chBody.clientHeight;
    chUp.classList.toggle('show', top > 2);
    chDown.classList.toggle('show', rest > 2);
  }
  chBody.addEventListener('scroll', updateChInds, { passive: true });
  window.addEventListener('resize', updateChInds);
  chUp.addEventListener('click', function () {
    chBody.scrollBy({ top: -chBody.clientHeight * 0.6, behavior: 'smooth' });
  });
  chDown.addEventListener('click', function () {
    chBody.scrollBy({ top: chBody.clientHeight * 0.6, behavior: 'smooth' });
  });

  function openChaptersInPlace(name) {
    cancelPendingRailClose();
    if (mqNarrow.matches && root.dataset.nav !== 'closed') {
      navBeforeCh = root.dataset.nav;
      root.dataset.nav = 'closed';
    } else {
      navBeforeCh = null;
    }
    markBookTile(name);
    root.dataset.ch = 'open';
    chBody.scrollTop = 0;
    decorateChapters();
    markRailTile();
    syncState();
    updateChInds();
    window.requestAnimationFrame(updateChInds);
  }
  function closeChapters(restorePanel) {
    if (root.dataset.ch !== 'open') return;
    root.dataset.ch = 'closed';
    hideTileTip();
    if (restorePanel && navBeforeCh) {
      root.dataset.nav = navBeforeCh;
    }
    navBeforeCh = null;
    syncState();
    updateChInds();
  }
  chCollapse.addEventListener('click', function () {
    cancelPendingRailClose();
    closeChapters(true);
    var row = panelBody.querySelector('.book[aria-current="true"]');
    if (root.dataset.nav !== 'closed' && row) row.focus();
    else panelOwner().focus();
  });

  /* book tiles: the page's own book toggles its chapter list in place;
     another book is a normal link to its own page */
  panelBody.querySelectorAll('.book').forEach(function (tile) {
    tile.addEventListener('click', function (event) {
      if (activeSection !== 'alkitab' || tile.dataset.name !== pageState.tileName) return;
      event.preventDefault();
      hideTileTip();
      if (root.dataset.ch === 'open') closeChapters(true);
      else openChaptersInPlace(pageState.tileName);
    });
  });

  /* ---------- Tata Ibadah contents: quicklinks that jump, never selected ---------- */
  function jumpTatibItem(anchor) {
    var target = document.getElementById(anchor);
    if (!target) return;
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    var previous = readBody.querySelector('.tatib__flash');
    if (previous) previous.classList.remove('tatib__flash');
    target.classList.add('tatib__flash');
  }
  chList.querySelectorAll('a.songrow').forEach(function (link) {
    var href = link.getAttribute('href') || '';
    if (href.charAt(0) !== '#') return;
    link.addEventListener('click', function (event) {
      event.preventDefault();
      jumpTatibItem(href.slice(1));
      if (mqNarrow.matches) closeChapters(false);
    });
  });

  /* ---------- panel filter ---------- */
  function applyFilter(query) {
    var needle = (query || '').trim().toLowerCase();
    var any = false;
    panelBody.querySelectorAll('.group').forEach(function (group) {
      var shownInGroup = 0;
      group.querySelectorAll('.book').forEach(function (row) {
        var hit = !needle
          || String(row.dataset.name).toLowerCase().indexOf(needle) !== -1
          || String(row.dataset.sim).toLowerCase().indexOf(needle) !== -1
          || row.textContent.toLowerCase().indexOf(needle) !== -1;
        row.parentNode.classList.toggle('is-hidden', !hit);
        if (hit) { shownInGroup++; any = true; }
      });
      group.classList.toggle('is-hidden', shownInGroup === 0);
    });
    panelEmpty.hidden = any;
    panelEmpty.textContent = activeSection === 'kidung'
      ? 'No matching songbooks.'
      : activeSection === 'tatib'
        ? 'No matching Tata Ibadah.' : 'No matching books.';
    if (needle) panelBody.scrollTop = 0;
    updateInds();
  }
  filter.addEventListener('input', function () { applyFilter(filter.value); });
  filter.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      event.stopPropagation();
      if (filter.value) { filter.value = ''; applyFilter(''); }
      else { closePanel(); panelOwner().focus(); }
    }
  });

  /* ---------- song / section list filter ---------- */
  function applySongFilter(needle) {
    needle = (needle || '').trim().toLowerCase();
    var any = false;
    chList.querySelectorAll('.toc__eos').forEach(function (li) {
      li.classList.toggle('is-hidden', !!needle);
    });
    chList.querySelectorAll('.songrow').forEach(function (row) {
      var hay = row.dataset.txt
        || row.querySelector('.songrow__t').textContent.toLowerCase()
           + ' ' + (row.dataset.num || '').toLowerCase();
      var hit = !needle || hay.indexOf(needle) !== -1;
      row.parentNode.classList.toggle('is-hidden', !hit);
      if (hit) any = true;
    });
    songEmpty.hidden = any;
    if (needle) chBody.scrollTop = 0;
    updateChInds();
  }
  songFilterEl.addEventListener('input', function () { applySongFilter(songFilterEl.value); });
  songFilterEl.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      event.stopPropagation();
      if (songFilterEl.value) { songFilterEl.value = ''; applySongFilter(''); }
      else {
        closeChapters(true);
        var row = panelBody.querySelector('.book[aria-current="true"]');
        if (root.dataset.nav !== 'closed' && row) row.focus();
        else panelOwner().focus();
      }
    }
  });

  /* ---------- state machine: closed <-> open <-> mini ---------- */
  function syncSearchBtn() {
    var sidebarOpen = root.dataset.nav !== 'closed' || root.dataset.ch !== 'closed';
    if (root.dataset.read === 'on' || sidebarOpen) railSearch.removeAttribute('aria-current');
    else railSearch.setAttribute('aria-current', 'page');
  }
  function syncState() {
    var mode = root.dataset.nav;
    var panelOpen = mode !== 'closed';
    var sectionOpen = panelOpen || root.dataset.ch === 'open';
    var name = SECTION_NAMES[activeSection];
    alkBtn.setAttribute('aria-expanded', String(sectionOpen && activeSection === 'alkitab'));
    kidBtn.setAttribute('aria-expanded', String(sectionOpen && activeSection === 'kidung'));
    tatBtn.setAttribute('aria-expanded', String(sectionOpen && activeSection === 'tatib'));
    panelCollapse.setAttribute('aria-expanded', String(mode === 'open'));
    panelCollapse.setAttribute('aria-label', mode !== 'open'
      ? 'Open ' + name + ' panel'
      : activeSection === 'alkitab'
        ? 'Collapse ' + name + ' panel' : 'Close ' + name + ' panel');
    panelExpand.setAttribute('aria-expanded', String(mode === 'mini'));
    chCollapse.setAttribute('aria-expanded', String(root.dataset.ch === 'open'));
    chCollapse.setAttribute('aria-label', activeSection === 'alkitab'
      ? 'Close chapter list'
      : activeSection === 'tatib' ? 'Close Tata Ibadah sections' : 'Close song list');
    hideTileTip();
    updateInds();
    syncSearchBtn();
  }

  function updateInds() {
    if (root.dataset.nav !== 'mini') {
      indUp.classList.remove('show');
      indDown.classList.remove('show');
      return;
    }
    var top = panelBody.scrollTop;
    var rest = panelBody.scrollHeight - top - panelBody.clientHeight;
    indUp.classList.toggle('show', top > 2);
    indDown.classList.toggle('show', rest > 2);
  }
  panelBody.addEventListener('scroll', updateInds, { passive: true });
  window.addEventListener('resize', updateInds);
  indUp.addEventListener('click', function () {
    panelBody.scrollBy({ top: -panelBody.clientHeight * 0.6, behavior: 'smooth' });
  });
  indDown.addEventListener('click', function () {
    panelBody.scrollBy({ top: panelBody.clientHeight * 0.6, behavior: 'smooth' });
  });

  /* scroll sync between open <-> mini: the tile at the centre stays centred */
  var pendingAnchor = null;
  function edgeOf(body) {
    var max = body.scrollHeight - body.clientHeight;
    if (body.scrollTop <= 2) return 'top';
    if (body.scrollTop >= max - 2) return 'bottom';
    return null;
  }
  function anchorName() {
    var viewport = panelBody.getBoundingClientRect();
    var mid = viewport.top + viewport.height / 2;
    var best = null, bestDistance = Infinity;
    panelBody.querySelectorAll('.book').forEach(function (book) {
      var r = book.getBoundingClientRect();
      if (!r.height || r.bottom < viewport.top || r.top > viewport.bottom) return;
      var distance = Math.abs((r.top + r.height / 2) - mid);
      if (distance < bestDistance) { bestDistance = distance; best = book; }
    });
    return best ? best.dataset.name : null;
  }
  function centerBook(name) {
    var viewport = panelBody.getBoundingClientRect();
    var target = null;
    panelBody.querySelectorAll('.book').forEach(function (book) {
      if (book.dataset.name === name) target = book;
    });
    if (!target) return;
    var r = target.getBoundingClientRect();
    if (!r.height) return;
    panelBody.scrollTop += (r.top + r.height / 2) - (viewport.top + viewport.height / 2);
  }
  function snapshotPos() {
    var edge = edgeOf(panelBody);
    return { edge: edge, anchor: edge ? null : anchorName() };
  }
  function restorePos(snapshot) {
    if (snapshot.edge === 'top') panelBody.scrollTop = 0;
    else if (snapshot.edge === 'bottom') panelBody.scrollTop = panelBody.scrollHeight;
    else if (snapshot.anchor) centerBook(snapshot.anchor);
    updateInds();
    if (snapshot.anchor) {
      pendingAnchor = snapshot.anchor;
      window.requestAnimationFrame(function () {
        if (pendingAnchor === snapshot.anchor) { centerBook(snapshot.anchor); updateInds(); }
      });
    }
  }
  panel.addEventListener('transitionend', function (event) {
    if (event.propertyName !== 'width' || !pendingAnchor) return;
    var anchor = pendingAnchor;
    pendingAnchor = null;
    centerBook(anchor);
    updateInds();
  });
  ['wheel', 'touchstart', 'keydown'].forEach(function (ev) {
    panelBody.addEventListener(ev, function () { pendingAnchor = null; }, { passive: true });
  });

  function openPanel() {
    cancelPendingRailClose();
    if (mqNarrow.matches && root.dataset.ch === 'open') closeChapters();
    if (root.dataset.chMode === 'song' && mqSongNarrow.matches
        && root.dataset.ch === 'open') closeChapters();
    var previous = root.dataset.nav;
    var snapshot = previous === 'mini' ? snapshotPos() : null;
    root.dataset.nav = 'open';
    syncState();
    if (snapshot) { restorePos(snapshot); return; }
    filter.focus();
    filter.select();
  }
  function miniPanel() {
    var snapshot = root.dataset.nav === 'open' ? snapshotPos() : null;
    root.dataset.nav = 'mini';
    syncState();
    if (snapshot) restorePos(snapshot);
  }
  function closePanel() {
    cancelPendingRailClose();
    root.dataset.nav = 'closed';
    syncState();
  }
  function closeAllPanels() {
    if (railCloseListener) return;      /* ignore duplicate clicks during the wipe */
    if (root.dataset.ch !== 'open') { closePanel(); return; }
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      closeChapters();
      closePanel();
      return;
    }
    var section = activeSection;
    function finish(event) {
      if (event && (event.target !== chaptersEl || event.propertyName !== 'clip-path')) return;
      cancelPendingRailClose();
      if (activeSection === section && root.dataset.ch === 'closed') closePanel();
    }
    railCloseListener = finish;
    chaptersEl.addEventListener('transitionend', finish);
    closeChapters();
    railCloseTimer = window.setTimeout(finish, transitionDurationMs() + 50);
  }
  panelCollapse.addEventListener('click', function () {
    if (activeSection === 'alkitab') {
      if (root.dataset.nav === 'open') { miniPanel(); alkBtn.focus(); }
      else if (root.dataset.nav === 'mini') openPanel();
      return;
    }
    closePanel();
    panelOwner().focus();
  });
  panelExpand.addEventListener('click', openPanel);

  /* rail menus: the page's own section toggles in place; another section is
     an ordinary link to its root */
  function railBtnClick(name, btn) {
    return function (event) {
      if (name !== activeSection) return;
      event.preventDefault();
      var fromClosed = root.dataset.nav === 'closed' && root.dataset.ch === 'closed';
      if (root.dataset.nav === 'open') {
        closeAllPanels();
        btn.focus();
        return;
      }
      openPanel();
      if (fromClosed) restoreCurrentPath(name);
    };
  }
  alkBtn.addEventListener('click', railBtnClick('alkitab', alkBtn));
  kidBtn.addEventListener('click', railBtnClick('kidung', kidBtn));
  tatBtn.addEventListener('click', railBtnClick('tatib', tatBtn));

  function restoreCurrentPath(name) {
    if (root.dataset.read !== 'on' || name !== activeSection) return;
    if (!pageState.tileName) return;
    var tile = null;
    panelBody.querySelectorAll('.book').forEach(function (row) {
      if (String(row.dataset.name) === String(pageState.tileName)) tile = row;
    });
    if (!tile) return;
    if (tile.closest('.is-hidden')) {
      filter.value = '';
      applyFilter('');
    }
    if (activeSection === 'alkitab') openChaptersInPlace(pageState.tileName);
    else {
      markBookTile(pageState.tileName);
      root.dataset.ch = 'open';
      markRailTile();
      syncState();
      updateChInds();
    }
    revealInSidebar(tile, panelBody);
    /* On narrow screens the child replaced its parent: hand focus to the
       exact reading destination, or the contents collapse control. */
    if (root.dataset.nav === 'closed') {
      var selected = chList.querySelector('[aria-current="true"]');
      if (selected) selected.focus({ preventScroll: true });
      else chCollapse.focus({ preventScroll: true });
    }
  }

  /* ---------- Escape closes the innermost open layer ---------- */
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    if (root.dataset.ch === 'open') {
      closeChapters(true);
      var row = panelBody.querySelector('.book[aria-current="true"]');
      if (root.dataset.nav !== 'closed' && row) row.focus();
      else panelOwner().focus();
    } else if (root.dataset.nav !== 'closed') {
      closePanel();
      panelOwner().focus();
    }
  });

  /* ---------- search: minimum length + keeping the last result set ---------- */
  function keywordLength(query) {
    return Array.from(String(query).matchAll(/[\p{L}\p{N}]/gu)).length;
  }
  function clearSearchValidation() {
    searchQuery.removeAttribute('aria-invalid');
    searchQuery.removeAttribute('aria-describedby');
    searchValidation.hidden = true;
  }
  searchQuery.addEventListener('input', clearSearchValidation);
  searchForm.addEventListener('submit', function (event) {
    var query = searchQuery.value.trim();
    if (keywordLength(query) < 3) {
      event.preventDefault();
      searchQuery.setAttribute('aria-invalid', 'true');
      searchQuery.setAttribute('aria-describedby', 'searchValidation');
      searchValidation.hidden = false;
      searchQuery.focus();
      return;
    }
    clearSearchValidation();
    searchQuery.value = query;
  });
  try {
    if (root.dataset.home === 'results') {
      /* remember the exact result URL, revealed rows included */
      localStorage.setItem('gkps-search', window.location.pathname + window.location.search);
    }
    var lastSearch = localStorage.getItem('gkps-search');
    if (lastSearch) railSearch.setAttribute('href', lastSearch);
    var logo = document.querySelector('.rail__logo');
    if (logo) {
      /* a fresh search: the logo forgets the last result set */
      logo.addEventListener('click', function () {
        try { localStorage.removeItem('gkps-search'); } catch (e) {}
      });
    }
  } catch (e) {}

  /* ---------- reveal search targets ---------- */
  function revealSearchTarget(target) {
    target.scrollIntoView({ block: 'start', behavior: 'instant' });
    /* sidebars push the reading width while their transition runs; re-anchor
       after wrapping settles, or a verse can drift offscreen */
    window.setTimeout(function () {
      if (root.dataset.read === 'on' && document.contains(target)) {
        target.scrollIntoView({ block: 'start', behavior: 'instant' });
      }
    }, transitionDurationMs() + 60);
  }

  /* ---------- init ---------- */
  applyTheme(root.dataset.theme
    || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'), false);
  syncState();
  decorateChapters();
  markRailTile();
  updateChInds();
  window.requestAnimationFrame(updateChInds);
  var visibleBlock = null;
  editionBlocks.forEach(function (block) { if (!block.el.hidden) visibleBlock = block.el; });
  var searchTarget = visibleBlock
    ? visibleBlock.querySelector('[data-search-target="true"]') : null;
  if (searchTarget && root.dataset.read === 'on') revealSearchTarget(searchTarget);
  if (window.location.hash.indexOf('#ti-') === 0) {
    jumpTatibItem(window.location.hash.slice(1));
  }
})();
