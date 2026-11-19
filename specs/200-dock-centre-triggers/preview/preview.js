/* The preview's behaviour, not the product's: it replays the dock's own centring
   maths (190 ms quintic ease-out glide, clamped, same layout coordinates as
   static/web/obs-dock.js:560-607) and gates it on the three triggers this slice
   keeps. Every condition the owner named is a control on the page, so each state
   is reachable by hand. */
(function () {
  var entryList = document.getElementById('entryList');
  var runBody = document.getElementById('runBody');
  var centreBtn = document.getElementById('centreBtn');
  var findScrim = document.getElementById('findScrim');
  var log = document.getElementById('pvLog');
  var read = document.getElementById('pvRead');
  var clockOut = document.getElementById('idleClock');
  var cb = {
    idleOn: document.getElementById('idleOn'),
    live: document.getElementById('cLive'),
    browsed: document.getElementById('cBrowsed'),
    layer: document.getElementById('cLayer'),
    other: document.getElementById('cOther')
  };
  cb.live.checked = true;
  cb.browsed.checked = true;

  /* ---------- a small service, in the runner's own shapes ------------------ */

  var NAMES = [
    'Pembuka', 'Nyanyian Pembuka — KJ 12 Hai Mari Berhimpun', 'Doa Pembukaan',
    'Pembacaan Pertama — Mazmur 100', 'Nyanyian — KJ 285 Suci, Suci, Suci', 'Persembahan',
    'Nyanyian Persembahan — KJ 336 Firman-Mu', 'Pelayanan Firman — Matius 5:1-8',
    'Nyanyian Firman — KJ 400 Tuhan, Dengar Doaku', 'Pengakuan Iman', 'Doa Syafaat',
    'Nyanyian — KJ 425 Doxology', 'Pemberitaan', 'Doxology', 'Berkat', 'Pengutusan',
    'Nyanyian Penutup — KJ 500', 'Amanat', 'Doa Penutup', 'Nyanyian — KJ 512',
    'Pengumuman Jemaat', 'Penutup', 'Nyanyian Tambahan — KJ 520', 'Salam Damai',
    'Doa Berkat', 'Pengutusan Akhir', 'Kesaksian', 'Nyanyian — KJ 530', 'Doa Syukur',
    'Pelayanan Anak', 'Pengumuman II', 'Penutup II', 'Nyanyian — KJ 540', 'Doa Malam'
  ];
  var ENTRIES = NAMES.map(function (label) {
    return {label: label, rows: ['Baris pertama', 'Baris kedua']};
  });
  ENTRIES[7] = {label: 'Pelayanan Firman — Matius 5:1-8',
                rows: ['Matius 5:1', 'Matius 5:2', 'Matius 5:3', 'Matius 5:4', 'Matius 5:5', 'Matius 5:6']};
  ENTRIES[1] = {label: 'Nyanyian Pembuka — KJ 12 Hai Mari Berhimpun',
                baits: [['Bait 1', ['Hai mari berhimpun', 'semua umat Tuhan']],
                        ['Bait 2', ['Bersoraklah bersama', 'memuji nama-Nya']]]};
  ENTRIES[21] = {label: 'Pelayanan Firman — Matius 5:1-8',
                 rows: ['Matius 5:1', 'Matius 5:2', 'Matius 5:3', 'Matius 5:4', 'Matius 5:5', 'Matius 5:6']};
  var LIVE_ENTRY = 21;         /* deep enough that the row can leave either end of the pane */
  var LIVE_SCREEN = 3;         /* its fourth row */

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function chevron() {
    var chev = el('span', 'entrychev');
    chev.setAttribute('aria-hidden', 'true');
    chev.innerHTML = '<svg viewBox="0 0 20 20"><polyline points="7 4 13 10 7 16"/></svg>';
    return chev;
  }

  function rowButton(entry, index) {
    var row = el('button', 'entryrow');
    row.type = 'button';
    row.tabIndex = -1;
    row.dataset.index = String(index);
    row.setAttribute('aria-current', 'false');
    row.appendChild(el('span', 'entryrow__c', String(index + 1)));
    row.appendChild(el('span', 'entryrow__t', entry.label));
    return row;
  }

  function buildInner(entry, index) {
    var inner = el('div', 'entryinner');
    inner.id = 'entryinner-' + index;
    inner.setAttribute('aria-hidden', 'true');
    var clip = el('div', 'entryinner__clip');
    var body = el('div', 'entryinner__body');
    var groups = entry.baits
      ? entry.baits.map(function (b) { return {head: b[0], rows: b[1]}; })
      : [{head: null, rows: entry.rows}];
    groups.forEach(function (group) {
      if (group.head) body.appendChild(el('div', 'baithead', group.head));
      group.rows.forEach(function (text) {
        var btn = el('button', 'screenerow', null);
        btn.type = 'button';
        btn.tabIndex = -1;
        btn.setAttribute('aria-current', 'false');
        var wrap = el('span', 'screenerow__t--lines');
        wrap.appendChild(el('span', 'screenerow__line', text));
        btn.appendChild(wrap);
        body.appendChild(btn);
      });
    });
    if (!body.children.length) return null;
    clip.appendChild(body);
    inner.appendChild(clip);
    return inner;
  }

  var nextBand = el('button', 'nextband');
  nextBand.type = 'button';
  nextBand.tabIndex = -1;
  nextBand.appendChild(el('span', 'nextband__cap', 'Next'));
  var nextLabel = el('span', 'nextband__label', '');
  nextBand.appendChild(nextLabel);

  ENTRIES.forEach(function (entry, index) {
    var li = el('li', 'entryli');
    li.dataset.index = String(index);
    li.appendChild(rowButton(entry, index));
    var inner = buildInner(entry, index);
    li.appendChild(inner);
    li.querySelector('.entryrow').setAttribute('aria-controls', inner.id);
    entryList.appendChild(li);
  });

  /* ---------- where the run stands ----------------------------------------- */

  function liOf(index) { return entryList.querySelector('.entryli[data-index="' + index + '"]'); }

  function paint(liveEntry, liveScreen) {
    entryList.querySelectorAll('.entryli').forEach(function (li) {
      var index = Number(li.dataset.index);
      var isLive = index === liveEntry;
      li.dataset.live = isLive ? 'true' : 'false';
      var row = li.querySelector('.entryrow');
      row.setAttribute('aria-current', isLive ? 'true' : 'false');
      var chev = li.querySelector('.entrychev');
      if (chev) chev.remove();
      if (!isLive) row.appendChild(chevron());
      var inner = li.querySelector('.entryinner');
      inner.classList.toggle('is-open', isLive || openByHand.indexOf(index) >= 0);
      var open = inner.classList.contains('is-open');
      inner.setAttribute('aria-hidden', open ? 'false' : 'true');
      if ('inert' in inner) inner.inert = !open;
      var screens = li.querySelectorAll('.screenerow');
      screens.forEach(function (s, i) {
        s.setAttribute('aria-current', (isLive && i === liveScreen) ? 'true' : 'false');
      });
    });
    var liveLi = liOf(liveEntry);
    liveLi.appendChild(nextBand);
    var next = ENTRIES[liveEntry + 1];
    nextBand.hidden = !next;
    nextLabel.textContent = next ? next.label : '';
  }

  var openByHand = [];
  var following = true;                 /* the dock starts following, as it does today */

  /* A flat step list so the preview's Previous/Next can cross entry boundaries. */
  var SCREENS = [];
  ENTRIES.forEach(function (entry, ei) {
    var count = entry.baits
      ? entry.baits.reduce(function (n, bait) { return n + bait[1].length; }, 0)
      : entry.rows.length;
    for (var i = 0; i < count; i++) SCREENS.push({entry: ei, row: i});
  });
  var livePos = SCREENS.findIndex(function (s) {
    return s.entry === LIVE_ENTRY && s.row === LIVE_SCREEN;
  });

  function syncLivePos() {
    var ei = Number(entryList.querySelector('.entryli[data-live="true"]').dataset.index);
    var row = entryList.querySelector('.screenerow[aria-current="true"]');
    var ri = row ? Array.prototype.indexOf.call(row.closest('.entryli').querySelectorAll('.screenerow'), row) : 0;
    livePos = SCREENS.findIndex(function (s) { return s.entry === ei && s.row === ri; });
  }

  function snapBlocks() {
    /* The product's crossing morph owns both block heights on one curve, so the
       arriving row's layout is settled when the scroll is derived. The preview
       snaps the blocks instead (no second motion) so its centring lands true. */
    var inners = entryList.querySelectorAll('.entryinner');
    inners.forEach(function (inner) {
      inner.classList.add('is-morph');
      inner.style.gridTemplateRows = inner.classList.contains('is-open') ? '1fr' : '0fr';
    });
    window.setTimeout(function () {
      inners.forEach(function (inner) {
        inner.classList.remove('is-morph');
        inner.style.gridTemplateRows = '';
      });
    }, 260);
  }

  function advance(dir) {
    var to = Math.max(0, Math.min(SCREENS.length - 1, livePos + dir));
    if (to === livePos) return;
    livePos = to;
    var s = SCREENS[livePos];
    paint(s.entry, s.row);
    snapBlocks();
    if (following) centre('an advance while following');
    else say('advanced while browsing — the list stayed put');
  }

  function liveRow() {
    return entryList.querySelector('.screenerow[aria-current="true"]') ||
           entryList.querySelector('.entryrow[aria-current="true"]');
  }

  /* ---------- the centring (the dock's own maths) -------------------------- */

  var glideFrame = null;

  function layoutTop(node) {
    if (node.classList.contains('entryrow')) {
      var li = node.closest('.entryli');
      if (li) return li.offsetTop;
    }
    return node.offsetTop;
  }

  function glide(target) {
    if (glideFrame) { cancelAnimationFrame(glideFrame); glideFrame = null; }
    var from = runBody.scrollTop;
    var started = performance.now();
    function frame(now) {
      var max = runBody.scrollHeight - runBody.clientHeight;
      var to = Math.max(0, Math.min(target, max));
      var t = Math.min(1, (now - started) / 190);
      runBody.scrollTop = from + (to - from) * (1 - Math.pow(1 - t, 5));
      glideFrame = t < 1 ? requestAnimationFrame(frame) : null;
    }
    glideFrame = requestAnimationFrame(frame);
  }

  function centre(reason) {
    var node = liveRow();
    if (!node) { say('nothing live to centre'); return; }
    var target = layoutTop(node) - (runBody.clientHeight - node.offsetHeight) / 2;
    glide(target);
    say('centred — ' + reason);
  }

  /* ---------- the three triggers ------------------------------------------- */

  centreBtn.addEventListener('click', function () {
    following = true;                   /* a re-entry: advances follow from here on */
    centre('the control');
  });

  entryList.addEventListener('click', function (event) {
    var item = event.target.closest('.screenerow');
    var band = event.target.closest('.nextband');
    if (!item && !band) return;                      /* a header only toggles its block */
    if (band) {
      /* The band's screen belongs to the NEXT ENTRY, not the next screen of this one. */
      var cur = Number(entryList.querySelector('.entryli[data-live="true"]').dataset.index);
      var nextEntry = Math.min(ENTRIES.length - 1, cur + 1);
      var at = SCREENS.findIndex(function (s) { return s.entry === nextEntry; });
      if (at >= 0) {
        livePos = at;
        paint(SCREENS[at].entry, SCREENS[at].row);
      }
    } else {
      var li = item.closest('.entryli');
      var screens = li.querySelectorAll('.screenerow');
      paint(Number(li.dataset.index), Array.prototype.indexOf.call(screens, item));
    }
    syncLivePos();
    snapBlocks();
    following = true;                                /* an item click is a re-entry */
    centre(band ? 'the Next band' : 'an item click');
  });

  entryList.addEventListener('click', function (event) {
    var row = event.target.closest('.entryrow');
    if (!row || event.target.closest('.screenerow')) return;
    var index = Number(row.dataset.index);
    var at = openByHand.indexOf(index);
    if (at >= 0) openByHand.splice(at, 1); else openByHand.push(index);
    if (at < 0) { following = false; say('browsing — another entry was expanded'); }
    paint(Number(entryList.querySelector('.entryli[data-live="true"]').dataset.index),
          currentScreen());
  });

  function currentScreen() {
    var row = entryList.querySelector('.screenerow[aria-current="true"]');
    if (!row) return 0;
    return Array.prototype.indexOf.call(row.closest('.entryli').querySelectorAll('.screenerow'), row);
  }

  /* ---------- the idle clock ----------------------------------------------- */

  var IDLE = Number(new URLSearchParams(location.search).get('idle')) || 15000;
  var lastActivity = performance.now();
  var holding = false;

  /* What counts as activity: a scroll, a press (a click, or a press held down —
     dragging included) and a key. Plain pointer MOVEMENT does not count: a pointer
     travelling across the dock is an operator doing nothing to it. */
  ['wheel', 'pointerdown', 'pointerup', 'pointercancel', 'keydown'].forEach(function (name) {
    document.addEventListener(name, function (event) {
      if (event.type === 'pointerdown') holding = true;
      if (event.type === 'pointerup' || event.type === 'pointercancel') holding = false;
      lastActivity = performance.now();
    }, {passive: true});
  });

  function offScreen(node) {
    var box = runBody.getBoundingClientRect();
    var r = node.getBoundingClientRect();
    return r.bottom <= box.top || r.top >= box.bottom;
  }

  function conditions() {
    var live = entryList.querySelector('.entryli[data-live="true"]');
    if (document.getElementById('dockPanel').dataset.view !== 'run') return 'the picker is the view';
    if (!cb.browsed.checked) return 'another service is open in the dock';
    if (!cb.live.checked) return 'the words are hidden';
    if (cb.layer.checked) return 'a layer is open';
    if (cb.other.checked) return 'another header is open';
    var node = liveRow();
    if (!node || !offScreen(node)) return 'the live row is still on screen';
    return null;
  }

  var lastSay = '';
  function say(text) { lastSay = text; log.textContent = text; }

  setInterval(function () {
    var now = performance.now();
    if (holding) lastActivity = now;              /* a held button is not idleness */
    var left = Math.max(0, (IDLE - (now - lastActivity)) / 1000);
    clockOut.textContent = left.toFixed(1) + ' s' + (holding ? ' (held)' : '');
    var row = liveRow();
    var box = runBody.getBoundingClientRect();
    var r = row ? row.getBoundingClientRect() : null;
    var off = r ? ((r.top + r.bottom) / 2) - ((box.top + box.bottom) / 2) : 0;
    var held = conditions();
    read.textContent = 'mode: ' + (following ? 'following' : 'browsing') +
      '\nscrollTop ' + Math.round(runBody.scrollTop) +
      ' · live row off centre ' + Math.round(off) + ' px' +
      '\nconditions: ' + (held ? 'held by — ' + held : 'all true');
    var modeOut = document.getElementById('pvMode');
    if (modeOut) modeOut.textContent = 'mode: ' + (following ? 'following' : 'browsing');
    var centre = document.getElementById('centreBtn');
    if (centre) centre.setAttribute('aria-pressed', following ? 'true' : 'false');
    if (cb.idleOn.checked && left === 0 && !held) {
      following = true;                 /* the idle re-centre is a re-entry */
      centre('15 s idle, every condition true');
      lastActivity = now;
    }
  }, 100);

  /* ---------- the page's own controls -------------------------------------- */

  document.getElementById('prevBtn').addEventListener('click', function () { advance(-1); });
  document.getElementById('nextBtn').addEventListener('click', function () { advance(1); });
  runBody.addEventListener('wheel', function () {
    following = false;
    say('browsing — a scroll ended following');
  }, {passive: true});

  document.getElementById('scrollAway').addEventListener('click', function () {
    runBody.scrollTop = runBody.scrollHeight;      /* the live entry ends up above the fold */
    following = false;                             /* the stand-in for a hand scroll */
    say('browsing — the live row is out of view');
  });
  document.getElementById('scrollBack').addEventListener('click', function () {
    var node = liveRow();
    if (node) runBody.scrollTop = Math.max(0, layoutTop(node) - 40);
    say('the live row is back in view');
  });
  cb.layer.addEventListener('change', function () {
    findScrim.hidden = !cb.layer.checked;
    findScrim.style.opacity = cb.layer.checked ? '1' : '';
    if (cb.layer.checked) { document.getElementById('findBand').classList.add('is-open'); }
    else { document.getElementById('findBand').classList.remove('is-open'); }
  });

  paint(LIVE_ENTRY, LIVE_SCREEN);
  runBody.scrollTop = 0;
})();
