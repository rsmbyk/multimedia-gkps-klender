/* The operator dock (spec 119): pick a Tata Ibadah, browse its entries, and run it.
 *
 * Built to the approved mockup (v70): the picker is a month-grouped list of service
 * rows (name, "On screen" pill, short date); the runner is a numbered list of entries
 * (songs: reference + title with a "Bait …" line; untitled text in quiet italics; a
 * section break as a hairline), one inner row per projector screen, the current entry
 * pinned with the next one named under it, and a transport row at the foot.
 *
 * The dock is a WRITER of the browser-local display state (web/display.js). Its one
 * display control is the slashed-eye button in the runner head: "Display this service"
 * when the browsed service is not on screen, "Hide words" while it is. The projector
 * and the caption overlay are readers.
 *
 * Keyboard (the dock owns it; every control is tabindex="-1" and the panel takes the
 * focus back on pointerdown):
 *
 *     ArrowDown / ArrowRight / PageDown     next screen
 *     ArrowUp / ArrowLeft / PageUp          previous screen
 *     Shift + the same                      next / previous bait
 *     Ctrl/⌘ + the same                     next / previous entry
 *     Home / End                            first / last of the same unit
 *     Space                                 display / hide this service
 *     T                                     show the other edition (passages)
 *     Escape                                back to the picker
 */
(function () {
  'use strict';

  var panel = document.getElementById('dockPanel');
  var viewPick = document.getElementById('viewPick');
  var viewRun = document.getElementById('viewRun');
  var pickBody = document.getElementById('pickBody');
  var entryList = document.getElementById('entryList');
  var runBody = document.getElementById('runBody');
  var runService = document.getElementById('runService');
  var runDate = document.getElementById('runDate');
  var runNote = document.getElementById('runNote');
  var blankBtn = document.getElementById('blankBtn');
  var prevBtn = document.getElementById('prevBtn');
  var nextBtn = document.getElementById('nextBtn');
  var transChip = document.getElementById('transChip');
  var baitStrip = document.getElementById('baitStrip');
  var baitChips = document.getElementById('baitChips');
  var switchBtn = document.getElementById('switchBtn');
  var reloadBtn = document.getElementById('reloadPickBtn');
  var themeBtn = document.getElementById('themeBtn');
  var root = document.documentElement;

  var cache = {};                 /* service id -> {entries, screens} */
  var dock = {
    service: null, name: '', date: '',
    entries: [], screens: [],
    on: false, screen: 0, translation: null,
    lastEntry: null,
    centerUnit: 'screen',         /* what the last move stepped: 'entry' or 'screen' */
  };

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
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

  /* ---------- reading the entry's own words ---------------------------------- */

  function entryLabel(entry) {
    var label = String(entry.label || '').trim();
    if (label) return label;
    if (entry.type === 'break') return 'Section break';
    if (entry.type === 'song') return 'Song';
    return 'Text';
  }

  function songParts(entry) {
    var label = String(entry.label || '').trim();
    /* "NKB 43 — Title", "NKB 43: Title", "NKB 43 Title" → reference + title. */
    var match = label.match(/^([A-Za-z]{2,6}\s*\d+[A-Za-z]?)\s*(?:[:—–-]\s*|\s+)(.+)$/);
    if (match) {
      return {reference: match[1].trim(), title: match[2].trim()};
    }
    return {reference: '', title: label};
  }

  function screenLines(screen) {
    var out = [];
    ((screen && screen.lines) || []).forEach(function (line) {
      var text = String(line.text || '').trim();
      if (text) out.push(text);
    });
    return out;
  }

  function quietLines(entry) {
    /* An untitled text entry is shown by its own first words (mockup: italic rows). */
    for (var i = entry.start; i <= entry.end; i++) {
      var screen = dock.screens[i];
      if (!screen || screen.blank) continue;
      var lines = screenLines(screen);
      if (lines.length) return lines.slice(0, 2);
    }
    return [];
  }

  /* ---------- the runner's list --------------------------------------------- */

  function entryRowContent(entry, index) {
    var row = el('button', 'entryrow');
    row.type = 'button';
    row.tabIndex = -1;
    row.dataset.index = String(index);
    row.setAttribute('aria-current', 'false');

    if (entry.type === 'break') {
      row.setAttribute('aria-label', 'Section break');
      var brk = el('span', 'entryrow__break');
      brk.appendChild(el('span'));
      row.appendChild(brk);
      return row;
    }

    row.appendChild(el('span', 'entryrow__c', String(index + 1)));

    if (entry.type === 'song') {
      var parts = songParts(entry);
      var t = el('span', 'entryrow__t entryrow__t--song');
      var head = el('span', 'entryrow__heading');
      if (parts.reference) head.appendChild(el('span', 'entryrow__reference', parts.reference));
      head.appendChild(el('span', 'entryrow__title', parts.title || 'Song'));
      t.appendChild(head);
      var baits = entry.baits || [];
      if (baits.length) {
        t.appendChild(el('span', 'entryrow__verses',
          'Bait ' + baits.map(function (bait) { return bait.number; }).join(', ')));
      }
      row.appendChild(t);
      return row;
    }

    var label = String(entry.label || '').trim();
    if (label) {
      row.appendChild(el('span', 'entryrow__t', label));
      return row;
    }

    var linesWrap = el('span', 'entryrow__t entryrow__t--lines');
    var lines = quietLines(entry);
    if (!lines.length) {
      linesWrap.appendChild(el('span', 'entryrow__line--quiet', entryLabel(entry)));
    } else {
      lines.forEach(function (text) {
        linesWrap.appendChild(el('span', 'entryrow__line--quiet', text));
      });
    }
    row.appendChild(linesWrap);
    return row;
  }

  function screenRow(index) {
    var screen = dock.screens[index];
    if (!screen) return null;
    var row = el('button');
    row.type = 'button';
    row.tabIndex = -1;
    row.dataset.screen = String(index);
    row.setAttribute('aria-current', 'false');

    if (screen.blank) {
      row.className = 'screenerow screenerow--rest';
      row.textContent = 'Rest';
      return row;
    }

    var lines = screenLines(screen);
    row.className = 'screenerow';
    var wrap = el('span', 'screenerow__t--lines');
    if (lines.length) {
      lines.forEach(function (text) { wrap.appendChild(el('span', 'screenerow__line', text)); });
    } else if (screen.header) {
      wrap.appendChild(el('span', 'screenerow__line', String(screen.header)));
    } else {
      return null;
    }
    row.appendChild(wrap);
    return row;
  }

  function buildInner(entry) {
    var inner = el('div', 'entryinner');
    inner.setAttribute('aria-hidden', 'true');
    if ('inert' in inner) inner.inert = true;
    var clip = el('div', 'entryinner__clip');
    var body = el('div', 'entryinner__body');
    var baits = entry.baits || [];
    if (baits.length) {
      baits.forEach(function (bait) {
        body.appendChild(el('div', 'baithead', 'Bait ' + bait.number));
        for (var s = bait.start; s <= bait.end; s++) {
          var row = screenRow(s);
          if (row) body.appendChild(row);
        }
      });
    } else {
      for (var i = entry.start; i <= entry.end; i++) {
        var screen = screenRow(i);
        if (screen) body.appendChild(screen);
      }
    }
    if (!body.children.length) return null;
    clip.appendChild(body);
    inner.appendChild(clip);
    return inner;
  }

  /* The band is the live entry's last child: in flow (so it can never cover a row
     the way an overlay would) and sticky, so it pins over the list's foot while the
     block runs past the fold. One element, moved to whichever entry is live. */
  var nextBand = el('button', 'nextband');
  nextBand.type = 'button';
  nextBand.tabIndex = -1;
  nextBand.hidden = true;
  nextBand.appendChild(el('span', 'nextband__cap', 'Next'));
  var nextBandLabel = el('span', 'nextband__label', '');
  nextBand.appendChild(nextBandLabel);

  function bandText(entry) {
    var parts = entry.type === 'song' ? songParts(entry) : null;
    if (parts) return parts.reference ? parts.reference + ' — ' + parts.title : parts.title;
    return entryLabel(entry);
  }

  function renderList() {
    entryList.replaceChildren();
    dock.entries.forEach(function (entry, index) {
      var item = el('li', 'entryli');
      item.dataset.index = String(index);
      item.appendChild(entryRowContent(entry, index));
      var inner = buildInner(entry);
      if (inner) item.appendChild(inner);
      entryList.appendChild(item);
    });
    runNote.hidden = dock.entries.length > 0;
    if (!dock.entries.length) runNote.textContent = 'This Tata Ibadah has no entries yet.';
  }

  /* ---------- views and focus ----------------------------------------------- */

  function focusPanel() {
    try { panel.focus({preventScroll: true}); } catch (e) { panel.focus(); }
  }

  function setView(name, back) {
    if (panel.dataset.view === name) return;
    panel.dataset.view = name;
    var incoming = name === 'run' ? viewRun : viewPick;
    var outgoing = name === 'run' ? viewPick : viewRun;
    outgoing.classList.remove('is-active', 'is-in-forward', 'is-in-back');
    incoming.classList.add('is-active');
    incoming.classList.remove('is-in-forward', 'is-in-back');
    void incoming.offsetWidth;                       /* restart the animation */
    incoming.classList.add(back ? 'is-in-back' : 'is-in-forward');
    window.setTimeout(function () {
      incoming.classList.remove('is-in-forward', 'is-in-back');
    }, 220);
    focusPanel();
  }

  function openService(id, name, date) {
    dock.service = id;
    dock.name = name;
    dock.date = date;
    dock.entries = [];
    dock.screens = [];
    dock.lastEntry = null;
    dock.centerUnit = 'screen';
    runService.textContent = name;
    runDate.textContent = date;
    entryList.replaceChildren();
    runNote.hidden = true;
    setView('run', false);
    var wanted = id;
    fetchService(id).then(function (data) {
      if (dock.service !== wanted) return;
      if (!data) {
        runNote.hidden = false;
        runNote.textContent = 'The service could not be loaded.';
        return;
      }
      dock.entries = data.entries;
      dock.screens = data.screens;
      renderList();
      sync(gkpsDisplay.read());
    });
  }

  /* ---------- projection (the state's verbs) -------------------------------- */

  function projectScreen(index, unit) {
    if (dock.service == null || !dock.screens.length) return;
    if (unit) dock.centerUnit = unit;
    var target = Math.max(0, Math.min(index, dock.screens.length - 1));
    var state = gkpsDisplay.read();
    if (state.service === dock.service) gkpsDisplay.screen(target);
    else gkpsDisplay.show(dock.service, target);
  }

  function step(delta) {
    if (dock.service == null || !dock.screens.length) return;
    var state = gkpsDisplay.read();
    var base = state.service === dock.service ? state.screen : -1;
    if (delta < 0 && base <= 0) return;
    projectScreen(base + delta, 'screen');
  }

  function entryOfScreen(index) {
    for (var i = 0; i < dock.entries.length; i++) {
      var entry = dock.entries[i];
      if (index >= entry.start && index <= entry.end) return i;
    }
    return -1;
  }

  /* ---------- glide and centring (190 ms ease-out, clamped) ------------------ */

  var glideFrame = null;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function glideScroll(target) {
    var max = runBody.scrollHeight - runBody.clientHeight;
    var to = Math.max(0, Math.min(target, max));
    var from = runBody.scrollTop;
    if (glideFrame) { window.cancelAnimationFrame(glideFrame); glideFrame = null; }
    if (Math.abs(to - from) < 1) return;
    if (reduceMotion.matches) { runBody.scrollTop = to; return; }
    var started = performance.now();
    function frame(now) {
      var t = Math.min(1, (now - started) / 190);
      runBody.scrollTop = from + (to - from) * (1 - Math.pow(1 - t, 3));
      glideFrame = t < 1 ? window.requestAnimationFrame(frame) : null;
    }
    glideFrame = window.requestAnimationFrame(frame);
  }

  /* A sticky row's offsetTop is its PINNED position (600 in the probe), not where
     the row lives in the list (250) — aiming by it can never unpin the row, which is
     why an entry near the fold would not centre. Measure the row's non-sticky parent
     for entry rows; screen rows are not sticky themselves and are safe. */
  function layoutTop(node) {
    if (node.classList.contains('entryrow')) {
      var li = node.closest('.entryli');
      if (li) return li.offsetTop;
    }
    return node.offsetTop;
  }

  function centerRow(node) {
    if (!node) return;
    var target = layoutTop(node) - (runBody.clientHeight - node.offsetHeight) / 2;
    glideScroll(target);
  }

  /* The centring target follows the navigation unit (spec 119): a move by entry
     centres the ENTRY row, a move by screen centres the SCREEN row. */
  function liveNode() {
    if (dock.centerUnit === 'entry') {
      return entryList.querySelector('.entryrow[aria-current="true"]') ||
             entryList.querySelector('.screenerow[aria-current="true"]');
    }
    return entryList.querySelector('.screenerow[aria-current="true"]') ||
           entryList.querySelector('.entryrow[aria-current="true"]');
  }

  /* One centring per frame, whatever number of state notices arrived. */
  var centerFrame = 0;

  function scheduleCenter() {
    if (centerFrame) return;
    centerFrame = window.requestAnimationFrame(function () {
      centerFrame = 0;
      centerRow(liveNode());
    });
  }

  /* When the layout itself is animating (one entry collapsing, another growing),
     a glide to a fixed point would aim at a spot the rows are moving away from.
     Instead the scroll FOLLOWS the live row for the animation's duration, easing
     toward the row's current position every frame: the motion comes from the
     layout, so it reads as one movement, not two — and never snaps to a target
     that is still moving. */
  var followFrame = 0;

  function followCenter(duration) {
    if (followFrame) { window.cancelAnimationFrame(followFrame); followFrame = 0; }
    if (reduceMotion.matches) { scheduleCenter(); return; }
    var until = performance.now() + (duration || 260) + 200;
    function step(now) {
      followFrame = 0;
      var node = liveNode();
      if (!node) return;
      var max = runBody.scrollHeight - runBody.clientHeight;
      var target = layoutTop(node) - (runBody.clientHeight - node.offsetHeight) / 2;
      target = Math.max(0, Math.min(target, max));
      var delta = target - runBody.scrollTop;
      if (Math.abs(delta) < 1) { runBody.scrollTop = target; return; }
      if (now >= until) { runBody.scrollTop = target; return; }
      runBody.scrollTop += delta * 0.25;          /* exponential ease, no overshoot */
      followFrame = window.requestAnimationFrame(step);
    }
    followFrame = window.requestAnimationFrame(step);
  }

  /* A hand on the list wins over the follow loop. */
  runBody.addEventListener('wheel', function () {
    if (followFrame) { window.cancelAnimationFrame(followFrame); followFrame = 0; }
  }, {passive: true});
  runBody.addEventListener('pointerdown', function () {
    if (followFrame) { window.cancelAnimationFrame(followFrame); followFrame = 0; }
  });

  /* ---------- the pinned row and the NEXT band ------------------------------ */

  function updateBand() {
    var liveEntry = entryList.querySelector('.entryli[data-live="true"]');
    if (!liveEntry) {
      nextBand.hidden = true;
      return;
    }
    var index = Number(liveEntry.dataset.index);
    if (nextBand.parentElement !== liveEntry) liveEntry.appendChild(nextBand);
    var box = runBody.getBoundingClientRect();
    var row = liveEntry.querySelector('.entryrow');
    if (row) row.classList.toggle('is-stuck', row.getBoundingClientRect().top - box.top <= 0.5);
    var next = dock.entries[index + 1];
    if (!next) {
      nextBand.hidden = true;
      return;
    }
    nextBand.dataset.index = String(index + 1);
    nextBandLabel.textContent = bandText(next);
    /* The band yields the moment the entry's own end is in view. */
    nextBand.hidden = liveEntry.getBoundingClientRect().bottom <= box.bottom + 6;
  }

  var scrollScheduled = false;
  runBody.addEventListener('scroll', function () {
    if (scrollScheduled) return;
    scrollScheduled = true;
    window.requestAnimationFrame(function () { scrollScheduled = false; updateBand(); });
  }, {passive: true});

  /* ---------- edition chip and bait strip ------------------------------------ */

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
      transChip.setAttribute('aria-pressed', 'false');
      return;
    }
    var entry = dock.entries[activeEntry] || {};
    var own = entry.translation || options[0];
    var shown = dock.translation || own;
    transChip.hidden = false;
    transChip.textContent = shown;
    transChip.dataset.editions = options.join(',');
    transChip.setAttribute('aria-pressed', shown !== own ? 'true' : 'false');
  }

  function updateBaitFades() {
    var max = baitChips.scrollWidth - baitChips.clientWidth;
    baitChips.classList.toggle('is-left', baitChips.scrollLeft > 2);
    baitChips.classList.toggle('is-right', max > 2 && baitChips.scrollLeft < max - 2);
  }

  function renderBaits(live, activeEntry) {
    baitChips.replaceChildren();
    var entry = live && activeEntry >= 0 ? dock.entries[activeEntry] : null;
    var baits = (entry && entry.baits) || [];
    baitStrip.hidden = !baits.length;
    if (!baits.length) return;
    var liveChip = null;
    baits.forEach(function (bait) {
      var chip = el('button', 'bait', String(bait.number));
      chip.type = 'button';
      chip.tabIndex = -1;
      chip.dataset.screen = String(bait.start);
      var current = dock.screen >= bait.start && dock.screen <= bait.end;
      chip.setAttribute('aria-pressed', current ? 'true' : 'false');
      if (current) liveChip = chip;
      baitChips.appendChild(chip);
    });
    updateBaitFades();
    if (liveChip) {
      var target = liveChip.offsetLeft - (baitChips.clientWidth - liveChip.offsetWidth) / 2;
      try { baitChips.scrollTo({left: target, behavior: reduceMotion.matches ? 'auto' : 'smooth'}); }
      catch (e) { baitChips.scrollLeft = target; }
    }
  }

  baitChips.addEventListener('scroll', updateBaitFades, {passive: true});

  /* ---------- the state ------------------------------------------------------ */

  function sync(state) {
    if (!state) state = gkpsDisplay.read();
    var live = state.service != null && state.service === dock.service;
    dock.on = live && state.on === true;
    dock.screen = live ? state.screen : 0;
    dock.translation = live ? state.translation : null;

    blankBtn.setAttribute('aria-pressed', dock.on ? 'false' : 'true');
    var title = dock.on ? 'Hide words' : 'Display this service';
    blankBtn.title = title;
    blankBtn.setAttribute('aria-label', title);

    var activeEntry = live ? entryOfScreen(state.screen) : -1;
    entryList.querySelectorAll('.entryli').forEach(function (li) {
      var index = Number(li.dataset.index);
      var current = live && index === activeEntry;
      li.dataset.live = current ? 'true' : 'false';
      var row = li.querySelector('.entryrow');
      if (row) row.setAttribute('aria-current', current ? 'true' : 'false');
      var inner = li.querySelector('.entryinner');
      if (inner) {
        inner.classList.toggle('is-open', current);
        inner.setAttribute('aria-hidden', current ? 'false' : 'true');
        if ('inert' in inner) inner.inert = !current;
      }
      li.querySelectorAll('.screenerow').forEach(function (screenRow) {
        screenRow.setAttribute('aria-current',
          current && Number(screenRow.dataset.screen) === state.screen ? 'true' : 'false');
      });
    });

    pickBody.querySelectorAll('.onscreen').forEach(function (pill) {
      pill.hidden = !(state.service != null && state.on === true &&
                      Number(pill.dataset.onscreenFor) === state.service);
    });

    prevBtn.disabled = !live || state.screen <= 0;
    nextBtn.disabled = !live || state.screen >= dock.screens.length - 1;

    updateChip(live, activeEntry);
    renderBaits(live, activeEntry);
    updateBand();
    if (live) {
      if (activeEntry !== dock.lastEntry) followCenter(260);
      else scheduleCenter();
    }
    dock.lastEntry = live ? activeEntry : null;
  }

  /* ---------- controls ------------------------------------------------------- */

  pickBody.addEventListener('click', function (event) {
    var row = event.target.closest('.servicerow');
    if (!row) return;
    openService(Number(row.dataset.service), row.dataset.name, row.dataset.date);
  });

  entryList.addEventListener('click', function (event) {
    var band = event.target.closest('.nextband');
    if (band) {
      var nextEntry = dock.entries[Number(band.dataset.index)];
      if (nextEntry) projectScreen(nextEntry.start, 'entry');
      focusPanel();
      return;
    }
    var screenRow = event.target.closest('.screenerow');
    if (screenRow) {
      projectScreen(Number(screenRow.dataset.screen), 'screen');
      focusPanel();
      return;
    }
    var row = event.target.closest('.entryrow');
    if (!row) return;
    var entry = dock.entries[Number(row.dataset.index)];
    if (!entry) return;
    projectScreen(entry.start, 'entry');
    focusPanel();
  });

  baitChips.addEventListener('click', function (event) {
    var chip = event.target.closest('.bait');
    if (!chip) return;
    projectScreen(Number(chip.dataset.screen), 'screen');
    focusPanel();
  });

  function flipEdition() {
    var editions = (transChip.dataset.editions || '').split(',').filter(Boolean);
    if (!editions.length) return;
    var index = editions.indexOf(transChip.textContent);
    gkpsDisplay.flip(editions[(index + 1) % editions.length] || null);
  }

  blankBtn.addEventListener('click', function () {
    if (dock.service == null) return;
    var state = gkpsDisplay.read();
    if (state.service === dock.service) {
      if (state.on) gkpsDisplay.hide();           /* Hide words: the place is kept */
      else gkpsDisplay.screen(state.screen);      /* resume where it was paused */
    } else {
      gkpsDisplay.show(dock.service, 0);          /* display from the start */
      dock.centerUnit = 'entry';
    }
    focusPanel();
  });

  transChip.addEventListener('click', function () { flipEdition(); focusPanel(); });
  prevBtn.addEventListener('click', function () { step(-1); focusPanel(); });
  nextBtn.addEventListener('click', function () { step(1); focusPanel(); });
  switchBtn.addEventListener('click', function () { setView('pick', true); });
  reloadBtn.addEventListener('click', function () { window.location.reload(); });

  /* ---------- keyboard (the dock owns it) ------------------------------------ */

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
      projectScreen(dock.entries[index].start, 'entry');
      return;
    }
    if (unit === 'bait' && at.entry && (at.entry.baits || []).length) {
      var baits = at.entry.baits;
      var bait = 0;
      for (var i = 0; i < baits.length; i++) {
        if (at.index >= baits[i].start) bait = i;
      }
      bait = Math.max(0, Math.min(baits.length - 1, bait + delta));
      projectScreen(baits[bait].start, 'screen');
      return;
    }
    step(delta);
  }

  function edgeOf(unit, end) {
    var at = unitAt();
    if (unit === 'entry') {
      if (!dock.entries.length) return;
      projectScreen(end ? dock.entries[dock.entries.length - 1].start : 0, 'entry');
      return;
    }
    if (unit === 'bait' && at.entry && (at.entry.baits || []).length) {
      var baits = at.entry.baits;
      projectScreen(end ? baits[baits.length - 1].start : baits[0].start, 'screen');
      return;
    }
    if (!dock.screens.length) return;
    projectScreen(end ? dock.screens.length - 1 : 0, 'screen');
  }

  panel.addEventListener('keydown', function (event) {
    if (event.altKey) return;
    var key = event.key;
    var shift = event.shiftKey;
    var ctrl = event.ctrlKey || event.metaKey;
    if (key === 'Escape') {
      if (panel.dataset.view === 'run') setView('pick', true);
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
    if (ctrl) return;                                   /* leave other combos alone */
    if (key === ' ') { event.preventDefault(); blankBtn.click(); return; }
    if (key === 't' || key === 'T') flipEdition();
  });

  /* A click must leave the focus where the keyboard lives, not on the clicked
     button: otherwise Space would re-press the last thing clicked. */
  panel.addEventListener('pointerdown', focusPanel);

  /* The transport arrows fill while this window holds the keyboard. */
  function markFocus() { root.classList.add('win-focus'); }
  function clearFocus() { root.classList.remove('win-focus'); }
  window.addEventListener('focus', markFocus);
  window.addEventListener('blur', clearFocus);
  if (document.hasFocus()) markFocus(); else clearFocus();

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
  focusPanel();
})();
