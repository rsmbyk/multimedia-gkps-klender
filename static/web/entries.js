/* Service entry modals (spec 006, slice 2).
 *
 * The same dialog the sidebar editors use: a fragment is fetched, the form posts
 * back with fetch (editors.js owns the submit), a 400 answer is the server's
 * re-rendered form with its errors, and a save dispatches `editor:saved`, which
 * the shell turns into an in-place refresh of the whole page -- stage included,
 * since the entries live there.
 *
 * This file owns the entry-specific behaviour: which fragment to open, the delete
 * confirmation, the three dropdowns (book, song, and the verse checklist), the
 * scripture cascade, and the text form's Save guard.
 */
(function () {
  'use strict';

  var modal = document.getElementById('editorModal');
  if (!modal || typeof modal.showModal !== 'function') return;
  var content = document.getElementById('editorContent');
  var status = document.getElementById('editorStatus');

  var trigger = null;
  var focusTools = window.gkpsFocus || {
    restoreQuietly: function (target) {
      if (!target) return;
      target.setAttribute('tabindex', '-1');
      target.classList.add('focus-restore-quiet');
      target.focus({ preventScroll: true });
    }
  };

  function focusTargetFor(opener) {
    if (!opener) return null;
    var entryId = opener.dataset.entryEdit || opener.dataset.entryDelete;
    var oldItemId = opener.dataset.oldItemEdit || opener.dataset.oldItemDelete;
    if (entryId) return document.querySelector('[data-entry-pk="' + entryId + '"]');
    if (oldItemId) return document.querySelector('[data-old-item-pk="' + oldItemId + '"]');
    if (opener.hasAttribute('data-entry-open')) {
      var addRow = opener.closest('[data-entry-after]');
      return (addRow && addRow.previousElementSibling) || document.getElementById('read');
    }
    return null;
  }

  function targetAfterDelete(id, oldItem) {
    var selector = oldItem ? '[data-old-item-pk="' : '[data-entry-pk="';
    var deleted = document.querySelector(selector + id + '"]');
    var items = Array.prototype.slice.call(document.querySelectorAll(
      '#readBody [data-entry-pk], #readBody [data-old-item-pk]'));
    var index = items.indexOf(deleted);
    var target = index < 0 ? null : items[index + 1] || items[index - 1];
    if (!target) return { kind: 'read', id: null };
    if (target.hasAttribute('data-entry-pk')) {
      return { kind: 'entry', id: target.dataset.entryPk };
    }
    return { kind: 'old-item', id: target.dataset.oldItemPk };
  }

  function announce(message) { if (status) status.textContent = message || ''; }

  /* The delete is a POST without a form, so it carries the token the way Django
     asks for it: in the header, read from the cookie. */
  function csrf() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[2]) : '';
  }
  function close() { if (modal.open) modal.close(); }

  modal.addEventListener('close', function () {
    var target = focusTargetFor(trigger);
    if (target && document.contains(target)) focusTools.restoreQuietly(target);
    trigger = null;
  });

  function get(url) {
    return fetch(url, { credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch' } })
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.text();
      });
  }

  function focusFirst(scope) {
    var first = scope.querySelector(
      '.editor__picker-trigger:not([disabled]), input[type="text"]:not([disabled]), ' +
      'textarea:not([disabled]), select:not([disabled])');
    if (first) first.focus();
  }

  function load(url) {
    announce('');
    get(url).then(function (html) {
      content.innerHTML = html;
      if (!modal.open) modal.showModal();
      wire(content);
      focusFirst(content);
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

  function oldItemEditUrl(id) {
    return (modal.dataset.oldItemEditUrl || '/editor/item/0/edit/').replace('/0/', '/' + id + '/');
  }


  /* ---------- the dropdowns -------------------------------------------------
     A picker is a trigger plus a menu. The book pick and the song pick filter
     their own options from inside; the verse pick is a checklist whose trigger
     reads what is still included. */

  function pickerOf(scope, name) {
    return scope.querySelector('.editor__picker[data-entry-picker="' + name + '"]');
  }

  function triggers(scope) {
    return [].slice.call(scope.querySelectorAll('[data-picker-trigger], [data-verses-trigger]'));
  }

  function closeMenus(scope) {
    [].slice.call(scope.querySelectorAll('.editor__picker-menu')).forEach(function (menu) {
      menu.hidden = true;
    });
    triggers(scope).forEach(function (trigger) {
      trigger.setAttribute('aria-expanded', 'false');
    });
  }

  /* Keep a menu against the viewport, not the dialog (spec 040). The dialog's content
     scrolls, so an absolutely-positioned menu is CLIPPED at its box; instead the menu
     is fixed, anchored to its trigger's rectangle, capped to the room the window has
     on the chosen side, flipping up when below is tight. The options scroll inside.
     Re-checked whenever the menu's own content arrives and on scroll/resize. */
  function placeMenu(menu) {
    if (!menu || menu.hidden) return;
    var picker = menu.closest('.editor__picker');
    var trigger = picker && picker.querySelector('[data-picker-trigger], [data-verses-trigger]');
    if (!trigger) return;
    var box = trigger.getBoundingClientRect();
    var gap = 6;
    var edge = 8;
    var cap = 268;
    var below = window.innerHeight - box.bottom - gap - edge;
    var above = box.top - gap - edge;
    var flip = below < Math.min(cap, 150) && above > below;
    menu.style.left = box.left + 'px';
    menu.style.width = box.width + 'px';
    menu.style.maxHeight = Math.max(84, Math.min(cap, flip ? above : below)) + 'px';
    if (flip) {
      menu.setAttribute('data-flip', 'up');
      menu.style.top = 'auto';
      menu.style.bottom = (window.innerHeight - box.top + gap) + 'px';
    } else {
      menu.removeAttribute('data-flip');
      menu.style.top = (box.bottom + gap) + 'px';
      menu.style.bottom = 'auto';
    }
  }

  function placeOpenMenus(scope) {
    [].slice.call(scope.querySelectorAll('.editor__picker-menu')).forEach(function (menu) {
      if (!menu.hidden) placeMenu(menu);
    });
  }

  function wirePickerMenus(scope) {
    [].slice.call(scope.querySelectorAll('.editor__picker')).forEach(function (picker) {
      var trigger = picker.querySelector('[data-picker-trigger], [data-verses-trigger]');
      var menu = picker.querySelector('.editor__picker-menu');
      if (!trigger || !menu) return;
      trigger.addEventListener('click', function (event) {
        event.preventDefault();
        if (trigger.disabled) return;
        var opening = menu.hidden;
        closeMenus(scope);
        if (!opening) return;
        menu.hidden = false;
        trigger.setAttribute('aria-expanded', 'true');
        placeMenu(menu);
        var field = menu.querySelector('input[type="search"]');
        if (field) field.focus();
      });
    });
  }

  /* A click outside every picker closes what is open. */
  document.addEventListener('click', function (event) {
    var target = event.target;
    if (!target || !target.closest || target.closest('.editor__picker')) return;
    closeMenus(content);
  });
  /* Escape closes an open menu, not the whole dialog. */
  content.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    if (!content.querySelector('.editor__picker-menu:not([hidden])')) return;
    event.preventDefault();
    event.stopPropagation();
    closeMenus(content);
  });
  /* the modal scrolls under an open menu: re-fit it rather than let it clip */
  content.addEventListener('scroll', function () { placeOpenMenus(content); }, { passive: true });
  window.addEventListener('resize', function () { placeOpenMenus(content); });
  modal.addEventListener('cancel', function (event) {
    if (!content.querySelector('.editor__picker-menu:not([hidden])')) return;
    event.preventDefault();
    closeMenus(content);
  });

  /* ---------- the scripture cascade -----------------------------------------
     Book -> chapter -> verse. The to-verse list keeps only the numbers that can
     still end a range, and turns the control off (with its hover note) when the
     start verse is the last one in the chapter. */

  function wireScripture(scope) {
    var picker = pickerOf(scope, 'book');
    if (!picker) return;
    var select = scope.querySelector('[name=book_translation]');
    var chapter = scope.querySelector('[name=chapter]');
    var from = scope.querySelector('[name=verse_start]');
    var to = scope.querySelector('[name=verse_end]');
    var wrap = scope.querySelector('[data-end-wrap]');
    var label = picker.querySelector('[data-picker-label]');
    var filter = picker.querySelector('input[type="search"]');
    var groups = [].slice.call(picker.querySelectorAll('[data-picker-group]'));
    var options = [].slice.call(picker.querySelectorAll('[data-book]'));
    var empty = picker.querySelector('[data-picker-empty]');
    if (!select || !chapter || !from || !to) return;

    var verses = [];

    function numbers(count) {
      var out = '';
      for (var n = 1; n <= count; n += 1) out += '<option value="' + n + '">' + n + '</option>';
      return out;
    }
    function keep(node, wanted) {
      if (wanted === undefined || wanted === null || wanted === '') return;
      var hit = [].slice.call(node.options).some(function (option) {
        return option.value === String(wanted);
      });
      if (hit) node.value = String(wanted);
    }
    function chosenBook() { return select.options[select.selectedIndex]; }
    function chapterCount() {
      var book = chosenBook();
      return (book && book.dataset.chapters) ? Number(book.dataset.chapters) : 0;
    }
    function fillChapters(wanted) {
      var count = chapterCount();
      chapter.disabled = !count;
      if (!count) { chapter.innerHTML = ''; return; }
      chapter.innerHTML = numbers(count);
      keep(chapter, wanted);
      if (!chapter.value) chapter.value = '1';
    }
    function syncTo() {
      var start = Number(from.value) || 1;
      var after = verses.filter(function (n) { return n > start; });
      to.innerHTML = '<option value=""></option>' + after.map(function (n) {
        return '<option value="' + n + '">' + n + '</option>';
      }).join('');
      if (after.length) {
        to.disabled = false;
        if (wrap) wrap.removeAttribute('data-empty');
      } else {
        to.disabled = true;
        if (wrap) wrap.setAttribute('data-empty', 'true');
      }
      return after;
    }
    function chapterUrl(pk, number) {
      return (modal.dataset.entryChapterUrl || '/editor/entry/chapter/0/0/')
        .replace('/0/', '/' + pk + '/').replace('/0/', '/' + number + '/');
    }
    function loadVerses(pk, number, wantedFrom, wantedTo) {
      return fetch(chapterUrl(pk, number), { credentials: 'same-origin' })
        .then(function (response) { return response.ok ? response.json() : { verses: [] }; })
        .then(function (data) {
          verses = data.verses || [];
          from.disabled = !verses.length;
          from.innerHTML = verses.map(function (n) {
            return '<option value="' + n + '">' + n + '</option>';
          }).join('');
          if (verses.length) from.value = String(verses[0]);
          keep(from, wantedFrom);
          syncTo();
          keep(to, wantedTo);
          return verses;
        })
        .catch(function () {
          verses = [];
          from.disabled = true;
          from.innerHTML = '';
          syncTo();
        });
    }
    function filterBooks() {
      var query = (filter.value || '').trim().toLowerCase();
      var visible = 0;
      options.forEach(function (option) {
        var names = (option.dataset.bookName || '') + ' ' + (option.dataset.bookOther || '');
        var hit = !query || names.toLowerCase().indexOf(query) !== -1;
        option.hidden = !hit;
        if (hit) visible += 1;
      });
      groups.forEach(function (group) {
        group.hidden = !group.querySelector('[data-book]:not([hidden])');
      });
      if (empty) empty.hidden = visible > 0;
    }
    function pickBook(button) {
      select.value = button.dataset.book;
      options.forEach(function (option) {
        option.setAttribute('aria-selected', option === button ? 'true' : 'false');
      });
      label.textContent = button.dataset.bookName || button.textContent.trim();
      filter.value = '';
      filterBooks();
      fillChapters(1);
      loadVerses(select.value, Number(chapter.value) || 1);
    }

    /* First paint: what the form already held, else a blank cascade to fill in. */
    if (select.value) {
      label.textContent = (chosenBook().textContent || '').trim();
      fillChapters(chapter.dataset.initial);
      loadVerses(select.value, Number(chapter.value) || 1,
                 from.dataset.initial, to.dataset.initial);
    } else {
      chapter.disabled = true;
      from.disabled = true;
      to.disabled = true;
    }

    filter.addEventListener('input', filterBooks);
    options.forEach(function (option) {
      option.addEventListener('click', function () { pickBook(option); closeMenus(scope); });
    });
    chapter.addEventListener('change', function () {
      loadVerses(select.value, Number(chapter.value) || 1);
    });
    from.addEventListener('change', function () { syncTo(); });
  }

  /* ---------- the song pick and its verse checklist ------------------------- */

  function verseSummary(picker, box) {
    if (!picker) return;
    var trigger = picker.querySelector('[data-verses-trigger]');
    var summary = picker.querySelector('[data-verses-summary]');
    var boxes = box ? [].slice.call(box.querySelectorAll('input[type=checkbox]')) : [];
    var checked = boxes.filter(function (input) { return input.checked; })
      .map(function (input) { return Number(input.value); })
      .sort(function (a, b) { return a - b; });
    if (!trigger || !summary) return;
    if (!boxes.length) {
      summary.textContent = 'Pick a song first';
      trigger.disabled = true;
    } else if (checked.length === boxes.length) {
      summary.textContent = 'All verses';
      trigger.disabled = boxes.length === 1;      /* one verse: nothing to choose */
    } else if (!checked.length) {
      summary.textContent = 'No verses: keep at least one';
      trigger.disabled = false;
    } else {
      summary.textContent = 'Verses ' + checked.join(', ');
      trigger.disabled = false;
    }
  }

  function renderVerses(box, numbers, chosen) {
    var wanted = chosen || numbers;               /* a new pick starts with all of them */
    box.innerHTML = numbers.map(function (n) {
      var on = wanted.indexOf(n) !== -1 ? ' checked' : '';
      return '<div><label class="editor__verse"><input type="checkbox" name="verses" value="' + n
        + '"' + on + '> <span>' + n + '</span></label></div>';
    }).join('');
  }

  function wireSongPicker(scope) {
    var picker = pickerOf(scope, 'song');
    if (!picker) return;
    var versesPicker = pickerOf(scope, 'verses');
    var trigger = picker.querySelector('[data-picker-trigger]');
    var hidden = scope.querySelector('#id_song');
    var search = scope.querySelector('#entry-song-search');
    var list = scope.querySelector('#entry-song-options');
    var label = picker.querySelector('[data-picker-label]');
    var box = scope.querySelector('#entry-verses');
    if (!hidden || !search || !list || !box) return;

    function find(query) {
      return fetch((modal.dataset.entrySongsUrl || '/editor/entry/songs/')
                   + '?q=' + encodeURIComponent(query), { credentials: 'same-origin' })
        .then(function (response) { return response.ok ? response.text() : ''; })
        .then(function (html) {
          /* A slow answer must not overwrite a newer one: the preload that runs
             when the menu opens can land after what the person has typed. */
          if (query !== (search.value || '').trim()) return;
          list.innerHTML = html;
          placeMenu(list.closest('.editor__picker-menu'));
        });
    }
    function loadVerses(songId) {
      var pattern = modal.dataset.entrySongVersesUrl || '/editor/entry/song/0/verses/';
      return fetch(pattern.replace('/0/', '/' + songId + '/'), { credentials: 'same-origin' })
        .then(function (response) { return response.ok ? response.json() : { verses: [] }; })
        .then(function (data) {
          renderVerses(box, data.verses || []);
          verseSummary(versesPicker, box);
          placeMenu(box.closest('.editor__picker-menu'));
        })
        .catch(function () { announce('Could not load that song\u2019s verses.'); });
    }

    search.addEventListener('input', function () {
      window.clearTimeout(search.dataset.timer);
      search.dataset.timer = window.setTimeout(function () { find(search.value.trim()); }, 140);
    });
    /* an empty menu is a dead end: offer the first songs when it opens */
    if (trigger) {
      trigger.addEventListener('click', function () {
        if (!list.innerHTML.trim()) find('');
      });
    }
    list.addEventListener('click', function (event) {
      var option = event.target.closest('[data-song]');
      if (!option) return;
      event.preventDefault();
      hidden.value = option.dataset.song;
      label.textContent = option.dataset.songTitle || option.textContent.trim();
      search.value = '';
      list.innerHTML = '';
      closeMenus(scope);
      loadVerses(option.dataset.song);
    });
    box.addEventListener('change', function () { verseSummary(versesPicker, box); });
    verseSummary(versesPicker, box);              /* editing: the boxes are already there */
  }

  /* ---------- the text form's Save guard ------------------------------------ */

  function wireTextSave(scope) {
    var form = scope.querySelector('[data-entry-form="text"]');
    if (!form) return;
    var area = form.querySelector('textarea[name=text]');
    var save = form.querySelector('.editor__save');
    if (!area || !save) return;
    function sync() { save.disabled = area.value.trim() === ''; }
    area.addEventListener('input', sync);
    sync();
  }

  function wire(scope) {
    wirePickerMenus(scope);
    wireScripture(scope);
    wireSongPicker(scope);
    wireTextSave(scope);
  }

  /* editors.js swaps the form back in after a 400; that copy needs wiring too. */
  document.addEventListener('editor:rendered', function () { wire(content); });

  /* ---------- the delete confirmation --------------------------------------- */

  function confirmDelete(id, oldItem) {
    announce('');
    content.innerHTML =
      '<div class="editor__confirm">'
      + '<p class="editor__confirm-title">Delete this ' + (oldItem ? 'row' : 'entry') + '?</p>'
      + '<p class="editor__hint">The service order stays as it was otherwise; only this item goes.</p>'
      + '<div class="editor__actions">'
      + '<button type="button" class="editor__cancel" data-editor-close>Cancel</button>'
      + '<button type="button" class="editor__danger" data-confirm-delete>Delete</button>'
      + '</div></div>';
    if (!modal.open) modal.showModal();
    content.querySelector('[data-confirm-delete]').addEventListener('click', function () {
      var pattern = oldItem
        ? (modal.dataset.oldItemDeleteUrl || '/editor/item/0/delete/')
        : (modal.dataset.entryDeleteUrl || '/editor/entry/0/delete/');
      announce('Deleting...');
      fetch(pattern.replace('/0/', '/' + id + '/'), {
        method: 'POST', credentials: 'same-origin',
        headers: { 'X-Requested-With': 'fetch', 'X-CSRFToken': csrf() }
      }).then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        announce('');
        var focus = targetAfterDelete(id, oldItem);
        close();
        document.dispatchEvent(new CustomEvent('editor:saved', {
          detail: {
            id: id,
            kind: oldItem ? 'old-item' : 'entry',
            focusKind: focus.kind,
            focusId: focus.id
          }
        }));
      }).catch(function () { announce('Could not delete. Try again.'); });
    });
  }

  document.addEventListener('click', function (event) {
    /* Spec 026: projecting no longer refuses an entry write. The operator keeps working
       while a Tata Ibadah is on screen, and the display follows every change. */
    var oldDel = event.target.closest('[data-old-item-delete]');
    if (oldDel) {
      event.preventDefault();
      trigger = oldDel;
      confirmDelete(oldDel.dataset.oldItemDelete, true);
      return;
    }
    var oldEdit = event.target.closest('[data-old-item-edit]');
    if (oldEdit) {
      event.preventDefault();
      trigger = oldEdit;
      load(oldItemEditUrl(oldEdit.dataset.oldItemEdit));
      return;
    }
    var del = event.target.closest('[data-entry-delete]');
    if (del) {
      event.preventDefault();
      trigger = del;
      confirmDelete(del.dataset.entryDelete);
      return;
    }
    var edit = event.target.closest('[data-entry-edit]');
    if (edit) {
      event.preventDefault();
      trigger = edit;
      load(editUrl(edit.dataset.entryEdit));
      return;
    }
    var opener = event.target.closest('[data-entry-open]');
    if (!opener || opener.disabled) return;
    event.preventDefault();
    trigger = opener;
    var row = opener.closest('[data-entry-after]');
    var after = row ? row.dataset.entryAfter
                    : (opener.closest('[data-entry-start]') ? 'start' : '');
    load(newUrl(opener.dataset.entryOpen, opener.dataset.entryTatib, after));
  });

  /* ---------- a hovered item reveals its neighbouring add rows (spec 037) ----
     CSS cannot reach a preceding sibling, so the pair of add rows around the row
     under the pointer (or holding keyboard focus) is revealed here. Hovering an add
     row itself reveals only that row (spec 036): the item is not hovered then. The
     first item's "above" row is the start bar, which is always visible already. */
  function neighboursOf(item) {
    return [item.previousElementSibling, item.nextElementSibling].filter(function (node) {
      return node && node.classList && node.classList.contains('entry__add');
    });
  }

  function revealNeighbours(item, on) {
    neighboursOf(item).forEach(function (row) {
      row.classList.toggle('is-revealed', on);
    });
  }

  function itemOf(node) {
    return node && node.closest ? node.closest('.tatib__item, .tatib__eos') : null;
  }

  document.addEventListener('mouseover', function (event) {
    var item = itemOf(event.target);
    if (item) revealNeighbours(item, true);
  });
  document.addEventListener('mouseout', function (event) {
    var item = itemOf(event.target);
    if (!item || item.contains(event.relatedTarget)) return;
    revealNeighbours(item, false);
  });
  document.addEventListener('focusin', function (event) {
    var item = itemOf(event.target);
    if (item) revealNeighbours(item, true);
  });
  document.addEventListener('focusout', function (event) {
    var item = itemOf(event.target);
    if (!item || item.contains(event.relatedTarget)) return;
    revealNeighbours(item, false);
  });
})();
