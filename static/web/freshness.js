/* Spec 258: poll versions, invalidate a stale page, reconcile sidebars in place. */
(function () {
  var INTERVAL = Number(window.GKPS_FRESHNESS_INTERVAL || 10000);
  var read = document.getElementById('read');
  var badge = document.getElementById('freshnessBadge');
  var inFlight = {};
  var baselines = {};

  function getJSON(url) {
    return fetch(url, {credentials: 'same-origin', cache: 'no-store'})
      .then(function (response) { return response.ok ? response.json() : null; })
      .catch(function () { return null; });
  }

  function once(name, work) {
    if (inFlight[name]) return;
    inFlight[name] = true;
    Promise.resolve(work()).then(function () { inFlight[name] = false; },
                                 function () { inFlight[name] = false; });
  }

  function visible() { return document.visibilityState !== 'hidden'; }

  function invalidate() {
    if (document.documentElement.dataset.pageStale === 'true') return;
    document.documentElement.dataset.pageStale = 'true';
    document.querySelectorAll('dialog[open]').forEach(function (dialog) { dialog.close(); });
    read.querySelectorAll('button').forEach(function (button) { button.disabled = true; });
    if (badge) badge.hidden = false;
  }

  document.addEventListener('shell:page', function (event) {
    if (event.detail && event.detail.kind === 'refresh') {
      delete document.documentElement.dataset.pageStale;
      if (badge) badge.hidden = true;
    }
  });

  if (badge) {
    badge.querySelector('[data-freshness-reload]').addEventListener('click', function () {
      if (window.gkpsNavigate) {
        window.gkpsNavigate(window.location.pathname + window.location.search,
                            {kind: 'refresh'});
      }
    });
  }

  function pollPage() {
    var baseline = read ? Number(read.dataset.pageVersion) : 0;
    if (!read || !baseline || document.documentElement.dataset.pageStale === 'true') return;
    var kind = read.dataset.pageKind === 'tatib' ? 'service' : read.dataset.pageKind;
    var id = read.dataset.pageId;
    if (!kind || !id) return;
    once('page', function () {
      return getJSON('/freshness/page/?kind=' + encodeURIComponent(kind)
                     + '&id=' + encodeURIComponent(id)).then(function (data) {
        if (data && data.version !== baseline) invalidate();
      });
    });
  }

  function rowKey(li) {
    var link = li.querySelector('a[href]');
    return link ? link.getAttribute('href') : '';
  }

  function reconcile(container, fresh) {
    if (!container || !fresh) return;
    var scroll = container.scrollTop;
    var filter = container.querySelector('input[type="search"]');
    var filterValue = filter ? filter.value : null;
    var liveRows = Array.prototype.slice.call(container.querySelectorAll('li'))
      .filter(function (li) { return rowKey(li); });
    var freshRows = Array.prototype.slice.call(fresh.querySelectorAll('li'))
      .filter(function (li) { return rowKey(li); });
    var freshByKey = {};
    freshRows.forEach(function (li) { freshByKey[rowKey(li)] = li; });
    liveRows.forEach(function (li) {
      var match = freshByKey[rowKey(li)];
      if (!match) { li.remove(); return; }
      if (li.outerHTML === match.outerHTML) return;
      li.replaceWith(match.cloneNode(true));
    });
    freshRows.forEach(function (li) {
      var key = rowKey(li);
      if (!container.querySelector('li a[href="' + key + '"]')) {
        var clone = li.cloneNode(true);
        clone.classList.add('freshness-row-enter');
        var parent = container.querySelector('ul') || container;
        parent.appendChild(clone);
      }
    });
    container.scrollTop = scroll;
    if (filter && filterValue !== null) filter.value = filterValue;
  }

  function watchList(name, endpoint, selector) {
    var container = document.querySelector(selector);
    if (!container) return;
    once('baseline-' + name, function () {
      return getJSON(endpoint).then(function (data) {
        if (data) baselines[name] = data.fingerprint;
      });
    });
    setInterval(function () {
      if (!visible() || baselines[name] === undefined) return;
      once('list-' + name, function () {
        return getJSON(endpoint).then(function (data) {
          if (!data || data.fingerprint === baselines[name]) return;
          baselines[name] = data.fingerprint;
          return fetch(window.location.href, {credentials: 'same-origin', cache: 'no-store'})
            .then(function (response) { return response.text(); })
            .then(function (html) {
              var fresh = new DOMParser().parseFromString(html, 'text/html');
              reconcile(container, fresh.querySelector(selector));
            });
        });
      });
    }, INTERVAL);
  }

  if (read && read.dataset.pageVersion) {
    setInterval(function () { if (visible()) pollPage(); }, INTERVAL);
  }

  var section = document.documentElement.dataset.section;
  if (section === 'tatib') {
    var mode = new URLSearchParams(window.location.search).get('mode') === 'template'
      ? 'template' : 'service';
    watchList('services', '/freshness/services/?mode=' + mode, '#panelBody');
  } else if (section === 'kidung') {
    watchList('songbooks', '/freshness/songbooks/', '#panelBody');
    var book = document.getElementById('chBody').dataset.bookId;
    if (book) watchList('songs', '/freshness/songs/?book=' + encodeURIComponent(book), '#chBody');
  }
})();
