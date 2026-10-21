/* The OBS caption overlay (spec 119).
 *
 * A listen-only browser source. It owns no controls and no server data: it reads the
 * browser-local display state (written by the dock and the reading page, stored under
 * `gkps-display`, announced on `gkps-service-display`) and captions whatever is on
 * air. The service's screen data comes from the projector page's data islands — one
 * fetch per service, cached for the session.
 *
 * Text screens caption their lines; blank, hidden, released, and media screens
 * (image, audio, video, PDF, PPTX) render nothing in this slice.
 */
(function () {
  'use strict';

  var KEY = 'gkps-display';
  var CHANNEL = 'gkps-service-display';
  var stage = document.getElementById('overlayStage');
  var cache = {};        /* service id -> screenData array */
  var pending = {};      /* service id -> callbacks waiting on the fetch */
  var painted = '';      /* signature of what is on screen, to avoid repainting */

  function readState() {
    try {
      var stored = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (stored && typeof stored === 'object') {
        return {service: stored.service == null ? null : Number(stored.service),
                screen: Number(stored.screen) || 0,
                on: stored.on === true,
                translation: stored.translation || null};
      }
    } catch (e) { /* no stored state */ }
    return {service: null, screen: 0, on: false, translation: null};
  }

  /* The caption lines for a screen: the entry's own words, or the shown translation
     when a passage carries one. Media and blank screens carry no caption. */
  function linesOf(screen, translation) {
    if (!screen || screen.blank) return [];
    var variant = translation && screen.translations ? screen.translations[translation] : null;
    if (variant && variant.line) return [variant.line];
    if (!screen.lines || !screen.lines.length) return [];
    return screen.lines.map(function (line) {
      return String(line.text || '').trim();
    }).filter(Boolean);
  }

  function paint(lines) {
    var signature = lines.join('\u0000');
    if (signature === painted) return;
    painted = signature;
    if (!lines.length) {
      stage.replaceChildren();
      return;
    }
    var caption = document.createElement('p');
    caption.className = 'obs-overlay__caption';
    lines.forEach(function (text) {
      var span = document.createElement('span');
      span.textContent = text;
      caption.appendChild(span);
    });
    stage.replaceChildren(caption);
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
        var island = parsed.getElementById('projectorScreenData');
        if (!island) { callbacks.forEach(function (fn) { fn(null); }); return; }
        cache[service] = JSON.parse(island.textContent) || [];
        callbacks.forEach(function (fn) { fn(cache[service]); });
      })
      .catch(function () {
        var callbacks = pending[service] || [];
        delete pending[service];
        callbacks.forEach(function (fn) { fn(null); });
      });
  }

  function sync() {
    var state = readState();
    if (!state.service || state.on !== true) { paint([]); return; }
    ensure(state.service, function (screens) {
      if (!screens) { paint([]); return; }
      /* The state may have moved on while the fetch was in the air. */
      var latest = readState();
      if (latest.service !== state.service) return;
      paint(linesOf(screens[Math.max(0, latest.screen)] || null, latest.translation));
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

  sync();
})();
