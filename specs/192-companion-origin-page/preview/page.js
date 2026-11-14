/* Config-page preview — the add/edit/delete grammar is the spec's FR-002, verbatim behaviour.
   Icons are inline SVG, stroke currentColor — the product's own icon convention. */

var ICON_EDIT = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.3 2.5a1.6 1.6 0 0 1 2.3 2.3L5.2 13.2l-3.1.9.9-3.1 8.3-8.5z"/></svg>';
var ICON_TRASH = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 4h11M5.5 4V2.8a.8.8 0 0 1 .8-.8h3.4a.8.8 0 0 1 .8.8V4M4 4l.6 9.2a1 1 0 0 0 1 .8h4.8a1 1 0 0 0 1-.8L12 4"/></svg>';

var list = document.getElementById('list');
var empty = document.getElementById('empty');
var form = document.getElementById('addform');
var input = document.getElementById('origin');
var err = document.getElementById('err');

function load() {
  try { return JSON.parse(localStorage.getItem('gkps-preview-origins')) || []; }
  catch (e) { return []; }
}

function save() { localStorage.setItem('gkps-preview-origins', JSON.stringify(recorded)); }
var recorded = load();

function showEmpty() { empty.hidden = recorded.length > 0; }
showEmpty();

function rules(t) {
  if (/\s/.test(t)) return 'an origin is one line with no spaces';
  if (!/^https?:\/\//.test(t)) return 'an origin starts with its scheme — http:// or https://';
  if (t.indexOf('@') !== -1) return 'an origin carries no credentials — no @';
  var rest = t.slice(t.indexOf('://') + 3);
  if (/[\/?#]/.test(rest)) return 'an origin carries no path, query or trailing slash';
  var host, port = '';
  if (rest.charAt(0) === '[') {
    var close = rest.indexOf(']');
    if (close === -1) return 'an origin needs a hostname after the scheme';
    host = rest.slice(0, close + 1);
    if (rest.charAt(close + 1) === ':') port = rest.slice(close + 2);
    else if (rest.length > close + 1) return 'an origin carries no path, query or trailing slash';
  } else {
    var c = rest.lastIndexOf(':');
    if (c !== -1) { host = rest.slice(0, c); port = rest.slice(c + 1); } else host = rest;
  }
  if (!host) return 'an origin needs a hostname after the scheme';
  if (port && !/^\d{1,5}$/.test(port)) return 'an origin needs a numeric port in range';
  if (port && parseInt(port, 10) > 65535) return 'an origin needs a numeric port in range';
  return '';
}

function showErr(text) {
  err.textContent = text;
  err.hidden = false;
  input.classList.add('is-invalid');
}

function clearErr() {
  err.hidden = true;
  input.classList.remove('is-invalid');
}

function actButton(cls, icon, label, fn) {
  var b = document.createElement('button');
  b.type = 'button';
  b.className = 'row__act ' + cls;
  b.title = label;
  b.setAttribute('aria-label', label);
  b.innerHTML = icon;
  b.addEventListener('click', fn);
  return b;
}

function render() {
  list.textContent = '';
  showEmpty();
  recorded.forEach(function (o, i) {
    var li = document.createElement('li');
    li.className = 'row';
    var origin = document.createElement('span');
    origin.className = 'row__origin';
    origin.textContent = o;
    li.appendChild(origin);
    li.appendChild(actButton('row__act--edit', ICON_EDIT, 'Edit', function () { startEdit(li, i); }));
    li.appendChild(actButton('row__act--danger', ICON_TRASH, 'Delete', function () {
      recorded.splice(i, 1);
      save();
      render();
    }));
    list.appendChild(li);
  });
}

function startEdit(li, i) {
  render();
  var row = list.children[i];
  row.innerHTML = '';
  var field = document.createElement('input');
  field.className = 'row__field';
  field.value = recorded[i];
  row.appendChild(field);
  var confirm = document.createElement('button');
  confirm.type = 'button';
  confirm.className = 'btn-confirm';
  confirm.textContent = 'Confirm';
  confirm.addEventListener('click', function () { commitEdit(i, field.value); });
  var discard = document.createElement('button');
  discard.type = 'button';
  discard.className = 'btn-discard';
  discard.textContent = 'Discard';
  discard.addEventListener('click', render);
  row.appendChild(confirm);
  row.appendChild(discard);
  field.focus();
  field.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') commitEdit(i, field.value);
    if (e.key === 'Escape') render();
  });
}

function commitEdit(i, value) {
  var field = list.querySelector('.row__field');
  var t = value.replace(/^\s+|\s+$/g, '');
  var rule = rules(t);
  if (rule) {
    showErr(rule);
    if (field) field.classList.add('is-invalid');
    return;
  }
  if (recorded.some(function (o, j) { return j !== i && o === t; })) {
    showErr('that origin is already recorded');
    if (field) field.classList.add('is-invalid');
    return;
  }
  recorded[i] = t;
  save();
  render();
}

form.addEventListener('submit', function (e) {
  e.preventDefault();
  var t = input.value.replace(/^\s+|\s+$/g, '');
  var rule = rules(t);
  if (rule) { showErr(rule); return; }
  if (recorded.indexOf(t) !== -1) { showErr('that origin is already recorded'); return; }
  recorded.push(t);
  save();
  input.value = '';
  clearErr();
  render();
});

// A pointer press outside the editing row discards the unconfirmed edit.
document.addEventListener('pointerdown', function (e) {
  var field = list.querySelector('.row__field');
  if (!field || field.closest('.row').contains(e.target)) return;
  render();
});

render();
