/* Transfers belong to the local companion; this view only observes and starts them. */
(function () {
  'use strict';
  const endpoint = 'http://127.0.0.1:63174/v1';
  const paths = {
    upload: '<path d="M12 16V4m0 0L8 8m4-4 4 4M4.5 15.5v3.3c0 .9.7 1.7 1.7 1.7h11.6c1 0 1.7-.8 1.7-1.7v-3.3"/>',
    download: '<path d="M12 4v12m0 0-4-4m4 4 4-4M4.5 15.5v3.3c0 .9.7 1.7 1.7 1.7h11.6c1 0 1.7-.8 1.7-1.7v-3.3"/>',
    both: '<path d="M8 18V5m0 0L5 8m3-3 3 3M16 6v13m0 0-3-3m3 3 3-3"/>',
    finished: '<circle cx="12" cy="12" r="8.3"/><path d="M12 7v5l3.2 2"/>',
    cloudCheck: '<path d="M7 18.5H5.8A4.3 4.3 0 0 1 5.5 10a6.6 6.6 0 0 1 12.7-1.4A4.6 4.6 0 0 1 18 18.5h-1m-9.2-3 2.4 2.4 4.3-4.5"/>',
    cloudOff: '<path d="M3 3l18 18M7 18.5H5.8A4.3 4.3 0 0 1 5.5 10a6.6 6.6 0 0 1 12.7-1.4 4.6 4.6 0 0 1 1.1 7.3"/>',
    cloudUp: '<path d="M7 18.5H5.8A4.3 4.3 0 0 1 5.5 10a6.6 6.6 0 0 1 12.7-1.4A4.6 4.6 0 0 1 18 18.5h-1M12 20v-8m0 0-3.1 3.1M12 12l3.1 3.1"/>',
    localCheck: '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 21h8m-4-3v3m-3.2-10 2.2 2.2 4.2-4.2"/>',
    localMissing: '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 21h8m-4-3v3M9.5 9.5l5 5m0-5-5 5"/>'
  };
  const glyph = name => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths[name] + '</svg>';
  let token = '', connected = false, transfers = [], retrying = [], files = [], online = {}, session = null, source = 'library', lastCloudAt = 0;
  const $ = id => document.getElementById(id);
  const json = (url, options) => fetch(url, Object.assign({ cache: 'no-store' }, options || {})).then(async response => {
    const data = await response.json();
    if (!response.ok) throw Error(data.error || 'Transfer unavailable');
    return data;
  });
  const local = (path, options) => json(endpoint + path, Object.assign({ mode: 'cors' }, options || {}));
  const write = (path, method, body) => local(path, { method, headers: { 'Content-Type': 'application/json', 'X-GKPS-Media-Token': token }, body: body === undefined ? undefined : JSON.stringify(body) });
  const csrf = () => (document.cookie.match(/(?:^|; )csrftoken=([^;]*)/) || [])[1] || '';
  const post = (url) => json(url, { method: 'POST', credentials: 'same-origin', headers: { 'X-CSRFToken': decodeURIComponent(csrf()) } });
  function close(dialog) {
    if (!dialog.open) return;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return dialog.close();
    dialog.classList.add('closing');
    setTimeout(() => { dialog.close(); dialog.classList.remove('closing'); }, 150);
  }
  function renderTransfers() {
    const button = $('mediaTransferRail'), host = $('mediaTransfersList');
    if (!button || !host) return;
    const active = transfers.filter(t => t.status === 'active');
    if (active.length && !session) session = { started: Date.now(), seen: new Set(), viewed: false };
    if (session) transfers.filter(t => t.status !== 'active' && Date.parse(t.ended_at) >= session.started).forEach(t => session.seen.add(t.id));
    const visible = active.length || session && !session.viewed;
    button.hidden = !visible || !connected;
    if (visible) {
      const kind = active.length ? (active.every(t => t.direction === 'upload') ? 'upload' : active.every(t => t.direction === 'download') ? 'download' : 'both') : 'finished';
      $('mediaTransferRailIcon').innerHTML = glyph(kind);
      $('mediaTransferRailDot').dataset.state = active.length ? 'active' : transfers.some(t => session.seen.has(t.id) && t.status !== 'completed') ? 'failed' : 'completed';
      button.title = active.length ? 'Transfer progress' : 'Recent transfers';
    }
    const shown = source === 'rail' && active.length ? active : transfers;
    host.replaceChildren();
    if (!connected) { const p = document.createElement('p'); p.className = 'media-transfers__empty'; p.textContent = 'Local library unavailable on this computer.'; host.append(p); return; }
    if (!shown.length) { const p = document.createElement('p'); p.className = 'media-transfers__empty'; p.textContent = 'No transfers yet.'; host.append(p); return; }
    let separated = false;
    shown.forEach(t => {
      if (source === 'rail' && !active.length && session && !session.seen.has(t.id) && !separated) {
        const divider = document.createElement('hr'); divider.className = 'media-transfers__divider'; host.append(divider); separated = true;
      }
      const row = document.createElement('div'); row.className = 'media-transfers__row';
      const mark = document.createElement('span'); mark.className = 'media-transfers__mark'; mark.innerHTML = glyph(t.direction);
      const main = document.createElement('div'); main.className = 'media-transfers__main';
      const name = document.createElement('strong'); name.textContent = t.name; main.append(name);
      const state = document.createElement('span'); state.textContent = t.status === 'active' ? Math.min(100, Math.round(100 * t.bytes_done / Math.max(1, t.size))) + '%' : t.status === 'completed' ? 'Completed' : t.status === 'cancelled' ? 'Cancelled' : 'Failed'; main.append(state);
      row.append(mark, main); host.append(row);
    });
  }
  function renderService() {
    const dialog = $('serviceMediaDialog'); if (!dialog) return;
    dialog.querySelectorAll('[data-media-sha]').forEach(row => {
      if (window.gkpsMediaIcon) row.querySelector('.service-media__icon').innerHTML = window.gkpsMediaIcon(row.dataset.mediaFamily);
      const sha = row.dataset.mediaSha;
      const file = files.find(f => f.sha256 === sha), job = transfers.find(t => t.sha256 === sha && t.direction === 'download' && t.status === 'active');
      const onlineAt = online[sha], localState = row.querySelector('[data-local-state]'), cloudState = row.querySelector('[data-online-state]'), action = row.querySelector('[data-download-action]');
      localState.innerHTML = connected ? glyph(file ? 'localCheck' : 'localMissing') : '−'; localState.title = !connected ? 'Local library unavailable' : file ? 'On this computer' : 'Missing on this computer';
      localState.setAttribute('role', 'img'); localState.setAttribute('aria-label', localState.title);
      cloudState.innerHTML = glyph(onlineAt ? 'cloudCheck' : 'cloudOff'); cloudState.title = onlineAt ? 'Available online' : 'Unavailable online';
      cloudState.setAttribute('role', 'img'); cloudState.setAttribute('aria-label', cloudState.title);
      localState.classList.toggle('is-missing', connected && !file);
      localState.classList.toggle('is-unavailable', !connected);
      cloudState.classList.toggle('is-offline', !onlineAt);
      action.replaceChildren();
      if (job) {
        const progress = document.createElement(job.automatic ? 'span' : 'button'); progress.className = 'media-handoff__ring'; progress.style.setProperty('--progress', (100 * job.bytes_done / Math.max(1, job.size)) + '%'); progress.textContent = job.automatic ? '↓' : '×'; progress.title = job.automatic ? 'Automatic download' : 'Cancel download';
        if (job.automatic) { progress.setAttribute('role', 'progressbar'); progress.setAttribute('aria-label', 'Download progress'); progress.setAttribute('aria-valuemin', '0'); progress.setAttribute('aria-valuemax', '100'); progress.setAttribute('aria-valuenow', String(Math.round(100 * job.bytes_done / Math.max(1, job.size)))); }
        else { progress.type = 'button'; progress.setAttribute('aria-label', 'Cancel download, ' + Math.round(100 * job.bytes_done / Math.max(1, job.size)) + '% complete'); }
        if (!job.automatic) progress.addEventListener('click', () => write('/transfers/' + job.id, 'DELETE').then(poll));
        action.append(progress);
      } else if (retrying.some(task => task.sha256 === sha)) {
        const retry = document.createElement('span'); retry.className = 'media-handoff__retry'; retry.textContent = '↻'; retry.title = 'Retrying automatic download'; retry.setAttribute('aria-label', 'Retrying automatic download'); action.append(retry);
      } else if (connected && !file && onlineAt && row.dataset.mediaPast === 'true') {
        const button = document.createElement('button'); button.type = 'button'; button.className = 'media-handoff__action'; button.innerHTML = glyph('download'); button.title = 'Download'; button.setAttribute('aria-label', 'Download file');
        button.addEventListener('click', () => download(sha, false)); action.append(button);
      }
    });
  }
  function render() { renderTransfers(); renderService(); document.dispatchEvent(new CustomEvent('media:status', { detail: { transfers, online, files } })); }
  async function poll() {
    let uploadJustFinished = false;
    try {
      const status = await local('/status'); token = status.write_token;
      const [jobs, inventory] = await Promise.all([local('/transfers'), local('/files')]);
      const hadActiveUpload = transfers.some(t => t.direction === 'upload' && t.status === 'active');
      connected = true; transfers = jobs.transfers || []; retrying = jobs.retrying || []; files = inventory.files || [];
      uploadJustFinished = hadActiveUpload && !transfers.some(t => t.direction === 'upload' && t.status === 'active');
    } catch (_) { connected = false; token = ''; files = []; }
    if (uploadJustFinished || Date.now() - lastCloudAt > 60000) {
      try { online = (await json('/media-library/cloud/status/')).online || {}; lastCloudAt = Date.now(); } catch (_) { /* Keep the last known status until the next check. */ }
    }
    render();
  }
  async function download(sha, automatic, eligibleUntil) {
    if (!token) await poll();
    const permission = await json('/media-library/cloud/' + sha + '/download/');
    await write('/transfers', 'POST', Object.assign({ direction: 'download', automatic, eligible_until: eligibleUntil }, permission));
    poll();
  }
  async function reconcile() {
    try {
      await poll(); if (!token) return;
      const manifest = await json('/media-library/cloud/manifest/');
      await write('/auto-downloads/sync', 'POST', { hashes: (manifest.files || []).map(file => file.sha256) });
      for (const file of manifest.files || []) {
        if (!files.some(localFile => localFile.sha256 === file.sha256) && !retrying.some(task => task.sha256 === file.sha256)) await download(file.sha256, true, file.eligible_until);
      }
    } catch (_) { /* Retry on the next poll/reconnect. */ }
  }
  async function share(sha) {
    if (!token) await poll();
    const permission = await post('/media-library/cloud/' + sha + '/begin/');
    if (!permission.online) await write('/transfers', 'POST', Object.assign({ direction: 'upload' }, permission));
    lastCloudAt = 0;
    poll();
  }
  function open(sourceName) {
    source = sourceName; const dialog = $('mediaTransfersDialog'); if (!dialog) return;
    renderTransfers(); dialog.showModal();
    if (sourceName === 'rail' && session && !transfers.some(t => t.status === 'active')) {
      session.viewed = true;
      dialog.addEventListener('close', () => { session = null; renderTransfers(); }, { once: true });
    }
  }
  document.addEventListener('click', event => {
    if (event.target.closest('#mediaTransferRail')) open('rail');
    if (event.target.closest('#mediaTransfersButton')) open('library');
    if (event.target.closest('#serviceMediaButton')) { renderService(); $('serviceMediaDialog').showModal(); }
    if (event.target.closest('[data-transfer-close]')) close(event.target.closest('dialog'));
  });
  document.addEventListener('click', event => {
    if (event.target.matches('#mediaTransfersDialog, #serviceMediaDialog')) close(event.target);
  });
  document.addEventListener('cancel', event => {
    if (event.target.matches('#mediaTransfersDialog, #serviceMediaDialog')) { event.preventDefault(); close(event.target); }
  }, true);
  window.gkpsMediaHandoff = { share, download, poll, open, glyph, getState: () => ({ transfers, online, files }) };
  document.addEventListener('shell:page', () => { setTimeout(() => { renderService(); reconcile(); }, 0); });
  reconcile(); setInterval(poll, 2000); setInterval(reconcile, 60000);
})();
