(function () {
  var NOTES = {
    edit: 'The Edit Tata Ibadah dialog, as the server sends it — Copy as template sits in the header.',
    confirm: 'The confirmation as a dialog of its own: its scrim reaches every edge of the window, the Edit dialog stays open and dimmed behind it, and the name the copy is saved under is editable. Clicking the name selects all of it, so typing replaces it.'
  };

  var dialog = document.querySelector('.pv__dialog');
  var layer = document.querySelector('[data-copy-confirm]');
  var nameInput = layer.querySelector('[data-copy-name]');
  var accept = layer.querySelector('[data-copy-accept]');
  var note = document.querySelector('[data-note]');
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-state]'));
  var themeBtn = document.querySelector('[data-theme-toggle]');
  var sizeBtn = document.querySelector('[data-size-toggle]');
  var serviceEl = document.querySelector('[data-fragment="service"]');
  var templateEl = document.querySelector('[data-fragment="template"]');
  var current = 'edit';

  /* a static page has no server: the form must not navigate away */
  document.addEventListener('submit', function (event) { event.preventDefault(); });

  /* Clicking the name selects all of it, so the first click is immediately
     replaceable. The mouseup that follows would collapse the selection again,
     hence the guard; a later click inside the field places a caret as usual. */
  var selectOnFocus = true;
  nameInput.addEventListener('focus', function () { if (selectOnFocus) nameInput.select(); });
  nameInput.addEventListener('mouseup', function (event) {
    if (!selectOnFocus) return;
    event.preventDefault();
    selectOnFocus = false;
  });
  nameInput.addEventListener('blur', function () { selectOnFocus = true; });

  function syncAccept() { accept.disabled = nameInput.value.trim() === ''; }
  nameInput.addEventListener('input', syncAccept);

  function paint() {
    layer.hidden = current !== 'confirm';
    tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.dataset.state === current)); });
    note.textContent = NOTES[current];
    syncAccept();
  }

  function open() {
    current = 'confirm';
    selectOnFocus = true;
    paint();
    accept.focus();
  }

  function close() {
    current = 'edit';
    paint();
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      if (t.dataset.state === 'confirm') open(); else close();
    });
  });

  document.addEventListener('click', function (event) {
    if (event.target.closest('[data-copy-open]')) { open(); return; }
    if (event.target.closest('[data-copy-cancel]')) { close(); return; }
    if (event.target === layer) close();      /* the scrim */
  });

  document.addEventListener('keydown', function (event) {
    /* the shortcuts are harness chrome: typing a name must not switch states */
    if (event.target.closest('input, textarea, select') && event.key !== 'Escape') return;
    if (event.key === 'Escape' && current === 'confirm') { event.preventDefault(); close(); }
    if (event.key === '1') close();
    if (event.key === '2') open();
    if (event.key === 't') themeBtn.click();
    if (event.key === 's') sizeBtn.click();
  });

  sizeBtn.addEventListener('click', function () {
    var showTemplate = templateEl.hidden;
    templateEl.hidden = !showTemplate;
    serviceEl.hidden = showTemplate;
    sizeBtn.textContent = showTemplate ? 'Template dialog' : 'Service dialog';
    dialog.style.height = '';
  });

  themeBtn.addEventListener('click', function () {
    var next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    themeBtn.textContent = next === 'dark' ? 'Dark' : 'Light';
  });

  paint();
})();
