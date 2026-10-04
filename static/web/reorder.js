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

  function rowFor(pk) {
    var l = list();
    var grip = l && l.querySelector('[data-move-grip="' + pk + '"]');
    return grip ? grip.closest('li') : null;
  }
  /* The rows that can be moved: a normal entry's row, and a break's row -- which is the thin
     line rather than a link. What they share is the grip. */
  function rows() {
    var l = list();
    if (!l) return [];
    return [].slice.call(l.children).filter(function (item) {
      return !!item.querySelector('[data-move-grip]');
    });
  }
  function pkOfRow(item) {
    var grip = item.querySelector('[data-move-grip]');
    return grip ? Number(grip.dataset.moveGrip) : null;
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
  function renumber(what) {
    var l = list();
    if (!l) return;
    /* the numbers come from the sidebar's own non-entry rows, which the server numbered */
    var others = [].slice.call(l.querySelectorAll('a[data-i]')).filter(function (link) {
      return link.dataset.i.charAt(0) !== 'e';
    }).map(function (link) { return Number(link.dataset.num) || 0; });
    var base = others.length ? Math.max.apply(null, others) : 0;
    (what || order()).forEach(function (pk, index) {
      var item = rowFor(pk);
      var cell = item && item.querySelector('.songrow__c');   /* a break's row has none */
      if (cell) cell.textContent = String(base + index + 1);
    });
  }

  /* ---------- the morph ----------------------------------------------------- */

  /* Every row is measured before a change; each one that moved is put back where it was and
     released on the next frame, so the browser animates the difference. The eye follows the
     row that travelled instead of the list blinking into a new shape. */
  function snapshot() {
    var before = {};
    rows().forEach(function (item) {
      before[pkOfRow(item)] = item.getBoundingClientRect().top;
    });
    return before;
  }
  function morph(before) {
    rows().forEach(function (item) {
      if (item.classList.contains('is-dragging')) return;
      var was = before[pkOfRow(item)];
      if (was == null) return;
      var delta = was - item.getBoundingClientRect().top;
      if (!delta) return;
      item.style.transition = 'none';
      item.style.transform = 'translateY(' + delta + 'px)';
      window.requestAnimationFrame(function () {
        item.style.transition = '';
        item.style.transform = '';
      });
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
        var item = rowFor(Number(pk));
        var cell = item && item.querySelector('.songrow__c');
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
    var before = snapshot();
    var moved = what.slice();
    moved.splice(to, 0, moved.splice(at, 1)[0]);
    place(moved);
    renumber();
    morph(before);
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
    /* The row ITSELF travels through the list -- no gap is inserted beside it. A gap would
       stand in addition to the row that is still occupying its own space, so the list would
       gain a row and everything below would be pushed down. What the person sees while
       dragging is the order they will get. */
    var mids = [];
    rows().forEach(function (each) {
      if (each === item) return;
      var rect = each.getBoundingClientRect();
      mids.push({pk: pkOfRow(each), middle: rect.top + rect.height / 2});
    });
    drag = {pk: pk, row: item, mids: mids, start: event.clientY, y: event.clientY,
            moved: false};
    item.classList.add('is-dragging');
    list().classList.add('is-dragging');    /* the list shortens the morph while a drag runs */
    if (item.setPointerCapture && event.pointerId != null) {
      try { item.setPointerCapture(event.pointerId); } catch (e) { /* no capture */ }
    }
  }

  /* Where the row goes for a pointer at y, measured against the OTHER rows' midpoints as they
     were when the drag started. Frozen on purpose: the row moving through the list changes the
     layout under the pointer, so measuring live would move the goalposts with every step and
     the row would stall a place short of where it was released. */
  function placeRowAt(y) {
    var target = null;
    for (var i = 0; i < drag.mids.length; i += 1) {
      if (y < drag.mids[i].middle) { target = drag.mids[i].pk; break; }
    }
    var l = list();
    if (target == null) l.appendChild(drag.row);
    else l.insertBefore(drag.row, rowFor(target));
  }

  function moveDrag(event) {
    if (!drag) return;
    drag.y = event.clientY;
    if (Math.abs(event.clientY - drag.start) > 3) drag.moved = true;
    if (!drag.moved) return;
    var before = snapshot();
    placeRowAt(drag.y);
    /* the numbers read the order the drag has produced, and the rows that parted animate */
    renumber();
    morph(before);
  }

  function endDrag(event) {
    if (!drag) return;
    var moved = drag.moved;
    var item = drag.row;
    var before = snapshot();
    item.classList.remove('is-dragging');
    list().classList.remove('is-dragging');
    if (moved) {
      if (event && typeof event.clientY === 'number') {
        before = snapshot();
        placeRowAt(event.clientY);          /* one last placement with the release's own Y */
      }
      /* A drag that ended on a row would otherwise fire its link: the row jumps to the entry,
         and a reorder that jumps the page is not what anyone asked for. */
      swallow = true;
      renumber();
      morph(before);
      applyPaneOrder(order());
    }
    drag = null;
  }

  /* ---------- what the person does ----------------------------------------- */

  /* The drag's own listeners are in the CAPTURE phase. A bubble-phase listener on the document
     stopped seeing the later moves of a gesture -- measured with a capture-phase trace that saw
     every one of them -- which is why a row kept landing a step short of where it was released. */
  document.addEventListener('pointerdown', function (event) {
    if (event.button !== 0) return;
    /* Only the grip starts a drag: it is the one control the sidebar draws, and a row's body
       belongs to the link that opens the entry. */
    var grip = event.target.closest('[data-move-grip]');
    if (grip) startDrag(event, Number(grip.dataset.moveGrip));
  }, true);
  document.addEventListener('pointermove', moveDrag, true);
  document.addEventListener('pointerup', endDrag, true);
  document.addEventListener('pointercancel', endDrag, true);
  window.addEventListener('blur', endDrag, true);
  /* A drag that ended on a link must not fire it as well. Capture phase, so this beats the
     shell's own click handling -- which would otherwise navigate mid-reorder. */
  document.addEventListener('click', function (event) {
    if (!swallow) return;
    swallow = false;
    event.preventDefault();
    event.stopPropagation();
  }, true);

  document.addEventListener('click', function (event) {
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

  /* The grip is a button: a keyboard can take hold of it and move the row with the arrow
     keys. It is the only control there is -- no arrows are drawn -- so this is what keeps
     the order rearrangable without a pointer. */
  document.addEventListener('keydown', function (event) {
    var grip = event.target.closest && event.target.closest('[data-move-grip]');
    if (!grip) return;
    if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return;
    event.preventDefault();
    var pk = Number(grip.dataset.moveGrip);
    moveBy(pk, event.key === 'ArrowUp' ? -1 : 1);
    var again = rowFor(pk) && rowFor(pk).querySelector('[data-move-grip]');
    if (again) again.focus();                     /* keep the keyboard's place */
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
