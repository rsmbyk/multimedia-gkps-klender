/* Use template (spec 167).
 *
 * The generate modal is two steps: settle every fill-in and choice, then the normal
 * Tata Ibadah form. A slot is resolved by VALIDATING its kind's form -- the same form the
 * page's add rows open -- and nothing is written until Create. The template is never the
 * write target: the resolution lives in this script until the one POST at the end.
 */
(function () {
  'use strict';

  /* The reading shell swaps the stage in place when a sidebar row is opened, so the modal
     this module talks to is not the one it was loaded beside: on a Normal page there is no
     modal at all, and on a template the node is replaced by the next page's. Everything is
     therefore resolved on demand -- nothing is cached across a swap -- and the click that
     opens the modal re-reads the document first. */
  var modal = null;
  var bodyOne, bodyTwo, steps, rows, nextButton, backButton, closeButton, createButton,
      status, nameInput, dateInput, confirmLayer, leaveLayer, summary;
  // the editor dialog is shell-level: it survives a stage swap, so it is read once
  var editorModal = document.getElementById('editorModal');
  var editorContent = document.getElementById('editorContent');
  var opener = null;

  function bindModal() {
    if (modal.dataset.genBound) return;
    modal.dataset.genBound = 'true';
    modal.addEventListener('cancel', function (event) {
      if (escapeHandled) {
        /* the keydown path opened the leave layer; the browser's own cancel must not
           then treat that layer as one to dismiss */
        escapeHandled = false;
        event.preventDefault();
        return;
      }
      if (openChooser) { event.preventDefault(); hideChooser(); }
      else if (!confirmLayer.hidden) { event.preventDefault(); confirmLayer.hidden = true; }
      else if (leaveLayer && !leaveLayer.hidden) { event.preventDefault(); leaveLayer.hidden = true; }
      else if (dirty()) { event.preventDefault(); attemptClose(); }
    });
    /* The backdrop is the dialog's own element: a click there, and not on any layer
       inside it, dismisses the dialog the way Cancel does. */
    modal.addEventListener('click', function (event) {
      if (event.target === modal && !openChooser) attemptClose();
    });
    modal.addEventListener('click', function (event) {
      if (event.target.closest('[data-generate-close]')) attemptClose();
      if (event.target.closest('[data-generate-back]')) { setStep(1); save(); }
      if (event.target.closest('[data-generate-next]') && !nextButton.disabled) { setStep(2); save(); }
      if (event.target.closest('[data-generate-cancel]')) confirmLayer.hidden = true;
      if (event.target.closest('[data-leave-stay]') && leaveLayer) leaveLayer.hidden = true;
      if (event.target.closest('[data-leave-accept]') && leaveLayer) {
        leaveLayer.hidden = true;
        close();
      }
      var accept = event.target.closest('[data-generate-accept]');
      if (accept) submit(accept);
    });
    modal.addEventListener('input', function (event) {
      if (event.target === nameInput) save();
    });
    modal.addEventListener('change', function (event) {
      if (event.target === dateInput) save();
    });
    // the footer's Create opens the confirmation, not the request
    modal.addEventListener('click', function (event) {
      if (!event.target.closest('[data-generate-create]')) return;
      var name = (nameInput.value || '').trim() || modal.dataset.generateName;
      var day = dateInput.value;
      if (!name || !day) {
        status.textContent = !name ? 'The Tata Ibadah needs a name.' : 'Choose a date.';
        return;
      }
      summary.textContent = name + ' · ' + new Date(day + 'T00:00:00')
        .toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
      confirmLayer.hidden = false;
    });
  modal.addEventListener('click', function (event) {
    if (event.target === confirmLayer) { confirmLayer.hidden = true; return; }
    if (leaveLayer && event.target === leaveLayer) { leaveLayer.hidden = true; return; }
    if (openChooser && event.target === openChooser) { hideChooser(); return; }

    var row = event.target.closest('.g-row--slot');
    var setter = event.target.closest('[data-slot-action]');
    if (setter && row) { openKindForm(row); return; }
    var chooserOpen = event.target.closest('[data-choice-open]');
    if (chooserOpen && row) {
      var layer = modal.querySelector('[data-choose="' + slotOf(row) + '"]');
      if (layer) showChooser(layer, chooserOpen);
      return;
    }
    var pick = event.target.closest('[data-choose-pick]');
    if (pick && sync()) {
      /* The chooser is a layer of the modal, not a child of the row: the row is found
         by the id the layer names. */
      var choiceRow = modal.querySelector('[data-choice-row="' + openChooser.dataset.choose + '"]');
      /* The server names the picked option in its own words: a media reads type first,
         then the title or file name that tells it from its neighbours. */
      var pickedRow = pick.closest('.choose__item');
      settled[slotOf(choiceRow)] = {
        label: pickedRow.dataset.pickLabel,
        main: pickedRow.dataset.pickMain,
        mute: pickedRow.dataset.pickMute,
        title: pickedRow.dataset.pickTitle,
        body: pickedRow.dataset.pickBody,
        option: pick.dataset.choosePick
      };
      Array.prototype.forEach.call(openChooser.querySelectorAll('[data-choose-pick]'),
        function (button) { button.setAttribute('aria-pressed', String(button === pick)); });
      refresh();
      save();
      hideChooser();
      return;
    }
    if (event.target.closest('[data-choose-close]')) { hideChooser(); return; }
  });
  }

  /* Re-read the modal when the document's node is a different one. Returns false when the
     page holds no modal at all -- a Normal Tata Ibadah -- so the caller can stay quiet. */
  function sync() {
    var next = document.getElementById('generateModal');
    if (!next || typeof next.showModal !== 'function') { modal = null; return false; }
    if (next !== modal) {
      modal = next;
      bodyOne = modal.querySelector('[data-generate-step="1"]');
      bodyTwo = modal.querySelector('[data-generate-step="2"]');
      steps = Array.prototype.slice.call(modal.querySelectorAll('.generate__steps li'));
      rows = Array.prototype.slice.call(modal.querySelectorAll('.g-row--slot'));
      nextButton = modal.querySelector('[data-generate-next]');
      backButton = modal.querySelector('[data-generate-back]');
      closeButton = modal.querySelector('[data-generate-close]');
      createButton = modal.querySelector('[data-generate-create]');
      status = modal.querySelector('[data-generate-status]');
      nameInput = modal.querySelector('[data-generate-name-input]');
      dateInput = modal.querySelector('[data-generate-date]');
      confirmLayer = modal.querySelector('[data-generate-confirm]');
      leaveLayer = modal.querySelector('[data-generate-leave]');
      summary = modal.querySelector('[data-generate-summary]');
      editorModal = document.getElementById('editorModal');
      editorContent = document.getElementById('editorContent');
      settled = {};
      bindModal();
    }
    return true;
  }
  var settled = {};
  var pendingSlot = null;         // the row whose kind form is open, if any
  var openChooser = null;
  var chooserOpener = null;
  var escapeHandled = false;   // the keydown path already answered this Escape

  /* ---------- progress kept for this template on this browser, for seven days ---------- */
  /* One key per template: two templates never share work, and a Create clears only the
     template it generated. localStorage outlives the browser session; savedAt carries the
     seven-day rule because the web storage API has no expiry of its own. Storage is
     best-effort -- a browser that refuses it still gets a working modal, just no resume. */
  var STORAGE_PREFIX = 'gkps:generate:';
  var LIFETIME = 7 * 24 * 60 * 60 * 1000;

  function storageKey() {
    return modal && modal.dataset.generateTatib
      ? STORAGE_PREFIX + modal.dataset.generateTatib : '';
  }
  function liveRecord(id) {
    if (!id) return null;
    var key = STORAGE_PREFIX + id;
    try {
      var raw = window.localStorage.getItem(key);
      if (!raw) return null;
      var value = JSON.parse(raw);
      if (!value || value.v !== 2 || !value.savedAt ||
          !value.settled || typeof value.settled !== 'object') return null;
      if (Date.now() - value.savedAt > LIFETIME) {
        window.localStorage.removeItem(key);
        return null;
      }
      return value;
    } catch (error) { return null; }
  }
  function save() {
    var key = storageKey();
    try {
      window.localStorage.setItem(key, JSON.stringify({
        v: 2,
        step: Number(modal.dataset.step || 1),
        settled: settled,
        name: nameInput ? nameInput.value : '',
        date: dateInput ? dateInput.value : '',
        savedAt: Date.now()
      }));
    } catch (error) { /* storage unavailable: the modal itself still works */ }
    paintMark();
  }
  function saved() {
    return modal && modal.dataset.generateTatib
      ? liveRecord(modal.dataset.generateTatib) : null;
  }
  function clearSaved() {
    var key = storageKey();
    try { if (key) window.localStorage.removeItem(key); } catch (error) {}
    try { if (key) window.sessionStorage.removeItem(key); } catch (error) {}
    paintMark();
  }
  /* A record left unopened would otherwise sit in storage for ever, and the button mark is
     read from storage: an expired key would paint a mark the modal then refuses to restore. */
  function pruneExpired() {
    try {
      for (var i = window.localStorage.length - 1; i >= 0; i--) {
        var key = window.localStorage.key(i);
        if (!key || key.indexOf(STORAGE_PREFIX) !== 0) continue;
        var value = null;
        try { value = JSON.parse(window.localStorage.getItem(key)); } catch (error) {}
        if (!value || value.v !== 2 || !value.savedAt ||
            Date.now() - value.savedAt > LIFETIME) {
          window.localStorage.removeItem(key);
        }
      }
    } catch (error) { /* storage unavailable: nothing to sweep */ }
  }
  /* The stage's Use template button says a draft exists before the modal is opened. The dot
     is aria-hidden; the accessible name carries the state so the mark is not colour-only. */
  function paintMark() {
    var button = document.querySelector('[data-generate-open]');
    if (!button) return;
    if (liveRecord(button.dataset.generateTatib)) {
      button.dataset.draft = 'true';
      button.setAttribute('aria-label', 'Use template, draft saved');
    } else {
      if (button.dataset.draft) delete button.dataset.draft;
      button.removeAttribute('aria-label');
    }
  }
  function dirty() {
    return settledCount() > 0 || !!saved();
  }

  /* The step badge centres its digit by the glyph's ink, not by the line box: a lining
     figure sits high in its line box and `1` carries a wide left bearing, and how far off
     that is depends on the font -- so it is measured here instead of guessed in CSS (a
     constant nudge is only right for one font at one device-pixel ratio). Canvas reports
     the ink box of the same text in the same font, and the line box's baseline comes from
     the font's own ascent and descent. */
  function centreDigit(mark) {
    var text = (mark.textContent || '').trim();
    if (!text || mark.querySelector('svg')) {
      // the check is drawn symmetric about its own box, so it needs no lift -- and it must
      // not inherit the numeral's, which is still on the element from the step before
      mark.style.transform = '';
      return;
    }
    var style = getComputedStyle(mark);
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    if (!context || !context.measureText) return;
    context.font = style.fontStyle + ' ' + style.fontWeight + ' ' + style.fontSize
      + ' ' + style.fontFamily;
    var metrics = context.measureText(text);
    var size = parseFloat(style.fontSize);
    if (!size || metrics.actualBoundingBoxAscent === undefined) return;

    var inkLeft = metrics.actualBoundingBoxLeft || 0;
    var inkRight = metrics.actualBoundingBoxRight || 0;
    var inkAscent = metrics.actualBoundingBoxAscent || 0;
    var inkDescent = metrics.actualBoundingBoxDescent || 0;
    var fontAscent = metrics.fontBoundingBoxAscent || inkAscent;
    var fontDescent = metrics.fontBoundingBoxDescent || inkDescent;

    // line-height is 1: the box is the font size, the baseline sits half-leading down
    var halfLeading = (size - (fontAscent + fontDescent)) / 2;
    var baseline = halfLeading + fontAscent;
    var inkCentreY = baseline - (inkAscent - inkDescent) / 2;
    /* Vertically the ink box is what the eye centres. Horizontally it is not: `1` is a
       narrow stem with a flag reaching left, so centring its ink box pushes the stem right
       and the numeral reads off-centre. The font centres each digit in its own advance, so
       the advance is left alone. */
    var dx = 0;
    var dy = (size / 2) - inkCentreY;
    if (!isFinite(dx) || !isFinite(dy)) return;
    mark.style.transform = 'translate(' + dx.toFixed(2) + 'px,' + dy.toFixed(2) + 'px)';
  }

  /* The label's capitals must meet the badge's centre. How far the ink of capitals sits
     above its line box is a fact about the font this browser resolved -- the app asks for
     ui-sans-serif, and every platform answers with something else -- so it is measured
     here, exactly like the digit. The stylesheet's em lift is only the no-script fallback. */
  function centreLabel(label) {
    var mark = label.parentElement.querySelector('.generate__step-mark');
    var text = (label.textContent || '').trim();
    if (!mark || !text) return;
    label.style.transform = '';                 // measure the box, not the previous shift
    var box = label.getBoundingClientRect();
    var circle = mark.getBoundingClientRect();
    // a closed dialog measures nothing: skip until it is on screen
    if (!box.height || !circle.height) return;
    // the stylesheet's fallback lift is already in this box, so the measurement is the
    // extra it needs on top of that, not the whole shift
    var applied = 0;
    var current = getComputedStyle(label).transform;
    if (current && current !== 'none') applied = new DOMMatrixReadOnly(current).m42 || 0;
    var style = getComputedStyle(label);
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    if (!context || !context.measureText) return;
    context.font = style.fontStyle + ' ' + style.fontWeight + ' ' + style.fontSize
      + ' ' + style.fontFamily;
    var metrics = context.measureText(text);
    if (metrics.actualBoundingBoxAscent === undefined) return;
    var size = parseFloat(style.fontSize);
    var lineHeight = parseFloat(style.lineHeight) || size * 1.2;
    if (!size) return;
    var fontAscent = metrics.fontBoundingBoxAscent || metrics.actualBoundingBoxAscent;
    var fontDescent = metrics.fontBoundingBoxDescent || 0;
    var halfLeading = (lineHeight - (fontAscent + fontDescent)) / 2;
    var inkAscent = metrics.actualBoundingBoxAscent || fontAscent;
    var inkCentre = box.y + halfLeading + fontAscent - (inkAscent / 2);
    var delta = ((circle.y + circle.height / 2) - inkCentre) + applied;
    if (!isFinite(delta) || Math.abs(delta) > 6) return;
    label.style.transform = 'translateY(' + delta.toFixed(2) + 'px)';
  }

  function centreSteps() {
    Array.prototype.forEach.call(document.querySelectorAll('.generate__steps li .generate__step-mark i'),
                                 centreDigit);
    Array.prototype.forEach.call(document.querySelectorAll('.generate__step-label'), centreLabel);
  }

  function slotOf(row) { return row.dataset.slotRow; }

  function csrfToken() {
    var match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }

  function nearestSunday() {
    var today = new Date();
    var day = new Date(today.getTime());
    day.setDate(today.getDate() + ((7 - today.getDay()) % 7));
    return day.toISOString().slice(0, 10);
  }
  function isChoice(row) { return row.dataset.slotKindName === 'choice'; }

  function settledCount() { return Object.keys(settled).length; }

  /* The picked option's quiet detail -- a file name under its type, the verses under a
     song -- is a step back from the name it belongs to. */
  function paintValue(value, state) {
    value.textContent = '';
    if (state.body) {
      /* A chosen prayer keeps its two parts apart: the title it was given reads as a
         name, the words under it as the quiet line of a body. */
      value.classList.add('g-value--text');
      if (state.title) {
        var title = document.createElement('span');
        title.className = 'g-value-title';
        title.textContent = state.title;
        value.appendChild(title);
      }
      var words = document.createElement('span');
      words.className = 'g-value-body';
      words.textContent = state.body;
      value.appendChild(words);
      return;
    }
    if (!state.mute) { value.textContent = state.label; return; }
    var main = document.createElement('span');
    main.className = 'g-value-main';
    main.textContent = state.main;
    var mute = document.createElement('span');
    mute.className = 'g-value-mute';
    mute.textContent = state.mute;
    value.appendChild(main);
    value.appendChild(document.createTextNode(' · '));
    value.appendChild(mute);
  }

  function refresh() {
    /* The rows are re-read every time: the dialog's markup can be replaced under the
       script (an in-page swap), and a stale list counted a row that no longer existed --
       a page of settled rows still said "1 left to fill in". */
    rows = Array.prototype.slice.call(modal.querySelectorAll('.g-row--slot'));
    var total = rows.length;
    var done = settledCount();
    rows.forEach(function (row) {
      var state = settled[slotOf(row)];
      row.dataset.set = state ? 'true' : 'false';
      var value = row.querySelector('[data-slot-value]');
      var action = row.querySelector('[data-slot-action], [data-choice-open]');
      if (!value || !action) return;
      if (isChoice(row)) {
        var count = Number(row.dataset.choiceCount || 0);
        if (state) {
          paintValue(value, state);
          action.textContent = 'Change';
        } else if (!count) {
          value.textContent = 'No options yet';
          action.textContent = 'No options';
        } else {
          value.textContent = count + (count === 1 ? ' option' : ' options');
          action.textContent = 'Choose';
        }
        return;
      }
      value.textContent = state ? state.label : 'Not set';
      action.textContent = state ? 'Change' : 'Set';
    });
    var left = total - done;
    status.textContent = total === 0
      ? 'This template holds no fill-in and no choice: create it as it is.'
      : (left === 0
        ? 'All ' + total + ' ' + (total === 1 ? 'entry' : 'entries') + ' settled.'
        : done + ' of ' + total + ' settled — ' + left + ' left to fill in' +
          (emptyChoice() ? ' · one choice has no options' : '') + '.');
    nextButton.disabled = left !== 0;
  }

  function emptyChoice() {
    return rows.some(function (row) {
      var action = row.querySelector('[data-choice-open]');
      return isChoice(row) && action && action.disabled;
    });
  }

  function setStep(step) {
    modal.dataset.step = String(step);
    bodyOne.hidden = step !== 1;
    bodyTwo.hidden = step !== 2;
    steps.forEach(function (item) {
      var done = step === 2 && item.dataset.step === '1';
      item.toggleAttribute('data-done', done);
      var mark = item.querySelector('.generate__step-mark i');
      mark.innerHTML = done
        ? '<svg viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M2.5 6.3 4.8 8.6 9.5 3.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        : item.dataset.step;
      if (item.dataset.step === String(step)) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
      centreDigit(mark);
    });
    nextButton.hidden = step === 2;
    backButton.hidden = step !== 2;
    createButton.hidden = step !== 2;
  }

  function syncDateLabel() {
    var label = modal.querySelector('[data-date-picker-label]');
    if (!label || !dateInput || !dateInput.value) return;
    /* the same wording the New Tata Ibadah modal's picker prints: '1 November 2026',
       not a short month only this dialog would show */
    var day = new Date(dateInput.value + 'T00:00:00');
    label.textContent = window.gkpsDateLabel
      ? window.gkpsDateLabel(day)
      : day.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  /* A saved record re-applies to the dialog that is open now: slot ids that are no
     longer in this template are dropped, so an edited template never paints a row
     that does not exist or counts one that was removed. */
  function reset(state) {
    rows = Array.prototype.slice.call(modal.querySelectorAll('.g-row--slot'));
    settled = {};
    if (state) {
      Object.keys(state.settled).forEach(function (id) {
        if (rows.some(function (row) { return slotOf(row) === id; })) {
          settled[id] = state.settled[id];
        }
      });
    }
    setStep(state && Number(state.step) === 2 ? 2 : 1);
    if (nameInput) nameInput.value = (state && state.name) || modal.dataset.generateName || '';
    if (dateInput) dateInput.value = (state && state.date) || nearestSunday();
    syncDateLabel();
    rows.forEach(function (row) { row.dataset.set = 'false'; });
    /* the choosers keep their own marks: every row's picked option must match the
       state just applied, so a fresh open starts them all at false */
    Array.prototype.forEach.call(modal.querySelectorAll('[data-choose-pick]'), function (button) {
      button.setAttribute('aria-pressed', 'false');
    });
    if (state) {
      Object.keys(settled).forEach(function (id) {
        var chosen = settled[id].option;
        if (!chosen) return;
        var layer = modal.querySelector('[data-choose="' + id + '"]');
        if (!layer) return;
        Array.prototype.forEach.call(layer.querySelectorAll('[data-choose-pick]'), function (button) {
          button.setAttribute('aria-pressed', String(Number(button.dataset.choosePick) === Number(chosen)));
        });
      });
    }
    refresh();
  }

  function open() {
    if (!sync()) return;
    reset(saved());
    modal.showModal();
    // the labels are measured against the badge, so only once the dialog has a box
    window.requestAnimationFrame(centreSteps);
    var first = modal.querySelector('[data-slot-action], [data-choice-open]:not([disabled])');
    if (first) first.focus();
  }

  function close() {
    hideChooser();
    confirmLayer.hidden = true;
    if (leaveLayer) leaveLayer.hidden = true;
    if (modal.open) modal.close();
    if (opener && document.contains(opener)) opener.focus();
  }

  /* Cancel, the backdrop and the cancel event all ask here before dismissal. The
     record is already written, so Leave only closes; Stay keeps the dialog in place. */
  function attemptClose() {
    hideChooser();
    if (confirmLayer) confirmLayer.hidden = true;
    if (dirty() && leaveLayer) { leaveLayer.hidden = false; return; }
    close();
  }

  /* ---------- a slot's kind form: fetched, validated, never saved ------------------ */
  function openKindForm(row) {
    if (!window.gkpsEntry || !window.gkpsEntry.openSlotForm) return;
    var validate = (editorModal.dataset.entryValidateUrl || '/editor/entry/validate/');
    pendingSlot = slotOf(row);
    window.gkpsEntry.openSlotForm(row.dataset.slotKind,
                                  modal.dataset.generateTatib || '',
                                  slotOf(row), validate);
  }

  document.addEventListener('editor:saved', function (event) {
    var detail = event.detail || {};
    if (!pendingSlot || !detail.value) return;   /* a page add, not a slot resolution */
    var target = pendingSlot;
    settled[target] = {
      label: [detail.value.line, detail.value.meta].filter(Boolean).join(' · '),
      data: detail.data
    };
    pendingSlot = null;
    refresh();
    save();
  });

  // dismissed without resolving: the row stays unsettled. Deferred, because the editor
  // dispatches `editor:saved` straight after close() and that event needs the target.
  editorModal.addEventListener('close', function () {
    window.setTimeout(function () { pendingSlot = null; }, 0);
  });

  /* ---------- the chooser: a layer that closes itself, not the modal -------------- */
  function showChooser(layer, from) {
    hideChooser();
    layer.hidden = false;
    openChooser = layer;
    chooserOpener = from;
    var first = layer.querySelector('[data-choose-pick]');
    if (first) first.focus();
  }
  function hideChooser() {
    if (!openChooser) return;
    openChooser.hidden = true;
    openChooser = null;
    if (chooserOpener && document.contains(chooserOpener)) chooserOpener.focus();
    chooserOpener = null;
  }


  document.addEventListener('click', function (event) {
    var generateOpen = event.target.closest('[data-generate-open]');
    if (!generateOpen) return;
    event.preventDefault();
    opener = generateOpen;
    open();
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape' || !modal || !modal.open) return;
    if (openChooser) return;   // the chooser's own handler owns Escape
    if (!confirmLayer.hidden || (leaveLayer && !leaveLayer.hidden)) return;
    /* A modal dialog fires `cancel` on Escape only while focus is inside it. After a
       slot form saves, focus can land on the body, and the dialog stays open with no
       answer at all. Handle that case here; the flag stops the `cancel` event that
       follows when focus is inside from dismissing the layer just opened. */
    escapeHandled = true;
    event.preventDefault();
    attemptClose();
    window.setTimeout(function () { escapeHandled = false; }, 0);
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape' || !openChooser) return;
    /* A chooser can be covered by another dialog -- the Preview opened from one of its
       rows, say. Escape belongs to that dialog then: swallowing it here left the preview
       open and closed this modal instead. */
    if (modal && !modal.open) return;
    if (document.querySelectorAll('dialog[open]').length > 1) return;
    event.preventDefault();
    hideChooser();
  });

  function submit(button) {
    var name = (nameInput.value || '').trim() || modal.dataset.generateName;
    var slots = rows.map(function (row) {
      var state = settled[slotOf(row)] || {};
      var entry = { entry: Number(slotOf(row)) };
      if (isChoice(row)) entry.option = Number(state.option || 0);
      else entry.data = state.data || {};
      return entry;
    });
    button.disabled = true;
    fetch(modal.dataset.generateUrl, {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken() },
      body: JSON.stringify({ name: name, date: dateInput.value, slots: slots })
    }).then(function (response) {
      return response.json().then(function (data) { return { ok: response.ok, data: data }; });
    }).then(function (result) {
      button.disabled = false;
      if (!result.ok) {
        status.textContent = (result.data && result.data.error) || 'The service could not be created.';
        confirmLayer.hidden = true;
        return;
      }
      clearSaved();
      window.location.href = result.data.url;
    }).catch(function () {
      button.disabled = false;
      status.textContent = 'The service could not be created.';
    });
  }

  if (sync()) refresh();
  pruneExpired();
  paintMark();
  /* The reading shell swaps the stage in place; the new button must get its mark at once. */
  document.addEventListener('shell:page', function () {
    pruneExpired();
    paintMark();
  });
  centreSteps();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(centreSteps);
})();
