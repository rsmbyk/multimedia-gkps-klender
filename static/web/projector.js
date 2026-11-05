/* The service projector (specs 006 and 091).
 *
 * One service screen at a time, with quiet corner controls for keyboard or mouse.
 * The page arrives with every service screen rendered, so ordinary steps are instant.
 *
 * It shares the display state with the app's tabs over the same channel (see
 * web/display.js): whatever the operator does here, the shell hears. Update re-reads
 * the whole page -- how a song whose lyrics changed reaches the screen -- and the
 * screen that was showing stays where it was. Spec 026: the shell asks for that same
 * re-read after every saved change, so the screen follows an edit without a press.
 */
(function () {
  'use strict';

  var body = document.body;
  var channelName = body.dataset.displayChannel || 'gkps-service-display';
  var service = Number(body.dataset.service);
  if (!service) {
    /* /projector?service=<id> — the adoption parameter is also the page's own
       service before the state says otherwise (spec 119). */
    var adoptParam = new URLSearchParams(window.location.search).get('service');
    if (adoptParam) service = Number(adoptParam);
    body.dataset.service = String(service);
  }
  var screen = document.getElementById('projectorScreen');
  var stage = document.getElementById('projectorScreens');
  var entries = JSON.parse(document.getElementById('projectorEntryData').textContent) || [];
  var screenData = JSON.parse(document.getElementById('projectorScreenData').textContent) || [];
  var KEY = 'gkps-display';

  var channel = null;
  try { channel = new BroadcastChannel(channelName); } catch (e) { channel = null; }

  var current = Number(body.dataset.currentScreen || 0);
  var showing = body.dataset.showing === 'true';
  var imageHost = null;
  var imageController = null;
  var imageUrl = null;
  var imageToken = 0;
  var audioHost = null;
  var audioController = null;
  var audioPlayer = null;
  var audioUrl = null;
  var audioToken = 0;
  var audioIdleTimer = null;
  var audioWasFullscreen = false;
  var audioFullscreenToken = 0;
  var videoHost = null;
  var videoController = null;
  var videoPlayer = null;
  var videoUrl = null;
  var videoToken = 0;
  var videoIdleTimer = null;
  var videoWasFullscreen = false;
  var videoFullscreenToken = 0;
  var pdfHost = null;
  var pdfDocument = null;
  var pdfController = null;
  var pdfPaintController = null;
  var pdfToken = 0;
  var pdfPage = 1;
  var pdfEnterFromEnd = false;

  /* ---------- fitting a media screen to the stage (spec 158) ------------------
     The fit is the smaller of the stage's two ratios, above 1 as well as below; `T`
     takes the other ratio instead, and the excess either leaves is panned by dragging
     or with the wheel. It belongs to the active media host: another entry starts at
     the fit again, another page of the same document keeps it. */
  var fitHost = null;
  var fitState = 'fit';                 // 'fit' | 'width' | 'height'
  var fitOwn = null;                    // the media's own size: pixels for an image, points for a page
  var fitPan = {x: 0, y: 0};
  var fitOverflow = {x: 0, y: 0};

  function audioActivity() {
    if (!audioHost) return;
    audioHost.classList.remove('is-idle');
    clearTimeout(audioIdleTimer);
    if (audioPlayer && !audioPlayer.audio.paused) {
      audioIdleTimer = setTimeout(function () {
        if (audioHost && audioPlayer && !audioPlayer.audio.paused) audioHost.classList.add('is-idle');
      }, 3500);
    }
  }
  document.addEventListener('pointermove', audioActivity);
  document.addEventListener('pointerdown', audioActivity);
  document.addEventListener('keydown', audioActivity);

  function videoActivity() {
    if (!videoHost) return;
    videoHost.classList.remove('is-idle');
    clearTimeout(videoIdleTimer);
    if (videoPlayer && !videoPlayer.video.paused) {
      videoIdleTimer = setTimeout(function () {
        if (videoHost && videoPlayer && !videoPlayer.video.paused) videoHost.classList.add('is-idle');
      }, 2000);
    }
  }
  document.addEventListener('pointermove', videoActivity);
  document.addEventListener('pointerdown', videoActivity);
  document.addEventListener('keydown', videoActivity);

  /* Spec 155: a playing recording takes the screen the way a playing video does —
     the audio box becomes the fullscreen element, so the corner cue and the mouse
     zones are off screen and the only way back is to pause. */
  function audioPlaying() {
    return Boolean(audioHost && audioPlayer && !audioPlayer.audio.paused);
  }
  function requestAudioFullscreen(host) {
    if (!host || !host.requestFullscreen) return;
    var token = ++audioFullscreenToken;
    var request;
    try { request = host.requestFullscreen(); }
    catch (error) { return; }
    Promise.resolve(request).then(function () {
      if (token !== audioFullscreenToken || host !== audioHost || !audioPlaying())
        exitAudioFullscreen(host);
    }).catch(function () { /* The recording remains playable in the normal projector area. */ });
  }
  function exitAudioFullscreen(host) {
    audioFullscreenToken++;
    var currentFullscreen = document.fullscreenElement;
    if (currentFullscreen && (currentFullscreen === host
        || currentFullscreen.classList.contains('screen__audio-box'))) {
      document.exitFullscreen().catch(function () {});
    }
  }
  function syncAudioFullscreen() {
    var isAudioFullscreen = Boolean(audioHost && document.fullscreenElement === audioHost);
    /* Leaving the fullscreen screen by Escape (or any browser gesture) pauses the
       recording, so it never plays on under the normal projector page. */
    if (audioWasFullscreen && !isAudioFullscreen && audioPlaying()) audioPlayer.pause();
    audioWasFullscreen = isAudioFullscreen;
    if (isAudioFullscreen) audioActivity();
  }

  function clearAudioScreen() {
    audioToken++;
    clearTimeout(audioIdleTimer);
    if (audioController) audioController.abort();
    audioController = null;
    if (audioPlayer) audioPlayer.stop();
    audioPlayer = null;
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    audioUrl = null;
    if (audioHost) audioHost.classList.remove('is-idle');
    audioHost = null;
  }
  function renderAudioScreen(active) {
    var host = showing && !detour && active && active.querySelector('[data-media-audio]');
    if (host === audioHost) return;
    clearAudioScreen();
    if (!host) return;
    audioHost = host;
    var player = host.querySelector('.screen__audio-player');
    var missing = host.querySelector('.screen__image-missing');
    player.hidden = true;
    missing.setAttribute('hidden', '');
    audioController = new AbortController();
    var token = ++audioToken;
    window.GKPSMediaAudio.load(host.dataset.mediaAudio, audioController.signal).then(function (url) {
      if (token !== audioToken || host !== audioHost) { URL.revokeObjectURL(url); return; }
      audioUrl = url;
      audioPlayer = window.GKPSMediaAudio.attach(host, {
        onReady: function () { if (token === audioToken) player.hidden = false; },
        onError: function () { if (token === audioToken) { clearAudioScreen(); missing.removeAttribute('hidden'); } },
        onPlayRequest: function () { if (token === audioToken) requestAudioFullscreen(host); },
        onPlayback: function (playing) {
          if (token !== audioToken) return;
          audioActivity();
          if (!playing) exitAudioFullscreen(host);
        }
      });
      audioPlayer.setUrl(url);
    }).catch(function () {
      if (token === audioToken && host === audioHost) missing.removeAttribute('hidden');
    }).finally(function () { if (token === audioToken) audioController = null; });
  }

  function clearVideoScreen() {
    videoToken++;
    clearTimeout(videoIdleTimer);
    if (videoController) videoController.abort();
    videoController = null;
    if (videoPlayer) videoPlayer.stop();
    videoPlayer = null;
    if (videoUrl) URL.revokeObjectURL(videoUrl);
    videoUrl = null;
    if (videoHost) {
      videoHost.classList.remove('is-idle', 'is-fullscreen');
      var video = videoHost.querySelector('video');
      var missing = videoHost.querySelector('.screen__video-missing');
      if (video) video.hidden = true;
      if (missing) missing.setAttribute('hidden', '');
    }
    videoHost = null;
    videoWasFullscreen = false;
    exitVideoFullscreen();
  }

  function renderVideoScreen(active) {
    var host = showing && !detour && active && active.querySelector('[data-media-video]');
    if (host === videoHost) return;
    clearVideoScreen();
    if (!host) return;
    videoHost = host;
    var video = host.querySelector('video');
    var play = host.querySelector('.screen__video-play');
    var missing = host.querySelector('.screen__video-missing');
    video.hidden = true;
    missing.setAttribute('hidden', '');
    play.dataset.playing = 'false';
    play.setAttribute('aria-label', 'Play video');
    videoController = new AbortController();
    var token = ++videoToken;
    window.GKPSMediaVideo.load(host.dataset.mediaVideo, videoController.signal).then(function (url) {
      if (token !== videoToken || host !== videoHost) { URL.revokeObjectURL(url); return; }
      videoUrl = url;
      videoPlayer = window.GKPSMediaVideo.attach(host, {
        onReady: function () {
          if (token !== videoToken) return;
          video.hidden = false;
        },
        onPlayRequest: function () {
          if (token === videoToken) {
            videoActivity();
            requestVideoFullscreen(host);
          }
        },
        onPlayback: function (playing) {
          if (token !== videoToken) return;
          videoActivity();
          if (!playing) exitVideoFullscreen(host);
        },
        onError: function () {
          if (token !== videoToken) return;
          video.hidden = true;
          missing.removeAttribute('hidden');
          clearVideoScreen();
          missing.removeAttribute('hidden');
        }
      });
      videoPlayer.setUrl(url);
      videoController = null;
    }).catch(function () {
      if (token === videoToken && host === videoHost) missing.removeAttribute('hidden');
    }).finally(function () { if (token === videoToken) videoController = null; });
  }

  function clearImageScreen() {
    imageToken++;
    if (imageController) imageController.abort();
    imageController = null;
    if (imageUrl) URL.revokeObjectURL(imageUrl);
    imageUrl = null;
    if (imageHost) {
      var image = imageHost.querySelector('.screen__image');
      clearFit(imageHost, image);
      if (image) { image.hidden = true; image.removeAttribute('src'); }
      imageHost.querySelector('.screen__image-missing').setAttribute('hidden', '');
    }
    imageHost = null;
  }

  /* The fitted size is written in px: `object-fit` can fill a box but it cannot express
     fit width (which is the fit's other state), and the pan needs a number to clamp. */
  function beginFit(host) {
    if (host === fitHost) return;
    fitHost = host; fitState = 'fit'; fitPan = {x: 0, y: 0};
  }

  function fitScale(box, own) {
    var byWidth = box.width / own.w;
    var byHeight = box.height / own.h;
    return fitState === 'width' ? byWidth : fitState === 'height' ? byHeight
      : Math.min(byWidth, byHeight);
  }

  function applyFit(host, element, size, box) {
    var screen = host.closest('.screen');
    if (screen) screen.classList.add('is-fitted');
    setFitOverflow(size, box);
    applyPan(element);
  }

  function fitMedia(host, element, natural) {
    beginFit(host);
    fitOwn = natural;
    var box = host.getBoundingClientRect();
    var scale = fitScale(box, natural);
    var size = {w: Math.floor(natural.w * scale), h: Math.floor(natural.h * scale)};
    element.style.width = size.w + 'px';
    element.style.height = size.h + 'px';
    applyFit(host, element, size, box);
    return size;
  }

  function setFitOverflow(size, box) {
    fitOverflow = {x: Math.max(0, (size.w - box.width) / 2),
                   y: Math.max(0, (size.h - box.height) / 2)};
    body.classList.toggle('media-overflow', Boolean(fitOverflow.x || fitOverflow.y));
  }

  /* Half the overflow each way: the media is centred in its box, so that is the travel
     that brings either of its edges to the stage's edge, and no further. */
  function applyPan(element) {
    fitPan.x = Math.min(fitOverflow.x, Math.max(-fitOverflow.x, fitPan.x));
    fitPan.y = Math.min(fitOverflow.y, Math.max(-fitOverflow.y, fitPan.y));
    element.style.transform = fitPan.x || fitPan.y
      ? 'translate(' + Math.round(fitPan.x) + 'px,' + Math.round(fitPan.y) + 'px)' : '';
  }

  function clearFit(host, element) {
    var screen = host && host.closest && host.closest('.screen');
    if (screen) screen.classList.remove('is-fitted');
    if (element) {
      element.style.width = '';
      element.style.height = '';
      element.style.transform = '';
    }
    if (host === fitHost) {
      fitHost = null; fitState = 'fit'; fitOwn = null; fitPan = {x: 0, y: 0};
    }
    fitOverflow = {x: 0, y: 0};
    body.classList.remove('media-overflow');
  }

  /* `T`: the fit is one of the two states, so this always offers the other one, and the
     pan starts again from the centre. */
  function toggleFit() {
    var host = imageHost || pdfHost;
    if (!host || !fitOwn) return;
    var box = host.getBoundingClientRect();
    var defaultState = box.width / fitOwn.w < box.height / fitOwn.h ? 'width' : 'height';
    fitState = (fitState === 'fit' ? defaultState : fitState) === 'width' ? 'height' : 'width';
    fitPan = {x: 0, y: 0};
    if (imageHost) refitImage();
    else if (pdfDocument) paintPDFScreen();
  }

  function refitImage() {
    if (!imageHost) return;
    var image = imageHost.querySelector('.screen__image');
    if (image && image.naturalWidth) {
      fitMedia(imageHost, image, {w: image.naturalWidth, h: image.naturalHeight});
    }
  }

  function renderImageScreen(active) {
    var host = showing && !detour && active && active.querySelector('[data-media-image]');
    if (host === imageHost) return;
    clearImageScreen();
    if (!host) return;
    imageHost = host;
    var image = host.querySelector('.screen__image');
    var missing = host.querySelector('.screen__image-missing');
    image.hidden = true;
    missing.setAttribute('hidden', '');
    imageController = new AbortController();
    var token = ++imageToken;
    window.GKPSMediaImage.load(host.dataset.mediaImage, imageController.signal)
      .then(function (result) {
        if (token !== imageToken || host !== imageHost) {
          URL.revokeObjectURL(result.url); return;
        }
        imageUrl = result.url;
        image.src = imageUrl;
        image.hidden = false;
        fitMedia(host, image, {w: result.width, h: result.height});
      }).catch(function () {
        if (token === imageToken && host === imageHost) missing.removeAttribute('hidden');
      });
  }

  function clearPDFScreen() {
    body.classList.remove('pdf-unavailable');
    pdfToken++;
    if (pdfController) pdfController.abort();
    if (pdfPaintController) pdfPaintController.abort();
    pdfController = pdfPaintController = null;
    if (pdfDocument) pdfDocument.destroy();
    pdfDocument = null;
    if (pdfHost) {
      var canvas = pdfHost.querySelector('canvas');
      clearFit(pdfHost, canvas);
      canvas.hidden = true;
      canvas.width = canvas.height = 0;
    }
    pdfHost = null;
    pdfPage = 1;
  }

  function paintPDFScreen() {
    if (!pdfDocument || !pdfHost) return;
    if (pdfPaintController) pdfPaintController.abort();
    pdfPaintController = new AbortController();
    var signal = pdfPaintController.signal;
    var token = ++pdfToken;
    var host = pdfHost;
    var previous = pdfHost.querySelector('canvas');
    var canvas = previous.cloneNode(false);
    previous.replaceWith(canvas);
    var missing = pdfHost.querySelector('.screen__pdf-missing');
    var bounds = pdfHost.getBoundingClientRect();
    beginFit(pdfHost);
    window.GKPSMediaPDF.paint(pdfDocument, pdfPage, canvas, bounds.width, bounds.height, signal,
      {fit: fitState, upscale: true})
      .then(function (size) {
        if (signal.aborted || token !== pdfToken || host !== pdfHost) return;
        canvas.hidden = false;
        missing.setAttribute('hidden', '');
        body.classList.remove('pdf-unavailable');
        fitOwn = size.own;
        applyFit(host, canvas, {w: Math.floor(size.width), h: Math.floor(size.height)}, bounds);
        renderCue();
      }).catch(function () {
        if (signal.aborted || token !== pdfToken) return;
        canvas.hidden = true;
        missing.removeAttribute('hidden');
        body.classList.add('pdf-unavailable');
      });
  }

  function renderPDFScreen(active) {
    var host = showing && !detour && active && active.querySelector('[data-media-pdf], [data-media-slides]');
    if (host === pdfHost) return;
    clearPDFScreen();
    if (!host) return;
    pdfHost = host;
    host.querySelector('canvas').hidden = true;
    host.querySelector('.screen__pdf-missing').setAttribute('hidden', '');
    pdfController = new AbortController();
    var signal = pdfController.signal;
    var token = ++pdfToken;
    var loading = host.dataset.mediaSlides
      ? window.GKPSMediaPDF.loadSlides(host.dataset.mediaSlides, signal)
      : window.GKPSMediaPDF.load(host.dataset.mediaPdf, signal);
    loading.then(function (document) {
      if (signal.aborted || token !== pdfToken || host !== pdfHost) { document.destroy(); return; }
      pdfDocument = document;
      pdfPage = pdfEnterFromEnd ? document.numPages : 1;
      pdfEnterFromEnd = false;
      paintPDFScreen();
    }).catch(function () {
      if (signal.aborted || token !== pdfToken || host !== pdfHost) return;
      host.querySelector('.screen__pdf-missing').removeAttribute('hidden');
      body.classList.add('pdf-unavailable');
    });
  }
  window.addEventListener('resize', function () {
    refitImage();
    if (pdfDocument && pdfHost) paintPDFScreen();
  });

  function screens() {
    return [].slice.call(stage.querySelectorAll('.screen[data-screen]'));
  }
  /* The empty-service notice is the stage's sibling (projector.html), so it is not one of the
     screens `render` toggles: it follows what the stage holds — a service screen, or a Go To
     detour painted over an empty service — from one place, so no path paints over it. */
  function syncEmptyNotice() {
    var notice = screen.querySelector('.projector__empty');
    if (!notice) return;
    notice.hidden = Boolean(detour) || screens().length > 0;
  }
  function read() {
    try {
      var stored = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (stored && typeof stored === 'object' &&
          window.GKPSDisplaySession && window.GKPSDisplaySession.owns(stored)) return stored;
    } catch (e) { /* no stored state */ }
    return null;
  }
  function write(state) {
    try {
      /* A write that says nothing about the go to leaves it alone: the projector moves
         the service underneath nothing, and only a named `goto: null` ends one
         (spec 185, the shared module's own rule). */
      var held = state.goto === undefined ? ((read() || {}).goto || null) : state.goto;
      localStorage.setItem(KEY, JSON.stringify({
        service: state.service, screen: state.screen, on: state.on,
        translation: state.translation, at: state.at,
        goto: held,
        /* The session this write belongs to (spec 184). */
        session: window.GKPSDisplaySession ? window.GKPSDisplaySession.stamp() : null
      }));
    } catch (e) { /* private mode */ }
  }
  function post(message) {
    if (channel) channel.postMessage(message);
  }

  /* ---------- the beat has gone (spec 119) ----------------------------------
     The display no longer depends on any window staying open: closing every surface
     changes nothing, and only `release` ends it. No stamps, no watchdogs. */

  /* ---------- fitting the words to the accepted projector stage ------------ */
  var GOLDEN_RATIO = (1 + Math.sqrt(5)) / 2;

  function overflows(head, lines) {
    if (head && (head.scrollWidth > stage.clientWidth + 1
                 || head.getBoundingClientRect().bottom > stage.getBoundingClientRect().bottom)) return true;
    if (!lines) return false;
    if (lines.scrollHeight > lines.clientHeight + 1) return true;
    var range = document.createRange();
    range.selectNodeContents(lines);
    var ink = range.getBoundingClientRect();
    var box = lines.getBoundingClientRect();
    var stageBox = stage.getBoundingClientRect();
    return ink.left < box.left - 1 || ink.right > box.right + 1
      || ink.top < box.top - 2 || ink.bottom > box.bottom + 2
      || ink.top < stageBox.top - 1 || ink.bottom > stageBox.bottom + 1;
  }

  function truncateText(head, lines) {
    if (!lines || !overflows(head, lines)) return;
    var rows = [].slice.call(lines.querySelectorAll('.screen__line'));
    while (rows.length > 1 && overflows(head, lines)) rows.pop().remove();
    var last = lines.querySelector('.screen__line:last-child');
    if (!last) return;
    while (last.textContent.length && overflows(head, lines)) {
      last.textContent = last.textContent.slice(0, -1);
    }
    last.textContent = last.textContent.replace(/\s+$/, '') + '\u2026';
  }

  function fit(active) {
    if (!active) return;
    var head = active.querySelector('.screen__head');
    var lines = active.querySelector('.screen__lines');
    if (!lines) return;
    for (var size = 200; size >= 2; size -= 1) {
      lines.style.fontSize = size + 'px';
      if (head) head.style.fontSize = (size / GOLDEN_RATIO) + 'px';
      if (!overflows(head, lines)) break;
    }
    if (active.dataset.fit === 'single') truncateText(head, lines);
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
      var on = each === active && !detour;
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
    body.classList.toggle('words-hidden', !showing);
    /* Before anything is fitted: the notice's band is part of the stage only while the notice
       is painted, so the fit below must measure the stage it will actually live in. */
    syncEmptyNotice();
    if (active && !detour) {
      applyPassageTranslation(active);
      fit(active);
    }
    renderImageScreen(active);
    renderAudioScreen(active);
    renderVideoScreen(active);
    renderPDFScreen(active);
    renderCue();
    if (!silent) {
      write({service: service, screen: current, on: showing,
             translation: translation || null, at: Date.now()});
      post(showing ? {type: 'show', service: service, screen: current} : {type: 'hide'});
    }
  }

  var direction = 1;
  var previousIndex = current;

  function move(step) {
    if (detour) { stepGoto(step, 'plain'); return; }
    if (pdfHost && pdfDocument && pdfPage + step >= 1 && pdfPage + step <= pdfDocument.numPages) {
      pdfPage += step;
      paintPDFScreen();
      renderCue();
      return;
    }
    var next = current + step;
    if (next < 0 || next > screens().length - 1) return;
    pdfEnterFromEnd = step < 0 && Boolean(screens()[next].querySelector('[data-media-pdf], [data-media-slides]'));
    direction = step;
    if (entryAt(next) !== entryAt(current)) translation = '';
    current = next;
    showing = true;
    render();
  }

  /* ---------- quiet HUD and shared input operations ------------------------ */
  var cue = document.getElementById('corner-cue');
  var cueService = document.getElementById('cue-service');
  var cuePrefix = document.getElementById('cue-prefix');
  var baitList = document.getElementById('cue-baits');
  var cueProgress = document.getElementById('cue-progress');
  var cueNext = document.getElementById('cue-next');
  var cueArrow = document.getElementById('cue-arrow');
  var cueNextName = document.getElementById('cue-next-name');
  var keysButton = document.querySelector('.keys');
  var entryList = document.getElementById('entry-list');
  var entryDismiss = document.getElementById('entry-list-dismiss');
  var entryListSearch = document.getElementById('entry-list-search');
  var entryListClear = document.getElementById('entry-list-clear');
  var entryListResults = document.getElementById('entry-list-results');
  var entryListMatches = [];
  var entryListChoice = 0;
  var findPanel = document.getElementById('projectorFind');
  var findDismiss = document.getElementById('projectorFindDismiss');
  var findInput = document.getElementById('projectorFindInput');
  var findClear = document.getElementById('projectorFindClear');
  var findResults = document.getElementById('projectorFindResults');
  var findSuggestion = findResults.querySelector('.projector-find__suggestion');
  var findCount = findResults.querySelector('.projector-find__count');
  var translation = '';
  var translationTimer;
  var findKind = '';
  var findRows = [];
  var findChoice = 0;
  var detour = null;
  var runningCueLabels = [];

  function clearRunningCueLabels() {
    runningCueLabels.forEach(function (node) { if (node.stopRun) node.stopRun(); });
    runningCueLabels = [];
    cue.classList.remove('cue--fit-text');
    delete cue.dataset.runningLimit;
    cueNextName.classList.remove('cue-running');
    delete cueNextName.dataset.fullText;
    cueNextName.onpointerenter = null;
    cueNextName.onpointerleave = null;
    cueNextName.style.width = '';
  }
  function makeRunningCueLabel(node, full) {
    node.classList.add('cue-running');
    node.dataset.fullText = full;
    var still = document.createElement('span');
    still.className = 'cue-running__still';
    var moving = document.createElement('span');
    moving.className = 'cue-running__moving';
    moving.textContent = full;
    node.replaceChildren(still, moving);
    var animation;
    node.stopRun = function () {
      if (animation) animation.cancel();
      animation = null;
      node.classList.remove('is-running');
      node.style.width = '';
    };
    node.onpointerenter = function () {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      node.stopRun();
      node.style.width = node.getBoundingClientRect().width + 'px';
      node.classList.add('is-running');
      var distance = Math.max(0, moving.scrollWidth - node.clientWidth);
      if (!distance) { node.stopRun(); return; }
      animation = moving.animate([
        {transform: 'translateX(0)'},
        {transform: 'translateX(0)', offset: .1},
        {transform: 'translateX(-' + distance + 'px)', offset: .9},
        {transform: 'translateX(-' + distance + 'px)'}
      ], {duration: Math.max(4000, distance / 45 * 1000), easing: 'linear', iterations: Infinity});
    };
    node.onpointerleave = node.stopRun;
    runningCueLabels.push(node);
  }
  function fitRunningCueLabels() {
    if (!runningCueLabels.length) return;
    runningCueLabels.forEach(function (node) { node.stopRun(); });
    cue.classList.add('cue--fit-text');
    function applyLimit(limit) {
      runningCueLabels.forEach(function (node) {
        var characters = Array.from(node.dataset.fullText);
        node.querySelector('.cue-running__still').textContent = characters.length > limit
          ? characters.slice(0, limit).join('') + '…' : node.dataset.fullText;
      });
    }
    var low = 1, high = 50, chosen = 1;
    while (low <= high) {
      var trial = Math.floor((low + high) / 2);
      applyLimit(trial);
      if (cue.scrollWidth <= cue.clientWidth + 1) { chosen = trial; low = trial + 1; }
      else high = trial - 1;
    }
    applyLimit(chosen);
    cue.dataset.runningLimit = String(chosen);
  }

  function bindSearchClear(input, clear) {
    function sync() { clear.hidden = !input.value; }
    clear.addEventListener('click', function (event) {
      event.stopPropagation();
      input.value = '';
      input.dispatchEvent(new Event('input', {bubbles: true}));
      input.focus();
    });
    ['input', 'change', 'search'].forEach(function (name) { input.addEventListener(name, sync); });
    sync();
    return sync;
  }
  var syncEntryListClear = bindSearchClear(entryListSearch, entryListClear);
  var syncFindClear = bindSearchClear(findInput, findClear);

  function entryAt(index) {
    var active = screens()[index];
    return active ? entries[Number(active.dataset.entry)] : null;
  }
  function entryIndex() {
    var active = screens()[current];
    return active ? Number(active.dataset.entry) : 0;
  }
  function moveTo(index) {
    if (index < 0 || index >= screens().length) return;
    pdfEnterFromEnd = false;
    direction = index >= current ? 1 : -1;
    if (entryAt(index) !== entryAt(current)) translation = '';
    current = index;
    showing = true;
    render();
  }
  function moveEntry(offset) {
    if (detour) { if (detour.kind === 'passage') stepGoto(offset, 'ctrl'); return; }
    var next = entries[entryIndex() + offset];
    if (next && next.start <= next.end) moveTo(next.start);
  }
  function moveToBait(index) {
    var entry = entryAt(current);
    if (entry && entry.type === 'song' && entry.baits[index]) moveTo(entry.baits[index].start);
  }
  function baitIndex() {
    var entry = entryAt(current);
    if (!entry || !entry.baits.length) return -1;
    return entry.baits.findIndex(function (bait) {
      return current >= bait.start && current <= bait.end;
    });
  }
  function moveBait(offset) {
    if (detour) { stepGoto(offset, detour.kind === 'passage' ? 'shift' : 'bait'); return; }
    moveToBait(baitIndex() + offset);
  }
  function unitBoundary(last, modifier) {
    if (detour) { gotoBoundary(last, modifier); return; }
    var entry = entryAt(current);
    if (!entry) return;
    if (modifier === 'ctrl') {
      var target = entries[last ? entries.length - 1 : 0];
      if (target) moveTo(target.start);
      return;
    }
    if (entry.type === 'song' && entry.baits.length) {
      var bait = entry.baits[modifier === 'shift' ? (last ? entry.baits.length - 1 : 0) : baitIndex()];
      if (bait) moveTo(last && modifier !== 'shift' ? Math.max(bait.start, bait.end - 1) : bait.start);
      return;
    }
    moveTo(last ? Math.max(entry.start, entry.end - (screenData[entry.end] && screenData[entry.end].blank ? 1 : 0)) : entry.start);
  }
  function toggleWords() { showing = !showing; render(); }
  function applyPassageTranslation(active) {
    var entry = entryAt(current);
    if (!entry || entry.type !== 'passage') return;
    var variant = ((screenData[current] || {}).translations || {})[translation || entry.translation];
    if (!variant || !active.querySelector('.screen__head')) return;
    active.querySelector('.screen__head').textContent = variant.header;
    active.querySelector('.screen__line').textContent = variant.line;
  }

  function renderCue() {
    if (!cue || !entries.length) return;
    clearRunningCueLabels();
    if (detour) { renderDetourCue(); return; }
    var entry = entryAt(current);
    if (!entry) return;
    var data = screenData[current] || {};
    var isRest = Boolean(data.blank);
    var lastBaitRest = entry.type === 'song' && isRest && baitIndex() === entry.baits.length - 1;
    baitList.replaceChildren();
    baitList.hidden = entry.type !== 'song';
    if (entry.type === 'song') {
      entry.baits.forEach(function (bait, index) {
        var key = document.createElement('button');
        key.type = 'button'; key.className = 'cue-bait';
        key.dataset.baitIndex = String(index);
        key.textContent = String(bait.number);
        key.setAttribute('aria-label', 'Go to bait ' + bait.number);
        key.setAttribute('aria-pressed', String(index === (isRest ? baitIndex() + 1 : baitIndex())));
        baitList.appendChild(key);
      });
    }
    cuePrefix.replaceChildren();
    var label = document.createElement(entry.untitled ? 'i' : 'span');
    if (entry.type === 'text' && entry.untitled) makeRunningCueLabel(label, entry.label);
    else label.textContent = entry.label + (entry.type === 'song' || entry.type === 'passage' ? ' ·' : '');
    cuePrefix.appendChild(label);
    if (entry.type === 'passage') {
      var flip = document.createElement('button');
      flip.type = 'button'; flip.className = 'cue-translation';
      flip.textContent = translation || entry.translation;
      flip.setAttribute('aria-label', 'Flip passage translation');
      cuePrefix.appendChild(document.createTextNode(' '));
      cuePrefix.appendChild(flip);
    }
    cueProgress.textContent = pdfHost && pdfDocument && !isRest
      ? pdfPage + '/' + pdfDocument.numPages
      : (!isRest && data.split_total ? data.split + '/' + data.split_total : '');
    cueNext.classList.toggle('on', entry.type === 'break' || (isRest && (entry.type !== 'song' || lastBaitRest)));
    cueArrow.classList.toggle('on', entry.type === 'break' || (isRest && (entry.type !== 'song' || lastBaitRest)));
    var next = entries[entryIndex() + 1];
    cueNext.hidden = !next;
    if (next && next.type === 'text' && next.untitled) makeRunningCueLabel(cueNextName, next.label);
    else cueNextName.textContent = next ? next.label : '';
    cueNext.setAttribute('aria-label', next ? 'Go to next entry: ' + next.label : 'No next entry');
    fitRunningCueLabels();
    renderEntryList();
  }
  function renderEntryList() {
    if (!entryList) return;
    var query = normalize(entryListSearch.value.trim());
    entryListMatches = entries.map(function (entry, index) { return index; }).filter(function (index) {
      var entry = entries[index];
      var searchable = (index + 1) + ' ' + (entry.label || 'Section break') + ' ' +
        (entry.baits.length ? 'Bait ' + entry.baits.map(function (bait) { return bait.number; }).join(', ') : '');
      return normalize(searchable).includes(query);
    });
    if (!entryListMatches.includes(entryListChoice)) entryListChoice = entryListMatches[0];
    entryListResults.replaceChildren();
    entryListMatches.forEach(function (index) {
      var entry = entries[index];
      var row = document.createElement('button');
      row.type = 'button'; row.className = 'entry-list__item';
      row.id = 'entry-list-option-' + index;
      row.setAttribute('role', 'option');
      row.dataset.entryIndex = String(index);
      if (index === entryIndex()) row.setAttribute('aria-current', 'true');
      row.dataset.active = String(index === entryListChoice);
      row.setAttribute('aria-selected', String(index === entryListChoice));
      var number = document.createElement('span');
      number.className = 'entry-list__number'; number.textContent = String(index + 1);
      var title = document.createElement('span'); title.textContent = entry.label || 'Section break';
      if (entry.baits.length) {
        var meta = document.createElement('small'); meta.className = 'entry-list__meta';
        meta.textContent = 'Bait ' + entry.baits.map(function (bait) { return bait.number; }).join(', ');
        title.appendChild(meta);
      }
      row.append(number, title); entryListResults.appendChild(row);
    });
    if (!entryListMatches.length) {
      var empty = document.createElement('div');
      empty.className = 'entry-list__empty'; empty.textContent = 'No matching entries';
      empty.setAttribute('role', 'status');
      entryListResults.appendChild(empty);
    }
    if (entryListChoice == null) entryListSearch.removeAttribute('aria-activedescendant');
    else entryListSearch.setAttribute('aria-activedescendant', 'entry-list-option-' + entryListChoice);
  }
  function scrollEntryListChoice() {
    var selected = entryList.querySelector('[data-active="true"]');
    if (!selected) return;
    var position = entryListMatches.indexOf(entryListChoice);
    if (position === entryListMatches.length - 1) entryList.scrollTop = entryList.scrollHeight;
    else if (position === 0) entryList.scrollTop = 0;
    else {
      var header = entryList.querySelector('.entry-list__header').getBoundingClientRect();
      var row = selected.getBoundingClientRect();
      var visibleHeight = entryList.clientHeight - header.height;
      entryList.scrollTop += row.top - header.bottom - (visibleHeight - row.height) / 2;
    }
  }
  function flashTranslationLabel() {
    window.clearTimeout(translationTimer);
    var flip = cuePrefix.querySelector('.cue-translation');
    if (!flip) return;
    flip.classList.add('flash');
    translationTimer = window.setTimeout(function () { flip.classList.remove('flash'); }, 1000);
  }
  function flipTranslation() {
    if (detour && detour.kind === 'passage') {
      var alternate = detour.translation === 'TB' ? 'SIM' : 'TB';
      if (!detour.translations[alternate]) return;
      detour.translation = alternate;
      renderDetour();
      flashTranslationLabel();
      return;
    }
    var entry = entryAt(current);
    if (!entry || entry.type !== 'passage') return;
    var translations = (screenData[current] || {}).translations || {};
    var currentTranslation = translation || entry.translation;
    var target = currentTranslation === 'TB' ? 'SIM' : 'TB';
    if (!translations[target]) return;
    translation = target;
    var active = screens()[current];
    active.querySelector('.screen__head').textContent = translations[target].header;
    active.querySelector('.screen__line').textContent = translations[target].line;
    renderCue(); fit(active);
    flashTranslationLabel();
  }
  var layerCloseMs = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 180;
  var keysCloseTimer, entryCloseTimer, findCloseTimer;
  function setKeysOpen(open) {
    if (open) setEntryListOpen(false);
    if (open) {
      window.clearTimeout(keysCloseTimer);
      body.classList.remove('keys-closing');
      body.classList.add('keys-open');
    } else if (body.classList.contains('keys-open')) {
      keysButton.blur();
      window.clearTimeout(keysCloseTimer);
      body.classList.remove('keys-open');
      body.classList.add('keys-closing');
      keysCloseTimer = window.setTimeout(function () {
        body.classList.remove('keys-closing');
        cue.inert = false;
        revealControls();
      }, layerCloseMs);
    }
    keysButton.setAttribute('aria-expanded', String(open));
    cue.inert = open || body.classList.contains('keys-closing');
    revealControls();
  }
  function setEntryListOpen(open) {
    if (open && body.classList.contains('keys-open')) return;
    if (open) {
      entryListSearch.value = '';
      syncEntryListClear();
      entryListChoice = entryIndex();
      renderEntryList();
      window.clearTimeout(entryCloseTimer);
      body.classList.remove('entry-list-closing');
      body.classList.add('entry-list-open');
      entryList.hidden = false;
      entryList.inert = false;
      entryDismiss.hidden = true;
      window.requestAnimationFrame(function () {
        if (body.classList.contains('entry-list-open')) entryDismiss.hidden = false;
      });
      entryListSearch.focus();
    } else if (body.classList.contains('entry-list-open')) {
      entryListSearch.blur();
      cueService.blur();
      window.clearTimeout(entryCloseTimer);
      body.classList.remove('entry-list-open');
      body.classList.add('entry-list-closing');
      entryList.inert = true;
      entryCloseTimer = window.setTimeout(function () {
        body.classList.remove('entry-list-closing');
        entryList.hidden = true;
        entryDismiss.hidden = true;
        revealControls();
      }, layerCloseMs);
    }
    cueService.setAttribute('aria-expanded', String(open));
    revealControls();
    if (open) scrollEntryListChoice();
  }
  var cursorTimer, controlsTimer;
  function revealCursor() {
    body.classList.remove('cursor-hidden');
    window.clearTimeout(cursorTimer);
    cursorTimer = window.setTimeout(function () { body.classList.add('cursor-hidden'); }, 2000);
  }
  function revealControls() {
    window.clearTimeout(controlsTimer);
    if (body.classList.contains('corner-hidden')) return;
    body.classList.remove('controls-idle');
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open') ||
        body.classList.contains('keys-closing') || body.classList.contains('entry-list-closing') ||
        body.classList.contains('find-open') || body.classList.contains('find-closing')) return;
    controlsTimer = window.setTimeout(function () { body.classList.add('controls-idle'); }, 30000);
  }
  ['pointermove', 'pointerdown', 'click'].forEach(function (name) {
    document.addEventListener(name, revealCursor, {passive: true});
  });
  ['pointermove', 'pointerdown', 'click', 'keydown'].forEach(function (name) {
    document.addEventListener(name, revealControls, {passive: true});
  });
  revealCursor(); revealControls();

  keysButton.addEventListener('click', function (event) {
    event.stopPropagation(); setKeysOpen(!body.classList.contains('keys-open'));
  });
  cueService.addEventListener('click', function (event) {
    event.stopPropagation(); if (audioPlaying()) return;
    setEntryListOpen(!body.classList.contains('entry-list-open'));
  });
  entryDismiss.addEventListener('click', function (event) {
    event.stopPropagation(); setEntryListOpen(false);
  });
  function chooseEntryList(index) {
    if (audioPlaying()) return;
    if (!entries[index]) return;
    leaveDetour(); moveTo(entries[index].start);
    setEntryListOpen(false);
  }
  entryListSearch.addEventListener('input', function () {
    entryListChoice = undefined;
    renderEntryList();
    scrollEntryListChoice();
  });
  entryListSearch.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' || (event.key === 'Backspace' && !entryListSearch.value)) {
      event.preventDefault(); event.stopPropagation(); setEntryListOpen(false);
    } else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault(); event.stopPropagation();
      if (!entryListMatches.length) return;
      var position = entryListMatches.indexOf(entryListChoice);
      entryListChoice = entryListMatches[(position + (event.key === 'ArrowDown' ? 1 : -1) + entryListMatches.length) % entryListMatches.length];
      renderEntryList();
      scrollEntryListChoice();
    } else if (event.key === 'Enter') {
      event.preventDefault(); event.stopPropagation(); chooseEntryList(entryListChoice);
    }
  });
  entryList.addEventListener('click', function (event) {
    var row = event.target.closest('.entry-list__item');
    if (!row) return;
    event.stopPropagation(); chooseEntryList(Number(row.dataset.entryIndex));
  });
  cueNext.addEventListener('click', function (event) {
    event.stopPropagation();
    if (audioPlaying()) return;
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open')) return;
    if (detour) leaveDetour(); else moveEntry(1);
  });
  baitList.addEventListener('click', function (event) {
    var bait = event.target.closest('.cue-bait');
    if (!bait) return;
    event.stopPropagation();
    if (audioPlaying()) return;
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open')) return;
    if (detour && detour.kind === 'song') {
      detour.index = detour.baits[Number(bait.dataset.baitIndex)].start; renderDetour();
    } else moveToBait(Number(bait.dataset.baitIndex));
  });
  cuePrefix.addEventListener('click', function (event) {
    if (!event.target.closest('.cue-translation')) return;
    event.stopPropagation(); if (!body.classList.contains('keys-open') && !body.classList.contains('entry-list-open')) flipTranslation();
  });
  /* ---------- panning a fitted media screen (spec 158) -----------------------
     The pointer rides the corner's own zones, which already cover the stage: a press
     that moves more than 4 px pans and eats the click, a press that does not is still
     their click. Capture waits for the threshold — taken on press, it would retarget
     the click to the zones and navigation would stop. */
  var mouseZones = document.querySelector('.mouse-zones');
  var panDrag = null;
  var suppressClick = false;

  function mediaOverflows() { return Boolean(fitOverflow.x || fitOverflow.y); }
  function panElement() {
    if (imageHost) return imageHost.querySelector('.screen__image');
    if (pdfHost) return pdfHost.querySelector('.screen__pdf-page');
    return null;
  }
  function layersOpen() {
    return body.classList.contains('keys-open') || body.classList.contains('entry-list-open')
      || body.classList.contains('find-open') || !findPanel.hidden;
  }

  if (mouseZones) {
    mouseZones.addEventListener('pointerdown', function (event) {
      if (event.button !== 0 || !showing || !mediaOverflows() || layersOpen()) return;
      panDrag = {id: event.pointerId, x: event.clientX, y: event.clientY,
                 start: {x: fitPan.x, y: fitPan.y}, moved: false};
    });

    mouseZones.addEventListener('pointermove', function (event) {
      if (!panDrag || event.pointerId !== panDrag.id) return;
      var dx = event.clientX - panDrag.x;
      var dy = event.clientY - panDrag.y;
      if (!panDrag.moved) {
        if (Math.abs(dx) + Math.abs(dy) < 4) return;
        panDrag.moved = true;
        try { mouseZones.setPointerCapture(event.pointerId); } catch (error) { /* no capture */ }
      }
      var element = panElement();
      if (!element) return;
      fitPan.x = panDrag.start.x + dx;
      fitPan.y = panDrag.start.y + dy;
      applyPan(element);
      event.preventDefault();
    });

    function endPan(event) {
      if (!panDrag || event.pointerId !== panDrag.id) return;
      if (panDrag.moved) suppressClick = true;
      try { mouseZones.releasePointerCapture(panDrag.id); } catch (error) { /* not captured */ }
      panDrag = null;
    }
    mouseZones.addEventListener('pointerup', endPan);
    mouseZones.addEventListener('pointercancel', endPan);

    /* The wheel pans and never navigates: with nothing overflowing it is left alone. */
    mouseZones.addEventListener('wheel', function (event) {
      if (!showing || !mediaOverflows() || layersOpen()) return;
      var element = panElement();
      if (!element) return;
      event.preventDefault();
      fitPan.x -= event.deltaX + (event.shiftKey ? event.deltaY : 0);
      fitPan.y -= event.shiftKey ? 0 : event.deltaY;
      applyPan(element);
    }, {passive: false});
  }

  document.addEventListener('click', function (event) {
    if (suppressClick) { suppressClick = false; return; }
    if (body.classList.contains('keys-closing') || body.classList.contains('entry-list-closing') ||
        body.classList.contains('find-closing')) return;
    if (body.classList.contains('keys-open')) {
      if (!event.target.closest('.sheet') && !event.target.closest('.keys')) setKeysOpen(false);
      return;
    }
    if (body.classList.contains('entry-list-open')) {
      if (!event.target.closest('.entry-list')) setEntryListOpen(false);
      return;
    }
    if (!findPanel.hidden) return;
    var zone = event.target.closest('.mouse-zone');
    if (!zone) return;
    /* Spec 155: the playing recording owns the screen until it pauses. */
    if (audioPlaying()) return;
    if (!document.fullscreenElement && !fullscreenDenied && document.fullscreenEnabled &&
        document.documentElement.requestFullscreen) {
      enterFullscreen();
      return; // This click belongs only to entering fullscreen.
    }
    if (zone.dataset.mouseAction === 'previous') move(-1);
    else if (zone.dataset.mouseAction === 'next') move(1);
    else toggleWords();
  });

  // In windowed mode, any click on the projected page is reserved for the
  // fullscreen gesture. Capture it before the mouse zones can navigate — except
  // on the audio screen's play control, which is a control and not a gesture
  // (spec 156): its first click starts the audio, not the fullscreen.
  document.addEventListener('click', function (event) {
    if (document.fullscreenElement || fullscreenDenied || !document.fullscreenEnabled ||
        !document.documentElement.requestFullscreen) return;
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open') ||
        body.classList.contains('keys-closing') || body.classList.contains('entry-list-closing') ||
        !findPanel.hidden) return;
    if (!event.target.closest('#projectorScreen, .mouse-zones')) return;
    if (event.target.closest('[data-audio-play]')) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    enterFullscreen();
  }, true);

  /* ---------- find and temporary library detours ---------------------------- */
  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  }
  function findUrl(path, params) {
    return window.location.pathname + path + '?' + new URLSearchParams(params).toString();
  }
  /* ---------- the Go To's loading state (spec 136) ------------------------- */
  var gotoBusy = false;
  var cueLoading = null;
  function beginGotoLoad(row) {
    gotoBusy = true;
    findInput.disabled = true;
    if (row && !row.classList.contains('is-loading')) {
      row.classList.add('is-loading');
      var spinner = document.createElement('span');
      spinner.className = 'projector-find__spinner';
      spinner.setAttribute('aria-hidden', 'true');
      row.appendChild(spinner);
    }
    if (!cueLoading) {
      cueLoading = document.createElement('span');
      cueLoading.className = 'cue-loading';
      cueLoading.setAttribute('role', 'status');
      cueLoading.setAttribute('aria-label', 'Loading');
      keysButton.parentNode.insertBefore(cueLoading, keysButton);
    }
  }
  function endGotoLoad() {
    gotoBusy = false;
    findInput.disabled = false;
    if (findResults && findResults.classList.contains('is-loading')) {
      findResults.classList.remove('is-loading');
      var spinner = findResults.querySelector('.projector-find__spinner');
      if (spinner) spinner.remove();
    }
    if (cueLoading) { cueLoading.remove(); cueLoading = null; }
  }
  /* One guard for every input path: while the Go To is fetching, no key and no click
     reaches the page — the shortcuts, the mouse zones, the cue and the panel itself. */
  ['keydown', 'click', 'pointerdown', 'contextmenu'].forEach(function (name) {
    document.addEventListener(name, function (event) {
      if (!gotoBusy) return;
      event.preventDefault();
      event.stopImmediatePropagation();
    }, true);
  });
  function waitForIndex() {
    beginGotoLoad(findResults);
    findSuggestion.textContent = 'Loading search…';
    findCount.textContent = '0 / 0';
    window.GKPSProjectorLibrary.load().then(function () {
      endGotoLoad();
      refreshFind();
      findInput.focus();
    }).catch(function () {
      endGotoLoad();
      findSuggestion.textContent = 'Search unavailable';
      findCount.textContent = '0 / 0';
    });
  }

  function openFind(kind) {
    if (kind === 'j') { setEntryListOpen(true); return; }
    window.clearTimeout(findCloseTimer);
    body.classList.remove('find-closing');
    findKind = kind; findChoice = 0;
    findInput.value = '';
    syncFindClear();
    findPanel.hidden = false;
    findPanel.inert = false;
    findDismiss.hidden = false;
    body.classList.add('find-open');
    revealControls();
    if (window.GKPSProjectorLibrary && !window.GKPSProjectorLibrary.ready()) {
      waitForIndex();
    } else {
      refreshFind();
      findInput.focus();
    }
  }
  function closeFind() {
    if (gotoBusy) return;
    if (!body.classList.contains('find-open')) return;
    ++lookupSequence;
    findInput.blur();
    findDismiss.blur();
    body.classList.remove('find-open');
    body.classList.add('find-closing');
    findPanel.inert = true;
    findKind = ''; findRows = [];
    window.clearTimeout(findCloseTimer);
    findCloseTimer = window.setTimeout(function () {
      body.classList.remove('find-closing');
      findPanel.hidden = true;
      findDismiss.hidden = true;
      revealControls();
    }, layerCloseMs);
    revealControls();
  }
  findDismiss.addEventListener('click', function (event) {
    event.stopPropagation(); closeFind();
  });
  var lookupSequence = 0;
  var paintedFindQuery = '';
  function refreshFind() {
    ++lookupSequence;
    var query = normalize(findInput.value.trim());
    var rows = query && window.GKPSProjectorLibrary
      ? window.GKPSProjectorLibrary.lookup(findInput.value.trim()) : [];
    if (query === paintedFindQuery && JSON.stringify(rows) === JSON.stringify(findRows)) return;
    paintedFindQuery = query;
    findRows = rows; findChoice = 0; paintFind();
  }
  function paintFind() {
    findResults.disabled = !findRows.length;
    findSuggestion.textContent = '';
    if (findRows.length) {
      var row = findRows[findChoice];
      findSuggestion.appendChild(document.createTextNode(row.label));
      if (row.editionSuffix) {
        var suffix = document.createElement('span');
        suffix.className = 'projector-find__edition';
        suffix.textContent = ' · ' + row.editionSuffix;
        findSuggestion.appendChild(suffix);
      }
    } else {
      findSuggestion.textContent = findInput.value.trim()
        ? 'No matching passage or song' : 'Start typing to find a match';
    }
    findCount.textContent = findRows.length ? (findChoice + 1) + ' / ' + findRows.length : '0 / 0';
  }
  function chooseFind(index) {
    var row = findRows[index];
    if (!row) return;
    openDetour(row);
    closeFind();
  }
  findInput.addEventListener('input', refreshFind);
  document.addEventListener('projector-library:ready', function () {
    if (body.classList.contains('find-open') && findInput.value.trim()) refreshFind();
  });
  findInput.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); closeFind(); }
    else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault(); event.stopPropagation();
      if (findRows.length) findChoice = (findChoice + (event.key === 'ArrowDown' ? 1 : -1) + findRows.length) % findRows.length;
      paintFind();
    } else if (event.key === 'Enter') {
      event.preventDefault(); event.stopPropagation(); chooseFind(findChoice);
    } else if (event.key === 'Backspace' && !findInput.value) {
      event.preventDefault(); event.stopPropagation(); closeFind();
    }
  });
  findResults.addEventListener('click', function () { chooseFind(findChoice); });

  /* ---------- the go to, read from the state (spec 185) ---------------------
     The projector keeps no detour of its own: `detour` is the payload for the state's
     current go to, fetched when the state names one it does not hold, and every act
     below writes the state first. */

  var detourNode = document.createElement('section');
  detourNode.className = 'screen projector-detour';
  detourNode.innerHTML = '<h1 class="screen__head"></h1><div class="screen__lines"></div>';
  stage.appendChild(detourNode);

  var gotoCache = {key: '', payload: null, loading: false};

  function gotoKey(goto) {
    if (!goto) return '';
    return goto.kind === 'song' ? 'song:' + goto.song_id
      : 'passage:' + goto.book_id + ':' + goto.chapter;
  }

  function gotoStateOf() {
    var stored = read() || {};
    var goto = stored.goto;
    if (!goto || typeof goto !== 'object') return null;
    return goto;
  }

  function writeGoto(goto) {
    write({service: service, screen: current, on: true,
           translation: translation || null, at: Date.now(), goto: goto});
    post({type: 'goto', goto: goto});
  }

  function fetchGotoPayload(goto, done, fail) {
    var key = gotoKey(goto);
    if (gotoCache.key === key && gotoCache.payload) { done(gotoCache.payload); return; }
    gotoCache.key = key;
    gotoCache.payload = null;
    gotoCache.loading = true;
    var url = goto.kind === 'song' ? '/projector/goto/song/' + goto.song_id + '/'
      : '/projector/goto/chapter/' + goto.book_id + '/' + goto.chapter + '/';
    fetch(url, {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function (payload) {
        gotoCache.loading = false;
        gotoCache.payload = payload;
        done(payload);
      })
      .catch(function (error) {
        gotoCache.loading = false;
        gotoCache.key = '';
        if (window.console && console.error) console.error('Go To load failed:', error);
        if (fail) fail(error);
      });
  }

  /* The payload the detour paints, in the shape `renderDetour` already uses. */
  function detourFrom(goto, payload) {
    if (goto.kind === 'song') {
      return {kind: 'song', label: payload.label, screens: payload.screens || [],
              baits: payload.baits || [], index: Math.max(0, Number(goto.index) || 0)};
    }
    var data = window.GKPSProjectorLibrary.fromChapter(
      payload, goto.verse, goto.translation || '');
    if (!data) return null;
    data.translation = goto.translation || data.translation;
    return data;
  }

  function applyGoto() {
    var stored = read() || {};
    var goto = gotoStateOf();
    /* `on` is one flag for whatever is on air, so the page takes it from the state on
       every go to change — a stale local flag left the service blank after Back. */
    showing = stored.on === true;
    if (!goto) {
      var hadDetour = Boolean(detour);
      detour = null;
      detourNode.classList.remove('is-active');
      /* A stored state that names no service is idle: painting this page's own service
         would put a screen on air that nothing named (FR-011). A page with no stored
         state at all stands alone and keeps what it painted. */
      if (stored && stored.service == null) { paintIdle(); return; }
      if (hadDetour) render();
      return;
    }
    fetchGotoPayload(goto, function (payload) {
      var made = detourFrom(goto, payload);
      if (!made) return;
      detour = made;
      renderDetour();
    });
  }

  /* The projector's `G` puts the pick on air by writing the state, not by keeping it:
     the dock and the overlay learn about it the way they learn about a screen. */
  function openDetour(row) {
    if (gotoBusy || !window.GKPSProjectorLibrary) return;
    beginGotoLoad(findResults);
    window.GKPSProjectorLibrary.detour(row).then(function (data) {
      if (!data) throw new Error('Nothing to paint');
      if (data.kind === 'song') {
        writeGoto({kind: 'song', song_id: row.target.song_id, index: 0});
      } else {
        writeGoto({kind: 'passage', book_id: data.book_id, chapter: data.chapter,
                   verse: data.verse, translation: data.translation});
      }
      endGotoLoad();
      closeFind();
      applyGoto();
    }).catch(function (error) {
      if (window.console && console.error) console.error('Go To load failed:', error);
      endGotoLoad();
      findSuggestion.textContent = 'Could not load — try again';
      if (findRows.length) findCount.textContent = (findChoice + 1) + ' / ' + findRows.length;
    });
  }

  function leaveDetour() {
    if (!detour) return;
    writeGoto(null);
    detour = null;
    detourNode.classList.remove('is-active');
    showing = true;
    render();
  }

  function requestPassage(action, level) {
    if (!detour || detour.kind !== 'passage' || gotoBusy) return;
    if (!window.GKPSProjectorLibrary) return;
    var step = window.GKPSProjectorLibrary.movePassage(detour, action, level);
    if (!step) return;
    if (step.detour) {
      writeGoto({kind: 'passage', book_id: step.detour.book_id, chapter: step.detour.chapter,
                 verse: step.detour.verse, translation: step.detour.translation});
      applyGoto();
      return;
    }
    beginGotoLoad(null);
    window.GKPSProjectorLibrary.fetchChapter(step.request.book_id, step.request.chapter,
      step.request.verse, step.request.edition).then(function (data) {
      if (!data) return;
      writeGoto({kind: 'passage', book_id: data.book_id, chapter: data.chapter,
                 verse: data.verse, translation: data.translation});
      applyGoto();
    }).catch(function () { /* keep the screen that is showing */ })
      .then(endGotoLoad);
  }

  function stepGoto(step, level) {
    var goto = gotoStateOf();
    if (!goto || !detour) return;
    if (goto.kind === 'passage') { requestPassage(step > 0 ? 'next' : 'previous', level); return; }
    if (level === 'ctrl') return;
    var index = detour.index;
    if (level === 'bait') {
      var currentBait = detour.baits.findIndex(function (bait) {
        return index >= bait.start && index <= bait.end;
      });
      var target = detour.baits[currentBait + step];
      if (target) index = target.start;
    } else {
      index = Math.max(0, Math.min(index + step, detour.screens.length - 1));
    }
    writeGoto({kind: 'song', song_id: goto.song_id, index: index});
    applyGoto();
  }

  function gotoBoundary(last, level) {
    var goto = gotoStateOf();
    if (!goto || !detour) return;
    if (goto.kind === 'passage') { requestPassage(last ? 'last' : 'first', level); return; }
    if (level === 'ctrl') return;
    var index = detour.index;
    if (level === 'shift') {
      index = detour.baits[last ? detour.baits.length - 1 : 0].start;
    } else {
      var bait = detour.baits.find(function (item) {
        return index >= item.start && index <= item.end;
      });
      if (bait) index = last ? Math.max(bait.start, bait.end - 1) : bait.start;
    }
    writeGoto({kind: 'song', song_id: goto.song_id, index: index});
    applyGoto();
  }

  function renderDetour() {
    if (!detour) return;
    /* A go to arriving over the channel takes the screen from a playing recording, the
       way another screen does (FR-012): the media hosts are released before it paints. */
    renderImageScreen(null);
    renderAudioScreen(null);
    renderVideoScreen(null);
    renderPDFScreen(null);
    screens().forEach(function (screen) { screen.classList.remove('is-active'); });
    var data = detour.kind === 'passage' ? detour.translations[detour.translation]
      : detour.screens[detour.index];
    if (!data) return;
    var head = detourNode.querySelector('.screen__head');
    var lines = detourNode.querySelector('.screen__lines');
    head.hidden = !data.header;
    head.textContent = data.header || '';
    lines.replaceChildren();
    (data.lines || [{text: data.line || ''}]).forEach(function (line) {
      var p = document.createElement('p'); p.className = 'screen__line'; p.textContent = line.text;
      lines.appendChild(p);
    });
    detourNode.classList.add('is-active');
    body.dataset.showing = showing ? 'true' : 'false';
    /* The notice goes first: hiding it returns its band to the stage, and the fitting below
       measures that stage. */
    syncEmptyNotice();
    fit(detourNode); renderCue();
  }
  function renderDetourCue() {
    /* The service's own place is frozen while a go to is up (D001), so the cue's return
       names the entry the projector already stands on. */
    var returnEntry = entryAt(current);
    cuePrefix.replaceChildren();
    var label = document.createElement('span');
    label.textContent = detour.label + (detour.kind === 'passage' ? ' · ' : ' ·');
    cuePrefix.appendChild(label);
    if (detour.kind === 'passage') {
      var flip = document.createElement('button'); flip.type = 'button';
      flip.className = 'cue-translation'; flip.textContent = detour.translation;
      flip.setAttribute('aria-label', 'Flip passage translation'); cuePrefix.appendChild(flip);
    }
    baitList.replaceChildren();
    baitList.hidden = detour.kind !== 'song';
    if (detour.kind === 'song') detour.baits.forEach(function (bait, index) {
      var button = document.createElement('button'); button.type = 'button';
      button.className = 'cue-bait'; button.dataset.baitIndex = String(index);
      button.textContent = String(bait.number);
      button.setAttribute('aria-pressed', String(detour.index >= bait.start && detour.index <= bait.end));
      baitList.appendChild(button);
    });
    var screen = detour.kind === 'song' ? detour.screens[detour.index] : null;
    cueProgress.textContent = screen && !screen.blank ? screen.split + '/' + screen.split_total : '';
    cueNext.hidden = false;
    cueNext.classList.remove('on'); cueArrow.classList.remove('on');
    cueNextName.textContent = 'back to ' + (returnEntry ? returnEntry.label : 'service');
    cueNext.setAttribute('aria-label', 'Back to service');
  }

  function closeLayers() {
    if (body.classList.contains('keys-closing') || body.classList.contains('entry-list-closing') ||
        body.classList.contains('find-closing')) return true;
    // Escape changes the browser's focus modality even after a pointer-opened
    // layer. Release its trigger so it does not light up on the mirrored display.
    if (body.classList.contains('keys-open')) {
      setKeysOpen(false); keysButton.blur(); return true;
    }
    if (body.classList.contains('entry-list-open')) {
      setEntryListOpen(false); cueService.blur(); return true;
    }
    if (!findPanel.hidden) { closeFind(); return true; }
    return false;
  }
  document.addEventListener('keydown', function (event) {
    if (event.target === entryListSearch) return;
    if (event.key === 'Escape') {
      if (closeLayers()) { event.preventDefault(); return; }
      if (detour) { event.preventDefault(); leaveDetour(); return; }
      return;
    }
    if (body.classList.contains('find-closing') && event.key.toLowerCase() === 'g' &&
        !event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey) {
      event.preventDefault(); openFind('g'); return;
    }
    if (!findPanel.hidden) return;
    var videoFullscreenPlaying = videoHost && document.fullscreenElement === videoHost
      && videoPlayer && !videoPlayer.video.paused;
    if (videoFullscreenPlaying && ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
      'PageUp', 'PageDown', 'Home', 'End'].includes(event.key)) {
      event.preventDefault();
      event.stopImmediatePropagation();
      return;
    }
    /* Spec 155: while a recording plays, no key moves the projector off its screen —
       not the page steps, not the entry or bait jumps, not the Go To. Space pauses,
       which is what gives the screen back. */
    if (audioPlaying()) {
      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
           'PageUp', 'PageDown', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        event.stopImmediatePropagation();
        return;
      }
      if (!event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey &&
          ['g', 'j'].includes(event.key.toLowerCase())) {
        event.preventDefault();
        return;
      }
    }
    if (!event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.repeat) {
      if (event.key.toLowerCase() === 'k') {
        event.preventDefault(); setKeysOpen(!body.classList.contains('keys-open')); return;
      }
      if (event.key.toLowerCase() === 'f') {
        event.preventDefault();
        if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
        else enterFullscreen();
        return;
      }
    }
    if (body.classList.contains('keys-open') || body.classList.contains('entry-list-open')) return;
    if (event.altKey) return;
    /* `⌘` and `Ctrl` are one modifier for the navigation chords (FR-010); any other
       ⌘ chord falls through to the browser, which owns it. */
    var ctrl = event.ctrlKey || event.metaKey;
    var key = event.key.toLowerCase();
    if (!ctrl && !event.shiftKey && ['j', 'g'].includes(key)) {
      event.preventDefault(); openFind(key); return;
    }
    if (!ctrl && !event.shiftKey && key === 'c') {
      event.preventDefault();
      var hide = !body.classList.contains('corner-hidden');
      body.classList.toggle('corner-hidden', hide);
      cue.hidden = hide; keysButton.hidden = hide;
      if (!hide) revealControls();
      return;
    }
    if (!ctrl && !event.shiftKey && key === 't') {
      event.preventDefault();
      if (imageHost || pdfHost) toggleFit(); else flipTranslation();
      return;
    }
    if (!ctrl && event.key === ' ') {
      event.preventDefault();
      if (audioHost && audioPlayer) { if (!event.repeat) audioPlayer.toggle(); }
      else if (videoHost && videoPlayer) { if (!event.repeat) videoPlayer.toggle(); }
      else if (!event.repeat) toggleWords();
      return;
    }
    var forward = ['ArrowRight', 'ArrowDown', 'PageDown'].includes(event.key);
    var backward = ['ArrowLeft', 'ArrowUp', 'PageUp'].includes(event.key);
    if (forward || backward) {
      if (ctrl && (event.key === 'PageUp' || event.key === 'PageDown')) return;
      event.preventDefault();
      if (ctrl) moveEntry(forward ? 1 : -1);
      else if (event.shiftKey) moveBait(forward ? 1 : -1);
      else move(forward ? 1 : -1);
    } else if (event.key === 'Home' || event.key === 'End') {
      event.preventDefault();
      unitBoundary(event.key === 'End', ctrl ? 'ctrl' : event.shiftKey ? 'shift' : 'plain');
    }
  });

  /* The operator's own gesture asks for the screen, rather than the window grabbing
     it on the way in. Escape from the browser gives it back. */
  function enterFullscreen() {
    if (document.fullscreenElement || !document.documentElement.requestFullscreen) return;
    document.documentElement.requestFullscreen().then(function () {
      if (navigator.keyboard && navigator.keyboard.lock) {
        navigator.keyboard.lock(['Escape']).catch(function () { /* browser retains Escape */ });
      }
    }).catch(function () {
      fullscreenDenied = true;
      syncFullscreenCursor();
    });
  }
  function requestVideoFullscreen(host) {
    if (!host || !host.requestFullscreen) return;
    var token = ++videoFullscreenToken;
    var request;
    try { request = host.requestFullscreen(); }
    catch (error) { return; }
    Promise.resolve(request).then(function () {
      if (token !== videoFullscreenToken || host !== videoHost
          || !videoPlayer || videoPlayer.video.paused) exitVideoFullscreen(host);
    }).catch(function () { /* The video remains playable in the normal projector area. */ });
  }
  function exitVideoFullscreen(host) {
    videoFullscreenToken++;
    var currentFullscreen = document.fullscreenElement;
    if (currentFullscreen && (currentFullscreen === host
        || currentFullscreen.classList.contains('screen__video-box'))) {
      document.exitFullscreen().catch(function () {});
    }
  }
  function syncVideoFullscreen() {
    var isVideoFullscreen = Boolean(videoHost && document.fullscreenElement === videoHost);
    if (videoHost) videoHost.classList.toggle('is-fullscreen', isVideoFullscreen);
    if (videoWasFullscreen && !isVideoFullscreen && videoPlayer && !videoPlayer.video.paused)
      videoPlayer.pause();
    videoWasFullscreen = isVideoFullscreen;
    if (isVideoFullscreen) videoActivity();
  }
  var fullscreenDenied = false;
  function syncFullscreenCursor() {
    body.classList.toggle('is-fullscreen', Boolean(document.fullscreenElement));
    body.classList.toggle('fullscreen-available', Boolean(
      !fullscreenDenied && document.fullscreenEnabled && document.documentElement.requestFullscreen));
  }
  document.addEventListener('fullscreenchange', syncFullscreenCursor);
  document.addEventListener('fullscreenchange', syncVideoFullscreen);
  document.addEventListener('fullscreenchange', syncAudioFullscreen);
  syncFullscreenCursor();
  var escapeHoldTimer;
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape' || event.repeat || !document.fullscreenElement) return;
    window.clearTimeout(escapeHoldTimer);
    escapeHoldTimer = window.setTimeout(function () {
      if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
    }, 900);
  });
  document.addEventListener('keyup', function (event) {
    if (event.key === 'Escape') window.clearTimeout(escapeHoldTimer);
  });

  /* ---------- what the other tabs say --------------------------------------- */

  if (channel) {
    channel.addEventListener('message', function (event) {
      var message = event.data || {};
      if (message.type === 'show') {
        var target = Number(message.service);
        if (target && target !== service) {
          /* Spec 119: the projector adopts the service the dock names — the same
             page, a new service, no navigation and no step-aside. */
          adoptService(target, Number(message.screen) || 0, function (index) {
            current = index;
            showing = true;
            translation = '';
            render(true);
          });
          return;
        }
        current = Number(message.screen != null ? message.screen : current);
        showing = true;
        render(true);
      } else if (message.type === 'hide') {
        showing = false;
        render(true);
      } else if (message.type === 'release') {
        showing = false;
        render(true);
      } else if (message.type === 'flip') {
        translation = message.translation || '';
        render(true);
      } else if (message.type === 'goto') {
        applyGoto();
      } else if (message.type === 'update') {
        reflow();
      }
    });
  }

  /* Update: re-read the page (a song's lyrics may have changed) and keep the place. */
  function reflow() {
    /* A saved change reads back at once; no-store keeps a cached page from being served
       for the read that follows close behind it. */
    fetch(window.location.href, {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) { return response.ok ? response.text() : ''; })
      .then(function (html) {
        if (!html) return;
        var parsed = new DOMParser().parseFromString(html, 'text/html');
        var fresh = parsed.getElementById('projectorScreens');
        if (!fresh) return;
        stage.innerHTML = fresh.innerHTML;
        stage.appendChild(detourNode);
        var freshEntries = parsed.getElementById('projectorEntryData');
        var freshScreens = parsed.getElementById('projectorScreenData');
        if (freshEntries && freshScreens) {
          entries = JSON.parse(freshEntries.textContent);
          screenData = JSON.parse(freshScreens.textContent);
        }
        render(true);
      })
      .catch(function () { /* keep showing what we have */ });
    if (window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.refresh) {
      window.GKPSProjectorLibrary.refresh().catch(function () { /* the panel keeps its state */ });
    }
  }

  /* Spec 119: adopt another Tata Ibadah in place. The same fetch-and-swap as reflow()
     (the data islands are the single contract), releasing the old service's media
     exactly as a reuse swap does; no navigation, no reload flicker. */
  function adoptService(id, screenIndex, done) {
    var targetId = Number(id);
    if (!targetId) { if (done) done(screenIndex); return; }
    if (targetId === service) { if (done) done(screenIndex); return; }
    fetch('/projector?service=' + encodeURIComponent(targetId),
          {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) { return response.ok ? response.text() : ''; })
      .then(function (html) {
        if (!html) return;
        var parsed = new DOMParser().parseFromString(html, 'text/html');
        var fresh = parsed.getElementById('projectorScreens');
        var freshEntries = parsed.getElementById('projectorEntryData');
        var freshScreens = parsed.getElementById('projectorScreenData');
        if (!fresh || !freshEntries || !freshScreens) return;
        /* Leaving the old service: release its media and drop its PDF document. */
        if (pdfDocument && pdfDocument.destroy) { try { pdfDocument.destroy(); } catch (e) { } }
        pdfDocument = null; pdfHost = null; pdfPage = 1;
        clearImageScreen();
        clearVideoScreen();
        detour = null;
        service = targetId;
        body.dataset.service = String(service);
        stage.innerHTML = fresh.innerHTML;
        stage.appendChild(detourNode);
        entries = JSON.parse(freshEntries.textContent) || [];
        screenData = JSON.parse(freshScreens.textContent) || [];
        current = Math.max(0, Number(screenIndex) || 0);
        previousIndex = current;
        syncEmptyNotice();
        if (done) done(current);
      })
      .catch(function () { /* keep showing what we have */ });
  }

  /* Spec 119: the page renders the browser-local state. `?service=<id>` opens that
     service (an act of projection — the adoption writes the state); without it the
     page follows whatever is stored, adopting another service in place. */
  var stored = read();
  var adoptId = Number(body.dataset.adopt || 0);
  function settle(screenIndex, on) {
    current = Math.max(0, Number(screenIndex) || 0);
    showing = on === true;
    translation = '';
    render(true);
  }
  if (adoptId) {
    if (adoptId === service) {
      write({service: adoptId, screen: 0, on: true, translation: null, at: Date.now()});
      post({type: 'show', service: adoptId, screen: 0});
      settle(0, true);
    } else {
      adoptService(adoptId, 0, function () {
        write({service: adoptId, screen: 0, on: true, translation: null, at: Date.now()});
        post({type: 'show', service: adoptId, screen: 0});
        settle(0, true);
      });
    }
  } else if (stored && stored.service && Number(stored.service) !== service) {
    adoptService(Number(stored.service), stored.screen, function () {
      settle(stored.screen, stored.on);
      if (stored.translation) { translation = stored.translation; render(true); }
    });
  } else if (stored && Number(stored.service) === service) {
    settle(stored.screen, stored.on);
    if (stored.translation) { translation = stored.translation; render(true); }
  } else {
    showing = false;
    render(true);
  }
  if (!screens().length && service) {
    var empty = screen.querySelector('.projector__empty');
    if (empty) empty.textContent = 'Nothing to show yet: this Tata Ibadah has no items.';
  }
  window.addEventListener('resize', function () { render(true); });
  /* The fit is measured in the face that is on screen. The bundled display faces
     arrive a frame or two after first paint, and their metrics differ from the
     fallback's, so a screen fitted against the fallback can overflow the frame once
     the real face lands (measured 10px past its bottom edge). Re-fit when the fonts
     are ready. */
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      var active = screens()[current];
      if (active) fit(active);
    });
  }
  /* The session may have ended while this page stayed open (spec 186): re-read, and paint
     from what the store now says — silently, because a re-read is not an act. */
  function paintIdle() {
    detour = null;
    detourNode.classList.remove('is-active');
    screens().forEach(function (each) {
      each.classList.remove('is-active', 'is-in', 'is-out');
      each.setAttribute('aria-hidden', 'true');
    });
    showing = false;
    body.dataset.showing = 'false';
    body.classList.add('words-hidden');
    syncEmptyNotice();
    renderCue();
  }

  function rereadSession() {
    var stored = read();
    if (stored && stored.goto) { applyGoto(); return; }
    if (!stored || !stored.service || Number(stored.service) !== Number(service)) {
      paintIdle();
      return;
    }
    detour = null;
    detourNode.classList.remove('is-active');
    current = Math.max(0, Number(stored.screen) || 0);
    previousIndex = current;
    showing = stored.on === true;
    translation = stored.translation || '';
    render(true);
  }

  window.addEventListener('focus', rereadSession);
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) rereadSession();
  });
  window.addEventListener('pageshow', function (event) {
    if (event.persisted) rereadSession();
  });

  /* A go to this page did not start: a fresh open, a reload, or another surface's write
     (FR-010, FR-014). */
  window.addEventListener('storage', function (event) {
    if (event.key === KEY) applyGoto();
  });
  applyGoto();
  window.addEventListener('pagehide', clearImageScreen);
  window.addEventListener('pagehide', clearVideoScreen);
})();
