/* The entry preview (spec 032; editable Text breaks in spec 069).
 *
 * The pane's Preview button copies the entry's inline payload into
 * the dialog, which owns no header and scrolls its body.
 * Esc closes it (native <dialog>), as does a click on the overlay. Focus returns to the
 * trigger without leaving a row outline (spec 025). While open, the entry that owns
 * the trigger keeps its hover look behind the backdrop (spec 065).
 */
(function () {
  'use strict';

  var modal = document.getElementById('previewModal');
  var content = document.getElementById('previewContent');
  var head = modal && modal.querySelector('[data-preview-head]');
  var headTitle = modal && modal.querySelector('#previewTitle');
  var tabsHost = modal && modal.querySelector('[data-preview-tabs-host]');
  var footer = modal && modal.querySelector('[data-screen-mode-footer]');
  var modeControl = modal && modal.querySelector('[data-preview-screen-mode]');
  var readonlyMode = modal && modal.querySelector('[data-mode-readonly]');
  var confirmLayer = modal && modal.querySelector('[data-mode-confirm]');
  var confirmTitle = modal && modal.querySelector('[data-confirm-title]');
  var confirmCancel = modal && modal.querySelector('[data-confirm-cancel]');
  var confirmAccept = modal && modal.querySelector('[data-confirm-accept]');
  if (!modal || typeof modal.showModal !== 'function') return;

  var trigger = null;
  var keyboardOpened = false;
  var origin = null;
  var split = null;
  var breaks = null;
  var defaultMode = 'multi_line';
  var pendingMode = null;
  var pendingButton = null;
  var saving = false;
  var focusTools = window.gkpsFocus || {
    restoreQuietly: function (target) {
      if (target) target.focus({ preventScroll: true });
    }
  };

  function wireTabs(scope) {
    var tabs = [].slice.call(scope.querySelectorAll('.preview__tab'));
    if (!tabs.length) return;
    var panels = [].slice.call(scope.querySelectorAll('.preview__panel'));
    tabs.forEach(function (tab, index) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (each, i) {
          each.setAttribute('aria-selected', i === index ? 'true' : 'false');
          each.tabIndex = i === index ? 0 : -1;
        });
        panels.forEach(function (panel, i) { panel.hidden = i !== index; });
      });
    });
  }

  /* The entry's identity leaves the scroller for the dialog's header (spec 085): whatever the
     payload renders as its reference or heading, and a song's verse tabs with it. An entry with
     nothing to name -- an untitled Text -- keeps the headerless dialog it has always had. */
  function liftIdentity() {
    var identity = content.querySelector('.preview__ref, .preview__song');
    var tabs = content.querySelector('.preview__tabs');
    head.hidden = !identity && !tabs;
    headTitle.textContent = identity ? identity.textContent : '';
    headTitle.hidden = !identity;
    if (identity) identity.remove();
    tabsHost.innerHTML = '';
    tabsHost.hidden = !tabs;
    if (tabs) tabsHost.appendChild(tabs);
    if (identity) {
      modal.setAttribute('aria-labelledby', 'previewTitle');
      modal.removeAttribute('aria-label');
    } else {
      modal.removeAttribute('aria-labelledby');
      modal.setAttribute('aria-label', 'Preview');
    }
  }

  function csrf() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[2]) : '';
  }

  function blockGaps(target) {
    var gaps = [].slice.call(split.querySelectorAll('[data-break-after]:not([hidden])'));
    var at = gaps.indexOf(target), start = at, end = at;
    while (start > 0 && Number(gaps[start - 1].dataset.breakAfter) + 1
           === Number(gaps[start].dataset.breakAfter)) start--;
    while (end < gaps.length - 1 && Number(gaps[end].dataset.breakAfter) + 1
           === Number(gaps[end + 1].dataset.breakAfter)) end++;
    return gaps.slice(start, end + 1).map(function (gap) {
      return Number(gap.dataset.breakAfter);
    });
  }

  function defaultBreaks() {
    if (defaultMode === 'single_screen') return [];
    var result = [];
    var gaps = [].slice.call(split.querySelectorAll('[data-break-after]:not([hidden])'));
    gaps.forEach(function (gap, index) {
      var current = Number(gap.dataset.breakAfter);
      var previous = index && Number(gaps[index - 1].dataset.breakAfter);
      var start = index === 0 || previous + 1 !== current;
      if (start) gap.dataset.blockFirst = String(current);
      else gap.dataset.blockFirst = gaps[index - 1].dataset.blockFirst;
      if ((current - Number(gap.dataset.blockFirst)) % 2 === 1) result.push(current);
    });
    return result;
  }

  function drawBreaks() {
    if (!split) return;
    split.querySelectorAll('[data-break-after]').forEach(function (gap) {
      gap.hidden = defaultMode === 'multi_line' && gap.dataset.multiBoundary !== 'true';
    });
    split.classList.toggle('is-custom', breaks !== null);
    var selected = breaks === null ? defaultMode : 'custom';
    modeControl.dataset.selected = selected;
    modeControl.querySelectorAll('[data-preview-mode]').forEach(function (button) {
      button.setAttribute('aria-pressed', button.dataset.previewMode === selected ? 'true' : 'false');
    });
    readonlyMode.textContent = selected === 'custom' ? 'Custom breaks'
      : selected === 'single_screen' ? 'Single-screen' : 'Multi-line';
    var shown = breaks === null ? defaultBreaks() : breaks;
    split.querySelectorAll('[data-break-after]:not([hidden])').forEach(function (gap) {
      var position = Number(gap.dataset.breakAfter);
      var set = shown.indexOf(position) !== -1;
      gap.classList.toggle('is-set', set);
      gap.setAttribute('aria-pressed', set ? 'true' : 'false');
      gap.setAttribute('aria-label', (set ? 'Remove' : 'Add')
        + ' screen break after line ' + position);
      gap.querySelector('[data-break-label]').textContent = set ? 'Remove break' : 'Add break';
    });
  }

  function saveBreaks(next, nextMode) {
    if (saving) return;
    saving = true;
    var activeSplit = split;
    var error = activeSplit.querySelector('[data-break-error]');
    error.hidden = true;
    activeSplit.querySelectorAll('[data-break-after]').forEach(function (gap) { gap.disabled = true; });
    modeControl.querySelectorAll('button').forEach(function (button) { button.disabled = true; });
    fetch(activeSplit.dataset.saveUrl, {
      method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf()},
      body: JSON.stringify({breaks: next, default_screen_mode: nextMode || defaultMode,
        text_signature: activeSplit.dataset.textSignature,
        screen_state_signature: activeSplit.dataset.screenStateSignature})
    }).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok) throw new Error(data.error || 'Could not save screen breaks.');
        return data;
      });
    }).then(function (data) {
      if (split === activeSplit) {
        breaks = next;
        defaultMode = data.default_screen_mode;
        activeSplit.dataset.screenStateSignature = data.screen_state_signature;
        var notice = activeSplit.querySelector('.preview__notice');
        if (notice) notice.remove();
        drawBreaks();
      }
      document.dispatchEvent(new CustomEvent('editor:saved', {detail: {kind: 'entry'}}));
    }).catch(function (failure) {
      if (split === activeSplit) {
        error.textContent = failure.message;
        error.hidden = false;
      }
    }).finally(function () {
      saving = false;
      if (split === activeSplit) {
        activeSplit.querySelectorAll('[data-break-after]').forEach(function (gap) {
          gap.disabled = false;
        });
      }
      modeControl.querySelectorAll('button').forEach(function (button) { button.disabled = false; });
    });
  }

  function wireSplit() {
    split = content.querySelector('.preview__split');
    footer.hidden = !split;
    if (!split) return;
    breaks = JSON.parse(split.dataset.screenBreaks);
    defaultMode = split.dataset.defaultScreenMode;
    var canEdit = split.dataset.canEdit === 'true';
    modeControl.hidden = !canEdit;
    readonlyMode.hidden = canEdit;
    if (!canEdit) {
      split.querySelectorAll('[data-break-after]').forEach(function (gap) { gap.disabled = true; });
    }
    drawBreaks();
  }

  content.addEventListener('click', function (event) {
    var control = event.target.closest('button, a, input, select, textarea, [tabindex], '
      + '[contenteditable="true"]');
    if (!control || control === content) content.focus({ preventScroll: true });
  });

  content.addEventListener('keydown', function (event) {
    if (event.target !== content) return;
    var atTop = content.scrollTop <= 0;
    var atBottom = content.scrollTop >= content.scrollHeight - content.clientHeight - 1;
    if (((event.key === 'ArrowUp' || event.key === 'PageUp') && atTop)
        || ((event.key === 'ArrowDown' || event.key === 'PageDown') && atBottom)) {
      event.preventDefault();
    }
  });

  document.addEventListener('click', function (event) {
    var opener = event.target.closest('[data-preview-open]');
    if (opener) {
      event.preventDefault();
      trigger = opener;
      keyboardOpened = event.detail === 0;
      var anchor = opener.dataset.previewFor;
      var data = anchor && document.querySelector(
        '.entry__preview-src[data-preview-for="' + anchor + '"]');
      content.innerHTML = data ? data.textContent : '';
      liftIdentity();
      /* the scope is the whole dialog: a song's tabs live in the header, its panels in the body */
      wireTabs(modal);
      wireSplit();
      if (!modal.open) {
        modal.showModal();
        origin = opener.closest('.tatib__item, .tatib__eos');
        if (origin) origin.classList.add('is-modal-origin');
      }
      return;
    }
    var gap = event.target.closest('[data-break-after]');
    if (gap && split && split.contains(gap) && split.dataset.canEdit === 'true') {
      var position = Number(gap.dataset.breakAfter);
      var current = breaks === null ? defaultBreaks() : breaks.slice();
      var index = current.indexOf(position);
      if (index !== -1) current.splice(index, 1);
      else if (breaks === null) {
        if (defaultMode === 'single_screen') {
          current = [position];
        } else {
          var block = blockGaps(gap);
          current = current.filter(function (value) { return block.indexOf(value) === -1; });
          block.forEach(function (value) {
            if (Math.abs(value - position) % 2 === 0) current.push(value);
          });
        }
        current.sort(function (a, b) { return a - b; });
      } else current.push(position);
      current.sort(function (a, b) { return a - b; });
      saveBreaks(current);
    }
  });

  modeControl.addEventListener('click', function (event) {
    var button = event.target.closest('[data-preview-mode]');
    if (!button || !split || saving || split.dataset.canEdit !== 'true') return;
    var targetMode = button.dataset.previewMode;
    if (breaks === null) {
      if (targetMode !== defaultMode) saveBreaks(null, targetMode);
      return;
    }
    pendingMode = targetMode;
    pendingButton = button;
    confirmTitle.textContent = 'Switch to '
      + (targetMode === 'single_screen' ? 'Single-screen' : 'Multi-line') + '?';
    confirmLayer.hidden = false;
    confirmCancel.focus();
  });

  function cancelConfirmation() {
    confirmLayer.hidden = true;
    pendingMode = null;
    if (pendingButton) pendingButton.focus();
    pendingButton = null;
  }

  confirmCancel.addEventListener('click', cancelConfirmation);
  confirmAccept.addEventListener('click', function () {
    var nextMode = pendingMode;
    cancelConfirmation();
    if (nextMode) saveBreaks(null, nextMode);
  });
  modal.addEventListener('keydown', function (event) {
    if (confirmLayer.hidden) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
      cancelConfirmation();
    } else if (event.key === 'Tab') {
      if (event.shiftKey && document.activeElement === confirmCancel) {
        event.preventDefault(); confirmAccept.focus();
      } else if (!event.shiftKey && document.activeElement === confirmAccept) {
        event.preventDefault(); confirmCancel.focus();
      }
    }
  });
  modal.addEventListener('cancel', function (event) {
    if (!confirmLayer.hidden) { event.preventDefault(); cancelConfirmation(); }
  });

  modal.addEventListener('click', function (event) {
    if (event.target === modal && confirmLayer.hidden) modal.close();
  });

  modal.addEventListener('close', function () {
    content.innerHTML = '';
    head.hidden = true;
    headTitle.textContent = '';
    tabsHost.innerHTML = '';
    tabsHost.hidden = true;
    modal.removeAttribute('aria-labelledby');
    modal.setAttribute('aria-label', 'Preview');
    split = null;
    breaks = null;
    confirmLayer.hidden = true;
    pendingMode = null;
    pendingButton = null;
    if (origin) origin.classList.remove('is-modal-origin');
    origin = null;
    if (trigger && document.contains(trigger)) {
      if (keyboardOpened) {
        trigger.classList.remove('focus-restore-quiet');
        trigger.focus({ preventScroll: true });
      } else {
        focusTools.restoreQuietly(trigger);
      }
    }
    keyboardOpened = false;
    trigger = null;
  });
})();
