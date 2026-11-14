/* Spec 138 prototype — the drawer shell's behaviour, on the real page.
   The page's own scripts are stripped by the builder, so this file owns
   data-nav / data-ch / data-rail and nothing else touches them.

   Model: level 0 is the rail (a drawer only on a phone), level 1 the section's
   list, level 2 the chapter or song list. Level 2 covers level 1 completely and
   slides out from under the rail; a sibling level never opens beside it. */
(function () {
  var root = document.documentElement;
  var state = {
    overlayMax: 1272,
    phoneMax: 720,
  };

  var panel = document.getElementById('panel');
  var chapters = document.getElementById('chapters');
  var rail = document.querySelector('.rail');

  /* ---------- the geometry, from the window width ---------- */
  function applyThresholds() {
    var w = window.innerWidth;
    var overlay = w <= state.overlayMax;
    root.dataset.mode = overlay ? 'overlay' : 'columns';
    root.dataset.phone = (overlay && w <= state.phoneMax) ? 'yes' : 'no';
    if (!overlay) closeAll(false);          /* the columns have no stack to keep */
    if (root.dataset.phone !== 'yes') root.dataset.rail = 'closed';
    placeFoot();
    sync();
  }

  /* ---------- per-section memory ---------- */
  var perSection = {};
  function currentSection() { return root.dataset.section || 'tatib'; }
  function rememberLevel(level) { perSection[currentSection()] = level; }
  function rememberedLevel() { return perSection[currentSection()] || 1; }

  /* ---------- the stack ---------- */
  function openRail() {
    root.dataset.rail = 'open';
    root.dataset.nav = 'closed';
    root.dataset.ch = 'closed';
    sync();
  }
  function openLevel1(fromMenu) {
    /* on a phone the menu stays open underneath, so the list slides over it */
    root.dataset.rail = (fromMenu && root.dataset.phone === 'yes') ? 'open' : 'closed';
    root.dataset.nav = 'open';
    root.dataset.ch = 'closed';
    rememberLevel(1);
    sync();
  }
  function level2Exists() {
    /* a service's contents list only jumps into the page it already sits on, so
       a phone never offers it */
    return !(root.dataset.phone === 'yes' && currentSection() === 'tatib');
  }
  function openLevel2() {
    if (!level2Exists()) return;
    root.dataset.rail = 'closed';
    root.dataset.nav = 'open';
    root.dataset.ch = 'open';
    rememberLevel(2);
    sync();
  }
  function restoreLast() {
    if (!isOverlay()) { openRail(); return; }
    if (rememberedLevel() === 2) openLevel2(); else openLevel1();
  }
  function closeLevel2() {
    root.dataset.ch = 'closed';
    rememberLevel(1);
    sync();
  }
  function closeAll(andSync) {
    root.dataset.nav = 'closed';
    root.dataset.ch = 'closed';
    root.dataset.rail = 'closed';
    if (andSync !== false) sync();
  }
  function isOverlay() { return root.dataset.mode === 'overlay'; }
  function anyOpen() {
    return root.dataset.nav === 'open' || root.dataset.ch === 'open' || root.dataset.rail === 'open';
  }

  /* ---------- the backdrop ---------- */
  var backdrop = document.createElement('div');
  backdrop.className = 'proto-backdrop';
  backdrop.setAttribute('aria-hidden', 'true');
  document.body.appendChild(backdrop);
  backdrop.addEventListener('click', function () { closeAll(); });

  /* ---------- the phone toolbar ---------- */
  var ICON = {
    menu: '<path d="M3.5 6.5h17M3.5 12h17M3.5 17.5h17"/>',
    back: '<path d="M20 12H4.5"/><path d="m10.5 5.5-6 6.5 6 6.5"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>',
  };

  var toolbar = document.createElement('header');
  toolbar.className = 'proto-toolbar';
  toolbar.setAttribute('aria-label', 'Site');
  toolbar.innerHTML =
    '<button class="proto-toolbar__control" type="button" data-icon="menu" aria-label="Open the menu">' +
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ' +
    'stroke-linecap="round" stroke-linejoin="round">' + ICON.menu + '</svg></button>' +
    '<a class="proto-toolbar__logo" href="#" aria-label="GKPS Klender">' +
    '<img src="../../../static/assets/gkps.png" alt="" width="34" height="34"></a>' +
    '<span class="proto-toolbar__title"></span>' +
    '<span class="proto-toolbar__spacer"></span>' +
    '<div class="proto-toolbar__right"></div>';
  document.body.appendChild(toolbar);

  var control = toolbar.querySelector('.proto-toolbar__control');
  /* one control, two glyphs: open the menu, or close whatever is open. Going
     back one level is each drawer's own back control. */
  control.addEventListener('click', function () {
    if (anyOpen()) { closeAll(); return; }
    openRail();
  });
  toolbar.querySelector('.proto-toolbar__logo').addEventListener('click', function (e) {
    e.preventDefault();          /* a mark, not a control, in this prototype */
  });

  /* the rail's foot (transfer progress and the theme) lives in the toolbar on a
     phone and in the rail everywhere else */
  var railFoot = rail.querySelector('.rail__foot');
  var footHost = toolbar.querySelector('.proto-toolbar__right');
  function placeFoot() {
    if (!railFoot) return;
    if (root.dataset.phone === 'yes' && railFoot.parentElement !== footHost) {
      footHost.appendChild(railFoot);
    } else if (root.dataset.phone !== 'yes' && railFoot.parentElement !== rail) {
      rail.appendChild(railFoot);
    }
  }

  /* ---------- names for the rail drawer ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('.rail__menu .rail__btn'), function (btn) {
    if (btn.querySelector('.proto-label')) return;
    var label = document.createElement('span');
    label.className = 'proto-label';
    label.textContent = btn.getAttribute('data-tip') || btn.getAttribute('aria-label') || '';
    btn.appendChild(label);
  });

  /* ---------- the rail's sections ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('.rail__menu .rail__btn'), function (btn) {
    btn.addEventListener('click', function (event) {
      if (!isOverlay()) return;              /* above the breakpoint the page keeps its own links */
      event.preventDefault();
      if (root.dataset.rail === 'open') { openLevel1(true); return; }
      if (root.dataset.nav === 'open' || root.dataset.ch === 'open') { openLevel1(true); return; }
      restoreLast();
    });
  });

  /* A row in level 1: on a tablet it opens level 2; on a phone a Tata Ibadah row
     opens the page it names — the service's contents list is not offered there —
     so the drawer closes and the page is what is left. */
  if (panel) {
    panel.addEventListener('click', function (event) {
      if (!isOverlay()) return;
      var row = event.target.closest('.book, .songrow');
      if (!row) return;
      event.preventDefault();
      if (root.dataset.phone === 'yes' && currentSection() === 'tatib') { closeAll(); return; }
      openLevel2();
    });
  }

  /* the two collapse chevrons: one level each */
  var panelCollapse = document.getElementById('panelCollapse');
  if (panelCollapse) panelCollapse.addEventListener('click', function (e) {
    if (!isOverlay()) return;
    e.preventDefault(); e.stopPropagation();
    if (root.dataset.phone === 'yes' && root.dataset.rail === 'open') { root.dataset.nav = 'closed'; sync(); return; }
    closeAll();
  });
  var chCollapse = document.getElementById('chCollapse');
  if (chCollapse) chCollapse.addEventListener('click', function (e) {
    if (!isOverlay()) return;
    e.preventDefault(); e.stopPropagation();
    closeLevel2();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOverlay() && anyOpen()) { e.preventDefault(); closeAll(); }
  });

  /* ---------- readouts ---------- */
  function sync() {
    var icon = anyOpen() ? 'close' : 'menu';
    if (control.dataset.icon !== icon) {
      control.dataset.icon = icon;
      control.querySelector('svg').innerHTML = ICON[icon];
      control.setAttribute('aria-label',
        icon === 'close' ? 'Close the menu' : icon === 'back' ? 'Back' : 'Open the menu');
    }
    var name = { alkitab: 'Alkitab', kidung: 'Kidung', tatib: 'Tata Ibadah' }[root.dataset.section] || '';
    toolbar.querySelector('.proto-toolbar__title').textContent = name;
    if (readout) {
      readout.textContent = window.innerWidth + 'px · ' + root.dataset.mode +
        ' · levels ' + (root.dataset.rail === 'open' ? '0 ' : '') +
        (root.dataset.nav === 'open' ? '1 ' : '') + (root.dataset.ch === 'open' ? '2' : '');
    }
  }

  /* ---------- the inspector ---------- */
  var chip = document.createElement('button');
  chip.className = 'proto-chip';
  chip.type = 'button';
  chip.textContent = '⚙ prototype';
  document.body.appendChild(chip);

  var inspector = document.createElement('section');
  inspector.className = 'proto-panel';
  inspector.setAttribute('aria-label', 'Prototype controls');
  inspector.hidden = true;
  inspector.innerHTML =
    '<h2>Drawer prototype</h2>' +
    '<div class="proto-panel__row"><span>Overlay at</span><select data-k="overlay">' +
    '<option value="1272">≤ 1272px</option><option value="1024">≤ 1024px</option>' +
    '<option value="720">≤ 720px</option></select></div>' +
    '<div class="proto-panel__row"><span>Toolbar at</span><select data-k="phone">' +
    '<option value="720">≤ 720px</option><option value="560">≤ 560px</option>' +
    '<option value="425">≤ 425px</option></select></div>' +
    '<div class="proto-panel__row"><span>Page</span><select data-k="page">' +
    '<option value="prototype-tatib.html">Tata Ibadah</option>' +
    '<option value="prototype-songs.html">Kidung</option></select></div>' +
    '<div class="proto-panel__buttons">' +
    '<button type="button" data-do="l1">Level 1</button>' +
    '<button type="button" data-do="l2">Level 2</button>' +
    '<button type="button" data-do="close">Close</button></div>' +
    '<p class="proto-panel__readout" data-readout></p>';
  document.body.appendChild(inspector);
  var readout = inspector.querySelector('[data-readout]');

  chip.addEventListener('click', function () {
    inspector.hidden = !inspector.hidden;
    chip.hidden = !inspector.hidden;
  });
  inspector.querySelector('[data-k="overlay"]').value = String(state.overlayMax);
  inspector.querySelector('[data-k="phone"]').value = String(state.phoneMax);
  inspector.querySelector('[data-k="page"]').value = location.pathname.split('/').pop();

  inspector.addEventListener('change', function (event) {
    var key = event.target.getAttribute('data-k');
    if (!key) return;
    if (key === 'page') { location.href = event.target.value; return; }
    state[key === 'phone' ? 'phoneMax' : 'overlayMax'] = Number(event.target.value);
    if (state.phoneMax > state.overlayMax) state.phoneMax = state.overlayMax;
    applyThresholds();
  });
  inspector.addEventListener('click', function (event) {
    var action = event.target.getAttribute('data-do');
    if (action === 'l1') openLevel1();
    if (action === 'l2') openLevel2();
    if (action === 'close') closeAll();
  });

  window.addEventListener('resize', applyThresholds);
  applyThresholds();
})();
