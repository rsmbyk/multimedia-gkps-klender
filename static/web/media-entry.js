/* Media entry creation: binary bytes go to the loopback companion, metadata to Django. */
(function () {
  'use strict';
  var helper = 'http://127.0.0.1:63174/v1';
  var names = { image: 'Image', audio: 'Audio', video: 'Video', pdf: 'PDF', slides: 'PowerPoint' };
  var error = document.getElementById('mediaErrorDialog');
  var editorDialog = document.getElementById('editorModal');
  if (editorDialog) {
    var nativeClose = editorDialog.close.bind(editorDialog);
    editorDialog.close = function (returnValue) {
      if (!editorDialog.querySelector('form[data-entry-form="media"]') ||
          matchMedia('(prefers-reduced-motion: reduce)').matches) {
        nativeClose(returnValue); return;
      }
      if (editorDialog.classList.contains('media-closing')) return;
      editorDialog.classList.add('media-closing');
      setTimeout(function () { nativeClose(returnValue); editorDialog.classList.remove('media-closing'); }, 150);
    };
    editorDialog.addEventListener('cancel', function (event) {
      if (editorDialog.querySelector('form[data-entry-form="media"]')) {
        event.preventDefault(); editorDialog.close();
      }
    });
  }
  function showError(title, message) {
    if (!error) return;
    error.querySelector('#mediaErrorTitle').textContent = title;
    error.querySelector('#mediaErrorMessage').textContent = message;
    if (!error.open) error.showModal();
  }
  if (error) {
    error.querySelector('#mediaErrorClose').onclick = function () { error.close(); };
    error.addEventListener('click', function (event) { if (event.target === error) error.close(); });
  }
  function csrf() {
    var found = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return found ? decodeURIComponent(found[2]) : '';
  }
  function formatSize(bytes) { return (bytes / 1000000).toFixed(1) + ' MB'; }
  function formatDate(value) {
    var date = new Date(value);
    return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
  }
  async function responseJson(response) {
    var body = await response.json();
    if (!response.ok) throw new Error(body.error || 'The local library could not complete the request.');
    return body;
  }
  async function status() {
    var response = await fetch(helper + '/status', { mode: 'cors', cache: 'no-store' });
    return responseJson(response);
  }
  function wire(scope) {
    var edit = scope.querySelector('[data-media-edit-hash]');
    if (edit) {
      fetch(helper + '/files', { mode: 'cors', cache: 'no-store' })
        .then(responseJson)
        .then(function (result) {
          if (!edit.isConnected) return;
          var found = (result.files || []).some(function (file) { return file.sha256 === edit.dataset.mediaEditHash; });
          edit.querySelector('[data-media-edit-availability]').textContent = found ? 'Available on this computer' : 'File missing on this computer';
          edit.classList.toggle('is-missing', !found);
        }).catch(function () { if (edit.isConnected) edit.querySelector('[data-media-edit-availability]').textContent = 'Local library unavailable'; });
    }
    var form = scope.querySelector('form[data-media-create]');
    if (!form || form.dataset.mediaWired) return;
    form.dataset.mediaWired = 'true';
    var tabs = form.querySelector('.media-entry__tabs');
    var panels = form.querySelectorAll('[data-media-panel]');
    var drop = form.querySelector('[data-media-drop]');
    var input = form.querySelector('[data-media-file]');
    var libraryList = form.querySelector('[data-media-library-list]');
    var save = form.querySelector('.editor__save');
    var selected = { upload: null, library: null };
    var active = 'upload';
    var files = [];

    function sync() {
      var item = selected[active];
      save.disabled = !item;
      form.querySelector('[data-media-prompt]').hidden = !!selected.upload;
      form.querySelector('[data-media-selected]').hidden = !selected.upload;
      if (selected.upload) {
        var uploaded = selected.upload;
        form.querySelector('[data-media-selected-icon]').innerHTML = window.gkpsMediaIcon(uploaded.family);
        form.querySelector('[data-media-selected-name]').textContent = uploaded.chosenName;
        form.querySelector('[data-media-selected-meta]').textContent = names[uploaded.family] + ' · ' + formatSize(uploaded.size);
        form.querySelector('[data-media-existing]').hidden = !uploaded.reused;
        var filename = form.querySelector('[data-media-library-name]');
        filename.hidden = !uploaded.reused;
        filename.textContent = uploaded.reused ? 'Library filename: ' + uploaded.name : '';
        form.querySelector('[data-media-note]').textContent = uploaded.reused
          ? 'This entry will use ' + uploaded.name + '. No second file copy will be made.'
          : "The file will be copied to this computer's Media Library when the entry is saved.";
      }
      Array.prototype.forEach.call(libraryList.querySelectorAll('[data-media-hash]'), function (button) {
        button.setAttribute('aria-selected', selected.library && button.dataset.mediaHash === selected.library.sha256 ? 'true' : 'false');
      });
    }
    function selectTab(tab) {
      active = tab;
      tabs.dataset.mediaTab = tab;
      Array.prototype.forEach.call(tabs.querySelectorAll('[data-media-tab-button]'), function (button) {
        button.setAttribute('aria-selected', button.dataset.mediaTabButton === tab ? 'true' : 'false');
      });
      Array.prototype.forEach.call(panels, function (panel) { panel.hidden = panel.dataset.mediaPanel !== tab; });
      sync();
      if (tab === 'library' && selected.library) {
        var row = Array.prototype.find.call(libraryList.querySelectorAll('[data-media-hash]'), function (button) {
          return button.dataset.mediaHash === selected.library.sha256;
        });
        if (row) row.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'center' });
      }
    }
    function renderLibrary() {
      libraryList.replaceChildren();
      var previous = '';
      files.slice().sort(function (a, b) { return b.uploaded_at.localeCompare(a.uploaded_at); }).forEach(function (item) {
        var day = formatDate(item.uploaded_at);
        if (day !== previous) {
          var heading = document.createElement('h3');
          heading.textContent = day;
          libraryList.appendChild(heading);
          previous = day;
        }
        var button = document.createElement('button');
        button.type = 'button';
        button.dataset.mediaHash = item.sha256;
        var icon = document.createElement('span');
        icon.className = 'media-entry__file-icon';
        icon.innerHTML = window.gkpsMediaIcon(item.family);
        var text = document.createElement('span');
        var title = document.createElement('strong');
        title.textContent = item.name;
        var meta = document.createElement('small');
        meta.textContent = names[item.family] + ' · ' + formatSize(item.size);
        text.append(title, meta);
        button.append(icon, text);
        button.onclick = function () { selected.library = item; sync(); };
        libraryList.appendChild(button);
      });
      if (!files.length) libraryList.textContent = 'No files in this Media Library.';
      sync();
    }
    async function refreshLibrary() {
      try {
        var result = await responseJson(await fetch(helper + '/files', { mode: 'cors', cache: 'no-store' }));
        files = result.files || [];
        if (form.isConnected) renderLibrary();
      } catch (problem) {
        if (form.isConnected) libraryList.textContent = 'Local library unavailable.';
      }
    }
    async function choose(file) {
      if (!file) return;
      if (file.size > 200000000) return showError('File too large', 'The maximum file size is 200 MB. Choose a smaller file.');
      if (!file.size) return showError('File not supported', 'Choose a non-empty image, audio, video, PDF, PPT, or PPTX file.');
      save.disabled = true;
      try {
        var local = await status();
        var result = await responseJson(await fetch(helper + '/inspect', {
          method: 'POST', mode: 'cors', body: file,
          headers: { 'X-GKPS-Media-Token': local.write_token, 'X-GKPS-Filename': file.name }
        }));
        if (!form.isConnected) return;
        selected.upload = Object.assign({ chosenName: file.name, sourceFile: file }, result);
        selectTab('upload');
      } catch (problem) {
        var unsupported = /not supported|malformed|file ended|plain filename/i.test(problem.message || '');
        showError(unsupported ? 'File not supported' : 'Could not add file',
                  problem.message || 'The local library is unavailable.');
        sync();
      }
    }
    tabs.onclick = function (event) {
      var button = event.target.closest('[data-media-tab-button]');
      if (button) selectTab(button.dataset.mediaTabButton);
    };
    form.querySelectorAll('[data-media-choose]').forEach(function (button) { button.onclick = function () { input.value = ''; input.click(); }; });
    input.onchange = function () { choose(input.files[0]); };
    drop.ondragover = function (event) { event.preventDefault(); drop.classList.add('is-dragging'); };
    drop.ondragleave = function () { drop.classList.remove('is-dragging'); };
    drop.ondrop = function (event) { event.preventDefault(); drop.classList.remove('is-dragging'); choose(event.dataTransfer.files[0]); };
    refreshLibrary();
    sync();

    form.addEventListener('submit', async function (event) {
      if (form.dataset.mediaReady) return;
      event.preventDefault();
      event.stopImmediatePropagation();
      var item = selected[active];
      if (!item) return;
      save.disabled = true;
      try {
        if (active === 'upload') {
          var local = await status();
          var imported = await responseJson(await fetch(helper + '/import', {
            method: 'POST', mode: 'cors', body: item.sourceFile,
            headers: { 'X-GKPS-Media-Token': local.write_token, 'X-GKPS-Filename': item.sourceFile.name }
          }));
          if (imported.sha256 !== item.sha256 || imported.family !== item.family) {
            throw new Error('The selected file changed since inspection. Choose it again.');
          }
          item = imported;
        }
        var registered = await responseJson(await fetch(form.dataset.mediaRegisterUrl, {
          method: 'POST', credentials: 'same-origin',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
          body: JSON.stringify({ sha256: item.sha256, size: item.size,
                                 family: item.family, name: item.name })
        }));
        if (!form.isConnected) return;
        form.querySelector('[name="media"]').value = registered.sha256;
        form.querySelector('[name="media_filename"]').value = item.name;
        form.dataset.mediaReady = 'true';
        save.disabled = false;
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      } catch (problem) {
        showError('Could not save media', problem.message || 'Try again.');
        sync();
      }
    }, true);
  }
  window.gkpsMediaEntry = { wire: wire };
})();
