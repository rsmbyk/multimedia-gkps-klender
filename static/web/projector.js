/* The service projector (specs 006 and 091).
 *
 * One service screen at a time, with quiet corner controls for keyboard or mouse.
 * The page arrives with every service screen rendered, so ordinary steps are instant.
 *
 * It shares the display state with the app's tabs over the same channel (see
 * web/display.js): whatever the operator does here, the shell hears. Update re-reads
 * the whole page -- how a song whose lyrics changed reaches the screen -- and the
 * screen that was showing stays where it was. Spec 026: the shell asks for that same
 * re-read after every saved change, so the screen follows an edit without a press.
 */
(function () {
  'use strict';

  var body = document.body;
  var channelName = body.dataset.displayChannel || 'gkps-service-display';
  var service = Number(body.dataset.service);
  if (!service) {
    var offlinePath = window.location.pathname.match(/^\/obs\/service\/(\d+)\/$/);
    if (offlinePath) service = Number(offlinePath[1]);
    body.dataset.service = String(service);
  }
  var screen = document.getElementById('projectorScreen');
  var stage = document.getElementById('projectorScreens');
  var entries = JSON.parse(document.getElementById('projectorEntryData').textContent) || [];
  var screenData = JSON.parse(document.getElementById('projectorScreenData').textContent) || [];
  var savedScreensSignature = JSON.stringify(screenData);
  var KEY = 'gkps-display';

  var channel = null;
  try { channel = new BroadcastChannel(channelName); } catch (e) { channel = null; }

  var current = Number(body.dataset.currentScreen || 0);
  var showing = body.dataset.showing === 'true';

  function screens() {
    return [].slice.call(stage.querySelectorAll('.screen[data-screen]'));
  }
  function read() {
    try {
      var stored = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (stored && typeof stored === 'object') return stored;
    } catch (e) { /* no stored state */ }
    return null;
  }
  function write(state) {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
  }
  function post(message) {
    if (channel) channel.postMessage(message);
  }

  /* ---------- the beat -------------------------------------------------------
     A window can be closed while the app stays open, and the browser gives the opener
     no "closed" event -- only the handle it holds. So this window keeps announcing
     itself: a stamp in localStorage (which every tab of the browser shares) and a
     message on the channel, every couple of seconds. A shell that sees the stamps stop
     takes the display down. A hidden tab is throttled to roughly one timer a minute,
     which is why the shell waits far longer than this interval before deciding the
     window is gone. */
  var BEAT_KEY = 'gkps-display-beat';

  function beat() {
    try { localStorage.setItem(BEAT_KEY, String(Date.now())); } catch (e) { /* private mode */ }
    post({type: 'beat', service: service, on: showing});
  }

  /* ---------- fitting the words to the accepted projector stage ------------ */
  var GOLDEN_RATIO = (1 + Math.sqrt(5)) / 2;

  function overflows(head, lines) {
    if (head && (head.scrollWidth > stage.clientWidth + 1
                 || head.getBoundingClientRect().bottom > stage.getBoundingClientRect().bottom)) return true;
    if (!lines) return false;
    if (lines.scrollHeight > lines.clientHeight + 1) return true;
    var range = document.createRange();
    range.selectNodeContents(lines);
    var ink = range.getBoundingClientRect();
    var box = lines.getBoundingClientRect();
    var stageBox = stage.getBoundingClientRect();
    return ink.left < box.left - 1 || ink.right > box.right + 1
      || ink.top < box.top - 2 || ink.bottom > box.bottom + 2
      || ink.top < stageBox.top - 1 || ink.bottom > stageBox.bottom + 1;
  }

  function truncateText(head, lines) {
    if (!lines || !overflows(head, lines)) return;
    var rows = [].slice.call(lines.querySelectorAll('.screen__line'));
    while (rows.length > 1 && overflows(head, lines)) rows.pop().remove();
    var last = lines.querySelector('.screen__line:last-child');
    if (!last) return;
    while (last.textContent.length && overflows(head, lines)) {
      last.textContent = last.textContent.slice(0, -1);
    }
    last.textContent = last.textContent.replace(/\s+$/, '') + '\u2026';
  }

  function fit(active) {
    if (!active) return;
    var head = active.querySelector('.screen__head');
    var lines = active.querySelector('.screen__lines');
    if (!lines) return;
    for (var size = 200; size >= 2; size -= 1) {
      lines.style.fontSize = size + 'px';
      if (head) head.style.fontSize = (size / GOLDEN_RATIO) + 'px';
      if (!overflows(head, lines)) break;
    }
    if (active.dataset.fit === 'single') truncateText(head, lines);
  }

  /* ---------- showing ------------------------------------------------------- */

  function render(silent) {
    var all = screens();
    if (current < 0) current = 0;
    if (all.length && current > all.length - 1) current = all.length - 1;
    var active = all[current] || null;
    var previous = all[previousIndex] || null;
    var moved = previous && previous !== active;

    all.forEach(function (each) {
      var on = each === active && !detour;
      each.classList.toggle('is-active', on);
      /* Both morph classes are cleared every time: a quick move back and forth would
         otherwise leave the arriving screen carrying "leaving" as well, and the
         leaving animation is the one that would win. */
      each.classList.remove('is-in');
      each.classList.remove('is-out');
      each.setAttribute('aria-hidden', on ? 'false' : 'true');
    });

    if (moved) {
      /* A quiet morph: the one that goes fades out the way the new one came from. */
      stage.dataset.move = direction >= 0 ? 'next' : 'prev';
      previous.classList.add('is-out');
      if (active) active.classList.add('is-in');
      window.setTimeout(function () { previous.classList.remove('is-out'); }, 260);
    }

    previousIndex = current;
    body.dataset.currentScreen = String(current);
    body.dataset.showing = showing ? 'true' : 'false';
    body.classList.toggle('words-hidden', !showing);
    if (active && !detour) {
      applyPassageTranslation(active);
      fit(active);
    }
    renderCue();
    if (!silent) {
      write({service: service, screen: current, on: showing});
      post(showing ? {type: 'show', service: service, screen: current} : {type: 'stop'});
    }
    beat();          /* every change is also a sign of life */
  }

  var direction = 1;
  var previousIndex = current;

  function move(step) {
    if (detour) { detourStep(step, 'plain'); return; }
    var next = current + step;
    if (next < 0 || next > screens().length - 1) return;
    direction = step;
    if (entryAt(next) !== entryAt(current)) translation = '';
    current = next;
    showing = true;
    render();
  }

  /* ---------- quiet HUD and shared input operations ------------------------ */
  var cue = document.getElementById('corner-cue');
  var cueService = document.getElementById('cue-service');
  var cuePrefix = document.getElementById('cue-prefix');
  var baitList = document.getElementById('cue-baits');
  var cueProgress = document.getElementById('cue-progress');
  var cueNext = document.getElementById('cue-next');
  var cueArrow = document.getElementById('cue-arrow');
  var cueNextName = document.getElementById('cue-next-name');
  var keysButton = document.querySelector('.keys');
  var entryList = document.getElementById('entry-list');
  var entryDismiss = document.getElementById('entry-list-dismiss');
  var entryListSearch = document.getElementById('entry-list-search');
  var entryListClear = document.getElementById('entry-list-clear');
  var entryListResults = document.getElementById('entry-list-results');
  var entryListMatches = [];
  var entryListChoice = 0;
  var findPanel = document.getElementById('projectorFind');
  var findDismiss = document.getElementById('projectorFindDismiss');
  var findInput = document.getElementById('projectorFindInput');
  var findClear = document.getElementById('projectorFindClear');
  var findResults = document.getElementById('projectorFindResults');
  var findSuggestion = findResults.querySelector('.projector-find__suggestion');
  var findCount = findResults.querySelector('.projector-find__count');
  var translation = '';
  var translationTimer;
  var findKind = '';
  var findRows = [];
  var findChoice = 0;
  var detour = null;
  var returnScreen = null;
  var runningCueLabels = [];

  function clearRunningCueLabels() {
    runningCueLabels.forEach(function (node) { if (node.stopRun) node.stopRun(); });
    runningCueLabels = [];
    cue.classList.remove('cue--fit-text');
    delete cue.dataset.runningLimit;
    cueNextName.classList.remove('cue-running');
    delete cueNextName.dataset.fullText;
    cueNextName.onpointerenter = null;
    cueNextName.onpointerleave = null;
    cueNextName.style.width = '';
  }
  function makeRunningCueLabel(node, full) {
    node.classList.add('cue-running');
    node.dataset.fullText = full;
    var still = document.createElement('span');
    still.className = 'cue-running__still';
    var moving = document.createElement('span');
    moving.className = 'cue-running__moving';
    moving.textContent = full;
    node.replaceChildren(still, moving);
    var animation;
    node.stopRun = function () {
      if (animation) animation.cancel();
      animation = null;
      node.classList.remove('is-running');
      node.style.width = '';
    };
    node.onpointerenter = function () {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      node.stopRun();
      node.style.width = node.getBoundingClientRect().width + 'px';
      node.classList.add('is-running');
      var distance = Math.max(0, moving.scrollWidth - node.clientWidth);
      if (!distance) { node.stopRun(); return; }
      animation = moving.animate([
        {transform: 'translateX(0)'},
        {transform: 'translateX(0)', offset: .1},
        {transform: 'translateX(-' + distance + 'px)', offset: .9},
        {transform: 'translateX(-' + distance + 'px)'}
      ], {duration: Math.max(4000, distance / 45 * 1000), easing: 'linear', iterations: Infinity});
    };
    node.onpointerleave = node.stopRun;
    runningCueLabels.push(node);
  }
  function fitRunningCueLabels() {
    if (!runningCueLabels.length) return;
    runningCueLabels.forEach(function (node) { node.stopRun(); });
    cue.classList.add('cue--fit-text');
    function applyLimit(limit) {
      runningCueLabels.forEach(function (node) {
        var characters = Array.from(node.dataset.fullText);
        node.querySelector('.cue-running__still').textContent = characters.length > limit
          ? characters.slice(0, limit).join('') + '…' : node.dataset.fullText;
      });
    }
    var low = 1, high = 50, chosen = 1;
    while (low <= high) {
      var trial = Math.floor((low + high) / 2);
      applyLimit(trial);
      if (cue.scrollWidth <= cue.clientWidth + 1) { chosen = trial; low = trial + 1; }
      else high = trial - 1;
    }
    applyLimit(chosen);
    cue.dataset.runningLimit = String(chosen);
  }

  function bindSearchClear(input, clear) {
    function sync() { clear.hidden = !input.value; }
    clear.addEventListener('click', function (event) {
      event.stopPropagation();
      input.value = '';
      input.dispatchEvent(new Event('input', {bubbles: true}));
      input.focus();
    });
    ['input', 'change', 'search'].forEach(function (name) { input.addEventListener(name, sync); });
    sync();
    return sync;
  }
  var syncEntryListClear = bindSearchClear(entryListSearch, entryListClear);
  var syncFindClear = bindSearchClear(findInput, findClear);

  function entryAt(index) {
    var active = screens()[index];
    return active ? entries[Number(active.dataset.entry)] : null;
  }
  function entryIndex() {
    var active = screens()[current];
    return active ? Number(active.dataset.entry) : 0;
  }
  function moveTo(index) {
    if (index < 0 || index >= screens().length) return;
    direction = index >= current ? 1 : -1;
    if (entryAt(index) !== entryAt(current)) translation = '';
    current = index;
    showing = true;
    render();
  }
  function moveEntry(offset) {
    if (detour) { if (detour.kind === 'passage') detourStep(offset, 'ctrl'); return; }
    var next = entries[entryIndex() + offset];
    if (next && next.start <= next.end) moveTo(next.start);
  }
  function moveToBait(index) {
    var entry = entryAt(current);
    if (entry && entry.type === 'song' && entry.baits[index]) moveTo(entry.baits[index].start);
  }
  function baitIndex() {
    var entry = entryAt(current);
    if (!entry || !entry.baits.length) return -1;
    return entry.baits.findIndex(function (bait) {
      return current >= bait.start && current <= bait.end;
    });
  }
  function moveBait(offset) {
    if (detour) { detourStep(offset, detour.kind === 'passage' ? 'shift' : 'bait'); return; }
    moveToBait(baitIndex() + offset);
  }
  function unitBoundary(last, modifier) {
    if (detour) { detourBoundary(last, modifier); return; }
    var entry = entryAt(current);
    if (!entry) return;
    if (modifier === 'ctrl') {
      var target = entries[last ? entries.length - 1 : 0];
      if (target) moveTo(target.start);
      return;
    }
    if (entry.type === 'song' && entry.baits.length) {
      var bait = entry.baits[modifier === 'shift' ? (last ? entry.baits.length - 1 : 0) : baitIndex()];
      if (bait) moveTo(last && modifier !== 'shift' ? Math.max(bait.start, bait.end - 1) : bait.start);
      return;
    }
    moveTo(last ? Math.max(entry.start, entry.end - (screenData[entry.end] && screenData[entry.end].blank ? 1 : 0)) : entry.start);
  }
  function toggleWords() { showing = !showing; render(); }
  function applyPassageTranslation(active) {
    var entry = entryAt(current);
    if (!entry || entry.type !== 'passage') return;
    var variant = ((screenData[current] || {}).translations || {})[translation || entry.translation];
    if (!variant || !active.querySelector('.screen__head')) return;
    active.querySelector('.screen__head').textContent = variant.header;
    active.querySelector('.screen__line').textContent = variant.line;
  }

  function renderCue() {
    if (!cue || !entries.length) return;
    clearRunningCueLabels();
    if (detour) { renderDetourCue(); return; }
    var entry = entryAt(current);
    if (!entry) return;
    var data = screenData[current] || {};
    var isRest = Boolean(data.blank);
    var lastBaitRest = entry.type === 'song' && isRest && baitIndex() === entry.baits.length - 1;
    baitList.replaceChildren();
    baitList.hidden = entry.type !== 'song';
    if (entry.type === 'song') {
      entry.baits.forEach(function (bait, index) {
        var key = document.createElement('button');
        key.type = 'button'; key.className = 'cue-bait';
        key.dataset.baitIndex = String(index);
        key.textContent = String(bait.number);
        key.setAttribute('aria-label', 'Go to bait ' + bait.number);
        key.setAttribute('aria-pressed', String(index === (isRest ? baitIndex() + 1 : baitIndex())));
        baitList.appendChild(key);
      });
    }
    cuePrefix.replaceChildren();
    var label = document.createElement(entry.untitled ? 'i' : 'span');
    if (entry.type === 'text' && entry.untitled) makeRunningCueLabel(label, entry.label);
    else label.textContent = entry.label + (entry.type === 'song' || entry.type === 'passage' ? ' ·' : '');
    cuePrefix.appendChild(label);
    if (entry.type === 'passage') {
      var flip = document.createElement('button');
      flip.type = 'button'; flip.className = 'cue-translation';
      flip.textContent = translation || entry.translation;
      flip.setAttribute('aria-label', 'Flip passage translation');
      cuePrefix.appendChild(document.createTextNode(' '));
      cuePrefix.appendChild(flip);
    }
    cueProgress.textContent = !isRest && data.split_total ? data.split + '/' + data.split_total : '';
    cueNext.classList.toggle('on', entry.type === 'break' || (isRest && (entry.type !== 'song' || lastBaitRest)));
    cueArrow.classList.toggle('on', entry.type === 'break' || (isRest && (entry.type !== 'song' || lastBaitRest)));
    var next = entries[entryIndex() + 1];
    cueNext.hidden = !next;
    if (next && next.type === 'text' && next.untitled) makeRunningCueLabel(cueNextName, next.label);
    else cueNextName.textContent = next ? next.label : '';
    cueNext.setAttribute('aria-label', next ? 'Go to next entry: ' + next.label : 'No next entry');
    fitRunningCueLabels();
    renderEntryList();
  }
  function renderEntryList() {
    if (!entryList) return;
    var query = normalize(entryListSearch.value.trim());
    entryListMatches = entries.map(function (entry, index) { return index; }).filter(function (index) {
      var entry = entries[index];
      var searchable = (index + 1) + ' ' + (entry.label || 'Section break') + ' ' +
        (entry.baits.length ? 'Bait ' + entry.baits.map(function (bait) { return bait.number; }).join(', ') : '');
      return normalize(searchable).includes(query);
    });
    if (!entryListMatches.includes(entryListChoice)) entryListChoice = entryListMatches[0];
    entryListResults.replaceChildren();
    entryListMatches.forEach(function (index) {
      var entry = entries[index];
      var row = document.createElement('button');
      row.type = 'button'; row.className = 'entry-list__item';
      row.id = 'entry-list-option-' + index;
      row.setAttribute('role', 'option');
      row.dataset.entryIndex = String(index);
      if (index === entryIndex()) row.setAttribute('aria-current', 'true');
      row.dataset.active = String(index === entryListChoice);
      row.setAttribute('aria-selected', String(index === entryListChoice));
      var number = document.createElement('span');
      number.className = 'entry-list__number'; number.textContent = String(index + 1);
      var title = document.createElement('span'); title.textContent = entry.label || 'Section break';
      if (entry.baits.length) {
        var meta = document.createElement('small'); meta.className = 'entry-list__meta';
        meta.textContent = 'Bait ' + entry.baits.map(function (bait) { return bait.number; }).join(', ');
        title.appendChild(meta);
      }
      row.append(number, title); entryListResults.appendChild(row);
    });
    if (!entryListMatches.length) {
      var empty = document.createElement('div');
      empty.className = 'entry-list__empty'; empty.textContent = 'No matching entries';
      empty.setAttribute('role', 'status');
      entryListResults.appendChild(empty);
    }
    if (entryListChoice == null) entryListSearch.removeAttribute('aria-activedescendant');
    else entryListSearch.setAttribute('aria-activedescendant', 'entry-list-option-' + entryListChoice);
  }
  function scrollEntryListChoice() {
    var selected = entryList.querySelector('[data-active="true"]');
    if (!selected) return;
    var position = entryListMatches.indexOf(entryListChoice);
    if (position === entryListMatches.length - 1) entryList.scrollTop = entryList.scrollHeight;
    else if (position === 0) entryList.scrollTop = 0;
    else {
      var header = entryList.querySelector('.entry-list__header').getBoundingClientRect();
      var row = selected.getBoundingClientRect();
      var visibleHeight = entryList.clientHeight - header.height;
      entryList.scrollTop += row.top - header.bottom - (visibleHeight - row.height) / 2;
    }
  }
  function flashTranslationLabel() {
    window.clearTimeout(translationTimer);
    var flip = cuePrefix.querySelector('.cue-translation');
    if (!flip) return;
    flip.classList.add('flash');
    translationTimer = window.setTimeout(function () { flip.classList.remove('flash'); }, 1000);
  }
  function flipTranslation() {
    if (detour && detour.kind === 'passage') {
      var alternate = detour.translation === 'TB' ? 'SIM' : 'TB';
      if (!detour.translations[alternate]) return;
      detour.translation = alternate;
      renderDetour();
      flashTranslationLabel();
      return;
    }
    var entry = entryAt(current);
    if (!entry || entry.type !== 'passage') return;
    var translations = (screenData[current] || {}).translations || {};
    var currentTranslation = translation || entry.translation;
    var target = currentTranslation === 'TB' ? 'SIM' : 'TB';
    if (!translations[target]) return;
    translation = target;
    var active = screens()[current];
    active.querySelector('.screen__head').textContent = translations[target].header;
    active.querySelector('.screen__line').textContent = translations[target].line;
    renderCue(); fit(active);
    flashTranslationLabel();
  }
  var layerCloseMs = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 180;
  var keysCloseTimer, entryCloseTimer, findCloseTimer;
  function setKeysOpen(open) {
    if (open) setEntryListOpen(false);
    if (open) {
      window.clearTimeout(keysCloseTimer);
      body.classList.remove('keys-closing');
      body.classList.add('keys-open');
    } else if (body.classList.contains('keys-open')) {
      keysButton.blur();
      window.clearTimeout(keysCloseTimer);
      body.classList.remove('keys-open');
      body.classList.add('keys-closing');
      keysCloseTimer = window.setTimeout(function () {
        body.classList.remove('keys-closing');
        cue.inert = false;
        revealControls();
      }, layerCloseMs);
    }
    keysButton.setAttribute('aria-expanded', String(open));
    cue.inert = open || body.classList.contains('keys-closing');
    revealControls();
  }
  function setEntryListOpen(open) {
    if (open && body.classList.contains('keys-open')) return;
    if (open) {
      entryListSearch.value = '';
      syncEntryListClear();
      entryListChoice = entryIndex();
      renderEntryList();
      window.clearTimeout(entryCloseTimer);
      body.classList.remove('entry-list-closing');
      body.classList.add('entry-list-open');
      entryList.hidden = false;
      entryList.inert = false;
      entryDismiss.hidden = true;
      window.requestAnimationFrame(function () {
        if (body.classList.contains('entry-list-open')) entryDismiss.hidden = false;
      });
      entryListSearch.focus();
    } else if (body.classList.contains('entry-list-open')) {
      entryListSearch.blur();
      cueService.blur();
      window.clearTimeout(entryCloseTimer);
      body.classList.remove('entry-list-open');
      body.classList.add('entry-list-closing');
      entryList.inert = true;
      entryCloseTimer = window.setTimeout(function () {
        body.classList.remove('entry-list-closing');
        entryList.hidden = true;
        entryDismiss.hidden = true;
        revealControls();
      }, layerCloseMs);
    }
    cueService.setAttribute('aria-expanded', String(open));
    revealControls();
    if (open) scrollEntryListChoice();
  }
  var cursorTimer, controlsTimer;
  function revealCursor() {
    body.classList.remove('cursor-hidden');
    window.clearTimeout(cursorTimer);
    cursorTimer = window.setTimeout(function () { body.classList.add('cursor-hidden'); }, 2000);
  }
  function revealControls() {
    window.clearTimeout(controlsTimer);
    if (body.classList.contains('corner-hidden')) return;
    body.classList.remove('controls-idle');
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open') ||
        body.classList.contains('keys-closing') || body.classList.contains('entry-list-closing') ||
        body.classList.contains('find-open') || body.classList.contains('find-closing')) return;
    controlsTimer = window.setTimeout(function () { body.classList.add('controls-idle'); }, 30000);
  }
  ['pointermove', 'pointerdown', 'click'].forEach(function (name) {
    document.addEventListener(name, revealCursor, {passive: true});
  });
  ['pointermove', 'pointerdown', 'click', 'keydown'].forEach(function (name) {
    document.addEventListener(name, revealControls, {passive: true});
  });
  revealCursor(); revealControls();

  keysButton.addEventListener('click', function (event) {
    event.stopPropagation(); setKeysOpen(!body.classList.contains('keys-open'));
  });
  cueService.addEventListener('click', function (event) {
    event.stopPropagation(); setEntryListOpen(!body.classList.contains('entry-list-open'));
  });
  entryDismiss.addEventListener('click', function (event) {
    event.stopPropagation(); setEntryListOpen(false);
  });
  function chooseEntryList(index) {
    if (!entries[index]) return;
    leaveDetour(); moveTo(entries[index].start);
    setEntryListOpen(false);
  }
  entryListSearch.addEventListener('input', function () {
    entryListChoice = undefined;
    renderEntryList();
    scrollEntryListChoice();
  });
  entryListSearch.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' || (event.key === 'Backspace' && !entryListSearch.value)) {
      event.preventDefault(); event.stopPropagation(); setEntryListOpen(false);
    } else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault(); event.stopPropagation();
      if (!entryListMatches.length) return;
      var position = entryListMatches.indexOf(entryListChoice);
      entryListChoice = entryListMatches[(position + (event.key === 'ArrowDown' ? 1 : -1) + entryListMatches.length) % entryListMatches.length];
      renderEntryList();
      scrollEntryListChoice();
    } else if (event.key === 'Enter') {
      event.preventDefault(); event.stopPropagation(); chooseEntryList(entryListChoice);
    }
  });
  entryList.addEventListener('click', function (event) {
    var row = event.target.closest('.entry-list__item');
    if (!row) return;
    event.stopPropagation(); chooseEntryList(Number(row.dataset.entryIndex));
  });
  cueNext.addEventListener('click', function (event) {
    event.stopPropagation();
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open')) return;
    if (detour) leaveDetour(); else moveEntry(1);
  });
  baitList.addEventListener('click', function (event) {
    var bait = event.target.closest('.cue-bait');
    if (!bait) return;
    event.stopPropagation();
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open')) return;
    if (detour && detour.kind === 'song') {
      detour.index = detour.baits[Number(bait.dataset.baitIndex)].start; renderDetour();
    } else moveToBait(Number(bait.dataset.baitIndex));
  });
  cuePrefix.addEventListener('click', function (event) {
    if (!event.target.closest('.cue-translation')) return;
    event.stopPropagation(); if (!body.classList.contains('keys-open') && !body.classList.contains('entry-list-open')) flipTranslation();
  });
  document.addEventListener('click', function (event) {
    if (body.classList.contains('keys-closing') || body.classList.contains('entry-list-closing') ||
        body.classList.contains('find-closing')) return;
    if (body.classList.contains('keys-open')) {
      if (!event.target.closest('.sheet') && !event.target.closest('.keys')) setKeysOpen(false);
      return;
    }
    if (body.classList.contains('entry-list-open')) {
      if (!event.target.closest('.entry-list')) setEntryListOpen(false);
      return;
    }
    if (!findPanel.hidden) return;
    var zone = event.target.closest('.mouse-zone');
    if (!zone) return;
    if (!document.fullscreenElement && !fullscreenDenied && document.fullscreenEnabled &&
        document.documentElement.requestFullscreen) {
      enterFullscreen();
      return; // This click belongs only to entering fullscreen.
    }
    if (zone.dataset.mouseAction === 'previous') move(-1);
    else if (zone.dataset.mouseAction === 'next') move(1);
    else toggleWords();
  });

  // In windowed mode, any click on the projected page is reserved for the
  // fullscreen gesture. Capture it before the mouse zones can navigate.
  document.addEventListener('click', function (event) {
    if (document.fullscreenElement || fullscreenDenied || !document.fullscreenEnabled ||
        !document.documentElement.requestFullscreen) return;
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open') ||
        body.classList.contains('keys-closing') || body.classList.contains('entry-list-closing') ||
        !findPanel.hidden) return;
    if (!event.target.closest('#projectorScreen, .mouse-zones')) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    enterFullscreen();
  }, true);

  /* ---------- find and temporary library detours ---------------------------- */
  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  }
  function findUrl(path, params) {
    return window.location.pathname + path + '?' + new URLSearchParams(params).toString();
  }
  function openFind(kind) {
    if (kind === 'j') { setEntryListOpen(true); return; }
    window.clearTimeout(findCloseTimer);
    body.classList.remove('find-closing');
    findKind = kind; findChoice = 0;
    findInput.value = '';
    syncFindClear();
    findPanel.hidden = false;
    findPanel.inert = false;
    findDismiss.hidden = false;
    body.classList.add('find-open');
    revealControls();
    refreshFind();
    findInput.focus();
  }
  function closeFind() {
    if (!body.classList.contains('find-open')) return;
    ++lookupSequence;
    findInput.blur();
    findDismiss.blur();
    body.classList.remove('find-open');
    body.classList.add('find-closing');
    findPanel.inert = true;
    findKind = ''; findRows = [];
    window.clearTimeout(findCloseTimer);
    findCloseTimer = window.setTimeout(function () {
      body.classList.remove('find-closing');
      findPanel.hidden = true;
      findDismiss.hidden = true;
      revealControls();
    }, layerCloseMs);
    revealControls();
  }
  findDismiss.addEventListener('click', function (event) {
    event.stopPropagation(); closeFind();
  });
  var lookupSequence = 0;
  function refreshFind() {
    ++lookupSequence;
    var query = normalize(findInput.value.trim());
    findRows = []; findChoice = 0; paintFind();
    if (query && window.GKPSProjectorLibrary) {
      findRows = window.GKPSProjectorLibrary.lookup(findInput.value.trim());
      paintFind();
    }
  }
  function paintFind() {
    findResults.disabled = !findRows.length;
    findSuggestion.textContent = '';
    if (findRows.length) {
      var row = findRows[findChoice];
      findSuggestion.appendChild(document.createTextNode(row.label));
      if (row.editionSuffix) {
        var suffix = document.createElement('span');
        suffix.className = 'projector-find__edition';
        suffix.textContent = ' · ' + row.editionSuffix;
        findSuggestion.appendChild(suffix);
      }
    } else {
      findSuggestion.textContent = findInput.value.trim()
        ? 'No matching passage or song' : 'Start typing to find a match';
    }
    findCount.textContent = findRows.length ? (findChoice + 1) + ' / ' + findRows.length : '0 / 0';
  }
  function chooseFind(index) {
    var row = findRows[index];
    if (!row) return;
    openDetour(row);
    closeFind();
  }
  findInput.addEventListener('input', refreshFind);
  document.addEventListener('projector-library:ready', function () {
    if (!findPanel.hidden && findInput.value.trim()) refreshFind();
  });
  findInput.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); closeFind(); }
    else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault(); event.stopPropagation();
      if (findRows.length) findChoice = (findChoice + (event.key === 'ArrowDown' ? 1 : -1) + findRows.length) % findRows.length;
      paintFind();
    } else if (event.key === 'Enter') {
      event.preventDefault(); event.stopPropagation(); chooseFind(findChoice);
    } else if (event.key === 'Backspace' && !findInput.value) {
      event.preventDefault(); event.stopPropagation(); closeFind();
    }
  });
  findResults.addEventListener('click', function () { chooseFind(findChoice); });

  var detourNode = document.createElement('section');
  detourNode.className = 'screen projector-detour';
  detourNode.innerHTML = '<h1 class="screen__head"></h1><div class="screen__lines"></div>';
  stage.appendChild(detourNode);
  function leaveDetour() {
    if (!detour) return;
    detour = null;
    detourNode.classList.remove('is-active');
    if (returnScreen != null) current = returnScreen;
    returnScreen = null;
    showing = true;
    render();
  }
  function openDetour(row) {
    var data = window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.detour(row);
    if (!data) return;
    if (!detour) returnScreen = current;
    detour = data;
    detour.index = 0;
    showing = true;
    renderDetour();
  }
  function requestPassage(action, level) {
    if (!detour || detour.kind !== 'passage') return;
    var data = window.GKPSProjectorLibrary
      && window.GKPSProjectorLibrary.movePassage(detour, action, level);
    if (data) { detour = data; renderDetour(); }
  }
  function detourStep(step, level) {
    if (detour.kind === 'passage') { requestPassage(step > 0 ? 'next' : 'previous', level); return; }
    if (level === 'ctrl') return;
    if (level === 'bait') {
      var currentBait = detour.baits.findIndex(function (bait) {
        return detour.index >= bait.start && detour.index <= bait.end;
      });
      var target = detour.baits[currentBait + step];
      if (target) detour.index = target.start;
    } else detour.index = Math.max(0, Math.min(detour.index + step, detour.screens.length - 1));
    renderDetour();
  }
  function detourBoundary(last, level) {
    if (detour.kind === 'passage') { requestPassage(last ? 'last' : 'first', level); return; }
    if (level === 'ctrl') return;
    if (level === 'shift') detour.index = detour.baits[last ? detour.baits.length - 1 : 0].start;
    else {
      var bait = detour.baits.find(function (item) {
        return detour.index >= item.start && detour.index <= item.end;
      });
      if (bait) detour.index = last ? Math.max(bait.start, bait.end - 1) : bait.start;
    }
    renderDetour();
  }
  function renderDetour() {
    if (!detour) return;
    screens().forEach(function (screen) { screen.classList.remove('is-active'); });
    var data = detour.kind === 'passage' ? detour.translations[detour.translation]
      : detour.screens[detour.index];
    var head = detourNode.querySelector('.screen__head');
    var lines = detourNode.querySelector('.screen__lines');
    head.hidden = !data.header;
    head.textContent = data.header || '';
    lines.replaceChildren();
    (data.lines || [{text: data.line || ''}]).forEach(function (line) {
      var p = document.createElement('p'); p.className = 'screen__line'; p.textContent = line.text;
      lines.appendChild(p);
    });
    detourNode.classList.add('is-active');
    body.dataset.showing = 'true';
    fit(detourNode); renderCue();
  }
  function renderDetourCue() {
    var returnEntry = entryAt(returnScreen == null ? current : returnScreen);
    cuePrefix.replaceChildren();
    var label = document.createElement('span');
    label.textContent = detour.label + (detour.kind === 'passage' ? ' · ' : ' ·');
    cuePrefix.appendChild(label);
    if (detour.kind === 'passage') {
      var flip = document.createElement('button'); flip.type = 'button';
      flip.className = 'cue-translation'; flip.textContent = detour.translation;
      flip.setAttribute('aria-label', 'Flip passage translation'); cuePrefix.appendChild(flip);
    }
    baitList.replaceChildren();
    baitList.hidden = detour.kind !== 'song';
    if (detour.kind === 'song') detour.baits.forEach(function (bait, index) {
      var button = document.createElement('button'); button.type = 'button';
      button.className = 'cue-bait'; button.dataset.baitIndex = String(index);
      button.textContent = String(bait.number);
      button.setAttribute('aria-pressed', String(detour.index >= bait.start && detour.index <= bait.end));
      baitList.appendChild(button);
    });
    var screen = detour.kind === 'song' ? detour.screens[detour.index] : null;
    cueProgress.textContent = screen && !screen.blank ? screen.split + '/' + screen.split_total : '';
    cueNext.hidden = false;
    cueNext.classList.remove('on'); cueArrow.classList.remove('on');
    cueNextName.textContent = 'back to ' + (returnEntry ? returnEntry.label : 'service');
    cueNext.setAttribute('aria-label', 'Back to service');
  }

  function closeLayers() {
    if (body.classList.contains('keys-closing') || body.classList.contains('entry-list-closing') ||
        body.classList.contains('find-closing')) return true;
    // Escape changes the browser's focus modality even after a pointer-opened
    // layer. Release its trigger so it does not light up on the mirrored display.
    if (body.classList.contains('keys-open')) {
      setKeysOpen(false); keysButton.blur(); return true;
    }
    if (body.classList.contains('entry-list-open')) {
      setEntryListOpen(false); cueService.blur(); return true;
    }
    if (!findPanel.hidden) { closeFind(); return true; }
    return false;
  }
  document.addEventListener('keydown', function (event) {
    if (event.target === entryListSearch) return;
    if (event.key === 'Escape') {
      if (closeLayers()) { event.preventDefault(); return; }
      if (detour) { event.preventDefault(); leaveDetour(); return; }
      return;
    }
    if (body.classList.contains('find-closing') && event.key.toLowerCase() === 'g' &&
        !event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey) {
      event.preventDefault(); openFind('g'); return;
    }
    if (!findPanel.hidden) return;
    if (!event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.repeat) {
      if (event.key.toLowerCase() === 'k') {
        event.preventDefault(); setKeysOpen(!body.classList.contains('keys-open')); return;
      }
      if (event.key.toLowerCase() === 'f') {
        event.preventDefault();
        if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
        else enterFullscreen();
        return;
      }
    }
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open')) return;
    if (event.altKey || event.metaKey) return;
    var key = event.key.toLowerCase();
    if (!event.ctrlKey && !event.shiftKey && ['j', 'g'].includes(key)) {
      event.preventDefault(); openFind(key); return;
    }
    if (!event.ctrlKey && !event.shiftKey && key === 'c') {
      event.preventDefault();
      var hide = !body.classList.contains('corner-hidden');
      body.classList.toggle('corner-hidden', hide);
      cue.hidden = hide; keysButton.hidden = hide;
      if (!hide) revealControls();
      return;
    }
    if (!event.ctrlKey && !event.shiftKey && key === 't') { event.preventDefault(); flipTranslation(); return; }
    if (!event.ctrlKey && event.key === ' ') { event.preventDefault(); toggleWords(); return; }
    var forward = ['ArrowRight', 'ArrowDown', 'PageDown'].includes(event.key);
    var backward = ['ArrowLeft', 'ArrowUp', 'PageUp'].includes(event.key);
    if (forward || backward) {
      if (event.ctrlKey && (event.key === 'PageUp' || event.key === 'PageDown')) return;
      event.preventDefault();
      if (event.ctrlKey) moveEntry(forward ? 1 : -1);
      else if (event.shiftKey) moveBait(forward ? 1 : -1);
      else move(forward ? 1 : -1);
    } else if (event.key === 'Home' || event.key === 'End') {
      event.preventDefault(); unitBoundary(event.key === 'End', event.ctrlKey ? 'ctrl' : event.shiftKey ? 'shift' : 'plain');
    }
  });

  /* The operator's own gesture asks for the screen, rather than the window grabbing
     it on the way in. Escape from the browser gives it back. */
  function enterFullscreen() {
    if (document.fullscreenElement || !document.documentElement.requestFullscreen) return;
    document.documentElement.requestFullscreen().then(function () {
      if (navigator.keyboard && navigator.keyboard.lock) {
        navigator.keyboard.lock(['Escape']).catch(function () { /* browser retains Escape */ });
      }
    }).catch(function () {
      fullscreenDenied = true;
      syncFullscreenCursor();
    });
  }
  var fullscreenDenied = false;
  function syncFullscreenCursor() {
    body.classList.toggle('is-fullscreen', Boolean(document.fullscreenElement));
    body.classList.toggle('fullscreen-available', Boolean(
      !fullscreenDenied && document.fullscreenEnabled && document.documentElement.requestFullscreen));
  }
  document.addEventListener('fullscreenchange', syncFullscreenCursor);
  syncFullscreenCursor();
  var escapeHoldTimer;
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape' || event.repeat || !document.fullscreenElement) return;
    window.clearTimeout(escapeHoldTimer);
    escapeHoldTimer = window.setTimeout(function () {
      if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
    }, 900);
  });
  document.addEventListener('keyup', function (event) {
    if (event.key === 'Escape') window.clearTimeout(escapeHoldTimer);
  });

  /* ---------- what the other tabs say --------------------------------------- */

  if (channel) {
    channel.addEventListener('message', function (event) {
      var message = event.data || {};
      if (message.type === 'show') {
        /* One Tata Ibadah at a time per browser: a different service takes the
           screen over, so this window steps aside without arguing. */
        if (Number(message.service) !== service) {
          showing = false;
          render(true);
          return;
        }
        current = Number(message.screen != null ? message.screen : current);
        showing = true;
        render(true);
      } else if (message.type === 'stop') {
        showing = false;
        render(true);
      } else if (message.type === 'update') {
        reflow();
      } else if (message.type === 'state' && showing) {
        post({type: 'show', service: service, screen: current});
      }
    });
  }

  /* Update: re-read the page (a song's lyrics may have changed) and keep the place. */
  function reflow() {
    if (window.GKPSOffline) {
      window.GKPSOffline.sync().then(function () {
        return window.GKPSOffline.get('service', service);
      }).then(function (saved) {
        if (saved) drawSavedScreens(saved);
      }).catch(function () { /* preserve the currently projected screen */ });
      return;
    }
    /* A saved change reads back at once; no-store keeps a cached page from being served
       for the read that follows close behind it. */
    fetch(window.location.href, {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) { return response.ok ? response.text() : ''; })
      .then(function (html) {
        if (!html) return;
        var parsed = new DOMParser().parseFromString(html, 'text/html');
        var fresh = parsed.getElementById('projectorScreens');
        if (!fresh) return;
        stage.innerHTML = fresh.innerHTML;
        stage.appendChild(detourNode);
        var freshEntries = parsed.getElementById('projectorEntryData');
        var freshScreens = parsed.getElementById('projectorScreenData');
        if (freshEntries && freshScreens) {
          entries = JSON.parse(freshEntries.textContent);
          screenData = JSON.parse(freshScreens.textContent);
        }
        render(true);
      })
      .catch(function () { /* keep showing what we have */ });
  }

  function drawSavedScreens(saved) {
    if (!saved || !Array.isArray(saved.screens)) return;
    savedScreensSignature = JSON.stringify(saved.screens);
    var fragment = document.createDocumentFragment();
    saved.screens.forEach(function (item, index) {
      var section = document.createElement('section');
      section.className = 'screen' + (item.blank ? ' is-blank' : '')
        + (item.single ? ' screen--single' : '');
      section.dataset.screen = String(index);
      section.dataset.entry = String(item.entry_index == null ? '' : item.entry_index);
      section.dataset.bait = String(item.bait == null ? '' : item.bait);
      section.dataset.split = String(item.split == null ? '' : item.split);
      section.dataset.splitTotal = String(item.split_total == null ? '' : item.split_total);
      section.dataset.baitRest = item.bait_rest ? 'true' : 'false';
      if (item.single) section.dataset.fit = 'single';
      section.setAttribute('aria-hidden', index === current ? 'false' : 'true');
      if (item.header) {
        var head = document.createElement('h1');
        head.className = 'screen__head';
        head.textContent = item.header;
        section.appendChild(head);
      }
      if (item.lines && item.lines.length) {
        var lines = document.createElement('div');
        lines.className = 'screen__lines';
        item.lines.forEach(function (line) {
          var p = document.createElement('p');
          p.className = 'screen__line' + (line.voice ? ' is-' + line.voice : '');
          p.textContent = line.text;
          lines.appendChild(p);
        });
        section.appendChild(lines);
      }
      fragment.appendChild(section);
    });
    stage.replaceChildren(fragment);
    stage.appendChild(detourNode);
    entries = saved.entries || [];
    screenData = saved.screens;
    var empty = screen.querySelector('.projector__empty');
    if (empty) empty.hidden = !!saved.screens.length;
    render(true);
  }

  /* A window opened for a service that is already displaying lands on its screen. */
  var stored = read();
  if (stored && Number(stored.service) === service && stored.screen != null) {
    current = Number(stored.screen);
    showing = stored.on === true;
  } else if (stored && stored.on && Number(stored.service) !== service) {
    showing = false;
  }
  render(true);
  if (!screens().length && service && window.GKPSOffline) {
    window.GKPSOffline.get('service', service).then(function (saved) {
      if (saved) drawSavedScreens(saved);
      else {
        var empty = screen.querySelector('.projector__empty');
        if (empty) empty.textContent = 'This service is not saved for offline use yet.';
      }
    }).catch(function () {});
  }
  document.addEventListener('offline:changed', function () {
    if (!window.GKPSOffline) return;
    window.GKPSOffline.get('service', service).then(function (saved) {
      if (saved && (!screens().length || JSON.stringify(saved.screens) !== savedScreensSignature))
        drawSavedScreens(saved);
    }).catch(function () {});
  });
  window.addEventListener('resize', function () { render(true); });
  /* The sign of life, and the reason a shell can tell that this window has gone: while it
     is open it shows up every couple of seconds, and when it closes the stamps stop. */
  window.setInterval(beat, 2000);
  document.addEventListener('visibilitychange', beat);
  window.addEventListener('focus', beat);
  post({type: 'state'});                 /* ask the other tabs what is on screen */
})();
