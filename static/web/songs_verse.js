/* Verse reorder on the song page (spec 189): ghost + frozen midpoints,
   carried from static/web/reorder.js (Sidebar shape). */
(function () {
  'use strict';

  function body() { return document.getElementById('readBody'); }
  function verses() {
    var b = body();
    return b ? [].slice.call(b.querySelectorAll('.v')) : [];
  }

  var drag = null;
  var pointerY = 0;

  function csrf() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[2]) : '';
  }

  function snapshot() {
    var before = {};
    verses().forEach(function (row) { before[row.dataset.verse] = row.getBoundingClientRect().top; });
    return before;
  }

  function paintNumbers() {
    verses().forEach(function (row, index) {
      var n = row.querySelector('.v__n');
      if (n) n.textContent = String(index + 1);
    });
    if (!drag) return;
    var target = (drag.ghost && drag.ghost.querySelector('.v__n')) || drag.row.querySelector('.v__n');
    var index = verses().indexOf(drag.row);
    if (target && index >= 0) target.textContent = drag.from + '→' + (index + 1);
  }

  function makeGhost() {
    var rect = drag.row.getBoundingClientRect();
    var copy = document.createElement('div');
    copy.className = 'v verse__ghost';
    copy.setAttribute('aria-hidden', 'true');
    copy.inert = true;
    copy.innerHTML = drag.row.innerHTML;
    [].slice.call(copy.querySelectorAll('a, button, [id], [tabindex]'))
      .forEach(function (node) { node.removeAttribute('id'); node.removeAttribute('tabindex'); });
    copy.style.width = rect.width + 'px';
    copy.style.height = rect.height + 'px';
    copy.style.left = (drag.pointerX - drag.offsetX) + 'px';
    copy.style.top = (pointerY - drag.offsetY) + 'px';
    document.body.appendChild(copy);
    drag.ghost = copy;
  }

  function positionGhost() {
    if (!drag || !drag.ghost) return;
    drag.ghost.style.left = (drag.pointerX - drag.offsetX) + 'px';
    drag.ghost.style.top = (pointerY - drag.offsetY) + 'px';
  }

  function clearGhost(current) {
    if (!current) return;
    if (current.ghost) current.ghost.remove();
    current.row.classList.remove('is-dragging');
    document.body.classList.remove('is-arranging');
  }

  function startDrag(event, row) {
    if (event.button !== 0) return;
    if (verses().length < 2) return;  /* one verse has nowhere to go (owner) */
    event.preventDefault();
    body().classList.add('is-dragging');
    if (row.setPointerCapture && event.pointerId != null) {
      try { row.setPointerCapture(event.pointerId); } catch (e) { /* preview */ }
    }
    /* B: collapse for the gesture. */
    setCompact(true);
    var rect = row.getBoundingClientRect();
    var mids = [];
    verses().forEach(function (other) {
      if (other === row) return;
      var r = other.getBoundingClientRect();
      mids.push({el: other, middle: r.top + r.height / 2});
    });
    drag = {
      row: row, mids: mids, startY: event.clientY, y: event.clientY,
      pointerX: event.clientX, moved: false, ghost: null,
      from: verses().indexOf(row) + 1,
      offsetX: event.clientX - rect.left,
      offsetY: Math.min(event.clientY - row.getBoundingClientRect().top, rect.height / 2),
      collapsed: true, pointerId: event.pointerId
    };
    /* recompute clamped offset after collapse (rect is compact now) */
    drag.offsetY = Math.min(event.clientY - rect.top, rect.height / 2);
    document.body.style.userSelect = 'none';
    document.body.classList.add('is-arranging');
    pointerY = event.clientY;
    /* Sidebar's 3px dead zone is in pointermove; the first frame is a no-op until then. */
    paintNumbers();
  }

  function setCompact(on) {
    verses().forEach(function (row) {
      var text = row.querySelector('.v__text');
      if (text) {
        if (on) {
          if (!row.dataset.fullText) row.dataset.fullText = text.innerHTML;
          text.textContent = row.dataset.fullText.split(/<br\s*\/?>/i)[0].replace(/<[^>]+>/g, '');
        } else if (row.dataset.fullText) {
          text.innerHTML = row.dataset.fullText;
          delete row.dataset.fullText;
        }
      }
      row.classList.toggle('is-compact', on);
    });
    var add = document.querySelector('.verse-add');
    if (add) add.hidden = on;
  }

  function placeRowAt(y) {
    var others = verses().filter(function (item) { return item !== drag.row; });
    var target = drag.mids.length;
    for (var i = 0; i < drag.mids.length; i += 1) {
      if (y < drag.mids[i].middle) { target = i; break; }
    }
    target = Math.max(0, Math.min(others.length, target));
    /* The Add row lives after the last verse: an end-of-list drop goes
       just before it, not after it. */
    var endAnchor = document.querySelector('.verse-add') || body().querySelector('.entry__empty');
    var insertBefore = others[target] || endAnchor;
    var already = (insertBefore === drag.row.nextElementSibling) ||
      (insertBefore === null && drag.row.nextElementSibling === null);
    if (already) return;
    var before = snapshot();
    body().insertBefore(drag.row, insertBefore);
    paintNumbers();
    verses().forEach(function (item) {
      if (item === drag.row || item.classList.contains('is-dragging')) return;
      var was = before[item.dataset.verse];
      if (was == null) return;
      var delta = was - item.getBoundingClientRect().top;
      if (!delta) return;
      item.style.transition = 'none';
      item.style.transform = 'translateY(' + delta + 'px)';
      requestAnimationFrame(function () {
        item.style.transition = '';
        item.style.transform = '';
      });
    });
  }

  function queue() { requestAnimationFrame(frame); }
  var frameQueued = false;
  function queueOnce() {
    if (frameQueued) return;
    frameQueued = true;
    requestAnimationFrame(function () { frameQueued = false; frame(); });
  }

  function frame() {
    if (!drag || !drag.moved) return;
    placeRowAt(pointerY);
    positionGhost();
    var edge = 72;
    if (pointerY < edge) window.scrollBy(0, -14);
    else if (pointerY > window.innerHeight - edge) window.scrollBy(0, 14);
  }

  function persist(orderedIds, songPk) {
    return fetch('/editor/verse/reorder/', {
      method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf(), 'X-Requested-With': 'fetch'},
      body: JSON.stringify({song: songPk, ordered_ids: orderedIds})
    }).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); });
  }

  function endDrag(event) {
    if (!drag) return;
    var current = drag;
    var moved = drag.moved;
    if (moved) {
      if (event && typeof event.clientY === 'number') pointerY = event.clientY;
      placeRowAt(pointerY);
    }
    clearGhost(current);
    drag = null;
    document.body.style.userSelect = '';
    if (moved) {
      var orderedIds = verses().map(function (r) { return Number(r.dataset.verse); });
      /* No reload: renumber is already painted; write the order once. */
      var rowEl = current.row;
      var songEl = document.querySelector('[data-add-verse]');
      var songPk = songEl ? Number(songEl.dataset.song) : null;
      if (songPk && orderedIds.length) persist(orderedIds, songPk).catch(function () { location.reload(); });
      setTimeout(function () { setCompact(false); paintNumbers(); }, 170);
    } else {
      setCompact(false);
      paintNumbers();
    }
  }

  document.addEventListener('pointermove', function (event) {
    if (!drag) return;
    pointerY = event.clientY;
    drag.pointerX = event.clientX;
    drag.y = event.clientY;
    if (!drag.moved && Math.abs(event.clientY - drag.startY) > 3) {
      drag.moved = true;
      makeGhost();
      drag.row.classList.add('is-dragging');
      paintNumbers();
    }
    if (!drag.moved) return;
    positionGhost();
    queueOnce();
  }, true);

  document.addEventListener('pointerup', endDrag, true);
  document.addEventListener('pointercancel', function () { if (drag) { endDrag(null); } }, true);

  document.addEventListener('pointerdown', function (event) {
    if (event.button !== 0) return;
    var grip = event.target.closest && event.target.closest('.v__grip');
    if (!grip) return;
    var row = grip.closest('.v');
    if (!row) return;
    /* Grip is hittable at rest (FR-006f) even though painted on hover. */
    startDrag(event, row);
  }, true);

  /* Add/Edit via the shared editor dialog. */
  document.addEventListener('click', function (event) {
    var add = event.target.closest && event.target.closest('[data-add-verse]');
    if (add) {
      var dialog = document.getElementById('editorModal');
      openEditor(dialog, '/editor/verse/new/?song=' + encodeURIComponent(add.dataset.song), 'New verse');
      return;
    }
    var edit = event.target.closest && event.target.closest('[data-verse-edit]');
    if (edit) {
      var row = edit.closest('.v');
      var n = row ? row.dataset.verseNumber : '';
      openEditor(document.getElementById('editorModal'),
                 '/editor/verse/' + edit.dataset.verseEdit + '/', 'Edit verse ' + n);
    }
  });

  function openEditor(dialog, url, title) {
    if (!dialog) return;
    fetch(url, {headers: {'X-Requested-With': 'fetch'}})
      .then(function (r) { return r.text(); })
      .then(function (html) {
        var content = document.getElementById('editorContent');
        content.innerHTML = html;
        if (!dialog.open) dialog.showModal();
        var t = content.querySelector('.editor__title, h2');
        if (t) t.textContent = title;
        var field = content.querySelector('textarea');
        if (field) { field.focus(); field.setSelectionRange(field.value.length, field.value.length); }
        /* Delete: one confirmation naming verse + song, then delete + reload. */
        content.addEventListener('click', function confirmWire(event) {
          var del = event.target.closest && event.target.closest('[data-verse-delete]');
          if (del && !del.disabled) {
            var number = (title.match(/\d+/) || [''])[0];
            content.innerHTML =
              '<div class="editor__confirm"><p class="editor__confirm-title">Delete verse ' + number + '?</p>' +
              '<p class="editor__hint">It is removed from this song, and the verses after it are renumbered. Nothing else changes.</p>' +
              '<div class="editor__actions"><button type="button" class="editor__cancel" data-editor-close>Cancel</button>' +
              '<button type="button" class="editor__danger" data-confirm-delete data-verse-row="' + del.dataset.verseRow + '">Delete</button></div></div>';
            content.querySelector('[data-editor-close]').addEventListener('click', function () { dialog.close(); content.innerHTML = ''; });
            content.querySelector('[data-confirm-delete]').addEventListener('click', function () {
              fetch('/editor/verse/' + del.dataset.verseRow + '/delete/', {method: 'POST', credentials: 'same-origin',
                headers: {'X-CSRFToken': csrf(), 'X-Requested-With': 'fetch'}})
                .then(function (r) { if (!r.ok) throw new Error('delete failed'); location.reload(); })
                .catch(function () { location.reload(); });
            });
          }
        }, {once: true});
        var form = content.querySelector('form');
        if (form) form.addEventListener('submit', function (ev) {
          ev.preventDefault();
          var lyric = field ? field.value : '';
          var isNew = url.indexOf('/new/') !== -1;
          var body = isNew
            ? {song: Number(url.match(/song=(\d+)/)[1]), lyric: lyric}
            : {lyric: lyric};
          var endpoint = isNew ? '/editor/verse/new/save/' : url.split('?')[0] + 'save/';
          fetch(endpoint, {method: 'POST', credentials: 'same-origin',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf(), 'X-Requested-With': 'fetch'},
            body: JSON.stringify(body)})
            .then(function (r) { if (!r.ok) throw new Error('save failed'); location.reload(); })
            .catch(function () { location.reload(); });
        });
      });
  }
})();
