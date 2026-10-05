/* Reordering a Tata Ibadah's entries (spec 006, slice 3).
 *
 * The order is ARRANGED IN THE SIDEBAR, where the order is listed: each entry's row carries
 * the grip, and there is NO Reorder button -- the first drag, or a keyboard arrow press
 * on the focused grip, is what starts rearranging. The strip below the sidebar's filter then appears
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
  var numbers = [];               /* each text row's number before the preview */
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
    numbers = [];
    var l = list();
    [].slice.call(l ? l.children : []).forEach(function (item) {
      var cell = item.querySelector('.songrow__c');
      if (cell) {
        var link = item.querySelector('a[data-i]');
        numbers.push({cell: cell, text: cell.textContent, link: link,
                      dataNum: link ? link.dataset.num : null});
      }
    });
    readNodes();
    on = true;
    root().dataset.reorder = 'on';
    status('');
    return true;
  }

  function leave(restore) {
    if (drag) cancelDrag();
    if (restore) {
      place(origin);
      numbers.forEach(function (saved) {
        saved.cell.textContent = saved.text;
        if (saved.link) saved.link.dataset.num = saved.dataNum;
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
        entries: order().map(function (pk) {
          var item = rowFor(pk);
          return {entry: pk, order_number: item
            ? Array.prototype.indexOf.call(list().children, item) + 1 : 0};
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
    if (drag) cancelDrag();
    on = false;
    origin = [];
    numbers = [];
    pending = null;
    root().dataset.reorder = 'off';
    status('');
  });
})();
