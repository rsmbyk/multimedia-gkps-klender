/* Service entry modals (spec 006, slice 2).
 *
 * The same dialog the sidebar editors use: a fragment is fetched, the form posts
 * back with fetch, a 400 answer is the server's re-rendered form with its errors,
 * and a save dispatches `editor:saved`, which the shell turns into an in-place
 * refresh of the whole page -- stage included, since the entries live there.
 *
 * This file owns four things: which fragment to open, the delete confirmation, the
 * scripture dropdowns and their resets, and the song pick with its verse checklist.
 */
(function () {
  'use strict';

  var modal = document.getElementById('editorModal');
  if (!modal || typeof modal.showModal !== 'function') return;
  var content = document.getElementById('editorContent');
  var status = document.getElementById('editorStatus');

  function announce(message) { if (status) status.textContent = message || ''; }

  /* The delete is a POST without a form, so it carries the token the way Django
     asks for it: in the header, read from the cookie. */
  function csrf() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[2]) : '';
  }
  function close() { if (modal.open) modal.close(); }

  function get(url) {
    return fetch(url, { credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch' } })
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.text();
      });
  }

  function load(url) {
    announce('');
    get(url).then(function (html) {
      content.innerHTML = html;
      if (!modal.open) modal.showModal();
      wire(content);
      var first = content.querySelector('input:not([type=hidden]), select, textarea');
      if (first) first.focus();
    }).catch(function () { announce('Could not open the editor.'); });
  }

  function newUrl(kind, tatib, after) {
    var url = (modal.dataset.entryNewUrl || '/editor/entry/new/')
      + '?kind=' + encodeURIComponent(kind) + '&tatib=' + encodeURIComponent(tatib);
    if (after) url += '&after=' + encodeURIComponent(after);
    return url;
  }

  function editUrl(id) {
    return (modal.dataset.entryEditUrl || '/editor/entry/0/edit/').replace('/0/', '/' + id + '/');
  }

  /* ---------- the scripture dropdowns ---------------------------------------
     Three dropdowns that know about each other: the book carries its chapter
     count, and picking a book or a chapter resets what follows it to 1. */

  function options(count) {
    var out = '';
    for (var n = 1; n <= count; n += 1) out += '<option value="' + n + '">' + n + '</option>';
    return out;
  }

  function asSelect(input) {
    if (!input || input.tagName === 'SELECT') return input;
    var select = document.createElement('select');
    select.name = input.name;
    select.id = input.id;
    if (input.value) select.dataset.initial = input.value;
    input.parentNode.replaceChild(select, input);
    return select;
  }

  function setValues(chapter, from, to, count, verseCount) {
    if (chapter) {
      chapter.innerHTML = options(count);
      if (chapter.dataset.keep) chapter.value = chapter.dataset.keep;
    }
    if (from) {
      from.innerHTML = options(verseCount);
      from.value = '1';
    }
    if (to) {
      to.innerHTML = '<option value=""></option>' + options(verseCount);
      to.value = '';
    }
  }

  function wireScripture(scope) {
    var book = scope.querySelector('[name=book_translation]');
    if (!book) return;
    var chapter = asSelect(scope.querySelector('[name=chapter]'));
    var from = asSelect(scope.querySelector('[name=verse_start]'));
    var to = asSelect(scope.querySelector('[name=verse_end]'));
    var selected = book.options[book.selectedIndex];
    var chapters = Number(selected && selected.dataset.chapters) || 1;

    function versesFor() {
      var pk = book.value;
      var n = chapter ? Number(chapter.value) || 1 : 1;
      var url = (modal.dataset.entryChapterUrl || '/editor/entry/chapter/0/0/')
        .replace('/0/', '/' + pk + '/').replace('/0/', '/' + n + '/');
      return fetch(url, { credentials: 'same-origin' })
        .then(function (r) { return r.ok ? r.json() : { count: 1 }; })
        .then(function (data) { return data.count || 1; })
        .catch(function () { return 1; });
    }

    /* First paint: the saved values stay put, everything else starts at 1. */
    var wanted = { chapter: chapter && chapter.dataset.initial, from: from && from.dataset.initial,
                   to: to && to.dataset.initial };
    versesFor().then(function (count) {
      setValues(chapter, from, to, chapters, count);
      if (wanted.chapter) chapter.value = wanted.chapter;
      if (wanted.from) from.value = wanted.from;
      if (wanted.to) to.value = wanted.to;
    });

    book.addEventListener('change', function () {
      chapters = Number(book.options[book.selectedIndex].dataset.chapters) || 1;
      versesFor().then(function (count) { setValues(chapter, from, to, chapters, count); });
    });
    if (chapter) {
      chapter.addEventListener('change', function () {
        versesFor().then(function (count) {
          if (from) { from.innerHTML = options(count); from.value = '1'; }
          if (to) { to.innerHTML = '<option value=""></option>' + options(count); to.value = ''; }
        });
      });
    }
  }

  /* ---------- the song pick and its verses ---------------------------------- */

  function verseLabel(box) {
    var boxes = box.querySelectorAll('input[type=checkbox]');
    var checked = [];
    boxes.forEach(function (input) { if (input.checked) checked.push(Number(input.value)); });
    var label = box.parentNode.querySelector('[data-verses-summary]');
    if (!label) {
      label = document.createElement('p');
      label.className = 'editor__hint';
      label.setAttribute('data-verses-summary', '');
      box.parentNode.appendChild(label);
    }
    if (!boxes.length) label.textContent = 'Pick a song first.';
    else if (checked.length === boxes.length) label.textContent = 'All verses.';
    else if (!checked.length) label.textContent = 'No verses: keep at least one.';
    else label.textContent = 'Verses ' + checked.sort(function (a, b) { return a - b; }).join(', ') + '.';
  }

  function renderVerses(box, numbers, chosen) {
    var wanted = chosen || numbers;                 /* a new entry starts with all of them */
    box.innerHTML = numbers.map(function (n) {
      var on = wanted.indexOf(n) !== -1 ? ' checked' : '';
      return '<label class="editor__verse"><input type="checkbox" name="verses" value="' + n
        + '"' + on + '> <span>' + n + '</span></label>';
    }).join('');
    box.addEventListener('change', function () { verseLabel(box); });
    verseLabel(box);
  }

  function wireSongPick(scope, search) {
    var box = scope.querySelector('#entry-verses');
    var hidden = scope.querySelector('#id_song');
    var list = scope.querySelector('#entry-song-options');
    if (!box || !hidden || !list) return;

    if (box.querySelector('input[type=checkbox]')) verseLabel(box);   /* editing: already full */

    function choose(songId, songTitle) {
      hidden.value = songId;
      search.value = songTitle;
      list.hidden = true;
      list.innerHTML = '';
      var pattern = modal.dataset.entrySongVersesUrl || '/editor/entry/song/0/verses/';
      fetch(pattern.replace('/0/', '/' + songId + '/'), { credentials: 'same-origin' })
        .then(function (r) { return r.ok ? r.json() : { verses: [] }; })
        .then(function (data) { renderVerses(box, data.verses || []); })
        .catch(function () { announce('Could not load that song\'s verses.'); });
    }

    function find(query) {
      var pattern = modal.dataset.entrySongsUrl || '/editor/entry/songs/';
      return fetch(pattern + '?q=' + encodeURIComponent(query), { credentials: 'same-origin' })
        .then(function (r) { return r.ok ? r.text() : ''; });
    }

    search.addEventListener('input', function () {
      window.clearTimeout(search.dataset.timer);
      var timer = window.setTimeout(function () {
        find(search.value.trim()).then(function (html) {
          list.innerHTML = html;
          list.hidden = false;
        });
      }, 140);
      search.dataset.timer = timer;
    });

    list.addEventListener('click', function (event) {
      var option = event.target.closest('[data-song]');
      if (!option) return;
      event.preventDefault();
      choose(option.dataset.song, option.dataset.songTitle || option.textContent.trim());
    });
  }

  function wire(scope) {
    wireScripture(scope);
    var search = scope.querySelector('#entry-song-search');
    if (search) wireSongPick(scope, search);
  }

  /* ---------- the delete confirmation --------------------------------------- */

  function confirmDelete(id) {
    announce('');
    content.innerHTML =
      '<div class="editor__confirm">'
      + '<p class="editor__confirm-title">Delete this entry?</p>'
      + '<p class="editor__hint">The service order stays as it was otherwise; only this item goes.</p>'
      + '<div class="editor__actions">'
      + '<button type="button" class="entry__ctrl entry__ctrl--danger" data-confirm-delete>Delete</button>'
      + '<button type="button" class="editor__cancel" data-editor-close>Cancel</button>'
      + '</div></div>';
    if (!modal.open) modal.showModal();
    content.querySelector('[data-confirm-delete]').addEventListener('click', function () {
      var pattern = modal.dataset.entryDeleteUrl || '/editor/entry/0/delete/';
      announce('Deleting...');
      fetch(pattern.replace('/0/', '/' + id + '/'), {
        method: 'POST', credentials: 'same-origin',
        headers: { 'X-Requested-With': 'fetch', 'X-CSRFToken': csrf() }
      }).then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        announce('');
        close();
        document.dispatchEvent(new CustomEvent('editor:saved', { detail: { id: id } }));
      }).catch(function () { announce('Could not delete. Try again.'); });
    });
  }

  document.addEventListener('click', function (event) {
    var del = event.target.closest('[data-entry-delete]');
    if (del) { event.preventDefault(); confirmDelete(del.dataset.entryDelete); return; }
    var edit = event.target.closest('[data-entry-edit]');
    if (edit) { event.preventDefault(); load(editUrl(edit.dataset.entryEdit)); return; }
    var opener = event.target.closest('[data-entry-open]');
    if (!opener || opener.disabled) return;
    event.preventDefault();
    var row = opener.closest('[data-entry-after]');
    load(newUrl(opener.dataset.entryOpen, opener.dataset.entryTatib,
                row ? row.dataset.entryAfter : ''));
  });
})();
