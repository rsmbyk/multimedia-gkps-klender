/* Preview rail (spec 204) — reads what is PAINTED, never a state variable.
 *
 * Every number in the readout comes from the dock's own DOM: the header's
 * aria-expanded, the inner's is-open class and its measured box height. The trail
 * records each click and, after every service open, what the open left standing.
 */
(function () {
  'use strict';

  var panel = document.getElementById('dockPanel');
  var entryList = document.getElementById('entryList');
  var runBody = document.getElementById('runBody');
  var readout = document.getElementById('readout');
  var stateLine = document.getElementById('stateLine');
  var verdict = document.getElementById('verdict');
  var logList = document.getElementById('log');
  var CHANNEL = 'gkps-service-display';

  function rows() {
    return [].slice.call(entryList.querySelectorAll('.entryli')).map(function (li) {
      var row = li.querySelector('.entryrow');
      var inner = li.querySelector('.entryinner');
      var title = row && row.querySelector('.entryrow__t');
      return {
        index: Number(li.dataset.index),
        label: ((title ? title.textContent : (row ? row.textContent : '')) || '')
                 .trim().replace(/\s+/g, ' '),
        expanded: row ? row.getAttribute('aria-expanded') : null,
        live: li.dataset.live === 'true',
        open: !!inner && inner.classList.contains('is-open'),
        height: inner ? Math.round(inner.getBoundingClientRect().height) : null
      };
    });
  }

  function display() {
    try { return JSON.parse(localStorage.getItem('gkps-display') || 'null'); }
    catch (e) { return null; }
  }

  function log(message) {
    var li = document.createElement('li');
    li.textContent = message;
    logList.appendChild(li);
    while (logList.children.length > 14) logList.removeChild(logList.firstChild);
  }

  function refresh() {
    var list = rows();
    readout.replaceChildren.apply(readout, list.map(function (r) {
      var tr = document.createElement('tr');
      if (r.open) tr.className = 'is-open';
      if (r.live) tr.className += ' is-live';
      [String(r.index + 1), r.label.slice(0, 34), r.expanded === null ? '—' : r.expanded,
       r.open ? 'true' : 'false', r.height === null ? '—' : r.height + ' px'].forEach(function (value, i) {
        var td = document.createElement('td');
        td.textContent = value;
        if (i === 0 || i >= 2) td.className = 'num';
        if (i === 1) td.className = 'label';
        tr.appendChild(td);
      });
      return tr;
    }));
    var state = display();
    var opens = list.filter(function (r) { return r.open; }).map(function (r) { return r.index; });
    stateLine.textContent =
      'behaviour: ' + window.__behaviour +
      '\nview: ' + panel.dataset.view +
      '   service: ' + (document.getElementById('runService').textContent || '—') +
      '\nopen blocks (index): [' + opens.join(', ') + ']' +
      '   live: ' + (list.filter(function (r) { return r.live; }).map(function (r) { return r.index; }).join(', ') || 'none') +
      '\nscrollTop: ' + Math.round(runBody.scrollTop) +
      '\ngkps-display: ' + JSON.stringify(state);
  }

  /* What an open left standing: the drafted rule says nothing but the live entry.
     Judged from the painted DOM once the open has settled — never from a timer that
     could fire against the previous list. */
  var pendingOpen = null;

  function judgeOpen(name) {
    pendingOpen = {name: name, at: Date.now()};
  }

  function settleOpen() {
    if (!pendingOpen || Date.now() - pendingOpen.at < 600) return;
    if (panel.dataset.view !== 'run') return;
    var name = pendingOpen.name;
    pendingOpen = null;
    var list = rows();
    var leaked = list.filter(function (r) { return r.open && !r.live; })
                     .map(function (r) { return r.index; });
    var live = list.filter(function (r) { return r.live; }).map(function (r) { return r.index; });
    var ok = leaked.length === 0;
    verdict.hidden = false;
    verdict.dataset.ok = ok ? 'true' : 'false';
    verdict.textContent = 'at the open of ' + name + ' → open blocks [' +
      list.filter(function (r) { return r.open; }).map(function (r) { return r.index; }).join(', ') +
      '], live [' + live.join(', ') + '], non-live open [' + leaked.join(', ') + '] ' +
      (ok ? '— nothing carried over' : '— CARRIED OVER by position') +
      '  (the state box below is now)';
    log('after opening ' + name + ': non-live open blocks [' + leaked.join(', ') + ']');
  }

  function pickerRow(id) {
    return document.querySelector('.servicerow[data-service="' + id + '"]');
  }

  function wait(ms) { return new Promise(function (r) { window.setTimeout(r, ms); }); }

  async function toPicker() {
    if (panel.dataset.view !== 'pick') {
      document.getElementById('switchBtn').click();
      await wait(260);
    }
  }

  async function openService(id) {
    await toPicker();
    var row = pickerRow(id);
    if (!row) { log('no picker row for service ' + id); return; }
    row.click();
    await wait(650);
    panel.focus();
  }

  async function ensureOpen(index) {
    var inner = document.getElementById('entryinner-' + index);
    if (!inner) { log('entry ' + (index + 1) + ' has no block to open'); return false; }
    if (!inner.classList.contains('is-open')) {
      var li = entryList.querySelector('.entryli[data-index="' + index + '"]');
      li.querySelector('.entryrow').click();
      await wait(420);
    }
    return true;
  }

  async function project(index) {
    if (!await ensureOpen(index)) return;
    var row = entryList.querySelector('.entryli[data-index="' + index + '"] .screenerow');
    if (!row) { log('entry ' + (index + 1) + ' has no screen row'); return; }
    row.scrollIntoView({block: 'center'});
    await wait(140);
    row.click();
    await wait(700);
    panel.focus();
  }

  var actions = {
    expand4: async function () {
      if (panel.dataset.view !== 'run') { log('open a service first'); return; }
      await ensureOpen(3);
      log('clicked the header of position 4');
    },
    project4: async function () { await project(3); log('projected position 4'); },
    picker: async function () { await toPicker(); log('back to the picker'); },
    reread: function () {
      /* the same message a saved change sends; the dock drops its cache and re-reads.
         The revision makes the payload differ, so the re-read really rebuilds. */
      window.__previewRevision = (window.__previewRevision || 0) + 1;
      try {
        var channel = new BroadcastChannel(CHANNEL);
        channel.postMessage({type: 'update'});
        channel.close();
        log('sent {type:"update"} on ' + CHANNEL + ' (payload rev' +
            window.__previewRevision + ') — a re-read, not an open');
      } catch (e) { log('BroadcastChannel unavailable: ' + e.message); }
    },
    reload: function () { window.location.reload(); }
  };

  document.getElementById('steps').addEventListener('click', function (event) {
    var button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.open) { openService(button.dataset.open); return; }
    if (button.dataset.run) { runSequence(); return; }
    var action = actions[button.dataset.step];
    if (action) action();
    panel.focus();
    refresh();
  });

  async function runSequence() {
    var buttons = document.querySelectorAll('#steps button');
    buttons.forEach(function (b) { b.disabled = true; });
    log('— the reported sequence —');
    await openService('155');
    await ensureOpen(3);
    log('position 4 opened by hand in 111ojo');
    await openService('149');
    await wait(300);
    await openService('155');
    await wait(400);
    buttons.forEach(function (b) { b.disabled = false; });
    panel.focus();
  }

  /* the dock's own clicks, recorded as they happen */
  document.addEventListener('click', function (event) {
    var service = event.target.closest('.servicerow');
    if (service) {
      log('picker: opened ' + service.dataset.name.slice(0, 24) + ' (' + service.dataset.service + ')');
      judgeOpen(service.dataset.name.slice(0, 24));
      return;
    }
    var header = event.target.closest('.entryrow');
    if (header) {
      log('header click on entry ' + header.dataset.index + ' (position ' + (Number(header.dataset.index) + 1) + ')');
    }
  }, true);

  document.getElementById('behaviourSwitch').addEventListener('change', function (event) {
    if (event.target.name !== 'behaviour') return;
    var url = new URL(window.location.href);
    url.searchParams.set('behaviour', event.target.value);
    window.location.href = url.toString();
  });

  var checked = document.querySelector(
    '#behaviourSwitch input[value="' + window.__behaviour + '"]');
  if (checked) checked.checked = true;

  window.setInterval(function () { settleOpen(); refresh(); }, 200);
  settleOpen();
  refresh();
  log('preview ready — behaviour: ' + window.__behaviour);
})();
