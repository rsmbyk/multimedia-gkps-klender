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
  var railMediaLibrary = document.getElementById('railMediaLibrary');
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
  var idleCollapseTimer = null;
  var IDLE_COLLAPSE_DELAY = 60000;
  var navBeforeCh = null;
  var pendingAnchor = null;
  var railCloseTimer = null;
  var railCloseListener = null;
  var selectionTransitionRestores = new WeakMap();

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

  function cancelIdleCollapse() {
    if (idleCollapseTimer !== null) window.clearTimeout(idleCollapseTimer);
    idleCollapseTimer = null;
  }
  function idleCollapseIsDeferred() {
    return panel.contains(document.activeElement)
      || !!document.querySelector('.ui.modal.visible, dialog[open], .is-dragging');
  }
  function scheduleIdleCollapse(delay, resumeAfterDeferred) {
    cancelIdleCollapse();
    if (mqNarrow.matches || root.dataset.nav !== 'open'
        || activeSection !== stageSection()) return;
    idleCollapseTimer = window.setTimeout(function () {
      idleCollapseTimer = null;
      if (mqNarrow.matches || root.dataset.nav !== 'open'
          || activeSection !== stageSection()) return;
      if (document.visibilityState === 'hidden') return;
      if (idleCollapseIsDeferred()) {
        /* A modal or an active drag can outlive the idle interval. Check again
           until it ends, then give the operator a full quiet interval. */
        if (!panel.contains(document.activeElement)) scheduleIdleCollapse(1000, true);
        return;
      }
      if (resumeAfterDeferred) { scheduleIdleCollapse(); return; }
      if (activeSection === 'alkitab') miniPanel();
      else closePanel();
    }, delay == null ? IDLE_COLLAPSE_DELAY : delay);
  }
  function noteSidebarActivity() {
    scheduleIdleCollapse();
  }
  ['pointerdown', 'pointermove', 'keydown', 'focusin', 'wheel', 'scroll'].forEach(function (eventName) {
    rail.addEventListener(eventName, noteSidebarActivity, { passive: true });
    panel.addEventListener(eventName, noteSidebarActivity, { passive: true });
  });
  panel.addEventListener('focusout', function (event) {
    if (!panel.contains(event.relatedTarget)) noteSidebarActivity();
  });
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') cancelIdleCollapse();
    else scheduleIdleCollapse();
  });
  function onIdleCollapseViewportChange() {
    if (mqNarrow.matches) cancelIdleCollapse();
    else scheduleIdleCollapse();
  }
  if (mqNarrow.addEventListener) mqNarrow.addEventListener('change', onIdleCollapseViewportChange);
  else mqNarrow.addListener(onIdleCollapseViewportChange);

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

  /* Keep stable reading nodes mounted while applying a server or saved-copy
     response. Stable keys let rows move without losing identity; unkeyed nodes
     are matched in place by position and element type. */
  function nodeIdentity(node) {
    if (!node || node.nodeType !== 1) return null;
    var attrs = ['id', 'data-entry-pk', 'data-old-item-pk', 'data-anchor',
      'data-entry-after', 'data-i', 'data-name', 'data-month', 'data-testament',
      'data-ed', 'data-move-grip'];
    for (var i = 0; i < attrs.length; i++) {
      var value = node.getAttribute(attrs[i]);
      if (value !== null) return node.tagName + ':' + attrs[i] + ':' + value;
    }
    if (node.tagName === 'LI') {
      var row = node.querySelector('a[data-i], a.book[data-name], a.songrow, a.ch-num');
      if (row) return 'LI:row:' + (nodeIdentity(row) || row.getAttribute('href') || '');
      var grip = node.querySelector('[data-move-grip]');
      if (grip) return 'LI:grip:' + grip.getAttribute('data-move-grip');
    }
    if (node.matches('a[href]')) return 'A:href:' + node.getAttribute('href');
    return null;
  }

  function compatibleNodes(live, fresh) {
    if (!live || !fresh || live.nodeType !== fresh.nodeType) return false;
    if (live.nodeType !== 1) return true;
    if (live.tagName !== fresh.tagName) return false;
    var liveKey = nodeIdentity(live);
    var freshKey = nodeIdentity(fresh);
    if (liveKey !== freshKey) return false;
    if (live.id === 'read' && live.dataset.kind !== fresh.dataset.kind) return false;
    return true;
  }

  function reconcileNode(live, fresh) {
    if (!compatibleNodes(live, fresh)) {
      var replacement = document.importNode(fresh, true);
      if (live && live.parentNode) live.parentNode.replaceChild(replacement, live);
      return replacement;
    }
    if (live.nodeType !== 1) {
      if (live.nodeValue !== fresh.nodeValue) live.nodeValue = fresh.nodeValue;
      return live;
    }
    if (live.isEqualNode(fresh)) return live;
    var selectionChanged = live.matches('.book, .songrow, .ch-num')
      && live.getAttribute('aria-current') !== fresh.getAttribute('aria-current');

    Array.prototype.slice.call(live.attributes).forEach(function (attribute) {
      if (!fresh.hasAttribute(attribute.name)) live.removeAttribute(attribute.name);
    });
    Array.prototype.forEach.call(fresh.attributes, function (attribute) {
      if (live.getAttribute(attribute.name) !== attribute.value) {
        live.setAttribute(attribute.name, attribute.value);
      }
    });
    if (selectionChanged) {
      var transitionState = selectionTransitionRestores.get(live);
      if (transitionState) window.clearTimeout(transitionState.timer);
      else transitionState = {
        value: live.style.getPropertyValue('transition'),
        priority: live.style.getPropertyPriority('transition')
      };
      live.style.setProperty('transition', 'none', 'important');
      transitionState.timer = window.setTimeout(function () {
        if (transitionState.value) {
          live.style.setProperty('transition', transitionState.value, transitionState.priority);
        } else {
          live.style.removeProperty('transition');
        }
        selectionTransitionRestores.delete(live);
      }, 250);
      selectionTransitionRestores.set(live, transitionState);
    }
    reconcileChildren(live, fresh);
    return live;
  }

  function reconcileChildren(liveParent, freshParent) {
    var desired = Array.prototype.slice.call(freshParent.childNodes);
    var cursor = liveParent.firstChild;
    desired.forEach(function (freshChild) {
      var key = nodeIdentity(freshChild);
      var candidate = null;
      if (key) {
        candidate = Array.prototype.find.call(liveParent.childNodes, function (child) {
          return nodeIdentity(child) === key && compatibleNodes(child, freshChild);
        });
      } else if (freshChild.nodeType === 1) {
        var search = cursor;
        while (search) {
          if (!nodeIdentity(search) && compatibleNodes(search, freshChild)) {
            candidate = search;
            break;
          }
          search = search.nextSibling;
        }
      } else if (compatibleNodes(cursor, freshChild) && !nodeIdentity(cursor)) {
        candidate = cursor;
      }
      if (!candidate) {
        candidate = document.importNode(freshChild, true);
        liveParent.insertBefore(candidate, cursor);
      } else {
        if (candidate !== cursor) liveParent.insertBefore(candidate, cursor);
        reconcileNode(candidate, freshChild);
      }
      cursor = candidate.nextSibling;
    });
    while (cursor) {
      var next = cursor.nextSibling;
      liveParent.removeChild(cursor);
      cursor = next;
    }
  }

  function setTextIfChanged(element, value) {
    value = value || '';
    if (element && element.textContent !== value) element.textContent = value;
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
  rail.addEventListener('click', function (event) {
    hideTip();
    window.setTimeout(hideTip, 260);         /* after any re-focus the state change does */
    var mainMenu = event.target.closest('.rail__btn[data-panel]');
    if (mainMenu && railMediaLibrary) railMediaLibrary.removeAttribute('aria-current');
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
    if (boundFloatTips.has(el)) return;
    boundFloatTips.add(el);
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
  var boundFloatTips = new WeakSet();
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
  var systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  function applyTheme(mode, persist) {
    root.dataset.themeMode = mode;
    root.dataset.theme = mode === 'system'
      ? (systemTheme.matches ? 'dark' : 'light') : mode;
    var label = mode.charAt(0).toUpperCase() + mode.slice(1) + ' mode';
    themeBtn.setAttribute('aria-label', label);
    themeBtn.setAttribute('data-tip', label);
    if (persist) { try { localStorage.setItem('gkps-theme', mode); } catch (e) {} }
  }
  themeBtn.addEventListener('click', function () {
    var mode = root.dataset.themeMode;
    applyTheme(mode === 'system' ? 'dark' : mode === 'dark' ? 'light' : 'system', true);
  });
  systemTheme.addEventListener('change', function () {
    if (root.dataset.themeMode === 'system') applyTheme('system', false);
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
  var rememberedEdition = root.dataset.bibleEdition;
  var requestedEdition = new URLSearchParams(location.search).get('ed') === 'sim' ? 'sim' : null;
  var selectedEdition = rememberedEdition === 'sim' || rememberedEdition === 'tb'
    ? rememberedEdition : requestedEdition || currentEdition();
  /* The document root survives every in-page menu and stage swap, but a full
     load gets a fresh root. Keep the tab-local choice there so shell hooks can
     reinitialize without mistaking a non-Bible page's language for the choice. */
  root.dataset.bibleEdition = selectedEdition;
  function syncRailTranslationLabels() {
    var names = selectedEdition === 'sim'
      ? { alkitab: 'Bibel', kidung: 'Doding', tatib: 'Agenda' }
      : { alkitab: 'Alkitab', kidung: 'Kidung', tatib: 'Tata Ibadah' };
    Object.keys(names).forEach(function (section) {
      var button = rail.querySelector('[data-panel="' + section + '"]');
      if (!button) return;
      var label = names[section];
      if (button.dataset.tip !== label) button.dataset.tip = label;
      if (button.getAttribute('aria-label') !== label) button.setAttribute('aria-label', label);
      if (button.getAttribute('data-tip-open') === 'true') {
        button.setAttribute('aria-describedby', 'tip-' + label.replace(/\s+/g, '-'));
      }
    });
  }
  function syncBibleSidebar() {
    if (activeSection !== 'alkitab') return;
    var simPrimary = selectedEdition === 'sim';
    panelBody.querySelectorAll('.group__head[data-label-tb]').forEach(function (heading) {
      var label = heading.dataset[simPrimary ? 'labelSim' : 'labelTb'];
      if (label && heading.textContent !== label) heading.textContent = label;
    });
    panelBody.querySelectorAll('.book').forEach(function (row) {
      var tb = row.dataset.name || '';
      var sim = row.dataset.sim || '';
      var hasTb = row.dataset.hasTb ? row.dataset.hasTb === 'true' : !!tb;
      var hasSim = row.dataset.hasSim ? row.dataset.hasSim === 'true' : !!sim;
      var primary = simPrimary && hasSim ? sim : tb;
      var secondary = hasTb && hasSim ? (simPrimary ? tb : sim) : '';
      var code = simPrimary ? row.dataset.simCode || row.dataset.tbCode
        : row.dataset.tbCode || '';
      var name = row.querySelector('.book__n');
      var other = row.querySelector('.book__s');
      var abbreviation = row.querySelector('.book__a');
      if (name && name.textContent !== primary) name.textContent = primary;
      if (abbreviation && code && abbreviation.textContent !== code) {
        abbreviation.textContent = code;
      }
      if (other) {
        if (secondary) {
          if (other.textContent !== secondary) other.textContent = secondary;
        } else other.remove();
      } else if (secondary && name) {
        other = document.createElement('span');
        other.className = 'book__s';
        other.textContent = secondary;
        row.appendChild(other);
      }
      var description = primary + (secondary ? ' (' + secondary + ')' : '');
      var tip = primary + (secondary ? ' — ' + secondary : '');
      if (row.getAttribute('aria-label') !== description) row.setAttribute('aria-label', description);
      if (row.dataset.tip !== tip) row.dataset.tip = tip;
      if (row.getAttribute('aria-describedby') === 'ftip') ftip.textContent = tip;
    });
  }
  function editionBlock(ed) {
    var found = null;
    editionBlocks.forEach(function (block) { if (block.ed === ed) found = block; });
    return found;
  }
  function syncVisibleBibleTitle() {
    if (!readEl || readEl.dataset.kind !== 'bible') return;
    var visibleBlock = null;
    editionBlocks.forEach(function (block) {
      if (!block.el.hidden) visibleBlock = block;
    });
    if (!visibleBlock) return;
    var name = visibleBlock.el.dataset.name || '';
    var readName = document.getElementById('readName');
    if (name && readName && readName.textContent !== name) readName.textContent = name;
    if (!name) return;
    var number = document.getElementById('readNo');
    document.title = name + (number && number.textContent ? ' ' + number.textContent : '')
      + ' — GKPS Klender';
  }
  function decorateChapters() {
    if (activeSection !== 'alkitab') return;
    var ed = selectedEdition;
    chList.querySelectorAll('.ch-num').forEach(function (a) {
      var ok = ed === 'sim' ? a.dataset.sim === 'true' : a.dataset.tb === 'true';
      a.classList.toggle('no-data', !ok);
      if (ok) a.removeAttribute('aria-disabled');
      else a.setAttribute('aria-disabled', 'true');
    });
  }
  function setEdition(ed, remember) {
    if (!editionBlocks.length) return;
    editionBlocks.forEach(function (block) { block.el.hidden = block.ed !== ed; });
    if (readEl) readEl.setAttribute('lang', ed === 'tb' ? 'id' : 'sim');
    if (langTb) langTb.setAttribute('aria-pressed', String(ed !== 'sim'));
    if (langSim) langSim.setAttribute('aria-pressed', String(ed === 'sim'));
    if (langTb) langTb.parentElement.dataset.edition = ed;
    if (remember) {
      selectedEdition = ed;
      root.dataset.bibleEdition = ed;
    }
    decorateChapters();
    syncBibleSidebar();
    syncRailTranslationLabels();
    syncVisibleBibleTitle();
  }
  function bindLangLinks() {
    if (!stage.dataset.langLinksBound) {
      stage.dataset.langLinksBound = 'true';
      stage.addEventListener('click', function (event) {
        var link = event.target.closest('#langTb, #langSim');
        if (!link || !stage.contains(link)) return;
        var want = link.id === 'langSim' ? 'sim' : 'tb';
        /* no text in the other edition: keep the last good view */
        if (!editionBlock(want) || want === currentEdition()) { event.preventDefault(); return; }
        event.preventDefault();
        setEdition(want, true);
      });
    }
    if (langTb) langTb.parentElement.classList.add('is-enhanced');
  }
  function restoreSelectedEdition() {
    if (selectedEdition !== currentEdition() && editionBlock(selectedEdition)) {
      setEdition(selectedEdition, false);
    }
  }
  restoreSelectedEdition();
  syncBibleSidebar();
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
  function ensureVisible(row, body, inset) {
    if (!row) return;
    var r = row.getBoundingClientRect();
    var b = body.getBoundingClientRect();
    inset = inset || 0;
    if (r.top < b.top + inset) body.scrollTop -= (b.top + inset - r.top);
    else if (r.bottom > b.bottom - inset) body.scrollTop += (r.bottom - b.bottom + inset);
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
    if (!panelBody.dataset.tileClicksBound) {
      panelBody.dataset.tileClicksBound = 'true';
      panelBody.addEventListener('click', function (event) {
        var tile = event.target.closest('.book');
        if (!tile || !panelBody.contains(tile)) return;
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
        navigate(tile.href, {
          kind: activeSection === 'alkitab' ? 'bible-book'
            : /\/tatib\//.test(href) ? 'service' : 'lists'
        });
      });
    }
    if (!panel.dataset.modeClicksBound) {
      panel.dataset.modeClicksBound = 'true';
      panel.addEventListener('click', function (event) {
        var mode = event.target.closest('.panel__filter .panel__mode');
        if (!mode || !panel.contains(mode)) return;
        event.preventDefault();
        var target = mode.href;
        if (stageSection() === 'tatib' && stageInfo.tile) {
          target = new window.URL(stageInfo.url, window.location.href).pathname
            + new window.URL(mode.href, window.location.href).search;
        }
        navigate(target, { kind: 'mode' });
      });
    }
  }
  bindPanelTiles();

  /* ---------- Tata Ibadah contents: quicklinks that jump, never selected ---------- */
  var activeTatibFlash = null;
  function releaseTatibFlash() {
    if (!activeTatibFlash) return;
    activeTatibFlash.removeEventListener('animationend', onTatibFlashEnd);
    activeTatibFlash.removeEventListener('animationcancel', onTatibFlashEnd);
    activeTatibFlash.classList.remove('tatib__flash');
    activeTatibFlash = null;
  }
  function onTatibFlashEnd(event) {
    if (event.target !== activeTatibFlash || event.animationName !== 'tatibFlash') return;
    releaseTatibFlash();
  }
  function jumpTatibItem(anchor) {
    var target = document.getElementById(anchor);
    if (!target) return;
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (activeTatibFlash && !activeTatibFlash.isConnected) releaseTatibFlash();
    if (activeTatibFlash) return;
    if (prefersReduce()) return;
    activeTatibFlash = target;
    target.addEventListener('animationend', onTatibFlashEnd);
    target.addEventListener('animationcancel', onTatibFlashEnd);
    target.classList.add('tatib__flash');
  }
  function bindChRows() {
    if (chList.dataset.rowClicksBound) return;
    chList.dataset.rowClicksBound = 'true';
    chList.addEventListener('click', function (event) {
      var link = event.target.closest('a');
      if (!link || !chList.contains(link)) return;
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
          || String(row.dataset.tbCode).toLowerCase().indexOf(needle) !== -1
          || String(row.dataset.simCode).toLowerCase().indexOf(needle) !== -1
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
    if (activeSection === 'alkitab') {
      songEmpty.hidden = true;
      updateChInds();
      return;
    }
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
  document.addEventListener('shell:local-entry-delete', function () {
    applySongFilter(songFilterEl.value);
    decorateChapters();
    markRailTile();
    syncState();
    updateChInds();
    window.requestAnimationFrame(updateChInds);
  });
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
    syncRailTranslationLabels();
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
    if (snapshot) { restorePos(snapshot); scheduleIdleCollapse(); return; }
    filter.focus();
    filter.select();
    scheduleIdleCollapse();
  }
  function miniPanel() {
    cancelIdleCollapse();
    var snapshot = root.dataset.nav === 'open' ? snapshotPos() : null;
    root.dataset.nav = 'mini';
    syncState();
    if (snapshot) restorePos(snapshot);
  }
  function closePanel() {
    cancelIdleCollapse();
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
  var pendingNavigation = null;
  var navigationGeneration = 0;
  var SEARCH_LAST = 'gkps-search-last-tab';
  var TAB_KEY = 'gkps-search-tab-id';
  /* The shell owns in-page history, including restoring each search result's
     scroll position. Leave scroll restoration to the route renderer instead
     of letting the browser race it after popstate. */
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function searchId() {
    return window.crypto && crypto.randomUUID ? crypto.randomUUID()
      : Date.now() + '-' + Math.random().toString(36).slice(2);
  }
  (function establishTabIdentity() {
    try {
      var known = sessionStorage.getItem(TAB_KEY);
      if (known && (window.name === 'gkps-tab:' + known
                    || history.state && history.state.gkpsTab === known)) {
        window.name = 'gkps-tab:' + known;
        return;
      }
      /* A new opener-created tab can inherit a copy of sessionStorage. Its window
         name is distinct, so drop only search memories, never the shared library. */
      Object.keys(sessionStorage).filter(function (key) {
        return key === SEARCH_LAST || key.indexOf('gkps-search-entry:') === 0;
      }).forEach(function (key) { sessionStorage.removeItem(key); });
      known = searchId();
      sessionStorage.setItem(TAB_KEY, known);
      window.name = 'gkps-tab:' + known;
    } catch (error) { /* private mode still allows current-page search */ }
  })();
  function readSearchSnapshot(id) {
    try { return JSON.parse(sessionStorage.getItem('gkps-search-entry:' + id) || 'null'); }
    catch (error) { return null; }
  }
  function saveSearchSnapshot() {
    if (root.dataset.home !== 'results') return;
    var state = history.state || {};
    if (!state.searchId) {
      state.searchId = searchId();
      history.replaceState(state, '', location.href);
    }
    var results = document.getElementById('searchResults');
    var input = document.getElementById('searchQuery');
    try { sessionStorage.setItem('gkps-search-entry:' + state.searchId, JSON.stringify({
      url: location.pathname + location.search,
      html: results ? results.innerHTML : '',
      input: input ? input.value : '', scroll: window.scrollY
    })); } catch (error) { /* private mode or storage quota */ }
  }
  function restoreSearchSnapshot(id) {
    var snapshot = id && readSearchSnapshot(id);
    if (!snapshot) return false;
    var results = document.getElementById('searchResults');
    var input = document.getElementById('searchQuery');
    if (results) {
      var snapshotTemplate = document.createElement('template');
      snapshotTemplate.innerHTML = snapshot.html;
      reconcileChildren(results, snapshotTemplate.content);
    }
    if (input) input.value = snapshot.input;
    bindStageExtras();
    window.scrollTo({top: snapshot.scroll || 0, behavior: 'auto'});
    return true;
  }
  document.addEventListener('input', function (event) {
    if (event.target.id === 'searchQuery') saveSearchSnapshot();
  });
  window.addEventListener('scroll', function () {
    if (root.dataset.home === 'results') window.requestAnimationFrame(saveSearchSnapshot);
  }, {passive: true});
  window.addEventListener('pagehide', saveSearchSnapshot);

  function releaseNavigation(success, resolve) {
    navBusy = false;
    if (resolve) resolve(!!success);
    if (!pendingNavigation) return;
    var next = pendingNavigation;
    pendingNavigation = null;
    navigate(next.url, next.opts).then(next.resolve);
  }

  function navigate(url, opts) {
    if (!url) return Promise.resolve(false);
    opts = opts || {};
    var resolveCompletion;
    var completion = new Promise(function (resolve) { resolveCompletion = resolve; });
    if (navBusy) {
      if (!opts.historyTraversal) saveSearchSnapshot();
      if (pendingNavigation) pendingNavigation.resolve(false);
      pendingNavigation = {url: url, opts: opts, resolve: resolveCompletion};
      return completion;
    }
    if (!opts.historyTraversal) saveSearchSnapshot();
    navBusy = true;
    var generation = ++navigationGeneration;
    var finished = false;
    function finish(success) {
      if (finished) return;
      finished = true;
      releaseNavigation(success, resolveCompletion);
    }
    function isSuperseded() { return !!pendingNavigation; }
    function fail(error) {
      if (window.console && console.error) console.error('in-page navigation failed:', error);
      if (!isSuperseded() && navigator.onLine && !opts.noLocationFallback) {
        window.location.href = url;
      } else if (!navigator.onLine) {
        var status = document.getElementById('searchStatus');
        if (status) status.textContent = 'This content is not saved for offline use.';
      }
      finish(false);
    }
    function applyFresh(doc, kind) {
      if (!doc || isSuperseded()) { finish(false); return false; }
      try {
        applyPage(doc, url, Object.assign({}, opts, kind ? {kind: kind} : {}));
        finish(true);
        return true;
      } catch (error) {
        fail(error);
        return false;
      }
    }
    function fromServer() {
      return fetch(url, { credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch' } })
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.text();
      })
      .then(function (html) {
        applyFresh(new window.DOMParser().parseFromString(html, 'text/html'));
      });
    }
    if (opts.forceServer) {
      fromServer().catch(fail);
      return completion;
    }
    var renderer = window.GKPSOfflineRender;
    if (renderer && renderer.route(url)) {
      function refreshFullPage() {
        var queryBeforeRequest = searchQuery && searchQuery.value;
        return fetch(url, {cache: 'no-store', credentials: 'same-origin',
          headers: {'X-Requested-With': 'fetch'}}).then(function (response) {
          if (!response.ok) throw new Error('HTTP ' + response.status);
          return response.text();
        }).then(function (html) {
          if (generation !== navigationGeneration || pendingNavigation || navBusy
              || opts.kind === 'results' && searchQuery
              && searchQuery.value !== queryBeforeRequest) return;
          var doc = new window.DOMParser().parseFromString(html, 'text/html');
          applyPage(doc, url, Object.assign({}, opts, {
            skipHistory: true, backgroundRefresh: true
          }));
        });
      }
      var ready = window.GKPSOffline && window.GKPSOffline.status
        ? window.GKPSOffline.status().then(function (state) { return state.ready; })
        : Promise.resolve(false);
      ready.then(function (isReady) {
        if (!isReady) return fromServer();
        if (navigator.onLine && (opts.kind === 'results' || opts.kind === 'search')
            && !opts.historyTraversal) {
          return fromServer().catch(function () {
            return renderer.render(url).then(function (doc) {
              if (!doc) throw new Error('No saved search page');
              applyFresh(doc);
            });
          }).catch(fail);
        }
        renderer.render(url).then(function (doc) {
          if (!doc) return fromServer();
          if (!applyFresh(doc)) return;
          if (navigator.onLine && window.GKPSOffline && generation === navigationGeneration
              && !(opts.historyTraversal && opts.restoreSearchId)) {
            renderer.chunkFor(url).then(function (chunkUrl) {
              if (!chunkUrl) return refreshFullPage();
              return fetch(chunkUrl, {cache: 'no-store', credentials: 'same-origin'})
                .then(function (response) {
                  if (!response.ok) throw new Error('HTTP ' + response.status);
                  return response.json();
                }).then(function (payload) {
                  if (payload.schema !== 1 || !payload.data) return;
                  if (generation !== navigationGeneration || pendingNavigation
                      || new URL(url, location.href).pathname !== location.pathname) return;
                  return renderer.render(url, payload.data).then(function (updated) {
                    if (!updated || navBusy || generation !== navigationGeneration
                        || pendingNavigation) return;
                    updated.querySelector('#offlineSavedSource').hidden = true;
                    applyPage(updated, url, {kind: 'refresh', skipHistory: true});
                    window.GKPSOffline.sync().catch(function () {});
                    return refreshFullPage();
                  });
                });
            }).catch(function () { /* the saved copy stays visible */ });
          }
        }).catch(function () { return fromServer(); }).catch(fail);
      }).catch(function () { return fromServer(); }).catch(fail);
    } else fromServer().catch(fail);
    return completion;
  }

  function txt(doc, sel) {
    var el = doc.querySelector(sel);
    return el ? el.textContent : '';
  }

  function restoreRequestedFocus(opts) {
    if (!opts.focusKind) return;
    var focusTarget = null;
    var scroller = panelBody;
    if (opts.focusKind === 'songbook' || opts.focusKind === 'song'
        || opts.focusKind === 'tatib') {
      var editor = '[data-editor-open="' + opts.focusKind + '"][data-editor-id="' + opts.what + '"]';
      var opener = chList.querySelector(editor) || panelBody.querySelector(editor);
      var row = opener && opener.closest('li');
      focusTarget = row && row.querySelector('a.book, a.songrow');
      if (focusTarget && chList.contains(focusTarget)) scroller = chBody;
    } else if (opts.focusKind === 'entry') {
      focusTarget = readBody.querySelector('[data-entry-pk="' + opts.what + '"]');
    } else if (opts.focusKind === 'old-item') {
      focusTarget = readBody.querySelector('[data-old-item-pk="' + opts.what + '"]');
    } else if (opts.focusKind === 'read') {
      focusTarget = document.getElementById('read');
    }
    if (!focusTarget) return;
    if (focusTarget.classList.contains('book') || focusTarget.classList.contains('songrow')) {
      revealRow(focusTarget, scroller);
      focusTarget.classList.add('row-flash');
    }
    if (focusTarget.tabIndex < 0 && !focusTarget.hasAttribute('tabindex')) {
      focusTarget.setAttribute('tabindex', '-1');
    }
    if (opts.entryKeyboardFocus
        && (opts.focusKind === 'entry' || opts.focusKind === 'old-item')) {
      focusTarget = focusTarget.querySelector('.entry__ctrl:not([disabled])') || focusTarget;
      focusTarget.classList.remove('focus-restore-quiet');
      focusTarget.focus({ preventScroll: true });
    } else if (window.gkpsFocus) window.gkpsFocus.restoreQuietly(focusTarget);
    else focusTarget.focus({ preventScroll: true });
  }

  function applyPage(doc, url, opts) {
    opts = opts || {};
    var fresh = doc.documentElement.dataset;
    var freshMediaLibrary = doc.getElementById('railMediaLibrary');
    if (railMediaLibrary && freshMediaLibrary) {
      if (freshMediaLibrary.getAttribute('aria-current') === 'page') {
        railMediaLibrary.setAttribute('aria-current', 'page');
      } else {
        railMediaLibrary.removeAttribute('aria-current');
      }
    }
    var kind = opts.kind || 'lists';
    /* A direct offline boot can finish after the operator has already opened a
       sidebar. Keep those live shell controls while replacing the page content. */
    var bootNavState = root.dataset.nav;
    var bootChState = root.dataset.ch;
    var bootPanelFilter = opts.directBoot ? filter.value : null;
    var bootSongFilter = opts.directBoot ? songFilterEl.value : null;
    var bootPanelScroll = opts.directBoot ? panelBody.scrollTop : null;
    var bootChScroll = opts.directBoot ? chBody.scrollTop : null;
    var bootSearchValue = opts.directBoot && searchQuery ? searchQuery.value : null;
    var bootFocusId = opts.directBoot && document.activeElement
      ? document.activeElement.id : '';
    var changingMainMenu = (kind === 'rail' && opts.section !== activeSection)
      || (!opts.directBoot && kind === 'results'
          && (root.dataset.read === 'on' || root.dataset.nav !== 'closed'));
    var previousChState = root.dataset.ch;
    var previousChScroll = chBody.scrollTop;
    var currentPanelScroll = panelBody.scrollTop;
    var currentChScroll = chBody.scrollTop;
    var swapsStage = kind === 'chapter' || kind === 'song' || kind === 'service'
      || kind === 'result' || kind === 'more' || kind === 'search' || kind === 'results'
      || kind === 'refresh';
    /* A page opened from a second-level list -- and the in-place refresh that follows a save --
       updates the reading stage while keeping the operator's first-panel open/mini choice.
       Every server reading page is rendered with nav="open", so copying that value over a
       live collapsed state is what sprang the panel open (spec 080). */
    var stageOnly = kind === 'chapter' || kind === 'song' || kind === 'service'
      || kind === 'refresh';

    /* A background refresh only replaces the saved screen content. Rebuilding
       the sidebars here detaches their rows while people are using them and can
       discard keyboard focus, filters, and scroll position. */
    if (kind === 'refresh') {
      root.dataset.read = fresh.read;
      root.dataset.home = fresh.home;
      var freshRead = doc.querySelector('#read');
      if (freshRead && freshRead.dataset.kind === 'tatib') {
        var freshChList = doc.querySelector('#chList');
        if (freshChList) {
          reconcileChildren(chList, freshChList);
          bindChRows();
        }
      }
      reconcileChildren(stage, doc.querySelector('.stage'));
      refreshStageRefs();
      restoreSelectedEdition();
      syncBibleSidebar();
      bindLangLinks();
      bindStageExtras();
      bindPanelTips();
      applyFilter(filter.value);
      applySongFilter(songFilterEl.value);
      panelBody.scrollTop = changingMainMenu ? 0 : currentPanelScroll;
      chBody.scrollTop = changingMainMenu ? 0 : currentChScroll;
      if (!opts.deferFocus) restoreRequestedFocus(opts);
      document.title = doc.title;
      syncVisibleBibleTitle();
      document.dispatchEvent(new CustomEvent('shell:page', {detail: {url: url, kind: kind}}));
      return true;
    }

    /* shared first column: books / songbooks / services */
    setTextIfChanged(panelTitleEl, txt(doc, '#panelTitle'));
    setTextIfChanged(panelFilterLabel, txt(doc, 'label[for="bookFilter"]'));
    var freshFilter = doc.querySelector('#bookFilter');
    if (freshFilter) filter.placeholder = freshFilter.getAttribute('placeholder') || '';
    reconcileChildren(panelBody, doc.querySelector('#panelBody'));
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
      if (oldMode) reconcileNode(oldMode, newMode);
      else panel.querySelector('.panel__filter').appendChild(document.importNode(newMode, true));
    } else if (oldMode) {
      oldMode.parentNode.removeChild(oldMode);
    }

    /* shared second column: chapters / song list / service contents */
    setTextIfChanged(chTitleEl, txt(doc, '#chTitle'));
    setTextIfChanged(chFilterLabel, txt(doc, 'label[for="songFilter"]'));
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
    reconcileChildren(chList, doc.querySelector('#chList'));

    /* state */
    activeSection = fresh.section || activeSection;
    root.dataset.section = activeSection;
    if (fresh.chMode) root.dataset.chMode = fresh.chMode;

    if (changingMainMenu) {
      /* Clear only after the destination loaded and its lists were swapped in.
         The input events reapply each filter and hide its clear control. */
      [filter, songFilterEl].forEach(function (input) {
        input.value = '';
        input.dispatchEvent(new window.Event('input', { bubbles: true }));
      });
    }

    if (swapsStage) {
      root.dataset.read = fresh.read;
      root.dataset.home = fresh.home;
      if (!stageOnly) {
        root.dataset.nav = opts.directBoot ? bootNavState : fresh.nav;
      }
      /* The second-level pane still follows the arriving page: a service opened from the
         first-level panel has to bring its contents with it, and for a chapter or song
         opened from the list the arriving value already matches the live one (spec 088). */
      root.dataset.ch = opts.directBoot ? bootChState : fresh.ch;
      releaseTatibFlash();
      reconcileChildren(stage, doc.querySelector('.stage'));
      refreshStageRefs();
      if (kind === 'results' && fresh.home !== 'results' && searchQuery) {
        var freshSearch = doc.querySelector('#searchQuery');
        searchQuery.value = freshSearch ? freshSearch.value : '';
      }
      restoreSelectedEdition();
      bindLangLinks();
      bindSearchForm();
      bindFieldClears();
      bindStageExtras();
    } else if (kind === 'rail') {
      /* section switch: the lists move to the target section; the stage keeps
         whatever it shows (mockup: setSection + openPanel) */
      if (root.dataset.ch === 'open') closeChapters();
      reconcileChildren(chList, document.createDocumentFragment());
      root.dataset.ch = 'closed';
      root.dataset.nav = fresh.nav || 'open';
    } else if (kind === 'mode') {
      /* Only the first list changes modes. Keep the entry pane as it was,
         including a deliberately closed pane, its filter, and its scroll. */
      root.dataset.nav = fresh.nav || root.dataset.nav;
      root.dataset.ch = previousChState;
      applySongFilter(songFilterEl.value);
      chBody.scrollTop = previousChScroll;
      applyFilter(filter.value);
      var currentService = panelBody.querySelector('.book[aria-current="true"]');
      if (currentService && currentService.closest('.is-hidden')) {
        filter.value = '';
        filter.dispatchEvent(new window.Event('input', { bubbles: true }));
      }
    } else if (kind === 'sync') {
      root.dataset.nav = fresh.nav || 'open';
      root.dataset.ch = fresh.ch || root.dataset.ch;
    } else if (kind === 'bible-book') {
      /* Changing books replaces the chapter list, not the operator's mini/open panel choice. */
      root.dataset.ch = fresh.ch || root.dataset.ch;
    } else {
      root.dataset.nav = fresh.nav || root.dataset.nav;
      root.dataset.ch = fresh.ch || root.dataset.ch;
    }
    if (opts.backgroundRefresh) {
      root.dataset.nav = bootNavState;
      root.dataset.ch = bootChState;
    }

    /* Sidebar add controls sit outside the scrollable row containers. Reconcile
       them in their fixed toolbars, inserting only when the destination adds one
       and removing only when its section has none. */
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
        reconcileNode(live, fresh);
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
    var freshPanelAdd = doc.querySelector('#panelAdd');
    if (oldPanelAdd && !freshPanelAdd) oldPanelAdd.remove();
    else if (freshPanelAdd && panelFilter && panelFilter.parentNode) {
      var panelAdd = oldPanelAdd
        ? reconcileNode(oldPanelAdd, freshPanelAdd)
        : document.importNode(freshPanelAdd, true);
      var panelAddBefore = panelFilter.nextSibling;
      if (panelAdd !== panelAddBefore) panelFilter.parentNode.insertBefore(panelAdd, panelAddBefore);
    }
    var chTop = document.querySelector('.ch__top');
    var oldChAdd = document.querySelector('.ch__add');
    var freshChAdd = doc.querySelector('.ch__add');
    if (oldChAdd && !freshChAdd) oldChAdd.remove();
    else if (freshChAdd && chTop && chTop.parentNode) {
      var chAdd = oldChAdd ? reconcileNode(oldChAdd, freshChAdd)
        : document.importNode(freshChAdd, true);
      var chAddBefore = chTop.nextSibling;
      if (chAdd !== chAddBefore) chTop.parentNode.insertBefore(chAdd, chAddBefore);
    }
    /* the Tata Ibadah reorder strip: created and dropped with the section that owns it,
       right below the filter where the sidebar does not scroll */
    var oldChOrder = document.querySelector('.ch__reorder');
    var freshChOrder = doc.querySelector('.ch__reorder');
    if (oldChOrder && !freshChOrder) oldChOrder.remove();
    else if (freshChOrder && chTop && chTop.parentNode) {
      var chOrder = oldChOrder ? reconcileNode(oldChOrder, freshChOrder)
        : document.importNode(freshChOrder, true);
      var chOrderBefore = chTop.nextSibling;
      if (chOrder !== chOrderBefore) chTop.parentNode.insertBefore(chOrder, chOrderBefore);
    }

    syncBibleSidebar();
    bindPanelTiles();
    bindPanelTips();
    bindChRows();
    if (opts.directBoot) {
      filter.value = bootPanelFilter;
      songFilterEl.value = bootSongFilter;
      filter.dispatchEvent(new window.Event('input', {bubbles: true}));
      songFilterEl.dispatchEvent(new window.Event('input', {bubbles: true}));
      panelBody.scrollTop = bootPanelScroll;
      chBody.scrollTop = bootChScroll;
      if (bootFocusId) {
        var bootFocusTarget = document.getElementById(bootFocusId);
        if (bootFocusTarget) bootFocusTarget.focus({preventScroll: true});
      }
    }

    if (!changingMainMenu) {
      applyFilter(filter.value);
      applySongFilter(songFilterEl.value);
    }
    panelBody.scrollTop = currentPanelScroll;
    chBody.scrollTop = currentChScroll;

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

    if (fresh.home === 'results') railSearch.setAttribute('href', url);
    document.title = doc.title;
    syncVisibleBibleTitle();
    if (opts.replaceUrl) {
      history.replaceState({gkps: true, url: url, kind: kind}, '', url);
    } else if (!opts.skipHistory) {
      var pushes = ['chapter', 'song', 'service', 'result', 'search', 'results'];
      if (pushes.indexOf(kind) !== -1) {
        history.pushState({gkps: true, url: url, kind: kind,
          searchId: fresh.home === 'results' ? searchId() : null}, '', url);
      } else if (kind === 'more') {
        history.replaceState({gkps: true, url: url, kind: 'search',
          searchId: history.state && history.state.searchId || searchId()}, '', url);
      }
    }
    if (fresh.home === 'results' && (kind === 'search' || kind === 'results')
        && !opts.skipHistory) {
      try { sessionStorage.setItem(SEARCH_LAST, history.state.searchId); } catch (error) {}
    }
    if (fresh.home === 'results' && opts.directBoot) {
      if (!history.state || !history.state.searchId) {
        history.replaceState({gkps: true, url: url, kind: 'search',
          searchId: searchId()}, '', url);
      }
      try { sessionStorage.setItem(SEARCH_LAST, history.state.searchId); } catch (error) {}
    }

    /* Anything the arriving page carries and another script owns -- the project
       button, for one -- needs its hook run again: the swap replaced the node the
       earlier binding sat on, which is how a control can be present on a deep link
       and dead on the path a person actually clicks through. */
    document.dispatchEvent(new CustomEvent('shell:page', {detail: {url: url, kind: kind}}));
    scheduleIdleCollapse();

    /* per-kind endings */
    if (kind === 'rail') {
      restoreCurrentPath(opts.section);
    }
    if (kind === 'mode') {
      var modeCurrent = panelBody.querySelector('.book[aria-current="true"]');
      if (modeCurrent) window.requestAnimationFrame(function () {
        if (document.contains(modeCurrent)) ensureVisible(modeCurrent, panelBody, 8);
      });
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
    if (kind === 'lists' && opts.focusKind) restoreRequestedFocus(opts);
    if (kind === 'search') {
      window.scrollTo({ top: 0, behavior: 'auto' });
    }
    if (fresh.home === 'results') {
      var restoreId = opts.restoreSearchId || opts.skipHistory
        && history.state && history.state.searchId;
      if (!opts.backgroundRefresh && !restoreSearchSnapshot(restoreId)) {
        window.scrollTo({top: kind === 'more' ? window.scrollY : 0, behavior: 'auto'});
      }
      if (opts.directBoot && bootSearchValue !== null && searchQuery) {
        searchQuery.value = bootSearchValue;
        searchQuery.dispatchEvent(new window.Event('input', {bubbles: true}));
      }
      saveSearchSnapshot();
    }
    return true;
  }

  /* results and "Show more" open in place too */
  function bindStageExtras() {
    if (!stage || stage.dataset.stageClicksBound) return;
    stage.dataset.stageClicksBound = 'true';
    stage.addEventListener('click', function (event) {
      var more = event.target.closest('.result-more');
      if (more && stage.contains(more)) {
        event.preventDefault();
        navigate(more.href, { kind: 'more' });
        return;
      }
      var row = event.target.closest('.result-row');
      if (row && stage.contains(row)) {
        event.preventDefault();
        navigate(row.href, { kind: 'result' });
      }
    });
    stage.addEventListener('submit', function (event) {
      var form = event.target.closest('#globalSearch');
      if (!form || !stage.contains(form)) return;
      var input = form.querySelector('#searchQuery') || searchQuery;
      var query = input ? input.value.trim() : '';
      if (!query) {
        event.preventDefault();
        navigate('/', {kind: 'results'});
        return;
      }
      input.value = query;
      event.preventDefault();
      var action = form.getAttribute('action') || '/search/';
      navigate(action + '?q=' + encodeURIComponent(query), { kind: 'search' });
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
    /* The stable stage owns submit handling, so a reconciled form cannot retain
       stale closures or accumulate one listener per navigation. */
    bindStageExtras();
  }
  bindSearchForm();
  /* The result snapshot belongs to this tab. A direct search URL replaces its
     latest search; the logo deliberately does not erase it. */
  if (root.dataset.home === 'results') {
    if (!history.state || !history.state.searchId) {
      history.replaceState({gkps: true, url: location.pathname + location.search,
        kind: 'search', searchId: searchId()}, '', location.href);
    }
    saveSearchSnapshot();
    try { sessionStorage.setItem(SEARCH_LAST, history.state.searchId); } catch (error) {}
  }
  function lastSearchSnapshot() {
    var id = null;
    try { id = sessionStorage.getItem(SEARCH_LAST); } catch (error) {}
    var snapshot = id && readSearchSnapshot(id);
    return snapshot && /^\/search\/?\?q=/.test(snapshot.url)
      ? {id: id, snapshot: snapshot} : null;
  }
  var initialLast = lastSearchSnapshot();
  railSearch.setAttribute('href', initialLast ? initialLast.snapshot.url : '/');

  function openSearch(event) {
    event.preventDefault();
    var last = lastSearchSnapshot();
    navigate(last ? last.snapshot.url : '/', {kind: 'results',
      restoreSearchId: last && last.id});
  }
  railSearch.addEventListener('click', openSearch);
  var railLogo = document.querySelector('.rail__logo');
  if (railLogo) railLogo.addEventListener('click', function (event) {
    event.preventDefault();
    navigate('/', {kind: 'results', replaceUrl: true});
  });

  function needsOfflineShellHydration() {
    var path = location.pathname;
    if (path === '/' || path === '/home/') return false;
    if (path === '/search' || path === '/search/') return root.dataset.home === 'landing';
    if (root.dataset.read === 'on') return false;
    if (/^\/bible(?:\/|$)/.test(path)) return root.dataset.nav === 'closed';
    if (/^\/songs(?:\/|$)/.test(path)) return root.dataset.section !== 'kidung';
    if (/^\/tatib(?:\/|$)/.test(path)) return root.dataset.section !== 'tatib';
    return false;
  }

  /* A sidebar editor saved something: re-render the page's regions in place, so
     every list, the panel selection and the reading stage agree again. */
  document.addEventListener('editor:saved', function (event) {
    /* In-page navigation does not change location. Refresh the section that
       supplied the visible sidebar; if the reader is in another section, keep
       its stage by swapping only the lists. */
    var stageMatchesSection = readKind() && stageSection() === activeSection;
    var currentSongbook = activeSection === 'kidung' && root.dataset.ch === 'open'
      ? panelBody.querySelector('.book[aria-current="true"]') : null;
    var url = stageMatchesSection ? stageInfo.url
      : currentSongbook ? currentSongbook.getAttribute('href')
        : panelOwner().getAttribute('href');
    var refreshOptions = {
      kind: stageMatchesSection ? 'refresh' : 'lists',
      what: event.detail && (event.detail.focusId || event.detail.id),
      focusKind: event.detail && (event.detail.focusKind || event.detail.kind),
      entryKeyboardFocus: !!(event.detail && event.detail.entryKeyboardFocus),
      deferFocus: !!(event.detail && event.detail.deferFocus)
    };
    /* Show the just-saved server state immediately. The full offline snapshot can
       refresh in parallel; waiting for it here delayed editor feedback and could
       leave the pane showing the previous generation. */
    var viewUpdate = navigate(url, Object.assign({}, refreshOptions, {
      forceServer: true,
      noLocationFallback: !!(event.detail && event.detail.noLocationFallback)
    }));
    if (event.detail) event.detail.viewUpdate = viewUpdate;
    if (navigator.onLine && window.GKPSOffline) {
      window.GKPSOffline.sync().catch(function () { /* the current page is already fresh */ });
    }
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
  applyTheme(root.dataset.themeMode || 'system', false);
  syncState();
  scheduleIdleCollapse();
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
  function historyKind(path) {
    if (/^\/bible\/\d+\/\d+\/$/.test(path)) return 'chapter';
    if (/^\/songs\/\d+\/$/.test(path)) return 'song';
    if (/^\/tatib\/\d+\/$/.test(path)) return 'service';
    if (path === '/search' || path === '/search/') return 'search';
    return 'results';
  }
  if (!history.state || !history.state.gkps) {
    history.replaceState({gkps: true, url: location.pathname + location.search,
      kind: historyKind(location.pathname)}, '', location.href);
  }
  window.addEventListener('popstate', function (event) {
    var state = event.state;
    var url = state && state.gkps ? state.url : location.pathname + location.search;
    navigate(url, {kind: state && state.kind || historyKind(location.pathname),
                   skipHistory: true, historyTraversal: true,
                   restoreSearchId: state && state.searchId});
  });
  if (root.dataset.home === 'landing' && needsOfflineShellHydration()
      && window.GKPSOfflineRender
      && window.GKPSOfflineRender.route(location.href)) {
    navigate(location.href, {kind: historyKind(location.pathname), skipHistory: true,
      directBoot: true});
  }
})();
