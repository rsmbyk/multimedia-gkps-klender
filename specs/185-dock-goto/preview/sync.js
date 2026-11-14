/* The sync page (spec 185): one display state, three surfaces, one document.
 *
 * Each step is the state a browser would hold in `gkps-display` at that moment. The dock
 * is the product's own runner (preview.js drives it, listening for the same message the
 * channel would carry); the projector and the overlay are painted here by the rules their
 * own pages apply — web/projector.js's overflows/fit and web/obs-overlay.js's
 * modelOf/caption/plate. Every surface reports what it painted, and those reports are what
 * the page prints.
 *
 * It is all one document because the desktop chat's preview frame runs no nested documents
 * (three iframes there stayed empty).
 */
(function () {
  'use strict';

  var PV = window.__PV;
  var GOLDEN_RATIO = (1 + Math.sqrt(5)) / 2;

  var STEPS = [
    {name: 'The service is on air',
     state: {screen: 12, on: true, goto: null}, view: 'rest'},
    {name: 'G — the Go To opens over the dock (nothing on air changes)',
     state: {screen: 12, on: true, goto: null}, view: 'find'},
    {name: 'NKB 43 is chosen — a song that is not in the service',
     state: {screen: 12, on: true, goto: {kind: 'song', song_id: 1434, index: 0}}},
    {name: 'the go to steps to the next screen',
     state: {screen: 12, on: true, goto: {kind: 'song', song_id: 1434, index: 2}}},
    {name: 'Matius 5:3 is chosen — a passage',
     state: {screen: 12, on: true,
             goto: {kind: 'passage', book_id: 40, chapter: 5, verse: 3, translation: 'TB'}}},
    {name: 'T — the passage flips to the Simalungun edition',
     state: {screen: 12, on: true,
             goto: {kind: 'passage', book_id: 40, chapter: 5, verse: 3, translation: 'SIM'}}},
    {name: 'Space — the words are hidden, the place is kept',
     state: {screen: 12, on: false,
             goto: {kind: 'passage', book_id: 40, chapter: 5, verse: 3, translation: 'TB'}}},
    {name: 'Back — the service returns, still blank',
     state: {screen: 12, on: false, goto: null}, view: 'rest'},
    {name: "Space — the service's own words come back",
     state: {screen: 12, on: true, goto: null}, view: 'rest'}
  ];

  var SERVICE = 142;
  var stepsBox = document.getElementById('svSteps');
  var title = document.getElementById('svTitle');
  var stateBox = document.getElementById('svState');
  var readBox = document.getElementById('svRead');
  var projCanvas = document.querySelector('.sv-projector');
  var projHost = document.getElementById('svProjScreens');
  var overlayStage = document.getElementById('svOverlayStage');
  var at = 0;
  var reports = {dock: '—', projector: '—', overlay: '—'};

  /* ---------- the projector: web/projector.js's render + overflows + fit ------ */

  function overflows(head, lines) {
    if (head && (head.scrollWidth > projHost.clientWidth + 1
                 || head.getBoundingClientRect().bottom > projHost.getBoundingClientRect().bottom)) return true;
    if (!lines) return false;
    if (lines.scrollHeight > lines.clientHeight + 1) return true;
    var range = document.createRange();
    range.selectNodeContents(lines);
    var ink = range.getBoundingClientRect();
    var box = lines.getBoundingClientRect();
    var stageBox = projHost.getBoundingClientRect();
    return ink.left < box.left - 1 || ink.right > box.right + 1
      || ink.top < box.top - 2 || ink.bottom > box.bottom + 2
      || ink.top < stageBox.top - 1 || ink.bottom > stageBox.bottom + 1;
  }

  function fit(active) {
    var head = active.querySelector('.screen__head');
    var lines = active.querySelector('.screen__lines');
    if (!lines) return;
    for (var size = 200; size >= 2; size -= 1) {
      lines.style.fontSize = size + 'px';
      if (head) head.style.fontSize = (size / GOLDEN_RATIO) + 'px';
      if (!overflows(head, lines)) break;
    }
  }

  function projContent(state) {
    if (!state.goto) {
      var screen = PV.service.screens[state.screen] || null;
      if (!screen || screen.blank) return {head: '', lines: []};
      return {head: screen.header || '',
              lines: (screen.lines || []).map(function (line) { return line.text; })};
    }
    if (state.goto.kind === 'song') {
      var payload = PV.songs[String(state.goto.song_id)];
      var shot = payload && payload.screens[state.goto.index];
      if (!shot || shot.blank) return {head: '', lines: []};
      return {head: shot.header || '',
              lines: (shot.lines || []).map(function (line) { return line.text; })};
    }
    var edition = PV.chapter.editions[state.goto.translation] || PV.chapter.editions.TB;
    var verse = (edition.verses || []).filter(function (row) { return row.n === state.goto.verse; })[0];
    if (!verse) return null;
    return {head: edition.name + ' ' + PV.chapter.chapter + ':' + verse.n
                  + (verse.title ? '\n' + verse.title : ''),
            lines: [verse.text]};
  }

  function renderProjector(state) {
    projHost.replaceChildren();
    projCanvas.dataset.showing = state.on ? 'true' : 'false';
    var made = projContent(state);
    if (!made) { reports.projector = '(nothing)'; return; }
    var section = document.createElement('section');
    section.className = 'screen is-active' + (state.goto ? ' projector-detour' : '');
    if (made.head) {
      var head = document.createElement('h1');
      head.className = 'screen__head';
      head.textContent = made.head;
      section.appendChild(head);
    }
    if (made.lines.length) {
      var box = document.createElement('div');
      box.className = 'screen__lines';
      made.lines.forEach(function (text) {
        var line = document.createElement('p');
        line.className = 'screen__line';
        line.textContent = text;
        box.appendChild(line);
      });
      section.appendChild(box);
    }
    projHost.appendChild(section);
    fit(section);
    var name = (made.head || '').split('\n')[0];
    reports.projector = state.on
      ? ((name ? name + ' · ' : '') + (made.lines[0] || '(nothing)'))
      : '(words hidden)';
  }

  /* ---------- the overlay: web/obs-overlay.js's modelOf / caption / plate ----- */

  function modelOf(screen, entry, translation) {
    if (!screen || screen.blank) return null;
    var variant = translation && screen.translations ? screen.translations[translation] : null;
    var heading = String((variant && variant.header) || screen.header || '').trim();
    var lines = variant && variant.line
      ? [{text: variant.line, voice: '', mark: '', words: variant.line}]
      : (screen.lines || []).map(function (line) {
          var text = String(line.text || '').trim();
          return {text: text, voice: String(line.voice || ''),
                  mark: String(line.mark || '').trim(),
                  words: String(line.words == null ? text : line.words).trim()};
        }).filter(function (line) { return line.text; });
    if (!lines.length) return null;
    var kind = entry ? entry.type : '';
    if (kind === 'passage') return {kind: 'passage', heading: heading, lines: lines};
    if (kind === 'text') return {kind: 'liturgy', heading: heading, lines: lines};
    if (kind === 'song') return {kind: 'song', heading: '', lines: lines};
    if (kind === 'media' || kind === 'break') return null;
    return {kind: 'song', heading: '', lines: lines};
  }

  function caption(model) {
    var node = document.createElement('p');
    node.className = 'obs-overlay__caption';
    model.lines.forEach(function (line) {
      var span = document.createElement('span');
      span.textContent = line.text;
      node.appendChild(span);
    });
    return node;
  }

  function plate(model) {
    var node = document.createElement('div');
    node.className = 'obs-overlay__plate';
    node.dataset.kind = model.kind;
    var parts = model.heading ? model.heading.split('\n') : [];
    var kicker = (parts.shift() || '').trim();
    var subtitleText = parts.join('\n').trim();
    if (kicker) {
      var head = document.createElement('p');
      head.className = 'obs-overlay__kicker';
      head.textContent = kicker;
      node.appendChild(head);
    }
    if (subtitleText) {
      var subtitle = document.createElement('p');
      subtitle.className = 'obs-overlay__title';
      subtitle.textContent = subtitleText;
      node.appendChild(subtitle);
    }
    if (kicker || subtitleText) {
      var rule = document.createElement('span');
      rule.className = 'obs-overlay__rule';
      node.appendChild(rule);
    }
    var body = document.createElement('div');
    body.className = 'obs-overlay__body';
    model.lines.forEach(function (line) {
      var row = document.createElement('p');
      row.className = 'obs-overlay__line' + (line.voice ? ' is-' + line.voice : '');
      if (line.mark && line.words) {
        row.className += ' has-mark';
        var speaker = document.createElement('span');
        speaker.className = 'obs-overlay__speaker';
        speaker.textContent = line.mark;
        var words = document.createElement('span');
        words.className = 'obs-overlay__words';
        words.textContent = line.words;
        row.appendChild(speaker);
        row.appendChild(words);
      } else {
        row.textContent = line.text;
      }
      body.appendChild(row);
    });
    node.appendChild(body);
    return node;
  }

  function overlayModel(state) {
    if (!state.goto) {
      var screen = PV.service.screens[state.screen] || null;
      var entry = screen && screen.entry_index != null ? PV.service.entries[screen.entry_index] : null;
      return modelOf(screen, entry, state.translation);
    }
    if (state.goto.kind === 'song') {
      var payload = PV.songs[String(state.goto.song_id)];
      var shot = payload && payload.screens[state.goto.index];
      if (!shot || shot.blank) return null;
      return {kind: 'song', heading: '',
              lines: (shot.lines || []).map(function (line) {
                return {text: line.text, voice: '', mark: '', words: line.text}; })};
    }
    var edition = PV.chapter.editions[state.goto.translation] || PV.chapter.editions.TB;
    var verse = (edition.verses || []).filter(function (row) { return row.n === state.goto.verse; })[0];
    if (!verse) return null;
    return {kind: 'passage',
            heading: edition.name + ' ' + PV.chapter.chapter + ':' + verse.n
                     + (verse.title ? '\n' + verse.title : ''),
            lines: [{text: verse.text, voice: '', mark: '', words: verse.text}]};
  }

  function renderOverlay(state) {
    overlayStage.replaceChildren();
    var model = state.on ? overlayModel(state) : null;
    overlayStage.dataset.kind = model ? model.kind : '';
    if (!model) {
      reports.overlay = state.on ? '(nothing)' : '(nothing: the words are hidden)';
      return;
    }
    overlayStage.appendChild(model.kind === 'song' ? caption(model) : plate(model));
    reports.overlay = model.kind + ' · '
      + (model.heading ? model.heading.split('\n')[0] + ' · ' : '')
      + (model.lines[0] ? model.lines[0].text : '');
  }

  /* ---------- the steps ------------------------------------------------------ */

  function displayState(step) {
    return {service: SERVICE, screen: step.state.screen, on: step.state.on,
            translation: step.state.goto ? (step.state.goto.translation || null) : null,
            goto: step.state.goto, session: 'preview'};
  }

  function go(index) {
    at = Math.max(0, Math.min(index, STEPS.length - 1));
    var step = STEPS[at];
    var state = displayState(step);
    reports = {dock: '—', projector: '—', overlay: '—'};
    window.postMessage({type: 'pv-go', state: state, view: step.view || 'rest'}, '*');
    renderProjector(state);
    renderOverlay(state);
    title.textContent = (at + 1) + '/' + STEPS.length + ' · ' + step.name;
    stateBox.textContent = 'gkps-display = ' + JSON.stringify(state, null, 2);
    Array.prototype.forEach.call(stepsBox.children, function (button, index2) {
      button.setAttribute('aria-current', index2 === at ? 'true' : 'false');
    });
    paintRead();
  }

  function paintRead() {
    readBox.replaceChildren();
    [['dock', 'Dock'], ['projector', 'Projector'], ['overlay', 'Overlay']].forEach(function (pair) {
      var row = document.createElement('div');
      var name = document.createElement('b');
      name.textContent = pair[1];
      var text = document.createElement('span');
      text.textContent = reports[pair[0]];
      row.appendChild(name);
      row.appendChild(text);
      readBox.appendChild(row);
    });
  }

  /* The board is a fixed 1084 px wide (dock 400 + gap 16 + display 640). In a narrow
     column — the chat's preview frame is 640 — shrink it as one piece instead of
     stacking it out of view: `zoom` scales the layout too, so the surfaces keep their
     proportions and every one of them stays where the other two are. */
  var BOARD = 1084;

  function fitBoard() {
    var stage = document.querySelector('.sv-stage');
    if (!stage) return;
    var room = document.documentElement.clientWidth - 28;
    stage.style.zoom = String(Math.min(1, room / BOARD).toFixed(4));
  }

  window.addEventListener('resize', fitBoard);
  fitBoard();

  STEPS.forEach(function (step, index) {
    var button = document.createElement('button');
    button.type = 'button';
    button.textContent = String(index + 1);
    button.title = step.name;
    button.addEventListener('click', function () { go(index); });
    stepsBox.appendChild(button);
  });

  document.getElementById('svPrev').addEventListener('click', function () { go(at - 1); });
  document.getElementById('svNext').addEventListener('click', function () { go(at + 1); });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowRight') { event.preventDefault(); go(at + 1); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); go(at - 1); }
  });

  window.addEventListener('message', function (event) {
    var message = event.data || {};
    if (message.type !== 'pv-rendered') return;
    reports[message.surface] = message.text;
    paintRead();
  });

  go(0);
})();
