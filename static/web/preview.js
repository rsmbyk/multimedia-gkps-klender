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
  var reset = modal && modal.querySelector('[data-break-reset]');
  var mode = modal && modal.querySelector('[data-break-mode]');
  var modeLabel = modal && modal.querySelector('[data-break-mode-label]');
  if (!modal || typeof modal.showModal !== 'function') return;

  var trigger = null;
  var keyboardOpened = false;
  var origin = null;
  var split = null;
  var breaks = null;
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

  function csrf() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[2]) : '';
  }

  function blockGaps(target) {
    var gaps = [].slice.call(split.querySelectorAll('[data-break-after]'));
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
    if (split.dataset.singleScreen === 'true') return [];
    var result = [];
    var gaps = [].slice.call(split.querySelectorAll('[data-break-after]'));
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
    split.classList.toggle('is-custom', breaks !== null);
    mode.textContent = breaks === null
      ? (split.dataset.singleScreen === 'true' ? 'Default · 1 screen' : 'Default · 2 lines')
      : 'Custom';
    var shown = breaks === null ? defaultBreaks() : breaks;
    split.querySelectorAll('[data-break-after]').forEach(function (gap) {
      var position = Number(gap.dataset.breakAfter);
      var set = shown.indexOf(position) !== -1;
      gap.classList.toggle('is-set', set);
      gap.setAttribute('aria-pressed', set ? 'true' : 'false');
      gap.setAttribute('aria-label', (set ? 'Remove' : 'Add')
        + ' screen break after line ' + position);
      gap.querySelector('[data-break-label]').textContent = set ? 'Remove break' : 'Add break';
    });
  }

  function saveBreaks(next) {
    if (saving) return;
    saving = true;
    var activeSplit = split;
    var error = activeSplit.querySelector('[data-break-error]');
    error.hidden = true;
    activeSplit.querySelectorAll('[data-break-after]').forEach(function (gap) { gap.disabled = true; });
    reset.disabled = true;
    fetch(activeSplit.dataset.saveUrl, {
      method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf()},
      body: JSON.stringify({breaks: next, text_signature: activeSplit.dataset.textSignature})
    }).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok) throw new Error(data.error || 'Could not save screen breaks.');
        return data;
      });
    }).then(function () {
      if (split === activeSplit) {
        breaks = next;
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
      reset.disabled = false;
    });
  }

  function wireSplit() {
    split = content.querySelector('.preview__split');
    reset.hidden = !split || split.dataset.canEdit !== 'true';
    modeLabel.hidden = !split;
    if (!split) return;
    breaks = JSON.parse(split.dataset.screenBreaks);
    if (split.dataset.canEdit !== 'true') {
      split.querySelectorAll('[data-break-after]').forEach(function (gap) { gap.disabled = true; });
    }
    drawBreaks();
  }

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
      wireTabs(content);
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
        if (split.dataset.singleScreen === 'true') {
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

  reset.addEventListener('click', function () { if (split && !saving) saveBreaks(null); });

  modal.addEventListener('click', function (event) {
    if (event.target === modal) modal.close();          /* the backdrop */
  });

  modal.addEventListener('close', function () {
    content.innerHTML = '';
    split = null;
    breaks = null;
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
