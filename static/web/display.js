/* The display state, in the browser that started it (specs 006 and 119).
 *
 * Which Tata Ibadah is on air, and which of its screens, is the operator's business
 * and nobody else's: it never reaches the server, so several laptops can drive
 * different screens at once. Within one browser it is shared by two means --
 * localStorage (so a tab opened later already knows) and the display channel (so
 * every tab hears about a change at once). Any number of tabs of any surface is
 * safe, and closing them all changes nothing (spec 119): the display ends only by
 * `release`, never because a window went away.
 *
 * This file is the shared state module. The dock is the writer; the projector
 * (web/projector.js) and the caption overlay (web/obs-overlay.js) render; the
 * reading page's project button is a writer for one act (project / release), and
 * its second control opens the projector window again while the service is on air
 * (spec 141) without writing anything.
 *
 * Messages, all on `gkps-service-display`:
 *
 *     {type: 'show', service: <id>, screen: <n>}   an entry screen is on air
 *     {type: 'goto', goto: <Goto|null>}            a go to started, moved, flipped or ended
 *     {type: 'hide'}                               words off; the place is kept
 *     {type: 'release'}                            no active service
 *     {type: 'flip', translation: 'TB'|'SIM'|null} the shown translation changed
 *     {type: 'update'}                             re-read what is on air
 *     {type: 'state'}                              a newcomer asks to be brought up to date
 *
 * Stored shape (`gkps-display`):
 *     {service, screen, on, translation, at, session, goto}
 *
 * `screen` and `translation` are the SERVICE's place. While `goto` is up they are frozen;
 * Back is `goto: null` and they are what every surface then paints (spec 185 D001).
 *
 * Everything here is DELEGATED and resolved from the document on each use. The
 * shell swaps the reading pane's contents in place (reading.js applyPage), which
 * replaces the project button's node: a handler bound to the old node is bound to
 * nothing, and the button then works on a deep link and does nothing on the path a
 * person actually clicks through. Hence no held nodes, and a re-sync on
 * `shell:page`.
 */
(function () {
  'use strict';

  var KEY = 'gkps-display';
  var DEFAULT_CHANNEL = 'gkps-service-display';

  /* What is on air instead of the service: a pointer, never any words (spec 185 FR-001).
     A goto that cannot be parsed is no goto, and the service's own screen is painted. */
  function gotoOf(raw) {
    if (!raw || typeof raw !== 'object') return null;
    if (raw.kind === 'song') {
      var songId = Number(raw.song_id);
      if (!songId) return null;
      return {kind: 'song', song_id: songId, index: Math.max(0, Number(raw.index) || 0)};
    }
    if (raw.kind === 'passage') {
      var book = Number(raw.book_id), chapter = Number(raw.chapter);
      var verse = Number(raw.verse);
      if (!book || !chapter || !verse) return null;
      var shown = raw.translation === 'SIM' ? 'SIM' : (raw.translation === 'TB' ? 'TB' : null);
      return {kind: 'passage', book_id: book, chapter: chapter, verse: verse,
              translation: shown};
    }
    return null;
  }

  function read() {
    try {
      var stored = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (stored && typeof stored === 'object' &&
          window.GKPSDisplaySession && window.GKPSDisplaySession.owns(stored)) {
        return {service: stored.service == null ? null : Number(stored.service),
                screen: Number(stored.screen) || 0,
                on: stored.on === true,
                translation: stored.translation || null,
                at: Number(stored.at) || 0,
                session: stored.session,
                goto: gotoOf(stored.goto)};
      }
    } catch (e) { /* a corrupt value is no value */ }
    return {service: null, screen: 0, on: false, translation: null, at: 0,
            session: null, goto: null};
  }

  var state = read();
  var subscribers = [];
  var group = document.querySelector('[data-project-group]');
  var channelName = (group && group.dataset.displayChannel) || DEFAULT_CHANNEL;
  var channel = null;
  try {
    channel = new BroadcastChannel(channelName);
  } catch (e) {
    channel = null;                     /* no channel: the state still persists */
  }

  function notify() {
    subscribers.forEach(function (fn) {
      try { fn(state); } catch (e) { /* a bad subscriber must not stop the others */ }
    });
  }

  function write(next) {
    next.at = Date.now();               /* when this browser last touched the display */
    /* A verb that says nothing about the goto leaves it alone: `hide` and `flip` act on
       whatever is on air, and only the verbs below end a goto by naming `goto: null`. */
    var goto = next.goto === undefined ? state.goto : gotoOf(next.goto);
    state = {service: next.service == null ? null : Number(next.service),
             screen: Number(next.screen) || 0,
             on: next.on === true,
             translation: next.translation || null,
             at: next.at,
             goto: goto,
             /* The session this write belongs to (spec 184): a state whose stamp no
                longer matches the browser's marker is not a state. */
             session: window.GKPSDisplaySession ? window.GKPSDisplaySession.stamp() : null};
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
    notify();
  }

  function post(message) {
    if (channel) channel.postMessage(message);
  }

  /* ---------- the verbs (spec 119) ------------------------------------------ */

  /* Put a service's screen on air — from its start, or at the given screen. */
  function show(service, screen) {
    var id = Number(service);
    if (!id) return;
    /* "The service is on air" is one statement, whichever act produces it (FR-002). */
    write({service: id, screen: Number(screen) || 0, on: true,
           translation: state.service === id ? state.translation : null, goto: null});
    post({type: 'show', service: state.service, screen: state.screen});
  }

  /* Move the live screen, keeping the service on air. */
  function moveTo(screen) {
    if (state.service == null) return;
    /* A service screen going on air ends a go to, or the service would move invisibly
       underneath it (FR-009, FR-015, D008). */
    write({service: state.service, screen: Number(screen) || 0, on: true,
           translation: state.translation, goto: null});
    post({type: 'show', service: state.service, screen: state.screen});
  }

  /* Words off; the service and screen stay for a resume in place. */
  function hide() {
    if (state.service == null) return;
    write({service: state.service, screen: state.screen, on: false,
           translation: state.translation});
    post({type: 'hide'});
  }

  /* Let go: no active service anywhere. */
  function release() {
    write({service: null, screen: 0, on: false, translation: null, goto: null});
    post({type: 'release'});
  }

  /* The shown translation of the live screen (null = the entry's own). */
  function flip(translation) {
    if (state.service == null) return;
    /* `flip` names the edition of whatever is on air: the go to's while one is up, the
       service's otherwise, which the service keeps for its return (FR-002, FR-015). */
    if (state.goto && state.goto.kind === 'passage') {
      write({service: state.service, screen: state.screen, on: state.on,
             translation: state.translation,
             goto: {kind: 'passage', book_id: state.goto.book_id,
                    chapter: state.goto.chapter, verse: state.goto.verse,
                    translation: translation === 'SIM' ? 'SIM' : (translation === 'TB' ? 'TB' : null)}});
      post({type: 'goto', goto: state.goto});
      return;
    }
    write({service: state.service, screen: state.screen, on: state.on,
           translation: translation || null});
    post({type: 'flip', translation: state.translation});
  }

  /* ---------- the go to (spec 185) ----------------------------------------- */

  /* Put a passage or a song on air. The service's own screen and edition are left as
     they are, so Back has somewhere exact to land. */
  function goTo(goto) {
    var next = gotoOf(goto);
    if (!next || state.service == null) return;
    write({service: state.service, screen: state.screen, on: true,
           translation: state.translation, goto: next});
    post({type: 'goto', goto: state.goto});
  }

  /* Move the go to: a song's screen index, or a passage's verse. */
  function stepGoto(position) {
    if (!state.goto) return;
    var next = state.goto.kind === 'song'
      ? {kind: 'song', song_id: state.goto.song_id,
         index: Math.max(0, Number(position) || 0)}
      : {kind: 'passage', book_id: state.goto.book_id, chapter: state.goto.chapter,
         verse: Math.max(1, Number(position) || 1), translation: state.goto.translation};
    write({service: state.service, screen: state.screen, on: state.on,
           translation: state.translation, goto: next});
    post({type: 'goto', goto: state.goto});
  }

  /* Words back on, in place: a resume must never end a go to (FR-002's `hide` keeps
     the place, and this is its other half). */
  function resume() {
    if (state.service == null) return;
    write({service: state.service, screen: state.screen, on: true,
           translation: state.translation});
    post({type: 'goto', goto: state.goto});
  }

  /* Back to the service, exactly where it stood; `on` is not touched, because it is one
     flag for whatever is on air (the spec's hidden-words edge case). */
  function back() {
    if (!state.goto) return;
    write({service: state.service, screen: state.screen, on: state.on,
           translation: state.translation, goto: null});
    post({type: 'goto', goto: null});
  }

  /* Ask the surfaces to re-read what is on air (a saved change, spec 026). */
  function update() {
    post({type: 'update'});
  }

  function subscribe(fn) {
    if (typeof fn !== 'function') return function () {};
    subscribers.push(fn);
    fn(state);
    return function () {
      var index = subscribers.indexOf(fn);
      if (index !== -1) subscribers.splice(index, 1);
    };
  }

  /* ---------- the project button's two states --------------------------------- */

  function nodes() {
    var container = document.querySelector('[data-project-group]');
    return {
      group: container,
      open: container && container.querySelector('[data-project-open]'),
    };
  }

  /* Is THIS page's Tata Ibadah the one on screen in this browser? */
  function isHere() {
    var n = nodes();
    if (!n.open) return false;
    return state.on === true && state.service === Number(n.open.dataset.projectService);
  }

  function syncButton() {
    var n = nodes();
    if (!n.group || !n.open) return;
    var here = isHere();
    var text = here ? (n.open.dataset.labelStop || 'Stop projecting')
                    : (n.open.dataset.labelProject || 'Project');
    n.group.dataset.displaying = here ? 'true' : 'false';
    /* The button carries an icon: only its label changes. */
    var label = n.open.querySelector('[data-project-label]');
    if (label) label.textContent = text;
    else n.open.textContent = text;
    n.open.setAttribute('aria-label', text);
    n.open.title = text;
  }

  /* ---------- the way back to a closed window (spec 141) -------------------- */

  /* The window this page last opened, so a second press focuses it. It is a hint,
     not the truth: after a reload it is gone, and the named window is asked for. */
  var projected = null;

  /* Bring the projector window forward, opening it only when it is not there. An
     empty URL reuses the named window without loading it; only a fresh, blank one
     is sent to the page. A blocked window opens nothing and changes nothing. */
  function openProjector(url) {
    if (projected && !projected.closed) {
      try { projected.focus(); } catch (e) { /* a window that is already gone */ }
      return;
    }
    var win = null;
    try { win = window.open('', 'gkps-projector', 'width=1280,height=800'); } catch (e) { win = null; }
    if (!win) return;
    projected = win;
    try {
      if (win.location.href === 'about:blank') win.location.href = url;
    } catch (e) { /* a window that is not ours is left where it is */ }
    try { win.focus(); } catch (e) { /* the window may already be gone */ }
  }

  document.addEventListener('click', function (event) {
    var reopen = event.target.closest('[data-project-window]');
    if (reopen) {
      event.preventDefault();
      /* Only this page's own service, and only while it is on air: the control is a
         reader, so it never releases, hides or adopts anything. */
      if (state.on !== true || state.service !== Number(reopen.dataset.projectService)) return;
      openProjector(reopen.dataset.projectorUrl || '/projector');
      return;
    }
    var open = event.target.closest('[data-project-open]');
    if (!open) return;
    event.preventDefault();
    var service = Number(open.dataset.projectService);
    if (state.on === true && state.service === service) {
      release();                                          /* Stop project: let go (spec 119) */
      syncButton();
      return;
    }
    /* A window, not a page you navigate to: opened beside the app and sized for a
       screen. The dock drives what it renders from here on (spec 119). */
    var projector = window.open(open.dataset.projectorUrl, 'gkps-projector',
                                'width=1280,height=800');
    if (projector) {
      projector.focus();
      projected = projector;                              /* the reopen control focuses it */
    }
    show(service, 0);                                     /* the display opens at its start */
    syncButton();
  });

  /* Another tab changed the display: follow it, and answer a newcomer. */
  if (channel) {
    channel.addEventListener('message', function (event) {
      var message = event.data || {};
      if (message.type === 'show') {
        write({service: message.service, screen: message.screen, on: true,
               translation: state.service === Number(message.service) ? state.translation : null});
      } else if (message.type === 'hide') {
        if (state.service != null) {
          write({service: state.service, screen: state.screen, on: false,
                 translation: state.translation});
        }
      } else if (message.type === 'release') {
        write({service: null, screen: 0, on: false, translation: null});
      } else if (message.type === 'flip') {
        write({service: state.service, screen: state.screen, on: state.on,
               translation: message.translation || null});
      } else if (message.type === 'goto') {
        /* The write that posted it is already stored: adopt it by re-reading, never by
           writing again, or two surfaces would bounce the state between them. */
        state = read();
      } else if (message.type === 'state') {
        /* The store is authoritative; every write persists, so a new surface never
           needs to be told. Kept tolerated for compatibility. */
        return;
      }
      syncButton();
    });
  }

  /* ---------- the re-read (spec 186) ---------------------------------------
     A surface that outlives its browser session keeps painting what it painted: the
     marker is a session cookie, so it goes when the browser closes or the jar is
     cleared, while localStorage survives. `read()` already refuses a state from another
     session; this makes the surfaces ask again when they come back into view, take the
     keyboard, or are restored from the back/forward cache. */

  /* One canonical spelling of the state, so the compare cannot depend on the order the
     fields were written in (`read()` and `write()` list `goto` and `session` differently). */
  function fingerprint(value) {
    return [value.service, value.screen, value.on === true, value.translation || null,
            value.at, value.session || null,
            value.goto ? JSON.stringify(value.goto) : ''].join('|');
  }

  function reread() {
    var next = read();
    if (fingerprint(next) === fingerprint(state)) return;          /* nothing to repaint */
    state = next;
    syncButton();
    notify();
  }

  window.addEventListener('focus', reread);
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) reread();
  });
  window.addEventListener('pageshow', function (event) {
    if (event.persisted) reread();               /* a restored page skipped its boot */
  });

  /* The same change from another tab, via storage rather than the channel. */
  window.addEventListener('storage', function (event) {
    if (event.key !== KEY) return;
    state = read();
    syncButton();
    notify();
  });

  /* The reading pane was swapped in place: the arriving button knows nothing of
     this browser's display mode until it is told. */
  document.addEventListener('shell:page', syncButton);

  /* ---------- the re-read after a change (spec 026) -------------------------
     The display is given its truth by the server: every saved change here asks the
     projector to re-read the page. Only the service on air needs it, so a page
     showing another Tata Ibadah stays out of it. The Update button and this hook
     are the same act. */

  function reflow() {
    if (!isHere()) return;
    update();
  }

  window.gkpsDisplay = {
    /* the state */
    read: read,
    state: read,
    subscribe: subscribe,
    /* the verbs */
    show: show,
    screen: moveTo,
    /* Ask the store again — the module's own act, also bound to focus and visibility. */
    reread: reread,
    goTo: goTo,
    stepGoto: stepGoto,
    back: back,
    resume: resume,
    hide: hide,
    release: release,
    flip: flip,
    update: update,
    /* This page's Tata Ibadah is the one on screen in this browser. */
    live: isHere,
    /* Ask the display to re-read, when it is showing this page's Tata Ibadah. */
    changed: reflow,
    channel: channelName,
  };

  /* `editor:saved` fires after an entry save/delete (entries.js), a sidebar editor
     save (editors.js), and a reorder write (reorder.js). One seam, every change. */
  document.addEventListener('editor:saved', reflow);

  syncButton();
})();
