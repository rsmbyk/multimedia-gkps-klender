/* Spec 092: render saved public content into the existing reading shell. */
(function () {
  'use strict';
  var library = window.GKPSOffline;
  if (!library) return;
  function escape(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (character) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[character];
    });
  }
  function route(url) {
    var parsed = new URL(url, location.href);
    if (parsed.origin !== location.origin) return null;
    var path = parsed.pathname;
    var match;
    if (path === '/bible/' || path === '/songs/' || path === '/tatib/')
      return {kind: 'list', section: path === '/bible/' ? 'alkitab'
        : path === '/songs/' ? 'kidung' : 'tatib', url: parsed};
    if ((match = path.match(/^\/bible\/(\d+)\/$/)))
      return {kind: 'book', section: 'alkitab', id: Number(match[1]), url: parsed};
    if ((match = path.match(/^\/songs\/book\/(\d+)\/$/)))
      return {kind: 'book', section: 'kidung', id: Number(match[1]), url: parsed};
    if ((match = path.match(/^\/bible\/(\d+)\/(\d+)\/$/)))
      return {kind: 'bible', id: Number(match[1]), chapter: Number(match[2]), url: parsed};
    if ((match = path.match(/^\/songs\/(\d+)\/$/)))
      return {kind: 'song', id: Number(match[1]), url: parsed};
    if ((match = path.match(/^\/tatib\/(\d+)\/$/)))
      return {kind: 'service', id: Number(match[1]), url: parsed};
    if (path === '/search' || path === '/search/')
      return {kind: 'search', query: (parsed.searchParams.get('q') || '').trim(), url: parsed};
    if (path === '/' || path === '/home/') return {kind: 'home', url: parsed};
    return null;
  }
  function loadShell() {
    return caches.match('/home/').then(function (response) {
      if (!response) return null;
      return response.text();
    }).then(function (html) {
      return html ? new DOMParser().parseFromString(html, 'text/html') : null;
    });
  }
  function bookLink(book, selected, kind, editorEnabled) {
    var name = kind === 'bible' ? (book.translations.find(function (item) {
      return item.version.toUpperCase() === 'TB';
    }) || book.translations[0] || {}).name || book.name : book.name;
    var short = kind === 'bible' ? book.name : kind === 'service'
      ? book.date_display || book.short_name : book.short_name;
    var href = kind === 'bible' ? '/bible/' + book.id + '/' : kind === 'songs'
      ? '/songs/book/' + book.id + '/' : '/tatib/' + book.id + '/';
    var editor = editorEnabled ? kind === 'service' ? 'tatib'
      : kind === 'songs' && !book.is_hymn_book ? 'songbook' : '' : '';
    return '<li><a class="book" href="' + href + '" data-name="' + escape(kind === 'bible' ? name : book.id)
      + '" data-sim="' + escape(kind === 'service' ? book.id : short || '') + '" aria-label="' + escape(name)
      + (short ? ' (' + escape(short) + ')' : '')
      + '"' + (selected ? ' aria-current="true"' : '') + '><span class="book__n">'
      + escape(name) + '</span><span class="book__s">' + escape(short || '') + '</span></a>'
      + (editor ? '<button class="row-edit" type="button" data-editor-open="' + editor
        + '" data-editor-id="' + book.id + '" aria-label="Edit ' + escape(name)
        + '">Edit</button>' : '') + '</li>';
  }
  function addButtons(serviceId) {
    return ['scripture', 'song', 'text', 'section_break'].map(function (kind) {
      var names = {scripture: 'Passage', song: 'Song', text: 'Text', section_break: 'Break'};
      return '<button type="button" class="entry__add-btn" data-entry-open="' + kind
        + '" data-entry-tatib="' + serviceId + '">+ ' + names[kind] + '</button>';
    }).join('');
  }
  function editorButton(kind, id, label, danger) {
    var icon = danger
      ? '<path d="M3.6 5.4h12.8M8.2 5.4V3.8h3.6v1.6M5.4 5.4l.8 10.4h7.6l.8-10.4M8.6 8.6v4.4M11.4 8.6v4.4"/>'
      : '<path d="M13.4 3.6l3 3-8.6 8.6H4.4v-2.2zM11.6 5.4l3 3"/>';
    var dataAttr = kind === 'entry' ? 'data-entry-' + (danger ? 'delete' : 'edit')
      : 'data-old-item-' + (danger ? 'delete' : 'edit');
    return '<button type="button" class="entry__ctrl' + (danger
      ? ' entry__ctrl--danger' : '') + '" ' + dataAttr + '="' + id + '">'
      + '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"'
      + ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + icon
      + '</svg>' + (danger ? 'Delete' : 'Edit') + '</button>';
  }
  function previewMarkup(preview, anchor, canEdit) {
    if (!preview) return '';
    var html = '';
    function paraMarkup(para, className) {
      return '<p class="' + className + (para.voice ? ' is-' + escape(para.voice) : '') + '">'
        + (para.mark ? '<span class="tatib__sp">' + escape(para.mark) + '</span> ' : '')
        + escape(para.text || '') + '</p>';
    }
    if (preview.kind === 'editable_text') {
      html = '<div class="preview__split" data-screen-breaks="' + escape(preview.breaks_json)
        + '" data-default-screen-mode="' + escape(preview.default_screen_mode)
        + '" data-screen-state-signature="' + escape(preview.screen_state_signature)
        + '" data-text-signature="' + escape(preview.signature) + '" data-save-url="'
        + escape(preview.save_url) + '" data-can-edit="' + (canEdit ? 'true' : 'false') + '">'
        + (preview.title ? '<p class="preview__ref">' + escape(preview.title) + '</p>' : '')
        + (preview.reset_notice ? '<p class="preview__notice" role="status">Text lines changed, so the custom breaks were reset.</p>' : '')
        + '<div class="preview__rows">' + (preview.lines || []).map(function (line) {
          var row = line.present ? paraMarkup(line, 'preview__line preview__row')
            : '<div class="preview__blank-line" aria-label="Blank line"></div>';
          return row + (line.can_break_after ? '<button type="button" class="preview__gap" data-break-after="'
            + line.index + '" data-multi-boundary="' + (line.multi_boundary ? 'true' : 'false')
            + '" aria-label="Add screen break after line ' + line.index + '"><span data-break-label>Add break</span></button>' : '');
        }).join('') + '</div><p class="preview__error" data-break-error role="alert" hidden></p></div>';
    } else if (preview.kind === 'song') {
      var verses = preview.verses || [];
      html = '<p class="preview__song">' + escape(preview.heading) + '</p>'
        + (verses.length > 1 ? '<div class="preview__tabs" role="tablist">' + verses.map(function (verse, index) {
          return '<button type="button" role="tab" class="preview__tab" aria-selected="'
            + (index === 0 ? 'true' : 'false') + '"' + (index ? ' tabindex="-1"' : '')
            + '>' + escape(verse.number) + '</button>';
        }).join('') + '</div>' : '')
        + '<div class="preview__panels">' + verses.map(function (verse, index) {
          return '<div class="preview__panel" role="tabpanel"' + (index ? ' hidden' : '')
            + '>' + (verse.lines || []).map(function (line) {
              return '<p class="preview__line">' + escape(line) + '</p>';
            }).join('') + '</div>';
        }).join('') + '</div>';
    } else {
      html = (preview.reference ? '<p class="preview__ref">' + escape(preview.reference) + '</p>' : '')
        + (preview.paras || []).map(function (para) {
          return paraMarkup(para, 'preview__line');
        }).join('');
    }
    return '<script type="text/template" class="entry__preview-src" data-preview-for="'
      + escape(anchor) + '">' + html + '</script>';
  }
  function panelAddButton(section) {
    var editor = section === 'kidung' ? 'songbook' : 'tatib';
    var label = section === 'kidung' ? 'Add songbook' : 'Add Tata Ibadah';
    return '<button class="editor-add" type="button" id="panelAdd" data-editor-open="'
      + editor + '" data-editor-label="' + label + '"><svg viewBox="0 0 20 20" fill="none"'
      + ' stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true">'
      + '<path d="M10 4.5v11M4.5 10h11"/></svg><span class="editor-add__label">'
      + label + '</span></button>';
  }
  function songAddButton(bookId) {
    return '<div class="ch__add"><button class="editor-add" type="button" id="songAdd"'
      + ' data-editor-open="song" data-editor-book="' + bookId + '"'
      + ' data-editor-label="Add song"><svg viewBox="0 0 20 20" fill="none"'
      + ' stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true">'
      + '<path d="M10 4.5v11M4.5 10h11"/></svg><span class="editor-add__label">Add song</span>'
      + '</button></div>';
  }
  function moveGrip(id, label) {
    return '<button type="button" class="toc__grip" data-move-grip="' + id
      + '" aria-label="Reorder ' + escape(label)
      + ': drag, or move it with the arrow keys" title="Drag to reorder">'
      + '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7"'
      + ' stroke-linecap="round" aria-hidden="true"><path d="M7 5.5h.01M13 5.5h.01M7 10h.01M13 10h.01M7 14.5h.01M13 14.5h.01"/></svg></button>';
  }
  var MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
  var MONTHS_LONG = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
  function dateParts(value) {
    var match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value || '');
    return match ? {year: Number(match[1]), month: Number(match[2]), day: Number(match[3])} : null;
  }
  function servicePanel(services, selectedId, mode, editor) {
    var filtered = services.filter(function (service) {
      return mode === 'template' ? !service.date : !!service.date;
    });
    var groups = {};
    if (mode === 'template') {
      filtered.sort(function (a, b) {
        return normalized(a.name).replace(/\|/g, '').localeCompare(normalized(b.name).replace(/\|/g, ''));
      });
      groups.Templates = filtered;
    } else {
      filtered.sort(function (a, b) {
        return String(b.date).localeCompare(String(a.date)) || b.id - a.id;
      });
      filtered.forEach(function (service) {
        var parts = dateParts(service.date);
        if (!parts) return;
        var key = parts.year + '-' + String(parts.month).padStart(2, '0');
        if (!groups[key]) groups[key] = [];
        groups[key].push(service);
      });
    }
    return Object.keys(groups).map(function (key) {
      var group = groups[key];
      var parts = mode === 'template' ? null : dateParts(group[0].date);
      var label = mode === 'template' ? key : MONTHS_LONG[parts.month - 1] + ' ' + parts.year;
      var rows = group.map(function (service) {
        var date = dateParts(service.date);
        var dateLabel = date ? date.day + ' ' + MONTHS_SHORT[date.month - 1] + ' ' + date.year : '';
        return bookLink(Object.assign({}, service, {date_display: dateLabel}),
          service.id === selectedId, 'service', editor);
      }).join('');
      return '<section class="group"' + (mode === 'dated' ? ' data-month="' + key + '"' : '')
        + '><h3 class="group__head">' + escape(label) + '</h3><ul>' + rows + '</ul></section>';
    }).join('');
  }
  function tatibModeButton(url, mode) {
    var label = mode === 'template' ? 'Show dated Tata Ibadah' : 'Show Tata Ibadah templates';
    return '<a class="ch__sort panel__mode" id="tatibMode" href="' + escape(url)
      + '" aria-pressed="' + (mode === 'template') + '" aria-label="' + label
      + '" title="' + label + '"><svg class="panel__mode-dated" viewBox="0 0 20 20" fill="none"'
      + ' stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
      + ' aria-hidden="true"><rect x="2.5" y="4.5" width="15" height="13" rx="2"/>'
      + '<path d="M2.5 8.5h15M6 2.5v4M14 2.5v4M6 12h2M12 12h2"/></svg>'
      + '<svg class="panel__mode-template" viewBox="0 0 20 20" fill="none" stroke="currentColor"'
      + ' stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
      + '<path d="M4 2.5h8l4 4v11H4zM12 2.5v4h4M7 10h6M7 13h6"/></svg></a>';
  }
  function common(doc, section, title, name, number, body, panel, children, target, songListOpen) {
    var root = doc.documentElement;
    root.dataset.section = section;
    root.dataset.nav = 'open';
    root.dataset.ch = 'open';
    root.dataset.read = 'on';
    root.dataset.home = 'reading';
    root.dataset.chMode = section === 'alkitab' ? 'chapter' : 'song';
    doc.title = title + ' — GKPS Klender';
    doc.querySelector('#panelTitle').textContent = section === 'alkitab' ? 'Books — Alkitab'
      : section === 'kidung' ? 'Songbooks' : 'Tata Ibadah';
    doc.querySelector('label[for="bookFilter"]').textContent = section === 'alkitab'
      ? 'Filter books' : section === 'kidung' ? 'Filter songbooks' : 'Filter Tata Ibadah';
    doc.querySelector('#panelBody').innerHTML = panel;
    doc.querySelector('#panelEmpty').textContent = section === 'alkitab' ? 'No matching books.'
      : section === 'kidung' ? 'No matching songbooks.' : 'No matching Tata Ibadah.';
    doc.querySelector('#chList').innerHTML = children;
    doc.querySelector('#chTitle').textContent = section === 'alkitab' ? 'Chapters — ' + name
      : section === 'kidung' ? 'Song list' : 'Service contents';
    doc.querySelector('.ch__search').hidden = section === 'alkitab';
    doc.querySelector('label[for="songFilter"]').textContent = section === 'tatib'
      ? 'Filter sections' : 'Filter songs';
    doc.querySelector('#songFilter').placeholder = section === 'tatib'
      ? 'Filter sections...' : 'Filter songs...';
    doc.querySelector('#chEmpty').textContent = section === 'tatib'
      ? 'No matching sections.' : 'No matching songs.';
    doc.querySelector('#songSort').hidden = section !== 'kidung' || !songListOpen;
    var panelAdd = doc.querySelector('#panelAdd');
    if (panelAdd) panelAdd.remove();
    var panelFilter = doc.querySelector('.panel__filter');
    if (doc.querySelector('#editorModal') && panelFilter
        && (section === 'kidung' || section === 'tatib')) {
      panelFilter.insertAdjacentHTML('afterend', panelAddButton(section));
    }
    var read = doc.querySelector('#read');
    read.dataset.kind = section === 'alkitab' ? 'bible' : section === 'kidung' ? 'song' : 'tatib';
    doc.querySelector('#readName').textContent = name;
    doc.querySelector('#readNo').textContent = number || '';
    doc.querySelector('#readEyebrow').textContent = section === 'alkitab' ? ''
      : section === 'kidung' ? 'Kidung' : 'Tata Ibadah';
    doc.querySelector('#readEyebrow').hidden = section === 'alkitab';
    doc.querySelector('#readBody').innerHTML = body;
    doc.querySelector('#offlineSavedSource').hidden = false;
    doc.querySelector('#searchResults').hidden = true;
    doc.querySelector('#searchResults').innerHTML = '';
    doc.querySelector('#searchQuery').value = '';
    doc.querySelector('#searchQuery').setAttribute('value', '');
    if (target) {
      var targetRow = doc.querySelector(target);
      if (targetRow) targetRow.dataset.searchTarget = 'true';
    }
    return doc;
  }
  function biblePage(doc, route, book, books) {
    var tb = book.translations.find(function (item) { return item.version.toUpperCase() === 'TB'; });
    var sim = book.translations.find(function (item) { return item.version.toUpperCase() === 'SIM'; });
    var name = (tb || sim || {}).name || book.name;
    var requested = route.url.searchParams.get('ed') === 'sim' && sim ? 'sim' : 'tb';
    function chapterRows(translation) {
      return translation ? translation.verses.filter(function (row) {
        return row.chapter === route.chapter;
      }) : [];
    }
    var tbRows = chapterRows(tb), simRows = chapterRows(sim);
    if (!tbRows.length && !simRows.length) return null;
    if (requested === 'tb' && !tbRows.length) requested = 'sim';
    function edition(rows, code) {
      return '<div class="read__ed" data-ed="' + code + '"'
        + (requested !== code ? ' hidden' : '') + '>' + rows.map(function (row) {
          return (row.title ? '<h2 class="read__sec">' + escape(row.title) + '</h2>' : '')
            + '<p class="v" data-verse="' + row.verse + '"><span class="v__n">'
            + row.verse + '</span><span>' + escape(row.text) + '</span></p>';
        }).join('') + '</div>';
    }
    var body = edition(tbRows, 'tb') + (simRows.length ? edition(simRows, 'sim') : '');
    var panel = '<section class="group"><ul>' + books.map(function (item) {
      return bookLink(item, item.id === book.id, 'bible', !!doc.querySelector('#editorModal'));
    }).join('') + '</ul></section>';
    var chapters = Array.from({length: book.chapters}, function (_, index) {
      var n = index + 1;
      var hasTb = tb && tb.verses.some(function (row) { return row.chapter === n; });
      var hasSim = sim && sim.verses.some(function (row) { return row.chapter === n; });
      return '<li><a class="ch-num' + (hasTb ? '' : ' no-data')
        + '" href="/bible/' + book.id + '/' + n + '/" data-n="' + n + '" data-tb="'
        + !!hasTb + '" data-sim="' + !!hasSim + '" aria-label="' + escape(name)
        + ' chapter ' + n + '"' + (n === route.chapter ? ' aria-current="true"' : '')
        + (!hasTb && !hasSim ? ' aria-disabled="true"' : '') + '>' + n + '</a></li>';
    }).join('');
    common(doc, 'alkitab', name + ' ' + route.chapter, name, route.chapter,
      body, panel, chapters, '[data-verse="' + (route.url.searchParams.get('v') || '') + '"]');
    var row = doc.querySelector('.read__row');
    var lang = doc.createElement('div');
    lang.className = 'read__lang';
    lang.setAttribute('role', 'group');
    lang.setAttribute('aria-label', 'Choose reading translation');
    lang.dataset.edition = requested;
    lang.innerHTML = '<span class="read__lang-thumb" aria-hidden="true"></span>'
      + '<a id="langTb" href="?ed=tb" aria-pressed="' + (requested === 'tb') + '">TB</a>'
      + '<a id="langSim" href="?ed=sim" aria-pressed="' + (requested === 'sim')
      + '"' + (!simRows.length ? ' data-empty="true" aria-disabled="true"' : '') + '>SIM</a>';
    row.appendChild(lang);
    return doc;
  }
  function songPage(doc, song, book, books) {
    var citation = book.is_hymn_book ? (book.name + ' ' + song.number
      + (song.sub_number || '').toUpperCase()) : song.title;
    if (!citation) citation = book.name;
    var panel = '<section class="group"><ul>' + books.map(function (item) {
      return bookLink(item, item.id === book.id, 'songs', !!doc.querySelector('#editorModal'));
    }).join('') + '</ul></section>';
    var editor = !!doc.querySelector('#editorModal') && !book.is_hymn_book;
    var children = book.songs.map(function (item, index) {
      var number = item.number == null ? '' : item.number + (item.sub_number || '').toUpperCase();
      return '<li><a class="songrow" href="/songs/' + item.id + '/" data-i="' + item.id
        + '" data-t="' + escape(item.sort_title || item.title.toLowerCase()) + '" data-o="' + index
        + '" data-m="' + escape(item.modified_key || '')
        + '" data-num="' + escape(number.toLowerCase()) + '"'
        + (item.id === song.id ? ' aria-current="true"' : '') + '><span class="songrow__c">'
        + escape(number) + '</span><span class="songrow__t">' + escape(item.title)
        + '</span></a>' + (editor ? '<button class="row-edit" type="button" data-editor-open="song"'
          + ' data-editor-id="' + item.id + '" aria-label="Edit ' + escape(item.title)
          + '"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7"'
          + ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          + '<path d="M12.5 4.5l3 3-8 8H4.5v-3z"/></svg></button>' : '') + '</li>';
    }).join('');
    var body = song.verses.map(function (verse, index) {
      return '<p class="v"><span class="v__n">' + (index + 1) + '</span><span>'
        + escape(verse.lyric).replace(/\n/g, '<br>') + '</span></p>';
    }).join('');
    common(doc, 'kidung', citation, song.title || citation, '',
      body, panel, children, null, true);
    doc.querySelector('#readEyebrow').textContent = citation;
    doc.querySelector('#readNo').textContent = '';
    if (editor) doc.querySelector('.ch__top').insertAdjacentHTML('afterend', songAddButton(book.id));
    return doc;
  }
  function servicePage(doc, service, services, target) {
    var editor = !!doc.querySelector('#editorModal');
    var mode = target.url.searchParams.get('mode') || (service.date ? 'dated' : 'template');
    if (mode !== 'template') mode = 'dated';
    var panel = servicePanel(services, service.id, mode, editor);
    var children = (service.toc || []).map(function (item) {
      if (item.eos) return '<li class="toc__eos" data-i="' + escape(item.anchor) + '"'
        + (item.entry ? ' data-move-row>' : ' aria-hidden="true">')
        + '<span class="toc__eosline"></span>'
        + (item.entry ? moveGrip(item.pk, 'this break') : '') + '</li>';
      var label = item.song_label
        ? '<span class="songrow__t songrow__t--song"><span class="songrow__heading">'
          + (item.song_reference ? '<span class="songrow__reference">' + escape(item.song_reference)
            + '</span> ' : '') + '<span class="songrow__title">' + escape(item.song_title)
            + '</span></span>' + (item.verse_line ? '<span class="songrow__verses">'
            + escape(item.verse_line) + '</span>' : '') + '</span>'
        : item.two_line_label
          ? '<span class="songrow__t songrow__t--lines">' + (item.label_lines || []).map(function (line) {
            return '<span class="songrow__line' + (line ? '' : ' songrow__line--blank')
              + '">' + (line ? escape(line) : '&nbsp;') + '</span>';
          }).join('') + '</span>'
          : '<span class="songrow__t">' + escape(item.label) + '</span>';
      return '<li' + (item.entry ? ' data-move-row' : '') + '><a class="songrow' + (item.titled ? '' : ' songrow--cont')
        + '" href="#ti-' + escape(item.anchor) + '"' + (item.entry ? ' draggable="false"' : '')
        + ' data-i="' + escape(item.anchor)
        + '" data-num="' + item.n + '" data-txt="' + escape((item.txt || '').toLowerCase())
        + '"><span class="songrow__c">' + item.n + '</span>' + label + '</a>'
        + (item.entry ? moveGrip(item.pk, item.label) : '') + '</li>';
    }).join('');
    var body = (service.items || []).map(function (item) {
      var actions = '<span class="entry__acts">'
        + (item.preview ? '<button type="button" class="entry__ctrl" data-preview-open'
          + ' data-preview-for="' + escape(item.anchor) + '" aria-label="Preview this entry">'
          + '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"'
          + ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          + '<path d="M2.6 10s2.8-4.6 7.4-4.6S17.4 10 17.4 10s-2.8 4.6-7.4 4.6S2.6 10 2.6 10z"/>'
          + '<circle cx="10" cy="10" r="2.1"/></svg>Preview</button>' : '')
        + (editor && item.pk ? item.entry
          ? (item.eos ? editorButton('entry', item.pk, '', true)
            : editorButton('entry', item.pk, '', false) + editorButton('entry', item.pk, '', true))
          : editorButton('old-item', item.pk, '', false) + editorButton('old-item', item.pk, '', true)
          : '') + '</span>';
      var after = editor ? '<div class="entry__add" data-entry-after="'
        + escape(item.after_marker || item.anchor) + '" role="group" aria-label="Add after this item">'
        + '<span class="entry__add-inner">' + addButtons(service.id) + '</span></div>' : '';
      if (item.eos) return '<div class="tatib__eos" id="ti-' + escape(item.anchor)
        + '" data-anchor="' + escape(item.anchor) + '"'
        + (item.entry ? ' data-entry-pk="' + item.pk + '"' : item.old_item
          ? ' data-old-item-pk="' + item.pk + '"' : '') + '>'
        + (item.note ? '<span class="tatib__note">' + escape(item.note) + '</span>' : '')
        + (editor && item.pk ? actions : '') + '</div>' + after;
      var title = item.title ? '<h2 class="read__sec">'
        + (item.jump ? '<a class="entry__jump" href="' + escape(item.jump)
          + '" data-entry-jump>' + escape(item.title) + '</a>'
          : '<span>' + escape(item.title) + '</span>') + '</h2>' : '';
      var paras = (item.paras || []).map(function (para) {
        return '<p class="tatib__tx' + (para.voice ? ' is-' + escape(para.voice) : '')
          + '">' + (para.mark ? '<span class="tatib__sp">' + escape(para.mark)
          + '</span> ' : '') + escape(para.text) + '</p>';
      }).join('');
      return '<section class="tatib__item' + (item.entry ? ' tatib__item--entry' : '')
        + (item.preview || item.entry || item.old_item ? ' tatib__item--acts' : '') + '" id="ti-' + escape(item.anchor)
        + '" data-anchor="' + escape(item.anchor) + '"'
        + (item.entry ? ' data-entry-pk="' + item.pk + '"' : item.old_item
          ? ' data-old-item-pk="' + item.pk + '"' : '')
        + (item.clipped ? ' data-clipped="true"' : '') + '>' + title
        + (item.deleted_target ? '<p class="entry__deleted-warning" role="status">'
          + 'This song, songbook, or an included verse was deleted.</p>' : '')
        + (item.subtitle ? '<p class="read__sub">' + escape(item.subtitle) + '</p>' : '')
        + paras + (editor || item.preview ? actions : '')
        + previewMarkup(item.preview, item.anchor, editor) + '</section>' + after;
    }).join('');
    if (editor && (service.items || []).length) body = '<div class="entry__start" data-entry-start role="group"'
      + ' aria-label="Add at the start of this Tata Ibadah"><span class="entry__start-inner">'
      + addButtons(service.id) + '</span></div>' + body;
    if (editor && !(service.items || []).length) body = '<div class="entry__empty">'
      + '<p class="entry__empty-title">This Tata Ibadah is empty.</p>'
      + '<p class="entry__empty-hint">Add the first item to start preparing the service.</p>'
      + '<div class="entry__empty-actions">' + addButtons(service.id)
        .replace(/entry__add-btn/g, 'entry__empty-btn').replace(/\+ /g, 'Add ')
      + '</div></div>';
    common(doc, 'tatib', service.name, service.name, '', body, panel, children);
    var otherMode = mode === 'template' ? 'dated' : 'template';
    doc.querySelector('.panel__filter').insertAdjacentHTML('afterbegin',
      tatibModeButton('/tatib/' + service.id + '/?mode=' + otherMode, mode));
    if ((service.toc || []).some(function (item) { return item.entry; })) {
      doc.querySelector('.ch__top').insertAdjacentHTML('afterend',
        '<div class="ch__reorder" data-reorder-group data-reorder-endpoint="/editor/entry/reorder/"'
        + ' data-reorder-for="' + service.id + '"><p class="reorder__status"'
        + ' data-reorder-status role="status"></p></div>');
    }
    var group = doc.createElement('div');
    group.className = 'read__project';
    group.dataset.projectGroup = '';
    group.dataset.displayChannel = 'gkps-service-display';
    group.innerHTML = '<button type="button" class="read__project-btn" data-project-open'
      + ' data-projector-url="/obs/service/' + service.id + '/" data-project-service="'
      + service.id + '" data-label-project="Project" data-label-stop="Stop projecting"'
      + ' aria-label="Project" title="Project"><svg viewBox="0 0 20 20" fill="none"'
      + ' stroke="currentColor" stroke-width="1.6" stroke-linecap="round"'
      + ' stroke-linejoin="round" aria-hidden="true"><rect x="2.4" y="5.2" width="8.6"'
      + ' height="9" rx="1.6"/><circle cx="6.7" cy="9.7" r="1.7"/>'
      + '<path d="M12.4 7.6l4.4-2.1M12.4 9.7h5M12.4 11.8l4.4 2.1"/></svg>'
      + '<span data-project-label>Project</span></button>';
    doc.querySelector('.read__head-top').appendChild(group);
    return doc;
  }
  function normalized(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/\s+/g, ' ').trim().toLowerCase();
  }
  function score(title, meta, body, query) {
    var a = normalized(title), b = normalized(meta), c = normalized(body);
    if (a === query || b === query) return 200;
    if (a.startsWith(query)) return 120;
    if (a.includes(query)) return 95;
    if (b.includes(query)) return 70;
    if (c.includes(query)) return 35;
    return 0;
  }
  function searchPage(doc, target, bible, books, services) {
    var query = target.query;
    if (!query) return homePage(doc, bible);
    var phrase = normalized(query);
    var rows = {bible: [], songs: [], tatib: []};
    function add(kind, title, meta, body, url, priority) {
      var rank = score(title, meta, body, phrase);
      if (rank || priority) rows[kind].push({title: title, meta: meta, body: body,
        url: url, score: priority || rank});
    }
    bible.forEach(function (book) {
      var tb = book.translations.find(function (item) { return item.version.toUpperCase() === 'TB'; });
      var preferred = tb || book.translations[0];
      var name = preferred ? preferred.name : book.name;
      add('bible', name, book.name + ' ' + book.translations.map(function (item) {
        return item.name;
      }).join(' '), '', '/bible/' + book.id + '/');
      book.translations.forEach(function (translation) {
        translation.verses.forEach(function (verse) {
          var label = name + ' ' + verse.chapter + ':' + verse.verse;
          var alias = book.name + ' ' + verse.chapter + ':' + verse.verse;
          var exact = phrase === normalized(label) || phrase === normalized(alias) ? 1000 : 0;
          add('bible', label, translation.version + ' · ' + (verse.title || ''),
              verse.text, '/bible/' + book.id + '/' + verse.chapter + '/?v=' + verse.verse,
              exact);
        });
      });
    });
    books.forEach(function (book) {
      add('songs', book.name, 'Songbook · ' + book.short_name, '', '/songs/book/' + book.id + '/');
      book.songs.forEach(function (song) {
        var reference = song.number == null ? '' : book.short_name + ' ' + song.number
          + (song.sub_number || '').toUpperCase();
        var longRef = song.number == null ? '' : book.name + ' ' + song.number
          + (song.sub_number || '').toUpperCase();
        var lyric = song.verses.map(function (verse) { return verse.lyric; }).join(' ');
        add('songs', song.title, reference + ' ' + longRef + ' ' + book.name,
            lyric, '/songs/' + song.id + '/', phrase === normalized(reference)
            || phrase === normalized(longRef) ? 1000 : 0);
      });
    });
    services.forEach(function (service) {
      var body = service.rows.filter(function (row) {
        return !(row.kind === 'legacy' && row.item_type === 1)
          && !(row.kind === 'entry' && row.entry_kind === 3);
      }).map(function (row) { return row.title + ' ' + row.text; }).join(' ');
      add('tatib', service.name, service.date || 'Tata Ibadah', body,
          '/tatib/' + service.id + '/');
    });
    var names = {bible: 'Alkitab', songs: 'Kidung', tatib: 'Tata Ibadah'};
    var html = '';
    ['bible', 'songs', 'tatib'].forEach(function (kind) {
      var group = rows[kind].sort(function (a, b) {
        return b.score - a.score || a.title.localeCompare(b.title);
      });
      if (!group.length) return;
      var amount = Math.max(8, Number(target.url.searchParams.get(kind)) || 8);
      html += '<section class="result-group" data-kind="' + kind + '"><div class="result-group__head">'
        + '<h2 class="result-group__title">' + names[kind] + '</h2><span class="result-group__count">'
        + group.length + (group.length === 1 ? ' result' : ' results') + '</span></div><ul class="result-list">';
      group.slice(0, amount).forEach(function (row) {
        var excerpt = normalized(row.body).includes(phrase)
          ? row.body.slice(Math.max(0, normalized(row.body).indexOf(phrase) - 44), 172) : '';
        html += '<li><a class="result-row" data-kind="' + kind + '" href="' + escape(row.url)
          + '"><span class="result-row__title">' + escape(row.title)
          + '</span><span class="result-row__meta">' + escape(row.meta)
          + '</span>' + (excerpt ? '<span class="result-row__excerpt">' + escape(excerpt)
          + '</span>' : '') + '</a></li>';
      });
      html += '</ul>';
      if (group.length > amount) {
        var more = new URL(target.url);
        more.searchParams.set(kind, String(amount + 8));
        html += '<a class="result-more" href="' + escape(more.pathname + more.search)
          + '">Show more</a>';
      }
      html += '</section>';
    });
    doc.documentElement.dataset.section = 'alkitab';
    doc.documentElement.dataset.nav = 'closed';
    doc.documentElement.dataset.ch = 'closed';
    doc.documentElement.dataset.read = 'off';
    doc.documentElement.dataset.home = 'results';
    doc.querySelector('#searchQuery').value = query;
    doc.querySelector('#searchQuery').setAttribute('value', query);
    doc.querySelector('#searchResults').innerHTML = '<p class="search-results__intro"'
      + ' id="searchStatus" role="status">' + (html ? 'Results for “' + escape(query)
      + '”' : 'No results for “' + escape(query) + '”. Try another keyword.') + '</p>' + html;
    doc.querySelector('#searchResults').hidden = false;
    doc.title = 'Results for “' + query + '” — GKPS Klender';
    return doc;
  }
  function homePage(doc, bible) {
    doc.documentElement.dataset.section = 'alkitab';
    doc.documentElement.dataset.nav = 'closed';
    doc.documentElement.dataset.ch = 'closed';
    doc.documentElement.dataset.read = 'off';
    doc.documentElement.dataset.home = 'landing';
    doc.querySelector('#searchQuery').value = '';
    doc.querySelector('#searchQuery').setAttribute('value', '');
    doc.querySelector('#searchResults').innerHTML = '';
    doc.querySelector('#searchResults').hidden = true;
    doc.querySelector('#panelBody').innerHTML = '<section class="group"><ul>'
      + bible.map(function (item) { return bookLink(item, false, 'bible', false); }).join('')
      + '</ul></section>';
    doc.title = 'GKPS Klender — Search Alkitab, Kidung, and Tata Ibadah';
    return doc;
  }
  function listPage(doc, target, bible, books, services) {
    var section = target.section;
    var collection = section === 'alkitab' ? bible : section === 'kidung' ? books : services;
    var selected = target.id && collection.find(function (item) { return item.id === target.id; });
    if (target.id && !selected) return null;
    doc.documentElement.dataset.section = section;
    doc.documentElement.dataset.nav = 'open';
    doc.documentElement.dataset.ch = selected ? 'open' : 'closed';
    doc.documentElement.dataset.read = 'off';
    doc.documentElement.dataset.home = 'landing';
    doc.documentElement.dataset.chMode = section === 'alkitab' ? 'chapter' : 'song';
    doc.querySelector('#panelTitle').textContent = section === 'alkitab' ? 'Books — Alkitab'
      : section === 'kidung' ? 'Songbooks' : 'Tata Ibadah';
    doc.querySelector('label[for="bookFilter"]').textContent = section === 'alkitab'
      ? 'Filter books' : section === 'kidung' ? 'Filter songbooks' : 'Filter Tata Ibadah';
    var editor = !!doc.querySelector('#editorModal');
    var mode = target.url.searchParams.get('mode') === 'template' ? 'template' : 'dated';
    var panel = section === 'tatib' ? servicePanel(collection, null, mode, editor)
      : '<section class="group"><ul>' + collection.map(function (item) {
        return bookLink(item, selected && item.id === selected.id,
          section === 'alkitab' ? 'bible' : 'songs', editor);
      }).join('') + '</ul></section>';
    doc.querySelector('#panelBody').innerHTML = panel;
    doc.querySelector('#panelEmpty').textContent = section === 'alkitab' ? 'No matching books.'
      : section === 'kidung' ? 'No matching songbooks.' : 'No matching Tata Ibadah.';
    doc.querySelector('#chTitle').textContent = section === 'alkitab' ? 'Chapters'
      : section === 'kidung' ? 'Song list' : 'Service contents';
    doc.querySelector('.ch__search').hidden = section === 'alkitab';
    doc.querySelector('label[for="songFilter"]').textContent = section === 'tatib'
      ? 'Filter sections' : 'Filter songs';
    doc.querySelector('#songFilter').placeholder = section === 'tatib'
      ? 'Filter sections...' : 'Filter songs...';
    doc.querySelector('#chEmpty').textContent = section === 'tatib'
      ? 'No matching sections.' : 'No matching songs.';
    doc.querySelector('#songSort').hidden = section !== 'kidung' || !selected || selected.is_hymn_book;
    var panelAdd = doc.querySelector('#panelAdd');
    if (panelAdd) panelAdd.remove();
    var panelFilter = doc.querySelector('.panel__filter');
    if (editor && panelFilter && (section === 'kidung' || section === 'tatib')) {
      panelFilter.insertAdjacentHTML('afterend', panelAddButton(section));
    }
    var modeButton = doc.querySelector('#tatibMode');
    if (modeButton) modeButton.remove();
    if (section === 'tatib') {
      var otherMode = mode === 'template' ? 'dated' : 'template';
      panelFilter.insertAdjacentHTML('afterbegin', tatibModeButton('/tatib/?mode=' + otherMode, mode));
    }
    var children = '';
    if (selected && section === 'alkitab') {
      var title = (selected.translations[0] || {}).name || selected.name;
      doc.querySelector('#chTitle').textContent = 'Chapters — ' + title;
      children = Array.from({length: selected.chapters}, function (_, index) {
        var n = index + 1;
        var tb = selected.translations.find(function (translation) {
          return translation.version.toUpperCase() === 'TB';
        });
        var sim = selected.translations.find(function (translation) {
          return translation.version.toUpperCase() === 'SIM';
        });
        var hasTb = tb && tb.verses.some(function (verse) { return verse.chapter === n; });
        var hasSim = sim && sim.verses.some(function (verse) { return verse.chapter === n; });
        return '<li><a class="ch-num' + (hasTb ? '' : ' no-data') + '" href="/bible/'
          + selected.id + '/' + n + '/" data-n="' + n + '" data-tb="' + !!hasTb
          + '" data-sim="' + !!hasSim + '" aria-label="' + escape(title)
          + ' chapter ' + n + '"'
          + (!hasTb && !hasSim ? ' aria-disabled="true"' : '') + '>' + n + '</a></li>';
      }).join('');
    } else if (selected && section === 'kidung') {
      children = selected.songs.map(function (song, index) {
        var number = song.number == null ? '' : song.number + (song.sub_number || '').toUpperCase();
        return '<li><a class="songrow" href="/songs/' + song.id + '/" data-i="' + song.id
          + '" data-t="' + escape(song.sort_title || song.title.toLowerCase()) + '" data-o="' + index
          + '" data-m="' + escape(song.modified_key || '')
          + '" data-num="' + escape(number.toLowerCase()) + '"><span class="songrow__c">' + escape(number)
          + '</span><span class="songrow__t">' + escape(song.title) + '</span></a>'
          + (editor && !selected.is_hymn_book ? '<button class="row-edit" type="button"'
            + ' data-editor-open="song" data-editor-id="' + song.id + '" aria-label="Edit '
            + escape(song.title) + '"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor"'
            + ' stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            + '<path d="M12.5 4.5l3 3-8 8H4.5v-3z"/></svg></button>' : '') + '</li>';
      }).join('');
    }
    doc.querySelector('#chList').innerHTML = children;
    var oldChAdd = doc.querySelector('.ch__add');
    if (oldChAdd) oldChAdd.remove();
    if (editor && selected && section === 'kidung' && !selected.is_hymn_book) {
      doc.querySelector('.ch__top').insertAdjacentHTML('afterend', songAddButton(selected.id));
    }
    doc.title = (selected ? selected.name : doc.querySelector('#panelTitle').textContent)
      + ' — GKPS Klender';
    return doc;
  }
  function chunkFor(url) {
    var target = route(url);
    if (!target) return Promise.resolve(null);
    if (target.kind === 'bible' || target.kind === 'service')
      return Promise.resolve('/offline/chunk/' + target.kind + '/' + target.id + '/');
    if (target.kind !== 'song') return Promise.resolve(null);
    return library.list('songs').then(function (books) {
      var book = books.find(function (item) {
        return item.songs.some(function (song) { return song.id === target.id; });
      });
      return book ? '/offline/chunk/songs/' + book.id + '/' : null;
    });
  }
  function render(url, replacement) {
    var target = route(url);
    if (!target || !window.caches) return Promise.resolve(null);
    return Promise.all([loadShell(), library.list('bible'), library.list('songs'),
                        library.list('service')]).then(function (values) {
      var doc = values[0];
      if (!doc) return null;
      if (replacement) {
        var slot = replacement.kind === 'bible' ? 1 : replacement.kind === 'songs' ? 2 : 3;
        values[slot] = values[slot].map(function (item) {
          return item.id === replacement.id ? replacement : item;
        });
      }
      if (target.kind === 'list' || target.kind === 'book')
        return listPage(doc, target, values[1], values[2], values[3]);
      if (target.kind === 'home') return homePage(doc, values[1]);
      if (target.kind === 'search') return searchPage(doc, target, values[1], values[2], values[3]);
      if (target.kind === 'bible') {
        var book = values[1].find(function (item) { return item.id === target.id; });
        return book ? biblePage(doc, target, book, values[1]) : null;
      }
      if (target.kind === 'song') {
        var songBook = values[2].find(function (item) {
          return item.songs.some(function (song) { return song.id === target.id; });
        });
        var song = songBook && songBook.songs.find(function (item) { return item.id === target.id; });
        return song ? songPage(doc, song, songBook, values[2]) : null;
      }
      var service = values[3].find(function (item) { return item.id === target.id; });
      return service ? servicePage(doc, service, values[3], target) : null;
    });
  }
  window.GKPSOfflineRender = {render: render, route: route, chunkFor: chunkFor};
})();
