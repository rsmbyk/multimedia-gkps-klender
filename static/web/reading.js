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
  var songSortBtn = document.getElementById('songSort');
  var songEmpty = document.getElementById('chEmpty');
  var searchForm = document.getElementById('globalSearch');
  var searchQuery = document.getElementById('searchQuery');
  var readEl = document.getElementById('read');
  var readBody = document.getElementById('readBody');
  var langTb = document.getElementById('langTb');
  var langSim = document.getElementById('langSim');
  var stage = document.querySelector('.stage');
  var panelTitleEl = document.getElementById('panelTitle');
  var panelFilterLabel = document.querySelector('label[for="bookFilter"]');
  var chTitleEl = document.getElementById('chTitle');
  var chFilterLabel = document.querySelector('label[for="songFilter"]');
  var chSearchEl = document.querySelector('.ch__search');

  var activeSection = root.dataset.section || 'alkitab';
  var songSort = 'm';                    /* 'm' = last modified, 'title' = alphabetical */
  var navBeforeCh = null;
  var pendingAnchor = null;
  var railCloseTimer = null;
  var railCloseListener = null;

  /* What the current DOM marks as this page's own content; refreshed after
     every in-page navigation. */
  function readPageState() {
    var tile = panelBody.querySelector('.book[aria-current="true"]');
    var row = chList.querySelector('.songrow[aria-current="true"]');
    var chapterTile = chList.querySelector('.ch-num[aria-current="true"]');
    return {
      tileName: tile ? tile.dataset.name : null,
      songId: row ? row.dataset.i : null,
      chapter: chapterTile ? chapterTile.dataset.n : null
    };
  }
  var pageState = readPageState();

  /* Identity of what the reading stage shows. Unlike pageState it survives a
     section switch (which clears the lists), so restoration can rebuild. */
  var KIND_SECTION = { bible: 'alkitab', song: 'kidung', tatib: 'tatib' };
  var stageInfo = (function () {
    var s = readPageState();
    return {
      tile: s.tileName, chapter: s.chapter, song: s.songId,
      url: window.location.pathname + window.location.search
    };
  })();
  function readKind() {
    return readEl && readEl.dataset.kind ? readEl.dataset.kind : '';
  }
  function stageSection() {
    return KIND_SECTION[readKind()] || null;
  }

  /* After a stage swap the element references below point at detached nodes;
     re-grab them from the fresh markup. */
  function refreshStageRefs() {
    readEl = document.getElementById('read');
    readBody = document.getElementById('readBody');
    langTb = document.getElementById('langTb');
    langSim = document.getElementById('langSim');
    searchForm = document.getElementById('globalSearch');
    searchQuery = document.getElementById('searchQuery');
    editionBlocks = [];
    if (readBody) {
      readBody.querySelectorAll('.read__ed').forEach(function (el) {
        editionBlocks.push({ ed: el.dataset.ed, el: el });
      });
    }
  }

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
    el.addEventListener('focus', function () {
      /* Closing a panel puts focus back on its rail tile, and a pointer-driven focus
         must not raise the label: only a keyboard focus should (review report). */
      if (!el.matches(':focus-visible')) return;
      showTip(el);
    });
    el.addEventListener('blur', hideTip);
  }
  /* A rail click leaves focus on the tile, and a focused tile keeps its label up --
     which reads as a stuck tooltip once the sidebar it opened has closed. */
  rail.addEventListener('click', function () {
    hideTip();
    window.setTimeout(hideTip, 260);         /* after any re-focus the state change does */
  });
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
      if (root.dataset.nav === 'mini' && el.matches(':focus-visible')) showTileTip(el);
    });
    el.addEventListener('blur', hideTileTip);
  }
  /* Every tooltip is about a state that a transition is about to change: a focused
     tile keeps its own label up, and a tile's floating label can be showing under the
     pointer as the panel closes, where no pointerleave ever arrives. Clear them all at
     each transition rather than guessing which one is up. */
  function hideTips() { hideTip(); hideTileTip(); }
  function bindPanelTips() {
    panelBody.querySelectorAll('.book').forEach(bindFloatTip);
  }
  bindPanelTips();
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
    if (langTb) langTb.parentElement.dataset.edition = ed;
    if (persist) { try { localStorage.setItem('gkps-lang', ed); } catch (e) {} }
    decorateChapters();
  }
  function bindLangLinks() {
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
    if (langTb) langTb.parentElement.classList.add('is-enhanced');
  }
  function restoreSavedEdition() {
    try {
      var savedLang = localStorage.getItem('gkps-lang');
      if ((savedLang === 'tb' || savedLang === 'sim') && savedLang !== currentEdition()
          && editionBlock(savedLang)) {
        setEdition(savedLang, false);
      }
    } catch (e) {}
  }
  restoreSavedEdition();
  bindLangLinks();

  /* ---------- shared helpers ---------- */
  function prefersReduce() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
  function flashRow(row) {
    if (!row) return;
    row.classList.remove('tatib__flash');
    void row.offsetWidth;                 /* restart a running flash */
    row.classList.add('tatib__flash');
  }
  /* The reveal: centre a row in its scrollport. It belongs to the two
     "here you are" moments only -- opening a search result, or opening a
     sidebar on the page being read -- and it travels, so the rows just before
     the target are seen moving past. A plain item click uses ensureVisible()
     instead: no motion unless the row is clipped. */
  var revealPending = 0;
  function beginReveal() {                /* tests wait for data-scroll-anim to clear */
    revealPending += 1;
    root.dataset.scrollAnim = 'on';
  }
  function endReveal() {
    revealPending = Math.max(0, revealPending - 1);
    if (!revealPending) root.removeAttribute('data-scroll-anim');
  }
  function centerOf(row, body) {
    var r = row.getBoundingClientRect();
    var b = body.getBoundingClientRect();
    var max = Math.max(0, body.scrollHeight - body.clientHeight);
    return Math.max(0, Math.min(max,
      body.scrollTop + (r.top + r.height / 2) - (b.top + b.height / 2)));
  }
  function animateScroll(body, to, done) {
    var from = body.scrollTop;
    var ms = prefersReduce() ? 0 : Math.max(120, Math.min(180, transitionDurationMs() * 0.9));
    if (!ms || Math.abs(to - from) < 1) {
      body.scrollTop = to;
      if (done) done();
      return to;
    }
    var start = null;
    window.requestAnimationFrame(function step(now) {
      if (start === null) start = now;
      var t = Math.min(1, (now - start) / ms);
      var eased = 1 - Math.pow(1 - t, 3);  /* easeOutCubic */
      body.scrollTop = from + (to - from) * eased;
      if (t < 1) window.requestAnimationFrame(step);
      else { body.scrollTop = to; if (done) done(); }
    });
    return to;
  }
  function revealRow(row, body, opts) {
    if (!row || !body) return;
    if (opts && opts.flash) flashRow(row);
    if (prefersReduce()) {
      body.scrollTop = centerOf(row, body);
      return;
    }
    beginReveal();
    /* A collapsing or expanding pane has no usable geometry yet: measuring it now
       would aim the travel at a stale offset and then visibly correct it. When
       that is the case, wait for the layout and make one travel of it; when the
       pane is already laid out, travel at once. Either way the second pass
       re-centres after the push transition has reflowed the list -- unless the
       reader has moved on in the meantime. */
    var laidOut = body.getBoundingClientRect().height > 120;
    var landed = null;
    function settle() {
      window.setTimeout(function () {
        if (document.contains(row) && (landed === null || Math.abs(body.scrollTop - landed) <= 2)) {
          var corrected = centerOf(row, body);
          /* A pixel or two of reflow is not worth a second visible travel. */
          if (Math.abs(corrected - body.scrollTop) < 48) {
            body.scrollTop = corrected;
            endReveal();
          } else {
            animateScroll(body, corrected, endReveal);
          }
        } else endReveal();
      }, transitionDurationMs() + 40);
    }
    if (laidOut) landed = animateScroll(body, centerOf(row, body), settle);
    else settle();
  }
  /* Minimal nudge: move a list only as far as needed to show the row fully.
     Clicking an already visible item must never move the list. */
  function ensureVisible(row, body) {
    if (!row) return;
    var r = row.getBoundingClientRect();
    var b = body.getBoundingClientRect();
    if (r.top < b.top) body.scrollTop -= (b.top - r.top);
    else if (r.bottom > b.bottom) body.scrollTop += (r.bottom - b.bottom);
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
      return;
    }
    if (activeSection === 'kidung') {
      chList.querySelectorAll('.songrow').forEach(function (x) {
        var on = !!pageState.songId && x.dataset.i === String(pageState.songId);
        if (on) x.setAttribute('aria-current', 'true');
        else x.removeAttribute('aria-current');
      });
      return;
    }
    /* Tata Ibadah contents rows are quicklinks, never a current destination. */
    chList.querySelectorAll('.songrow[aria-current]').forEach(function (row) {
      row.removeAttribute('aria-current');
    });
  }

  /* The Tata Ibadah item the stage was opened at: its contents row is a
     quicklink that is never selected, so it is flashed instead. */
  function stageAnchor() {
    var target = readBody ? readBody.querySelector('[data-search-target="true"]') : null;
    var section = target ? target.closest('[id^="ti-"]') : null;
    return section ? section.id.slice(3) : null;
  }
  function anchorFromUrl(url) {
    var hash = String(url || '').indexOf('#');
    return hash === -1 ? null : url.slice(hash + 1).replace(/^ti-/, '');
  }
  /* "here you are": centre the rows that identify what is on stage -- the panel
     tile (book / songbook / service) and the list row (chapter / song / contents
     item). Only ever called for the two reveal moments: a search result opened,
     or a sidebar opened on the page being read. */
  function revealCurrent(anchor) {
    revealRow(panelBody.querySelector('.book[aria-current="true"]'), panelBody);
    if (activeSection === 'alkitab') {
      revealRow(chList.querySelector('.ch-num[aria-current="true"]'), chBody);
    } else if (activeSection === 'kidung') {
      revealRow(chList.querySelector('.songrow[aria-current="true"]'), chBody);
    } else if (activeSection === 'tatib' && anchor) {
      var row = null;
      chList.querySelectorAll('.songrow').forEach(function (x) {
        if (x.dataset.i === anchor) row = x;
      });
      revealRow(row, chBody, { flash: true });
    }
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
    hideTips();
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
    hideTips();
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
    if (root.dataset.nav !== 'closed' && row) row.focus({ preventScroll: true });
    else panelOwner().focus();
  });

  /* book tiles: the page's own book toggles its chapter list in place;
     another book is a normal link to its own page */
  function bindPanelTiles() {
    panelBody.querySelectorAll('.book').forEach(function (tile) {
      tile.addEventListener('click', function (event) {
        if (activeSection === 'alkitab' && tile.dataset.name === pageState.tileName) {
          /* the open book toggles its chapter list in place */
          event.preventDefault();
          hideTileTip();
          if (root.dataset.ch === 'open') closeChapters(true);
          else openChaptersInPlace(pageState.tileName);
          return;
        }
        /* another book / songbook / service: navigate in place */
        event.preventDefault();
        hideTileTip();
        var href = tile.getAttribute('href') || '';
        navigate(tile.href, { kind: /\/tatib\//.test(href) ? 'service' : 'lists' });
      });
    });
    var mode = panel.querySelector('.panel__filter .panel__mode');
    if (mode) {
      mode.addEventListener('click', function (event) {
        event.preventDefault();
        navigate(mode.href, { kind: 'mode' });
      });
    }
  }
  bindPanelTiles();

  /* ---------- Tata Ibadah contents: quicklinks that jump, never selected ---------- */
  function jumpTatibItem(anchor) {
    var target = document.getElementById(anchor);
    if (!target) return;
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    var previous = readBody.querySelector('.tatib__flash');
    if (previous) previous.classList.remove('tatib__flash');
    target.classList.add('tatib__flash');
  }
  function bindChRows() {
    chList.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function (event) {
        var href = link.getAttribute('href') || '';
        if (href.charAt(0) === '#') {
          /* Tata Ibadah contents are quicklinks, never a destination */
          event.preventDefault();
          jumpTatibItem(href.slice(1));
          if (mqNarrow.matches) closeChapters(false);
          return;
        }
        if (link.classList.contains('ch-num') && link.classList.contains('no-data')) {
          event.preventDefault();          /* no text in this edition: inert tile */
          return;
        }
        if (link.classList.contains('ch-num') || link.classList.contains('songrow')) {
          event.preventDefault();
          navigate(link.href, { kind: link.classList.contains('ch-num') ? 'chapter' : 'song' });
        }
      });
    });
  }
  bindChRows();

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
        if (root.dataset.nav !== 'closed' && row) row.focus({ preventScroll: true });
        else panelOwner().focus();
      }
    }
  });

  /* ---------- song-list order: recently updated <-> alphabetical ---------- */
  function songRowEls() {
    return Array.prototype.filter.call(chList.children, function (li) {
      return li.querySelector('.songrow');
    });
  }
  function applySongOrder() {
    var rows = songRowEls();
    rows.sort(function (x, y) {
      var rx = x.querySelector('.songrow');
      var ry = y.querySelector('.songrow');
      if (songSort === 'title') {
        /* The key ignores a title's own leading "435. ", or A-Z would just repeat
           the file order. */
        var xt = String(rx.dataset.t || '');
        var yt = String(ry.dataset.t || '');
        if (xt !== yt) return xt < yt ? -1 : 1;
        return (parseInt(rx.dataset.o, 10) || 0) - (parseInt(ry.dataset.o, 10) || 0);
      }
      /* Last modified, newest first. Every song in the corpus currently shares one
         timestamp, so the tiebreak -- the file's own order -- is what you see. */
      var recent = (parseFloat(ry.dataset.m) || 0) - (parseFloat(rx.dataset.m) || 0);
      return recent || (parseInt(rx.dataset.o, 10) || 0) - (parseInt(ry.dataset.o, 10) || 0);
    });
    var frag = document.createDocumentFragment();
    rows.forEach(function (li) { frag.appendChild(li); });
    chList.appendChild(frag);
    updateChInds();
  }
  function syncSortBtn() {
    var recent = songSort === 'm';
    var label = recent
      ? 'Sort: last modified \u2014 switch to alphabetical'
      : 'Sort: alphabetical \u2014 switch to last modified';
    songSortBtn.setAttribute('aria-label', label);
    songSortBtn.title = label;
    songSortBtn.dataset.order = recent ? 'm' : 'title';
  }
  songSortBtn.addEventListener('click', function () {
    if (songSortBtn.hidden) return;
    songSort = songSort === 'm' ? 'title' : 'm';
    syncSortBtn();
    applySongOrder();
  });
  if (!songSortBtn.hidden) syncSortBtn();

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
    hideTips();
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
    hideTips();
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
      event.preventDefault();
      var fromClosed = root.dataset.nav === 'closed' && root.dataset.ch === 'closed';
      if (name !== activeSection) {
        /* another section: fetch its root and morph the shell in place */
        navigate(btn.getAttribute('href'), { kind: 'rail', section: name });
        return;
      }
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
    if (root.dataset.read !== 'on' || stageSection() !== name) return;
    if (chList.children.length === 0) {
      /* a section switch wiped the lists: rebuild them from the stage's page */
      if (stageInfo.url) navigate(stageInfo.url, { kind: 'sync' });
      return;
    }
    var tile = null;
    panelBody.querySelectorAll('.book').forEach(function (row) {
      if (String(row.dataset.name) === String(stageInfo.tile)) tile = row;
    });
    if (!tile) return;
    if (tile.closest('.is-hidden')) {
      filter.value = '';
      applyFilter('');
    }
    if (name === 'alkitab') openChaptersInPlace(stageInfo.tile);
    else {
      markBookTile(stageInfo.tile);
      root.dataset.ch = 'open';
      markRailTile();
      syncState();
      updateChInds();
    }
    revealCurrent(stageAnchor());
    /* On narrow screens the child replaced its parent: hand focus to the
       exact reading destination, or the contents collapse control. */
    if (root.dataset.nav === 'closed') {
      var selected = chList.querySelector('[aria-current="true"]');
      if (selected) selected.focus({ preventScroll: true });
      else chCollapse.focus({ preventScroll: true });
    }
  }

  /* ---------- in-page navigation: fetch a page, swap the shell in place ----------
     Every click inside the shell loads its target page in the background and
     swaps the sidebar / list / stage fragments, so the push and wipe
     transitions run instead of a full reload. The links keep their real
     hrefs: without JS (or when a fetch fails) the browser navigates. */
  var navBusy = false;

  function navigate(url, opts) {
    if (!url || navBusy) return;
    /* Unsaved work in the pane asks first -- an order being rearranged (spec 006, slice 3).
       It owns the navigation from here: it answers, then calls back. */
    if (window.gkpsUnsaved && window.gkpsUnsaved.holds()) {
      window.gkpsUnsaved.ask(function () { navigate(url, opts); });
      return;
    }
    /* Leaving the result set by any route: remember where in it the reader was,
       so the search icon can come back to that offset. */
    if (root.dataset.home === 'results'
        && !(opts && (opts.kind === 'search' || opts.kind === 'more' || opts.kind === 'results'))) {
      try { localStorage.setItem('gkps-search-scroll', String(window.scrollY)); } catch (e) {}
    }
    navBusy = true;
    fetch(url, { credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch' } })
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.text();
      })
      .then(function (html) {
        navBusy = false;
        applyPage(new window.DOMParser().parseFromString(html, 'text/html'), url, opts || {});
      })
      .catch(function (error) {
        navBusy = false;
        if (window.console && console.error) console.error('in-page navigation failed:', error);
        window.location.href = url;      /* fetch failed: fall back to the real page */
      });
  }

  function txt(doc, sel) {
    var el = doc.querySelector(sel);
    return el ? el.textContent : '';
  }

  function applyPage(doc, url, opts) {
    var fresh = doc.documentElement.dataset;
    var kind = opts.kind || 'lists';
    var swapsStage = kind === 'chapter' || kind === 'song' || kind === 'service'
      || kind === 'result' || kind === 'more' || kind === 'search' || kind === 'results'
      || kind === 'refresh';

    /* shared first column: books / songbooks / services */
    panelTitleEl.textContent = txt(doc, '#panelTitle');
    panelFilterLabel.textContent = txt(doc, 'label[for="bookFilter"]');
    var freshFilter = doc.querySelector('#bookFilter');
    if (freshFilter) filter.placeholder = freshFilter.getAttribute('placeholder') || '';
    panelBody.innerHTML = doc.querySelector('#panelBody').innerHTML;
    var freshEmpty = doc.querySelector('#panelEmpty');
    if (freshEmpty) {
      panelEmpty.textContent = freshEmpty.textContent;
      panelEmpty.hidden = freshEmpty.hidden;
    }
    var freshPanelCollapse = doc.querySelector('#panelCollapse');
    if (freshPanelCollapse) panelCollapse.setAttribute('aria-label', freshPanelCollapse.getAttribute('aria-label'));
    /* the Tata Ibadah mode switch lives in the filter strip */
    var oldMode = panel.querySelector('.panel__filter .panel__mode');
    var newMode = doc.querySelector('.panel__filter .panel__mode');
    if (newMode) {
      var imported = document.importNode(newMode, true);
      if (oldMode) oldMode.parentNode.replaceChild(imported, oldMode);
      else panel.querySelector('.panel__filter').appendChild(imported);
    } else if (oldMode) {
      oldMode.parentNode.removeChild(oldMode);
    }

    /* shared second column: chapters / song list / service contents */
    chTitleEl.textContent = txt(doc, '#chTitle');
    chFilterLabel.textContent = txt(doc, 'label[for="songFilter"]');
    var freshSongFilter = doc.querySelector('#songFilter');
    if (freshSongFilter) songFilterEl.placeholder = freshSongFilter.getAttribute('placeholder') || '';
    var freshChSearch = doc.querySelector('.ch__search');
    if (freshChSearch) chSearchEl.hidden = freshChSearch.hidden;
    songEmpty.hidden = true;
    songEmpty.textContent = txt(doc, '#chEmpty') || songEmpty.textContent;
    var freshChCollapse = doc.querySelector('#chCollapse');
    if (freshChCollapse) chCollapse.setAttribute('aria-label', freshChCollapse.getAttribute('aria-label'));
    var freshSort = doc.querySelector('#songSort');
    if (freshSort) songSortBtn.hidden = freshSort.hidden;
    chList.innerHTML = doc.querySelector('#chList').innerHTML;

    /* state */
    activeSection = fresh.section || activeSection;
    root.dataset.section = activeSection;
    if (fresh.chMode) root.dataset.chMode = fresh.chMode;

    if (swapsStage) {
      root.dataset.read = fresh.read;
      root.dataset.home = fresh.home;
      root.dataset.nav = fresh.nav;
      root.dataset.ch = fresh.ch;
      stage.innerHTML = doc.querySelector('.stage').innerHTML;
      refreshStageRefs();
      restoreSavedEdition();
      bindLangLinks();
      bindSearchForm();
      bindFieldClears();
      bindStageExtras();
    } else if (kind === 'rail') {
      /* section switch: the lists move to the target section; the stage keeps
         whatever it shows (mockup: setSection + openPanel) */
      if (root.dataset.ch === 'open') closeChapters();
      chList.innerHTML = '';
      root.dataset.ch = 'closed';
      root.dataset.nav = fresh.nav || 'open';
    } else if (kind === 'sync') {
      root.dataset.nav = fresh.nav || 'open';
      root.dataset.ch = fresh.ch || root.dataset.ch;
    } else {
      root.dataset.nav = fresh.nav || root.dataset.nav;
      root.dataset.ch = fresh.ch || root.dataset.ch;
    }

    /* The sidebar add buttons sit outside the swapped regions, so they cannot be
       updated in place: a page that never had one (the search-first home) has no
       element to update, which is exactly how they went missing on the home ->
       section path. Swap them whole from the page that just arrived instead, and
       drop them when it has none (Alkitab). */
    /* The mode toggle belongs to the Tata Ibadah toolbar only. Syncing the toolbar's
       labels was not enough: on the home -> section path the button itself was absent,
       so the section's toggle never appeared and the collapse sat in its place. */
    (function () {
      var toolbarEl = document.querySelector('.panel__filter');
      if (!toolbarEl) return;
      var live = document.getElementById('tatibMode');
      var fresh = doc.querySelector('#tatibMode');
      if (fresh && !live) {
        toolbarEl.insertBefore(fresh.cloneNode(true), toolbarEl.firstChild);
        live = document.getElementById('tatibMode');
      } else if (live && !fresh) {
        live.parentNode.removeChild(live);
        live = null;
      } else if (live && fresh) {
        ['href', 'aria-label', 'title', 'hidden'].forEach(function (attr) {
          if (fresh.hasAttribute(attr)) live.setAttribute(attr, fresh.getAttribute(attr));
          else live.removeAttribute(attr);
        });
        live.innerHTML = fresh.innerHTML;
      }
      /* One deterministic order, whatever the swap left behind: the mockup's
         [field, toggle, collapse]. Appending each in turn re-parents them. */
      [toolbarEl.querySelector('.filter-box'), live,
       document.getElementById('panelCollapse')].forEach(function (el) {
        if (el && el.parentNode) el.parentNode.appendChild(el);
      });
    })();
    var panelEl = document.getElementById('panel');
    var panelFilter = panelEl && panelEl.querySelector('.panel__filter');
    var oldPanelAdd = document.getElementById('panelAdd');
    if (oldPanelAdd) oldPanelAdd.parentNode.removeChild(oldPanelAdd);
    var freshPanelAdd = doc.querySelector('#panelAdd');
    if (freshPanelAdd && panelFilter && panelFilter.parentNode) {
      panelFilter.parentNode.insertBefore(freshPanelAdd, panelFilter.nextSibling);
    }
    var chTop = document.querySelector('.ch__top');
    var oldChAdd = document.querySelector('.ch__add');
    if (oldChAdd) oldChAdd.parentNode.removeChild(oldChAdd);
    var freshChAdd = doc.querySelector('.ch__add');
    if (freshChAdd && chTop && chTop.parentNode) {
      chTop.parentNode.insertBefore(freshChAdd, chTop.nextSibling);
    }
    /* the Tata Ibadah reorder strip: created and dropped with the section that owns it,
       right below the filter where the sidebar does not scroll */
    var oldChOrder = document.querySelector('.ch__reorder');
    if (oldChOrder) oldChOrder.parentNode.removeChild(oldChOrder);
    var freshChOrder = doc.querySelector('.ch__reorder');
    if (freshChOrder && chTop && chTop.parentNode) {
      chTop.parentNode.insertBefore(freshChOrder, chTop.nextSibling);
    }

    bindPanelTiles();
    bindPanelTips();
    bindChRows();

    pageState = readPageState();
    if (swapsStage) {
      stageInfo = { tile: pageState.tileName, chapter: pageState.chapter,
                    song: pageState.songId, url: url };
    }
    decorateChapters();
    markRailTile();
    syncState();
    updateChInds();
    window.requestAnimationFrame(updateChInds);

    /* The rail search icon restores the last result set. Only the page that IS
       the result set may update it -- a stale root state must never let a
       reading page overwrite the stored search. */
    if (fresh.home === 'results') {
      var searchPath = url.indexOf(window.location.origin) === 0
        ? url.slice(window.location.origin.length) : url;    /* store a path, not an origin */
      try { localStorage.setItem('gkps-search', searchPath); } catch (e) {}
      railSearch.setAttribute('href', searchPath);
    }
    document.title = doc.title;

    /* Anything the arriving page carries and another script owns -- the project
       button, for one -- needs its hook run again: the swap replaced the node the
       earlier binding sat on, which is how a control can be present on a deep link
       and dead on the path a person actually clicks through. */
    document.dispatchEvent(new CustomEvent('shell:page', {detail: {url: url, kind: kind}}));

    /* per-kind endings */
    if (kind === 'rail') {
      restoreCurrentPath(opts.section);
    }
    if (kind === 'sync') {
      revealCurrent(stageAnchor());
      if (root.dataset.nav === 'closed') {
        var syncRow = chList.querySelector('[aria-current="true"]');
        if (syncRow) syncRow.focus({ preventScroll: true });
        else chCollapse.focus({ preventScroll: true });
      }
    }
    if (kind === 'chapter' || kind === 'song' || kind === 'service') {
      if (kind === 'song' && mqNarrow.matches) closeChapters(false);
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    }
    if (kind === 'result') {
      revealCurrent(anchorFromUrl(url) || stageAnchor());
      var target = readBody ? readBody.querySelector('[data-search-target="true"]') : null;
      if (target) revealSearchTarget(target);
    }
    if (kind === 'refresh' && opts.what) {
      /* a save just closed its modal: show the row it touched */
      var saved = chList.querySelector('[data-editor-id="' + opts.what + '"]')
        || panelBody.querySelector('[data-editor-id="' + opts.what + '"]');
      if (saved) {
        var row = saved.closest('a') || saved;
        var scroller = panelBody.contains(row) ? panelBody : chBody;
        revealRow(row, scroller);
        row.classList.add('row-flash');
        saved.focus({ preventScroll: true });
      }
    }
    if (kind === 'search') {
      window.scrollTo({ top: 0, behavior: 'auto' });
    }
    if (kind === 'results') {
      /* landed on the result set: resume where the reader left it */
      var remembered = 0;
      if (fresh.home === 'results') {
        try { remembered = parseInt(localStorage.getItem('gkps-search-scroll') || '0', 10) || 0; } catch (e) {}
      }
      window.scrollTo({ top: remembered, behavior: 'auto' });
    }
  }

  /* results and "Show more" open in place too */
  function bindStageExtras() {
    if (!stage) return;
    stage.querySelectorAll('.result-row').forEach(function (row) {
      row.addEventListener('click', function (event) {
        event.preventDefault();
        navigate(row.href, { kind: 'result' });
      });
    });
    stage.querySelectorAll('.result-more').forEach(function (more) {
      more.addEventListener('click', function (event) {
        event.preventDefault();
        navigate(more.href, { kind: 'more' });
      });
    });
  }
  bindStageExtras();

  /* ---------- Escape closes the innermost open layer ---------- */
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    /* an open modal (the editors' <dialog>) is the innermost layer: the browser
       closes it and the keypress must stop there, or Esc also closes the sidebar
       behind it (review report) */
    if (document.querySelector('dialog[open]')) return;
    if (root.dataset.ch === 'open') {
      closeChapters(true);
      var row = panelBody.querySelector('.book[aria-current="true"]');
      if (root.dataset.nav !== 'closed' && row) row.focus({ preventScroll: true });
      else panelOwner().focus();
    } else if (root.dataset.nav !== 'closed') {
      closePanel();
      panelOwner().focus();
    }
  });

  /* ---------- search: any non-empty query runs, in place ---------- */
  /* ---------- clear controls: one per search / filter field ----------
     Shown only while the field holds something; clearing fires the field's own
     input event (so a filter re-applies) and leaves focus in the field. */
  function bindFieldClear(box) {
    var input = box.querySelector('input');
    var clear = box.querySelector('.field-clear');
    if (!input || !clear || clear.dataset.bound) return;
    clear.dataset.bound = 'true';
    var label = input.id ? document.querySelector('label[for="' + input.id + '"]') : null;
    var text = label ? label.textContent.trim() : '';
    text = text.replace(/^Filter\s+/i, '').replace(/^Search\b.*$/i, 'search');
    clear.setAttribute('aria-label', text ? 'Clear ' + text : 'Clear this field');
    function sync() { clear.hidden = input.value === ''; }
    clear.addEventListener('click', function () {
      if (input.value === '') return;
      input.value = '';
      sync();
      input.dispatchEvent(new window.Event('input', { bubbles: true }));
      input.focus();
    });
    ['input', 'change', 'search'].forEach(function (ev) { input.addEventListener(ev, sync); });
    sync();
  }
  function bindFieldClears() {
    document.querySelectorAll('.filter-box, .search-home__form').forEach(bindFieldClear);
  }
  bindFieldClears();

  function bindSearchForm() {
    if (!searchForm) return;
    searchForm.addEventListener('submit', function (event) {
      var input = searchForm.querySelector('#searchQuery') || searchQuery;
      var query = input ? input.value.trim() : '';
      if (!query) { event.preventDefault(); return; }
      input.value = query;
      event.preventDefault();
      var action = searchForm.getAttribute('action') || '/search/';
      navigate(action + '?q=' + encodeURIComponent(query), { kind: 'search' });
    });
  }
  bindSearchForm();
  try {
    if (root.dataset.home === 'results') {
      /* remember the exact result URL, revealed rows included */
      localStorage.setItem('gkps-search', window.location.pathname + window.location.search);
    }
    var lastSearch = storedSearchUrl();
    if (lastSearch) railSearch.setAttribute('href', lastSearch);
  } catch (e) {}

  /* The stored result-set URL, or nothing. A value written by an older build (or
     any non-search URL) is dropped, so the search icon can never open a reading
     page's sidebar by mistake. */
  function storedSearchUrl() {
    var value = null;
    try { value = localStorage.getItem('gkps-search'); } catch (e) {}
    if (value && /^\/search\/\?q=/.test(value)) return value;
    if (value) { try { localStorage.removeItem('gkps-search'); } catch (e) {} }
    return null;
  }

  /* The search destination. The rail's Search icon and the brand logo are the same
     route (owner request): back to the last result set, or the landing when there
     is none. Only the result page itself updates what is stored -- nothing clears
     it. */
  function openSearch(event) {
    event.preventDefault();
    navigate(storedSearchUrl() || '/home/', { kind: 'results' });
  }
  railSearch.addEventListener('click', openSearch);
  var railLogo = document.querySelector('.rail__logo');
  if (railLogo) railLogo.addEventListener('click', openSearch);

  /* A sidebar editor saved something: re-render the page's regions in place, so
     every list, the panel selection and the reading stage agree again. */
  document.addEventListener('editor:saved', function (event) {
    /* In-page navigation does not change location: a service opened from /home/
       still has /home/ in the address bar. Refresh the URL that supplied the
       displayed stage, not the landing page behind it. */
    navigate(readKind() ? stageInfo.url : window.location.pathname + window.location.search,
             { kind: 'refresh', what: event.detail && event.detail.id });
  });

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
  revealCurrent(stageAnchor() || anchorFromUrl(window.location.hash));
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
