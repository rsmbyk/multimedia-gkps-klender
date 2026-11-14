/* Slice 192 preview — walk-through scenarios plus a live setup simulator.
   The transcript lines are the spec's UI/UX, verbatim; the live mode applies the same grammar. */
'use strict';

var V = 'MULTIMEDIA_GKPS_KLENDER_PRODUCTION_ORIGIN';
var HINT = 'gkps: edit <n> or delete <n> reworks the list; an empty line proceeds';

var SCENARIOS = [
  {
    id: 'fresh-multi',
    title: 'US1 · fresh start, two origins, one typo',
    desc: 'No .env. One origin per prompt: the trailing slash is rejected naming position 1, each accepted entry shows the numbered list, the empty line proceeds.',
    lines: [
      { t: '$ docker\\up.ps1', c: 'cmd' },
      { t: 'gkps: no ' + V + ' found — the media companion needs it to accept this computer\'s pages' },
      { t: 'gkps: enter the origins this computer\'s pages may come from, one at a time' },
      { t: 'gkps: scheme and hostname only, no path, no trailing slash' },
      { t: 'gkps: the local origins are always allowed and need no entry' },
      { t: 'origin: https://multimedia.example.org/', c: 'input', cur: true },
      { t: 'gkps: origin 1 carries no path, query or trailing slash', c: 'reject' },
      { t: 'origin: https://multimedia.example.org', c: 'input', cur: true },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: HINT },
      { t: 'origin: https://staging.multimedia.example.org', c: 'input', cur: true },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: 'gkps:   2. https://staging.multimedia.example.org' },
      { t: HINT },
      { t: 'origin:', c: 'input', cur: true },
      { t: 'gkps: wrote ' + V + '=https://multimedia.example.org,https://staging.multimedia.example.org to .env', c: 'ok' },
      { t: 'gkps: font directories from this computer (2):', c: 'ok' },
      { t: 'gkps:   C:/Windows/Fonts' },
      { t: 'gkps:   C:/Users/<operator>/AppData/Local/Microsoft/Windows/Fonts' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'fresh-single',
    title: 'US1 · fresh start, one origin',
    desc: 'The same loop entered once and proceeded on the empty line: no position prefix, single-item write.',
    lines: [
      { t: '$ docker\\up.ps1', c: 'cmd' },
      { t: 'gkps: no ' + V + ' found — the media companion needs it to accept this computer\'s pages' },
      { t: 'gkps: enter the origins this computer\'s pages may come from, one at a time' },
      { t: 'gkps: scheme and hostname only, no path, no trailing slash' },
      { t: 'gkps: the local origins are always allowed and need no entry' },
      { t: 'origin: https://multimedia.example.org', c: 'input', cur: true },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: HINT },
      { t: 'origin:', c: 'input', cur: true },
      { t: 'gkps: wrote ' + V + '=https://multimedia.example.org to .env', c: 'ok' },
      { t: 'gkps: font directories from this computer (2):', c: 'ok' },
      { t: 'gkps:   C:/Windows/Fonts' },
      { t: 'gkps:   C:/Users/<operator>/AppData/Local/Microsoft/Windows/Fonts' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'duplicate',
    title: 'US3 · an origin already recorded',
    desc: 'Mid-loop: the duplicate is named, not recorded twice, the list is shown again, and the empty line proceeds.',
    lines: [
      { t: 'origin: https://multimedia.example.org', c: 'input', cur: true },
      { t: 'gkps: that origin is already recorded', c: 'reject' },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: HINT },
      { t: 'origin:', c: 'input', cur: true },
      { t: 'gkps: wrote ' + V + '=https://multimedia.example.org to .env', c: 'ok' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'edit-delete',
    title: 'US5 · delete a slot, edit another',
    desc: 'Mid-loop with two recorded: delete 2 removes and renumbers, edit 1 names the slot and takes the replacement, the empty line proceeds.',
    lines: [
      { t: 'origin: delete 2', c: 'input', cur: true },
      { t: 'gkps: deleted 2. https://staging.multimedia.example.org' },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: HINT },
      { t: 'origin: edit 1', c: 'input', cur: true },
      { t: 'gkps: editing 1. https://multimedia.example.org — enter the replacement' },
      { t: 'origin: https://www.multimedia.example.org', c: 'input', cur: true },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://www.multimedia.example.org' },
      { t: HINT },
      { t: 'origin:', c: 'input', cur: true },
      { t: 'gkps: wrote ' + V + '=https://www.multimedia.example.org to .env', c: 'ok' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'edit-cancelled',
    title: 'US5 · an edit cancelled by an empty line',
    desc: 'An empty line at the replacement prompt returns to the list unchanged.',
    lines: [
      { t: 'origin: edit 2', c: 'input', cur: true },
      { t: 'gkps: editing 2. https://staging.multimedia.example.org — enter the replacement' },
      { t: 'origin:', c: 'input', cur: true },
      { t: 'gkps: edit cancelled' },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: 'gkps:   2. https://staging.multimedia.example.org' },
      { t: HINT },
      { t: 'origin:', c: 'input', cur: true },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'out-of-range',
    title: 'US5 · a slot nobody recorded',
    desc: 'An unknown slot is named, the list is shown, nothing changes.',
    lines: [
      { t: 'origin: delete 3', c: 'input', cur: true },
      { t: 'gkps: no origin 3 is recorded', c: 'reject' },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: HINT },
      { t: 'origin:', c: 'input', cur: true },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'configured-single',
    title: 'US2 · configured start, no prompt',
    desc: 'The checkout\'s .env already names the origin: what is recorded is displayed one per line, never comma-separated, and the start continues.',
    lines: [
      { t: '$ ./docker/up.sh', c: 'cmd' },
      { t: 'gkps: production origins recorded:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: 'gkps: font directories from this computer (1):', c: 'ok' },
      { t: 'gkps:   /usr/share/fonts' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'configured-multi',
    title: 'US2 · configured with production and staging',
    desc: 'The same list carries every recorded origin; the font listing follows.',
    lines: [
      { t: '$ ./docker/up.sh', c: 'cmd' },
      { t: 'gkps: production origins recorded:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: 'gkps:   2. https://staging.multimedia.example.org' },
      { t: 'gkps: font directories from this computer (2):', c: 'ok' },
      { t: 'gkps:   /usr/share/fonts' },
      { t: 'gkps:   /home/<operator>/.local/share/fonts' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'shell-configured',
    title: 'US2 · the shell carries the origins',
    desc: 'No .env; the environment exports the value: the same numbered list whatever the source, and nothing is written.',
    lines: [
      { t: '$ MULTIMEDIA_GKPS_KLENDER_PRODUCTION_ORIGIN=https://multimedia.example.org ./docker/up.sh', c: 'cmd' },
      { t: 'gkps: production origins recorded:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: 'gkps: font directories from this computer (1):', c: 'ok' },
      { t: 'gkps:   /usr/share/fonts' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'no-fonts',
    title: 'US4 · no font directory found',
    desc: 'Zero found is said outright instead of a zero count; the stack starts exactly as before.',
    lines: [
      { t: '$ ./docker/up.sh', c: 'cmd' },
      { t: 'gkps: production origins recorded:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: 'gkps: no font directory found on this computer', c: 'ok' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  },
  {
    id: 'abort',
    title: 'US3 · empty line with nothing recorded, or EOF',
    desc: 'Non-zero exit, the variable is named, nothing is written.',
    lines: [
      { t: '$ docker\\up.ps1', c: 'cmd' },
      { t: 'gkps: no ' + V + ' found — the media companion needs it to accept this computer\'s pages' },
      { t: 'gkps: enter the origins this computer\'s pages may come from, one at a time' },
      { t: 'gkps: scheme and hostname only, no path, no trailing slash' },
      { t: 'gkps: the local origins are always allowed and need no entry' },
      { t: 'origin:', c: 'input', cur: true },
      { t: 'gkps: no origin entered — set ' + V + ' in .env and start again', c: 'reject' },
      { t: '(exit code 1, nothing written)', c: 'meta' }
    ]
  },
  {
    id: 'shell-broken',
    title: 'US3 · the shell\'s value is broken',
    desc: 'The value arrived from the environment, which wins over .env — the launcher says so and stops without writing.',
    lines: [
      { t: 'gkps: ' + V + ' in this shell is not an exact origin — fix the variable; the shell wins over .env', c: 'reject' },
      { t: '(exit code 1, nothing written)', c: 'meta' }
    ]
  },
  {
    id: 'env-broken',
    title: 'US3 · the .env value is broken',
    desc: 'A malformed line in .env is named, then the standard loop runs and the recorded set is written in place.',
    lines: [
      { t: '$ ./docker/up.sh', c: 'cmd' },
      { t: 'gkps: ' + V + ' in .env is not an exact origin — replace it', c: 'reject' },
      { t: 'gkps: enter the origins this computer\'s pages may come from, one at a time' },
      { t: 'gkps: scheme and hostname only, no path, no trailing slash' },
      { t: 'gkps: the local origins are always allowed and need no entry' },
      { t: 'origin: https://multimedia.example.org', c: 'input', cur: true },
      { t: 'gkps: recorded so far:' },
      { t: 'gkps:   1. https://multimedia.example.org' },
      { t: HINT },
      { t: 'origin:', c: 'input', cur: true },
      { t: 'gkps: wrote ' + V + '=https://multimedia.example.org to .env', c: 'ok' },
      { t: 'gkps: font directories from this computer (1):', c: 'ok' },
      { t: 'gkps:   /usr/share/fonts' },
      { t: '(start continues exactly as today)', c: 'meta' }
    ]
  }
];

var si = 0, li = 0, timer = null;
var term = document.getElementById('term');
var desc = document.getElementById('desc');
var pills = document.getElementById('pills');

// Outside the desktop chat frame the theme variables are not injected; theme the page itself.
if (!getComputedStyle(document.documentElement).getPropertyValue('--foreground').trim()) {
  document.documentElement.classList.add('standalone');
}

function makeLine(l, isLast) {
  var span = document.createElement('span');
  span.className = 'line ' + (l.c || '');
  if (l.c === 'input') {
    var lab = document.createElement('span');
    lab.className = 'label';
    lab.textContent = 'origin:';
    var val = document.createElement('span');
    val.className = 'val';
    val.textContent = l.t.replace(/^origin:\s?/, '');
    span.appendChild(lab);
    span.appendChild(document.createTextNode(' '));
    span.appendChild(val);
  } else {
    span.textContent = l.t;
  }
  if (l.cur && isLast) span.classList.add('cur');
  return span;
}

function render() {
  var s = SCENARIOS[si];
  desc.textContent = s.desc;
  term.textContent = '';
  for (var i = 0; i < li; i++) term.appendChild(makeLine(s.lines[i], i === li - 1));
  Array.prototype.forEach.call(pills.children, function (b, i) {
    b.setAttribute('aria-current', i === si ? 'true' : 'false');
  });
  var m = location.hash.match(/^#([\w-]+)\/(\d+)$/);
  var want = '#' + s.id + '/' + li;
  if (!m || m[1] !== s.id || +m[2] !== li) history.replaceState(null, '', want);
}

function stop() { if (timer) { clearInterval(timer); timer = null; } }
function next() { if (li < SCENARIOS[si].lines.length) { li++; render(); } else stop(); }
function back() { stop(); if (li > 1) { li--; render(); } }

function goTo(si2, li2) {
  stop();
  si = Math.max(0, Math.min(SCENARIOS.length - 1, si2));
  li = Math.max(1, Math.min(SCENARIOS[si].lines.length, li2 || 1));
  render();
}

SCENARIOS.forEach(function (s, i) {
  var b = document.createElement('button');
  b.type = 'button';
  b.textContent = s.title;
  b.addEventListener('click', function () { goTo(i, 1); });
  pills.appendChild(b);
});

document.getElementById('next').addEventListener('click', function () { stop(); next(); });
document.getElementById('back').addEventListener('click', back);
document.getElementById('run').addEventListener('click', function () {
  stop();
  if (li >= SCENARIOS[si].lines.length) li = 1;
  render();
  timer = setInterval(next, 220);
});
document.getElementById('prevS').addEventListener('click', function () { goTo(si - 1, 1); });
document.getElementById('nextS').addEventListener('click', function () { goTo(si + 1, 1); });

document.addEventListener('keydown', function (e) {
  if (live.on) return;
  if (e.key === 'Enter' || e.key === 'ArrowRight') { stop(); next(); e.preventDefault(); }
  else if (e.key === 'Backspace' || e.key === 'ArrowLeft') { back(); e.preventDefault(); }
  else if (e.key === 'ArrowUp' || e.key === '[') { goTo(si - 1, 1); e.preventDefault(); }
  else if (e.key === 'ArrowDown' || e.key === ']') { goTo(si + 1, 1); e.preventDefault(); }
  else if (e.key === 'a') {
    document.getElementById('run').click();
    e.preventDefault();
  }
});

/* ---- live setup mode: the simulator applies the spec's grammar (FR-002, FR-003, FR-005, FR-011) ---- */

var live = { on: false, recorded: [], editing: 0, done: false };

function emit(lines) {
  lines.forEach(function (l) { term.appendChild(makeLine(l, false)); });
  term.scrollTop = term.scrollHeight;
}

function liveList() {
  var out = [{ t: 'gkps: recorded so far:' }];
  live.recorded.forEach(function (o, i) { out.push({ t: 'gkps:   ' + (i + 1) + '. ' + o }); });
  out.push({ t: HINT });
  return out;
}

function validate(t) {
  if (/\s/.test(t)) return 'is one line with no spaces';
  if (!/^https?:\/\//.test(t)) return 'starts with its scheme — http:// or https://';
  if (t.indexOf('@') !== -1) return 'carries no credentials — no @';
  var rest = t.slice(t.indexOf('://') + 3);
  if (/[\/?#]/.test(rest)) return 'carries no path, query or trailing slash';
  var host, port = '';
  if (rest.charAt(0) === '[') {
    var close = rest.indexOf(']');
    if (close === -1) return 'needs a hostname after the scheme';
    host = rest.slice(0, close + 1);
    if (rest.charAt(close + 1) === ':') port = rest.slice(close + 2);
    else if (rest.length > close + 1) return 'carries no path, query or trailing slash';
  } else {
    var c = rest.lastIndexOf(':');
    if (c !== -1) { host = rest.slice(0, c); port = rest.slice(c + 1); } else host = rest;
  }
  if (!host) return 'needs a hostname after the scheme';
  if (port && !/^\d{1,5}$/.test(port)) return 'needs a numeric port in range';
  if (port && parseInt(port, 10) > 65535) return 'needs a numeric port in range';
  return '';
}

function reject(slot, rule) { emit([{ t: 'gkps: origin ' + slot + ' ' + rule, c: 'reject' }]); }

function endLive() {
  document.getElementById('livein').disabled = true;
  document.getElementById('reset').hidden = false;
}

function liveSubmit(raw) {
  if (live.done) return;
  var t = raw.replace(/^\s+|\s+$/g, '');
  emit([{ t: 'origin:' + (t ? ' ' + t : ''), c: 'input' }]);
  if (live.editing) {
    if (t === '') {
      emit([{ t: 'gkps: edit cancelled' }]);
      live.editing = 0;
      emit(liveList());
      return;
    }
    var rule = validate(t);
    if (rule) { reject(live.editing, rule); return; }
    if (live.recorded.some(function (o, i) { return i !== live.editing - 1 && o === t; })) {
      emit([{ t: 'gkps: that origin is already recorded', c: 'reject' }]);
      return;
    }
    live.recorded[live.editing - 1] = t;
    live.editing = 0;
    emit(liveList());
    return;
  }
  if (t === '') {
    live.done = true;
    if (live.recorded.length) {
      emit([
        { t: 'gkps: wrote ' + V + '=' + live.recorded.join(',') + ' to .env', c: 'ok' },
        { t: 'gkps: font directories from this computer (2):', c: 'ok' },
        { t: 'gkps:   C:/Windows/Fonts' },
        { t: 'gkps:   C:/Users/<operator>/AppData/Local/Microsoft/Windows/Fonts' },
        { t: '(simulated start — the real launcher continues with compose)', c: 'meta' }
      ]);
    } else {
      emit([
        { t: 'gkps: no origin entered — set ' + V + ' in .env and start again', c: 'reject' },
        { t: '(exit code 1, nothing written)', c: 'meta' }
      ]);
    }
    endLive();
    return;
  }
  var mDel = t.match(/^delete (\d+)$/), mEdit = t.match(/^edit (\d+)$/);
  if (mDel || mEdit) {
    var n = parseInt((mDel || mEdit)[1], 10);
    if (n < 1 || n > live.recorded.length) {
      emit([{ t: 'gkps: no origin ' + n + ' is recorded', c: 'reject' }]);
      emit(liveList());
      return;
    }
    if (mDel) {
      var removed = live.recorded.splice(n - 1, 1)[0];
      emit([{ t: 'gkps: deleted ' + n + '. ' + removed }]);
      if (live.recorded.length) emit(liveList());
      return;
    }
    live.editing = n;
    emit([{ t: 'gkps: editing ' + n + '. ' + live.recorded[n - 1] + ' — enter the replacement' }]);
    return;
  }
  var rule2 = validate(t);
  if (rule2) { reject(live.recorded.length + 1, rule2); return; }
  if (live.recorded.indexOf(t) !== -1) {
    emit([{ t: 'gkps: that origin is already recorded', c: 'reject' }]);
    emit(liveList());
    return;
  }
  live.recorded.push(t);
  emit(liveList());
}

function setMode(id) {
  document.getElementById('modeWalk').setAttribute('aria-pressed', id === 'modeWalk' ? 'true' : 'false');
  document.getElementById('modeLive').setAttribute('aria-pressed', id === 'modeLive' ? 'true' : 'false');
}

function liveStart() {
  live.on = true; live.recorded = []; live.editing = 0; live.done = false;
  stop();
  desc.textContent = 'Live setup — type at the origin: prompt below. The simulator applies the spec\'s grammar: exact-origin validation, edit <n>, delete <n>, an empty line proceeds (or aborts when nothing is recorded).';
  term.textContent = '';
  pills.hidden = true;
  document.querySelector('.controls').hidden = true;
  document.querySelector('.hint').hidden = true;
  document.getElementById('liverow').hidden = false;
  document.getElementById('livein').disabled = false;
  document.getElementById('reset').hidden = true;
  setMode('modeLive');
  history.replaceState(null, '', '#live');
  emit([
    { t: '$ docker\\up.ps1', c: 'cmd' },
    { t: 'gkps: no ' + V + ' found — the media companion needs it to accept this computer\'s pages' },
    { t: 'gkps: enter the origins this computer\'s pages may come from, one at a time' },
    { t: 'gkps: scheme and hostname only, no path, no trailing slash' },
    { t: 'gkps: the local origins are always allowed and need no entry' }
  ]);
  document.getElementById('livein').focus();
}

function walkStart() {
  live.on = false;
  pills.hidden = false;
  document.querySelector('.controls').hidden = false;
  document.querySelector('.hint').hidden = false;
  document.getElementById('liverow').hidden = true;
  setMode('modeWalk');
  render();
}

document.getElementById('livein').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') { liveSubmit(this.value); this.value = ''; e.preventDefault(); }
});
document.getElementById('modeLive').addEventListener('click', liveStart);
document.getElementById('modeWalk').addEventListener('click', walkStart);
document.getElementById('reset').addEventListener('click', liveStart);

(function init() {
  var m = location.hash.match(/^#([\w-]+)\/(\d+)$/);
  if (location.hash === '#live') { liveStart(); return; }
  if (m) {
    var i = SCENARIOS.findIndex(function (s) { return s.id === m[1]; });
    if (i >= 0) { goTo(i, Math.max(1, +m[2])); return; }
  }
  goTo(0, 2);
})();
