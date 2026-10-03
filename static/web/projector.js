/* The projector (spec 006, slice 4).
 *
 * One slide at a time, fitted to the screen, with three controls: previous, next
 * and an on/off toggle. The page arrives with every slide already rendered, so
 * moving is instant and nothing has to be fetched to show the next line.
 *
 * It shares the display state with the app's tabs over the same channel (see
 * web/display.js): whatever the operator does here, the shell hears. Update
 * re-reads the whole page -- that is how a song whose lyrics changed reaches the
 * screen -- and the slide that was showing stays where it was.
 */
(function () {
  'use strict';

  var body = document.body;
  var channelName = body.dataset.displayChannel || 'gkps-service-display';
  var service = Number(body.dataset.service);
  var screen = document.getElementById('projectorScreen');
  var stage = document.getElementById('projectorSlides');
  var KEY = 'gkps-display';

  var channel = null;
  try { channel = new BroadcastChannel(channelName); } catch (e) { channel = null; }

  var current = body.dataset.currentSlide || '';
  var showing = body.dataset.showing === 'true';

  function slides() {
    return [].slice.call(stage.querySelectorAll('.slide'));
  }
  function slideFor(id) {
    return slides().filter(function (slide) { return slide.dataset.slide === id; })[0] || null;
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

  /* The old projector's habit, kept: the title shrinks until it fits the width, the
     body until it fits what is left of the screen. */
  function fit(slide) {
    if (!slide) return;
    var title = slide.querySelector('.slide__title');
    var text = slide.querySelector('.slide__body');
    var size, limit;

    if (title) {
      title.style.fontSize = '50px';
      size = 50;
      while (title.scrollWidth > stage.clientWidth && size > 12) {
        size -= 1;
        title.style.fontSize = size + 'px';
      }
    }
    if (text) {
      text.style.fontSize = '100px';
      size = 100;
      limit = stage.clientHeight - (title ? title.offsetHeight : 0) - 8;
      while ((text.scrollHeight > limit || text.scrollWidth > stage.clientWidth) && size > 12) {
        size -= 1;
        text.style.fontSize = size + 'px';
      }
    }
  }

  /* ---------- showing ------------------------------------------------------- */

  function render(silent) {
    var found = slideFor(current);
    slides().forEach(function (slide) {
      var active = slide === found;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', active ? 'false' : 'true');
    });
    body.dataset.currentSlide = current;
    body.dataset.showing = showing ? 'true' : 'false';
    if (found) fit(found);
    var controls = {
      prev: document.querySelector('[data-projector="prev"]'),
      next: document.querySelector('[data-projector="next"]'),
      toggle: document.querySelector('[data-projector="toggle"]'),
    };
    var all = slides();
    var index = all.indexOf(found);
    if (controls.prev) controls.prev.disabled = index <= 0;
    if (controls.next) controls.next.disabled = index < 0 || index >= all.length - 1;
    if (controls.toggle) {
      controls.toggle.setAttribute('aria-pressed', showing ? 'true' : 'false');
      var label = showing ? 'Hide the display' : 'Show the display';
      controls.toggle.setAttribute('aria-label', label);   /* the name follows the state */
      controls.toggle.title = label;
    }
    if (!silent) {
      write({service: service, slide: current, on: showing});
      post(showing ? {type: 'show', service: service, slide: current} : {type: 'stop'});
    }
  }

  function move(step) {
    var all = slides();
    var index = all.indexOf(slideFor(current));
    var next = all[index + step];
    if (!next) return;
    current = next.dataset.slide;
    showing = true;
    render();
  }

  /* ---------- the three controls ------------------------------------------- */

  var prev = document.querySelector('[data-projector="prev"]');
  var next = document.querySelector('[data-projector="next"]');
  var toggle = document.querySelector('[data-projector="toggle"]');
  if (prev) prev.addEventListener('click', function () { move(-1); });
  if (next) next.addEventListener('click', function () { move(1); });
  if (toggle) {
    toggle.addEventListener('click', function () {
      showing = !showing;
      render();
    });
  }

  /* The operator's own gesture asks for the screen, rather than the window grabbing
     it on the way in. Escape from the browser gives it back. */
  if (screen) {
    screen.addEventListener('click', function (event) {
      if (document.fullscreenElement) return;
      if (event.target.closest('.projector__bar')) return;
      var root = document.documentElement;
      if (root.requestFullscreen) root.requestFullscreen().catch(function () { /* declined */ });
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
        current = message.slide || current;
        showing = true;
        render(true);
      } else if (message.type === 'stop') {
        showing = false;
        render(true);
      } else if (message.type === 'update') {
        reflow();
      } else if (message.type === 'state' && showing) {
        post({type: 'show', service: service, slide: current});
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
        var fresh = parsed.getElementById('projectorSlides');
        if (!fresh) return;
        stage.innerHTML = fresh.innerHTML;
        render(true);
      })
      .catch(function () { /* keep showing what we have */ });
  }

  /* A window opened for a service that is already displaying lands on its slide. */
  var stored = read();
  if (stored && Number(stored.service) === service && stored.slide) {
    current = stored.slide;
    showing = stored.on === true;
  } else if (stored && stored.on && Number(stored.service) !== service) {
    showing = false;
  }
  render(true);
  window.addEventListener('resize', function () { fit(slideFor(current)); });
  post({type: 'state'});                 /* ask the other tabs what is on screen */
  if (channel) channel.postMessage({type: 'state'});
})();
