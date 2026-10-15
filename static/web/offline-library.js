/* Spec 092: one atomic, shared, complete public-library generation. */
(function () {
  'use strict';
  var DB_NAME = 'gkps-public-library';
  var DB_VERSION = 1;
  var channel;
  try { channel = new BroadcastChannel('gkps-public-library'); } catch (error) { channel = null; }
  var listeners = [];
  var inFlight = null;
  var queuedSync = null;
  var lastError = null;

  function changed() {
    listeners.forEach(function (listener) { listener(); });
    document.dispatchEvent(new Event('offline:changed'));
  }
  if (channel) channel.addEventListener('message', changed);

  function open() {
    return new Promise(function (resolve, reject) {
      if (!window.indexedDB) { reject(new Error('Browser storage unavailable')); return; }
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains('chunks')) db.createObjectStore('chunks');
        if (!db.objectStoreNames.contains('meta')) db.createObjectStore('meta');
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error); };
    });
  }

  function read(store, key) {
    return open().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, 'readonly');
        var request = tx.objectStore(store).get(key);
        request.onsuccess = function () { resolve(request.result || null); };
        request.onerror = function () { reject(request.error); };
        tx.oncomplete = function () { db.close(); };
        tx.onerror = function () { db.close(); };
      });
    });
  }

  function storedKeys() {
    return open().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction('chunks', 'readonly');
        var request = tx.objectStore('chunks').getAllKeys();
        request.onsuccess = function () { resolve(new Set(request.result)); };
        request.onerror = function () { reject(request.error); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function commit(chunks, removed, manifest) {
    return open().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(['chunks', 'meta'], 'readwrite');
        var content = tx.objectStore('chunks');
        var meta = tx.objectStore('meta');
        var now = Date.now();
        removed.forEach(function (key) { content.delete(key); });
        chunks.forEach(function (chunk) { content.put(chunk, chunk.key); });
        meta.put({schema: 1, keys: manifest.chunks.map(function (row) { return row.key; }),
          revisions: Object.fromEntries(manifest.chunks.map(function (row) {
            return [row.key, row.revision];
          })), syncedAt: now, checkedAt: now}, 'generation');
        meta.put({checkedAt: now, error: null}, 'sync-state');
        tx.oncomplete = function () { db.close(); resolve(); };
        tx.onerror = function () { db.close(); reject(tx.error); };
        tx.onabort = function () { db.close(); reject(tx.error); };
      });
    });
  }

  function recordCheck() {
    return open().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction('meta', 'readwrite');
        var store = tx.objectStore('meta');
        var request = store.get('sync-state');
        request.onsuccess = function () {
          var state = request.result || {};
          state.checkedAt = Date.now();
          store.put(state, 'sync-state');
        };
        tx.oncomplete = function () { db.close(); resolve(); };
        tx.onerror = function () { db.close(); reject(tx.error); };
        tx.onabort = function () { db.close(); reject(tx.error); };
      });
    });
  }

  function markChecked() {
    return open().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction('meta', 'readwrite');
        var store = tx.objectStore('meta');
        var checkedAt = Date.now();
        var request = store.get('generation');
        request.onsuccess = function () {
          if (request.result) {
            request.result.checkedAt = checkedAt;
            store.put(request.result, 'generation');
          }
        };
        var statusRequest = store.get('sync-state');
        statusRequest.onsuccess = function () {
          var state = statusRequest.result || {};
          state.checkedAt = checkedAt;
          state.error = null;
          store.put(state, 'sync-state');
        };
        tx.oncomplete = function () { db.close(); resolve(); };
        tx.onerror = function () { db.close(); reject(tx.error); };
        tx.onabort = function () { db.close(); reject(tx.error); };
      });
    });
  }

  function recordFailure(error) {
    return open().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction('meta', 'readwrite');
        var store = tx.objectStore('meta');
        var request = store.get('sync-state');
        request.onsuccess = function () {
          var state = request.result || {};
          state.error = String(error && error.message || error || 'Library sync failed');
          store.put(state, 'sync-state');
        };
        tx.oncomplete = function () { db.close(); resolve(); };
        tx.onerror = function () { db.close(); reject(tx.error); };
        tx.onabort = function () { db.close(); reject(tx.error); };
      });
    });
  }

  function fetchJSON(url) {
    return fetch(url, {cache: 'no-store', credentials: 'same-origin'}).then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status + ': ' + url);
      return response.json();
    });
  }

  function performSync() {
    return Promise.all([read('meta', 'generation'), storedKeys(), fetchJSON('/offline/manifest/')])
      .then(function (pair) {
        var old = pair[0];
        var present = pair[1];
        var manifest = pair[2];
        if (manifest.schema !== 1 || !Array.isArray(manifest.chunks)) {
          throw new Error('Unsupported library manifest');
        }
        var oldRevisions = old && old.revisions || {};
        var wanted = manifest.chunks.filter(function (row) {
          return oldRevisions[row.key] !== row.revision || !present.has(row.key);
        });
        var nextKeys = new Set(manifest.chunks.map(function (row) { return row.key; }));
        var removed = old ? old.keys.filter(function (key) { return !nextKeys.has(key); }) : [];
        return recordCheck().then(function () {
          if (!wanted.length && !removed.length && old) return markChecked();
          /* Keep only four chunk responses in flight, including on first visit. No
             IndexedDB writes happen until all revisions have been verified. */
          var cursor = 0;
          var results = [];
          function worker() {
            if (cursor >= wanted.length) return Promise.resolve();
            var row = wanted[cursor++];
            return fetchJSON(row.url).then(function (payload) {
              if (payload.schema !== 1 || payload.revision !== row.revision
                  || !payload.data || row.key !== payload.data.kind + ':' + payload.data.id) {
                throw new Error('Library changed during sync: ' + row.key);
              }
              results.push({key: row.key, revision: row.revision, data: payload.data});
              return worker();
            });
          }
          return Promise.all(Array.from({length: Math.min(4, wanted.length)}, worker))
            .then(function () { return commit(results, removed, manifest); });
        });
      });
  }

  function sync() {
    if (inFlight) {
      /* A caller during sync can be reacting to a save that happened after the
         current manifest was read. Queue one fresh pass so that save is not lost. */
      if (!queuedSync) {
        var current = inFlight;
        queuedSync = Promise.resolve(current).then(function () {}, function () {})
          .then(function () {
            queuedSync = null;
            return sync();
          });
      }
      return queuedSync;
    }
    changed();
    var run = function () { return performSync(); };
    var task = navigator.locks && navigator.locks.request
      ? navigator.locks.request('gkps-public-library-sync', run) : run();
    inFlight = Promise.resolve(task).then(function (value) {
      lastError = null;
      if (channel) channel.postMessage({type: 'committed'});
      return value;
    }, function (error) {
      lastError = error;
      return recordFailure(error).catch(function () {}).then(function () { throw error; });
    }).finally(function () {
      inFlight = null;
      changed();
    });
    return inFlight;
  }

  function get(kind, id) {
    return read('chunks', kind + ':' + id).then(function (record) {
      return record && record.data || null;
    });
  }

  function list(kind) {
    return read('meta', 'generation').then(function (generation) {
      if (!generation || !generation.keys) return [];
      return Promise.all(generation.keys.filter(function (key) {
        return key.indexOf(kind + ':') === 0;
      }).map(function (key) {
        return read('chunks', key).then(function (record) { return record && record.data; });
      }));
    }).then(function (items) { return items.filter(Boolean); });
  }

  function shellReady() {
    if (!window.caches) return Promise.resolve(false);
    var required = ['/home/', '/offline/projector-shell/', '/static/assets/gkps.png',
      '/static/styles/design/tokens.css', '/static/styles/design/components.css',
      '/static/styles/design/projector.css', '/static/styles/design/offline.css',
      '/static/web/offline-library.js', '/static/web/offline-status.js',
      '/static/web/offline-render.js', '/static/web/reading.js',
      '/static/web/projector.js', '/static/web/projector-library.js',
      '/static/web/display.js', '/static/web/focus.js', '/static/web/editors.js',
      '/static/web/date-picker.js', '/static/web/entries.js', '/static/web/reorder.js',
      '/static/web/preview.js'];
    return Promise.all(required.map(function (url) {
      return caches.match(url).then(Boolean);
    })).then(function (checks) { return checks.every(Boolean); });
  }

  function status() {
    return Promise.all([read('meta', 'generation').catch(function () { return null; }),
                        read('meta', 'sync-state').catch(function () { return null; }),
                        shellReady().catch(function () { return false; }),
                        storedKeys().catch(function () { return new Set(); })])
      .then(function (values) {
        var generation = values[0];
        var syncState = values[1];
        return {ready: !!(generation && generation.keys && values[2]
                          && generation.keys.every(function (key) { return values[3].has(key); })),
                generation: generation, shellsReady: values[2],
                lastCheckedAt: syncState && syncState.checkedAt || generation && generation.checkedAt,
                syncing: !!inFlight, error: lastError || syncState && syncState.error,
                offline: !navigator.onLine};
      });
  }

  function subscribe(listener) {
    listeners.push(listener);
    return function () { listeners = listeners.filter(function (item) { return item !== listener; }); };
  }

  function install() {
    if (!('serviceWorker' in navigator)) return Promise.resolve();
    return navigator.serviceWorker.register('/service-worker.js', {scope: '/'})
      .then(function () { return navigator.serviceWorker.ready; })
      .then(function () { changed(); });
  }

  window.GKPSOffline = {get: get, list: list, sync: sync, status: status, subscribe: subscribe,
                        install: install};
  window.addEventListener('online', function () { sync().catch(function () {}); });
  window.addEventListener('offline', changed);
  install().then(function () { return sync(); }).catch(function () { changed(); });
})();
