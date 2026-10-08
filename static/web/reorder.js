/* Reordering a Tata Ibadah's entries (spec 006, slice 3; spec 026).
 *
 * The order is ARRANGED IN THE SIDEBAR, where the order is listed: each entry's row carries
 * the grip, and there is NO Reorder button -- the first drag, or a keyboard arrow press on the
 * focused grip, is what starts rearranging. The pane on the right follows the order.
 *
 * A change is written AS SOON AS IT IS MADE (spec 026): a completed drop, or a settled keyboard
 * move, posts the whole order, and the display re-reads. There is no mode, no Save and no
 * Discard, and nothing unsaved to lose -- so the shell never has to ask before it navigates.
 *
 * Everything is DELEGATED and resolved from the document on each use: the shell swaps the
 * reading pane in place, and re-creates the sidebar with the section that owns it.
 */
(function () {
  'use strict';

  function group() { return document.querySelector('[data-reorder-group]'); }
  function pane() { return document.getElementById('readBody'); }
  function list() { return document.getElementById('chList'); }

  var nodes = {};                 /* pk -> that entry's own nodes in the pane */
  var settled = [];               /* the last order the server confirmed */
  var drag = null;
  var swallow = false;            /* the click that follows a drag, to be swallowed */
  var inFlight = false;           /* one write at a time */
  var queued = false;             /* a newer order arrived while a write was in flight */
  var keyboardTimer = null;

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

  /* Reorder only entry rows in their existing slots; old rows keep their positions. */
  function place(what) {
    var l = list();
    if (!l) return;
    var slots = rows();
    var slotSet = new Set(slots);
    var moving = what.map(rowFor).filter(Boolean);
    var cursor = 0;
    var children = [].slice.call(l.children).map(function (item) {
      return slotSet.has(item) ? moving[cursor++] : item;
    });

    /* Move only nodes that changed position. Replacing the whole list detaches the
       grabbed row and cancels its pointer capture before the gesture finishes. */
    children.forEach(function (item, index) {
      if (l.children[index] !== item) l.insertBefore(item, l.children[index] || null);
    });
  }
  function renumber() {
    var l = list();
    if (!l) return;
    var number = 0;
    [].slice.call(l.children).forEach(function (item) {
      var link = item.querySelector('a[data-i]');
      var entryBreak = item.classList.contains('toc__eos')
        && !!item.querySelector('[data-move-grip]');
      if (link || entryBreak) number += 1;
      var cell = item.querySelector('.songrow__c');   /* breaks have no visible number */
      if (cell) cell.textContent = String(number);
      if (link) link.dataset.num = String(number);
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
    [].slice.call(body.querySelectorAll('[data-entry-pk]')).forEach(function (section) {
      var unit = [section];
      var next = section.nextElementSibling;
      if (next && next.classList.contains('entry__add')) unit.push(next);
      nodes[Number(section.dataset.entryPk)] = unit;
    });
  }
  function applyPaneOrder(what) {
    var body = pane();
    if (!body) return;
    var slotNodes = Object.keys(nodes).reduce(function (all, pk) {
      return all.concat(nodes[pk]);
    }, []);
    var slotSet = new Set(slotNodes);
    var moving = [].concat.apply([], what.map(function (pk) { return nodes[pk] || []; }));
    var cursor = 0;
    var children = [].slice.call(body.children).map(function (item) {
      return slotSet.has(item) ? moving[cursor++] : item;
    });
    body.replaceChildren.apply(body, children);
  }

  function status(message) {
    var line = document.querySelector('[data-reorder-status]');
    if (line) line.textContent = message || '';
  }

  function csrf() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[2]) : '';
  }

  /* ---------- writing the order (spec 026) ---------------------------------
     Every change is written at once. One request is in flight at a time; if another drop
     lands while it runs, only the newest order is sent next, so a burst settles on the last
     one. The full order goes every time, so a single write repairs an earlier failure. */

  function body() {
    var strip = group();
    if (!strip) return null;
    return JSON.stringify({
      tatib: Number(strip.dataset.reorderFor),
      entries: order().map(function (pk) {
        var item = rowFor(pk);
        return {entry: pk, order_number: item
          ? Array.prototype.indexOf.call(list().children, item) + 1 : 0};
      }),
    });
  }

  /* Put the list back to the last order the server confirmed. */
  function restore(saved) {
    if (!saved || !saved.length) return;
    readNodes();
    var before = snapshot();
    place(saved);
    renumber();
    morph(before);
    applyPaneOrder(saved);
  }

  function send() {
    var strip = group();
    var payload = body();
    if (!strip || payload == null) return;
    inFlight = true;
    status('');
    fetch(strip.dataset.reorderEndpoint, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {'Content-Type': 'application/json', 'X-Requested-With': 'fetch',
                'X-CSRFToken': csrf()},
      body: payload,
    }).then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    }).then(function () {
      inFlight = false;
      settled = order();
      if (queued) { queued = false; send(); return; }
      if (window.gkpsDisplay && window.gkpsDisplay.changed) window.gkpsDisplay.changed();
    }).catch(function () {
      inFlight = false;
      queued = false;
      status('Could not save the new order. It has been put back.');
      restore(settled);
    });
  }

  function persist() {
    if (inFlight) { queued = true; return; }
    send();
  }

  /* A held arrow key would fire a write per repeat: settle on the final order first. */
  function persistSoon() {
    window.clearTimeout(keyboardTimer);
    keyboardTimer = window.setTimeout(persist, 250);
  }

  /* ---------- moving one entry --------------------------------------------- */

  function moveBy(pk, step) {
    readNodes();
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
    persistSoon();
  }

  /* ---------- dragging a row ------------------------------------------------ */

  function clearGhost(current) {
    if (!current) return;
    if (current.ghost) current.ghost.remove();
    current.row.classList.remove('is-dragging');
    var l = list();
    if (l) l.classList.remove('is-dragging', 'is-grabbing');
  }

  function makeGhost(event) {
    var rect = drag.row.getBoundingClientRect();
    var copy = document.createElement('div');
    copy.className = 'reorder__ghost';
    copy.dataset.reorderGhost = '';
    copy.setAttribute('aria-hidden', 'true');
    copy.inert = true;
    /* Keep the row's paint, including its grip, but none of its controls or IDs. */
    copy.innerHTML = drag.row.innerHTML;
    [].slice.call(copy.querySelectorAll('a, button, [id], [tabindex], [data-move-grip]'))
      .forEach(function (node) {
        if (node.matches('a, button')) {
          var decoration = document.createElement('span');
          decoration.className = node.className;
          decoration.innerHTML = node.innerHTML;
          node.replaceWith(decoration);
        } else {
          node.removeAttribute('id');
          node.removeAttribute('tabindex');
          node.removeAttribute('data-move-grip');
        }
      });
    /* A section break is its own flex row rather than a child link. */
    if (drag.row.classList.contains('toc__eos')) copy.classList.add('toc__eos');
    copy.style.width = rect.width + 'px';
    copy.style.height = rect.height + 'px';
    document.body.appendChild(copy);
    drag.ghost = copy;
    drag.offsetX = drag.x - rect.left;
    drag.offsetY = drag.start - rect.top;
    positionGhost(event);
  }

  function positionGhost(event) {
    if (!drag || !drag.ghost) return;
    drag.ghost.style.left = (event.clientX - drag.offsetX) + 'px';
    drag.ghost.style.top = (event.clientY - drag.offsetY) + 'px';
  }

  function cancelDrag() {
    if (!drag) return;
    var current = drag;
    drag = null;  /* moving a captured node can fire pointercancel again during place() */
    clearGhost(current);
    if (current.moved && list() === current.row.parentNode) {
      var before = snapshot();
      place(current.order);
      renumber();
      morph(before);
      applyPaneOrder(current.order);
    }
  }

  function startDrag(event, pk) {
    if (event.button !== 0) return;
    window.clearTimeout(keyboardTimer);     /* the drop's own write supersedes a pending one */
    keyboardTimer = null;
    readNodes();
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
    drag = {pk: pk, row: item, mids: mids, start: event.clientY, x: event.clientX,
            y: event.clientY, order: order(), moved: false};
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
    var what = order();
    var at = what.indexOf(drag.pk);
    if (at < 0) return;
    what.splice(at, 1);
    var to = target == null ? what.length : what.indexOf(target);
    what.splice(to < 0 ? what.length : to, 0, drag.pk);
    place(what);
  }

  function moveDrag(event) {
    if (!drag) return;
    drag.y = event.clientY;
    if (!drag.moved && Math.abs(event.clientY - drag.start) > 3) {
      drag.moved = true;
      makeGhost(event);
      drag.row.classList.add('is-dragging');
      list().classList.add('is-grabbing');
    }
    if (!drag.moved) return;
    positionGhost(event);
    var before = snapshot();
    placeRowAt(drag.y);
    /* the numbers read the order the drag has produced, and the rows that parted animate */
    renumber();
    morph(before);
  }

  function endDrag(event) {
    if (!drag) return;
    var moved = drag.moved;
    var before = snapshot();
    clearGhost(drag);
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
    if (moved) persist();                   /* the drop is the write (spec 026) */
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
  document.addEventListener('pointercancel', cancelDrag, true);
  window.addEventListener('blur', cancelDrag, true);
  /* A drag that ended on a link must not fire it as well. Capture phase, so this beats the
     shell's own click handling -- which would otherwise navigate mid-reorder. */
  document.addEventListener('click', function (event) {
    if (!swallow) return;
    swallow = false;
    event.preventDefault();
    event.stopPropagation();
  }, true);

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

  /* A swap brings its own rows: the order that mattered went with the old ones. */
  document.addEventListener('shell:page', function () {
    if (drag) cancelDrag();
    window.clearTimeout(keyboardTimer);
    keyboardTimer = null;
    nodes = {};
    settled = order();
    status('');
  });

  settled = order();
})();
