/* The projector (spec 006, slice 4).
 *
 * White on black, one screen at a time, and nothing else on it: the operator drives
 * it from the keyboard -- left and right to move, space to turn the display on and
 * off. The page arrives with every screen already rendered, so moving is instant and
 * nothing has to be fetched to show the next two lines.
 *
 * It shares the display state with the app's tabs over the same channel (see
 * web/display.js): whatever the operator does here, the shell hears. Update re-reads
 * the whole page -- how a song whose lyrics changed reaches the screen -- and the
 * screen that was showing stays where it was.
 */
(function () {
  'use strict';

  var body = document.body;
  var channelName = body.dataset.displayChannel || 'gkps-service-display';
  var service = Number(body.dataset.service);
  var screen = document.getElementById('projectorScreen');
  var stage = document.getElementById('projectorScreens');
  var KEY = 'gkps-display';

  var channel = null;
  try { channel = new BroadcastChannel(channelName); } catch (e) { channel = null; }

  var current = Number(body.dataset.currentScreen || 0);
  var showing = body.dataset.showing === 'true';

  function screens() {
    return [].slice.call(stage.querySelectorAll('.screen'));
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

  /* ---------- fitting the words to the screen ------------------------------- */

  /* The current projector's habit, kept: the header shrinks until it fits the width,
     the words until they fit what is left of the screen. */
  function fit(active) {
    if (!active) return;
    var head = active.querySelector('.screen__head');
    var lines = active.querySelector('.screen__lines');
    var size, limit;

    if (head) {
      head.style.fontSize = '50px';
      size = 50;
      while (head.scrollWidth > stage.clientWidth && size > 12) {
        size -= 1;
        head.style.fontSize = size + 'px';
      }
    }
    if (lines) {
      lines.style.fontSize = '100px';
      size = 100;
      limit = stage.clientHeight - (head ? head.offsetHeight : 0) - 8;
      while ((lines.scrollHeight > limit || lines.scrollWidth > stage.clientWidth) && size > 12) {
        size -= 1;
        lines.style.fontSize = size + 'px';
      }
    }
  }

  /* ---------- showing ------------------------------------------------------- */

  function render(silent) {
    var all = screens();
    if (current < 0) current = 0;
    if (all.length && current > all.length - 1) current = all.length - 1;
    var active = all[current] || null;

    all.forEach(function (each) {
      var on = each === active;
      each.classList.toggle('is-active', on);
      each.setAttribute('aria-hidden', on ? 'false' : 'true');
    });
    body.dataset.currentScreen = String(current);
    body.dataset.showing = showing ? 'true' : 'false';
    if (active) fit(active);
    if (!silent) {
      write({service: service, screen: current, on: showing});
      post(showing ? {type: 'show', service: service, screen: current} : {type: 'stop'});
    }
  }

  function move(step) {
    var next = current + step;
    if (next < 0 || next > screens().length - 1) return;
    current = next;
    showing = true;
    render();
  }

  /* ---------- the operator's keyboard ---------------------------------------
     Left and right move; space turns the display on and off. Nothing is drawn for
     these: the screen carries only the header and the words. */

  document.addEventListener('keydown', function (event) {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown' || event.key === 'PageDown') {
      event.preventDefault();
      move(1);
    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp' || event.key === 'PageUp') {
      event.preventDefault();
      move(-1);
    } else if (event.key === ' ' || event.key === 'Spacebar' || event.key === 'Enter') {
      event.preventDefault();
      showing = !showing;
      render();
    } else if (event.key === 'Home') {
      event.preventDefault();
      current = 0;
      render();
    } else if (event.key === 'End') {
      event.preventDefault();
      current = screens().length - 1;
      render();
    }
  });

  /* The operator's own gesture asks for the screen, rather than the window grabbing
     it on the way in. Escape from the browser gives it back. */
  if (screen) {
    screen.addEventListener('click', function () {
      if (document.fullscreenElement) return;
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen().catch(function () { /* declined */ });
      }
    });
  }

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
    fetch(window.location.href, {credentials: 'same-origin'})
      .then(function (response) { return response.ok ? response.text() : ''; })
      .then(function (html) {
        if (!html) return;
        var parsed = new DOMParser().parseFromString(html, 'text/html');
        var fresh = parsed.getElementById('projectorScreens');
        if (!fresh) return;
        stage.innerHTML = fresh.innerHTML;
        render(true);
      })
      .catch(function () { /* keep showing what we have */ });
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
  window.addEventListener('resize', function () { render(true); });
  post({type: 'state'});                 /* ask the other tabs what is on screen */
})();
