/* Spec 189 preview — the states, the modal, and the two candidate reorder modes.
 *
 * Nothing here writes anywhere: the page is a static preview of a slice, and the
 * README says so. The numbers ARE real — they come from the probe.
 *
 * A  "Reorder verses" — a mode that turns the list into one-line rows.
 * B  grab a grip in the reading view — the list collapses for the gesture and
 *    expands again on release.
 *
 * Both share one drag engine: a single rAF loop, the row carried by transform only,
 * a FLIP pass on the rows that move (one measurement per crossing, never per frame),
 * and edge auto-scroll.
 */
(function () {
  'use strict';

  var root = document.documentElement;
  var read = document.getElementById('read');
  var body = document.getElementById('readBody');
  var modal = document.getElementById('editorModal');
  var content = document.getElementById('editorContent');
  if (!body || !modal || !content) return;

  var savedBody = body.innerHTML;

  /* The complaint is about LONG verses, and no ordinary song in the library has more
     than four stanzas — so the toggle swaps the page's verses for a fixture of eight
     real stanzas, one from each of eight ordinary songs (`long_song.json`, inlined by
     build.py). Every line is the library's own text; only the composition is the
     preview's, and the README says so. */
  var longOn = false;

  function applyLong() {
    if (!longOn) return;
    var fixture = window.__LONG_SONG && window.__LONG_SONG.verses;
    if (!fixture || !fixture.length) return;
    var template = verses()[0];
    if (!template) return;
    var add = document.querySelector('.verse-add');
    verses().forEach(function (row) { row.remove(); });
    fixture.forEach(function (stanza, index) {
      var copy = template.cloneNode(true);
      copy.removeAttribute('style');
      copy.classList.remove('is-dragging', 'is-acts', 'is-compact');
      copy.dataset.verse = 'long-' + (index + 1);   /* a row of its own, never a copy's key */
      copy.querySelector('.v__text').innerHTML = stanza.lines.join('<br>');
      body.insertBefore(copy, add || null);
    });
    numberRows();
  }

  function verses() {
    return [].slice.call(body.querySelectorAll('.v'));
  }
  function esc(text) {
    return String(text == null ? '' : text)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function lyricOf(row) {
    var text = row.querySelector('.v__text');
    return text ? text.innerHTML.replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, '') : '';
  }
  /* While a verse is in hand its own gutter reads `from→now` — the number it was
     taken from and the number it holds at this moment — so the order before the grab
     is not something the person has to remember. */
  function paintNumbers() {
    numberRows();
    verses().forEach(function (row) { row.classList.remove('is-seam-above'); });
    if (!drag) return;
    /* The seam above the slot the verse is about to land in. */
    var rows = verses();
    var above = rows[rows.indexOf(drag.row) - 1];
    if (above) above.classList.add('is-seam-above');
    var index = verses().indexOf(drag.row);
    if (index < 0) return;
    /* The readout rides the ghost while it travels (Sidebar's mirror of
       renumber): the real row's contents are hidden once the ghost is up. */
    var target = (drag.ghost && drag.ghost.querySelector('.v__n')) || drag.row.querySelector('.v__n');
    if (target) target.textContent = drag.from + '→' + (index + 1);
  }

  /* The hairlines are the list's, not the rows': while a verse is in hand the drawn
     lines must still be exactly the seams of the order on screen — one per 44px slot
     boundary, none riding along with the card, none missing where it was lifted from. */
  function seams() {
    var rows = verses();
    if (!rows.length) return {drawn: [], expected: [], ok: true};
    var drawn = [];
    var detail = [];
    rows.forEach(function (row) {
      var style = getComputedStyle(row);
      detail.push({n: row.querySelector('.v__n').textContent.trim(),
                   top: Math.round(row.getBoundingClientRect().top),
                   h: Math.round(row.getBoundingClientRect().height),
                   bt: style.borderTopWidth, bb: style.borderBottomWidth,
                   drag: row.classList.contains('is-dragging'),
                   compact: row.classList.contains('is-compact')});
      var rect = row.getBoundingClientRect();
      if (parseFloat(style.borderTopWidth) > 0) drawn.push(Math.round(rect.top));
      if (parseFloat(style.borderBottomWidth) > 0) drawn.push(Math.round(rect.bottom));
    });
    var unique = drawn.filter(function (value, index) {
      return drawn.indexOf(value) === index;
    }).sort(function (a, b) { return a - b; });
    /* The seams of the table, read off the slot grid rather than off individual rows:
       the row in hand is drawn somewhere else entirely, so its own rect is no guide,
       and a row a crossing just displaced is still travelling. A slot is one row's
       height, and every row in a mode has the same one. */
    var visible = rows.filter(function (row) {
      return !row.classList.contains('is-dragging');
    });
    if (!visible.length) return {drawn: [], expected: [], ok: true};
    var offset = rows.indexOf(visible[0]);
    var base = visible[0].getBoundingClientRect().top;
    var slot = visible[0].getBoundingClientRect().height;
    var expected = [];
    for (var index = 1; index < rows.length; index += 1) {
      expected.push(Math.round(base + (index - offset) * slot));
    }
    return {drawn: unique, expected: expected, detail: detail,
            ok: JSON.stringify(unique) === JSON.stringify(expected)};
  }

  function numberRows() {
    verses().forEach(function (row, index) {
      var n = row.querySelector('.v__n');
      if (n) n.textContent = String(index + 1);
      var grip = row.querySelector('.v__grip');
      if (grip) grip.setAttribute('aria-label', 'Drag to reorder verse ' + (index + 1));
      var edit = row.querySelector('.v__edit');
      if (edit) edit.setAttribute('aria-label', 'Edit verse ' + (index + 1));
      var acts = row.querySelector('.v__acts');
      if (acts) acts.setAttribute('aria-label', 'Verse ' + (index + 1));
    });
  }

  /* ---------- the modal ---------------------------------------------------- */

  function formHtml(title, lyric, options) {
    options = options || {};
    var help = options.help ? '<p class="editor__help">' + esc(options.help) + '</p>' : '';
    var del = options.deletable === false ? ''
      : '<button type="button" class="editor__danger editor__delete" data-verse-delete'
        + (options.disabledDelete ? ' disabled' : '') + '>Delete verse</button>';
    return '<h2 class="editor__title" id="editorTitle">' + esc(title) + '</h2>'
      + '<form class="editor__form" data-editor-size="large" onsubmit="return false">'
      + '<div class="editor__field" data-editor-grow><label for="verseLyric">Lyrics</label>'
      + '<textarea id="verseLyric" name="lyric">' + esc(lyric) + '</textarea>'
      + help + '</div>'
      + '<div class="editor__actions">' + del
      + '<button type="button" class="editor__cancel" data-editor-close>Cancel</button>'
      + '<button type="submit" class="editor__save">Save</button>'
      + '</div></form>';
  }

  function confirmHtml(pk, number) {
    return '<div class="editor__confirm">'
      + '<p class="editor__confirm-title">Delete verse ' + number + '?</p>'
      + '<p class="editor__hint">It is removed from this song, and the verses after it are '
      + 'renumbered. Nothing else changes.</p>'
      + '<div class="editor__actions">'
      + '<button type="button" class="editor__cancel" data-editor-close>Cancel</button>'
      + '<button type="button" class="editor__danger" data-confirm-delete data-verse-row="'
      + pk + '">Delete</button>'
      + '</div></div>';
  }

  function show(html) {
    content.innerHTML = html;
    if (!modal.open) modal.showModal();
    var field = content.querySelector('textarea');
    if (field) {
      field.focus();
      field.setSelectionRange(field.value.length, field.value.length);
    }
  }
  function close() {
    if (modal.open) modal.close();
    content.innerHTML = '';
  }
  modal.addEventListener('click', function (event) {
    if (event.target === modal || event.target.closest('[data-editor-close]')) close();
  });
  content.addEventListener('click', function (event) {
    var del = event.target.closest('[data-verse-delete]');
    if (del && !del.disabled) {
      show(confirmHtml(del.dataset.verseRow, del.dataset.verseNumber));
      return;
    }
    var confirmDelete = event.target.closest('[data-confirm-delete]');
    if (confirmDelete) {
      var pk = confirmDelete.dataset.verseRow;
      var target = body.querySelector('.v[data-verse="' + pk + '"]');
      if (target) target.remove();
      numberRows();
      close();
    }
  });

  function openEdit(row) {
    var number = row.querySelector('.v__n').textContent;
    var used = row.dataset.used || '';
    show(formHtml('Edit verse ' + number, lyricOf(row), {
      help: used
        ? 'This verse is used in ' + used + ' Tata Ibadah, so it cannot be deleted here.'
        : '',
      disabledDelete: !!used,
      deletable: true
    }));
    var del = content.querySelector('[data-verse-delete]');
    if (del) {
      del.dataset.verseRow = row.dataset.verse;
      del.dataset.verseNumber = number;
    }
  }

  function openNew() {
    show(formHtml('New verse', '', { deletable: false }));
  }

  /* ---------- the compact list (mode A and the grab-collapse B) ------------- */

  function setCompact(on) {
    verses().forEach(function (row) {
      var text = row.querySelector('.v__text');
      if (text) {
        if (on) {
          /* One line, not four: the stanza's own <br>s would still break the
             "compact" row into its full height. The full markup is kept on the
             row, so leaving the mode restores it byte for byte. */
          if (!row.dataset.fullText) row.dataset.fullText = text.innerHTML;
          text.textContent = row.dataset.fullText
            .split(/<br\s*\/?>/i)[0].replace(/<[^>]+>/g, '');
        } else if (row.dataset.fullText) {
          text.innerHTML = row.dataset.fullText;
          delete row.dataset.fullText;
        }
      }
      row.classList.toggle('is-compact', on);
    });
    var add = document.querySelector('.verse-add');
    if (add) add.hidden = on;
  }

  var arranging = false;
  /* The rejected alternative's control: it exists only while A is being compared, so
     the page at rest carries no reorder button at all — B adds no control. */
  var arrangeBtn = document.createElement('button');
  arrangeBtn.type = 'button';
  arrangeBtn.className = 'read__reorder';
  arrangeBtn.textContent = 'Reorder verses';
  arrangeBtn.setAttribute('aria-pressed', 'false');
  arrangeBtn.hidden = true;
  var headTop = read.querySelector('.read__head-top');
  (headTop || read.querySelector('.read__head') || read).appendChild(arrangeBtn);

  var hint = document.createElement('p');
  hint.className = 'arrange-hint';
  hint.textContent = 'Drag a verse by its handle to move it. Done when the order is right.';
  hint.hidden = true;
  read.insertBefore(hint, body);

  function enterArrange() {
    if (arranging) return;
    arranging = true;
    arrangeBtn.textContent = 'Done';
    arrangeBtn.setAttribute('aria-pressed', 'true');
    hint.hidden = false;
    setCompact(true);
  }
  function exitArrange() {
    if (!arranging) return;
    arranging = false;
    arrangeBtn.textContent = 'Reorder verses';
    arrangeBtn.setAttribute('aria-pressed', 'false');
    hint.hidden = true;
    setCompact(false);
  }
  arrangeBtn.addEventListener('click', function () {
    if (arranging) exitArrange(); else enterArrange();
  });

  /* ---------- the states --------------------------------------------------- */

  /* A hymn song's page and a restricted reader's page carry no control at all: the
     server does not render them, so the preview takes the nodes out rather than
     hiding them — a hidden control would still take a tab stop. */
  function lockControls() {
    exitArrange();
    arrangeBtn.hidden = true;
    verses().forEach(function (row) {
      var acts = row.querySelector('.v__acts');
      if (acts) acts.remove();
    });
    var add = document.querySelector('.verse-add');
    if (add) add.remove();
  }

  function clearStates() {
    exitArrange();
    arrangeBtn.hidden = true;
    body.style.paddingTop = '';
    verses().forEach(function (row) {
      row.classList.remove('is-acts', 'is-dragging', 'is-compact');
      row.style.transform = '';
      row.style.transition = '';
    });
    close();
  }

  var STATES = {
    rest: function () {},
    hover: function () {
      var rows = verses();
      if (rows[1]) rows[1].classList.add('is-acts');
    },
    new: openNew,
    edit: function () {
      var rows = verses();
      if (rows[1]) openEdit(rows[1]);
    },
    used: function () {
      var rows = verses();
      if (rows[1]) {
        rows[1].dataset.used = '2';
        openEdit(rows[1]);
        delete rows[1].dataset.used;
      }
    },
    confirm: function () {
      var rows = verses();
      if (!rows[1]) return;
      show(formHtml('Edit verse', lyricOf(rows[1]), { deletable: true }));
      var del = content.querySelector('[data-verse-delete]');
      del.dataset.verseRow = rows[1].dataset.verse;
      del.dataset.verseNumber = '2';
      del.click();
    },
    short: function () {
      var rows = verses();
      if (!rows[3]) return;
      rows[3].querySelector('.v__text').textContent = 'Amin.';
      rows[3].classList.add('is-acts');
    },
    arrange: function () {
      arrangeBtn.hidden = false;
      enterArrange();
    },
    grab: function () {
      /* B has no mode control at all: the header keeps its title and nothing else. */
      arrangeBtn.hidden = true;
      var rows = verses();
      setCompact(true);
      if (rows[2]) {
        rows[2].classList.add('is-dragging', 'is-acts');
        rows[2].style.transform = 'translateY(-70px)';
      }
    },
    empty: function () {
      body.innerHTML = document.getElementById('emptyState').innerHTML;
    },
    /* A gesture the probe can read: drag the first verse two slots down through the
       compact list, recording what every OTHER row does frame by frame. Each of them
       must step exactly one slot, once, per crossing — the shake this replaced threw
       them the list's whole height and slid them back. */
    longdrag: function () {
      enterArrange();
      var rows = verses();
      var grip = rows[0] && rows[0].querySelector('.v__grip');
      if (!grip) return;
      var trace = {series: {}, reversals: 0, steps: [], expected: [], shifts: [],
                   done: false};
      window.__dragTrace = trace;
      var startTop = grip.getBoundingClientRect().top + 8;
      var x = grip.getBoundingClientRect().left + 8;
      var last = {};
      function sample() {
        verses().forEach(function (row) {
          var key = row.querySelector('.v__text').textContent.trim().slice(0, 14);
          /* The row in hand travels with the pointer by design: it is not what this
             trace measures, so its key is dropped the moment it is picked up. */
          if (row.classList.contains('is-dragging')) {
            trace.dragged = key;
            delete trace.series[key];
            return;
          }
          var top = Math.round(row.getBoundingClientRect().top * 10) / 10;
          if (last[key] === undefined || Math.abs(top - last[key]) > 0.5) {
            (trace.series[key] = trace.series[key] || []).push(top);
            last[key] = top;
          }
        });
      }
      function send(type, y) {
        grip.dispatchEvent(new PointerEvent(type, {
          bubbles: true, cancelable: true, clientX: x, clientY: y,
          pointerId: 7, pointerType: 'mouse', button: 0, buttons: type === 'pointerup' ? 0 : 1
        }));
      }
      function order() {
        return verses().map(function (row) {
          return row.querySelector('.v__text').textContent.trim().slice(0, 14);
        });
      }
      var initial = order();
      sample();
      send('pointerdown', startTop);
      /* The grab itself must change nothing: the list collapses, but the verse stays in
         its own slot until the pointer travels a slot's worth — so the pointer is held
         still for 150ms and the order is read before any movement. */
      /* Cursor-following position: how far the row is from the pointer at grab time */
      var grabOffset = 0;
      window.setTimeout(function () {
        trace.grabOrder = order();
        grabOffset = pointerY - startTop;
        var step = 0;
        /* In bursts, with a hold between them: the hold is what a person does when they
           look at where the verse is going, and it is the only moment the drawn
           hairlines can be read — the rows a crossing displaced keep travelling for
           160ms after it, so a sample taken at a crossing reads their borders 2px out. */
        function burst(until, then) {
          var timer = window.setInterval(function () {
          step += 1;
          send('pointermove', startTop + step * 22);
          /* The ghost rides the hand 1:1 (Sidebar's rule) — no hand-written
             transform on the placeholder. */
          sample();
          /* Independently of the engine's own numbers: the slot the verse holds must be
             the slot it was grabbed from plus one per slot-height of pointer travel. A
             version that added the travel to the RUNNING slot instead of the origin ran
             the verse to an end of the list within two slots. */
          /* The card must be drawn IN its slot (zero offset), not under the pointer: a
          card that rides the cursor sits up to a stanza below the slot it is choosing,
          because the collapse moves the list under the hand. The offset is now from the
          compact slot grid, not the row's expanded-geometry rect captured at grab time. */
        /* Ghost rides the hand 1:1: its top plus the grab offset should
           equal the live pointer exactly (zero slack), unlike a parked
           slot card which visually decouples from the hand. */
        var handTransform = drag.ghost ? drag.ghost.getBoundingClientRect().top + drag.offsetY - (drag.y || pointerY) : 0;
        trace.shifts.push(handTransform);
          /* Read the engine's numbers on the NEXT frame: the pointermove has
             queued a frame that has not run yet, so reading synchronously
             returns the previous step's travel against this step's index.
             Want is the live-cursor rule itself: how many of the others'
             midpoints the current pointer has passed — measured as the
             independent check, not the engine's internal target. */
          window.requestAnimationFrame(function () {
            var debug = window.__dragDebug;
            if (debug && trace.expected) {
              /* Frozen-mids rule (Sidebar's): first frozen middle the live
                 pointer has not crossed yet is the target. */
              var want = drag.mids.length;
              for (var mi = 0; mi < drag.mids.length; mi += 1) {
                if (debug.pointerY < drag.mids[mi].middle) { want = mi; break; }
              }
              trace.expected.push([want, verses().indexOf(drag.row)]);
            }
          });
          if (step >= until) {
            window.clearInterval(timer);
            then();
          }
          }, 70);
        }
        burst(7, function () {
          window.setTimeout(function () {
            trace.seamsMid = seams();
            burst(14, function () {
              /* Sampled while the gesture is still live — the list is compact only
                 while a verse is in hand, and the rows need 160ms to settle. */
              window.setTimeout(function () {
              trace.seamsEnd = seams();
              send('pointerup', startTop + step * 22);
              window.setTimeout(function () { sample(); verdict(); }, 260);
              }, 220);
            });
          }, 340);
        });
      }, 150);

      function verdict() {
          /* Per row: where it started, where it settled, and whether it ever went back
             on itself. A crossing must be one slot, in one direction, once. */
          trace.rows = {};
          Object.keys(trace.series).forEach(function (key) {
            var series = trace.series[key].slice();
            var settled = series.filter(function (value, index) {
              return index + 1 < series.length && series[index + 1] === value;
            });
            var reversals = 0;
            for (var j = 2; j < settled.length; j += 1) {
              var d1 = settled[j] - settled[j - 1];
              var d0 = settled[j - 1] - settled[j - 2];
              if (d0 * d1 < 0) reversals += 1;
            }
            trace.reversals += reversals;
            trace.grabHeld = JSON.stringify(trace.grabOrder || []) === JSON.stringify(initial);
            trace.rows[key] = {
              first: series[0], last: series[series.length - 1],
              travel: Math.round((series[series.length - 1] - series[0]) * 10) / 10,
              reversals: reversals
            };
          });
        trace.indexFollowsTravel = trace.expected.every(function (pair) {
          return pair[0] === pair[1];
        });
        trace.seamsOk = !!(trace.seamsMid && trace.seamsMid.ok
                           && trace.seamsEnd && trace.seamsEnd.ok);
        trace.cardInSlot = trace.shifts.every(function (shift) {
          return Math.abs(shift) <= 0.5;
        });
        trace.cardShifts = trace.shifts.length;
        trace.seams = {mid: trace.seamsMid, end: trace.seamsEnd};
        trace.expectedPairs = trace.expected.length;
        trace.done = true;
      }
    },
    hymn: lockControls,
    restricted: lockControls
  };

  var DEFAULT_NOTE = 'Static preview: the drag and the saves are local. '
    + 'The verse text is song 1825 of the local library.';
  var STATE_NOTES = {
    rest: 'Rest — the page as every reader gets it: verses, numbers, one Add verse row.',
    arrange: 'A · Reorder mode — REJECTED: a header button collapsed the list until Done. Kept '
      + 'here only to be compared against the decision.',
    grab: 'B · Grab collapse — THE DESIGN: grab any verse\'s handle and the list collapses to '
      + 'one-line rows for the gesture, expanding again when you let go. No mode, no button.',
    hymn: 'Hymn song \u2014 no tools at all, and the number does not move on hover either.',
    restricted: 'Restricted reader \u2014 the same page with no tool in the DOM.'
  };

  function setState(name) {
    clearStates();
    if (name !== 'empty') body.innerHTML = savedBody;
    numberRows();
    applyLong();
    (STATES[name] || STATES.rest)();
    note.textContent = STATE_NOTES[name] || DEFAULT_NOTE;
    [].slice.call(document.querySelectorAll('[data-state]')).forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.state === name));
    });
    document.body.dataset.previewState = name;
  }

  /* ---------- one drag engine for both modes -------------------------------- */

  var drag = null;
  var pointerY = 0;
  var frameQueued = false;

  function startDrag(event, grip) {
    var row = grip.closest('.v');
    if (!row) return;
    event.preventDefault();
    var offset = event.clientY - row.getBoundingClientRect().top;
    var collapsed = false;
    if (!arranging) {
      setCompact(true);       /* B: the list gives the gesture a short list to cross */
      collapsed = true;
    }
    var rect = row.getBoundingClientRect();
    /* Sidebar's trick (static/web/reorder.js): freeze the other rows'
       midpoints right here, where the list stands collapsed. Compare the
       live hand against those frozen lines every frame, so moving a row
       never moves the goalposts while you decide where you are. */
    var mids = [];
    verses().forEach(function (other) {
      if (other === row) return;
      var r = other.getBoundingClientRect();
      mids.push({el: other, middle: r.top + r.height / 2});
    });
    drag = {
      row: row,
      mids: mids,
      grab: Math.min(offset, rect.height / 2),
      flowTop: rect.top,
      scroll: window.scrollY,
      collapsed: collapsed,
      /* The insertion target is evaluated every frame from the CURRENT
         cursor position against the CURRENT positions of the other verses.
         The list stays at its normal place — no shifting, no anchoring
         to the spot the verse started from. */
      slotOrigin: verses().indexOf(row),
      slot: verses().indexOf(row),
      startY: event.clientY,
      startX: event.clientX,
      pointerX: event.clientX,
      /* The order as it stood when the grip was taken: with the list collapsed, the
         row in hand is the only place that still knows where this verse started. */
      from: verses().indexOf(row) + 1,
      moved: false,
      ghost: null,
      /* Hand-on-ghost offset, clamped to the compact row's middle, so the
         ghost starts under the hand instead of a stanza below it after the
         collapse moves the list out from under the hand. */
      offsetX: event.clientX - rect.left,
      offsetY: Math.min(offset, rect.height / 2)
    };
    row.classList.add('is-acts');
    row.style.transition = 'none';
    try { grip.setPointerCapture(event.pointerId); } catch (error) { /* preview only */ }
    document.body.style.userSelect = 'none';
    pointerY = event.clientY;
    paintNumbers();          /* the row in hand reads `3→3` from the first frame */
    queue();
  }

  function makeGhost() {
    var rect = drag.row.getBoundingClientRect();
    var copy = document.createElement('div');
    copy.className = 'v v__ghost';
    copy.classList.add('is-dragging');
    copy.setAttribute('aria-hidden', 'true');
    copy.inert = true;
    copy.innerHTML = drag.row.innerHTML;
    [].slice.call(copy.querySelectorAll('a, button, [id], [tabindex]'))
      .forEach(function (node) { node.removeAttribute('id'); node.removeAttribute('tabindex'); });
    copy.style.width = rect.width + 'px';
    copy.style.height = rect.height + 'px';
    copy.style.left = (drag.pointerX - drag.offsetX) + 'px';
    copy.style.top = (pointerY - drag.offsetY) + 'px';
    document.body.appendChild(copy);
    drag.ghost = copy;
  }

  function positionGhost() {
    if (!drag || !drag.ghost) return;
    drag.ghost.style.left = (drag.pointerX - drag.offsetX) + 'px';
    drag.ghost.style.top = (pointerY - drag.offsetY) + 'px';
  }

  function clearGhost(current) {
    if (!current) return;
    if (current.ghost) current.ghost.remove();
    current.row.classList.remove('is-dragging');
    document.body.classList.remove('is-arranging');
  }

  function queue() {
    if (frameQueued) return;
    frameQueued = true;
    window.requestAnimationFrame(frame);
  }

  /* The ghost rides the hand (Sidebar's shape, static/web/reorder.js):
     it follows clientY 1:1 with the grab offset preserved, the real row
     stays in flow as a tinted placeholder, and the others morph under
     CSS. `cursor` is the ships feel now; `slot` parking is kept only as
     the rejected comparison behind the bar. */
  var cardMode = 'cursor';            /* 'slot' is the rejected parking */
  window.__cardMode = cardMode;

  function frame() {
    frameQueued = false;
    if (!drag) return;
    if (!drag.moved) return;
    var row = drag.row;

    /* A scroll between frames moves every row under the viewport: keep the
       cached flow position honest instead of measuring again. */
    var scrollNow = window.scrollY;
    if (scrollNow !== drag.scroll) {
      drag.flowTop += drag.scroll - scrollNow;
      drag.scroll = scrollNow;
    }

    /* Where the row goes for the live pointer, measured against the OTHER
       rows' midpoints as they stood at the grab (Sidebar's frozen rule).
       Frozen on purpose: the row moving through the list changes the
       layout under the pointer, so measuring live would move the goalposts
       and the row would stall short of where it was released. */
    var others = verses().filter(function (item) { return item !== row; });
    var slotHeight = others.length ? others[0].getBoundingClientRect().height : 44;
    var target = drag.mids.length;
    for (var i = 0; i < drag.mids.length; i += 1) {
      if (pointerY < drag.mids[i].middle) { target = i; break; }
    }
    /* placeRowAt: translate the frozen index into the live others list
       (same frozen order — the list only reorders by swapping). */
    target = Math.max(0, Math.min(others.length, target));
    window.__dragDebug = {origin: drag.slotOrigin, slot: drag.slot, startY: drag.startY,
                          pointerY: pointerY, travel: pointerY - drag.startY, slotHeight: slotHeight,
                          target: target, others: others.length, scrollY: window.scrollY,
                          grab: drag.grab};
    /* The Add row lives after the last verse: end drop goes just before it. */
    var endAnchor = document.querySelector('.verse-add') || body.querySelector('.entry__empty');
    var insertBefore = others[target] || endAnchor;

    var alreadyThere = (insertBefore === row.nextElementSibling)
      || (insertBefore === null && row.nextElementSibling === null);
    if (!alreadyThere) {
      /* Keyed by the ELEMENT, never by a data attribute: two rows sharing a key (a
         cloned row, a fixture) collapsed the snapshot to one entry and every row was
         thrown the whole list's height and slid back — the shake this replaced. */
      var before = [];
      verses().forEach(function (item) {
        if (item !== row) before.push([item, item.getBoundingClientRect().top]);
      });
      row.style.transform = 'none';
      body.insertBefore(row, insertBefore);
      drag.slot = target;
      drag.flowTop = row.getBoundingClientRect().top;
      /* The order the person is making is the order they must read (spec 081): the
         numbers renumber as the row crosses, not on release. */
      paintNumbers();
      before.forEach(function (pair) {
        var item = pair[0];
        var was = pair[1];
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

    /* The ghost rides the hand one to one; the real row stays in its slot
       as a tinted placeholder (Sidebar's shape). The others' only motion
       is the morph above, from CSS — 160ms at rest, 60ms mid-drag. */
    positionGhost();

    var edge = 72;
    var step = 0;
    if (pointerY < edge) step = -14;
    else if (pointerY > window.innerHeight - edge) step = 14;
    if (step) { window.scrollBy(0, step); queue(); }
  }

  function endDrag(event) {
    if (!drag) return;
    var current = drag;
    var row = drag.row;
    var collapsed = drag.collapsed;
    var moved = drag.moved;
    if (moved) {
      /* One last placement with the release's own Y, as Sidebar does. */
      if (event && typeof event.clientY === 'number') pointerY = event.clientY;
      var slotHeight = 44;
      var othersEnd = verses().filter(function (item) { return item !== row; });
      if (othersEnd.length) slotHeight = othersEnd[0].getBoundingClientRect().height || 44;
      var target = drag.mids.length;
      for (var i = 0; i < drag.mids.length; i += 1) {
        if (pointerY < drag.mids[i].middle) { target = i; break; }
      }
      target = Math.max(0, Math.min(othersEnd.length, target));
      var endAnchor = document.querySelector('.verse-add') || body.querySelector('.entry__empty');
      var insertBefore = othersEnd[target] || endAnchor;
      if (insertBefore !== row.nextElementSibling) body.insertBefore(row, insertBefore);
      paintNumbers();
    }
    clearGhost(current);
    drag = null;
    document.body.style.userSelect = '';
    row.style.transform = '';
    /** The seam above the slot belongs to the gesture: once the verse is home, the list
        draws its own lines again (the row's own border-top). */
    verses().forEach(function (other) { other.classList.remove('is-seam-above'); });
    numberRows();
    window.setTimeout(function () {
      row.style.transition = '';
      row.style.transform = '';
      if (collapsed && !arranging) {
        setCompact(false);
        numberRows();
      }
      row.classList.remove('is-acts');
    }, 170);
  }
  document.addEventListener('pointerup', endDrag);
  document.addEventListener('pointercancel', function () { if (drag) { var c = drag; clearGhost(c); drag = null; document.body.style.userSelect = ''; c.row.style.transform = ''; c.row.classList.remove('is-acts'); } });
  window.addEventListener('blur', function () { if (drag) { var c = drag; clearGhost(c); drag = null; document.body.style.userSelect = ''; c.row.style.transform = ''; c.row.classList.remove('is-acts'); } });

  document.addEventListener('pointermove', function (event) {
    if (!drag) return;
    pointerY = event.clientY;
    drag.pointerX = event.clientX;
    drag.y = event.clientY;
    /* Sidebar's dead zone (static/web/reorder.js): nothing happens until
       the hand has truly let go of the grip, so a press is still a click. */
    if (!drag.moved && Math.abs(event.clientY - drag.startY) > 3) {
      drag.moved = true;
      makeGhost();
      drag.row.classList.add('is-dragging');
      document.body.classList.add('is-arranging');
      paintNumbers();
    }
    if (!drag.moved) return;
    positionGhost();
    queue();
  }, true);

  /* ---------- the page's own controls -------------------------------------- */

  body.addEventListener('click', function (event) {
    if (event.target.closest('[data-add-verse]')) { openNew(); return; }
    var edit = event.target.closest('.v__edit');
    if (edit) {
      var row = edit.closest('.v');
      if (row) openEdit(row);
    }
  });

  body.addEventListener('pointerdown', function (event) {
    var grip = event.target.closest('.v__grip');
    if (!grip || event.button !== 0) return;
    startDrag(event, grip);
  });

  /* ---------- the control bar ---------------------------------------------- */

  var bar = document.createElement('div');
  bar.className = 'pv-bar';
  bar.setAttribute('role', 'group');
  bar.setAttribute('aria-label', 'Preview states');
  var STATE_LABELS = {longdrag: 'Drag trace'};
  bar.innerHTML = '<span class="pv-bar__label">State</span>'
    + ['rest', 'hover', 'new', 'edit', 'used', 'confirm', 'short', 'longdrag', 'empty',
       'hymn', 'restricted']
      .map(function (name) {
        return '<button type="button" data-state="' + name + '">'
          + (STATE_LABELS[name] || name.charAt(0).toUpperCase() + name.slice(1))
          + '</button>';
      }).join('')
    + '<span class="pv-bar__sep" aria-hidden="true"></span>'
    + '<span class="pv-bar__label">Reorder</span>'
    + '<button type="button" data-state="grab">B \u00b7 Grab collapse \u2014 ships</button>'
    + '<button type="button" data-state="arrange">A \u00b7 Reorder mode \u2014 rejected</button>'
    + '<button type="button" data-card-toggle aria-pressed="false">Card: rides cursor \u2014 ships</button>'
    + '<button type="button" data-long aria-pressed="false">Long song</button>'
    + '<span class="pv-bar__sep" aria-hidden="true"></span>'
    + '<button type="button" data-theme-toggle>Light</button>';
  document.body.appendChild(bar);

  var note = document.createElement('p');
  note.className = 'pv-note';
  note.textContent = DEFAULT_NOTE;
  document.body.appendChild(note);

  bar.addEventListener('click', function (event) {
    var cardButton = event.target.closest('[data-card-toggle]');
    if (cardButton) {
      cardMode = cardMode === 'cursor' ? 'slot' : 'cursor';
      window.__cardMode = cardMode;
      cardButton.setAttribute('aria-pressed', String(cardMode === 'cursor'));
      cardButton.textContent = cardMode === 'slot'
        ? 'Card: rides slot \u2014 rejected' : 'Card: rides cursor \u2014 ships';
      return;
    }
    var longButton = event.target.closest('[data-long]');
    if (longButton) {
      longOn = !longOn;
      longButton.setAttribute('aria-pressed', String(longOn));
      setState(document.body.dataset.previewState || 'rest');
      return;
    }
    var stateButton = event.target.closest('[data-state]');
    if (stateButton) { setState(stateButton.dataset.state); return; }
    var themeButton = event.target.closest('[data-theme-toggle]');
    if (themeButton) {
      var next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      themeButton.textContent = next === 'dark' ? 'Light' : 'Dark';
    }
  });

  root.dataset.theme = 'dark';
  bar.querySelector('[data-theme-toggle]').textContent = 'Light';
  numberRows();
  setState('rest');
})();
