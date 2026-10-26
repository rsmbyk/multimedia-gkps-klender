/* Spec 136: the projector's Go To reads a page-memory index and fetches its content.
 *
 * The page keeps no library. `load()` fetches one index of what the lookup matches on —
 * book names, editions, chapter and verse counts, songbooks and song titles — and holds
 * it in memory for the life of the page. A query is answered here, with no request; a
 * chosen result fetches its chapter (both editions) or its song.
 */
(function () {
  'use strict';
  var books = [], songbooks = [], songs = [];
  var ready = false;
  var loading = null;
  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/\s+/g, ' ').trim().toLowerCase();
  }

  /* ---------- the index ---------------------------------------------------- */
  function expandEdition(edition) {
    /* The index sends one verse count per chapter; the lookup expects the verse rows
       themselves, so they are rebuilt here — chapter 1 first, verses 1..count. */
    var verses = [];
    (edition.verses || []).forEach(function (pair) {
      for (var number = 1; number <= pair[1]; number += 1) {
        verses.push({chapter: pair[0], verse: number});
      }
    });
    return {version: edition.v, name: edition.name, abbreviation: edition.abbr || '',
            verses: verses};
  }
  function shape(payload) {
    books = (payload.books || []).map(function (book) {
      return {id: book.id, name: book.name,
              translations: (book.editions || []).map(expandEdition)};
    });
    songbooks = (payload.songbooks || []).map(function (book) {
      return {id: book.id, name: book.name, short_name: book.short_name || '',
              is_hymn_book: !!book.is_hymn_book, songs: []};
    });
    var byId = {};
    songbooks.forEach(function (book) { byId[book.id] = book; });
    songs = [];
    (payload.songs || []).forEach(function (song) {
      /* [id, songbook id, number, sub-number, title] — see the server's byte-budget note. */
      var shaped = {id: song[0],
                    number: song[2] === '' || song[2] == null ? null : song[2],
                    sub_number: song[3] || '', title: song[4] || '', verses: []};
      var book = byId[song[1]];
      if (book) book.songs.push(shaped);
      songs.push({book: book, song: shaped});
    });
  }
  function load() {
    if (loading) return loading;
    loading = fetch('/projector/goto/index/', {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function (payload) {
        if (!payload || payload.schema !== 1) throw new Error('Unexpected index');
        shape(payload);
        ready = true;
        document.dispatchEvent(new Event('projector-library:ready'));
        return true;
      })
      .catch(function (error) {
        loading = null;                    // a later open or Update may retry
        throw error;
      });
    return loading;
  }
  function isReady() { return ready; }
  function refresh() {
    /* The page's Update re-reads everything; the index is fetched again rather than
       reused, so a song added while the service runs is findable. */
    loading = null;
    return load();
  }

  /* ---------- the lookup (unchanged from spec 092) ------------------------- */
  function translationFor(book, edition) {
    if (!book) return null;
    return book.translations.find(function (item) {
      return item.version.toUpperCase() === edition;
    }) || null;
  }
  function defaultTranslation(book) {
    return translationFor(book, 'TB') || (book && book.translations[0]) || null;
  }
  function firstVerse(book, chapter, edition) {
    var translation = edition ? translationFor(book, edition) : defaultTranslation(book);
    var rows = translation ? translation.verses.filter(function (verse) {
      return verse.chapter === chapter;
    }) : [];
    return rows.length ? Math.min.apply(null, rows.map(function (verse) { return verse.verse; })) : null;
  }
  function passageLabel(book, chapter, verse, translation) {
    translation = translation || defaultTranslation(book);
    return (translation ? translation.name : book.name) + ' ' + chapter
      + (verse == null ? '' : ':' + verse);
  }
  function codeMatches(rawCode) {
    var matches = [], seen = {}, recognized = false;
    books.forEach(function (book) {
      if (normalize(book.name) === rawCode) {
        recognized = true;
        var tb = translationFor(book, 'TB');
        if (tb) add(book, tb, 'TB');
      }
      book.translations.forEach(function (translation) {
        if (!translation.abbreviation || normalize(translation.abbreviation) !== rawCode) return;
        var edition = translation.version.toUpperCase();
        if (edition !== 'TB' && edition !== 'SIM') return;
        recognized = true;
        add(book, translation, edition);
      });
    });
    function add(book, translation, edition) {
      var key = book.id + ':' + edition;
      if (seen[key]) return;
      seen[key] = true;
      matches.push({book: book, translation: translation, edition: edition});
    }
    return {recognized: recognized, matches: matches};
  }
  function nameMatches(rawName) {
    var matches = [];
    books.forEach(function (book) {
      book.translations.forEach(function (translation) {
        var edition = translation.version.toUpperCase();
        if ((edition === 'TB' || edition === 'SIM')
          && normalize(translation.name) === rawName) {
          matches.push({book: book, translation: translation, edition: edition});
        }
      });
    });
    return matches;
  }
  function passageMatches(matches, chapterPrefix, requestedVerse) {
    var chapters = new Set();
    matches.forEach(function (match) {
      match.translation.verses.forEach(function (row) { chapters.add(row.chapter); });
    });
    var results = [];
    Array.from(chapters).sort(function (a, b) { return a - b; })
      .filter(function (chapter) { return String(chapter).startsWith(chapterPrefix); })
      .forEach(function (chapter) {
        matches.forEach(function (match) {
          var verse = requestedVerse == null
            ? firstVerse(match.book, chapter, match.edition) : requestedVerse;
          if (verse == null || !match.translation.verses.some(function (row) {
            return row.chapter === chapter && row.verse === verse;
          })) return;
          results.push({kind: 'passage',
            label: passageLabel(match.book, chapter, requestedVerse == null ? null : verse,
              match.translation),
            target: {book_id: match.book.id, chapter: chapter, verse: verse,
              edition: match.edition}});
        });
      });
    var labelGroups = {};
    results.forEach(function (result) {
      var key = normalize(result.label);
      labelGroups[key] = labelGroups[key] || [];
      labelGroups[key].push(result);
    });
    Object.keys(labelGroups).forEach(function (key) {
      var group = labelGroups[key];
      if (new Set(group.map(function (result) { return result.target.edition; })).size < 2) return;
      group.forEach(function (result) { result.editionSuffix = result.target.edition; });
    });
    return results;
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
      var bookCode = ref[1].replace(/\.$/, '');
      var codeResult = codeMatches(bookCode);
      var chapterPrefix = ref[2].replace(/^0+/, '') || '0';
      if (codeResult.recognized) {
        return passageMatches(codeResult.matches, chapterPrefix,
          ref[3] ? Number(ref[3]) : null);
      }
      var namedMatches = nameMatches(bookCode);
      if (namedMatches.length) {
        return passageMatches(namedMatches, chapterPrefix,
          ref[3] ? Number(ref[3]) : null);
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

  /* ---------- the fetched content ----------------------------------------- */
  function fetchJson(url) {
    return fetch(url, {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      });
  }
  function variantsAt(editions, chapter, verse) {
    var variants = {};
    Object.keys(editions).forEach(function (code) {
      var edition = editions[code];
      var row = edition.verses.find(function (item) { return item.n === verse; });
      if (!row) return;
      var reference = edition.name + ' ' + chapter + ':' + verse;
      variants[code] = {header: reference + (row.title ? '\n' + row.title : ''),
                        line: (row.text || '').trim()};
    });
    return variants;
  }
  function chooseEdition(variants, requested) {
    if (requested && !variants[requested]) return '';
    return requested || (variants.TB ? 'TB' : Object.keys(variants)[0] || '');
  }
  function labelAt(editions, chapter, verse) {
    var edition = editions.TB || editions[Object.keys(editions)[0]];
    return edition.name + ' ' + chapter + (verse == null ? '' : ':' + verse);
  }
  function passageDetour(payload, verse, requestedEdition) {
    var editions = payload.editions || {};
    var preferred = editions.TB || editions[Object.keys(editions)[0]];
    if (!preferred || !preferred.verses.length) return null;
    var wanted = verse == null ? preferred.verses[0].n : verse;
    var variants = variantsAt(editions, payload.chapter, wanted);
    var selected = chooseEdition(variants, requestedEdition);
    if (!selected) return null;
    return {kind: 'passage', book_id: payload.book_id, chapter: payload.chapter,
            verse: wanted, translation: selected, editions: editions,
            label: labelAt(editions, payload.chapter, wanted), translations: variants};
  }
  function chapterUrl(bookId, chapter) {
    return '/projector/goto/chapter/' + encodeURIComponent(bookId) + '/'
      + encodeURIComponent(chapter) + '/';
  }
  function detour(row) {
    if (!row || !row.target) return Promise.reject(new Error('No result'));
    if (row.kind === 'song') {
      return fetchJson('/projector/goto/song/' + encodeURIComponent(row.target.song_id) + '/')
        .then(function (payload) {
          return {kind: 'song', label: payload.label, screens: payload.screens || [],
                  baits: payload.baits || [], index: 0};
        });
    }
    var bookId = Number(row.target.book_id);
    var chapter = Number(row.target.chapter);
    var verse = row.target.verse == null ? null : Number(row.target.verse);
    return fetchJson(chapterUrl(bookId, chapter)).then(function (payload) {
      var made = passageDetour(payload, verse, row.target.edition);
      if (!made && window.console && console.error) {
        console.error('empty passage detour', verse, row.target.edition, JSON.stringify(payload).slice(0, 400));
      }
      return made;
    });
  }
  function fetchChapter(bookId, chapter, verse, edition) {
    return fetchJson(chapterUrl(bookId, chapter)).then(function (payload) {
      return passageDetour(payload, verse, edition);
    });
  }

  /* ---------- stepping ----------------------------------------------------- */
  function positionsFor(book) {
    var preferred = book.translations.find(function (translation) {
      return translation.version.toUpperCase() === 'TB';
    }) || book.translations.find(function (translation) {
      return translation.verses.length;
    });
    return preferred ? preferred.verses : [];
  }
  function movePassage(current, action, level) {
    var candidates = books.filter(function (book) {
      return book.translations.some(function (translation) { return translation.verses.length; });
    });
    var at = candidates.findIndex(function (book) { return book.id === current.book_id; });
    if (at < 0) return null;
    if (level === 'ctrl' && action) {
      var targetBook = candidates[at];
      if (action === 'first') targetBook = candidates[0];
      if (action === 'last') targetBook = candidates[candidates.length - 1];
      if (action === 'next') targetBook = candidates[Math.min(at + 1, candidates.length - 1)];
      if (action === 'previous') targetBook = candidates[Math.max(at - 1, 0)];
      var firstPositions = positionsFor(targetBook);
      if (!firstPositions.length) return null;
      return {request: {book_id: targetBook.id, chapter: firstPositions[0].chapter,
                        verse: firstPositions[0].verse}};
    }
    var positions = positionsFor(candidates[at]);
    if (!positions.length) return null;
    if (level === 'shift' && action) {
      var chapters = Array.from(new Set(positions.map(function (pair) { return pair.chapter; })));
      var chapterAt = chapters.indexOf(current.chapter);
      if (chapterAt < 0) chapterAt = 0;
      if (action === 'first') chapterAt = 0;
      if (action === 'last') chapterAt = chapters.length - 1;
      if (action === 'next') chapterAt = Math.min(chapterAt + 1, chapters.length - 1);
      if (action === 'previous') chapterAt = Math.max(chapterAt - 1, 0);
      var chapter = chapters[chapterAt];
      var chapterPositions = positions.filter(function (pair) { return pair.chapter === chapter; });
      if (!chapterPositions.length) return null;
      return stepTo(current, current.book_id, chapter, chapterPositions[0].verse);
    }
    var index = positions.findIndex(function (pair) {
      return pair.chapter === current.chapter && pair.verse === current.verse;
    });
    if (index < 0) {
      index = positions.findIndex(function (pair) { return pair.chapter === current.chapter; });
      if (index < 0) return null;
    }
    if (action === 'first' || action === 'last') {
      var inChapter = positions.map(function (pair, position) {
        return pair.chapter === current.chapter ? position : -1;
      }).filter(function (position) { return position >= 0; });
      if (inChapter.length) index = inChapter[action === 'first' ? 0 : inChapter.length - 1];
    }
    if (action === 'next') index = Math.min(index + 1, positions.length - 1);
    if (action === 'previous') index = Math.max(index - 1, 0);
    return stepTo(current, current.book_id, positions[index].chapter, positions[index].verse);
  }
  function stepTo(current, bookId, chapter, verse) {
    if (bookId === current.book_id && chapter === current.chapter) {
      var variants = variantsAt(current.editions, chapter, verse);
      var selected = chooseEdition(variants, current.translation);
      if (!selected) return null;
      return {detour: {kind: 'passage', book_id: bookId, chapter: chapter, verse: verse,
                       translation: selected, editions: current.editions,
                       label: labelAt(current.editions, chapter, verse),
                       translations: variants}};
    }
    return {request: {book_id: bookId, chapter: chapter, verse: verse,
                      edition: current.translation}};
  }

  /* Spec 136: a browser that still holds the retired library drops it here — the service
     worker with its shell cache, and the IndexedDB store nothing reads any more. */
  function retireOfflineLibrary() {
    if (navigator.serviceWorker && navigator.serviceWorker.getRegistrations) {
      navigator.serviceWorker.getRegistrations().then(function (registrations) {
        registrations.forEach(function (registration) { registration.unregister(); });
      }).catch(function () { /* nothing to retire */ });
    }
    if (window.caches && caches.keys) {
      caches.keys().then(function (keys) {
        keys.filter(function (key) { return key.indexOf('gkps-public-shell-') === 0; })
          .forEach(function (key) { caches.delete(key); });
      }).catch(function () { /* no cache storage */ });
    }
    if (window.indexedDB && indexedDB.deleteDatabase) {
      try { indexedDB.deleteDatabase('gkps-public-library'); } catch (error) { /* none */ }
    }
  }
  retireOfflineLibrary();

  window.GKPSProjectorLibrary = {load: load, refresh: refresh, ready: isReady, lookup: lookup,
    detour: detour, fetchChapter: fetchChapter, movePassage: movePassage};
  load().catch(function () { /* the panel reports it when opened */ });
})();
