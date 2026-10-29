/* Preview behaviour for spec 158 — the intended fit, its two states, and panning the
 * overflow. Written to the numbers the spec states; this is an artifact of the preview,
 * not the shipping script: the product's projector.js gains the same rules.
 *
 * fit        scale = min(stage width / own width, stage height / own height)  ← the default
 * fit width  scale = stage width / own width      (the excess height is clipped)
 * fit height scale = stage height / own height    (the excess width is clipped)
 * pan        dragging, or the wheel, moves the media inside that excess, clamped to it
 */
(function () {
  'use strict';

  var stage = document.getElementById('projectorScreens');
  var screens = Array.prototype.slice.call(document.querySelectorAll('.screen'));
  var hud = document.getElementById('pv-hud');
  var keysButton = document.getElementById('keys-button');
  var body = document.body;

  var today = false;                                        // "Today (1:1)": what ships now
  var fits = screens.map(function () { return null; });     // per screen: null | 'width' | 'height'
  var pans = screens.map(function () { return {x: 0, y: 0}; });
  var limits = screens.map(function () { return {x: 0, y: 0}; });
  var last = null;                                          // what the HUD last painted

  /* the real page, rasterised from the real PDF at 4× — a static page cannot import pdf.js */
  var page = new Image();
  page.src = 'files/page-612x792.png';

  var CUE = [
    {label: 'images.jpeg', progress: '', next: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa581. Sangap di Jahowa'},
    {label: 'random.jpg', progress: '', next: 'Receipt-2773-9204.png'},
    {label: 'Receipt-2773-9204.png', progress: '1/1', next: 'VOTUM, INTROITUS, DOA'}
  ];

  function activeIndex() {
    return Math.max(0, screens.findIndex(function (s) { return s.classList.contains('is-active'); }));
  }

  function mediaOf(screen) {
    var kind = screen.dataset.mediaKind;
    return {
      kind: kind,
      own: {w: Number(screen.dataset.ownWidth), h: Number(screen.dataset.ownHeight)},
      el: screen.querySelector(kind === 'image' ? '.screen__image' : '.screen__pdf-page'),
      boxEl: screen.querySelector('.screen__image-box, .screen__pdf-box')
    };
  }

  function reset(screen) {
    var media = mediaOf(screen);
    screen.classList.remove('is-fitted');
    media.el.style.width = '';
    media.el.style.height = '';
    media.el.style.transform = '';
    media.el.style.cursor = '';
  }

  function drawPage(canvas, size) {
    var ratio = Math.min(window.devicePixelRatio || 1, 2,
      Math.sqrt(6000000 / Math.max(1, size.w * size.h)));
    canvas.width = Math.max(1, Math.floor(size.w * ratio));
    canvas.height = Math.max(1, Math.floor(size.h * ratio));
    canvas.style.width = Math.floor(size.w) + 'px';
    canvas.style.height = Math.floor(size.h) + 'px';
    var context = canvas.getContext('2d');
    if (page.complete && page.naturalWidth) {
      context.drawImage(page, 0, 0, canvas.width, canvas.height);
    } else {
      page.addEventListener('load', function () { drawPage(canvas, size); }, {once: true});
    }
  }

  /* The pan is clamped to the overflow — half of it each way, because the media is
     centred in its box, so the travel is symmetric. A fresh state starts at 0/0. */
  function applyPan(index) {
    var media = mediaOf(screens[index]);
    var pan = pans[index];
    var limit = limits[index];
    pan.x = Math.min(limit.x, Math.max(-limit.x, pan.x));
    pan.y = Math.min(limit.y, Math.max(-limit.y, pan.y));
    media.el.style.transform = pan.x || pan.y
      ? 'translate(' + Math.round(pan.x) + 'px,' + Math.round(pan.y) + 'px)' : '';
    media.el.style.cursor = limit.x || limit.y
      ? (drag && drag.index === index ? 'grabbing' : 'grab') : '';
    writeHud();
  }

  function apply(index) {
    var screen = screens[index];
    var media = mediaOf(screen);
    var state = fits[index];

    reset(screen);
    /* measure after the reset, so the box answers for the stage and not for its child */
    var box = media.boxEl.getBoundingClientRect();
    var stageBox = {w: box.width, h: box.height};
    var byWidth = stageBox.w / media.own.w;
    var byHeight = stageBox.h / media.own.h;

    if (today) {
      /* today: an image keeps its own size (the CSS cap can only shrink it), and the
         painter is clamped to 1:1 — the same two rules the product ships now. */
      if (media.kind === 'pdf') {
        var capped = Math.min(1, byWidth, byHeight);
        drawPage(media.el, {w: Math.floor(media.own.w * capped), h: Math.floor(media.own.h * capped)});
      }
      limits[index] = {x: 0, y: 0};
      last = {index: index, media: media, stageBox: stageBox, mode: 'today', scale: 1,
        w: media.own.w, h: media.own.h, byWidth: byWidth, byHeight: byHeight};
      applyPan(index);
      return;
    }

    var scale = state === 'width' ? byWidth : state === 'height' ? byHeight
      : Math.min(byWidth, byHeight);
    var size = {w: Math.floor(media.own.w * scale), h: Math.floor(media.own.h * scale)};

    screen.classList.add('is-fitted');
    media.el.style.width = size.w + 'px';
    media.el.style.height = size.h + 'px';
    if (media.kind === 'pdf') drawPage(media.el, size);

    limits[index] = {x: Math.max(0, (size.w - stageBox.w) / 2),
                     y: Math.max(0, (size.h - stageBox.h) / 2)};
    last = {index: index, media: media, stageBox: stageBox, mode: state || 'fit', scale: scale,
      w: size.w, h: size.h, byWidth: byWidth, byHeight: byHeight};
    applyPan(index);
  }

  function writeHud() {
    if (!last) return;
    var r = last;
    var pan = pans[r.index];
    var limit = limits[r.index];
    var cutX = Math.max(0, Math.round((r.w - r.stageBox.w) / 2));
    var cutY = Math.max(0, Math.round((r.h - r.stageBox.h) / 2));
    var name = r.mode === 'fit' ? 'fit'
      : r.mode === 'width' ? 'fit width' : r.mode === 'height' ? 'fit height' : 'today (1:1)';
    var bound = r.byWidth < r.byHeight ? 'width-bound' : 'height-bound';
    var html = 'stage <b>' + Math.round(r.stageBox.w) + '×' + Math.round(r.stageBox.h) + '</b>'
      + ' · media ' + r.media.own.w + '×' + r.media.own.h
      + ' · ' + (r.mode === 'today' ? 'today ' : name + ' ')
      + '<b>×' + r.scale.toFixed(2) + '</b> → <b>' + r.w + '×' + r.h + '</b>'
      + (r.mode === 'today' ? '' : ' (' + bound + ')');
    if (cutY) html += ' · cut ' + cutY + ' above/below';
    if (cutX) html += ' · cut ' + cutX + ' left/right';
    if (limit.x || limit.y) {
      html += ' · pan ' + (Math.round(pan.x) || 0) + '/' + (Math.round(pan.y) || 0)
        + ' of ±' + Math.round(limit.x) + '/±' + Math.round(limit.y);
    }
    hud.innerHTML = html;
  }

  function render() {
    var index = activeIndex();
    screens.forEach(function (screen, i) { if (i !== index) reset(screen); });
    apply(index);
    var cue = CUE[index];
    document.getElementById('cue-prefix').textContent = cue.label;
    document.getElementById('cue-progress').textContent = cue.progress;
    document.getElementById('cue-next-name').textContent = cue.next;
    document.getElementById('cue-next').setAttribute('aria-label',
      cue.next ? 'Go to next entry: ' + cue.next : 'No next entry');
    document.querySelectorAll('[data-pv-screen]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(Number(button.dataset.pvScreen) === index));
    });
    document.getElementById('pv-fit').setAttribute('aria-pressed', String(!today));
    document.getElementById('pv-today').setAttribute('aria-pressed', String(today));
  }

  function show(index) {
    pans[index] = {x: 0, y: 0};
    screens.forEach(function (screen, i) {
      screen.classList.toggle('is-active', i === index);
      screen.setAttribute('aria-hidden', i === index ? 'false' : 'true');
    });
    render();
  }

  function toggleFit() {
    if (today) return;
    var index = activeIndex();
    /* the default fit is one of the two states: T always offers the other one */
    var media = mediaOf(screens[index]);
    var box = media.boxEl.getBoundingClientRect();
    var defaultState = box.width / media.own.w < box.height / media.own.h ? 'width' : 'height';
    fits[index] = (fits[index] || defaultState) === 'width' ? 'height' : 'width';
    pans[index] = {x: 0, y: 0};
    apply(index);
  }

  function setKeysOpen(open) {
    body.classList.toggle('keys-open', open);
    keysButton.setAttribute('aria-expanded', String(open));
    document.getElementById('pv-keys').setAttribute('aria-pressed', String(open));
  }

  /* ---- panning: drag and the wheel, only where there is overflow ------------------ */
  var drag = null;

  stage.addEventListener('pointerdown', function (event) {
    var index = activeIndex();
    var limit = limits[index];
    if (event.button !== 0 || (!limit.x && !limit.y) || body.classList.contains('keys-open')) return;
    var media = mediaOf(screens[index]);
    drag = {index: index, id: event.pointerId, x: event.clientX, y: event.clientY,
      start: {x: pans[index].x, y: pans[index].y}};
    try { media.el.setPointerCapture(event.pointerId); } catch (error) { /* no capture */ }
    media.el.style.cursor = 'grabbing';
    event.preventDefault();
  });

  stage.addEventListener('pointermove', function (event) {
    if (!drag || event.pointerId !== drag.id) return;
    var pan = pans[drag.index];
    pan.x = drag.start.x + (event.clientX - drag.x);
    pan.y = drag.start.y + (event.clientY - drag.y);
    applyPan(drag.index);
  });

  function endDrag() {
    if (!drag) return;
    var index = drag.index;
    drag = null;
    applyPan(index);
  }
  stage.addEventListener('pointerup', endDrag);
  stage.addEventListener('pointercancel', endDrag);

  stage.addEventListener('wheel', function (event) {
    var index = activeIndex();
    var limit = limits[index];
    if (body.classList.contains('keys-open') || (!limit.x && !limit.y)) return;
    event.preventDefault();
    var pan = pans[index];
    pan.x -= event.deltaX + (event.shiftKey ? event.deltaY : 0);
    pan.y -= event.shiftKey ? 0 : event.deltaY;
    applyPan(index);
  }, {passive: false});

  document.querySelectorAll('[data-pv-screen]').forEach(function (button) {
    button.addEventListener('click', function () { show(Number(button.dataset.pvScreen)); });
  });
  document.getElementById('pv-fit').addEventListener('click', function () { today = false; render(); });
  document.getElementById('pv-today').addEventListener('click', function () { today = true; render(); });
  document.getElementById('pv-t').addEventListener('click', toggleFit);
  document.getElementById('pv-keys').addEventListener('click', function () {
    setKeysOpen(!body.classList.contains('keys-open'));
  });
  keysButton.addEventListener('click', function () { setKeysOpen(!body.classList.contains('keys-open')); });

  document.addEventListener('keydown', function (event) {
    if (event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    var key = event.key.toLowerCase();
    if (key === 'k') { event.preventDefault(); setKeysOpen(!body.classList.contains('keys-open')); return; }
    if (key === 'escape' && body.classList.contains('keys-open')) { setKeysOpen(false); return; }
    if (body.classList.contains('keys-open')) return;
    if (key === 't') { event.preventDefault(); toggleFit(); return; }
    if (event.key === 'ArrowRight') { event.preventDefault(); show((activeIndex() + 1) % screens.length); return; }
    if (event.key === 'ArrowLeft') { event.preventDefault(); show((activeIndex() + screens.length - 1) % screens.length); }
  });

  window.addEventListener('resize', function () { render(); });
  page.addEventListener('load', function () { render(); });
  render();
})();
