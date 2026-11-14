/* The OBS caption overlay (specs 119 and 165).
 *
 * A listen-only browser source. It owns no controls and no server data: it reads the
 * browser-local display state (written by the dock and the reading page, stored under
 * `gkps-display`, announced on `gkps-service-display`) and paints whatever is on air.
 * The service's screen data comes from the projector page's data islands — one fetch
 * per service, cached for the session.
 *
 * The surface reads by entry kind. A song is a lyric, so it keeps the bare subtitle
 * caption (white ink, dark outline, no plate). A passage and a liturgy text carry a
 * heading — the Bible reference and the verse's title, or the entry's own title — so
 * they wear a plate instead, and the words sit on it. Blank, hidden, released, and
 * media screens (image, audio, video, PDF, PPTX) paint nothing.
 */
(function () {
  'use strict';

  var KEY = 'gkps-display';
  var CHANNEL = 'gkps-service-display';
  var stage = document.getElementById('overlayStage');
  var cache = {};        /* service id -> {screens, entries} */
  var pending = {};      /* service id -> callbacks waiting on the fetch */
  var painted = '';      /* signature of what is on screen, to avoid repainting */

  function readState() {
    try {
      var stored = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (stored && typeof stored === 'object' &&
          window.GKPSDisplaySession && window.GKPSDisplaySession.owns(stored)) {
        return {service: stored.service == null ? null : Number(stored.service),
                screen: Number(stored.screen) || 0,
                on: stored.on === true,
                translation: stored.translation || null,
                goto: gotoOf(stored.goto)};
      }
    } catch (e) { /* no stored state */ }
    return {service: null, screen: 0, on: false, translation: null, goto: null};
  }

  function gotoOf(raw) {
    if (!raw || typeof raw !== 'object') return null;
    if (raw.kind === 'song' && Number(raw.song_id)) {
      return {kind: 'song', song_id: Number(raw.song_id),
              index: Math.max(0, Number(raw.index) || 0)};
    }
    if (raw.kind === 'passage' && Number(raw.book_id) && Number(raw.chapter) && Number(raw.verse)) {
      return {kind: 'passage', book_id: Number(raw.book_id), chapter: Number(raw.chapter),
              verse: Number(raw.verse),
              translation: raw.translation === 'SIM' ? 'SIM' : (raw.translation === 'TB' ? 'TB' : null)};
    }
    return null;
  }

  /* What a screen shows: its kind, its heading, and its lines. The shown translation,
     when a passage carries one, brings its own heading and words. */
  function modelOf(screen, entry, translation) {
    if (!screen || screen.blank) return null;
    var variant = translation && screen.translations ? screen.translations[translation] : null;
    var heading = String((variant && variant.header) || screen.header || '').trim();
    var lines = variant && variant.line ? [{text: variant.line, voice: '', mark: '', words: variant.line}]
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
    /* An unknown entry (a payload-only screen, or no entry island) keeps the caption,
       which is what every screen painted before the surface read by kind. */
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

  /* A plate: the heading above a hairline, the words under it. The heading's first
     line names the screen (a reference, an entry title); what follows is its own
     title, which a verse carries and a liturgy usually does not. */
  function plate(model) {
    var node = document.createElement('div');
    node.className = 'obs-overlay__plate';
    node.dataset.kind = model.kind;
    var parts = model.heading ? model.heading.split('\n') : [];
    var kicker = (parts.shift() || '').trim();
    var title = parts.join('\n').trim();
    if (kicker) {
      var head = document.createElement('p');
      head.className = 'obs-overlay__kicker';
      head.textContent = kicker;
      node.appendChild(head);
    }
    if (title) {
      var subtitle = document.createElement('p');
      subtitle.className = 'obs-overlay__title';
      subtitle.textContent = title;
      node.appendChild(subtitle);
    }
    if (kicker || title) {
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
        /* A speaker's mark gets its own column, so a wrapped line hangs under the
           words it introduces — not under the mark or the panel's edge. */
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

  var reduceMotion = window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;

  function detach(node) {
    if (node && node.parentNode) node.parentNode.removeChild(node);
  }

  /* A panel ARRIVES with a short fade and drift, and LEAVES the same way (spec 165).
     The words inside a panel stay a cut: a screen step is not an entrance. */
  function animateIn(node) {
    if (reduceMotion && reduceMotion.matches) return;
    node.classList.add('is-entering');
    node.addEventListener('animationend', function () {
      node.classList.remove('is-entering');
    }, {once: true});
  }

  function animateOut(node) {
    if (reduceMotion && reduceMotion.matches) { detach(node); return; }
    node.classList.add('is-leaving');
    var done = function () { detach(node); };
    node.addEventListener('animationend', done, {once: true});
    /* A backgrounded tab may not run the animation; never leave the old panel behind. */
    window.setTimeout(done, 400);
  }

  /* The same panel on the next screen keeps its place and morphs its box: the old measure
     is pinned, then released to the new one on the shared 180 ms clock. */
  function resizePlate(node, fromWidth, fromHeight) {
    var toWidth = node.offsetWidth;
    var toHeight = node.offsetHeight;
    if (!fromWidth || !toWidth) return;
    if (fromWidth === toWidth && fromHeight === toHeight) return;
    if (reduceMotion && reduceMotion.matches) return;

    /* The box morphs empty, then the words resolve inside it: the new lines are laid out at
       the final measure from the first frame, so nothing re-wraps while the card moves. */
    var children = Array.prototype.slice.call(node.children);
    children.forEach(function (child) {
      child.style.transition = 'none';
      child.style.opacity = '0';
    });

    node.style.width = fromWidth + 'px';
    node.style.height = fromHeight + 'px';
    node.classList.add('is-resizing');
    node.offsetWidth;                                   // settle the start state
    window.requestAnimationFrame(function () {
      node.style.width = toWidth + 'px';
      node.style.height = toHeight + 'px';
    });
    var reveal = window.setTimeout(function () {
      children.forEach(function (child) {
        child.style.transition = 'opacity 110ms linear';
        child.style.opacity = '1';
      });
    }, 110);

    var settled = false;
    var settle = function () {
      if (settled) return;
      settled = true;
      window.clearTimeout(reveal);
      node.classList.remove('is-resizing');
      node.style.width = '';
      node.style.height = '';
      children.forEach(function (child) {
        child.style.transition = '';
        child.style.opacity = '';
      });
    };
    node.addEventListener('transitionend', function (event) {
      if (event.propertyName === 'width') settle();
    });
    /* A hidden tab may not run the transition; never leave the box pinned. */
    window.setTimeout(settle, 400);
  }

  /* One column for the marks on a screen, sized by the widest of them, so every line's
     words begin at the same x — a script, not a ragged stack. */
  function applySpeakerColumn(plateNode) {
    var widest = 0;
    plateNode.querySelectorAll('.obs-overlay__speaker').forEach(function (mark) {
      if (mark.offsetWidth > widest) widest = mark.offsetWidth;
    });
    var body = plateNode.querySelector('.obs-overlay__body');
    if (body && widest) body.style.setProperty('--speaker-col', widest + 'px');
  }

  function paint(model) {
    var signature = model ? JSON.stringify(model) : '';
    if (signature === painted) return;
    painted = signature;
    stage.dataset.kind = model ? model.kind : '';
    var shown = stage.querySelector('.obs-overlay__plate');
    if (!model) {
      /* Nothing on air: whatever is up fades out of its own place. */
      stage.querySelectorAll('.obs-overlay__caption').forEach(function (node) {
        if (!node.classList.contains('is-leaving')) animateOut(node);
      });
      if (shown && !shown.classList.contains('is-leaving')) animateOut(shown);
      return;
    }
    if (model.kind === 'song') {
      /* A lyric is one object: it arrives when the song starts and leaves when it ends;
         stepping to the next lyric swaps the words, which is a cut. */
      var hadCaption = stage.querySelector('.obs-overlay__caption');
      var line = caption(model);
      stage.replaceChildren(line);
      if (!hadCaption) animateIn(line);
      return;
    }
    var node = plate(model);
    var fromWidth = shown ? shown.offsetWidth : 0;
    var fromHeight = shown ? shown.offsetHeight : 0;
    stage.replaceChildren(node);
    if (shown && !shown.classList.contains('is-leaving')) resizePlate(node, fromWidth, fromHeight);
    else if (!shown) animateIn(node);
    applySpeakerColumn(node);
  }

  function ensure(service, done) {
    if (!service) { done(null); return; }
    if (cache[service]) { done(cache[service]); return; }
    if (pending[service]) { pending[service].push(done); return; }
    pending[service] = [done];
    fetch('/projector?service=' + encodeURIComponent(service),
          {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) { return response.ok ? response.text() : ''; })
      .then(function (html) {
        var callbacks = pending[service] || [];
        delete pending[service];
        if (!html) { callbacks.forEach(function (fn) { fn(null); }); return; }
        var parsed = new DOMParser().parseFromString(html, 'text/html');
        var screens = parsed.getElementById('projectorScreenData');
        if (!screens) { callbacks.forEach(function (fn) { fn(null); }); return; }
        var entries = parsed.getElementById('projectorEntryData');
        cache[service] = {
          screens: JSON.parse(screens.textContent) || [],
          entries: entries ? JSON.parse(entries.textContent) || [] : []
        };
        callbacks.forEach(function (fn) { fn(cache[service]); });
      })
      .catch(function () {
        var callbacks = pending[service] || [];
        delete pending[service];
        callbacks.forEach(function (fn) { fn(null); });
      });
  }

  /* ---------- the go to (spec 185) ------------------------------------------- */

  /* A go to carries a pointer, so the overlay fetches the words it paints — the same
     three payloads the projector reads, `no-store`, cached per song/chapter. */
  var gotoCache = {};    /* key -> payload */

  function gotoModel(goto, payload) {
    if (goto.kind === 'song') {
      var screen = (payload.screens || [])[goto.index];
      if (!screen || screen.blank) return null;
      var lines = (screen.lines || []).map(function (line) {
        var text = String(line.text || '').trim();
        return {text: text, voice: String(line.voice || ''),
                mark: String(line.mark || '').trim(),
                words: String(line.words == null ? text : line.words).trim()};
      }).filter(function (line) { return line.text; });
      if (!lines.length) return null;
      return {kind: 'song', heading: '', lines: lines};
    }
    var editions = payload.editions || {};
    var edition = editions[goto.translation] || editions.TB || editions[Object.keys(editions)[0]];
    if (!edition) return null;
    var verse = (edition.verses || []).filter(function (row) { return row.n === goto.verse; })[0];
    if (!verse) return null;
    var heading = edition.name + ' ' + payload.chapter + ':' + verse.n
                  + (verse.title ? '\n' + verse.title : '');
    return {kind: 'passage', heading: heading,
            lines: [{text: verse.text, voice: '', mark: '', words: verse.text}]};
  }

  function syncGoto(state) {
    var goto = state.goto;
    var key = goto.kind === 'song' ? 'song:' + goto.song_id
      : 'passage:' + goto.book_id + ':' + goto.chapter;
    var held = gotoCache[key];
    if (held) { paint(gotoModel(goto, held)); return; }
    var url = goto.kind === 'song' ? '/projector/goto/song/' + goto.song_id + '/'
      : '/projector/goto/chapter/' + goto.book_id + '/' + goto.chapter + '/';
    fetch(url, {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function (payload) {
        gotoCache[key] = payload;
        var latest = readState();
        if (!latest.goto || latest.on !== true) return;
        if (latest.goto.kind !== goto.kind) return;
        if (goto.kind === 'song' && latest.goto.song_id !== goto.song_id) return;
        if (goto.kind === 'passage' && (latest.goto.book_id !== goto.book_id
            || latest.goto.chapter !== goto.chapter)) return;
        paint(gotoModel(latest.goto, payload));
      })
      .catch(function () { paint(null); });
  }

  function sync() {
    var state = readState();
    if (state.on !== true) { paint(null); return; }
    /* A go to paints from its own payload, so it needs no service underneath it
       (spec 187 FR-011): check it before the service is required. */
    if (state.goto) { syncGoto(state); return; }
    if (!state.service) { paint(null); return; }
    ensure(state.service, function (data) {
      if (!data) { paint(null); return; }
      /* The state may have moved on while the fetch was in the air. */
      var latest = readState();
      if (latest.service !== state.service) return;
      var screen = data.screens[Math.max(0, latest.screen)] || null;
      var entry = screen && screen.entry_index != null
        ? data.entries[screen.entry_index] || null : null;
      paint(modelOf(screen, entry, latest.translation));
    });
  }

  var channel = null;
  try { channel = new BroadcastChannel(CHANNEL); } catch (e) { channel = null; }
  if (channel) {
    channel.addEventListener('message', function (event) {
      var message = event.data || {};
      if (message.type && message.type !== 'state') sync();
    });
  }
  window.addEventListener('storage', function (event) {
    if (event.key === KEY) sync();
  });
  document.addEventListener('visibilitychange', sync);
  window.addEventListener('focus', sync);
  window.addEventListener('resize', function () {
    var current = stage.querySelector('.obs-overlay__plate');
    if (current) applySpeakerColumn(current);
  });

  sync();
})();
