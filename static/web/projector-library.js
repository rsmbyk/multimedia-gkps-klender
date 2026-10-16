/* Spec 092: projector Go To reads only the committed browser library. */
(function () {
  'use strict';
  var books = [], songbooks = [], songs = [];
  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/\s+/g, ' ').trim().toLowerCase();
  }
  function load() {
    if (!window.GKPSOffline) return Promise.resolve();
    return Promise.all([GKPSOffline.list('bible'), GKPSOffline.list('songs')])
      .then(function (values) {
        books = values[0];
        songbooks = values[1];
        songs = songbooks.flatMap(function (book) {
          return book.songs.map(function (song) { return {book: book, song: song}; });
        });
        document.dispatchEvent(new Event('projector-library:ready'));
      });
  }
  function firstVerse(book, chapter) {
    var translation = book.translations.find(function (item) {
      return item.version.toUpperCase() === 'TB';
    }) || book.translations[0];
    var rows = translation ? translation.verses.filter(function (verse) {
      return verse.chapter === chapter;
    }) : [];
    return rows.length ? Math.min.apply(null, rows.map(function (verse) { return verse.verse; })) : null;
  }
  function bookAliases(book) {
    return [book.name].concat(book.translations.flatMap(function (item) {
      return [item.name, item.abbreviation || ''];
    }));
  }
  function passageLabel(book, chapter, verse) {
    var translation = book.translations.find(function (item) {
      return item.version.toUpperCase() === 'TB';
    }) || book.translations[0];
    return (translation ? translation.name : book.name) + ' ' + chapter
      + (verse == null ? '' : ':' + verse);
  }
  function songLabel(book, song) {
    if (!book.is_hymn_book) return song.title + ' · ' + book.name;
    return book.short_name + ' ' + song.number + (song.sub_number || '').toUpperCase()
      + (song.title ? ' ' + song.title : '');
  }
  function lookup(raw) {
    var phrase = normalize(raw);
    if (!phrase) return [];
    var ref = phrase.match(/^(.+?)\s+(\d{1,3})(?::(\d{1,3}))?([a-z])?$/);
    if (ref) {
      var namedBook = books.find(function (book) {
        return bookAliases(book).some(function (alias) { return normalize(alias) === ref[1].replace(/\.$/, ''); });
      });
      if (namedBook) {
        var chapterPrefix = ref[2].replace(/^0+/, '') || '0';
        var chapters = new Set();
        namedBook.translations.forEach(function (translation) {
          translation.verses.forEach(function (row) { chapters.add(row.chapter); });
        });
        return Array.from(chapters).sort(function (a, b) { return a - b; })
          .filter(function (chapter) { return String(chapter).startsWith(chapterPrefix); })
          .map(function (chapter) {
            var verse = ref[3] ? Number(ref[3]) : firstVerse(namedBook, chapter);
            if (verse == null) return null;
            if (ref[3] && !namedBook.translations.some(function (translation) {
              return translation.verses.some(function (row) {
                return row.chapter === chapter && row.verse === verse;
              });
            })) return null;
            return {kind: 'passage', label: passageLabel(namedBook, chapter, ref[3] ? verse : null),
              target: {book_id: namedBook.id, chapter: chapter, verse: verse}};
          }).filter(Boolean);
      }
      var songbook = songbooks.find(function (book) {
        return [book.name, book.short_name].some(function (name) { return normalize(name) === ref[1]; });
      });
      if (songbook && !ref[3]) {
        return songbook.songs.filter(function (song) {
          return song.number != null && (String(song.number) + normalize(song.sub_number))
            .startsWith(ref[2] + (ref[4] || ''));
        }).map(function (song) {
          return {kind: 'song', label: songLabel(songbook, song), target: {song_id: song.id}};
        });
      }
    }
    var numeric = /^\d+$/.test(phrase);
    var numericQuery = numeric ? phrase.replace(/^0+(?=\d)/, '') : phrase;
    var hits = songs.map(function (entry) {
      var title = normalize(entry.song.title);
      var number = String(entry.song.number == null ? '' : entry.song.number);
      var score = numeric ? (number === numericQuery ? 3 : number.startsWith(numericQuery) ? 2
        : number.includes(numericQuery) ? 1 : 0)
        : title === phrase ? 200 : title.startsWith(phrase) ? 120 : title.includes(phrase) ? 95 : 0;
      return {entry: entry, score: score};
    }).filter(function (row) { return row.score; });
    if (!hits.length) return [];
    if (numeric) {
      hits.sort(function (a, b) {
        return b.score - a.score
          || Number(a.entry.song.number) - Number(b.entry.song.number)
          || normalize(a.entry.book.short_name || a.entry.book.name)
            .localeCompare(normalize(b.entry.book.short_name || b.entry.book.name))
          || normalize(a.entry.song.sub_number).localeCompare(normalize(b.entry.song.sub_number))
          || normalize(a.entry.song.title).localeCompare(normalize(b.entry.song.title))
          || a.entry.song.id - b.entry.song.id;
      });
      return hits.map(function (row) {
        return {kind: 'song', label: songLabel(row.entry.book, row.entry.song),
          target: {song_id: row.entry.song.id}};
      });
    }
    var best = Math.max.apply(null, hits.map(function (row) { return row.score; }));
    return hits.filter(function (row) { return row.score === best; }).slice(0, 12)
      .map(function (row) {
        return {kind: 'song', label: songLabel(row.entry.book, row.entry.song),
          target: {song_id: row.entry.song.id}};
      });
  }
  function linePairs(text) {
    var screens = [], pair = [];
    String(text || '').split('\n').forEach(function (raw) {
      var line = raw.trim();
      if (!line) {
        if (pair.length) { screens.push(pair); pair = []; }
        return;
      }
      pair.push({text: line, voice: ''});
      if (pair.length === 2) { screens.push(pair); pair = []; }
    });
    if (pair.length) screens.push(pair);
    return screens;
  }
  function songDetour(id) {
    var entry = songs.find(function (item) { return item.song.id === id; });
    if (!entry) return null;
    var screens = [], baits = [];
    entry.song.verses.forEach(function (verse) {
      var start = screens.length;
      var pairs = linePairs(verse.lyric);
      pairs.forEach(function (lines, index) {
        screens.push({blank: false, header: '', lines: lines, bait: verse.number,
          split: index + 1, split_total: pairs.length});
      });
      screens.push({blank: true, header: '', lines: [], bait: verse.number, bait_rest: true});
      baits.push({number: verse.number, start: start, end: screens.length - 1});
    });
    return {kind: 'song', label: songLabel(entry.book, entry.song), screens: screens,
      baits: baits, index: 0};
  }
  function passageDetour(bookId, chapter, verse) {
    var book = books.find(function (item) { return item.id === bookId; });
    if (!book) return null;
    var variants = {};
    book.translations.forEach(function (translation) {
      var code = translation.version.toUpperCase();
      if (code !== 'TB' && code !== 'SIM') return;
      var row = translation.verses.find(function (item) {
        return item.chapter === chapter && item.verse === verse;
      });
      if (!row) return;
      var reference = translation.name + ' ' + chapter + ':' + verse;
      variants[code] = {header: reference + (row.title ? '\n' + row.title : ''),
        line: row.text.trim()};
    });
    var selected = variants.TB ? 'TB' : Object.keys(variants)[0];
    if (!selected) return null;
    return {kind: 'passage', book_id: bookId, chapter: chapter, verse: verse,
      translation: selected, label: passageLabel(book, chapter, verse), translations: variants};
  }
  function detour(row) {
    if (row.kind === 'song') return songDetour(Number(row.target.song_id));
    return passageDetour(Number(row.target.book_id), Number(row.target.chapter),
      Number(row.target.verse) || firstVerse(books.find(function (book) {
        return book.id === Number(row.target.book_id);
      }), Number(row.target.chapter)));
  }
  function movePassage(current, action, level) {
    var candidates = books.filter(function (book) { return book.translations.some(function (tr) {
      return tr.verses.length;
    }); });
    var bookIndex = candidates.findIndex(function (book) { return book.id === current.book_id; });
    if (bookIndex < 0) return current;
    var book = candidates[bookIndex];
    if (level === 'ctrl') {
      if (action === 'first') book = candidates[0];
      if (action === 'last') book = candidates[candidates.length - 1];
      if (action === 'next') book = candidates[Math.min(bookIndex + 1, candidates.length - 1)];
      if (action === 'previous') book = candidates[Math.max(bookIndex - 1, 0)];
      return passageDetour(book.id, 1, firstVerse(book, 1));
    }
    var preferred = book.translations.find(function (item) { return item.version.toUpperCase() === 'TB'; })
      || book.translations[0];
    var positions = preferred.verses.map(function (row) { return [row.chapter, row.verse]; });
    if (level === 'shift') {
      var chapters = Array.from(new Set(positions.map(function (pair) { return pair[0]; })));
      var chapterIndex = chapters.indexOf(current.chapter);
      if (action === 'first') chapterIndex = 0;
      if (action === 'last') chapterIndex = chapters.length - 1;
      if (action === 'next') chapterIndex = Math.min(chapterIndex + 1, chapters.length - 1);
      if (action === 'previous') chapterIndex = Math.max(chapterIndex - 1, 0);
      var chapter = chapters[chapterIndex];
      return passageDetour(book.id, chapter, firstVerse(book, chapter));
    }
    var index = positions.findIndex(function (pair) {
      return pair[0] === current.chapter && pair[1] === current.verse;
    });
    if (index < 0) return current;
    if (action === 'first' || action === 'last') {
      var chapterPositions = positions.map(function (pair, i) { return pair[0] === current.chapter ? i : -1; })
        .filter(function (i) { return i >= 0; });
      index = chapterPositions[action === 'first' ? 0 : chapterPositions.length - 1];
    }
    if (action === 'next') index = Math.min(index + 1, positions.length - 1);
    if (action === 'previous') index = Math.max(index - 1, 0);
    return passageDetour(book.id, positions[index][0], positions[index][1]);
  }
  window.GKPSProjectorLibrary = {load: load, lookup: lookup, detour: detour,
    movePassage: movePassage};
  if (window.GKPSOffline) {
    load();
    document.addEventListener('offline:changed', load);
  }
})();
