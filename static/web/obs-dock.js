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
 * focus back on pointerdown). The keys are listed where the operator reads them — the
 * `K` sheet in `obs_dock.html`, in the projector's wording — and one grammar spans both
 * surfaces (spec 187):
 *
 *     ↑ / ↓                                 move the pick (the picker only)
 *     Enter                                 open the marked service (the picker only)
 *     G                                     go to a passage or a song (both views)
 *     K                                     the shortcut sheet (both views)
 *     ArrowDown / ArrowRight / PageDown     next screen; in a go to, the next verse
 *     ArrowUp / ArrowLeft / PageUp          previous screen / verse
 *     Shift + the same                      next / previous bait, or chapter in a go to
 *     Ctrl/⌘ + the same                     next / previous entry, or book in a go to
 *     Home / End                            first / last of the unit on show
 *     Shift / Ctrl + Home / End             the unit's first / last bait, chapter or entry
 *     Space                                 display / hide what is on air
 *     T                                     show the other edition (passages)
 *     Escape (held 900 ms)                  back to the picker
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
  var findBtn = document.getElementById('findBtn');
  var bandSwap = document.getElementById('bandSwap');
  var transportRow = document.getElementById('transportRow');
  var findBand = document.getElementById('findBand');
  var findInput = document.getElementById('findInput');
  var findResult = document.getElementById('findResult');
  var findLabel = document.getElementById('findLabel');
  var findCount = document.getElementById('findCount');
  var findScrim = document.getElementById('findScrim');
  var offBlock = document.getElementById('offBlock');
  var offLabel = document.getElementById('offLabel');
  var offBack = document.getElementById('offBack');
  var offBody = document.getElementById('offBody');
  var themeBtn = document.getElementById('themeBtn');
  var root = document.documentElement;

  var cache = {};                 /* service id -> {entries, screens} */
  var dock = {
    service: null, name: '', date: '',
    entries: [], screens: [], stops: [],
    pickIndex: -1,
    on: false, screen: 0, translation: null,
    lastEntry: null,
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

  /* Media screens carry no words, only a payload — they still get an inner row so
     navigation can land on (and centre) them like any other screen. */
  var MEDIA_KINDS = [
    ['image_sha256', 'Image'],
    ['video_sha256', 'Video'],
    ['audio_sha256', 'Audio'],
    ['pdf_sha256', 'PDF'],
    ['slides_sha256', 'Slides'],
  ];

  function mediaLabel(screen) {
    for (var i = 0; i < MEDIA_KINDS.length; i++) {
      if (screen[MEDIA_KINDS[i][0]]) return MEDIA_KINDS[i][1];
    }
    return '';
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
      var media = mediaLabel(screen);
      if (!media) return null;
      row.classList.add('screenerow--media');
      row.appendChild(el('span', 'screenerow__media', media));
      return row;
    }
    row.appendChild(wrap);
    return row;
  }

  function buildInner(entry) {
    if (isDivider(entry)) return null;             /* a hairline has nothing to open */
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

  /* ---------- the picker's cursor -------------------------------------------- */

  function pickRows() {
    return Array.prototype.slice.call(pickBody.querySelectorAll('.servicerow'));
  }

  /* An arrow-move cursor for the picker: the panel keeps the keyboard (every control
     is tabindex="-1"), so this is a marked row, not a focused one. The last row the
     operator touched stays marked when they come back from a service. */
  function setPickCursor(index, scroll) {
    var rows = pickRows();
    if (!rows.length) { dock.pickIndex = -1; return; }
    var i = Math.max(0, Math.min(index, rows.length - 1));
    dock.pickIndex = i;
    rows.forEach(function (row, n) {
      var on = n === i;
      row.classList.toggle('is-cursor', on);
      if (on) row.setAttribute('aria-current', 'true');
      else row.removeAttribute('aria-current');
    });
    if (scroll) {
      try { rows[i].scrollIntoView({block: 'nearest'}); }
      catch (e) { rows[i].scrollIntoView(); }
    }
  }

  function openCursorRow() {
    var rows = pickRows();
    var row = rows[dock.pickIndex];
    if (!row) return;
    openService(Number(row.dataset.service), row.dataset.name, row.dataset.date);
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
    if (name === 'pick') {
      var rows = pickRows();
      if (rows.length && dock.pickIndex < 0) setPickCursor(0, false);
      else if (rows.length) setPickCursor(dock.pickIndex, true);
    }
    cancelEscapeHold();
    if (keysOpen) applyKeysGroup();
    focusPanel();
  }

  function openService(id, name, date) {
    dock.service = id;
    dock.name = name;
    dock.date = date;
    dock.entries = [];
    dock.screens = [];
    dock.stops = [];
    dock.lastEntry = null;
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
      buildStops();
      renderList();
      sync(gkpsDisplay.read());
    });
  }

  /* ---------- projection (the state's verbs) -------------------------------- */

  function projectScreen(index) {
    if (dock.service == null || !dock.screens.length) return;
    var target = Math.max(0, Math.min(index, dock.screens.length - 1));
    var state = gkpsDisplay.read();
    if (state.service === dock.service) gkpsDisplay.screen(target);
    else gkpsDisplay.show(dock.service, target);
  }

  function step(delta) {
    if (dock.service == null || !dock.stops.length) return;
    var state = gkpsDisplay.read();
    /* The transport steps what is on air: the go to while one is up, the service
       otherwise (FR-015). */
    if (state.goto) { stepGoto(delta); return; }
    var base = state.service === dock.service ? state.screen : -1;
    var list = dock.stops;
    var at = list.indexOf(base);
    var target;
    if (at >= 0) {
      target = list[Math.max(0, Math.min(list.length - 1, at + delta))];
    } else if (base < 0) {
      target = list[0];
    } else {
      /* a divider screen left in stored state: snap to the nearest content screen */
      var next = null;
      for (var i = 0; i < list.length; i++) {
        if (list[i] > base) { next = list[i]; break; }
      }
      if (delta > 0) target = next == null ? list[list.length - 1] : next;
      else target = next == null ? list[list.length - 1] : (list[list.indexOf(next) - 1] != null ? list[list.indexOf(next) - 1] : list[0]);
    }
    projectScreen(target);
  }

  function entryOfScreen(index) {
    for (var i = 0; i < dock.entries.length; i++) {
      var entry = dock.entries[i];
      if (index >= entry.start && index <= entry.end) return i;
    }
    return -1;
  }

  /* A section break is a hairline in the list, not a place the service stands:
     it has no inner, is not clickable, and every step passes over its blank
     screens (a Tata Ibadah can end in a run of unfilled section breaks). */
  function isDivider(entry) {
    return !!entry && entry.type === 'break';
  }

  function contentEntries() {
    return dock.entries.filter(function (entry) { return !isDivider(entry); });
  }

  function buildStops() {
    dock.stops = [];
    dock.entries.forEach(function (entry) {
      if (isDivider(entry)) return;
      for (var i = entry.start; i <= entry.end; i++) dock.stops.push(i);
    });
  }

  /* ---------- glide and centring (190 ms ease-out, clamped) ------------------ */

  var glideFrame = null;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  var glideTarget = null;

  function glideScroll(target) {
    /* Several notices can land for one move (the state echoes back to this tab).
       Restarting the glide each time would hold it at its start, so a glide that
       is already heading to this target is left alone. */
    if (glideFrame && glideTarget !== null && Math.abs(target - glideTarget) < 2) return;
    if (glideFrame) { window.cancelAnimationFrame(glideFrame); glideFrame = null; }
    glideTarget = target;
    if (reduceMotion.matches) { runBody.scrollTop = target; return; }
    /* `from` is read on the first frame, not here: closing a block can shrink the
       scroll range for a moment and the browser clamps scrollTop, so the position
       this glide actually starts from may differ from the one at call time. */
    var from = null;
    var started = performance.now();
    function frame(now) {
      if (from === null) {
        from = runBody.scrollTop;
        started = now;
        if (Math.abs(target - from) < 1) { glideFrame = null; return; }
      }
      /* The list may still be growing (the arriving block opening), so the
         reachable end moves during the glide: clamp against it every frame rather
         than freezing a target that was measured too early. */
      var max = runBody.scrollHeight - runBody.clientHeight;
      var to = Math.max(0, Math.min(target, max));
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

  /* The centring target is always the live INNER row (the current screen, or a
     song's current bait row); the entry's label row only stands in when the screen
     has no row of its own. */
  function liveNode() {
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

  /* One continuous crossing (mockup v14/v15): both inner heights are animated by
     hand and, on the same curve, the arriving row's screen position blends from
     where it is to the middle. Because scrollTop is derived from the row's live
     layout position each frame, the collapsing block and the opening block cannot
     tug the row around — expand, collapse and scroll are one transition. */
  var morphFrame = 0;
  var morphState = null;

  function easeInOut(t) {
    return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  }

  function startMorph(outInner, inInner, node) {
    cancelPendingCenter();
    if (morphState) finishMorph();
    var outBody = outInner.querySelector('.entryinner__body');
    var inBody = inInner.querySelector('.entryinner__body');
    var hOut = outBody ? outBody.offsetHeight : outInner.offsetHeight;
    var hIn = inBody ? inBody.offsetHeight : 0;
    var box = runBody.getBoundingClientRect();
    var rect = node.getBoundingClientRect();
    var startY = rect.top - box.top;
    var centreY = (runBody.clientHeight - node.offsetHeight) / 2;
    var started = performance.now();
    var duration = 230;

    outInner.classList.add('is-morph');
    inInner.classList.add('is-morph');
    inInner.classList.add('is-open');              /* pointer events; height is inline */
    /* sync() skips both inners while the morph runs, so the arriving block's
       inert/aria-hidden must be cleared HERE — otherwise the block opens visible
       but unclickable. */
    inInner.setAttribute('aria-hidden', 'false');
    if ('inert' in inInner) inInner.inert = false;
    morphState = {out: outInner, inn: inInner, node: node};
    if (reduceMotion.matches) { finishMorph(); return; }

    function frame(now) {
      var t = Math.min(1, (now - started) / duration);
      var e = easeInOut(t);
      outInner.style.gridTemplateRows = Math.max(0, hOut * (1 - e)) + 'px';
      inInner.style.gridTemplateRows = Math.max(0, hIn * e) + 'px';
      /* The row's layout position already includes both height changes, so this
         puts it exactly where the curve says it should be on screen. */
      var desired = startY + (centreY - startY) * e;
      var max = runBody.scrollHeight - runBody.clientHeight;
      runBody.scrollTop = Math.max(0, Math.min(layoutTop(node) - desired, max));
      if (t < 1) morphFrame = window.requestAnimationFrame(frame);
      else finishMorph();
    }
    morphFrame = window.requestAnimationFrame(frame);
  }

  function finishMorph() {
    if (morphFrame) { window.cancelAnimationFrame(morphFrame); morphFrame = 0; }
    if (!morphState) return;
    var out = morphState.out;
    var inn = morphState.inn;
    var node = morphState.node;
    morphState = null;
    out.classList.remove('is-morph');
    inn.classList.remove('is-morph');
    out.classList.remove('is-open');
    inn.classList.add('is-open');
    out.setAttribute('aria-hidden', 'true');
    if ('inert' in out) out.inert = true;
    inn.setAttribute('aria-hidden', 'false');
    if ('inert' in inn) inn.inert = false;
    out.style.gridTemplateRows = '';
    inn.style.gridTemplateRows = '';
    if (node) centerRow(node);
  }

  function cancelPendingCenter() {
    if (morphState) finishMorph();
    if (glideFrame) { window.cancelAnimationFrame(glideFrame); glideFrame = null; }
    glideTarget = null;
  }

  /* A hand on the list wins over any pending centring or glide. */
  runBody.addEventListener('wheel', cancelPendingCenter, {passive: true});
  runBody.addEventListener('pointerdown', cancelPendingCenter);

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
    var next = null;
    for (var i = index + 1; i < dock.entries.length; i++) {
      if (!isDivider(dock.entries[i])) { next = dock.entries[i]; break; }
    }
    if (!next) {
      nextBand.hidden = true;
      return;
    }
    nextBand.dataset.screen = String(next.start);
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

  /* ---------- the go to (spec 185) ------------------------------------------- */

  /* The find band is a layer over the dock, and it is where the index is read: the
     lookup module is injected on the first open, so a dock that is never searched
     pays nothing for a 29 KB index (D004). */
  var find = {open: false, rows: [], choice: 0, status: 'idle', fromPicker: false};
  var shown = {key: '', payload: null, loading: false};

  function measureBand() {
    var transport = transportRow.scrollHeight || 40;
    bandSwap.style.setProperty('--transport-h', transport + 'px');
    var band = findBand.scrollHeight;
    if (band) bandSwap.style.setProperty('--band-h', band + 'px');
  }

  function ensureLibrary() {
    if (window.GKPSProjectorLibrary) return;
    var tag = document.createElement('script');
    tag.src = panel.dataset.libraryUrl || '/static/web/projector-library.js';
    tag.onerror = function () { find.status = 'failed'; paintFind(); };
    document.head.appendChild(tag);
  }

  function paintFind() {
    var row = find.rows[find.choice] || null;
    var typed = findInput.value.trim();
    findResult.dataset.match = row ? 'true' : 'false';
    findResult.disabled = !row;
    if (find.status === 'loading') findLabel.textContent = 'Loading search…';
    else if (find.status === 'failed') findLabel.textContent = 'Could not load — try again';
    else if (!typed) findLabel.textContent = 'Start typing to find a match';
    else if (!row) findLabel.textContent = 'No matching passage or song';
    else findLabel.textContent = row.label;
    findCount.textContent = find.rows.length
      ? (find.choice + 1) + ' / ' + find.rows.length : '0 / 0';
  }

  function refreshFind() {
    if (find.status !== 'ready' || !window.GKPSProjectorLibrary) { paintFind(); return; }
    find.rows = window.GKPSProjectorLibrary.lookup(findInput.value) || [];
    find.choice = 0;
    paintFind();
  }

  function openFind() {
    if (find.open || keysOpen) return;
    /* The picker may start a go to with nothing underneath it (FR-002); from the
       runner the band still needs the service it browses. */
    if (dock.service == null && panel.dataset.view !== 'pick') return;
    find.fromPicker = panel.dataset.view === 'pick';
    cancelEscapeHold();
    find.open = true;
    find.status = window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.ready()
      ? 'ready' : 'loading';
    find.rows = [];
    find.choice = 0;
    findInput.value = '';
    findInput.disabled = find.status !== 'ready';
    /* The footer that carries the band is hidden on the picker until the band needs it
       (FR-002), so it is shown before its rows are measured. */
    panel.classList.add('is-find');
    measureBand();
    bandSwap.classList.add('is-find');
    findScrim.hidden = false;
    window.requestAnimationFrame(function () { findScrim.classList.add('is-on'); });
    paintFind();
    ensureLibrary();
    try { findInput.focus({preventScroll: true}); } catch (e) { findInput.focus(); }
  }

  function closeFind() {
    if (!find.open) return;
    find.open = false;
    bandSwap.classList.remove('is-find');
    /* The footer folds away with the band on the picker, after its own 200 ms. */
    window.setTimeout(function () {
      if (!find.open) panel.classList.remove('is-find');
    }, 210);
    findScrim.classList.remove('is-on');
    window.setTimeout(function () { if (!find.open) findScrim.hidden = true; }, 170);
    findInput.value = '';
    findInput.disabled = false;
    find.rows = [];
    find.choice = 0;
    find.status = 'idle';
    paintFind();
    focusPanel();
  }

  /* What is on air as a pointer (FR-001): the payload that paints it is fetched here
     and cached, keyed by the goto, never stored (D003). */
  function gotoKey(goto) {
    if (!goto) return '';
    return goto.kind === 'song' ? 'song:' + goto.song_id
      : 'passage:' + goto.book_id + ':' + goto.chapter;
  }

  function fetchGoto(state) {
    var key = gotoKey(state.goto);
    if (shown.key === key) return;                 /* held or already in flight */
    shown.key = key;
    shown.payload = null;
    shown.loading = true;
    var url = state.goto.kind === 'song'
      ? '/projector/goto/song/' + state.goto.song_id + '/'
      : '/projector/goto/chapter/' + state.goto.book_id + '/' + state.goto.chapter + '/';
    window.fetch(url, {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function (payload) {
        shown.loading = false;
        shown.payload = state.goto.kind === 'song'
          ? {kind: 'song', label: payload.label, screens: payload.screens || [],
             baits: payload.baits || []}
          : {kind: 'passage', label: payload.label, editions: payload.editions || {}};
        sync(gkpsDisplay.read());
      })
      .catch(function () {
        shown.loading = false;
        shown.payload = null;
        var key2 = gotoKey(gkpsDisplay.read().goto);
        if (key2 === key) {
          shown.key = '';                          /* a later sync may retry */
          runNote.hidden = false;
          runNote.textContent = 'The go to could not be loaded.';
        }
      });
  }

  function gotoLabelOf(state) {
    if (gotoBusy || !shown.payload) return 'Loading…';
    if (shown.payload.kind === 'song') return shown.payload.label;
    var editions = shown.payload.editions || {};
    var edition = editions.TB || editions[Object.keys(editions)[0]];
    if (!edition) return 'Loading…';
    return edition.name + ' ' + state.goto.chapter + ':' + state.goto.verse;
  }

  function baitHeads(payload) {
    return (payload.baits || []).map(function (bait) {
      return {kind: 'head', number: bait.number};
    });
  }

  function songRows(payload) {
    var rows = [];
    (payload.baits || []).forEach(function (bait) {
      rows.push({kind: 'head', label: 'Bait ' + bait.number});
      for (var i = bait.start; i <= bait.end; i++) {
        var screen = payload.screens[i];
        if (!screen) continue;
        if (screen.blank) { rows.push({kind: 'rest', pos: i, label: 'Rest'}); continue; }
        rows.push({kind: 'lyric', pos: i,
                   label: (screen.lines || []).map(function (line) { return line.text; })
                     .join(' ')});
      }
    });
    return rows;
  }

  function passageRows(payload) {
    var editions = payload.editions || {};
    var edition = editions.TB || editions[Object.keys(editions)[0]];
    var verses = (edition && edition.verses) || [];
    return verses.map(function (verse) {
      return {kind: 'verse', pos: verse.n, label: verse.n + '. ' + verse.text};
    });
  }

  function renderBlock(state) {
    if (!state.goto) { offBlock.hidden = true; entryList.hidden = false; return; }
    entryList.hidden = true;
    offBlock.hidden = false;
    fetchGoto(state);
    offLabel.textContent = gotoLabelOf(state);
    offBody.replaceChildren();
    if (!shown.payload) return;
    var rows = shown.payload.kind === 'song' ? songRows(shown.payload)
      : passageRows(shown.payload);
    var current = state.goto.kind === 'song' ? state.goto.index : state.goto.verse;
    rows.forEach(function (row) {
      if (row.kind === 'head') {
        offBody.appendChild(el('div', 'baithead', row.label));
        return;
      }
      var button = el('button', 'screenerow' + (row.kind === 'rest' ? ' is-rest' : ''),
                      row.label);
      button.type = 'button';
      button.tabIndex = -1;
      button.classList.add('offrow');
      button.dataset.pos = String(row.pos);
      button.setAttribute('aria-current', row.pos === current ? 'true' : 'false');
      offBody.appendChild(button);
    });
  }

  function pickBaitTarget(payload, index, step, last) {
    var baits = payload.baits || [];
    if (!baits.length) return null;
    var at = -1;
    baits.forEach(function (bait, n) { if (index >= bait.start && index <= bait.end) at = n; });
    if (last) return step > 0 ? baits[baits.length - 1].start : baits[0].start;
    at = Math.max(0, Math.min(baits.length - 1, (at < 0 ? 0 : at) + step));
    return baits[at].start;
  }

  function paintGotoTransport(state) {
    var payload = shown.payload;
    var goto = state.goto;
    /* Edition chip: the go to's own editions, with the one it shows (FR-002). */
    if (payload && payload.kind === 'passage') {
      var codes = Object.keys(payload.editions || {});
      if (codes.length) {
        transChip.hidden = false;
        transChip.textContent = goto.translation || codes[0];
        transChip.dataset.editions = codes.join(',');
        transChip.setAttribute('aria-pressed', 'false');
      } else {
        transChip.hidden = true;
      }
    } else {
      transChip.hidden = true;
    }
    /* Baits: the song's own, with the one on air pressed. */
    baitChips.replaceChildren();
    var baits = (payload && payload.kind === 'song' && payload.baits) || [];
    baitStrip.hidden = !baits.length;
    if (baits.length) {
      baits.forEach(function (bait) {
        var chip = el('button', 'bait', String(bait.number));
        chip.type = 'button';
        chip.tabIndex = -1;
        chip.dataset.screen = String(bait.start);
        chip.setAttribute('aria-pressed',
          goto.index >= bait.start && goto.index <= bait.end ? 'true' : 'false');
        baitChips.appendChild(chip);
      });
      updateBaitFades();
    }
    var lastIndex = payload && payload.screens ? payload.screens.length - 1 : 0;
    if (goto.kind === 'song') {
      prevBtn.disabled = goto.index <= 0;
      nextBtn.disabled = goto.index >= lastIndex;
    } else {
      var verses = payload && payload.editions
        ? (payload.editions[goto.translation] || payload.editions.TB || {}).verses || [] : [];
      var first = verses.length ? verses[0].n : null;
      var end = verses.length ? verses[verses.length - 1].n : null;
      prevBtn.disabled = first == null || goto.verse <= first;
      nextBtn.disabled = end == null || goto.verse >= end;
    }
  }

  function adoptGoto(row, payload) {
    /* A go to chosen on the picker stands alone: it never adopts the marked service
       (FR-004). Chosen from the runner, it keeps adopting the browsed service, so Back
       always has a place to land (FR-016 of spec 185). */
    if (!find.fromPicker && gkpsDisplay.read().service == null) {
      gkpsDisplay.show(dock.service, 0);
    }
    if (payload.kind === 'song') {
      gkpsDisplay.goTo({kind: 'song', song_id: row.target.song_id, index: 0});
      return;
    }
    gkpsDisplay.goTo({kind: 'passage', book_id: payload.book_id, chapter: payload.chapter,
                      verse: payload.verse, translation: payload.translation});
  }

  function chooseFind(index) {
    var row = find.rows[index];
    if (!row || !window.GKPSProjectorLibrary) return;
    var fromPicker = find.fromPicker;
    find.status = 'loading';
    paintFind();
    window.GKPSProjectorLibrary.detour(row).then(function (payload) {
      if (!payload) throw new Error('Nothing to paint');
      /* The block paints from this same payload: one request per selection, never two. */
      shown.key = gotoKey(payload.kind === 'song'
        ? {kind: 'song', song_id: row.target.song_id}
        : {kind: 'passage', book_id: payload.book_id, chapter: payload.chapter});
      shown.payload = payload.kind === 'song'
        ? {kind: 'song', label: payload.label, screens: payload.screens || [],
           baits: payload.baits || []}
        : {kind: 'passage', label: payload.label, editions: payload.editions || {}};
      shown.loading = false;
      adoptGoto(row, payload);
      closeFind();
      /* The block is where a go to is stepped and `Back` lives, so a go to started on
         the picker hands the stage to the runner (FR-004). */
      if (fromPicker) setView('run', false);
    }).catch(function () {
      find.status = 'failed';
      findInput.disabled = false;
      paintFind();
    });
  }

  function stepGoto(delta) {
    var state = gkpsDisplay.read();
    if (!state.goto) return;
    if (!shown.payload) return;
    var target;
    if (state.goto.kind === 'song') {
      var last = (shown.payload.screens || []).length - 1;
      target = Math.max(0, Math.min(state.goto.index + delta, last));
    } else {
      var verses = ((shown.payload.editions || {})[state.goto.translation]
                    || (shown.payload.editions || {}).TB || {}).verses || [];
      var at = verses.findIndex(function (verse) { return verse.n === state.goto.verse; });
      if (at < 0) at = 0;
      var next = verses[Math.max(0, Math.min(at + delta, verses.length - 1))];
      target = next ? next.n : state.goto.verse;
    }
    gkpsDisplay.stepGoto(target);
  }

  /* ---------- the state ------------------------------------------------------ */

  function sync(state) {
    if (!state) state = gkpsDisplay.read();
    var live = state.service != null && state.service === dock.service;
    dock.on = live && state.on === true;
    dock.screen = live ? state.screen : 0;
    dock.translation = live ? state.translation : null;

    /* A go to can stand with no service underneath it (FR-003): it is what is on air,
       so the dock paints its block though no service is live. */
    var hadGoto = dock.goto != null;
    var goto = state.goto && (live || state.service == null) ? state.goto : null;
    dock.goto = goto;
    /* The runner holding a go to alone names its mode; the block below names the go to
       itself, so the head does not repeat it. */
    var alone = goto != null && state.service == null;
    panel.classList.toggle('is-alone', alone);
    if (alone) runService.textContent = 'Go To';
    else if (dock.name) runService.textContent = dock.name;
    /* A go to that stood alone and has just ended leaves the dock with nothing to run,
       so Back hands it back to the picker it was started from (FR-004). */
    if (hadGoto && !goto && state.service == null && panel.dataset.view === 'run') {
      setView('pick', true);
    }
    /* The switch-service control is disabled, not hidden, while a go to is up: the
       head keeps its width and the exit stays visible (FR-019). */
    /* A go to can stand with no service underneath it: there is none to lose, and the
       control returns to the picker (FR-004). */
    switchBtn.disabled = !!dock.goto && state.service != null;

    blankBtn.setAttribute('aria-pressed', dock.on ? 'false' : 'true');
    var title = dock.on ? 'Hide words'
      : (dock.goto ? 'Show words' : 'Display this service');
    blankBtn.title = title;
    blankBtn.setAttribute('aria-label', title);

    if (dock.goto) {
      /* What is on air is the go to, and nothing else: the service's own rows are not
         drawn, and no picker row wears the pill (FR-007, FR-017). */
      renderBlock(state);
      paintGotoTransport(state);
      pickBody.querySelectorAll('.onscreen').forEach(function (pill) { pill.hidden = true; });
      /* The service's rows are not drawn, so none of them is marked as on air (FR-017). */
      entryList.querySelectorAll('[aria-current="true"]').forEach(function (row) {
        row.setAttribute('aria-current', 'false');
      });
      runNote.hidden = true;
      return;
    }
    renderBlock(state);

    var activeEntry = live ? entryOfScreen(state.screen) : -1;
    if (activeEntry >= 0 && isDivider(dock.entries[activeEntry])) activeEntry = -1;

    /* A crossing travels as ONE motion: the old block closes and the new one opens
       on a single 230 ms curve, and the arriving row's place on screen rides that
       same curve into the middle. No instant jump, no second phase to wait for. */
    var crossing = live && activeEntry >= 0 && activeEntry !== dock.lastEntry;
    var departingLi = crossing ? entryList.querySelector('.entryli[data-live="true"]') : null;
    var arrivingLi = crossing ? entryList.querySelector('.entryli[data-index="' + activeEntry + '"]') : null;
    var departingInner = departingLi ? departingLi.querySelector('.entryinner') : null;
    var arrivingInner = arrivingLi ? arrivingLi.querySelector('.entryinner') : null;
    var arrivingRow = crossing
      ? (entryList.querySelector('.screenerow[data-screen="' + state.screen + '"]') ||
         (arrivingLi && arrivingLi.querySelector('.entryrow')))
      : null;
    var morphing = !!(departingInner && arrivingInner && arrivingInner !== departingInner &&
                      arrivingRow && departingInner.classList.contains('is-open'));
    if (morphing) startMorph(departingInner, arrivingInner, arrivingRow);

    entryList.querySelectorAll('.entryli').forEach(function (li) {
      var index = Number(li.dataset.index);
      var current = live && index === activeEntry;
      li.dataset.live = current ? 'true' : 'false';
      var row = li.querySelector('.entryrow');
      if (row) row.setAttribute('aria-current', current ? 'true' : 'false');
      var inner = li.querySelector('.entryinner');
      if (inner && !(morphing && (inner === departingInner || inner === arrivingInner))) {
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

    var at = dock.stops.indexOf(live ? state.screen : -1);
    prevBtn.disabled = !live || at <= 0;
    nextBtn.disabled = !live || at < 0 || at >= dock.stops.length - 1;

    if (!morphing) {
      /* Closing a block can shorten the list below the current position; clamp in
         this same frame so a glide starts from a position that really exists. */
      runBody.scrollTop = Math.min(runBody.scrollTop,
                                   Math.max(0, runBody.scrollHeight - runBody.clientHeight));
    }

    updateChip(live, activeEntry);
    renderBaits(live, activeEntry);
    updateBand();
    if (live && !morphing) scheduleCenter();       /* the morph brings its own curve */
    dock.lastEntry = live ? activeEntry : null;
  }

  /* ---------- controls ------------------------------------------------------- */

  pickBody.addEventListener('click', function (event) {
    var row = event.target.closest('.servicerow');
    if (!row) return;
    setPickCursor(pickRows().indexOf(row), false);
    openService(Number(row.dataset.service), row.dataset.name, row.dataset.date);
  });

  entryList.addEventListener('click', function (event) {
    if (gotoBusy) return;                    /* nothing changes what is on air */
    var band = event.target.closest('.nextband');
    if (band) {
      projectScreen(Number(band.dataset.screen));
      focusPanel();
      return;
    }
    var screenRow = event.target.closest('.screenerow');
    if (screenRow) {
      projectScreen(Number(screenRow.dataset.screen));
      focusPanel();
      return;
    }
    var row = event.target.closest('.entryrow');
    if (!row) return;
    var entry = dock.entries[Number(row.dataset.index)];
    if (!entry || isDivider(entry)) return;
    projectScreen(entry.start);
    focusPanel();
  });

  baitChips.addEventListener('click', function (event) {
    if (gotoBusy) return;
    var chip = event.target.closest('.bait');
    if (!chip) return;
    if (gkpsDisplay.read().goto) gkpsDisplay.stepGoto(Number(chip.dataset.screen));
    else projectScreen(Number(chip.dataset.screen));
    focusPanel();
  });

  offBack.addEventListener('click', function () {
    gkpsDisplay.back();
    focusPanel();
  });

  offBody.addEventListener('click', function (event) {
    var row = event.target.closest('.offrow');
    if (!row) return;
    gkpsDisplay.stepGoto(Number(row.dataset.pos));
    focusPanel();
  });

  function flipEdition() {
    var editions = (transChip.dataset.editions || '').split(',').filter(Boolean);
    if (!editions.length) return;
    var index = editions.indexOf(transChip.textContent);
    gkpsDisplay.flip(editions[(index + 1) % editions.length] || null);
  }

  blankBtn.addEventListener('click', function () {
    if (gotoBusy) return;
    var state = gkpsDisplay.read();
    /* A go to standing with no service is still something to hide and resume
       (FR-003), so the browsed service is only needed when there is nothing else. */
    if (dock.service == null && !state.goto) return;
    if (state.service === dock.service || state.service == null) {
      if (state.on) gkpsDisplay.hide();           /* Hide words: the place is kept */
      /* Resume in place — and `screen()` would end a go to, which a resume must not. */
      else if (state.goto) gkpsDisplay.resume();
      else gkpsDisplay.screen(state.screen);      /* resume where it was paused */
    } else {
      gkpsDisplay.show(dock.service, 0);          /* display from the start */
    }
    focusPanel();
  });

  findBtn.addEventListener('click', function () { openFind(); });
  findScrim.addEventListener('pointerdown', function (event) {
    event.preventDefault();
    closeFind();
  });
  findResult.addEventListener('click', function () { chooseFind(find.choice); });
  findInput.addEventListener('input', refreshFind);
  findInput.addEventListener('keydown', function (event) {
    var key = event.key;
    if (key === 'Escape') { event.preventDefault(); event.stopPropagation(); closeFind(); return; }
    if (key === 'ArrowDown' || key === 'ArrowUp') {
      event.preventDefault(); event.stopPropagation();
      if (!find.rows.length) return;
      find.choice = (find.choice + (key === 'ArrowDown' ? 1 : -1) + find.rows.length)
        % find.rows.length;
      paintFind();
      return;
    }
    if (key === 'Enter') { event.preventDefault(); event.stopPropagation(); chooseFind(find.choice); return; }
    if (key === 'Backspace' && !findInput.value) {
      event.preventDefault(); event.stopPropagation(); closeFind();
    }
  });
  /* The library is injected on the first open and its index is fetched then; this is
     where the band learns that the query can finally be answered. */
  document.addEventListener('projector-library:ready', function () {
    /* A chapter or book step asked for before the index arrived replays here. */
    if (pendingStep) {
      var step = pendingStep;
      pendingStep = null;
      passageStep(step.action, step.level);
    }
    if (!find.open || find.status === 'ready') return;
    find.status = 'ready';
    findInput.disabled = false;
    refreshFind();
    try { findInput.focus({preventScroll: true}); } catch (e) { findInput.focus(); }
  });
  window.addEventListener('resize', measureBand);

  transChip.addEventListener('click', function () { if (gotoBusy) return; flipEdition(); focusPanel(); });
  prevBtn.addEventListener('click', function () { if (gotoBusy) return; step(-1); focusPanel(); });
  nextBtn.addEventListener('click', function () { if (gotoBusy) return; step(1); focusPanel(); });
  switchBtn.addEventListener('click', function () { setView('pick', true); });
  reloadBtn.addEventListener('click', function () { window.location.reload(); });

  /* ---------- the shortcut sheet (K) ----------------------------------------- */

  /* A layer, not a view: it opens over whichever view is showing, lists the dock's own
     keys, and while it is up nothing behind it acts (FR-007). The picker's own two keys
     ride with the view, so the runner's sheet never offers a key it does not have
     (FR-008). */
  var keysOpen = false;
  var keysheet = document.getElementById('keysheet');
  var keysScrim = document.getElementById('keysScrim');
  var keysSheetClose = document.getElementById('keysClose');

  function applyKeysGroup() {
    if (!keysheet) return;
    keysheet.querySelectorAll('.ksgroup[data-keys="pick"]').forEach(function (group) {
      group.hidden = panel.dataset.view !== 'pick';
    });
  }

  function setKeysOpen(open) {
    if (!keysheet || keysOpen === open) return;
    if (open) { closeFind(); cancelEscapeHold(); }
    keysOpen = open;
    keysheet.hidden = !open;
    keysheet.setAttribute('aria-hidden', open ? 'false' : 'true');
    root.classList.toggle('keys-open', open);
    if (open) {
      applyKeysGroup();
      void keysheet.offsetWidth;                  /* restart the entry animation */
      keysheet.classList.add('is-on');
    } else {
      keysheet.classList.remove('is-on');
      focusPanel();
    }
  }

  if (keysSheetClose) keysSheetClose.addEventListener('click', function () {
    setKeysOpen(false);
  });
  if (keysScrim) keysScrim.addEventListener('pointerdown', function (event) {
    event.preventDefault();
    setKeysOpen(false);
  });

  /* ---------- keyboard (the dock owns it) ------------------------------------ */

  /* The held `Esc` (FR-001): the same gesture the projector uses to leave fullscreen,
     and the same 900 ms, but a release before it cancels the whole thing — the dock's
     own rule, which the projector's timer does not need. */
  var escapeHold = null;

  function cancelEscapeHold() {
    if (escapeHold == null) return;
    window.clearTimeout(escapeHold);
    escapeHold = null;
  }

  function startEscapeHold() {
    cancelEscapeHold();
    escapeHold = window.setTimeout(function () {
      escapeHold = null;
      if (find.open || keysOpen) return;
      if (panel.dataset.view === 'run') setView('pick', true);
    }, 900);
  }

  function unitAt() {
    var state = gkpsDisplay.read();
    var live = state.service === dock.service;
    var index = live ? state.screen : 0;
    var entryIndex = entryOfScreen(index);
    return {index: index, entryIndex: entryIndex,
            entry: entryIndex >= 0 ? dock.entries[entryIndex] : null};
  }

  function baitIndexOf(entry, index) {
    var baits = entry.baits || [];
    for (var i = 0; i < baits.length; i++) {
      if (index >= baits[i].start && index <= baits[i].end) return i;
    }
    return -1;
  }

  /* The projector's own boundary arithmetic (projector.js `unitBoundary`): a plain
     Home / End takes the unit on show, `Shift` its first or last bait, and
     `Ctrl`/`⌘` the service's first or last entry. The plain chord never reaches the
     service's own ends — that is what the modifier is for (FR-012). */
  function unitBoundary(last, modifier, at) {
    if (modifier === 'entry') {
      var entries = contentEntries();
      if (entries.length) projectScreen(entries[last ? entries.length - 1 : 0].start);
      return;
    }
    var entry = at.entry;
    if (!entry || isDivider(entry)) return;      /* between entries: nothing moves */
    if (entry.type === 'song' && (entry.baits || []).length) {
      var baits = entry.baits;
      var bait = baits[modifier === 'bait'
        ? (last ? baits.length - 1 : 0)
        : Math.max(0, baitIndexOf(entry, at.index))];
      if (bait) {
        projectScreen(last && modifier !== 'bait'
          ? Math.max(bait.start, bait.end - 1) : bait.start);
      }
      return;
    }
    /* A text entry has no bait to take, so `Shift` falls through to the entry's own
       ends — exactly the projector's `unitBoundary` (FR-012), so one chord lands on one
       screen on both surfaces. */
    var screen = dock.screens[entry.end];
    projectScreen(last
      ? Math.max(entry.start, entry.end - (screen && screen.blank ? 1 : 0))
      : entry.start);
  }

  /* ---------- the go to's own units (FR-005, FR-009) ------------------------- */

  /* Raised while the go to's content or a crossing is in flight: every key and every
     pointer action that could change what is on air is refused until it settles. */
  var gotoBusy = false;
  var pendingStep = null;

  function setGotoBusy(on) {
    gotoBusy = on;
    panel.dataset.gotoBusy = on ? 'true' : 'false';
    if (dock.goto) offLabel.textContent = gotoLabelOf(gkpsDisplay.read());
  }

  function passageStep(action, level) {
    var state = gkpsDisplay.read();
    var goto = state.goto;
    if (!goto || goto.kind !== 'passage') return false;
    var payload = shown.payload;
    if (!payload || payload.kind !== 'passage') return false;
    /* A chapter or book step reads the index; the band is not the only way in, so the
       first such step loads the module and replays itself when it arrives. */
    if (!window.GKPSProjectorLibrary || !window.GKPSProjectorLibrary.ready()) {
      pendingStep = {action: action, level: level};
      ensureLibrary();
      return false;
    }
    var current = {book_id: goto.book_id, chapter: goto.chapter, verse: goto.verse,
                   translation: goto.translation, editions: payload.editions || {}};
    var moved = window.GKPSProjectorLibrary.movePassage(current, action, level);
    if (!moved) return false;
    if (moved.detour) { gkpsDisplay.stepGoto(moved.detour.verse); return true; }
    if (gotoBusy) return false;
    setGotoBusy(true);
    window.GKPSProjectorLibrary.fetchChapter(moved.request.book_id, moved.request.chapter,
      moved.request.verse, moved.request.edition).then(function (data) {
        if (!data) return;
        /* The block paints from this same payload: one request per crossing, never two
           (FR-005) — the fetch the step already made becomes the block's own. */
        shown.key = gotoKey({kind: 'passage', book_id: data.book_id, chapter: data.chapter});
        shown.payload = {kind: 'passage', label: data.label, editions: data.editions || {}};
        shown.loading = false;
        gkpsDisplay.goTo({kind: 'passage', book_id: data.book_id, chapter: data.chapter,
                          verse: data.verse, translation: data.translation});
      }).catch(function () {
        runNote.hidden = false;
        runNote.textContent = 'The go to could not be loaded.';
      }).then(function () { setGotoBusy(false); });
    return true;
  }

  /* Home / End inside a go to: the projector's own `gotoBoundary`. */
  function gotoBoundary(last, modifier) {
    var state = gkpsDisplay.read();
    var goto = state.goto;
    if (!goto) return;
    if (goto.kind === 'passage') {
      passageStep(last ? 'last' : 'first',
                  modifier === 'entry' ? 'ctrl' : modifier === 'bait' ? 'shift' : 'plain');
      return;
    }
    if (modifier === 'entry') return;            /* a song has no book to take */
    var payload = shown.payload;
    if (!payload || payload.kind !== 'song') return;
    var baits = payload.baits || [];
    if (!baits.length) return;
    if (modifier === 'bait') {
      gkpsDisplay.stepGoto(last ? baits[baits.length - 1].start : baits[0].start);
      return;
    }
    var at = 0;
    baits.forEach(function (bait, n) {
      if (goto.index >= bait.start && goto.index <= bait.end) at = n;
    });
    var bait = baits[Math.max(0, Math.min(at, baits.length - 1))];
    gkpsDisplay.stepGoto(last ? Math.max(bait.start, bait.end - 1) : bait.start);
  }

  function stepUnit(delta, unit) {
    var state = gkpsDisplay.read();
    if (state.goto) {
      if (state.goto.kind === 'passage') {
        passageStep(delta > 0 ? 'next' : 'previous',
                    unit === 'entry' ? 'ctrl' : unit === 'bait' ? 'shift' : 'plain');
        return;
      }
      if (unit === 'entry') return;              /* a song has no book to take */
      if (unit === 'bait' && shown.payload && shown.payload.kind === 'song') {
        var target = pickBaitTarget(shown.payload, state.goto.index, delta, false);
        if (target != null) gkpsDisplay.stepGoto(target);
        return;
      }
      stepGoto(delta);
      return;
    }
    var at = unitAt();
    if (unit === 'entry') {
      var entries = contentEntries();
      if (!entries.length) return;
      var here = -1;
      for (var i = 0; i < entries.length; i++) {
        if (at.index >= entries[i].start && at.index <= entries[i].end) here = i;
      }
      if (here < 0) here = 0;
      var next = Math.max(0, Math.min(entries.length - 1, here + delta));
      if (next !== here) projectScreen(entries[next].start);
      return;
    }
    if (unit === 'bait' && at.entry && (at.entry.baits || []).length) {
      var baits = at.entry.baits;
      var bait = Math.max(0, baitIndexOf(at.entry, at.index));
      bait = Math.max(0, Math.min(baits.length - 1, bait + delta));
      projectScreen(baits[bait].start);
      return;
    }
    step(delta);
  }

  function edgeOf(unit, end) {
    unitBoundary(end, unit, unitAt());
  }

  panel.addEventListener('keydown', function (event) {
    if (event.altKey) return;
    var key = event.key;
    var shift = event.shiftKey;
    var ctrl = event.ctrlKey || event.metaKey;
    /* The sheet is a layer: it owns the Esc and the `K`, and nothing behind it acts. */
    if (keysOpen) {
      if (key === 'Escape' || key === 'k' || key === 'K') {
        event.preventDefault();
        setKeysOpen(false);
      }
      return;
    }
    /* While the band is open it owns the keys: the covered dock acts on nothing. */
    if (find.open) {
      if (key === 'Escape') { event.preventDefault(); closeFind(); }
      return;
    }
    /* A hold, not a tap: a press released before 900 ms moves nothing (FR-001). */
    if (key === 'Escape') {
      event.preventDefault();
      if (panel.dataset.view === 'run' && !event.repeat) startEscapeHold();
      return;
    }
    if ((key === 'k' || key === 'K') && !ctrl && !shift) {
      event.preventDefault();
      setKeysOpen(true);
      return;
    }
    if (panel.dataset.view === 'pick') {
      var rows = pickRows();
      if (!rows.length) return;
      /* Only the two arrows move the mark (FR-006); the rest of the pad is inert here. */
      if (key === 'ArrowDown' || key === 'ArrowUp') {
        event.preventDefault();
        var step0 = key === 'ArrowDown' ? 1 : -1;
        setPickCursor((dock.pickIndex < 0 ? (step0 > 0 ? -1 : 0) : dock.pickIndex) + step0, true);
        return;
      }
      if (key === 'Enter') {
        event.preventDefault();
        openCursorRow();
        return;
      }
      if ((key === 'g' || key === 'G') && !ctrl && !shift) {
        event.preventDefault();
        openFind();
        return;
      }
      return;                                    /* the picker has no other keys */
    }
    if (panel.dataset.view !== 'run') return;
    if (gotoBusy) return;                        /* nothing changes what is on air */
    if (ctrl && (key === 'PageUp' || key === 'PageDown')) return;   /* the browser's tabs */
    if ((key === 'g' || key === 'G') && !ctrl) { event.preventDefault(); openFind(); return; }
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

  panel.addEventListener('keyup', function (event) {
    if (event.key === 'Escape') cancelEscapeHold();
  });
  window.addEventListener('blur', cancelEscapeHold);
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { cancelEscapeHold(); return; }
    if (find.open) parkFocus();                  /* the band keeps the keyboard (FR-015) */
  });

  /* A click must leave the focus where the keyboard lives, not on the clicked
     button: otherwise Space would re-press the last thing clicked. The panel is the
     only focusable thing here, so a click on the page AROUND it would leave focus on
     <body> and kill every shortcut while the transport — which tracks the window's
     focus — still reads armed. Park focus again for those too. */
  /* The focus belongs to whoever is taking the keys: the band's field while it is open
     and usable, the panel otherwise (FR-015). A window that comes back from another app
     re-parks it, because the dock's own panel is not what the operator is typing into. */
  function parkFocus() {
    if (find.open && !findInput.disabled) {
      try { findInput.focus({preventScroll: true}); return; } catch (e) { /* fall through */ }
    }
    focusPanel();
  }

  panel.addEventListener('pointerdown', parkFocus);

  document.addEventListener('pointerdown', function (event) {
    if (panel.contains(event.target)) return;
    window.requestAnimationFrame(parkFocus);
  }, true);

  document.addEventListener('focusin', function (event) {
    if (panel.contains(event.target)) return;
    window.requestAnimationFrame(parkFocus);
  });


  /* The transport arrows fill while this window holds the keyboard. */
  function markFocus() {
    root.classList.add('win-focus');
    if (find.open) parkFocus();
  }
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
  if (pickRows().length) setPickCursor(0, false);

  /* A refresh lands where the operator already is (FR-016): the service on air opens
     in the runner — or, when the go to stands alone, the runner holding its block.
     Nothing on air leaves the picker, and a service this picker does not list cannot
     be opened, so the dock stays put rather than guess. */
  (function resumeOnAir() {
    var state = gkpsDisplay.read();
    if (state.goto && state.service == null) { setView('run', false); return; }
    if (state.service == null) return;
    var row = pickRows().filter(function (candidate) {
      return Number(candidate.dataset.service) === Number(state.service);
    })[0];
    if (!row) return;
    openService(Number(row.dataset.service), row.dataset.name, row.dataset.date);
  })();

  focusPanel();
})();
