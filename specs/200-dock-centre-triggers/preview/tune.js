/* Tuning harness behaviour. Each pane replays the dock's own glide maths:
   drive the live row's own offset to zero on the chosen curve, sampled per
   animation frame. No recording — motion is watched live, at 1x or slowed. */
(function () {
  'use strict';

  var EASES = {
    out1_3: function (t) { return 1 - Math.pow(1 - t, 1.3); },
    out2:   function (t) { return 1 - Math.pow(1 - t, 2); },
    out3:   function (t) { return 1 - Math.pow(1 - t, 3); },
    inout:  function (t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; },
    smooth: function (t) { return t * t * (3 - 2 * t); },
    sin:    function (t) { return .5 - Math.cos(Math.PI * t) / 2; },
    linear: function (t) { return t; }
  };
  var EASE_LABELS = [
    ['out1_3', 'ease-out 1.3 (current)'], ['out2', 'ease-out 2'],
    ['out3', 'ease-out 3'], ['inout', 'ease-in-out (quad)'],
    ['smooth', 'smoothstep'], ['sin', 'sine in-out'], ['linear', 'linear']
  ];
  var PRESETS = {
    current: {dur: 190, ease: 'out1_3', label: 'current 190'},
    brisk:   {dur: 260, ease: 'out3',   label: 'brisk 260'},
    gentle:  {dur: 320, ease: 'out2',   label: 'gentle 320'},
    smooth:  {dur: 400, ease: 'sin',    label: 'smooth 400'},
    slow:    {dur: 500, ease: 'out2',   label: 'slow 500'}
  };
  var LIVE = 12;
  var NAMES = [
    'Pembuka', 'Nyanyian Pembuka — KJ 12', 'Doa Pembukaan', 'Mazmur 100',
    'Nyanyian — KJ 285', 'Persembahan', 'Nyanyian Persembahan — KJ 336',
    'Matius 5:1-8', 'Nyanyian Firman — KJ 400', 'Pengakuan Iman', 'Doa Syafaat',
    'Nyanyian — KJ 425', 'Pelayanan Firman — Matius 5:9-12', 'Doxology',
    'Berkat', 'Pengutusan', 'Nyanyian Penutup — KJ 500', 'Doa Penutup'
  ];
  var SCREENS = ['Baris pertama', 'Baris kedua', 'Baris ketiga', 'Baris keempat'];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function buildList(ul) {
    NAMES.forEach(function (label, index) {
      var li = el('li', 'entryli');
      li.dataset.index = String(index);
      li.dataset.live = index === LIVE ? 'true' : 'false';
      var row = el('button', 'entryrow');
      row.type = 'button'; row.tabIndex = -1;
      row.setAttribute('aria-current', index === LIVE ? 'true' : 'false');
      row.appendChild(el('span', 'entryrow__c', String(index + 1)));
      row.appendChild(el('span', 'entryrow__t', label));
      li.appendChild(row);
      if (index === LIVE || index === LIVE - 1) {
        var inner = el('div', 'entryinner is-open');
        var clip = el('div', 'entryinner__clip');
        var body = el('div', 'entryinner__body');
        SCREENS.forEach(function (text, i) {
          var r = el('button', 'screenerow');
          r.type = 'button'; r.tabIndex = -1;
          r.dataset.live = index === LIVE && i === 1 ? 'true' : 'false';
          r.appendChild(el('span', 'screenerow__t--lines'));
          r.lastChild.appendChild(el('span', 'screenerow__line', text));
          body.appendChild(r);
        });
        clip.appendChild(body); inner.appendChild(clip); li.appendChild(inner);
      }
      ul.appendChild(li);
    });
  }

  function liveRow(body) {
    return body.querySelector('.entryli[data-live="true"] > .entryrow');
  }

  function offset(body) {
    var row = liveRow(body);
    return row.getBoundingClientRect().top + row.getBoundingClientRect().height / 2
      - body.getBoundingClientRect().top - body.clientHeight / 2;
  }

  function make(side, preset) {
    var state = {side: side, dur: preset.dur, ease: preset.ease, frames: [], raf: 0, started: 0};
    var controls = document.querySelector('[data-controls="' + side + '"]');
    var range = el('input'); range.type = 'range'; range.min = '120'; range.max = '700';
    range.step = '10'; range.value = String(preset.dur);
    var out = el('span', '', preset.dur + ' ms');
    var durField = el('label', 'tune__field');
    durField.appendChild(document.createTextNode('duration'));
    var line = el('span'); line.appendChild(range); line.appendChild(out);
    durField.appendChild(line);
    var easeField = el('label', 'tune__field');
    easeField.appendChild(document.createTextNode('easing'));
    var select = el('select');
    EASE_LABELS.forEach(function (pair) {
      var opt = el('option', '', pair[1]); opt.value = pair[0]; select.appendChild(opt);
    });
    select.value = preset.ease;
    easeField.appendChild(select);
    controls.appendChild(durField); controls.appendChild(easeField);
    range.addEventListener('input', function () {
      state.dur = Number(range.value); out.textContent = state.dur + ' ms';
    });
    select.addEventListener('change', function () { state.ease = select.value; });

    var chips = el('div', 'tune__chips');
    Object.keys(PRESETS).forEach(function (key) {
      var chip = el('button', 'tune__chip', PRESETS[key].label);
      chip.type = 'button';
      if (key === (side === 'A' ? 'current' : 'smooth')) chip.classList.add('is-on');
      chip.addEventListener('click', function () {
        state.dur = PRESETS[key].dur; state.ease = PRESETS[key].ease;
        range.value = String(state.dur); out.textContent = state.dur + ' ms';
        select.value = state.ease;
        chips.querySelectorAll('.tune__chip').forEach(function (c) { c.classList.remove('is-on'); });
        chip.classList.add('is-on');
        reset(state);
      });
      chips.appendChild(chip);
    });
    controls.parentNode.insertBefore(chips, controls.nextSibling);

    state.body = document.querySelector('[data-body="' + side + '"]');
    state.read = document.querySelector('[data-read="' + side + '"]');
    state.trace = document.querySelector('[data-trace="' + side + '"]');
    buildList(state.body.querySelector('ul'));
    reset(state);
    return state;
  }

  function reset(s) {
    if (s.raf) cancelAnimationFrame(s.raf);
    s.raf = 0; s.frames = [];
    s.body.scrollTop = 0;   /* live row starts below the pane, as in the dock probe */
    s.read.textContent = 'ready · ' + s.dur + ' ms · ' +
      (EASE_LABELS.filter(function (p) { return p[0] === s.ease; })[0] || [,'?'])[1];
    s.trace.innerHTML = '';
  }

  function trace(s) {
    var peak = 1;
    s.frames.forEach(function (f) { peak = Math.max(peak, f.v); });
    var points = s.frames.map(function (f, i) {
      var x = 300 * (i / Math.max(1, s.frames.length - 1));
      var y = 42 - 40 * (f.v / peak);
      return x.toFixed(1) + ',' + y.toFixed(1);
    }).join(' ');
    var poly = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    poly.setAttribute('points', points);
    poly.setAttribute('fill', 'none');
    poly.setAttribute('stroke', s.side === 'A' ? '#7c9cf0' : '#e0a458');
    poly.setAttribute('stroke-width', '2');
    s.trace.appendChild(poly);
  }

  function play(s, factor) {
    if (s.raf) cancelAnimationFrame(s.raf);
    s.frames = []; s.trace.innerHTML = '';
    var from = offset(s.body);
    var start = null;
    var last = null;
    var duration = s.dur * factor;
    var ease = EASES[s.ease];
    function frame(now) {
      if (start === null) { start = now; last = now; }
      var t = Math.min(1, (now - start) / duration);
      var want = from * (1 - ease(t));
      s.body.scrollTop += offset(s.body) - want;
      var dt = Math.max(1, now - last);
      var moved = Math.abs(s.body.scrollTop - (s.frames.length
        ? s.frames[s.frames.length - 1].top : s.body.scrollTop));
      s.frames.push({t: now - start, top: s.body.scrollTop, v: 1000 * moved / dt});
      last = now;
      var f = s.frames[s.frames.length - 1];
      s.read.textContent = 't=' + Math.round(f.t) + 'ms · top=' + Math.round(f.top) +
        ' · ' + Math.round(f.v) + 'px/s';
      if (t < 1) s.raf = requestAnimationFrame(frame);
      else {
        s.raf = 0;
        var tail = Math.round(Math.abs(offset(s.body)));
        s.read.textContent = 'settled ' + Math.round(duration) + 'ms · ' +
          s.frames.length + ' frames · ' + tail + 'px off';
        trace(s);
      }
    }
    s.raf = requestAnimationFrame(frame);
  }

  var factor = 1;
  var A = make('A', PRESETS.current);
  var B = make('B', PRESETS.smooth);
  document.getElementById('distOut').textContent =
    'one move ≈ ' + Math.round(Math.abs(offset(B.body))) + ' px';

  document.getElementById('playBoth').addEventListener('click', function () {
    reset(A); reset(B);
    setTimeout(function () { play(A, factor); play(B, factor); }, 120);
  });
  document.getElementById('resetBoth').addEventListener('click', function () {
    reset(A); reset(B);
  });
  document.querySelectorAll('.tune__seg').forEach(function (btn) {
    btn.addEventListener('click', function () {
      factor = Number(btn.dataset.speed);
      document.querySelectorAll('.tune__seg').forEach(function (b) {
        b.classList.toggle('is-on', b === btn);
      });
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.target.matches('input, select')) return;
    if (e.code === 'Space') { e.preventDefault(); document.getElementById('playBoth').click(); }
    if (e.key === 'r' || e.key === 'R') document.getElementById('resetBoth').click();
  });
})();
