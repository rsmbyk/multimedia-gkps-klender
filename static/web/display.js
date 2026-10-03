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
        return {service: stored.service, slide: stored.slide, on: stored.on === true};
      }
    } catch (e) { /* a corrupt value is no value */ }
    return {service: null, slide: null, on: false};
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
    n.group.dataset.displaying = here ? 'true' : 'false';
    n.open.textContent = here ? (n.open.dataset.labelStop || 'Stop projecting')
                              : (n.open.dataset.labelProject || 'Project');
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
        write({service: service, slide: state.slide, on: false});   /* Stop projecting */
        post({type: 'stop'});
        sync();
        return;
      }
      /* A window, not a page you navigate to: opened beside the app and sized for a
         screen. Nothing grabs the screen -- the projector asks for full screen when
         the operator clicks inside it. */
      var anchors = document.querySelectorAll('#readBody [data-anchor]');
      var first = anchors.length ? (anchors[0].dataset.anchor || '') : '';
      var projector = window.open(open.dataset.projectorUrl, 'gkps-projector',
                                  'width=1280,height=800');
      if (projector) projector.focus();
      write({service: service, slide: first, on: true});
      post({type: 'show', service: service, slide: first});
      sync();
      return;
    }
    if (event.target.closest('[data-project-update]')) {
      event.preventDefault();
      post({type: 'update'});
      say('The display is re-reading this Tata Ibadah.');
    }
  });

  /* Another tab changed the display: follow it. */
  if (channel) {
    channel.addEventListener('message', function (event) {
      var message = event.data || {};
      if (message.type === 'show') write({service: message.service, slide: message.slide, on: true});
      else if (message.type === 'stop') write({service: state.service, slide: state.slide, on: false});
      else if (message.type === 'state' && state.on) {
        post({type: 'show', service: state.service, slide: state.slide});
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
