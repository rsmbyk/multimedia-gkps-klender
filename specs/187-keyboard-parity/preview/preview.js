/* The Go To in the dock — preview driver (spec 185).
 *
 * The list, the rows and the inner blocks are the product's own builders, copied
 * from static/web/obs-dock.js (entryRowContent, screenRow, buildInner, bandText and
 * their helpers) so the runner is the runner, not a redrawing of it. What this file
 * adds is only what the slice proposes: the find band, the off-service strip, the
 * transport acting on the goto, and the harness that reaches each state.
 *
 * The lookup is NOT copied: the page loads static/web/projector-library.js and
 * answers its one index request from the capture, so the grammar and the labels are
 * the product's.
 */
(function () {
  'use strict';

  var PV = window.__PV;
  var service = PV.service;
  var SONGS = PV.songs;
  var CHAPTER = PV.chapter;

  var entryList = document.getElementById('entryList');
  var runBody = document.getElementById('runBody');
  var runNote = document.getElementById('runNote');
  var blankBtn = document.getElementById('blankBtn');
  var switchBtn = document.getElementById('switchBtn');
  var findBtn = document.getElementById('findBtn');
  var offBlock = document.getElementById('offBlock');
  var offStrip = document.getElementById('offStrip');
  var offBody = document.getElementById('offBody');
  var offLabel = document.getElementById('offLabel');
  var offBack = document.getElementById('offBack');
  var transportRow = document.getElementById('transportRow');
  var findBand = document.getElementById('findBand');
  var findInput = document.getElementById('findInput');
  var findCount = document.getElementById('findCount');
  var findResult = document.getElementById('findResult');
  var findLabel = document.getElementById('findLabel');
  var findScrim = document.getElementById('findScrim');
  var bandSwap = document.getElementById('bandSwap');
  var prevBtn = document.getElementById('prevBtn');
  var nextBtn = document.getElementById('nextBtn');
  var transChip = document.getElementById('transChip');
  var baitStrip = document.getElementById('baitStrip');
  var baitChips = document.getElementById('baitChips');
  var pvRead = document.getElementById('pvRead');
  var pvNote = document.getElementById('pvNote');
  var frame = document.getElementById('pvFrame');
  var dockPanel = document.getElementById('dockPanel');
  var viewPick = document.getElementById('viewPick');
  var viewRun = document.getElementById('viewRun');
  var runService = document.getElementById('runService');
  var runDate = document.getElementById('runDate');
  var keysheet = document.getElementById('keysheet');
  var keysScrim = document.getElementById('keysScrim');
  var keysClose = document.getElementById('keysClose');
  var keysBody = document.getElementById('keysBody');

  var entries = service.entries;
  var screens = service.screens;

  var st = {
    screen: 12,           /* the service's own place, the value Back restores */
    on: true,
    goto: null,           /* {kind:'song', payload, index} | {kind:'passage', verse, translation} */
    find: {open: false, query: '', choice: 0, rows: [], loading: false, failed: false},
    keys: false,
    alone: false,         /* the go to stands with no service: the slice's new state */
    state: 'rest'
  };

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  /* ---------- the product's builders (copied from obs-dock.js) ---------------- */

  function entryLabel(entry) {
    var label = String(entry.label || '').trim();
    if (label) return label;
    if (entry.type === 'break') return 'Section break';
    if (entry.type === 'song') return 'Song';
    return 'Text';
  }

  function songParts(entry) {
    var label = String(entry.label || '').trim();
    var match = label.match(/^([A-Za-z]{2,6}\s*\d+[A-Za-z]?)\s*(?:[:—–-]\s*|\s+)(.+)$/);
    if (match) return {reference: match[1].trim(), title: match[2].trim()};
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
    for (var i = entry.start; i <= entry.end; i++) {
      var screen = screens[i];
      if (!screen || screen.blank) continue;
      var lines = screenLines(screen);
      if (lines.length) return lines.slice(0, 2);
    }
    return [];
  }

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

  var MEDIA_KINDS = [
    ['image_sha256', 'Image'], ['video_sha256', 'Video'], ['audio_sha256', 'Audio'],
    ['pdf_sha256', 'PDF'], ['slides_sha256', 'Slides']
  ];

  function mediaLabel(screen) {
    for (var i = 0; i < MEDIA_KINDS.length; i++) {
      if (screen[MEDIA_KINDS[i][0]]) return MEDIA_KINDS[i][1];
    }
    return '';
  }

  function screenRow(index) {
    var screen = screens[index];
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
    if (entry.type === 'break') return null;
    var inner = el('div', 'entryinner');
    inner.setAttribute('aria-hidden', 'true');
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

  function renderList() {
    entryList.replaceChildren();
    entries.forEach(function (entry, index) {
      var item = el('li', 'entryli');
      item.dataset.index = String(index);
      item.appendChild(entryRowContent(entry, index));
      var inner = buildInner(entry);
      if (inner) item.appendChild(inner);
      entryList.appendChild(item);
    });
  }

  /* ---------- what the goto names ------------------------------------------- */

  /* The go to as a list block: its own screens under its pinned label row. */
  var builtKey = '';

  function gotoKey() {
    if (!st.goto) return '';
    var suffix = st.goto.loading ? ':loading' : '';
    return (st.goto.kind === 'song' ? 'song:' + st.goto.payload.id
                                    : 'passage:' + st.goto.translation) + suffix;
  }

  function buildGotoBlock() {
    var key = gotoKey();
    if (key === builtKey) return;
    builtKey = key;
    offBody.replaceChildren();
    if (!st.goto) return;
    if (st.goto.loading) return;            /* the fetch in flight: the header says so */
    if (st.goto.kind === 'song') {
      st.goto.payload.baits.forEach(function (bait) {
        offBody.appendChild(el('div', 'baithead', 'Bait ' + bait.number));
        for (var i = bait.start; i <= bait.end; i++) {
          var screen = st.goto.payload.screens[i];
          if (!screen) continue;
          var row = el('button', 'screenerow' + (screen.blank ? ' screenerow--rest' : ''));
          row.type = 'button';
          row.tabIndex = -1;
          row.dataset.pos = String(i);
          row.setAttribute('aria-current', 'false');
          if (screen.blank) {
            row.textContent = 'Rest';
          } else {
            var wrap = el('span', 'screenerow__t--lines');
            screenLines(screen).forEach(function (text) {
              wrap.appendChild(el('span', 'screenerow__line', text));
            });
            row.appendChild(wrap);
          }
          offBody.appendChild(row);
        }
      });
      return;
    }
    var verses = (CHAPTER.editions[st.goto.translation] || CHAPTER.editions.TB).verses;
    verses.forEach(function (verse) {
      var row = el('button', 'screenerow');
      row.type = 'button';
      row.tabIndex = -1;
      row.dataset.pos = String(verse.n);
      row.setAttribute('aria-current', 'false');
      var wrap = el('span', 'screenerow__t--lines');
      wrap.appendChild(el('span', 'screenerow__line', verse.n + '. ' + String(verse.text || '').trim()));
      row.appendChild(wrap);
      offBody.appendChild(row);
    });
  }

  var centredAt = '';

  function markGotoRows() {
    var pos = !st.goto ? null : (st.goto.kind === 'song' ? st.goto.index : st.goto.verse);
    var current = null;
    offBody.querySelectorAll('[data-pos]').forEach(function (row) {
      var on = pos != null && Number(row.dataset.pos) === pos;
      row.setAttribute('aria-current', on ? 'true' : 'false');
      if (on) current = row;
    });
    if (!current || centredAt === gotoKey() + ':' + pos) return;
    centredAt = gotoKey() + ':' + pos;
    var target = current.offsetTop - (runBody.clientHeight - current.offsetHeight) / 2;
    var max = runBody.scrollHeight - runBody.clientHeight;
    runBody.scrollTop = Math.max(0, Math.min(target, max));
  }

  function gotoLabel() {
    if (!st.goto) return '';
    if (st.goto.loading) return 'Loading…';
    if (st.goto.kind === 'song') return st.goto.payload.label;
    return 'Matius ' + CHAPTER.chapter + ':' + st.goto.verse;
  }

  function gotoBounds() {
    if (!st.goto || st.goto.loading) return [0, 0];
    if (st.goto.kind === 'song') return [0, st.goto.payload.screens.length - 1];
    var verses = (CHAPTER.editions[st.goto.translation] || CHAPTER.editions.TB).verses;
    return [verses[0].n, verses[verses.length - 1].n];
  }

  function stepGoto(delta) {
    if (!st.goto) return;
    if (st.goto.kind === 'song') {
      var last = st.goto.payload.screens.length - 1;
      st.goto.index = Math.max(0, Math.min(st.goto.index + delta, last));
    } else {
      var bounds = gotoBounds();
      st.goto.verse = Math.max(bounds[0], Math.min(st.goto.verse + delta, bounds[1]));
    }
    apply();
  }

  function stepBait(delta) {
    if (!st.goto || st.goto.kind !== 'song') return;
    var baits = st.goto.payload.baits;
    var at = 0;
    baits.forEach(function (bait, i) { if (st.goto.index >= bait.start) at = i; });
    var target = baits[Math.max(0, Math.min(at + delta, baits.length - 1))];
    st.goto.index = target.start;
    apply();
  }

  function flip() {
    if (!st.goto || st.goto.kind !== 'passage') return;
    st.goto.translation = st.goto.translation === 'TB' ? 'SIM' : 'TB';
    apply();
  }

  function back() {
    if (!st.goto) return;
    st.goto = null;
    builtKey = '';
    centredAt = '';
    st.state = 'rest';
    apply();
    var live = entryList.querySelector('.screenerow[aria-current="true"]');
    if (live) {
      var target = live.offsetTop - (runBody.clientHeight - live.offsetHeight) / 2;
      runBody.scrollTop = Math.max(0, Math.min(target, runBody.scrollHeight - runBody.clientHeight));
    }
  }

  /* ---------- the find band -------------------------------------------------- */

  function libReady() {
    return !!(window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.ready());
  }

  function showScrim() {
    findScrim.hidden = false;
    window.requestAnimationFrame(function () { findScrim.classList.add('is-on'); });
  }

  function hideScrim() {
    findScrim.classList.remove('is-on');
    window.setTimeout(function () { if (!st.find.open) findScrim.hidden = true; }, 170);
  }

  function openFind() {
    st.find.open = true;
    st.find.query = '';
    st.find.choice = 0;
    st.find.rows = [];
    st.find.failed = false;
    st.find.loading = !libReady();
    findInput.value = '';
    st.state = st.find.loading ? 'loading' : 'find';
    showScrim();
    apply();
    if (libReady()) refreshFind();
    else window.GKPSProjectorLibrary.load().then(function () { st.find.loading = false; apply(); });
    try { findInput.focus(); } catch (e) { /* the frame may not take focus */ }
  }

  function closeFind() {
    st.find.open = false;
    hideScrim();
    st.find.rows = [];
    st.find.query = '';
    st.find.failed = false;
    st.state = st.goto ? (st.on ? 'song' : 'hidden') : 'rest';
    apply();
  }

  /* ---------- the shortcut sheet (the slice's proposal) ---------------------- */

  var keysHideTimer = null;

  /* The picker has keys of its own (the list's arrows, Enter) that mean nothing
     once a service is open, so its group rides with the view. */
  function applyKeysGroup() {
    var group = keysBody.querySelector('[data-keys="pick"]');
    if (group) group.hidden = dockPanel.dataset.view !== 'pick';
  }

  function setView(name) {
    dockPanel.dataset.view = name;
    viewPick.classList.toggle('is-active', name === 'pick');
    viewRun.classList.toggle('is-active', name === 'run');
    applyKeysGroup();
  }

  function openKeys() {
    if (st.find.open) return;              /* the band owns the keys while it is open */
    st.keys = true;
    window.clearTimeout(keysHideTimer);
    keysheet.hidden = false;
    keysBody.scrollTop = 0;
    applyKeysGroup();
    window.requestAnimationFrame(function () { keysheet.classList.add('is-on'); });
    st.state = 'keys';
    readout();
  }

  function closeKeys() {
    if (!st.keys) return;
    st.keys = false;
    keysheet.classList.remove('is-on');
    window.clearTimeout(keysHideTimer);
    keysHideTimer = window.setTimeout(function () {
      if (!st.keys) keysheet.hidden = true;
    }, 180);
    st.state = st.goto ? (st.on ? 'song' : 'hidden') : 'rest';
    apply();
  }

  function refreshFind() {
    st.find.rows = window.GKPSProjectorLibrary
      ? window.GKPSProjectorLibrary.lookup(findInput.value.trim()) : [];
    st.find.query = findInput.value.trim();
    st.find.choice = 0;
    st.find.failed = false;
    st.state = 'find';
    apply();
  }

  function paintFind() {
    var row = st.find.rows[st.find.choice] || null;
    findResult.disabled = !row;
    findResult.dataset.match = row ? 'true' : 'false';
    findLabel.textContent = '';
    if (st.find.loading) {
      findLabel.textContent = 'Loading search…';
    } else if (!st.find.query) {
      findLabel.textContent = 'Start typing to find a match';
    } else if (st.find.failed) {
      findLabel.textContent = 'Could not load — try again';
    } else if (!row) {
      findLabel.textContent = 'No matching passage or song';
    } else {
      findLabel.textContent = row.label;
      if (row.editionSuffix) {
        findLabel.appendChild(el('span', 'findresult__edition', ' · ' + row.editionSuffix));
      }
    }
    findCount.textContent = st.find.rows.length ? (st.find.choice + 1) + ' / ' + st.find.rows.length : '0 / 0';
    findInput.disabled = !!st.find.loading;
  }

  function choose() {
    var row = st.find.rows[st.find.choice];
    if (!row) return;
    if (row.kind === 'song') {
      var payload = SONGS[String(row.target.song_id)];
      if (!payload) { st.find.failed = true; paintFind(); return; }
      st.goto = {kind: 'song', payload: payload, index: 0};
    } else {
      if (Number(row.target.book_id) !== 40 || Number(row.target.chapter) !== Number(CHAPTER.chapter)) {
        st.find.failed = true;
        paintFind();
        return;
      }
      st.goto = {kind: 'passage', verse: Number(row.target.verse || 1),
                 translation: row.target.edition || 'TB'};
    }
    st.find.open = false;
    hideScrim();
    st.find.rows = [];
    st.on = true;
    st.state = 'song';
    apply();
  }

  /* ---------- apply --------------------------------------------------------- */

  function apply() {
    offBlock.hidden = !st.goto;
    entryList.hidden = !!st.goto;          /* the service's rows are not drawn while a go to is up */
    offBody.hidden = !st.goto;
    offLabel.textContent = gotoLabel();
    buildGotoBlock();
    markGotoRows();

    /* The head names what the dock is showing: a service when one is browsed, the mode
       when the go to stands alone and there is no service to name (the block below it
       carries the go to's own name, so the head does not repeat it). */
    dockPanel.classList.toggle('is-alone', !!st.alone);
    runService.textContent = st.alone ? 'Go To' : 'Ibadah Minggu';
    runDate.textContent = '4 Oktober 2026';

    bandSwap.classList.toggle('is-find', !!st.find.open);
    transportRow.inert = !!st.find.open;
    findBand.inert = !st.find.open;
    findBand.setAttribute('aria-hidden', st.find.open ? 'false' : 'true');
    if (st.find.open) paintFind();

    var modeFind = st.find.open && !st.find.loading;
    findBtn.setAttribute('aria-pressed', st.find.open ? 'true' : 'false');

    /* A go to is not the service: switching services under it would leave the state
       naming a service the operator never chose. Back first — and a go to that stands
       alone has no service to lose, so its switch control stays usable. */
    switchBtn.disabled = !!st.goto && !st.alone;

    blankBtn.setAttribute('aria-pressed', st.on ? 'false' : 'true');
    var eyeLabel = st.goto ? (st.on ? 'Hide words' : 'Show words')
                           : (st.on ? 'Hide words' : 'Display this service');
    blankBtn.title = eyeLabel;
    blankBtn.setAttribute('aria-label', eyeLabel);

    /* the service's own place: expanded, never marked as on air while a goto is up */
    var liveEntry = -1;
    entries.forEach(function (entry, index) {
      if (st.screen >= entry.start && st.screen <= entry.end) liveEntry = index;
    });
    entryList.querySelectorAll('.entryli').forEach(function (li) {
      var index = Number(li.dataset.index);
      var current = !st.goto && index === liveEntry;
      li.dataset.live = current ? 'true' : 'false';
      var row = li.querySelector('.entryrow');
      if (row) row.setAttribute('aria-current', current ? 'true' : 'false');
      var inner = li.querySelector('.entryinner');
      if (inner) {
        var open = index === liveEntry;
        inner.classList.toggle('is-open', open);
        inner.setAttribute('aria-hidden', open ? 'false' : 'true');
      }
      li.querySelectorAll('.screenerow').forEach(function (screenRow) {
        screenRow.setAttribute('aria-current',
          current && Number(screenRow.dataset.screen) === st.screen ? 'true' : 'false');
      });
    });

    /* transport: what is on air owns it */
    var song = st.goto && st.goto.kind === 'song' ? st.goto.payload : null;
    var passage = st.goto && st.goto.kind === 'passage' && !st.goto.loading;
    var editions = Object.keys(CHAPTER.editions);
    transChip.hidden = !passage;
    if (passage) {
      transChip.textContent = st.goto.translation;
      transChip.dataset.editions = editions.join(',');
      transChip.setAttribute('aria-pressed', 'false');
    }
    baitStrip.hidden = !song;
    baitChips.replaceChildren();
    if (song) {
      song.baits.forEach(function (bait) {
        var chip = el('button', 'bait', String(bait.number));
        chip.type = 'button';
        chip.tabIndex = -1;
        var current = st.goto.index >= bait.start && st.goto.index <= bait.end;
        chip.setAttribute('aria-pressed', current ? 'true' : 'false');
        chip.dataset.start = String(bait.start);
        baitChips.appendChild(chip);
      });
    }
    var bounds = st.goto ? gotoBounds() : [0, 0];
    var pos = st.goto ? (song ? st.goto.index : st.goto.verse) : 0;
    prevBtn.disabled = !st.goto || !!st.goto.loading || pos <= bounds[0];
    nextBtn.disabled = !st.goto || !!st.goto.loading || pos >= bounds[1];

    runNote.hidden = true;
    readout();
  }

  /* ---------- the readout --------------------------------------------------- */

  function box(node) {
    if (!node || node.hidden) return null;
    var r = node.getBoundingClientRect();
    var f = getComputedStyle(node);
    return {x: +(r.x - frame.getBoundingClientRect().x).toFixed(1),
            y: +(r.y - frame.getBoundingClientRect().y).toFixed(1),
            w: +r.width.toFixed(1), h: +r.height.toFixed(1),
            font: f.fontSize + '/' + f.fontWeight, color: f.color};
  }

  function readout() {
    var pick = dockPanel.dataset.view === 'pick';
    var lines = [];
    lines.push('<b>view</b> ' + (pick ? 'picker' : 'runner'));
    lines.push('<b>state</b> ' + (st.goto ? (st.goto.kind + (st.on ? '' : ' · hidden')) : 'service')
      + (st.find.open ? ' · find open' : '') + (st.keys ? ' · sheet open' : '')
      + (st.alone ? ' · alone' : ''));
    if (pick) {
      var pickHead = box(viewPick.querySelector('.dock__head'));
      var pickBody = box(viewPick.querySelector('.dock__body'));
      var pickRows = viewPick.querySelectorAll('.servicerow');
      lines.push('<b>head</b> ' + (pickHead ? pickHead.w + '×' + pickHead.h : '—'));
      lines.push('<b>services</b> ' + pickRows.length + ' · list '
        + (pickBody ? pickBody.w + '×' + pickBody.h : '—'));
    } else {
      lines.push('<b>head</b> ' + (runService.textContent || '—') + ' · date '
        + (getComputedStyle(runDate).display === 'none' ? 'hidden' : 'shown'));
      var strip = box(offStrip);
      lines.push('<b>strip</b> ' + (strip ? strip.w + '×' + strip.h + ' @ ' + strip.x + ',' + strip.y
        + ' · ' + strip.font : '—'));
      var band = box(findBand);
      lines.push('<b>band</b> ' + (band ? band.w + '×' + band.h + ' @ ' + band.x + ',' + band.y : '—'));
      var field = box(findInput);
      lines.push('<b>field</b> ' + (field ? field.w + '×' + field.h + ' · ' + field.font : '—'));
      var row = box(findResult);
      lines.push('<b>result</b> ' + (row ? row.w + '×' + row.h + ' · ' + row.font : '—'));
      var chip = box(transChip);
      var baits = box(baitStrip);
      lines.push('<b>transport</b> chip ' + (chip ? chip.w + '×' + chip.h : '—')
        + ' · baits ' + (baits ? baits.w + '×' + baits.h : '—'));
      var liveRow = entryList.querySelector('.entryrow[aria-current="true"]');
      var liveBox = box(liveRow);
      lines.push('<b>live row</b> ' + (liveBox ? liveBox.w + '×' + liveBox.h : 'none'));
      lines.push('<b>eye</b> ' + blankBtn.title);
    }

    var panel = document.querySelector('.keysheet__panel');
    var panelBox = keysheet.hidden ? null : box(panel);
    lines.push('<b>sheet</b> ' + (panelBox ? panelBox.w + '×' + panelBox.h + ' @ '
      + panelBox.x + ',' + panelBox.y : 'closed'));
    var rows = [].filter.call(keysBody.querySelectorAll('.krow'), function (n) {
      return n.getClientRects().length;
    });
    if (!keysheet.hidden && rows.length) {
      var firstRow = box(rows[0]);
      var lastRow = box(rows[rows.length - 1]);
      lines.push('<b>rows</b> ' + rows.length + ' · ' + firstRow.w + '×' + firstRow.h
        + ' · last y ' + lastRow.y + ' · body ' + keysBody.clientHeight + '/'
        + keysBody.scrollHeight);
    }
    reportToParent();
    pvRead.innerHTML = lines.join('<br>');
  }

  /* ---------- the harness --------------------------------------------------- */

  var buttons = document.querySelectorAll('.pv-bar [data-state]');
  function setState(name) {
    st.goto = null;
    builtKey = '';
    centredAt = '';
    st.find.open = false;
    hideScrim();
    st.find.loading = false;
    st.find.failed = false;
    st.on = true;
    st.alone = false;
    st.keys = false;
    window.clearTimeout(keysHideTimer);
    keysheet.classList.remove('is-on');
    keysheet.hidden = true;
    st.state = name;
    findInput.value = '';
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.state === name ? 'true' : 'false'); });

    setView(name === 'pick' || name === 'pickkeys' ? 'pick' : 'run');
    if (name === 'pick') { readout(); return; }
    if (name === 'pickkeys') { openKeys(); return; }

    if (name === 'rest') { st.screen = 12; }
    if (name === 'find' || name === 'nomatch') {
      openFind();
      findInput.value = name === 'find' ? 'NKB 4' : 'zzzz';
      st.find.loading = false;
      if (libReady()) refreshFind(); else {
        window.GKPSProjectorLibrary.load().then(refreshFind);
      }
      return;
    }
    if (name === 'loading') {
      st.find.open = true;
      st.find.loading = true;
      showScrim();
      st.find.query = '';
      findResult.disabled = true;
      apply();
      return;
    }
    if (name === 'song' || name === 'hidden') {
      st.goto = {kind: 'song', payload: SONGS['1434'], index: 0};
      st.on = name !== 'hidden';
    }
    if (name === 'passage') {
      st.goto = {kind: 'passage', verse: 3, translation: 'TB'};
    }
    if (name === 'alone') {
      /* the owner's ruling: a go to started on the picker stands with no service */
      st.goto = {kind: 'song', payload: SONGS['1434'], index: 0};
      st.alone = true;
    }
    if (name === 'fetching') {
      /* a chapter step in flight: the go to keeps its header, and no rows yet */
      st.goto = {kind: 'passage', verse: 3, translation: 'TB', loading: true};
      st.alone = true;
    }
    if (name === 'keys') {
      st.screen = 12;
      apply();
      openKeys();
      return;
    }
    apply();
  }

  buttons.forEach(function (button) {
    button.addEventListener('click', function () { setState(button.dataset.state); });
  });

  document.querySelectorAll('.pv-bar [data-width]').forEach(function (button) {
    button.addEventListener('click', function () {
      frame.style.width = button.dataset.width + 'px';
      document.querySelectorAll('.pv-bar [data-width]').forEach(function (other) {
        other.setAttribute('aria-pressed', other === button ? 'true' : 'false');
      });
      readout();
    });
  });

  document.querySelectorAll('.pv-bar [data-height]').forEach(function (button) {
    button.addEventListener('click', function () {
      frame.style.height = button.dataset.height + 'px';
      document.querySelectorAll('.pv-bar [data-height]').forEach(function (other) {
        other.setAttribute('aria-pressed', other === button ? 'true' : 'false');
      });
      readout();
    });
  });

  document.querySelectorAll('.pv-bar [data-theme]').forEach(function (button) {
    button.addEventListener('click', function () {
      var mode = button.dataset.theme;
      document.documentElement.dataset.theme = mode;
      document.documentElement.dataset.themeMode = mode;
      document.querySelectorAll('.pv-bar [data-theme]').forEach(function (other) {
        other.setAttribute('aria-pressed', other === button ? 'true' : 'false');
      });
    });
  });

  findInput.addEventListener('input', function () {
    if (!libReady()) return;
    refreshFind();
  });
  findInput.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') { event.preventDefault(); closeFind(); return; }
    if (event.key === 'Backspace' && !findInput.value) {
      event.preventDefault(); closeFind(); return;     /* the projector's own rule */
    }
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      if (!st.find.rows.length) return;
      st.find.choice = (st.find.choice + (event.key === 'ArrowDown' ? 1 : -1) + st.find.rows.length)
        % st.find.rows.length;
      paintFind();
      return;
    }
    if (event.key === 'Enter') { event.preventDefault(); choose(); }
  });
  findResult.addEventListener('click', choose);
  findScrim.addEventListener('click', closeFind);
  keysScrim.addEventListener('click', closeKeys);
  keysClose.addEventListener('click', closeKeys);
  findBtn.addEventListener('click', function () {
    if (st.find.open) closeFind(); else openFind();
  });
  offBack.addEventListener('click', back);
  offBody.addEventListener('click', function (event) {
    var row = event.target.closest('[data-pos]');
    if (!row || !st.goto) return;
    if (st.goto.kind === 'song') st.goto.index = Number(row.dataset.pos);
    else st.goto.verse = Number(row.dataset.pos);
    apply();
  });

  document.addEventListener('keydown', function (event) {
    /* The sync page drives its own steps with the arrows; there the dock takes no
       page-level keys. */
    if (document.body.classList.contains('sv')) return;
    /* The sheet is a layer: K and Esc close it, and every other key is inert. */
    if (st.keys) {
      if (event.key === 'Escape' || event.key === 'k' || event.key === 'K') {
        event.preventDefault();
        closeKeys();
      }
      return;
    }
    if (event.key === 'k' || event.key === 'K') {
      if (st.find.open) return;
      event.preventDefault();
      openKeys();
      return;
    }
    if (event.key === 'Escape' && st.find.open) { closeFind(); return; }
    if (event.key === 'g' || event.key === 'G') {
      if (st.find.open) return;
      event.preventDefault();
      openFind();
      return;
    }
    if (!st.goto || st.find.open) return;
    if (event.key === 'ArrowDown' || event.key === 'ArrowRight') { event.preventDefault(); stepGoto(1); }
    if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') { event.preventDefault(); stepGoto(-1); }
    if (event.key === 't' || event.key === 'T') flip();
    if (event.key === ' ') { event.preventDefault(); st.on = !st.on; apply(); }
  });

  prevBtn.addEventListener('click', function () { stepGoto(-1); });
  nextBtn.addEventListener('click', function () { stepGoto(1); });
  transChip.addEventListener('click', flip);
  baitChips.addEventListener('click', function (event) {
    var chip = event.target.closest('.bait');
    if (!chip) return;
    st.goto.index = Number(chip.dataset.start);
    apply();
  });
  blankBtn.addEventListener('click', function () { st.on = !st.on; apply(); });
  switchBtn.addEventListener('click', function () {
    if (!switchBtn.disabled) document.getElementById('pvNote').textContent =
      'Switch service is the dock’s own view change; the preview shows the runner only.';
  });

  /* ---------- the sync page's remote control (preview only) ------------------ */

  function pvState(state, view) {
    st.goto = null;
    builtKey = '';
    centredAt = '';
    hideScrim();
    st.find.open = false;
    st.screen = Number(state.screen) || 0;
    st.on = state.on !== false;
    if (state.goto && state.goto.kind === 'song' && SONGS[String(state.goto.song_id)]) {
      st.goto = {kind: 'song', payload: SONGS[String(state.goto.song_id)],
                 index: Number(state.goto.index) || 0};
    }
    if (state.goto && state.goto.kind === 'passage') {
      st.goto = {kind: 'passage', verse: Number(state.goto.verse) || 1,
                 translation: state.goto.translation || 'TB'};
    }
    if (st.goto) st.state = 'song';
    apply();
    if (view === 'find') openFind();
  }

  window.addEventListener('message', function (event) {
    var message = event.data || {};
    if (message.type === 'pv-go') pvState(message.state || {}, message.view || 'rest');
  });

  function reportToParent() {
    /* Inside the sync page: to that page itself (it may in turn be an srcdoc frame, but
       the dock's report still belongs to it). Standalone in a frame: to the host. */
    var sink = document.body.classList.contains('sv') || window.parent === window
      ? window : window.parent;
    var liveLabel = entryList.querySelector('.entryrow[aria-current="true"] .entryrow__t');
    var text = st.goto
      ? 'go to · ' + gotoLabel() + (st.goto.kind === 'passage' ? ' · ' + st.goto.translation : '')
      : 'service · ' + (liveLabel ? liveLabel.textContent.trim().slice(0, 48) : 'screen ' + st.screen);
    if (st.find.open) text = 'find band open · ' + text;
    sink.postMessage({type: 'pv-rendered', surface: 'dock', text: text}, '*');
  }

  pvNote.textContent = 'The runner, its rows and its inner blocks are the product\'s, drawn by the '
    + 'product\'s own builders from the live service 142. The lookup is the product\'s module '
    + '(projector-library.js) over a captured index; the word "NKB 43" and "Matius 5" carry content '
    + 'here, and any other result shows the product\'s own "could not load" row because a static '
    + 'page cannot fetch. The find band and the off-service strip are the proposal.';

  renderList();
  setState('rest');
  /* The two band rows' own heights, for the swap's transition. */
  document.documentElement.style.setProperty('--transport-h', transportRow.scrollHeight + 'px');
  document.documentElement.style.setProperty('--band-h', findBand.scrollHeight + 'px');
})();
