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

  /* ---------- fitting the words to the screen -------------------------------
     The current projector's own two loops, kept in its shape -- do...while, one pixel at
     a time, from 50 for the title and 100 for the text, floor 2 -- so the words come out
     as large as they can be and no larger: the loop stops at the first size that fits,
     which is one pixel more than the first size that does not.

     Two things differ from the original, both deliberate: the measure is the display's
     own box rather than the window, and the text's condition also reads the INK's box --
     a wrapped block can report a height a few pixels inside the words' real extents, and
     the last line then hangs over the bottom edge. */

  function resizeTitleFont(head) {
    if (!head) return;
    var fontSize = 50;
    do {
      head.style.fontSize = fontSize + 'px';
      fontSize -= 1;
      /* Strictly greater, against the display's own box: the original compared
         `>= window - 72`, which only works because the window is a different box from
         the element's parent. Measured against its own parent, a full-width block is
         always ">= clientWidth - margin", and the loop would run to the floor. */
    } while ((head.scrollWidth > stage.clientWidth
              || head.scrollHeight > stage.clientHeight * 0.45) && fontSize > 10);
  }

  function resizeTextFont(head, lines) {
    if (!lines) return;
    var box = stage.getBoundingClientRect();
    var range = document.createRange();
    var overflows = function () {
      if (lines.scrollHeight > stage.clientHeight - (head ? head.offsetHeight : 0) - 8) {
        return true;
      }
      range.selectNodeContents(lines);
      var ink = range.getBoundingClientRect();
      return (ink.top < box.top + 4 || ink.bottom > box.bottom - 4
              || ink.left < box.left - 1 || ink.right > box.right + 2);
    };
    var fontSize = 100;
    do {
      lines.style.fontSize = fontSize + 'px';
      fontSize -= 1;
    } while (overflows() && fontSize > 1);
  }

  function fit(active) {
    if (!active) return;
    var head = active.querySelector('.screen__head');
    var lines = active.querySelector('.screen__lines');
    resizeTitleFont(head);
    resizeTextFont(head, lines);
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
      var on = each === active;
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
    if (active) fit(active);
    if (!silent) {
      write({service: service, screen: current, on: showing});
      post(showing ? {type: 'show', service: service, screen: current} : {type: 'stop'});
    }
    beat();          /* every change is also a sign of life */
  }

  var direction = 1;
  var previousIndex = current;

  function move(step) {
    var next = current + step;
    if (next < 0 || next > screens().length - 1) return;
    direction = step;
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
  /* The sign of life, and the reason a shell can tell that this window has gone: while it
     is open it shows up every couple of seconds, and when it closes the stamps stop. */
  window.setInterval(beat, 2000);
  document.addEventListener('visibilitychange', beat);
  window.addEventListener('focus', beat);
  post({type: 'state'});                 /* ask the other tabs what is on screen */
})();
