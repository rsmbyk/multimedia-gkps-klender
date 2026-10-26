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
  function bookLink(book, selected, kind, editorEnabled, edition) {
    var translations = book.translations || [];
    var tb = kind === 'bible' && translations.find(function (item) {
      return item.version.toUpperCase() === 'TB';
    });
    var sim = kind === 'bible' && translations.find(function (item) {
      return item.version.toUpperCase() === 'SIM';
    });
    var tbName = tb ? tb.name : (translations[0] || {}).name || book.name;
    var simName = sim ? sim.name : '';
    var simPrimary = kind === 'bible' && edition === 'sim' && !!simName;
    var otherTranslation = tb && sim ? (simPrimary ? tb : sim) : null;
    var name = kind === 'bible' ? (simPrimary ? simName : tbName) : book.name;
    var otherName = otherTranslation ? otherTranslation.name : '';
    var tbCode = book.name;
    var simCode = sim ? sim.abbreviation || book.name : book.name;
    var miniCode = simPrimary ? simCode : tbCode;
    var short = kind === 'bible' ? otherName : kind === 'service'
      ? book.date_display || book.short_name : book.short_name;
    var href = kind === 'bible' ? '/bible/' + book.id + '/' : kind === 'songs'
      ? '/songs/book/' + book.id + '/' : '/tatib/' + book.id + '/';
    var editor = editorEnabled ? kind === 'service' ? 'tatib'
      : kind === 'songs' && !book.is_hymn_book ? 'songbook' : '' : '';
    return '<li><a class="book" href="' + href + '" data-name="' + escape(kind === 'bible' ? tbName : book.id)
      + '" data-sim="' + escape(kind === 'bible' ? simName : kind === 'service' ? book.id : short || '') + '"'
      + (kind === 'bible' ? ' data-tb-code="' + escape(tbCode) + '" data-sim-code="'
        + escape(simCode) + '" data-has-tb="' + !!tb + '" data-has-sim="' + !!sim
        + '" data-tip="' + escape(name + (short ? ' — ' + short : '')) + '"' : '')
      + ' aria-label="' + escape(name)
      + (short ? ' (' + escape(short) + ')' : '')
      + (kind === 'service' && book.today ? ' — today' : '')
      + '"' + (selected ? ' aria-current="true"' : '') + '><span class="book__n">'
      + escape(name) + '</span>'
      + (kind === 'service' && book.today ? '<span class="book__today">Today</span>' : '')
      + (kind === 'bible' ? '<span class="book__a">'
        + escape(miniCode) + '</span>' : '') + (kind === 'bible'
        ? (short ? '<span class="book__s">' + escape(short) + '</span>' : '')
        : '<span class="book__s">' + escape(short || '') + '</span>') + '</a>'
      + (editor ? '<button class="row-edit" type="button" data-editor-open="' + editor
        + '" data-editor-id="' + book.id + '" aria-label="Edit ' + escape(name)
        + '"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7"'
        + ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        + '<path d="M12.5 4.5l3 3-8 8H4.5v-3z"/></svg></button>' : '') + '</li>';
  }
  function songbookNameKey(name) {
    return normalized(name);
  }
  function bySongbookName(a, b) {
    var ka = songbookNameKey(a.name), kb = songbookNameKey(b.name);
    if (ka < kb) return -1;
    if (ka > kb) return 1;
    return a.name < b.name ? -1 : a.name > b.name ? 1 : 0;
  }
  function songbookGroups(books) {
    var hymns = books.filter(function (book) { return book.is_hymn_book; });
    var ordinary = books.filter(function (book) { return !book.is_hymn_book; });
    hymns.sort(function (a, b) {
      return b.songs.length - a.songs.length || bySongbookName(a, b);
    });
    ordinary.sort(bySongbookName);
    return [hymns, ordinary].filter(function (group) { return group.length; });
  }
  function songbooksPanel(books, selectedId, editor) {
    return songbookGroups(books).map(function (group) {
      return '<section class="group"><ul>' + group.map(function (item) {
        return bookLink(item, item.id === selectedId, 'songs', editor);
      }).join('') + '</ul></section>';
    }).join('');
  }
  function biblePanel(books, selectedId, edition) {
    edition = edition === 'sim' ? 'sim' : 'tb';
    return [
      ['old', 'Perjanjian Lama', 'Padan na Basaia'],
      ['new', 'Perjanjian Baru', 'Padan na Baru']
    ].map(function (group) {
      var rows = books.filter(function (book) { return book.testament === group[0]; });
      if (!rows.length) return '';
      return '<section class="group" data-testament="' + group[0] + '"><h3 class="group__head" data-label-tb="'
        + group[1] + '" data-label-sim="' + group[2] + '">'
        + group[edition === 'sim' ? 2 : 1] + '</h3><ul>' + rows.map(function (book) {
          return bookLink(book, book.id === selectedId, 'bible', false, edition);
        }).join('') + '</ul></section>';
    }).join('');
  }
  function addButtons(serviceId) {
    return ['scripture', 'song', 'text', 'media'].map(function (kind) {
      var names = {scripture: 'Passage', song: 'Song', text: 'Text', media: 'Media'};
      return '<button type="button" class="entry__add-btn" data-entry-open="' + kind
        + '" data-entry-tatib="' + serviceId + '">+ ' + names[kind] + '</button>';
    }).join('');
  }
  function emptyAddButtons(serviceId) {
    var icons = {
      scripture: '<path d="M12 6.6S10.1 4.2 6.4 4.2H3.3v13.6h3.1c3.7 0 5.6 2.4 5.6 2.4s1.9-2.4 5.6-2.4h3.1V4.2h-3.1C13.9 4.2 12 6.6 12 6.6z"/><path d="M12 6.6v13.6"/>',
      song: '<path d="M9 17.4V5.6l10.2-2v11.6"/><circle cx="6.7" cy="17.4" r="2.4"/><circle cx="16.9" cy="15.2" r="2.4"/>',
      text: '<path d="M4.5 6.5h15M4.5 12h15M4.5 17.5h9"/>',
      media: '<rect x="3.2" y="5.2" width="17.6" height="13.6" rx="2.4"/><path d="M10.4 9.2v5.6l4.6-2.8z"/>'
    };
    var names = {scripture: 'Passage', song: 'Song', text: 'Text', media: 'Media'};
    return ['scripture', 'song', 'text', 'media'].map(function (kind) {
      var label = 'Add ' + names[kind];
      return '<button type="button" class="entry__empty-btn" data-entry-open="' + kind
        + '" data-entry-tatib="' + serviceId + '" title="' + label + '">'
        + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        + ' stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
        + ' aria-hidden="true">' + icons[kind] + '</svg>'
        + '<span class="sr">' + label + '</span></button>';
    }).join('');
  }
  function bibleSidebarTitle(book) {
    var translations = (book.translations || []).slice().sort(function (a, b) {
      var aTb = a.version.toUpperCase() === 'TB', bTb = b.version.toUpperCase() === 'TB';
      return aTb === bTb ? a.id - b.id : aTb ? -1 : 1;
    });
    var display = translations.length ? translations[0].name : book.name;
    return 'Chapters — ' + display
      + (translations.length > 1 ? ' (' + translations[1].name + ')' : '');
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
    } else if (preview.kind === 'video') {
      html = (preview.title ? '<p class="preview__ref">' + escape(preview.title) + '</p>' : '')
        + '<div class="preview__video" data-preview-video="' + escape(preview.sha256) + '">'
        + '<div class="preview__video-frame"><video class="preview__video-element" playsinline preload="metadata" hidden></video>'
        + '<button type="button" class="preview__video-overlay-play" data-video-play aria-label="Play video"></button></div>'
        + '<div class="preview__video-controls"><button type="button" class="preview__video-play" data-video-play aria-label="Play video"></button>'
        + '<input class="preview__video-seek" data-video-seek type="range" min="0" max="1" value="0" step="0.1" aria-label="Seek video"></div>'
        + '<div class="preview__video-meta"><span class="preview__video-filename">' + escape(preview.filename)
        + '</span><span><span data-video-elapsed>0:00</span> / <span data-video-total>0:00</span></span></div></div>'
        + '<div class="preview__video-unavailable" role="status" hidden>'
        + '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="7" y="9" width="34" height="29" rx="3"/>'
        + '<path d="m20 17 12 7-12 7zM12 5l24 38"/></svg>'
        + '<span>Video unavailable on this computer</span></div>';
    } else if (preview.kind === 'pdf' || preview.kind === 'slides') {
      var slides = preview.kind === 'slides';
      html = '<p class="preview__ref">' + escape(preview.title) + '</p>'
        + '<div class="preview__pdf" ' + (slides ? 'data-preview-slides' : 'data-preview-pdf') + '="' + escape(preview.sha256) + '">'
        + (slides ? '<div class="preview__pdf-preparing" role="status">Preparing slides…</div>' : '')
        + '<div class="preview__pdf-page"><canvas aria-label="' + (slides ? 'PowerPoint slide' : 'PDF page') + '"></canvas></div>'
        + '<div class="preview__pdf-controls" hidden><button type="button" data-pdf-prev aria-label="Previous ' + (slides ? 'slide' : 'PDF page') + '">←</button>'
        + '<span data-pdf-count aria-live="polite"></span><button type="button" data-pdf-next aria-label="Next ' + (slides ? 'slide' : 'PDF page') + '">→</button></div>'
        + '<div class="preview__pdf-unavailable" role="status" hidden>'
        + '<svg viewBox="0 0 48 48" aria-hidden="true">'
        + (slides ? '<rect x="7" y="7" width="34" height="34" rx="3"/><path d="M13 15h22M13 33h22M17 25l5-5 4 4 5-5M12 5l27 38"/>'
          : '<path d="M11 4h17l9 9v27H11a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3zM28 4v9h9M15 23h15M12 6l27 36"/>') + '</svg>'
        + '<span>' + (slides ? 'PowerPoint' : 'PDF') + ' unavailable on this computer</span></div></div>';
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
  /* The Tata Ibadah list's four age buckets (spec 132): the server's rule, repeated
     here because a saved page is rebuilt in the browser with no server to ask. */
  var TATIB_BUCKETS = [['upcoming', 'Upcoming'], ['last-30-days', 'Last 30 days'],
    ['earlier-this-year', 'Earlier this year'], ['older', 'Older']];
  var TATIB_RECENT_DAYS = 30;
  function jakartaToday() {
    try {
      return new Intl.DateTimeFormat('en-CA', {timeZone: 'Asia/Jakarta',
        year: 'numeric', month: '2-digit', day: '2-digit'}).format(new Date());
    } catch (e) {
      /* An old engine without Intl time zones: the operator's own day is the best
         available answer, and the panel is read in the congregation's time zone. */
      var now = new Date();
      return now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0')
        + '-' + String(now.getDate()).padStart(2, '0');
    }
  }
  function isoDay(value) {
    var match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value || '');
    return match ? match[1] + '-' + match[2] + '-' + match[3] : '';
  }
  function utcDays(iso) {
    return Date.UTC(Number(iso.slice(0, 4)), Number(iso.slice(5, 7)) - 1,
      Number(iso.slice(8, 10))) / 86400000;
  }
  function tatibBucket(iso, todayIso) {
    if (iso >= todayIso) return 'upcoming';
    if (utcDays(todayIso) - utcDays(iso) <= TATIB_RECENT_DAYS) return 'last-30-days';
    if (iso.slice(0, 4) === todayIso.slice(0, 4)) return 'earlier-this-year';
    return 'older';
  }
  function dateParts(value) {
    var match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value || '');
    return match ? {year: Number(match[1]), month: Number(match[2]), day: Number(match[3])} : null;
  }
  function servicePanel(services, selectedId, mode, editor) {
    var filtered = services.filter(function (service) {
      return mode === 'template' ? !service.date : !!service.date;
    });
    var todayIso = jakartaToday();
    var sections = [];
    if (mode === 'template') {
      filtered.sort(function (a, b) {
        return normalized(a.name).replace(/\|/g, '').localeCompare(normalized(b.name).replace(/\|/g, ''));
      });
      sections.push({key: '', label: 'Templates', rows: filtered});
    } else {
      filtered.sort(function (a, b) {
        return String(b.date).localeCompare(String(a.date))
          || String(b.created_at || '').localeCompare(String(a.created_at || ''))
          || b.id - a.id;
      });
      var byKey = {};
      filtered.forEach(function (service) {
        var iso = isoDay(service.date);
        if (!iso) return;
        var key = tatibBucket(iso, todayIso);
        if (!byKey[key]) byKey[key] = [];
        byKey[key].push(service);
      });
      if (byKey.upcoming) {
        /* Today's rows lead, then the future farthest-first: the list is already in
           date-descending order, so a stable partition is the whole rule (spec 132). */
        byKey.upcoming.sort(function (a, b) {
          return (isoDay(a.date) !== todayIso) - (isoDay(b.date) !== todayIso);
        });
      }
      TATIB_BUCKETS.forEach(function (bucket) {
        var rows = byKey[bucket[0]];
        if (rows && rows.length) sections.push({key: bucket[0], label: bucket[1], rows: rows});
      });
    }
    return sections.map(function (section) {
      var rows = section.rows.map(function (service) {
        var date = dateParts(service.date);
        var dateLabel = date ? date.day + ' ' + MONTHS_SHORT[date.month - 1] + ' ' + date.year : '';
        return bookLink(Object.assign({}, service, {date_display: dateLabel,
          today: isoDay(service.date) === todayIso}),
          service.id === selectedId, 'service', editor);
      }).join('');
      var attr = section.key ? ' data-bucket="' + section.key + '"' : '';
      return '<section class="group"' + attr + '><h3 class="group__head">'
        + escape(section.label) + '</h3><ul>' + rows + '</ul></section>';
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
  /* Both sidebar empty states name their own list, so the saved renderer
     re-labels them for the section it is building: the shell it rebuilds from
     is the cached home page, whose blocks are the Bible's (spec 129). */
  var LIST_EMPTY = {
    alkitab: {
      panelTitle: 'No books yet.', panelHint: 'Add a Bible edition to start reading.',
      panelFilter: 'No matching books.',
      chTitle: 'No chapters.', chHint: 'This edition has no text in this book.',
      chFilter: 'No matching chapters.',
      panelGlyph: '<path d="M12 6.6S10.1 4.2 6.4 4.2H3.3v13.6h3.1c3.7 0 5.6 2.4 5.6 2.4s1.9-2.4 5.6-2.4h3.1V4.2h-3.1C13.9 4.2 12 6.6 12 6.6z"/>'
        + '<path d="M12 6.6v13.6"/>',
      chGlyph: ['3.5', '13.5'].map(function (x) {
        return ['3.5', '13.5'].map(function (y) {
          return '<rect x="' + x + '" y="' + y + '" width="7" height="7" rx="1.4"/>';
        }).join('');
      }).join('')
    },
    kidung: {
      panelTitle: 'No songbooks yet.', panelHint: 'Add a songbook to start collecting songs.',
      panelFilter: 'No matching songbooks.',
      chTitle: 'No songs yet.', chHint: 'Add the first song to this songbook.',
      chFilter: 'No matching songs.',
      panelGlyph: '<path d="M9 17.4V5.6l10.2-2v11.6"/><circle cx="6.7" cy="17.4" r="2.4"/>'
        + '<circle cx="16.9" cy="15.2" r="2.4"/>',
      chGlyph: '<path d="M9 17.4V5.6l10.2-2v11.6"/><circle cx="6.7" cy="17.4" r="2.4"/>'
        + '<circle cx="16.9" cy="15.2" r="2.4"/>'
    },
    tatib: {
      panelTitle: 'No Tata Ibadah yet.', panelHint: 'Add the first service to start preparing it.',
      panelFilter: 'No matching Tata Ibadah.',
      chTitle: 'No sections yet.', chHint: 'Add the first item to start preparing the service.',
      chFilter: 'No matching sections.',
      panelGlyph: '<rect x="4.4" y="3.4" width="15.2" height="17.2" rx="1.8"/>'
        + '<path d="M8.6 8.8h6.8M8.6 12.6h6.8M8.6 16.4h4.2"/>',
      chGlyph: '<path d="M4.5 6.5h3.2M4.5 12h3.2M4.5 17.5h3.2"/>'
        + '<path d="M11 6.5h8.5M11 12h8.5M11 17.5h8.5"/>'
    }
  };
  var EMPTY_ICON_OPEN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
    + ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">';

  function labelListEmpty(doc, section) {
    var copy = LIST_EMPTY[section] || LIST_EMPTY.alkitab;
    [['#panelEmpty', 'panelTitle', 'panelHint', 'panelFilter', 'panelGlyph'],
      ['#chEmpty', 'chTitle', 'chHint', 'chFilter', 'chGlyph']].forEach(function (spec) {
      var block = doc.querySelector(spec[0]);
      if (!block) return;
      block.dataset.emptyTitle = copy[spec[1]];
      block.dataset.emptyHint = copy[spec[2]];
      block.dataset.filterTitle = copy[spec[3]];
      var icon = block.querySelector('.listempty__icon[data-when="empty"]');
      if (icon) icon.innerHTML = EMPTY_ICON_OPEN + copy[spec[4]] + '</svg>';
    });
  }

  function paintListEmptyStates(doc) {
    var paint = window.shellListEmpty;
    if (!paint) return;
    var panel = doc.querySelector('#panelEmpty');
    var books = doc.querySelectorAll('#panelBody .book').length;
    if (panel) paint(panel, books > 0, books);
    var chapters = doc.querySelector('#chEmpty');
    var rows = doc.querySelectorAll('#chList .songrow, #chList .ch-num').length;
    if (chapters) paint(chapters, rows > 0, rows);
  }

  function common(doc, section, title, name, number, body, panel, children, target, songListOpen) {
    var root = doc.documentElement;
    root.dataset.section = section;
    root.dataset.nav = 'open';
    root.dataset.ch = 'open';
    root.dataset.read = 'on';
    root.dataset.home = 'reading';
    root.dataset.chMode = section === 'alkitab' ? 'chapter' : 'song';
    doc.title = title + ' — Multimedia GKPS Klender';
    doc.querySelector('#panelTitle').textContent = section === 'alkitab' ? 'Books — Alkitab'
      : section === 'kidung' ? 'Songbooks' : 'Tata Ibadah';
    doc.querySelector('label[for="bookFilter"]').textContent = section === 'alkitab'
      ? 'Filter books' : section === 'kidung' ? 'Filter songbooks' : 'Filter Tata Ibadah';
    doc.querySelector('#bookFilter').placeholder = section === 'alkitab' ? 'Filter books...'
      : section === 'kidung' ? 'Filter songbooks...' : 'Filter Tata Ibadah...';
    doc.querySelector('#panelBody').innerHTML = panel;
    labelListEmpty(doc, section);
    doc.querySelector('#chList').innerHTML = children;
    doc.querySelector('#chTitle').textContent = section === 'alkitab' ? 'Chapters — ' + name
      : section === 'kidung' ? 'Song list' : 'Chapters';
    doc.querySelector('.ch__search').hidden = section === 'alkitab';
    doc.querySelector('label[for="songFilter"]').textContent = section === 'tatib'
      ? 'Filter sections' : 'Filter songs';
    doc.querySelector('#songFilter').placeholder = section === 'tatib'
      ? 'Filter sections...' : 'Filter songs...';
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
    paintListEmptyStates(doc);
    return doc;
  }
  function biblePage(doc, route, book, books) {
    var tb = book.translations.find(function (item) { return item.version.toUpperCase() === 'TB'; });
    var sim = book.translations.find(function (item) { return item.version.toUpperCase() === 'SIM'; });
    var name = (tb || sim || {}).name || book.name;
    var requested = route.url.searchParams.get('ed') === 'sim' ? 'sim' : 'tb';
    function chapterRows(translation) {
      return translation ? translation.verses.filter(function (row) {
        return row.chapter === route.chapter;
      }) : [];
    }
    var tbRows = chapterRows(tb), simRows = chapterRows(sim);
    if (!tbRows.length && !simRows.length) return null;
    var visible = requested;
    if (!({tb: tbRows, sim: simRows})[visible].length) {
      visible = tbRows.length ? 'tb' : 'sim';
    }
    function edition(rows, code, translation) {
      return '<div class="read__ed" data-ed="' + code + '" data-name="'
        + escape(translation ? translation.name : name) + '"'
        + (visible !== code ? ' hidden' : '') + '>' + rows.map(function (row) {
          return (row.title ? '<h2 class="read__sec">' + escape(row.title) + '</h2>' : '')
            + '<p class="v" data-verse="' + row.verse + '"><span class="v__n">'
            + row.verse + '</span><span>' + escape(row.text) + '</span></p>';
        }).join('') + '</div>';
    }
    var body = edition(tbRows, 'tb', tb) + (simRows.length ? edition(simRows, 'sim', sim) : '');
    var panel = biblePanel(books, book.id, requested);
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
    var visibleName = (visible === 'sim' ? sim : tb || sim || {}).name || book.name;
    common(doc, 'alkitab', visibleName + ' ' + route.chapter, visibleName, route.chapter,
      body, panel, chapters, '[data-verse="' + (route.url.searchParams.get('v') || '') + '"]');
    doc.querySelector('#chTitle').textContent = bibleSidebarTitle(book);
    doc.documentElement.dataset.bibleEdition = requested;
    doc.querySelector('#read').setAttribute('lang', visible === 'sim' ? 'sim' : 'id');
    var railLabels = requested === 'sim'
      ? {alkitab: 'Bibel', kidung: 'Doding', tatib: 'Agenda'}
      : {alkitab: 'Alkitab', kidung: 'Kidung', tatib: 'Tata Ibadah'};
    Object.keys(railLabels).forEach(function (section) {
      var button = doc.querySelector('.rail [data-panel="' + section + '"]');
      if (!button) return;
      button.dataset.tip = railLabels[section];
      button.setAttribute('aria-label', railLabels[section]);
    });
    var row = doc.querySelector('.read__row');
    var lang = doc.createElement('div');
    lang.className = 'read__lang';
    lang.setAttribute('role', 'group');
    lang.setAttribute('aria-label', 'Choose reading translation');
    lang.dataset.edition = visible;
    lang.innerHTML = '<span class="read__lang-thumb" aria-hidden="true"></span>'
      + '<a id="langTb" href="?ed=tb" aria-pressed="' + (visible === 'tb') + '">TB</a>'
      + '<a id="langSim" href="?ed=sim" aria-pressed="' + (visible === 'sim')
      + '"' + (!simRows.length ? ' data-empty="true" aria-disabled="true"' : '') + '>SIM</a>';
    row.appendChild(lang);
    return doc;
  }
  function songPage(doc, song, book, books) {
    var citation = book.is_hymn_book ? ((book.short_name || book.name)
      + (song.number != null ? ' ' + song.number + (song.sub_number || '').toUpperCase() : ''))
      : book.name;
    var panel = songbooksPanel(books, book.id, !!doc.querySelector('#editorModal'));
    var editor = !!doc.querySelector('#editorModal') && !book.is_hymn_book;
    var children = book.songs.map(function (item, index) {
      var number = book.is_hymn_book && item.number != null
        ? (book.short_name || '') + ' ' + item.number + (item.sub_number || '').toUpperCase() : '';
      return '<li><a class="songrow" href="/songs/' + item.id + '/" data-i="' + item.id
        + '" data-t="' + escape(item.sort_title || item.title.toLowerCase()) + '" data-o="' + index
        + '" data-m="' + escape(item.modified_key || '')
        + '"' + (number ? ' data-num="' + escape(number) + '"' : '')
        + (item.id === song.id ? ' aria-current="true"' : '') + '>'
        + (number ? '<span class="songrow__c">' + escape(number) + '</span>' : '')
        + '<span class="songrow__t">' + escape(item.title)
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
    /* A hymn book keeps number order, so its page offers no sort control — the same rule the
       server applies (`show_song_sort = not book.is_hymn_book`, spec 011). */
    common(doc, 'kidung', citation, song.title || citation, '',
      body, panel, children, null, !book.is_hymn_book);
    doc.querySelector('#chTitle').textContent = 'Song list — ' + book.name;
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
        : '<span class="songrow__t">' + (item.label_lines || [item.label])
          .map(function (line) { return escape(line || ''); }).join('<br>') + '</span>';
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
      var media = item.kind === 'media';
      return '<section class="tatib__item' + (item.entry ? ' tatib__item--entry' : '')
        + (item.preview || item.entry || item.old_item ? ' tatib__item--acts' : '')
        + (media ? ' tatib__item--media' : '') + '" id="ti-' + escape(item.anchor)
        + '" data-anchor="' + escape(item.anchor) + '"'
        + (item.entry ? ' data-entry-pk="' + item.pk + '"' : item.old_item
          ? ' data-old-item-pk="' + item.pk + '"' : '')
        + (media ? ' data-media-hash="' + escape(item.media_hash)
          + '" data-media-family="' + escape(item.media_family) + '"' : '')
        + (item.clipped ? ' data-clipped="true"' : '') + '>'
        + (media ? '<span class="entry__media-icon" aria-hidden="true" data-media-icon="'
          + escape(item.media_family) + '"></span>' : '') + title
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
      + '<div class="entry__empty-actions">' + emptyAddButtons(service.id)
      + '</div></div>';
    common(doc, 'tatib', service.name, service.name, '', body, panel, children);
    /* Same rule as the server's format_date_long: a dated service leads with its date. */
    var serviceDate = dateParts(service.date);
    doc.querySelector('#readEyebrow').textContent = serviceDate
      ? serviceDate.day + ' ' + MONTHS_LONG[serviceDate.month - 1] + ' ' + serviceDate.year
      : 'Tata Ibadah';
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
      + ' data-projector-url="/projector?service=' + service.id + '" data-project-service="'
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
  var NOTICE_EXCLUSION_ONLY = 'Nothing to search — an exclusion like “-Israel” needs at least one other word.';
  var NOTICE_NO_WORDS = 'Nothing to search — add at least one word.';

  function isWordChar(ch) {
    return /^[\p{L}\p{N}]$/u.test(ch) || /^[\u0300-\u036f]$/.test(ch);
  }

  // Spec 105: symbols separate words, quotes make a phrase, a dash excludes.
  function parseQuery(input) {
    var text = String(input || ''), tokens = [], excluded = false, index = 0;
    while (index < text.length) {
      var ch = text[index];
      if (ch === '"') {
        index += 1;
        var words = [], word = '';
        while (index < text.length && text[index] !== '"') {
          if (isWordChar(text[index])) { word += text[index]; }
          else if (word) { words.push(word); word = ''; }
          index += 1;
        }
        if (word) words.push(word);
        if (index < text.length) index += 1;
        if (words.length) tokens.push({words: words, excluded: excluded, phrase: true});
        excluded = false;
        continue;
      }
      if (ch === '-' && index + 1 < text.length
          && (isWordChar(text[index + 1]) || text[index + 1] === '"')) {
        excluded = true;
        index += 1;
        continue;
      }
      if (isWordChar(ch)) {
        var bare = '';
        while (index < text.length && isWordChar(text[index])) { bare += text[index]; index += 1; }
        tokens.push({words: [bare], excluded: excluded, phrase: false});
        excluded = false;
        continue;
      }
      excluded = false;
      index += 1;
    }
    tokens.forEach(function (token) {
      token.display = token.words.join(' ');
      token.text = normalized(token.display);
    });
    var canonical = tokens.map(function (token) {
      var body = token.phrase ? "'" + token.display + "'" : token.display;
      return token.excluded ? '-' + body : body;
    }).join(' ');
    var notice = '';
    if (!tokens.length) notice = NOTICE_NO_WORDS;
    else if (!tokens.some(function (token) { return !token.excluded; })) {
      notice = NOTICE_EXCLUSION_ONLY;
    }
    return {tokens: tokens, canonical: canonical, notice: notice};
  }

  function occurrences(text, token) {
    var found = [], start = text.indexOf(token.text);
    while (start !== -1) { found.push(start); start = text.indexOf(token.text, start + 1); }
    return found;
  }

  // Longest run of matched tokens that keeps the query's order inside one field.
  function bestOrder(fields, tokens) {
    var best = 0;
    fields.forEach(function (field) {
      var events = [];
      tokens.forEach(function (token, index) {
        occurrences(field, token).forEach(function (position) {
          events.push([position, -index]);
        });
      });
      if (!events.length) return;
      events.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
      var tails = [];
      events.forEach(function (event) {
        var value = -event[1], low = 0, high = tails.length;
        while (low < high) {
          var middle = (low + high) >> 1;
          if (tails[middle] < value) { low = middle + 1; } else { high = middle; }
        }
        if (low === tails.length) { tails.push(value); } else { tails[low] = value; }
      });
      best = Math.max(best, tails.length);
    });
    return best;
  }

  function metrics(title, body, tokens) {
    var fields = [normalized(title), normalized(body)], matched = [];
    for (var index = 0; index < tokens.length; index += 1) {
      var token = tokens[index];
      var hit = fields.some(function (field) { return field.indexOf(token.text) !== -1; });
      if (token.excluded) {
        if (hit) return null;
        continue;
      }
      if (hit) matched.push(token);
    }
    if (!matched.length) return {coverage: 0, order: 0};
    return {coverage: matched.length, order: bestOrder(fields, matched)};
  }

  function anchorExcerpt(body, tokens) {
    var text = String(body || '').replace(/\s+/g, ' ').trim();
    if (!text) return '';
    var folded = normalized(text), token = null;
    for (var index = 0; index < tokens.length; index += 1) {
      if (!tokens[index].excluded && folded.indexOf(tokens[index].text) !== -1) {
        token = tokens[index];
        break;
      }
    }
    var position = token ? folded.indexOf(token.text) : 0;
    var start = Math.max(0, position - 44), end = start + 172;
    return (start ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');
  }
  function searchPage(doc, target, bible, books, services) {
    var query = target.query;
    if (!query) return homePage(doc, bible);
    var parsed = parseQuery(query), tokens = parsed.tokens;
    var include = tokens.filter(function (token) { return !token.excluded; });
    var rows = {bible: [], songs: [], tatib: []};
    function add(kind, title, meta, body, url, fieldTitle) {
      var found = metrics(fieldTitle === undefined ? title : fieldTitle, body, tokens);
      if (!found || !found.coverage) return;
      rows[kind].push({title: title, meta: meta, body: body, url: url,
                       coverage: found.coverage, order: found.order});
    }
    if (include.length) {
      bible.forEach(function (book) {
        var tb = book.translations.find(function (item) { return item.version.toUpperCase() === 'TB'; });
        var preferred = tb || book.translations[0];
        var name = preferred ? preferred.name : book.name;
        book.translations.forEach(function (translation) {
          translation.verses.forEach(function (verse) {
            var label = name + ' ' + verse.chapter + ':' + verse.verse;
            add('bible', label, translation.version + ' · ' + (verse.title || ''),
                verse.text, '/bible/' + book.id + '/' + verse.chapter + '/?v=' + verse.verse,
                verse.title || '');
          });
        });
      });
      books.forEach(function (book) {
        book.songs.forEach(function (song) {
          var reference = song.number == null ? '' : book.short_name + ' ' + song.number
            + (song.sub_number || '').toUpperCase();
          var longRef = song.number == null ? '' : book.name + ' ' + song.number
            + (song.sub_number || '').toUpperCase();
          var lyric = song.verses.map(function (verse) { return verse.lyric; }).join(' ');
          add('songs', song.title, reference + ' ' + longRef + ' ' + book.name,
              lyric, '/songs/' + song.id + '/');
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
    }
    var names = {bible: 'Alkitab', songs: 'Kidung', tatib: 'Tata Ibadah'};
    var html = '';
    ['bible', 'songs', 'tatib'].forEach(function (kind) {
      var group = rows[kind].sort(function (a, b) {
        return b.coverage - a.coverage || b.order - a.order || a.title.localeCompare(b.title);
      });
      if (!group.length) return;
      var amount = Math.max(8, Number(target.url.searchParams.get(kind)) || 8);
      html += '<section class="result-group" data-kind="' + kind + '"><div class="result-group__head">'
        + '<h2 class="result-group__title">' + names[kind] + '</h2><span class="result-group__count">'
        + group.length + (group.length === 1 ? ' result' : ' results') + '</span></div><ul class="result-list">';
      group.slice(0, amount).forEach(function (row) {
        var excerpt = anchorExcerpt(row.body, tokens);
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
    var status = html ? 'Results for “' + escape(parsed.canonical) + '”'
      : parsed.notice ? escape(parsed.notice)
      : 'No results for “' + escape(parsed.canonical) + '”. Try another keyword.';
    doc.querySelector('#searchResults').innerHTML = '<p class="search-results__intro"'
      + ' id="searchStatus" role="status">' + status + '</p>' + html;
    doc.querySelector('#searchResults').hidden = false;
    doc.title = 'Results for “' + parsed.canonical + '” — Multimedia GKPS Klender';
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
    doc.querySelector('#panelBody').innerHTML = biblePanel(bible, null);
    doc.title = 'Multimedia GKPS Klender';
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
    doc.querySelector('#bookFilter').placeholder = section === 'alkitab' ? 'Filter books...'
      : section === 'kidung' ? 'Filter songbooks...' : 'Filter Tata Ibadah...';
    var editor = !!doc.querySelector('#editorModal');
    var mode = target.url.searchParams.get('mode') === 'template' ? 'template' : 'dated';
    var panel = section === 'tatib' ? servicePanel(collection, null, mode, editor)
      : section === 'alkitab' ? biblePanel(collection, selected && selected.id)
      : songbooksPanel(collection, selected && selected.id, editor);
    doc.querySelector('#panelBody').innerHTML = panel;
    labelListEmpty(doc, section);
    doc.querySelector('#chTitle').textContent = section === 'kidung' && selected
      ? 'Song list — ' + selected.name : 'Chapters';
    doc.querySelector('.ch__search').hidden = section === 'alkitab';
    doc.querySelector('label[for="songFilter"]').textContent = section === 'tatib'
      ? 'Filter sections' : 'Filter songs';
    doc.querySelector('#songFilter').placeholder = section === 'tatib'
      ? 'Filter sections...' : 'Filter songs...';
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
      doc.querySelector('#chTitle').textContent = bibleSidebarTitle(selected);
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
        var number = selected.is_hymn_book && song.number != null
          ? (selected.short_name || '') + ' ' + song.number + (song.sub_number || '').toUpperCase() : '';
        return '<li><a class="songrow" href="/songs/' + song.id + '/" data-i="' + song.id
          + '" data-t="' + escape(song.sort_title || song.title.toLowerCase()) + '" data-o="' + index
          + '" data-m="' + escape(song.modified_key || '')
          + '"' + (number ? ' data-num="' + escape(number) + '"' : '') + '>'
          + (number ? '<span class="songrow__c">' + escape(number) + '</span>' : '')
          + '<span class="songrow__t">' + escape(song.title) + '</span></a>'
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
      + ' — Multimedia GKPS Klender';
    paintListEmptyStates(doc);
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
