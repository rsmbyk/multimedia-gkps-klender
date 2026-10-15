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
  function bookLink(book, selected, kind) {
    var name = kind === 'bible' ? (book.translations.find(function (item) {
      return item.version.toUpperCase() === 'TB';
    }) || book.translations[0] || {}).name || book.name : book.name;
    var short = kind === 'bible' ? book.name : book.short_name;
    var href = kind === 'bible' ? '/bible/' + book.id + '/' : kind === 'songs'
      ? '/songs/book/' + book.id + '/' : '/tatib/' + book.id + '/';
    return '<li><a class="book" href="' + href + '" data-name="' + escape(kind === 'bible' ? name : book.id)
      + '" data-sim="' + escape(short) + '" aria-label="' + escape(name)
      + '"' + (selected ? ' aria-current="true"' : '') + '><span class="book__n">'
      + escape(name) + '</span><span class="book__s">' + escape(short || '') + '</span></a></li>';
  }
  function common(doc, section, title, name, number, body, panel, children, target) {
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
    doc.querySelector('#chList').innerHTML = children;
    doc.querySelector('#chTitle').textContent = section === 'alkitab' ? 'Chapters — ' + name
      : section === 'kidung' ? 'Song list' : 'Service contents';
    doc.querySelector('.ch__search').hidden = section === 'alkitab';
    doc.querySelector('#songSort').hidden = section !== 'kidung';
    var read = doc.querySelector('#read');
    read.dataset.kind = section === 'alkitab' ? 'bible' : section === 'kidung' ? 'song' : 'tatib';
    doc.querySelector('#readName').textContent = name;
    doc.querySelector('#readNo').textContent = number || '';
    doc.querySelector('#readEyebrow').textContent = section === 'alkitab' ? 'Alkitab'
      : section === 'kidung' ? 'Kidung' : 'Tata Ibadah';
    doc.querySelector('#readEyebrow').hidden = false;
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
      return bookLink(item, item.id === book.id, 'bible');
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
    var label = book.is_hymn_book ? (book.short_name + ' ' + song.number
      + (song.sub_number || '').toUpperCase()) : song.title;
    var panel = '<section class="group"><ul>' + books.map(function (item) {
      return bookLink(item, item.id === book.id, 'songs');
    }).join('') + '</ul></section>';
    var children = book.songs.map(function (item, index) {
      var number = item.number == null ? '' : item.number + (item.sub_number || '').toUpperCase();
      return '<li><a class="songrow" href="/songs/' + item.id + '/" data-i="' + item.id
        + '" data-t="' + escape(item.title.toLowerCase()) + '" data-o="' + index + '"'
        + (item.id === song.id ? ' aria-current="true"' : '') + '><span class="songrow__c">'
        + escape(number) + '</span><span class="songrow__t">' + escape(item.title)
        + '</span></a></li>';
    }).join('');
    var body = song.verses.map(function (verse, index) {
      return '<p class="v"><span class="v__n">' + (index + 1) + '</span><span>'
        + escape(verse.lyric).replace(/\n/g, '<br>') + '</span></p>';
    }).join('');
    return common(doc, 'kidung', label, song.title || label, book.is_hymn_book ? label : '',
      body, panel, children);
  }
  function servicePage(doc, service, services) {
    var panel = '<section class="group"><ul>' + services.map(function (item) {
      return bookLink(item, item.id === service.id, 'service');
    }).join('') + '</ul></section>';
    var children = (service.toc || []).map(function (item) {
      if (item.eos) return '<li class="toc__eos" data-i="' + escape(item.anchor)
        + '" aria-hidden="true"><span class="toc__eosline"></span></li>';
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
      return '<li><a class="songrow' + (item.titled ? '' : ' songrow--cont')
        + '" href="#ti-' + escape(item.anchor) + '" data-i="' + escape(item.anchor)
        + '" data-num="' + item.n + '" data-txt="' + escape((item.txt || '').toLowerCase())
        + '"><span class="songrow__c">' + item.n + '</span>' + label + '</a></li>';
    }).join('');
    var body = (service.items || []).map(function (item) {
      if (item.eos) return '<div class="tatib__eos" id="ti-' + escape(item.anchor)
        + '" data-anchor="' + escape(item.anchor) + '">'
        + (item.note ? '<span class="tatib__note">' + escape(item.note) + '</span>' : '') + '</div>';
      var title = item.title ? '<h2 class="read__sec">'
        + (item.jump ? '<a class="entry__jump" href="' + escape(item.jump)
          + '" data-entry-jump>' + escape(item.title) + '</a>'
          : '<span>' + escape(item.title) + '</span>') + '</h2>' : '';
      var paras = (item.paras || []).map(function (para) {
        return '<p class="tatib__tx' + (para.voice ? ' is-' + escape(para.voice) : '')
          + '">' + (para.mark ? '<span class="tatib__sp">' + escape(para.mark)
          + '</span> ' : '') + escape(para.text) + '</p>';
      }).join('');
      return '<section class="tatib__item" id="ti-' + escape(item.anchor)
        + '" data-anchor="' + escape(item.anchor) + '"'
        + (item.clipped ? ' data-clipped="true"' : '') + '>' + title
        + (item.deleted_target ? '<p class="entry__deleted-warning" role="status">'
          + 'This song, songbook, or an included verse was deleted.</p>' : '')
        + (item.subtitle ? '<p class="read__sub">' + escape(item.subtitle) + '</p>' : '')
        + paras + '</section>';
    }).join('');
    common(doc, 'tatib', service.name, service.name, '', body, panel, children);
    var group = doc.createElement('div');
    group.className = 'read__project';
    group.dataset.projectGroup = '';
    group.dataset.displayChannel = 'gkps-service-display';
    group.innerHTML = '<button type="button" class="read__project-btn" data-project-open'
      + ' data-projector-url="/obs/service/' + service.id + '/" data-project-service="'
      + service.id + '" data-label-project="Project" data-label-stop="Stop projecting"'
      + ' aria-label="Project" title="Project"><span data-project-label>Project</span></button>';
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
      + bible.map(function (item) { return bookLink(item, false, 'bible'); }).join('')
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
    doc.querySelector('#panelBody').innerHTML = '<section class="group"><ul>'
      + collection.map(function (item) { return bookLink(item, selected && item.id === selected.id,
        section === 'alkitab' ? 'bible' : section === 'kidung' ? 'songs' : 'service'); }).join('')
      + '</ul></section>';
    doc.querySelector('#chTitle').textContent = section === 'alkitab' ? 'Chapters'
      : section === 'kidung' ? 'Song list' : 'Service contents';
    doc.querySelector('.ch__search').hidden = section === 'alkitab';
    doc.querySelector('#songSort').hidden = section !== 'kidung';
    var children = '';
    if (selected && section === 'alkitab') {
      var title = (selected.translations[0] || {}).name || selected.name;
      doc.querySelector('#chTitle').textContent = 'Chapters — ' + title;
      children = Array.from({length: selected.chapters}, function (_, index) {
        var n = index + 1;
        return '<li><a class="ch-num" href="/bible/' + selected.id + '/' + n
          + '/" data-n="' + n + '" aria-label="' + escape(title)
          + ' chapter ' + n + '">' + n + '</a></li>';
      }).join('');
    } else if (selected && section === 'kidung') {
      children = selected.songs.map(function (song, index) {
        var number = song.number == null ? '' : song.number + (song.sub_number || '').toUpperCase();
        return '<li><a class="songrow" href="/songs/' + song.id + '/" data-i="' + song.id
          + '" data-t="' + escape(song.title.toLowerCase()) + '" data-o="' + index
          + '"><span class="songrow__c">' + escape(number)
          + '</span><span class="songrow__t">' + escape(song.title) + '</span></a></li>';
      }).join('');
    }
    doc.querySelector('#chList').innerHTML = children;
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
      return service ? servicePage(doc, service, values[3]) : null;
    });
  }
  window.GKPSOfflineRender = {render: render, route: route, chunkFor: chunkFor};
})();
