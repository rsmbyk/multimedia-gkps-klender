/* Local availability is a fact about this computer, not the saved service entry. */
(function () {
  'use strict';
  var paths = {
    image: '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9" r="1.5"/><path d="m4 17 5-5 3.5 3.5 2.5-2.5 5 5"/>',
    audio: '<path d="M3.6 10.2v3.6M7.2 7.2v9.6M10.8 4.4v15.2M14.4 7.2v9.6M18 10.2v3.6"/>',
    video: '<rect x="3" y="5" width="18" height="15" rx="2"/><path d="M3 10h18M7 5l3 5m4-5 3 5"/><path d="m10 12 5 3-5 3z"/>',
    pdf: '<path d="M6 2h8l5 5v15H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM14 2v5h5M8 16h8M8 19h6"/>',
    slides: '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M12 18v3m-4 0h8M7 9h10M7 12h7"/>',
    missing: '<path d="M6 2h8l5 5v8M14 2v5h5M4 5v15a2 2 0 0 0 2 2h7"/><circle cx="18" cy="18" r="4"/><path d="M18 16v2m0 2h.01"/>'
  };
  function icon(kind) { return '<svg viewBox="0 0 24 24" aria-hidden="true">' + (paths[kind] || paths.missing) + '</svg>'; }
  window.gkpsMediaIcon = icon;
  function renderRow(row, state) {
    var symbol = row.querySelector('[data-media-icon]');
    var subtitle = row.querySelector('.read__sub');
    if (!symbol || !subtitle) return;
    row.classList.toggle('is-missing', state === 'missing');
    row.classList.toggle('is-unavailable', state === 'unavailable');
    symbol.innerHTML = icon(state === 'missing' ? 'missing' : row.dataset.mediaFamily);
    var status = subtitle.querySelector('.entry__media-availability');
    if (status) status.remove();
    if (state === 'unavailable') {
      status = document.createElement('span');
      status.className = 'entry__media-availability';
      status.textContent = '· Local library unavailable';
      subtitle.appendChild(status);
    }
    symbol.setAttribute('aria-label', state === 'missing' ? 'File missing on this computer' : '');
    symbol.setAttribute('aria-hidden', state === 'missing' ? 'false' : 'true');
  }
  /* Every chip names its own family, so a placeholder that never gets a availability
     pass -- the muted rows inside the Use template dialog -- still draws its glyph. */
  function paintAll() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-media-icon]'), function (symbol) {
      if (symbol.querySelector('svg')) return;
      symbol.innerHTML = icon(symbol.dataset.mediaIcon || 'image');
    });
  }
  window.gkpsMediaPaint = paintAll;

  function refresh() {
    paintAll();
    var rows = Array.prototype.slice.call(document.querySelectorAll('.tatib__item--media'));
    if (!rows.length) return;
    rows.forEach(function (row) { renderRow(row, 'unavailable'); });
    fetch('http://127.0.0.1:63174/v1/files', { mode: 'cors', cache: 'no-store' })
      .then(function (response) { if (!response.ok) throw new Error('Local library unavailable'); return response.json(); })
      .then(function (result) {
        var hashes = new Set((result.files || []).map(function (file) { return file.sha256; }));
        rows.forEach(function (row) { if (row.isConnected) renderRow(row, hashes.has(row.dataset.mediaHash) ? 'available' : 'missing'); });
      }).catch(function () { /* Unknown availability stays distinct from missing. */ });
  }
  document.addEventListener('shell:page', refresh);
  document.addEventListener('editor:saved', function () { setTimeout(refresh, 150); });
  refresh();
})();
