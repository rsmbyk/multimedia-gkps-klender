/* The browser session that owns the display state (spec 184).
 *
 * Which Tata Ibadah is on air may not outlive the browser that started it. The state
 * carries a `session` stamp, and the stamp's value lives in `gkps-session` — a cookie
 * with no expiry, the browser's own definition of "this session". Closing a dock, a
 * projector, the overlay or every surface changes nothing; the browser session ending
 * makes the stored state foreign, and every surface reads it as no state.
 *
 * Loaded before display.js, projector.js and obs-overlay.js. They ask `owns()` whether
 * a stored object belongs to the live session and stamp what they write with `stamp()`.
 * The marker carries no service, screen, translation or operator: one opaque id.
 */
(function () {
  'use strict';

  var NAME = 'gkps-session';
  var memory = '';              /* the page's own id when cookies are unavailable */

  function readCookie() {
    try {
      var match = document.cookie.match(/(?:^|;\s*)gkps-session=([^;]+)/);
      return match ? decodeURIComponent(match[1]) : '';
    } catch (e) {
      return '';
    }
  }

  function candidate() {
    try {
      if (window.crypto && window.crypto.randomUUID) return window.crypto.randomUUID();
    } catch (e) { /* fall through to the older shape */ }
    return Date.now().toString(36) + '.' + Math.random().toString(36).slice(2);
  }

  /* The live marker, or '' when this page has neither read nor minted one. */
  function current() {
    return readCookie() || memory;
  }

  /* The marker to stamp a write with. A session with none mints one, and a mint takes
     the value the jar holds AFTER writing: two surfaces starting together then agree
     on the last value written instead of stamping one the session no longer holds. */
  function stamp() {
    var held = current();
    if (held) return held;
    var made = candidate();
    try {
      document.cookie = NAME + '=' + encodeURIComponent(made) + '; path=/; SameSite=Lax';
    } catch (e) { /* a browser that refuses cookies */ }
    held = readCookie();
    if (held) return held;
    /* No cookie storage: this page is its own session. The display works for the life
       of the page; a reload starts idle (spec 184 FR-006). */
    memory = memory || made;
    return memory;
  }

  /* Does a stored display state belong to this browser session? A state with no stamp,
     or one from another session, is no state at all. */
  function owns(stored) {
    if (!stored || typeof stored !== 'object') return false;
    var held = current();
    return !!held && stored.session === held;
  }

  window.GKPSDisplaySession = {current: current, stamp: stamp, owns: owns};
})();
