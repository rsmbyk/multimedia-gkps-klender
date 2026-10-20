/* The operator dock (spec 119): pick a Tata Ibadah, browse its entries, and run it.
 *
 * The dock is a WRITER of the browser-local display state (web/display.js): clicking an
 * entry or a screen projects exactly that screen, the display button toggles the
 * projection, and the blank button is the reversible pause. The projector and the
 * caption overlay are readers; nothing here talks to the server but the service data
 * (the projector page's data islands, one fetch per service).
 *
 * Keyboard (spec 119): the dock owns the transport keys. The panel is the only focus
 * target — every control is tabindex="-1", and a pointerdown hands focus back to the
 * panel — so a key never lands on a button and Space never re-presses the last click.
 *
 *     ArrowDown / ArrowRight / PageDown     next screen
 *     ArrowUp / ArrowLeft / PageUp          previous screen
 *     Home / End                            first / last screen
 *     Space                                 project / hide (this service)
 *     T                                     show the other edition (passages)
 *     Escape                                back to the picker
 */
(function () {
  'use strict';

  var panel = document.getElementById('dockPanel');
  var viewPick = document.getElementById('viewPick');
  var viewRun = document.getElementById('viewRun');
  var pickList = document.getElementById('dockServices');
  var entryList = document.getElementById('entryList');
  var runBody = document.getElementById('runBody');
  var runService = document.getElementById('runService');
  var runDate = document.getElementById('runDate');
  var runNote = document.getElementById('runNote');
  var displayBtn = document.getElementById('displayBtn');
  var displayLabel = displayBtn.querySelector('[data-project-label]');
  var blankBtn = document.getElementById('blankBtn');
  var prevBtn = document.getElementById('prevBtn');
  var nextBtn = document.getElementById('nextBtn');
  var transChip = document.getElementById('transChip');
  var baitChips = document.getElementById('baitChips');
  var switchBtn = document.getElementById('switchBtn');
  var reloadBtn = document.getElementById('reloadPickBtn');
  var themeBtn = document.getElementById('themeBtn');
  var root = document.documentElement;

  var SVG_NS = 'http://www.w3.org/2000/svg';
  var cache = {};                 /* service id -> {entries, screens} */
  var dock = {
    service: null, name: '', date: '',
    entries: [], screens: [],
    openEntry: null,
    on: false, screen: 0, translation: null,
  };

  function icon(path, cls) {
    var svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-width', '1.7');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('aria-hidden', 'true');
    if (cls) svg.setAttribute('class', cls);
    var p = document.createElementNS(SVG_NS, 'path');
    p.setAttribute('d', path);
    svg.appendChild(p);
    return svg;
  }

  /* ---------- the service's data (the projector page's islands) -------------- */

  function fetchService(id) {
    if (cache[id]) return Promise.resolve(cache[id]);
    return fetch('/projector?service=' + encodeURIComponent(id),
                 {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) { return response.ok ? response.text() : ''; })
      .then(function (html) {
        if (!html) return null;
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var entryIsland = doc.getElementById('projectorEntryData');
        var screenIsland = doc.getElementById('projectorScreenData');
        if (!entryIsland || !screenIsland) return null;
        var data = {entries: JSON.parse(entryIsland.textContent) || [],
                    screens: JSON.parse(screenIsland.textContent) || []};
        cache[id] = data;
        return data;
      })
      .catch(function () { return null; });
  }

  /* ---------- the runner's list --------------------------------------------- */

  function firstLine(screen) {
    var lines = (screen && screen.lines) || [];
    for (var i = 0; i < lines.length; i++) {
      var text = String(lines[i].text || '').trim();
      if (text) return text;
    }
    return '';
  }

  function entryLabel(entry) {
    var label = String(entry.label || '').trim();
    if (label) return label;
    if (entry.type === 'break') return 'Istirahat';
    if (entry.type === 'song') return 'Lagu';
    return 'Teks';
  }

  function isQuiet(entry) {
    return entry.type === 'break' || (!entry.label && entry.untitled);
  }

  function entryMeta(entry) {
    var baits = entry.baits || [];
    if (baits.length) return baits.length + ' bait';
    var count = 0;
    for (var i = entry.start; i <= entry.end; i++) {
      if (dock.screens[i] && !dock.screens[i].blank) count++;
    }
    return count ? count + ' layar' : '';
  }

  function screenLabel(screen, entry) {
    var line = firstLine(screen);
    var header = String(screen.header || '').trim();
    if (header && header !== entryLabel(entry)) {
      return line ? header + ' — ' + line : header;
    }
    return line || 'Kosong';
  }

  function renderList() {
    entryList.replaceChildren();
    dock.entries.forEach(function (entry, index) {
      var item = document.createElement('li');
      item.className = 'entry';
      item.dataset.entry = String(index);

      var row = document.createElement('button');
      row.type = 'button';
      row.className = 'entry__row';
      row.tabIndex = -1;
      row.dataset.entry = String(index);
      row.appendChild(icon('M9 6l6 6-6 6', 'entry__chev'));

      var label = document.createElement('span');
      label.className = 'entry__label' + (isQuiet(entry) ? ' entry__label--quiet' : '');
      label.textContent = entryLabel(entry);
      row.appendChild(label);

      var meta = document.createElement('span');
      meta.className = 'entry__meta';
      meta.textContent = entryMeta(entry);
      row.appendChild(meta);
      item.appendChild(row);

      var inner = document.createElement('div');
      inner.className = 'entry__inner';
      var ul = document.createElement('ul');
      var baits = entry.baits || [];
      if (baits.length) {
        /* A song's screens group under their bait, so a number names its place. */
        baits.forEach(function (bait) {
          var head = document.createElement('li');
          head.className = 'baithead';
          head.textContent = 'Bait ' + bait.number;
          ul.appendChild(head);
          for (var s = bait.start; s <= bait.end; s++) appendScreenRow(ul, entry, s);
        });
      } else {
        for (var i = entry.start; i <= entry.end; i++) appendScreenRow(ul, entry, i);
      }
      if (ul.children.length) {
        inner.appendChild(ul);
        item.appendChild(inner);
      }
      entryList.appendChild(item);
    });
    runNote.hidden = dock.entries.length > 0;
    if (!dock.entries.length) runNote.textContent = 'Tata Ibadah ini belum punya isi.';
    applyOpen();
    updateStuck();
  }

  function appendScreenRow(ul, entry, index) {
    var screen = dock.screens[index];
    if (!screen || screen.blank) return;
    var cell = document.createElement('li');
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'srow';
    button.tabIndex = -1;
    button.dataset.screen = String(index);
    var no = document.createElement('span');
    no.className = 'srow__no';
    no.textContent = String(index - entry.start + 1);
    var text = document.createElement('span');
    text.className = 'srow__text';
    text.textContent = screenLabel(screen, entry);
    button.appendChild(no);
    button.appendChild(text);
    cell.appendChild(button);
    ul.appendChild(cell);
  }

  function applyOpen() {
    entryList.querySelectorAll('.entry').forEach(function (el) {
      el.classList.toggle('is-open', Number(el.dataset.entry) === dock.openEntry);
    });
  }

  /* ---------- views and focus ----------------------------------------------- */

  function focusPanel() {
    try { panel.focus({preventScroll: true}); } catch (e) { panel.focus(); }
  }

  function setView(name) {
    panel.dataset.view = name;
    viewPick.hidden = name !== 'pick';
    viewRun.hidden = name !== 'run';
    focusPanel();
  }

  function openService(id, name, date) {
    dock.service = id;
    dock.name = name;
    dock.date = date;
    dock.entries = [];
    dock.screens = [];
    dock.openEntry = null;
    runService.textContent = name;
    runDate.textContent = date;
    entryList.replaceChildren();
    runNote.hidden = true;
    setView('run');
    var wanted = id;
    fetchService(id).then(function (data) {
      if (dock.service !== wanted) return;
      if (!data) {
        runNote.hidden = false;
        runNote.textContent = 'Data layanan tidak termuat.';
        return;
      }
      dock.entries = data.entries;
      dock.screens = data.screens;
      renderList();
      sync(gkpsDisplay.read());
    });
  }

  /* ---------- projection (the state's verbs) -------------------------------- */

  function projectScreen(index) {
    if (dock.service == null) return;
    var size = dock.screens.length;
    var target = Math.max(0, size ? Math.min(index, size - 1) : index);
    var state = gkpsDisplay.read();
    if (state.service === dock.service) gkpsDisplay.screen(target);
    else gkpsDisplay.show(dock.service, target);
  }

  function step(delta) {
    if (dock.service == null || !dock.screens.length) return;
    var state = gkpsDisplay.read();
    var base = state.service === dock.service ? state.screen : -1;
    if (delta < 0 && base <= 0) return;
    projectScreen(Math.max(0, base + delta));
  }

  /* ---------- the state ------------------------------------------------------ */

  var glideFrame = null;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* One glide per move (spec 119): 190 ms ease-out, clamped at the ends, never a
     bounce. Reduced motion jumps instead. */
  function glideScroll(target) {
    var max = runBody.scrollHeight - runBody.clientHeight;
    var to = Math.max(0, Math.min(target, max));
    var from = runBody.scrollTop;
    if (glideFrame) { window.cancelAnimationFrame(glideFrame); glideFrame = null; }
    if (Math.abs(to - from) < 1) return;
    if (reduceMotion.matches) { runBody.scrollTop = to; return; }
    var started = performance.now();
    var duration = 190;
    function frame(now) {
      var t = Math.min(1, (now - started) / duration);
      var eased = 1 - Math.pow(1 - t, 3);
      runBody.scrollTop = from + (to - from) * eased;
      glideFrame = t < 1 ? window.requestAnimationFrame(frame) : null;
    }
    glideFrame = window.requestAnimationFrame(frame);
  }

  function centerRow(el) {
    if (!el) return;
    var box = runBody.getBoundingClientRect();
    var rect = el.getBoundingClientRect();
    glideScroll(runBody.scrollTop + (rect.top - box.top) - (box.height - rect.height) / 2);
  }

  function centerLive() {
    var live = entryList.querySelector('.srow.is-live') ||
               entryList.querySelector('.entry.is-live > .entry__row');
    if (!live) return;
    /* The entry's expansion animates 200 ms; the glide follows it, so a boundary
       crossing reads as one motion rather than two. */
    centerRow(live);
    window.setTimeout(function () { centerRow(live); }, 210);
  }

  function entryOfScreen(index) {
    for (var i = 0; i < dock.entries.length; i++) {
      var entry = dock.entries[i];
      if (index >= entry.start && index <= entry.end) return i;
    }
    return -1;
  }

  /* The pinned row, the dissolve under it, and the NEXT band (spec 119). */
  function updateStuck() {
    var row = entryList.querySelector('.entry.is-live > .entry__row');
    var stuck = false;
    if (row) {
      var box = runBody.getBoundingClientRect();
      /* A sticky row pins at the list's padding edge, so that edge is the line to
         measure against — not the scrollport's own top. */
      var edge = parseFloat(getComputedStyle(runBody).paddingTop) || 0;
      stuck = row.getBoundingClientRect().top - box.top <= edge + 1;
      row.classList.toggle('is-stuck', stuck);
    }
    runBody.dataset.stuck = stuck ? 'true' : 'false';
    var nextBand = document.getElementById('nextBand');
    var nextBandLabel = document.getElementById('nextBandLabel');
    var activeEntry = dock.on ? entryOfScreen(dock.screen) : -1;
    var next = activeEntry >= 0 ? dock.entries[activeEntry + 1] : null;
    if (stuck && next) {
      nextBandLabel.textContent = entryLabel(next);
      nextBand.hidden = false;
    } else {
      nextBand.hidden = true;
    }
    runBody.dataset.band = nextBand.hidden ? 'false' : 'true';
  }

  var scrollScheduled = false;
  runBody.addEventListener('scroll', function () {
    if (scrollScheduled) return;
    scrollScheduled = true;
    window.requestAnimationFrame(function () {
      scrollScheduled = false;
      updateStuck();
    });
  }, {passive: true});

  function translationOptions(screen) {
    var translations = (screen && screen.translations) || {};
    return Object.keys(translations).filter(function (key) {
      return translations[key] && translations[key].line;
    });
  }

  function updateChip(live, activeEntry) {
    var screen = dock.screens[dock.screen] || null;
    var options = translationOptions(screen);
    if (!live || !options.length) {
      transChip.hidden = true;
      delete transChip.dataset.custom;
      return;
    }
    var entry = dock.entries[activeEntry] || {};
    var own = entry.translation || options[0];
    var shown = dock.translation || own;
    transChip.hidden = false;
    transChip.textContent = shown;
    transChip.dataset.editions = options.join(',');
    /* Filled only while the shown edition is not the entry's own (spec 119). */
    if (shown !== own) transChip.dataset.custom = 'true';
    else delete transChip.dataset.custom;
  }

  function renderChips(live, activeEntry) {
    baitChips.replaceChildren();
    delete baitChips.dataset.overflow;
    if (!live || activeEntry < 0) return;
    var entry = dock.entries[activeEntry];
    var baits = (entry && entry.baits) || [];
    var liveChip = null;
    baits.forEach(function (bait) {
      var chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'chip';
      chip.tabIndex = -1;
      chip.dataset.screen = String(bait.start);
      chip.textContent = String(bait.number);
      var isLive = dock.screen >= bait.start && dock.screen <= bait.end;
      chip.classList.toggle('is-live', isLive);
      if (isLive) liveChip = chip;
      baitChips.appendChild(chip);
    });
    if (!baits.length) return;
    /* The chip strip glides its current chip to the centre; fades only while it
       overflows (spec 119). */
    baitChips.dataset.overflow = baitChips.scrollWidth > baitChips.clientWidth + 1 ? 'true' : 'false';
    if (liveChip) {
      var target = liveChip.offsetLeft - (baitChips.clientWidth - liveChip.offsetWidth) / 2;
      try {
        baitChips.scrollTo({left: target, behavior: reduceMotion.matches ? 'auto' : 'smooth'});
      } catch (e) {
        baitChips.scrollLeft = target;
      }
    }
  }

  function sync(state) {
    if (!state) state = gkpsDisplay.read();
    var live = state.service != null && state.service === dock.service;
    dock.on = live && state.on === true;
    dock.screen = live ? state.screen : 0;
    dock.translation = live ? state.translation : null;

    displayBtn.dataset.on = dock.on ? 'true' : 'false';
    displayBtn.setAttribute('aria-pressed', dock.on ? 'true' : 'false');
    displayLabel.textContent = dock.on ? 'Projecting' : 'Project';
    displayBtn.title = dock.on ? 'Hide the words (space)' : 'Project this service (space)';
    displayBtn.setAttribute('aria-label', displayBtn.title);

    blankBtn.dataset.on = live && state.on !== true ? 'true' : 'false';
    blankBtn.setAttribute('aria-pressed', blankBtn.dataset.on);
    blankBtn.disabled = !live;
    blankBtn.title = blankBtn.dataset.on === 'true'
      ? 'Resume the words (space)' : 'Blank the screen (space)';
    blankBtn.setAttribute('aria-label', blankBtn.title);

    var activeEntry = live ? entryOfScreen(state.screen) : -1;
    if (live && activeEntry !== -1) dock.openEntry = activeEntry;

    entryList.querySelectorAll('.entry').forEach(function (el) {
      var index = Number(el.dataset.entry);
      el.classList.toggle('is-live', index === activeEntry);
      el.classList.toggle('is-open', index === dock.openEntry);
    });
    entryList.querySelectorAll('.srow').forEach(function (el) {
      el.classList.toggle('is-live', live && Number(el.dataset.screen) === state.screen);
    });

    updateChip(live, activeEntry);
    renderChips(live, activeEntry);
    if (live) centerLive();
    updateStuck();
  }

  /* ---------- the controls --------------------------------------------------- */

  pickList.addEventListener('click', function (event) {
    var row = event.target.closest('.servicerow');
    if (!row) return;
    openService(Number(row.dataset.service), row.dataset.name, row.dataset.date);
  });

  entryList.addEventListener('click', function (event) {
    var chevron = event.target.closest('.entry__chev');
    var screenRow = event.target.closest('.srow');
    var entryRow = event.target.closest('.entry__row');
    if (screenRow) {
      projectScreen(Number(screenRow.dataset.screen));
      centerRow(screenRow);
      focusPanel();
      return;
    }
    if (!entryRow) return;
    var index = Number(entryRow.dataset.entry);
    var entry = dock.entries[index];
    if (!entry) return;
    if (chevron) {
      dock.openEntry = dock.openEntry === index ? null : index;
      applyOpen();
      focusPanel();
      return;
    }
    dock.openEntry = index;
    applyOpen();
    projectScreen(entry.start);
    centerRow(entryRow);
    focusPanel();
  });

  baitChips.addEventListener('click', function (event) {
    var chip = event.target.closest('.chip');
    if (!chip) return;
    projectScreen(Number(chip.dataset.screen));
    focusPanel();
  });

  displayBtn.addEventListener('click', function () {
    if (dock.service == null) return;
    var state = gkpsDisplay.read();
    if (state.service === dock.service) {
      if (state.on) gkpsDisplay.hide();
      else gkpsDisplay.screen(state.screen);        /* resume where it was paused */
    } else {
      gkpsDisplay.show(dock.service, 0);            /* project from the start */
    }
    focusPanel();
  });

  blankBtn.addEventListener('click', function () {
    if (dock.service == null) return;
    var state = gkpsDisplay.read();
    if (state.service !== dock.service) return;
    if (state.on) gkpsDisplay.hide();
    else gkpsDisplay.screen(state.screen);
    focusPanel();
  });

  transChip.addEventListener('click', function () {
    var editions = (transChip.dataset.editions || '').split(',').filter(Boolean);
    if (!editions.length) return;
    var index = editions.indexOf(transChip.textContent);
    gkpsDisplay.flip(editions[(index + 1) % editions.length] || null);
    focusPanel();
  });

  prevBtn.addEventListener('click', function () { step(-1); focusPanel(); });
  nextBtn.addEventListener('click', function () { step(1); focusPanel(); });
  switchBtn.addEventListener('click', function () { setView('pick'); });
  reloadBtn.addEventListener('click', function () { window.location.reload(); });

  /* ---------- keyboard (the dock owns it) ------------------------------------ */

  /* The unit grammar (spec 119): a plain key moves a screen, Shift moves a bait,
     Ctrl/⌘ moves an entry; Home and End take the same modifier. Ctrl/⌘+PgUp/PgDn
     stay the browser's own tab keys. */
  function unitAt() {
    var state = gkpsDisplay.read();
    var live = state.service === dock.service;
    var index = live ? state.screen : 0;
    var entryIndex = entryOfScreen(index);
    return {index: index, entryIndex: entryIndex,
            entry: entryIndex >= 0 ? dock.entries[entryIndex] : null};
  }

  function stepUnit(delta, unit) {
    var at = unitAt();
    if (unit === 'entry') {
      if (!dock.entries.length) return;
      var index = Math.max(0, Math.min(dock.entries.length - 1,
                                       (at.entryIndex < 0 ? 0 : at.entryIndex) + delta));
      projectScreen(dock.entries[index].start);
      return;
    }
    if (unit === 'bait' && at.entry && (at.entry.baits || []).length) {
      var baits = at.entry.baits;
      var bait = 0;
      for (var i = 0; i < baits.length; i++) {
        if (at.index >= baits[i].start) bait = i;
      }
      bait = Math.max(0, Math.min(baits.length - 1, bait + delta));
      projectScreen(baits[bait].start);
      return;
    }
    step(delta);
  }

  function edgeOf(unit, end) {
    var at = unitAt();
    if (unit === 'entry') {
      if (!dock.entries.length) return;
      projectScreen(end ? dock.entries[dock.entries.length - 1].start : 0);
      return;
    }
    if (unit === 'bait' && at.entry && (at.entry.baits || []).length) {
      var baits = at.entry.baits;
      projectScreen(end ? baits[baits.length - 1].start : baits[0].start);
      return;
    }
    if (!dock.screens.length) return;
    projectScreen(end ? dock.screens.length - 1 : 0);
  }

  panel.addEventListener('keydown', function (event) {
    if (event.altKey) return;
    var key = event.key;
    var shift = event.shiftKey;
    var ctrl = event.ctrlKey || event.metaKey;
    if (key === 'Escape') {
      if (panel.dataset.view === 'run') setView('pick');
      return;
    }
    if (panel.dataset.view !== 'run') return;
    if (ctrl && (key === 'PageUp' || key === 'PageDown')) return;   /* the browser's tabs */
    var unit = shift ? 'bait' : ctrl ? 'entry' : 'screen';
    if (key === 'ArrowDown' || key === 'ArrowRight' || key === 'PageDown' ||
        key === 'ArrowUp' || key === 'ArrowLeft' || key === 'PageUp') {
      event.preventDefault();
      stepUnit(key === 'ArrowUp' || key === 'ArrowLeft' || key === 'PageUp' ? -1 : 1, unit);
      return;
    }
    if (key === 'Home') { event.preventDefault(); edgeOf(unit, false); return; }
    if (key === 'End') { event.preventDefault(); edgeOf(unit, true); return; }
    if (ctrl) return;                                               /* leave other combos alone */
    if (key === ' ') { event.preventDefault(); displayBtn.click(); return; }
    if (key === 't' || key === 'T') { transChip.click(); }
  });

  /* A click must leave the focus where the keyboard lives, not on the clicked
     button: otherwise Space would re-press the last thing clicked. */
  panel.addEventListener('pointerdown', focusPanel);

  /* ---------- appearance (shared key and glyphs with the public site) -------- */

  var systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  var morphTimer = null;

  function applyTheme(mode, persist) {
    root.dataset.themeMode = mode;
    root.dataset.theme = mode === 'system'
      ? (systemTheme.matches ? 'dark' : 'light') : mode;
    var label = 'Appearance: ' + mode.charAt(0).toUpperCase() + mode.slice(1);
    themeBtn.setAttribute('aria-label', label);
    themeBtn.title = label;
    if (persist) {
      try { localStorage.setItem('gkps-theme', mode); } catch (e) { /* private mode */ }
      /* A user switch morphs (colour sweep + icon pop); loading never does. */
      root.classList.add('theme-morph');
      window.clearTimeout(morphTimer);
      morphTimer = window.setTimeout(function () { root.classList.remove('theme-morph'); }, 420);
    }
  }

  themeBtn.addEventListener('click', function () {
    var mode = root.dataset.themeMode;
    applyTheme(mode === 'system' ? 'dark' : mode === 'dark' ? 'light' : 'system', true);
    focusPanel();
  });

  systemTheme.addEventListener('change', function () {
    if (root.dataset.themeMode === 'system') applyTheme('system', false);
  });

  /* ---------- boot ----------------------------------------------------------- */

  applyTheme(root.dataset.themeMode || 'dark', false);
  gkpsDisplay.subscribe(sync);
  setView('pick');
})();
