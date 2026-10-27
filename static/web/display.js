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
 *     {type: 'hide'}                               words off; the place is kept
 *     {type: 'release'}                            no active service
 *     {type: 'flip', translation: 'TB'|'SIM'|null} the shown translation changed
 *     {type: 'update'}                             re-read what is on air
 *     {type: 'state'}                              a newcomer asks to be brought up to date
 *
 * Stored shape (`gkps-display`):
 *     {service, screen, on, translation, at}
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

  function read() {
    try {
      var stored = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (stored && typeof stored === 'object') {
        return {service: stored.service == null ? null : Number(stored.service),
                screen: Number(stored.screen) || 0,
                on: stored.on === true,
                translation: stored.translation || null,
                at: Number(stored.at) || 0};
      }
    } catch (e) { /* a corrupt value is no value */ }
    return {service: null, screen: 0, on: false, translation: null, at: 0};
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
    state = {service: next.service == null ? null : Number(next.service),
             screen: Number(next.screen) || 0,
             on: next.on === true,
             translation: next.translation || null,
             at: next.at};
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
    write({service: id, screen: Number(screen) || 0, on: true,
           translation: state.service === id ? state.translation : null});
    post({type: 'show', service: state.service, screen: state.screen});
  }

  /* Move the live screen, keeping the service on air. */
  function moveTo(screen) {
    if (state.service == null) return;
    write({service: state.service, screen: Number(screen) || 0, on: true,
           translation: state.translation});
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
    write({service: null, screen: 0, on: false, translation: null});
    post({type: 'release'});
  }

  /* The shown translation of the live screen (null = the entry's own). */
  function flip(translation) {
    if (state.service == null) return;
    write({service: state.service, screen: state.screen, on: state.on,
           translation: translation || null});
    post({type: 'flip', translation: state.translation});
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
      } else if (message.type === 'state') {
        /* The store is authoritative; every write persists, so a new surface never
           needs to be told. Kept tolerated for compatibility. */
        return;
      }
      syncButton();
    });
  }

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
