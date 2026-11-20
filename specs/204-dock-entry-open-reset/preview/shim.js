/* Preview shim (spec 204) — loaded BEFORE the product's own scripts.
 *
 * Two jobs, neither of which touches the dock's logic:
 *   1. pick the behaviour under review from the query string: `?behaviour=today` runs
 *      develop's rule, anything else runs the drafted reset. The drafted line lives in
 *      assets/obs-dock.js, gated on this flag, exactly where the slice puts it.
 *   2. answer `/projector?service=N` from the captured islands, in the same
 *      `json_script` shape the projector template serves, so the dock's own
 *      fetch → DOMParser → JSON.parse path runs unchanged.
 *
 * Every other URL goes to the real fetch.
 */
(function () {
  'use strict';

  var params = new URLSearchParams(window.location.search);
  window.__openReset = params.get('behaviour') !== 'today';
  window.__behaviour = window.__openReset ? 'drafted' : 'today';

  var island = document.getElementById('previewPayloads');
  var payloads = island ? JSON.parse(island.textContent) : {};
  var realFetch = window.fetch ? window.fetch.bind(window) : null;

  /* A re-read of UNCHANGED data takes the dock's own shortcut and never rebuilds the
     list, so a preview that only re-served the same payload would prove nothing about
     the repaint. The rail's "Re-read now" bumps this revision and the served payload
     carries it in the first entry's label — a saved change, as the product sees one. */
  window.__previewRevision = 0;

  function served(id) {
    var data = payloads[id];
    if (!data) return null;
    var rev = window.__previewRevision || 0;
    if (!rev || !data.entries.length) return data;
    var entries = data.entries.map(function (entry, i) {
      if (i !== 0) return entry;
      var copy = {};
      for (var key in entry) copy[key] = entry[key];
      copy.label = String(entry.label || '') + ' · rev' + rev;
      return copy;
    });
    return {entries: entries, screens: data.screens};
  }

  function jsonScript(id, value) {
    return '<script id="' + id + '" type="application/json">' +
      JSON.stringify(value).replace(/</g, '\\u003c') + '<\/script>';
  }

  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    var match = url.match(/\/projector\?service=(\d+)/);
    if (match) {
      var data = served(match[1]);
      if (!data) return Promise.resolve(new Response('', {status: 404}));
      var html = '<!doctype html><html lang="id"><body>' +
        jsonScript('projectorEntryData', data.entries) +
        jsonScript('projectorScreenData', data.screens) +
        '</body></html>';
      return Promise.resolve(new Response(html, {
        status: 200, headers: {'Content-Type': 'text/html; charset=utf-8'}
      }));
    }
    if (realFetch) return realFetch(input, init);
    return Promise.reject(new Error('no fetch available'));
  };
})();
