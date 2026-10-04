/* Reordering a Tata Ibadah's entries (spec 006, slice 3).
 *
 * The order is ARRANGED IN THE SIDEBAR, where the order is listed: each entry's row carries
 * the handle and the arrows, and there is NO Reorder button -- the first drag, or the first
 * arrow press, is what starts rearranging. The strip below the sidebar's filter then appears
 * with Save and Discard, and the pane on the right follows the order.
 *
 * Nothing is written until Save; Discard puts back what was there. Leaving with unsaved
 * changes asks first: the shell's own in-page navigation is intercepted through navigate()
 * in reading.js, and a tab close through beforeunload.
 *
 * ONE state attribute, on the document root, drives all of it: the strip, the sidebar's
 * handles and the pane's hidden add controls live in different subtrees, and only the root
 * is above them all.
 *
 * Everything is DELEGATED and resolved from the document on each use: the shell swaps the
 * reading pane in place, and re-creates the strip with the section that owns it.
 */
(function () {
  'use strict';

  function group() { return document.querySelector('[data-reorder-group]'); }
  function pane() { return document.getElementById('readBody'); }
  function list() { return document.getElementById('chList'); }
  function root() { return document.documentElement; }

  var on = false;                 /* the reorder mode */
  var origin = [];                /* the order the rows were in when it started */
  var numbers = {};               /* pk -> the number its row showed then */
  var nodes = {};                 /* pk -> that entry's own nodes in the pane */
  var pending = null;             /* what to run once a guarded question is answered */
  var drag = null;
  var swallow = false;            /* the click that follows a drag, to be swallowed */

  /* ---------- the sidebar's rows ------------------------------------------- */

  function rowOf(pk) {
    var l = list();
    return l ? l.querySelector('a[data-i="e' + pk + '"]') : null;
  }
  function rowFor(pk) { var link = rowOf(pk); return link ? link.closest('li') : null; }
  function rows() {
    var l = list();
    if (!l) return [];
    return [].slice.call(l.children).filter(function (item) {
      var link = item.querySelector('a[data-i]');
      return !!link && link.dataset.i.charAt(0) === 'e';
    });
  }
  function pkOfRow(item) {
    var grip = item.querySelector('[data-move-grip]');
    if (grip) return Number(grip.dataset.moveGrip);
    var link = item.querySelector('a[data-i]');
    return link ? Number(link.dataset.i.slice(1)) : null;
  }
  function order() { return rows().map(pkOfRow); }
  function changed() {
    var now = order();
    return now.length !== origin.length || now.some(function (pk, index) {
      return pk !== origin[index];
    });
  }

  /* Put the rows in a given order (they are the last rows in the list, so appending lands
     them right), renumber them to what that order would show, and move the pane to match. */
  function place(what) {
    var l = list();
    if (!l) return;
    what.forEach(function (pk) {
      var item = rowFor(pk);
      if (item) l.appendChild(item);
    });
  }
  function renumber() {
    var l = list();
    if (!l) return;
    /* the numbers come from the sidebar's own non-entry rows, which the server numbered */
    var others = [].slice.call(l.querySelectorAll('a[data-i]')).filter(function (link) {
      return link.dataset.i.charAt(0) !== 'e';
    }).map(function (link) { return Number(link.dataset.num) || 0; });
    var base = others.length ? Math.max.apply(null, others) : 0;
    order().forEach(function (pk, index) {
      var link = rowOf(pk);
      var cell = link && link.querySelector('.songrow__c');
      if (cell) cell.textContent = String(base + index + 1);
    });
  }

  /* ---------- the pane follows --------------------------------------------- */

  /* A unit is a section AND the add row that follows it: the add row is anchored to the item
     it follows, so moving one without the other would leave a later add pointing at the
     wrong place. */
  function readNodes() {
    nodes = {};
    var body = pane();
    if (!body) return;
    [].slice.call(body.querySelectorAll('section[data-entry-pk]')).forEach(function (section) {
      var unit = [section];
      var next = section.nextElementSibling;
      if (next && next.classList.contains('entry__add')) unit.push(next);
      nodes[Number(section.dataset.entryPk)] = unit;
    });
  }
  function applyPaneOrder(what) {
    var body = pane();
    if (!body) return;
    what.forEach(function (pk) {
      (nodes[pk] || []).forEach(function (each) { body.appendChild(each); });
    });
  }

  function status(message) {
    var line = document.querySelector('[data-reorder-status]');
    if (line) line.textContent = message || '';
  }

  /* ---------- the mode ------------------------------------------------------ */

  function enter() {
    if (on) return true;
    if (!group()) return false;
    if (window.gkpsDisplay && window.gkpsDisplay.locked()) {
      window.gkpsDisplay.refuse();                  /* the display owns the order */
      return false;
    }
    if (!rows().length) return false;
    origin = order();
    numbers = {};
    rows().forEach(function (item) {
      var cell = item.querySelector('.songrow__c');
      numbers[pkOfRow(item)] = cell ? cell.textContent : '';
    });
    readNodes();
    on = true;
    root().dataset.reorder = 'on';
    status('');
    return true;
  }

  function leave(restore) {
    if (restore) {
      place(origin);
      Object.keys(numbers).forEach(function (pk) {
        var link = rowOf(Number(pk));
        var cell = link && link.querySelector('.songrow__c');
        if (cell) cell.textContent = numbers[pk];
      });
      applyPaneOrder(origin);
    }
    on = false;
    pending = null;
    root().dataset.reorder = 'off';
    status('');
  }

  function csrf() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[2]) : '';
  }

  /* Save, then either carry on with what the person was doing (the guard's answer) or let
     the shell refresh in place, so every list comes back from the server. */
  function save(next) {
    var strip = group();
    if (!strip) return;
    status('Saving...');
    fetch(strip.dataset.reorderEndpoint, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {'Content-Type': 'application/json', 'X-Requested-With': 'fetch',
                'X-CSRFToken': csrf()},
      body: JSON.stringify({
        tatib: Number(strip.dataset.reorderFor),
        entries: order().map(function (pk, index) {
          return {entry: pk, order_number: index + 1};
        }),
      }),
    }).then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    }).then(function () {
      leave(false);
      if (next) { next(); return; }                 /* carry on to where they were going */
      document.dispatchEvent(new CustomEvent('editor:saved', {detail: {id: null}}));
    }).catch(function () {
      status('Could not save the new order. Nothing was changed.');
    });
  }

  /* ---------- moving one entry --------------------------------------------- */

  function moveBy(pk, step) {
    if (!enter()) return;
    var what = order();
    var at = what.indexOf(pk);
    var to = at + step;
    if (at < 0 || to < 0 || to >= what.length) return;
    var moved = what.slice();
    moved.splice(to, 0, moved.splice(at, 1)[0]);
    place(moved);
    renumber();
    applyPaneOrder(order());
    status('');
  }

  /* ---------- dragging a row ------------------------------------------------ */

  function startDrag(event, pk) {
    if (event.button !== 0) return;
    if (!enter()) return;
    var item = rowFor(pk);
    if (!item) return;
    event.preventDefault();
    drag = {pk: pk, row: item, start: event.clientY, y: event.clientY, moved: false};
    item.classList.add('is-dragging');
    /* The gesture belongs to this row for its whole journey: without capture, the browser
       hands the sequence to whatever is under the pointer next, and a drag that carried a
       row over its neighbours lost the rest of its moves. */
    if (item.setPointerCapture && event.pointerId != null) {
      try { item.setPointerCapture(event.pointerId); } catch (e) { /* no capture */ }
    }
  }

  function moveDrag(event) {
    if (!drag) return;
    drag.y = event.clientY;                  /* the module's OWN record of the pointer */
    if (Math.abs(event.clientY - drag.start) > 3) drag.moved = true;
    if (!drag.moved) return;
    /* The row FOLLOWS the pointer visually and the move is committed on release. Moving the
       node during the drag would remove it from the document mid-gesture, and the browser
       answers a pointer whose target has gone with `pointercancel` -- which ended the drag
       after its first step. */
    drag.row.style.position = 'relative';
    drag.row.style.zIndex = '2';
    drag.row.style.transform = 'translateY(' + Math.round(event.clientY - drag.start) + 'px)';
  }

  function endDrag() {
    if (!drag) return;
    var moved = drag.moved;
    var captured = drag.row;
    /* The drop is where the pointer was last SEEN by this module, not whatever coordinates
       the release event carries: the two disagreed in practice, and the row landed a
       position or two short of where it was let go. */
    var dropped = typeof drag.y === 'number' ? drag.y : drag.start;
    if (captured.releasePointerCapture) {
      try { captured.releasePointerCapture(1); } catch (e) { /* it was never captured */ }
    }
    drag.row.classList.remove('is-dragging');
    drag.row.style.transform = '';
    drag.row.style.zIndex = '';
    drag.row.style.position = '';
    if (moved) {
      /* A drag that ended on a row would otherwise fire its link: the row jumps to the
         entry, and a reorder that jumps the page is not what anyone asked for. */
      swallow = true;
      /* Where it was dropped: the first OTHER row whose middle sits below the pointer, or
         the end of the list when there is none. */
      var others = rows().filter(function (item) { return item !== drag.row; });
      var target = null;
      for (var i = 0; i < others.length; i += 1) {
        var box = others[i].getBoundingClientRect();
        if (dropped < box.top + box.height / 2) { target = others[i]; break; }
      }
      var l = list();
      if (target) l.insertBefore(drag.row, target);
      else l.appendChild(drag.row);
      renumber();
      applyPaneOrder(order());
    }
    drag = null;
  }

  /* ---------- what the person does ----------------------------------------- */

  document.addEventListener('pointerdown', function (event) {
    if (event.button !== 0) return;
    var grip = event.target.closest('[data-move-grip]');
    if (grip) { startDrag(event, Number(grip.dataset.moveGrip)); return; }
    /* once the mode is on, anywhere on the row is a handle */
    var item = on ? event.target.closest('#chList li') : null;
    if (item) startDrag(event, pkOfRow(item));
  });
  document.addEventListener('pointermove', moveDrag);
  document.addEventListener('pointerup', endDrag);
  document.addEventListener('pointercancel', endDrag);
  window.addEventListener('blur', endDrag);

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
      var again = rowFor(pkUp) && rowFor(pkUp).querySelector('[data-move-up]');
      if (again) again.focus();                     /* keep the keyboard's place */
      return;
    }
    var down = event.target.closest('[data-move-down]');
    if (down) {
      event.preventDefault();
      var pkDown = Number(down.dataset.moveDown);
      moveBy(pkDown, 1);
      var next = rowFor(pkDown) && rowFor(pkDown).querySelector('[data-move-down]');
      if (next) next.focus();
      return;
    }
    if (event.target.closest('[data-reorder-save]')) {
      event.preventDefault();
      save(null);
      return;
    }
    if (event.target.closest('[data-reorder-discard]')) {
      event.preventDefault();
      leave(true);
      return;
    }
  });

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
      leave(true);
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

  /* The shell asks before it swaps the pane (reading.js, navigate): an order that has not
     been saved must not disappear without a word. */
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

  /* A swap brings its own rows and its own strip: whatever was pending went with the old
     ones, and only the ROOT carries the attribute, so clear it here. */
  document.addEventListener('shell:page', function () {
    on = false;
    origin = [];
    numbers = {};
    pending = null;
    root().dataset.reorder = 'off';
    status('');
  });
})();
