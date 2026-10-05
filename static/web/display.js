/* The display state, in the browser that started it (spec 006, slice 4).
 *
 * Which Tata Ibadah is on screen, and which of its entries, is the operator's
 * business and nobody else's: it never reaches the server, so several laptops can
 * drive different screens at once. Within one browser it is shared by two means --
 * localStorage (so a tab opened later already knows) and the display channel (so
 * every tab hears about a change at once).
 *
 * This file is the SHELL side: the project button, its Stop projecting and Update
 * the current state states, and the entry lock. The projector window has its own
 * script (web/projector.js); both speak the same messages:
 *
 *     {type: 'show', service: <id>, slide: <slide id>}   an entry is on screen
 *     {type: 'stop'}                                     nothing is on screen
 *     {type: 'update'}                                   re-read what is on screen
 *     {type: 'beat', service: <id>, on: <bool>}          the projector window is still open
 *
 * Everything here is DELEGATED and resolved from the document on each use. The
 * shell swaps the reading pane's contents in place (reading.js applyPage), which
 * replaces the project button's node: a handler bound to the old node is bound to
 * nothing, and the button then works on a deep link and does nothing on the path a
 * person actually clicks through. Hence no held nodes, and a re-sync on
 * `shell:page`.
 *
 * The lock is the shell declining an action, never a server rule, which is what
 * keeps the current API exactly as it is.
 */
(function () {
  'use strict';

  var KEY = 'gkps-display';

  function read() {
    try {
      var stored = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (stored && typeof stored === 'object') {
        return {service: stored.service, screen: stored.screen, on: stored.on === true,
                at: Number(stored.at) || 0};
      }
    } catch (e) { /* a corrupt value is no value */ }
    return {service: null, screen: 0, on: false, at: 0};
  }

  var state = read();
  var group = document.querySelector('[data-project-group]');
  var channelName = (group && group.dataset.displayChannel) || 'gkps-service-display';
  var channel = null;
  try {
    channel = new BroadcastChannel(channelName);
  } catch (e) {
    channel = null;                     /* no channel: the state still persists */
  }

  function write(next) {
    next.at = Date.now();               /* when this browser last touched the display */
    state = next;
    try { localStorage.setItem(KEY, JSON.stringify(next)); } catch (e) { /* private mode */ }
  }

  function post(message) {
    if (channel) channel.postMessage(message);
  }

  function nodes() {
    var container = document.querySelector('[data-project-group]');
    return {
      group: container,
      open: container && container.querySelector('[data-project-open]'),
      update: container && container.querySelector('[data-project-update]'),
      note: container && container.querySelector('[data-project-note]'),
    };
  }

  /* ---------- the button's two states --------------------------------------- */

  function sync() {
    var n = nodes();
    if (!n.group || !n.open) return;
    var service = Number(n.open.dataset.projectService);
    var here = state.on === true && state.service === service;
    var text = here ? (n.open.dataset.labelStop || 'Stop projecting')
                    : (n.open.dataset.labelProject || 'Project');
    n.group.dataset.displaying = here ? 'true' : 'false';
    /* The button carries an icon: only its label changes. */
    var label = n.open.querySelector('[data-project-label]');
    if (label) label.textContent = text;
    else n.open.textContent = text;
    n.open.setAttribute('aria-label', text);
    n.open.title = text;
    if (n.update) n.update.hidden = !here;
  }

  /* A click the display mode refused: say why, briefly, where the person is looking. */
  var noteTimer = null;
  function say(message) {
    var n = nodes();
    if (!n.note) return;
    n.note.textContent = message;
    n.note.hidden = false;
    window.clearTimeout(noteTimer);
    noteTimer = window.setTimeout(function () { n.note.hidden = true; }, 6000);
  }

  document.addEventListener('click', function (event) {
    var open = event.target.closest('[data-project-open]');
    if (open) {
      event.preventDefault();
      var service = Number(open.dataset.projectService);
      if (state.on === true && state.service === service) {
        write({service: service, screen: state.screen, on: false});   /* Stop projecting */
        post({type: 'stop'});
        sync();
        return;
      }
      /* A window, not a page you navigate to: opened beside the app and sized for a
         screen. Nothing grabs the screen -- the projector asks for full screen when
         the operator clicks inside it. */
      var projector = window.open(open.dataset.projectorUrl, 'gkps-projector',
                                  'width=1280,height=800');
      if (projector) projector.focus();
      watch(projector);                                       /* and know when it goes */
      write({service: service, screen: 0, on: true});          /* the display opens at its start */
      post({type: 'show', service: service, screen: 0});
      sync();
      return;
    }
    if (event.target.closest('[data-project-update]')) {
      event.preventDefault();
      post({type: 'update'});
      say('The display is re-reading this Tata Ibadah.');
    }
  });

  /* ---------- a display whose window has gone --------------------------------
     Closing the projector window has to end the display. Otherwise every tab of this
     browser stays locked -- refusing entry writes, showing Stop projecting -- for a
     screen nobody is driving, and the only way out is to press Stop on a display that
     is not running.

     Two signals, in order of speed. The window THIS tab opened: the browser tells the
     opener the moment its handle is closed, so closing the window stops the display at
     once. And the beat the projector leaves behind (web/projector.js), which covers the
     tabs that did not open it, a shell reloaded since, and a window that died instead of
     closing. The wait is long because a hidden tab's timers are throttled to about one a
     minute: quiet for a minute and a half means gone. A state written just now counts as
     alive by its own stamp, so the moment between pressing Project and the window's first
     beat cannot stop the display it just started. */
  var BEAT_KEY = 'gkps-display-beat';
  var QUIET_AFTER = 90 * 1000;

  function lastBeat() {
    try { return Number(localStorage.getItem(BEAT_KEY)) || 0; } catch (e) { return 0; }
  }

  function gone() {
    if (state.on !== true) return false;
    var stamp = Math.max(lastBeat(), Number(state.at) || 0);
    return Date.now() - stamp > QUIET_AFTER;
  }

  function stopBecauseGone() {
    if (state.on !== true) return;
    write({service: state.service, screen: state.screen, on: false});
    post({type: 'stop'});
    sync();
    say('The projector window is gone, so the display stopped.');
  }

  function watch(win) {
    if (!win) return;
    var timer = window.setInterval(function () {
      if (!win.closed) return;
      window.clearInterval(timer);
      stopBecauseGone();
    }, 700);
  }

  window.setInterval(function () { if (gone()) stopBecauseGone(); }, 5000);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible' && gone()) stopBecauseGone();
  });
  if (gone()) stopBecauseGone();        /* a display left on from an earlier session */

  /* Another tab changed the display: follow it. */
  if (channel) {
    channel.addEventListener('message', function (event) {
      var message = event.data || {};
      if (message.type === 'show') write({service: message.service, screen: message.screen, on: true});
      else if (message.type === 'stop') write({service: state.service, screen: state.screen, on: false});
      else if (message.type === 'state' && state.on) {
        post({type: 'show', service: state.service, screen: state.screen});
      }
      sync();
    });
  }

  /* The same change from another tab, via storage rather than the channel. */
  window.addEventListener('storage', function (event) {
    if (event.key !== KEY) return;
    state = read();
    sync();
  });

  /* The reading pane was swapped in place: the arriving button knows nothing of
     this browser's display mode until it is told. */
  document.addEventListener('shell:page', sync);

  /* ---------- the entry lock ------------------------------------------------ */

  var LOCKED = 'This browser is displaying a Tata Ibadah. Stop projecting first.';

  window.gkpsDisplay = {
    locked: function () { return state.on === true; },
    reason: LOCKED,
    refuse: function () { say(LOCKED); },
    channel: channelName,
  };

  sync();
})();
