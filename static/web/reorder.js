/* Reordering a service order (spec 006, slice 3).
 *
 * The order is changed in the PAGE and shown at once -- in the pane and in the sidebar's
 * contents list -- but nothing is saved until Save; Discard puts back what was there.
 * While the mode is on the pane's add controls are gone (there is one thing to do), and
 * leaving with unsaved changes asks first: the shell's own in-page navigation is
 * intercepted through navigate() in reading.js, and a tab close through beforeunload.
 *
 * Everything is DELEGATED and resolved from the document on each use: the shell swaps the
 * reading pane in place, so a handler bound to the nodes at load time is bound to nothing
 * after the first swap.
 *
 * One unit is a section AND the add row that follows it: the add row is anchored to the
 * item it follows, so moving one without the other would leave a later add pointing at the
 * wrong place.
 */
(function () {
  'use strict';

  function group() { return document.querySelector('[data-reorder-group]'); }
  function pane() { return document.getElementById('readBody'); }
  function list() { return document.getElementById('chList'); }

  var on = false;                 /* the reorder mode */
  var origin = [];                /* the order it had when the mode was entered */
  var nodes = {};                 /* pk -> that entry's own nodes, as read */
  var pending = null;             /* what to run once a guarded question is answered */
  var drag = null;
  var swallow = false;            /* the click that follows a drag, to be swallowed */

  function sections() {
    var body = pane();
    return body ? [].slice.call(body.querySelectorAll('section[data-entry-pk]')) : [];
  }
  function pkOf(section) { return Number(section.dataset.entryPk); }
  function unitOf(section) {
    var unit = [section];
    var next = section.nextElementSibling;
    if (next && next.classList.contains('entry__add')) unit.push(next);
    return unit;
  }
  function order() { return sections().map(pkOf); }
  function node(pk) { return pane() && pane().querySelector('section[data-entry-pk="' + pk + '"]'); }

  function changed() {
    var now = order();
    return now.length !== origin.length || now.some(function (pk, index) {
      return pk !== origin[index];
    });
  }

  /* Read the pane: which entry is which, and the order they are in now. */
  function read() {
    nodes = {};
    var order = [];
    sections().forEach(function (section) {
      var pk = pkOf(section);
      nodes[pk] = unitOf(section);
      order.push(pk);
    });
    return order;
  }

  /* Put the pane into a given order. Re-appending moves the existing nodes, so the
     markup, the handlers and every anchor stay as they are. The entries are the last
     thing in the pane, so appending lands them in the right place. */
  function applyOrder(what) {
    var body = pane();
    if (!body) return;
    what.forEach(function (pk) {
      (nodes[pk] || []).forEach(function (each) { body.appendChild(each); });
    });
  }

  /* The sidebar's contents list follows the drag immediately. Its own numbers are the
     server's item numbers, so they are renumbered here to match -- the numbers the
     sidebar would show once this order is saved. */
  function preview(what) {
    var rows = list();
    if (!rows) return;
    var others = [].slice.call(rows.querySelectorAll('a[data-i]')).filter(function (row) {
      return !/^e\d+$/.test(row.dataset.i);
    }).map(function (row) { return Number(row.dataset.num) || 0; });
    var base = others.length ? Math.max.apply(null, others) : 0;
    what.forEach(function (pk, index) {
      var row = rows.querySelector('a[data-i="e' + pk + '"]');
      if (!row) return;
      var item = row.closest('li');
      rows.appendChild(item);                       /* the entries are the last rows */
      var cell = row.querySelector('.songrow__c');
      if (cell) cell.textContent = String(base + index + 1);
    });
  }

  function status(message) {
    var line = document.querySelector('[data-reorder-status]');
    if (line) line.textContent = message || '';
  }

  /* ---------- the mode ------------------------------------------------------- */

  function enter() {
    var g = group();
    if (!g || on) return;
    if (window.gkpsDisplay && window.gkpsDisplay.locked()) {
      window.gkpsDisplay.refuse();                  /* the display owns the order */
      return;
    }
    origin = read();
    if (!origin.length) return;
    on = true;
    /* ONE state attribute, and on the PANE: the toolbar is a sibling of the entries, not
       their parent, so a state on it could not reach them. Absent means off. */
    pane().dataset.reorder = 'on';
    status('');
  }

  function leave() {
    on = false;
    pending = null;
    var body = pane();
    if (body) body.dataset.reorder = 'off';
    status('');
  }

  function discard() {
    applyOrder(origin);
    preview(origin);
    leave();
  }

  function csrf() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[2]) : '';
  }

  /* Save, then either carry on with what the person was doing (the guard's answer) or
     refresh the shell in place, so the sidebar's numbers come from the server. */
  function save(next) {
    var g = group();
    if (!g) return;
    var order_ = order();
    status('Saving...');
    fetch(g.dataset.reorderEndpoint, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {'Content-Type': 'application/json', 'X-Requested-With': 'fetch',
                'X-CSRFToken': csrf()},
      body: JSON.stringify({
        tatib: Number(g.dataset.reorderFor),
        entries: order_.map(function (pk, index) {
          return {entry: pk, order_number: index + 1};
        }),
      }),
    }).then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    }).then(function () {
      leave();
      if (next) { next(); return; }                 /* carry on to where they were going */
      document.dispatchEvent(new CustomEvent('editor:saved', {detail: {id: null}}));
    }).catch(function () {
      status('Could not save the new order. Nothing was changed.');
    });
  }

  /* ---------- moving one entry ---------------------------------------------- */

  function placeBefore(unit, reference) {
    // reference is the node the unit goes in front of; null appends it last
    var body = pane();
    unit.forEach(function (each) {
      if (reference) reference.parentNode.insertBefore(each, reference);
      else body.appendChild(each);
    });
  }

  function moveBy(pk, step) {
    var order_ = order();
    var at = order_.indexOf(pk);
    var to = at + step;
    if (at < 0 || to < 0 || to >= order_.length) return;
    var moving = order_.slice();
    moving.splice(to, 0, moving.splice(at, 1)[0]);
    var unit = unitOf(node(pk));
    var reference = node(moving[to + 1]);
    placeBefore(unit, reference);
    preview(order());
    status('');
  }

  /* ---------- dragging ------------------------------------------------------ */

  function startDrag(event, pk) {
    if (!on) return;
    event.preventDefault();
    var section = node(pk);
    if (!section) return;
    drag = {pk: pk, unit: unitOf(section), section: section, at: event.clientY, moved: false};
    section.classList.add('is-dragging');
  }

  function moveDrag(event) {
    if (!drag) return;
    if (Math.abs(event.clientY - drag.at) > 4) drag.moved = true;
    if (!drag.moved) return;
    var over = null;
    var middle = 0;
    var every = sections();
    for (var i = 0; i < every.length; i += 1) {
      var box = every[i].getBoundingClientRect();
      if (event.clientY >= box.top && event.clientY <= box.bottom) {
        over = every[i];
        middle = box.top + box.height / 2;
        break;
      }
    }
    if (!over || over === drag.section) return;
    if (event.clientY < middle) placeBefore(drag.unit, over);
    else placeBefore(drag.unit, unitOf(over).pop().nextSibling);
    preview(order());
  }

  function endDrag() {
    if (!drag) return;
    drag.section.classList.remove('is-dragging');
    /* A drag that ended on a link would otherwise fire its click: the entry is full of
       jump links, and a reorder that jumps the page is not what anyone asked for. */
    if (drag.moved) swallow = true;
    drag = null;
    preview(order());
  }

  /* ---------- what the person does ----------------------------------------- */

  /* A drag that ended on a link must not fire it as well. Capture phase, so this beats the
     shell's own click handling -- which would otherwise navigate mid-reorder. */
  document.addEventListener('click', function (event) {
    if (!swallow) return;
    swallow = false;
    event.preventDefault();
    event.stopPropagation();
  }, true);

  document.addEventListener('click', function (event) {
    var up = event.target.closest('[data-move-up]');
    if (up) {
      event.preventDefault();
      var pkUp = Number(up.dataset.moveUp);
      moveBy(pkUp, -1);
      var again = node(pkUp) && node(pkUp).querySelector('[data-move-up]');
      if (again) again.focus();                     /* keep the keyboard's place */
      return;
    }
    var down = event.target.closest('[data-move-down]');
    if (down) {
      event.preventDefault();
      var pkDown = Number(down.dataset.moveDown);
      moveBy(pkDown, 1);
      var next = node(pkDown) && node(pkDown).querySelector('[data-move-down]');
      if (next) next.focus();
      return;
    }
    if (event.target.closest('[data-reorder-start]')) {
      event.preventDefault();
      enter();
      return;
    }
    if (event.target.closest('[data-reorder-save]')) {
      event.preventDefault();
      save(null);
      return;
    }
    if (event.target.closest('[data-reorder-discard]')) {
      event.preventDefault();
      discard();
      return;
    }
  });

  document.addEventListener('pointerdown', function (event) {
    if (!on || event.button !== 0) return;
    /* the grip, or anywhere on the entry: in reorder mode the whole entry is a handle */
    var section = event.target.closest('section[data-entry-pk]');
    if (section) startDrag(event, Number(section.dataset.entryPk));
  });
  document.addEventListener('pointermove', moveDrag);
  document.addEventListener('pointerup', endDrag);
  document.addEventListener('pointercancel', endDrag);
  window.addEventListener('blur', endDrag);

  /* ---------- the question before leaving ---------------------------------- */

  function dialog() { return document.querySelector('[data-reorder-confirm]'); }

  document.addEventListener('click', function (event) {
    var d = dialog();
    if (event.target.closest('[data-reorder-stay]')) {
      event.preventDefault();
      if (d) d.close();
      pending = null;
      return;
    }
    if (event.target.closest('[data-reorder-leave]')) {
      event.preventDefault();
      var carrying = pending;
      pending = null;
      if (d) d.close();
      discard();
      if (carrying) carrying();
      return;
    }
    if (event.target.closest('[data-reorder-and-save]')) {
      event.preventDefault();
      var carry = pending;
      pending = null;
      if (d) d.close();
      save(carry);
      return;
    }
  });

  /* The shell asks before it swaps the pane (reading.js, navigate): a reorder that has
     not been saved must not disappear without a word. */
  window.gkpsUnsaved = {
    holds: function () { return on && changed(); },
    ask: function (proceed) {
      var d = dialog();
      pending = proceed;
      if (d && !d.open) d.showModal();
      else if (proceed) proceed();
    },
  };

  window.addEventListener('beforeunload', function (event) {
    if (!on || !changed()) return;
    event.preventDefault();
    event.returnValue = '';                        /* a tab close asks too */
  });

  /* A swap brings its own toolbar: whatever was pending went with the old pane, and the
     pane keeps the attribute (it is the swapped element's parent, so clear it here). */
  document.addEventListener('shell:page', function () {
    on = false;
    origin = [];
    pending = null;
    var body = pane();
    if (body) body.dataset.reorder = 'off';
    status('');
  });
})();
