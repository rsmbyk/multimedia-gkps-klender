/* Per-computer library view: service references come from Django, bytes from the loopback companion. */
(function () {
  'use strict';
  var page = document.getElementById('mediaLibrary');
  if (!page) return;
  var endpoint = 'http://127.0.0.1:63174/v1';
  var familyNames = { image: 'Image', audio: 'Audio', video: 'Video', pdf: 'PDF', slides: 'PowerPoint' };
  var files = [], uses = null, token = '', retention = '30', connected = false;
  var types = new Set(), unusedOnly = false, sort = 'date-desc', pendingRemove = null;
  var $ = function (id) { return document.getElementById(id); };
  var fmtSize = function (bytes) { return bytes < 1000000 ? Math.round(bytes / 1000) + ' KB' : (bytes / 1000000).toFixed(1) + ' MB'; };
  var date = function (value) { return new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(value)); };
  function request(path, options) {
    return fetch(endpoint + path, Object.assign({ mode: 'cors', cache: 'no-store' }, options || {})).then(function (response) {
      return response.json().then(function (data) { if (!response.ok) throw new Error(data.error || 'Local library unavailable'); return data; });
    });
  }
  function write(path, method, body) {
    return request(path, { method: method, headers: { 'Content-Type': 'application/json', 'X-GKPS-Media-Token': token }, body: body === undefined ? undefined : JSON.stringify(body) });
  }
  function node(tag, className, content) {
    var el = document.createElement(tag); if (className) el.className = className;
    if (content !== undefined) el.textContent = content; return el;
  }
  function setStatus(status) {
    connected = !!status;
    $('mediaSettingsButton').disabled = !connected;
    $('mediaStatusDot').classList.toggle('is-connected', connected);
    $('mediaStatusPopup').classList.toggle('is-unavailable', !connected);
    $('mediaConnection').textContent = connected ? 'Connected' : 'Unavailable';
    document.querySelectorAll('[data-media-connected]').forEach(function (el) { el.hidden = !connected; });
    if (connected) {
      token = status.write_token; retention = status.retention;
      $('mediaCount').textContent = String(files.length);
      $('mediaTotalSize').textContent = fmtSize(files.reduce(function (sum, file) { return sum + file.size; }, 0));
    }
  }
  function unusedLabel(file) {
    if (file.delete_at) {
      var days = Math.max(1, Math.ceil((new Date(file.delete_at) - new Date()) / 86400000));
      return days === 1 ? 'Unused · Deletes tomorrow' : 'Unused · Deletes in ' + days + ' days';
    }
    return 'Unused · Kept on this computer';
  }
  function row(file) {
    var el = node('div', 'media-library__file' + (uses && !(uses[file.sha256] || []).length ? ' is-unused' : ''));
    var icon = node('div', 'media-library__file-icon'); icon.innerHTML = window.gkpsMediaIcon ? window.gkpsMediaIcon(file.family) : ''; el.appendChild(icon);
    var main = node('div', 'media-library__file-main');
    main.appendChild(node('div', 'media-library__filename', file.name));
    main.appendChild(node('div', 'media-library__meta', (familyNames[file.family] || 'File') + ' · ' + date(file.uploaded_at) + ' · ' + fmtSize(file.size)));
    var refs = uses && uses[file.sha256] || [];
    if (refs.length) {
      var links = node('div', 'media-library__uses');
      refs.forEach(function (ref) {
        var line = node('div'); var a = node('a', '', (ref.date ? date(ref.date + 'T12:00:00') + ' · ' : '') + ref.service); a.href = ref.url; line.appendChild(a);
        if (ref.title) line.appendChild(node('span', '', ' · ' + ref.title)); links.appendChild(line);
      }); main.appendChild(links);
    } else if (uses) main.appendChild(node('div', 'media-library__unused', unusedLabel(file)));
    else main.appendChild(node('div', 'media-library__unused', 'Service uses unavailable'));
    el.appendChild(main);
    var remove = node('button', 'media-library__remove'); remove.type = 'button';
    remove.setAttribute('aria-label', 'Remove ' + file.name); remove.title = 'Remove file';
    remove.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M10 4h4m-8 3 1 14h10l1-14M10 11v6m4-6v6"/></svg>';
    remove.addEventListener('click', function () { pendingRemove = file; $('mediaRemoveCopy').textContent = 'Remove “' + file.name + '” from this computer? Tata Ibadah entries that use it will remain.'; openDialog($('mediaRemoveDialog')); });
    el.appendChild(remove); return el;
  }
  function render() {
    var list = $('mediaFileList'); list.replaceChildren();
    var shown = files.filter(function (file) { return (!types.size || types.has(file.family)) && (!unusedOnly || uses && !(uses[file.sha256] || []).length); });
    shown.sort(function (a, b) { return sort.startsWith('size') ? (sort.endsWith('desc') ? b.size - a.size : a.size - b.size) : (sort.endsWith('desc') ? b.uploaded_at.localeCompare(a.uploaded_at) : a.uploaded_at.localeCompare(b.uploaded_at)); });
    $('mediaResultCount').textContent = shown.length + ' of ' + files.length + ' files shown';
    $('mediaEmpty').hidden = !!shown.length;
    $('mediaEmpty').textContent = !connected ? 'Local library unavailable on this computer.' : unusedOnly && !uses ? 'Service uses unavailable.' : files.length ? 'No files match these filters.' : 'No files on this computer yet.';
    var group = null;
    shown.forEach(function (file) {
      if (sort.startsWith('date')) {
        var label = date(file.uploaded_at);
        if (label !== group) { group = label; list.appendChild(node('h2', 'media-library__group', label)); }
      }
      list.appendChild(row(file));
    });
    if (connected) setStatus({ write_token: token, retention: retention });
  }
  function openDialog(dialog) { dialog.showModal(); }
  function closeDialog(dialog) {
    if (!dialog.open) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { dialog.close(); return; }
    dialog.classList.add('closing'); setTimeout(function () { dialog.close(); dialog.classList.remove('closing'); }, 150);
  }
  document.querySelectorAll('.media-library__dialog').forEach(function (dialog) {
    dialog.addEventListener('click', function (event) { if (event.target === dialog) closeDialog(dialog); });
    dialog.addEventListener('cancel', function (event) { event.preventDefault(); closeDialog(dialog); });
    dialog.querySelectorAll('[data-media-close]').forEach(function (button) { button.addEventListener('click', function () { closeDialog(dialog); }); });
  });
  function hideStatus() {
    var popup = $('mediaStatusPopup');
    if (popup.hidden || popup.classList.contains('closing')) return;
    $('mediaStatusButton').setAttribute('aria-expanded', 'false');
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { popup.hidden = true; return; }
    popup.classList.add('closing');
    setTimeout(function () { popup.hidden = true; popup.classList.remove('closing'); }, 150);
  }
  $('mediaStatusButton').addEventListener('click', function () {
    var popup = $('mediaStatusPopup');
    if (popup.hidden) { popup.classList.remove('closing'); popup.hidden = false; this.setAttribute('aria-expanded', 'true'); }
    else hideStatus();
  });
  document.addEventListener('click', function (event) { if (!$('mediaLibraryActions').contains(event.target)) hideStatus(); if (!$('mediaSortButton').parentElement.contains(event.target)) { $('mediaSortMenu').hidden = true; $('mediaSortButton').setAttribute('aria-expanded', 'false'); } });
  document.addEventListener('keydown', function (event) { if (event.key === 'Escape') { hideStatus(); $('mediaSortMenu').hidden = true; $('mediaSortButton').setAttribute('aria-expanded', 'false'); } });
  $('mediaSettingsButton').addEventListener('click', function () { document.querySelector('input[name="retention"][value="' + retention + '"]').checked = true; openDialog($('mediaSettingsDialog')); });
  $('mediaSettingsDialog').querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault(); var value = this.querySelector('input[name="retention"]:checked').value;
    write('/settings', 'POST', { retention: value }).then(function (result) { retention = result.retention; closeDialog($('mediaSettingsDialog')); return refresh(); }).catch(function (error) { window.alert(error.message); });
  });
  $('mediaConfirmRemove').addEventListener('click', function () { if (!pendingRemove) return; write('/files/' + pendingRemove.sha256, 'DELETE').then(function () { pendingRemove = null; closeDialog($('mediaRemoveDialog')); return refresh(); }).catch(function (error) { window.alert(error.message); }); });
  page.querySelectorAll('[data-media-type]').forEach(function (button) { button.addEventListener('click', function () { var type = button.dataset.mediaType; if (types.has(type)) types.delete(type); else types.add(type); button.setAttribute('aria-pressed', String(types.has(type))); render(); }); });
  $('mediaUnusedFilter').addEventListener('click', function () { unusedOnly = !unusedOnly; this.setAttribute('aria-pressed', String(unusedOnly)); render(); });
  $('mediaSortButton').addEventListener('click', function () { $('mediaSortMenu').hidden = !$('mediaSortMenu').hidden; this.setAttribute('aria-expanded', String(!$('mediaSortMenu').hidden)); });
  page.querySelectorAll('[data-media-sort]').forEach(function (button) { button.addEventListener('click', function () { sort = button.dataset.mediaSort; $('mediaSortLabel').textContent = button.textContent; $('mediaSortButton').setAttribute('aria-label', 'Sort files: ' + button.textContent); page.querySelectorAll('[data-media-sort]').forEach(function (option) { option.setAttribute('aria-checked', String(option === button)); }); $('mediaSortMenu').hidden = true; $('mediaSortButton').setAttribute('aria-expanded', 'false'); render(); }); });
  function refresh() {
    return Promise.all([request('/status'), request('/files')]).then(function (results) {
      files = results[1].files || []; uses = null; setStatus(results[0]); render();
      return fetch(page.dataset.referencesUrl, { credentials: 'same-origin' }).then(function (response) {
        if (!response.ok) throw new Error('Cannot load service references');
        return response.json();
      }).then(function (references) {
        uses = references.uses || {};
        return write('/references', 'POST', { hashes: Object.keys(uses) }).then(function (synced) {
          files = synced.files || []; render();
        });
      }).catch(function () { uses = null; render(); });
    }).catch(function () { files = []; uses = null; setStatus(null); render(); });
  }
  refresh();
})();
