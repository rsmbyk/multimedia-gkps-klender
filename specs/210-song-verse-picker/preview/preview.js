/* Interactive preview. No product code, no framework: the dialog markup and
   classes come from the product; only the Verses control is rebuilt per option. */
(function () {
  'use strict';
  var OPTIONS = ['tiles', 'chips', 'typed', 'checkboxes', 'song', 'soft'];
  var INFO = {
    tiles: {
      title: '1 · Number tiles',
      text: 'Verse numbers are tiles: a click ticks or unticks one verse. Hold the pointer down on a tile and drag across the others to extend a range. The field is hidden until a song is picked, then reveals in one motion, starting with verse 1 ticked.',
      body: '<ol><li><strong>Best for:</strong> touch and the common “press verse 1, drag to verse 4” move — range picking without a modifier key.</li>' +
            '<li><strong>Cost:</strong> a long song with 24 verses wraps to four rows; the grid grows instead of scrolling.</li>' +
            '<li><strong>Keyboard:</strong> arrows move between tiles; Space toggles the focused tile; Shift+Arrow extends from the last ticked tile for those without a pointer.</li>' +
            '<li><strong>All / Clear</strong> disable themselves at the two ends — all ticked, or none ticked.</li></ol>'
    },
    chips: {
      title: '2 · From / To → range chips',
      text: 'Two number boxes add one stretch at a time. Each added stretch becomes a removable chip, so the picked set is readable even when it is not contiguous.',
      body: '<ol><li><strong>Best for:</strong> long songs and non-contiguous sets — no hunting for a number in a grid.</li>' +
            '<li><strong>Cost:</strong> two fields and a button per range; three ranges is nine actions against two taps in the tile version.</li>' +
            '<li><strong>Chips show the plan:</strong> “1–3”, “5”, “8–10” stay visible and each has its own remove button.</li>' +
            '<li><strong>Keyboard / touch:</strong> plain number inputs work with both; no modifier keys involved.</li></ol>'
    },
    typed: {
      title: '3 · Typed range',
      text: 'One field accepts the range notation the team already says out loud: 1-3,5,8-10. A parsed chip preview shows what was understood as you type.',
      body: '<ol><li><strong>Best for:</strong> an operator who knows exactly which verses — fastest by far once the notation is familiar.</li>' +
            '<li><strong>Cost:</strong> syntax is a new thing to learn; a typo can silently drop a verse, so the parsed preview and the error line matter.</li>' +
            '<li><strong>Forgiving input:</strong> en dash or hyphen, spaces, trailing comma; out-of-range and reversed ranges report what was ignored.</li>' +
            '<li><strong>Still a form control:</strong> the hidden checkboxes carry the real values, not the text string.</li></ol>'
    },
    checkboxes: {
      title: '4 · Checkboxes + helpers',
      text: 'The shipped control, kept: one checkbox per verse. This version enlarges the tap target to 36px, adds All / Clear, and lets Shift+click fill a stretch.',
      body: '<ol><li><strong>Best for:</strong>smallest change — every existing test and muscle memory keeps working.</li>' +
            '<li><strong>Cost:</strong> still one small target per verse, and Shift+click does not exist on touch.</li>' +
            '<li><strong>All / Clear</strong> fix the worst case (a 24-verse song where you want none but the default is all).</li>' +
            '<li><strong>Native inputs stay</strong> — the accessible state and form submission are unchanged.</li></ol>'
    },
    song: {
      title: '5 · Song search + verse tiles (combined)',
      text: 'The song field is a live search from the first frame of the modal: type a title, number or book name and results narrow under the field. Selecting a song reveals the verse tiles with verse 1 ticked.',
      body: '<ol><li><strong>On open:</strong> the search input already has focus — no second click to reach it.</li>' +
            '<li><strong>Results:</strong> grouped by book, each row a short reference and title; a hymn reference like <em>kj 12</em> resolves as it does in the product.</li>' +
            '<li><strong>Keyboard:</strong> arrows move through results, Enter picks, Escape closes the list and leaves the input.</li>' +
            '<li><strong>After a pick:</strong> the field becomes the chosen label and the verse field reveals in the same motion; a song with no verses hides the field; a one-verse song mutes it.</li>' +
            '<li><strong>Unchanged:</strong> the backend ranking, book-first order and 200-result cap stay as they are.</li></ol>'
    },
    soft: {
      title: '6 · Soft trigger (verses style B)',
      text: 'The Verses control keeps its dropdown component but loses the dropdown look: a flat summary row with no chevron or box. The tiles expand directly under it, behind a thin rule.',
      body: '<ol><li><strong>Same behavior</strong> as tab 1: click ticks one, press and drag previews a range until release.</li>' +
            '<li><strong>Different look</strong>: the summary reads as a plain line, not a select; the tile block is separated by a hairline, not a floating panel.</li>' +
            '<li><strong>Tap the summary</strong> to collapse or reopen the tiles.</li>' +
            '<li><strong>Compare</strong> with tab 1, where the tiles sit in a visible tinted panel.</li></ol>'
    }
  };
  var state = {
    option: 'tiles', count: 12, selected: new Set([1]), anchor: null,
    typed: '1-3,5,8-10', from: '', to: '', typedError: '', song: 'picked', drag: null, verseStyle: 'inline',
    songChoice: null, songResults: [], songActive: 0
  };
  var $ = function (sel) { return document.querySelector(sel); };
  var control = $('#pvTilesRoot');
  var songFieldOriginal = null;
  window.__pvState = state;  /* preview-only inspection hook */

  function makeSet(a, b) {
    var s = new Set();
    for (var i = a; i <= b; i++) s.add(i);
    return s;
  }
  function numbers() { return Array.from(state.selected).sort(function (a, b) { return a - b; }); }
  function displayCount() {
    return state.song === 'empty' ? 0 : (state.song === 'single' ? 1 : state.count);
  }
  function bounds(n) { return Math.max(1, Math.min(state.count, n)); }
  function rangesOf(list) {
    var out = [];
    list.forEach(function (n) {
      var last = out[out.length - 1];
      if (last && n === last.end + 1) last.end = n;
      else out.push({ start: n, end: n });
    });
    return out;
  }
  function fmtList(list) {
    return rangesOf(list).map(function (r) {
      return r.start === r.end ? String(r.start) : r.start + '–' + r.end;
    }).join(', ');
  }
  function setSelected(list) {
    state.selected = new Set(Array.from(list).filter(function (n) { return n >= 1 && n <= state.count; }));
  }
  function addRange(a, b) {
    var lo = Math.min(a, b), hi = Math.max(a, b);
    for (var n = lo; n <= hi; n++) state.selected.add(bounds(n));
  }
  function carrier() {
    return '<div hidden>' + Array.from({ length: displayCount() }, function (_, i) {
      var n = i + 1;
      return '<input type="checkbox" name="verses" value="' + n + '"' + (state.selected.has(n) ? ' checked' : '') + '>';
    }).join('') + '</div>';
  }
  function quick(label) {
    return '<div class="pv-quick"><span class="pv-quick__label">' + label + '</span>' +
      '<span class="pv-quick__actions"><button type="button" data-act="all">All</button>' +
      '<button type="button" data-act="none">Clear</button></span></div>';
  }
  function summary() {
    if (state.song === 'none') return 'Pick a song first';
    if (state.song === 'empty') return 'This song has no verses';
    var list = numbers();
    if (!list.length) return 'No verses: keep at least one';
    return 'Bait ' + fmtList(list);
  }
  function syncField() {
    var trigger = $('#entry-verses-trigger');
    trigger.textContent = summary();
    trigger.setAttribute('data-muted', String(state.song !== 'picked'));
    $('#editorModal').dataset.song = state.song;
    document.querySelectorAll('[data-song]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.song === state.song));
    });
    var field = $('#pvVersesField');
    var err = field.querySelector('.pv-form-error');
    if (state.song === 'picked' && !state.selected.size) {
      if (!err) {
        err = document.createElement('p');
        err.className = 'pv-form-error';
        err.setAttribute('role', 'alert');
        field.appendChild(err);
      }
      err.textContent = 'No verses: keep at least one';
    } else if (err) err.remove();
    document.querySelectorAll('[data-preset]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.preset === activePreset()));
    });
    syncCarrier();
    syncQuick();
    $('#pvReadout').textContent = INFO[state.option].title + ' · ' + numbers().length + ' of ' + state.count +
      ' verses · ' + (numbers().length ? fmtList(numbers()) : 'none') +
      (state.anchor ? ' · start marked at ' + state.anchor : '');
    $('#pvValues').textContent = numbers().length ? 'verses=' + numbers().join('&verses=') : '(none — the save would be refused)';
  }
  function activePreset() {
    var list = numbers().join(',');
    if (list === Array.from({ length: state.count }, function (_, i) { return i + 1; }).join(',')) return 'all';
    if (list === '1,2,3,5,8,9,10') return 'ranges';
    if (list === '5') return 'one';
    if (!list) return 'none';
    if (state.count === 24) return 'long';
    return '';
  }
  function renderTiles() {
    var html = quick('Click to tick · hold and drag across tiles to extend') + '<div class="pv-tiles" role="group" aria-label="Verses">';
    for (var n = 1; n <= displayCount(); n++) {
      html += '<button type="button" class="pv-tile" data-n="' + n + '" aria-pressed="' +
        state.selected.has(n) + '"' +
        ' aria-label="Verse ' + n + (state.selected.has(n) ? ', selected' : '') + '">' + n + '</button>';
    }
    html += '</div><p class="pv-hint">Click ticks or unticks one verse. Press and drag across tiles to fill the range; it previews until you release.</p>' + carrier();
    return html;
  }
  function renderChips() {
    var html = quick('Add a stretch, remove any chip') +
      '<div class="pv-rangerow"><label>From<input type="number" min="1" max="' + state.count + '" data-from placeholder="1" value="' + state.from + '"></label>' +
      '<label>To<input type="number" min="1" max="' + state.count + '" data-to placeholder="4" value="' + state.to + '"></label>' +
      '<button type="button" data-act="add">Add range</button></div><div class="pv-chips">';
    if (!state.selected.size) html += '<span class="pv-hint">No ranges yet.</span>';
    rangesOf(numbers()).forEach(function (r) {
      html += '<span class="pv-chip">' + (r.start === r.end ? r.start : r.start + '–' + r.end) +
        '<button type="button" data-remove="' + r.start + '-' + r.end + '" aria-label="Remove verses ' + r.start + ' to ' + r.end + '">×</button></span>';
    });
    return html + '</div><p class="pv-typederror" data-error></p>' + carrier();
  }

  /* ---- song search: focused on open, results under the field ------------- */
  var SONGS = [
    { id: 105, book: 'Kidung Jemaat', short: 'KJ', number: 3, sub: '', title: 'Puji Tuhan', verses: 6 },
    { id: 102, book: 'Kidung Jemaat', short: 'KJ', number: 12, sub: '', title: 'Sai puji Naibata', verses: 1 },
    { id: 103, book: 'Kidung Jemaat', short: 'KJ', number: 12, sub: 'a', title: 'Sai puji Naibata', verses: 7 },
    { id: 104, book: 'Kidung Jemaat', short: 'KJ', number: 123, sub: '', title: 'Tuhan yang baik', verses: 8 },
    { id: 101, book: 'Kidung Jemaat', short: 'KJ', number: 152, sub: '', title: 'Kasih setia Tuhan', verses: 12 },
    { id: 108, book: 'Kidung Jemaat', short: 'KJ', number: 411, sub: '', title: 'Waktu pagi', verses: 4 },
    { id: 111, book: 'Kidung Jemaat', short: 'KJ', number: 90, sub: '', title: 'Pagi yang cerah', verses: 0 },
    { id: 106, book: 'Haleluya', short: 'HAL', number: 3, sub: '', title: 'Sai puji Naibata', verses: 0 },
    { id: 107, book: 'Haleluya', short: 'HAL', number: 41, sub: '', title: 'Kasih setia Tuhan', verses: 5 },
    { id: 110, book: 'Lagu Sion', short: 'LS', number: 21, sub: '', title: 'Kasih setia Tuhan', verses: 9 },
    { id: 109, book: 'Lagu Sion', short: 'LS', number: 90, sub: '', title: 'Bait Tunggal', verses: 1 }
  ];
  function songLabel(s) {
    return (s.number ? s.short + ' ' + s.number + (s.sub || '') + ' — ' : '') + s.title;
  }
  function filterSongs(q) {
    q = (q || '').trim().toLowerCase();
    if (!q) return SONGS;
    var m = q.match(/^([a-z]+)\s*(\d+)?/);
    if (m && SONGS.some(function (s) {
      return s.short.toLowerCase() === m[1] || s.book.toLowerCase().indexOf(m[1]) === 0;
    })) {
      return SONGS.filter(function (s) {
        var book = s.short.toLowerCase() === m[1] || s.book.toLowerCase().indexOf(m[1]) === 0;
        return book && (!m[2] || String(s.number).indexOf(m[2]) === 0);
      });
    }
    return SONGS.filter(function (s) {
      return songLabel(s).toLowerCase().indexOf(q) !== -1;
    });
  }
  /* The product's picker menu is fixed to the viewport and capped to the space
     beside its trigger (spec 040). The results must never sit in dialog flow. */
  function placeSongResults() {
    var box = $('[data-songresults]'), input = $('[data-songsearch]');
    if (!box || !input || box.hidden) return;
    var r = input.getBoundingClientRect(), gap = 6, edge = 8;
    var below = window.innerHeight - r.bottom - gap - edge;
    var above = r.top - gap - edge;
    var flip = below < 150 && above > below;
    box.style.left = r.left + 'px';
    box.style.width = r.width + 'px';
    box.style.maxHeight = Math.max(84, flip ? above : below) + 'px';
    if (flip) {
      box.setAttribute('data-flip', 'up');
      box.style.top = 'auto';
      box.style.bottom = (window.innerHeight - r.top + gap) + 'px';
    } else {
      box.removeAttribute('data-flip');
      box.style.top = (r.bottom + gap) + 'px';
      box.style.bottom = 'auto';
    }
    syncHeight();
  }
  function syncHeight() {
    var el = $('#pvHeight'), dialog = $('#editorModal');
    if (el && dialog) el.textContent = 'Modal height: ' + Math.round(dialog.getBoundingClientRect().height) +
      'px · results are a fixed overlay, outside the dialog flow.';
  }
  window.addEventListener('scroll', placeSongResults, true);
  window.addEventListener('resize', placeSongResults);

  function renderSongResults(q) {
    var list = filterSongs(q), box = $('[data-songresults]');
    if (!box) return;
    state.songResults = list;
    if (state.songActive >= list.length) state.songActive = Math.max(0, list.length - 1);
    var html = '', lastBook = null;
    list.forEach(function (s) {
      if (s.book !== lastBook) {
        html += '<p class="pv-songgroup-label">' + s.book + '</p>';
        lastBook = s.book;
      }
      var i = list.indexOf(s);
      html += '<button type="button" class="pv-songrow' + (i === state.songActive ? ' is-active' : '') +
        '" data-songid="' + s.id + '"><span class="pv-songref">' +
        (s.short + ' ' + s.number + (s.sub || '')) + '</span><span class="pv-songtitle">' +
        esc(s.title) + '</span><span class="pv-songn">' +
        (s.verses ? s.verses + ' verses' : 'no verses') + '</span></button>';
    });
    if (!list.length) html = '<p class="pv-hint" style="padding:10px 12px">No songs match.</p>';
    box.innerHTML = html;
    placeSongResults();
    syncHeight();
  }
  function selectSong(song) {
    state.songChoice = song;
    state.song = song.verses === 0 ? 'empty' : (song.verses === 1 ? 'single' : 'picked');
    state.selected = state.song === 'empty' ? new Set() : new Set([1]);
    state.anchor = null;
    state.typed = state.song === 'picked' ? '1' : '';
    var input = $('[data-songsearch]');
    if (input) input.value = songLabel(song);
    var hidden = $('#id_song');
    if (hidden) hidden.value = song.id;
    var results = $('[data-songresults]');
    if (results) results.hidden = true;
    render();
    syncHeight();
  }
  function setSongSearchMode(on) {
    var field = $('#pvSongField');
    if (!field) return;
    if (on) {
      if (!songFieldOriginal) songFieldOriginal = field.innerHTML;
      var choice = state.songChoice;
      field.innerHTML = '<label for="pvSongSearch">Song</label><div class="editor__picker" data-entry-picker="song">' +
        '<input type="search" id="pvSongSearch" data-songsearch autocomplete="off" spellcheck="false" ' +
        'aria-label="Search songs" placeholder="Search songs..." value="' + esc(choice ? songLabel(choice) : '') + '">' +
        '<input type="hidden" name="song" id="id_song" value="' + (choice ? choice.id : '') + '">' +
        '<div class="pv-songsearch-results" data-songresults></div></div>';
      renderSongResults('');
      var input = field.querySelector('[data-songsearch]');
      window.setTimeout(function () { input.focus(); input.select(); }, 0);
    } else if (songFieldOriginal) {
      field.innerHTML = songFieldOriginal;
      var label = field.querySelector('[data-picker-label]');
      if (label) label.textContent = state.songChoice ? songLabel(state.songChoice) : 'Choose a song';
      var hidden = field.querySelector('#id_song');
      if (hidden) hidden.value = state.songChoice ? state.songChoice.id : '';
    }
  }
  var songField = $('#pvSongField');
  songField.addEventListener('input', function (event) {
    if (!event.target.matches('[data-songsearch]')) return;
    var box = $('[data-songresults]');
    box.hidden = false;
    state.songActive = 0;
    renderSongResults(event.target.value);
  });
  songField.addEventListener('focusin', function (event) {
    if (!event.target.matches('[data-songsearch]')) return;
    var box = $('[data-songresults]');
    box.hidden = false;
    renderSongResults(event.target.value);
  });
  songField.addEventListener('click', function (event) {
    var row = event.target.closest('[data-songid]');
    if (!row) return;
    var id = Number(row.dataset.songid);
    var song = SONGS.filter(function (s) { return s.id === id; })[0];
    if (song) selectSong(song);
  });
  songField.addEventListener('keydown', function (event) {
    if (!event.target.matches('[data-songsearch]')) return;
    var input = event.target;
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      state.songActive = Math.max(0, Math.min(state.songResults.length - 1,
        state.songActive + (event.key === 'ArrowDown' ? 1 : -1)));
      renderSongResults(input.value);
    } else if (event.key === 'Enter') {
      event.preventDefault();
      if (state.songResults[state.songActive]) selectSong(state.songResults[state.songActive]);
    } else if (event.key === 'Escape') {
      event.stopPropagation();
      $('[data-songresults]').hidden = true;
    }
  });

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function chipMarkup() {
    var html = '';
    if (!state.selected.size) html = '<span class="pv-hint">No ranges yet.</span>';
    rangesOf(numbers()).forEach(function (r) {
      html += '<span class="pv-chip">' + (r.start === r.end ? r.start : r.start + '–' + r.end) +
        '<button type="button" data-remove="' + r.start + '-' + r.end +
        '" aria-label="Remove verses ' + r.start + ' to ' + r.end + '">×</button></span>';
    });
    return html;
  }
  function renderTyped() {
    return quick('Type the verses as you say them') +
      '<div class="pv-typedrow"><input type="text" data-typed spellcheck="false" ' +
      'aria-label="Verse ranges" placeholder="1-3,5,8-10" value="' + esc(state.typed) + '">' +
      '<button type="button" data-act="parse">Apply</button></div>' +
      '<div class="pv-chip-area" data-chiparea>' + chipMarkup() + '</div>' +
      '<p class="pv-typederror" data-error></p>' + carrier();
  }
  function renderCheckboxes() {
    var html = quick('The shipped list, with larger targets and helpers') + '<div class="pv-checkboxes" role="group" aria-label="Verses">';
    for (var n = 1; n <= displayCount(); n++) {
      html += '<label' + (state.anchor === n ? ' data-anchor="true"' : '') + '><input type="checkbox" data-v="' +
        n + '"' + (state.selected.has(n) ? ' checked' : '') + '><span>' + n + '</span></label>';
    }
    return html + '</div><p class="pv-hint">Shift+tick extends from the last ticked verse.</p>' + carrier();
  }
  function parseTyped(raw) {
    var picked = new Set(), bad = [];
    String(raw).split(',').forEach(function (part) {
      part = part.trim();
      if (!part) return;
      var m = part.match(/^(\d+)\s*(?:[-–]\s*(\d+))?$/);
      if (!m) { bad.push(part); return; }
      var a = Number(m[1]), b = m[2] ? Number(m[2]) : a;
      if (a < 1 || b < 1 || a > state.count || b > state.count || a > b) { bad.push(part); return; }
      for (var n = a; n <= b; n++) picked.add(n);
    });
    return { set: picked, bad: bad };
  }
  function applyTyped() {
    var parsed = parseTyped(state.typed);
    setSelected(Array.from(parsed.set));
    state.typedError = parsed.bad.length ? 'Could not read: ' + parsed.bad.join(', ') + '. Ignored.' : '';
    var area = control.querySelector('[data-chiparea]');
    if (area) area.innerHTML = chipMarkup();
    var err = control.querySelector('[data-error]');
    if (err) err.textContent = state.typedError;
    syncField();
  }
  function render() {
    var html = (state.option === 'tiles' || state.option === 'song' || state.option === 'soft') ? renderTiles()
      : state.option === 'chips' ? renderChips()
      : state.option === 'typed' ? renderTyped()
      : renderCheckboxes();
    control.innerHTML = html;
    var err = control.querySelector('[data-error]');
    if (err) err.textContent = state.option === 'typed' ? state.typedError : (state.chipError || '');
    syncField();
  }
  function syncCarrier() {
    control.querySelectorAll('input[name="verses"]').forEach(function (input) {
      input.checked = state.selected.has(Number(input.value));
    });
  }
  function afterChange(refocus) {
    render();
    if (refocus && control.querySelector('[data-n="' + refocus + '"]')) {
      control.querySelector('[data-n="' + refocus + '"]').focus();
    }
  }
  function handleTile(n, shift) {
    if (shift && state.anchor !== null) addRange(state.anchor, n);
    else if (state.selected.has(n)) state.selected.delete(n);
    else state.selected.add(n);
    state.anchor = n;   /* the last ticked verse is the Shift anchor */
    afterChange(n);
  }
  function syncQuick() {
    control.querySelectorAll('[data-act="all"]').forEach(function (b) {
      b.disabled = state.selected.size >= displayCount();
    });
    control.querySelectorAll('[data-act="none"]').forEach(function (b) {
      b.disabled = state.selected.size === 0;
    });
  }
  function removeRange(spec) {
    var pair = spec.split('-').map(Number);
    for (var n = pair[0]; n <= pair[1]; n++) state.selected.delete(n);
    if (state.option === 'typed') {
      state.typed = rangesOf(numbers()).map(function (r) {
        return r.start === r.end ? String(r.start) : r.start + '-' + r.end;
      }).join(',');
      render();
    } else afterChange();
  }
  function addTypedRange() {
    var fromEl = control.querySelector('[data-from]'), toEl = control.querySelector('[data-to]');
    var a = Number(fromEl.value), b = Number(toEl.value);
    state.from = fromEl.value; state.to = toEl.value;
    if (!a || !b || a < 1 || b < 1 || a > state.count || b > state.count || a > b) {
      state.chipError = 'Enter two verse numbers from 1 to ' + state.count + ', lowest first.';
      render();
      return;
    }
    state.chipError = '';
    addRange(a, b);
    afterChange();
  }

  control.addEventListener('click', function (event) {
    var act = event.target.closest('[data-act]');
    if (act) {
      if (act.dataset.act === 'all') setSelected(Array.from({ length: state.count }, function (_, i) { return i + 1; }));
      if (act.dataset.act === 'none') setSelected([]);
      if (act.dataset.act === 'add') { addTypedRange(); return; }
      if (act.dataset.act === 'parse') { state.typed = control.querySelector('[data-typed]').value; applyTyped(); return; }
      state.anchor = null; state.chipError = ''; render(); return;
    }
    var remove = event.target.closest('[data-remove]');
    if (remove) { removeRange(remove.dataset.remove); return; }
    var tile = event.target.closest('[data-n]');
    if (tile) { if (event.detail === 0) handleTile(Number(tile.dataset.n), event.shiftKey); return; }
    var box = event.target.closest('input[data-v]');
    if (box) {
      event.preventDefault();
      var n = Number(box.dataset.v);
      if (event.shiftKey && state.anchor !== null) addRange(state.anchor, n);
      else if (state.selected.has(n)) state.selected.delete(n);
      else state.selected.add(n);
      state.anchor = n;
      afterChange();
    }
  });
  control.addEventListener('input', function (event) {
    if (event.target.matches('[data-typed]')) { state.typed = event.target.value; applyTyped(); }
    if (event.target.matches('[data-from]')) state.from = event.target.value;
    if (event.target.matches('[data-to]')) state.to = event.target.value;
  });
  control.addEventListener('input', function () { syncCarrier(); });
  function onTileDragMove(event) {
    if (!state.drag) return;
    var el = document.elementFromPoint(event.clientX, event.clientY);
    var tile = el && el.closest ? el.closest('[data-n]') : null;
    if (!tile) return;
    var n = Number(tile.dataset.n);
    if (n === state.drag.current) return;
    state.drag.current = n;
    state.drag.moved = true;
    paintDragPreview();
  }
  function paintDragPreview() {
    if (!state.drag) return;
    var lo = Math.min(state.drag.start, state.drag.current);
    var hi = Math.max(state.drag.start, state.drag.current);
    document.querySelectorAll('.pv-tile').forEach(function (tile) {
      var n = Number(tile.dataset.n);
      tile.classList.toggle('is-preview', n >= lo && n <= hi);
      tile.classList.toggle('is-dragover', n === state.drag.current);
    });
    $('#pvReadout').textContent = 'Preview: Bait ' + lo + (hi === lo ? '' : '–' + hi) +
      ' · release to keep';
  }
  function onTileDragEnd() {
    if (!state.drag) return;
    var drag = state.drag;
    state.drag = null;
    document.removeEventListener('pointermove', onTileDragMove);
    document.removeEventListener('pointerup', onTileDragEnd);
    document.removeEventListener('pointercancel', onTileDragEnd);
    if (!drag.moved) {
      if (state.selected.has(drag.start)) state.selected.delete(drag.start);
      else state.selected.add(drag.start);
      state.anchor = null;
    } else {
      addRange(drag.start, drag.current);   /* commit only on release */
      state.anchor = null;
    }
    afterChange(drag.current);
  }
  control.addEventListener('pointerdown', function (event) {
    var tile = event.target.closest('[data-n]');
    if (!tile || event.button !== 0) return;
    event.preventDefault();
    var n = Number(tile.dataset.n);
    state.drag = { start: n, current: n, moved: false };
    state.anchor = null;
    document.addEventListener('pointermove', onTileDragMove);
    document.addEventListener('pointerup', onTileDragEnd);
    document.addEventListener('pointercancel', onTileDragEnd);
  });
  control.addEventListener('keydown', function (event) {
    if (!event.target.matches('[data-n]')) return;
    var n = Number(event.target.dataset.n), next = null;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = event.key === 'ArrowUp' ? n - 5 : n - 1;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = event.key === 'ArrowDown' ? n + 5 : n + 1;
    if (next === null) return;
    event.preventDefault();
    next = bounds(next);
    if (event.shiftKey) { addRange(state.anchor === null ? n : state.anchor, next); state.anchor = next; afterChange(next); }
    else { state.anchor = next; afterChange(next); }
  });

  function setVerseStyle(option) {
    var box = $('#pvControl');
    box.classList.remove('pv-inline-panel', 'pv-verse-panel', 'pv-soft-panel');
    $('#pvTilesRoot').hidden = false;
    box.classList.add(option === 'tiles' ? 'pv-verse-panel'
      : option === 'soft' ? 'pv-soft-panel' : 'pv-inline-panel');
  }
  function selectOption(name, updateHash) {
    if (OPTIONS.indexOf(name) === -1) name = 'tiles';
    state.option = name;
    state.anchor = null;
    state.chipError = '';
    var info = INFO[name];
    $('#pvOptionTitle').textContent = info.title;
    $('#pvOptionText').textContent = info.text;
    $('#pvDescription').innerHTML = info.body;
    document.querySelectorAll('[data-option]').forEach(function (b) {
      b.setAttribute('aria-selected', String(b.dataset.option === name));
    });
    if (updateHash) history.replaceState(null, '', '#' + name);
    setSongSearchMode(name === 'song');
    setVerseStyle(name);
    render();
    window.requestAnimationFrame(syncHeight);
    window.setTimeout(syncHeight, 250);
  }
  function applyPreset(name) {
    if (name === 'all') setSelected(Array.from({ length: state.count }, function (_, i) { return i + 1; }));
    if (name === 'ranges') { state.count = 12; setSelected([1, 2, 3, 5, 8, 9, 10]); }
    if (name === 'one') setSelected([5]);
    if (name === 'none') setSelected([]);
    if (name === 'long') { state.count = 24; setSelected(makeSet(1, 24)); }
    state.anchor = null;
    state.chipError = '';
    state.typed = numbers().map(function (n) { return String(n); }).join(',');
    if (name === 'all') state.typed = '1-' + state.count;
    if (name === 'ranges') state.typed = '1-3,5,8-10';
    if (name === 'long') state.typed = '1-24';
    state.typedError = '';
    if (name === 'one') state.typed = '5';
    if (name === 'none') state.typed = '';
    state.from = ''; state.to = '';
    render();
  }
  $('#entry-verses-trigger').addEventListener('click', function () {
    if (state.option !== 'soft') return;
    var box = $('#pvTilesRoot');
    box.hidden = !box.hidden;
  });
  document.querySelectorAll('[data-option]').forEach(function (b) {
    b.addEventListener('click', function () { selectOption(b.dataset.option, true); });
  });
  document.querySelectorAll('[data-preset]').forEach(function (b) {
    b.addEventListener('click', function () { applyPreset(b.dataset.preset); });
  });
  document.querySelectorAll('[data-song]').forEach(function (b) {
    b.addEventListener('click', function () {
      state.song = b.dataset.song;
      if (state.song === 'picked' || state.song === 'single') setSelected([1]);
      if (state.song === 'empty') setSelected([]);
      state.anchor = null;
      document.querySelector('[data-picker-label]').textContent = state.song === 'picked'
        ? 'KJ 152 — Kasih setia Tuhan'
        : (state.song === 'none' ? 'Choose a song'
          : (state.song === 'single' ? 'KJ 12 — (one verse)' : 'KJ 12 — (no verses)'));
      $('#id_song').value = state.song === 'picked' ? '152' : (state.song === 'none' ? '' : '12');
      render();
    });
  });
  $('#pvPrev').addEventListener('click', function () {
    selectOption(OPTIONS[(OPTIONS.indexOf(state.option) + OPTIONS.length - 1) % OPTIONS.length], true);
  });
  $('#pvNext').addEventListener('click', function () {
    selectOption(OPTIONS[(OPTIONS.indexOf(state.option) + 1) % OPTIONS.length], true);
  });
  $('#pvSlow').addEventListener('click', function () {
    var on = document.body.classList.toggle('pv-slow');
    this.setAttribute('aria-pressed', String(on));
  });
  $('#pvTheme').addEventListener('click', function () {
    var root = document.documentElement;
    var dark = root.getAttribute('data-theme') === 'dark';
    root.setAttribute('data-theme', dark ? 'light' : 'dark');
    this.textContent = dark ? 'Dark' : 'Light';
  });
  $('#pvForm').addEventListener('submit', function (event) {
    event.preventDefault();
    $('#pvReadout').textContent += ' · Save pressed with ' + numbers().length + ' verse value(s)';
  });
  window.addEventListener('hashchange', function () { selectOption(location.hash.slice(1), false); });
  document.addEventListener('keydown', function (event) {
    if (event.target.matches('input, textarea')) return;
    if (event.key >= '1' && event.key <= '4') { selectOption(OPTIONS[Number(event.key) - 1], true); return; }
    if (event.key === 'ArrowLeft') { $('#pvPrev').click(); return; }
    if (event.key === 'ArrowRight') { $('#pvNext').click(); return; }
    if (event.key === 's' || event.key === 'S') { $('#pvSlow').click(); return; }
    if (event.key === 't' || event.key === 'T') { $('#pvTheme').click(); return; }
    if (event.key === 'Escape' && state.anchor !== null) { state.anchor = null; afterChange(); }
  });
  if (window.ResizeObserver) new ResizeObserver(syncHeight).observe($('#editorModal'));
  state.songChoice = SONGS.filter(function (s) { return s.id === 101; })[0];
  selectOption(location.hash.slice(1), false);

})();
