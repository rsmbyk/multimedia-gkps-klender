/* Sidebar editors (spec 005).
 *
 * One modal, three record kinds. The form is fetched from the server (empty for a
 * new record, prefilled when editing) and posted back with fetch; a 400 answer is
 * the server's re-rendered form -- errors included -- so the validation lives in
 * one place. A successful save refreshes the shell's regions in place, so the
 * lists, panel selection and reading stage agree without a reload.
 */
(function () {
  'use strict';

  var modal = document.getElementById('editorModal');
  if (!modal || typeof modal.showModal !== 'function') return;
  var content = document.getElementById('editorContent');
  var status = document.getElementById('editorStatus');
  var feedback = window.gkpsEditFeedback;
  if (feedback) feedback.guardDialog(modal);
  var trigger = null;
  var pendingFormLoad = null;
  var focusTools = window.gkpsFocus || {
    restoreQuietly: function (target) {
      if (!target) return;
      target.classList.add('focus-restore-quiet');
      target.focus({ preventScroll: true });
    }
  };

  function canOpenEditor() {
    return !pendingFormLoad && !modal.open;
  }

  function invalidateFormLoad() {
    if (!pendingFormLoad) return;
    var request = pendingFormLoad;
    pendingFormLoad = null;
    modal.classList.remove('is-loading');
    if (request.controller) {
      try { request.controller.abort(); } catch (error) { /* The request identity is enough. */ }
    }
  }

  function renderLoading(title) {
    var body = document.createElement('div');
    body.className = 'editor__body editor__body--loading';

    var heading = document.createElement('h2');
    heading.className = 'editor__title editor__loading-title';
    heading.id = 'editorTitle';
    heading.textContent = title;

    var loading = document.createElement('div');
    loading.className = 'editor__loading';
    loading.setAttribute('role', 'status');
    loading.setAttribute('aria-live', 'polite');

    var spinner = document.createElement('span');
    spinner.className = 'editor__loading-spinner';
    spinner.setAttribute('aria-hidden', 'true');

    var label = document.createElement('span');
    label.className = 'editor__loading-label';
    label.textContent = 'Loading editor…';
    loading.append(spinner, label);

    var actions = document.createElement('div');
    actions.className = 'editor__actions';
    var cancel = document.createElement('button');
    cancel.className = 'editor__cancel';
    cancel.type = 'button';
    cancel.dataset.editorClose = '';
    cancel.textContent = 'Cancel';
    actions.appendChild(cancel);

    body.append(heading, loading, actions);
    content.replaceChildren(body);
    return cancel;
  }

  function loadEditorForm(options) {
    if (!canOpenEditor()) return false;

    var controller = typeof AbortController === 'function' ? new AbortController() : null;
    var request = { controller: controller, onLoad: options.onLoad, onFailure: options.onFailure };
    pendingFormLoad = request;
    modal.classList.add('is-loading');
    var cancel = renderLoading(options.title);
    modal.showModal();
    cancel.focus();

    var fetchOptions = {
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'fetch' }
    };
    if (controller) fetchOptions.signal = controller.signal;

    fetch(options.url, fetchOptions).then(function (response) {
      if (response.status === 403) throw new Error('forbidden');
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.text().then(function (html) {
        if (!html.trim()) throw new Error('empty');
        return html;
      });
    }).then(function (html) {
      if (pendingFormLoad !== request || !modal.open) return;
      pendingFormLoad = null;
      modal.classList.remove('is-loading');
      try {
        request.onLoad(html);
      } catch (error) {
        if (modal.open) modal.close();
        request.onFailure(error);
      }
    }).catch(function (error) {
      if (pendingFormLoad !== request) return;
      pendingFormLoad = null;
      modal.classList.remove('is-loading');
      if (modal.open) modal.close();
      request.onFailure(error);
    });
    return true;
  }

  /* Sidebar and entry editors share one dialog, so they also share one request
     identity. Publish this before entries.js is loaded. */
  window.gkpsEditorLoadForm = {
    canOpen: canOpenEditor,
    open: loadEditorForm
  };
  modal.addEventListener('cancel', invalidateFormLoad);
  modal.addEventListener('close', invalidateFormLoad);
  modal.addEventListener('click', function (event) {
    if (pendingFormLoad && (event.target === modal
        || event.target.closest('[data-editor-close]'))) invalidateFormLoad();
  }, true);

  function urlFor(kind, id, book) {
    var pattern = modal.dataset.editorNew;
    if (id) pattern = modal.dataset.editorEdit.replace('/0/', '/' + id + '/');
    var url = pattern.replace('KIND', kind);
    if (!id && book) url += '?book=' + encodeURIComponent(book);
    return url;
  }

  function csrfToken() {
    var match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }

  function announce(message) {
    if (status) status.textContent = message || '';
  }

  function close() {
    if (feedback && feedback.isDialogBusy(modal)) return;
    if (modal.open) modal.close();
  }

  function open(kind, id, book) {
    announce('');
    var nouns = { songbook: 'songbook', song: 'song', tatib: 'Tata Ibadah' };
    return window.gkpsEditorLoadForm.open({
      url: urlFor(kind, id, book),
      title: (id ? 'Edit ' : 'New ') + (nouns[kind] || 'editor'),
      onLoad: function (html) {
        document.dispatchEvent(new CustomEvent('date-picker:cleanup'));
        content.innerHTML = html;
        document.dispatchEvent(new CustomEvent('date-picker:initialize'));
        var first = content.querySelector('input:not([type=hidden]), select, textarea');
        if (first) first.focus();
      },
      onFailure: function (error) {
        announce('');
        if (feedback) feedback.showFailure('Could not load editor',
          error.message === 'forbidden'
            ? 'Editing is restricted to signed-in staff.'
            : 'The editor could not be loaded. Try again.');
      }
    });
  }

  /* A 403 has two honest readings: the server's own "Editing is restricted."
     body means permission; anything else -- a refused CSRF check, say -- must
     not wear that message. The response body tells them apart. */
  function forbiddenFrom(text) {
    var error = new Error('forbidden');
    error.userMessage = /restricted/i.test(text)
      ? 'Editing is restricted to signed-in staff.'
      : 'The change was refused. Reload the page and try again.';
    return error;
  }

  function submit(form) {
    if (feedback && feedback.isDialogBusy(modal)) return;
    var body = new FormData(form);
    announce('');
    var resource = /\/songbook\//.test(form.action) ? 'songbook'
      : /\/tatib\//.test(form.action) ? 'Tata Ibadah'
        : /\/song\//.test(form.action) ? 'song' : 'changes';
    var action = feedback && feedback.beginAction({
      pendingTitle: 'Saving ' + resource + '…',
      successTitle: resource.charAt(0).toUpperCase() + resource.slice(1) + ' saved',
      failureTitle: 'Could not save ' + resource,
      failureMessage: 'Your changes were not saved. Try again.'
    });
    var release = feedback ? feedback.setDialogBusy(modal) : null;
    var invalid = null;
    fetch(form.action, {
      method: 'POST', body: body, credentials: 'same-origin',
      headers: { 'X-Requested-With': 'fetch' }
    }).then(function (response) {
      if (response.status === 400) {
        return response.text().then(function (html) {
          if (!html.trim()) throw new Error('unexpected');
          document.dispatchEvent(new CustomEvent('date-picker:cleanup'));
          content.innerHTML = html;
          announce('');
          document.dispatchEvent(new CustomEvent('date-picker:initialize'));
          invalid = content.querySelector('.is-invalid input, .is-invalid select, .is-invalid textarea');
          /* the entry modals re-wire their own controls onto the fresh fragment */
          document.dispatchEvent(new CustomEvent('editor:rendered'));
          if (action) action.failure('Please check the highlighted fields.');
        });
      }
      if (response.status === 403) {
        return response.text().then(function (text) { throw forbiddenFrom(text); });
      }
      if (!response.ok) {
        throw new Error('request-failed');
      }
      return response.json().then(function (data) {
        if (!data || typeof data !== 'object' || Array.isArray(data)) {
          throw new Error('unexpected');
        }
        if (release) { release(); release = null; }
        trigger = null;
        var slotEntry = form.dataset && form.dataset.slotEntry;
        if (slotEntry) data.slotEntry = slotEntry;
        close();
        document.dispatchEvent(new CustomEvent('editor:saved', { detail: data }));
        if (action) action.success();
      });
    }).catch(function (error) {
      announce('');
      if (action) action.failure(error.userMessage
        || (error.message === 'unexpected'
          ? 'The server returned an unexpected response.'
          : 'Your changes were not saved. Try again.'));
    }).finally(function () {
      if (release) release();
      if (invalid && invalid.isConnected) invalid.focus();
    });
  }

  /* ---------- delete a sidebar record (spec 190) ------------------------------ */
  var DELETE_NOUNS = { songbook: 'songbook', song: 'song',
                       tatib: 'Tata Ibadah', template: 'template' };
  function nounFor(kind) { return DELETE_NOUNS[kind] || 'record'; }
  function deleteUrl(dataset, kind, id) {
    return dataset.replace('KIND', kind).replace('/0/', '/' + id + '/');
  }
  function openDeleteConfirm(kind, id) {
    announce('');
    return window.gkpsEditorLoadForm.open({
      url: deleteUrl(modal.dataset.editorDeleteConfirm, kind, id),
      title: 'Delete ' + nounFor(kind),
      onLoad: function (html) {
        document.dispatchEvent(new CustomEvent('date-picker:cleanup'));
        content.innerHTML = html;
        document.dispatchEvent(new CustomEvent('date-picker:initialize'));
        var accept = content.querySelector('.editor__danger');
        if (accept) accept.focus();
      },
      onFailure: function (error) {
        announce('');
        if (feedback) feedback.showFailure('Could not open delete confirmation',
          error.message === 'forbidden'
            ? 'Editing is restricted to signed-in staff.'
            : 'The confirmation could not be loaded. Try again.');
      }
    });
  }
  /* The row lives in the song list (songs) or the section panel (everything
     else). It leaves the list, and its neighbour quietly takes the focus. */
  function applyDelete(kind, id) {
    var scope = document.getElementById(kind === 'song' ? 'chList' : 'panelBody');
    if (!scope) return null;
    var link = scope.querySelector(kind === 'song'
      ? '.songrow[data-i="' + id + '"]' : '.book[data-name="' + id + '"]');
    var row = link && link.closest('li');
    if (!row || !row.parentNode) return null;
    var neighbourLink = null;
    var candidate = row.previousElementSibling;
    while (candidate && !neighbourLink) {
      neighbourLink = candidate.querySelector('a.book, a.songrow');
      candidate = neighbourLink ? null : candidate.previousElementSibling;
    }
    candidate = row.nextElementSibling;
    while (candidate && !neighbourLink) {
      neighbourLink = candidate.querySelector('a.book, a.songrow');
      candidate = neighbourLink ? null : candidate.nextElementSibling;
    }
    row.parentNode.removeChild(row);
    return neighbourLink;
  }
  /* Reading what you are deleting? The stage's section, tile and song say so. */
  function wasOnStage(kind, id) {
    var stage = window.gkpsStage ? window.gkpsStage() : null;
    if (!stage || !stage.section) return false;
    if (kind === 'song') return stage.section === 'kidung' && String(stage.song) === String(id);
    if (kind === 'songbook') return stage.section === 'kidung' && String(stage.tile) === String(id);
    return stage.section === 'tatib' && String(stage.tile) === String(id);
  }
  /* Where a deleted-on-stage reader lands: the list the record belonged to. */
  function parentListUrl(kind) {
    if (kind === 'song') {
      var tile = document.querySelector('#panelBody .book[aria-current="true"]');
      if (tile) return tile.getAttribute('href');
      return '/songs/';
    }
    if (kind === 'template') return '/tatib/?mode=template';
    if (kind === 'tatib') return '/tatib/';
    return '/songs/';
  }
  function submitDelete(form) {
    var kind = form.dataset.editorDeleteKind;
    var id = form.dataset.editorDeleteId;
    var noun = nounFor(kind);
    announce('');
    var body = new FormData(form);   /* before setDialogBusy: it disables the
                                        fields, and FormData skips disabled ones
                                        -- the CSRF input must be read first */
    var action = feedback && feedback.beginAction({
      pendingTitle: 'Deleting ' + noun + '…',
      successTitle: noun.charAt(0).toUpperCase() + noun.slice(1) + ' deleted',
      failureTitle: 'Could not delete the ' + noun,
      failureMessage: 'It was not deleted. Try again.'
    });
    var release = feedback ? feedback.setDialogBusy(modal) : null;
    fetch(form.action, {
      method: 'POST', body: body, credentials: 'same-origin',
      headers: { 'X-Requested-With': 'fetch' }
    }).then(function (response) {
      if (response.status === 403) {
        return response.text().then(function (text) { throw forbiddenFrom(text); });
      }
      if (!response.ok) throw new Error('request-failed');
      return response.json();
    }).then(function (data) {
      if (!data || !data.ok) throw new Error('unexpected');
      if (release) { release(); release = null; }
      trigger = null;
      var onStage = wasOnStage(kind, id);
      var neighbourLink = onStage ? null : applyDelete(kind, id);
      close();
      if (neighbourLink && !neighbourLink.closest('.is-hidden')) {
        focusTools.restoreQuietly(neighbourLink);
      }
      if (!onStage) document.dispatchEvent(new CustomEvent('shell:sidebar-delete'));
      if (action) action.success();
      if (onStage && window.gkpsNavigate) {
        /* The stage was showing what was just deleted: swap to the parent list
           and replace the history entry, so Back never revisits the removal. */
        window.gkpsNavigate(parentListUrl(kind), { kind: 'refresh', replaceUrl: true });
      }
    }).catch(function (error) {
      announce('');
      if (action) action.failure(error.userMessage
        || (error.message === 'unexpected'
          ? 'The server returned an unexpected response.'
          : 'It was not deleted. Try again.'));
    }).finally(function () {
      if (release) release();
    });
  }

  /* One delegated listener each: the shells replace their rows on every swap. */
  document.addEventListener('click', function (event) {
    var closeButton = event.target.closest('[data-editor-close]');
    if (closeButton && modal.contains(closeButton)) { close(); return; }
    var deleteOpener = event.target.closest('[data-editor-delete]');
    if (deleteOpener && !deleteOpener.disabled && window.gkpsEditorLoadForm.canOpen()) {
      event.preventDefault();
      trigger = deleteOpener;
      openDeleteConfirm(deleteOpener.dataset.editorDelete, deleteOpener.dataset.editorId);
      return;
    }
    var opener = event.target.closest('[data-editor-open]');
    if (!opener || opener.disabled || !window.gkpsEditorLoadForm.canOpen()) return;
    event.preventDefault();
    trigger = opener;
    open(opener.dataset.editorOpen, opener.dataset.editorId, opener.dataset.editorBook);
  });

  content.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form.classList.contains('editor__form')) return;
    event.preventDefault();
    if (feedback && feedback.isDialogBusy(modal)) return;
    if (form.dataset.editorDeleteForm) { submitDelete(form); return; }
    submit(form);
  });

  modal.addEventListener('click', function (event) {
    if (event.target === modal) close();          /* the backdrop */
  });

  modal.addEventListener('close', function () {
    delete modal.dataset.focusRestorePending;
    document.dispatchEvent(new CustomEvent('date-picker:cleanup'));
    content.innerHTML = '';
    announce('');
    if (trigger && document.contains(trigger)) {
      var focusTarget = trigger;
      if (trigger.classList.contains('row-edit')
          || trigger.classList.contains('row-delete')) {
        var row = trigger.closest('li');
        focusTarget = row && row.querySelector('a.book, a.songrow') || trigger;
      }
      focusTools.restoreQuietly(focusTarget);
    }
    trigger = null;
  });

  /* ---------- the Tata Ibadah type chips (spec 167) ---------------------------
     Normal carries a date; Template carries none, so the field and its picker are
     removed rather than emptied -- the server refuses either disagreement anyway. */
  modal.addEventListener('click', function (event) {
    var chip = event.target.closest('[data-tatib-kind]');
    if (!chip) return;
    var group = chip.closest('[data-tatib-kinds]');
    Array.prototype.forEach.call(group.querySelectorAll('[data-tatib-kind]'), function (button) {
      button.setAttribute('aria-pressed', String(button === chip));
    });
    // the thumb slides on the wrapper's own state, not on a class per button
    group.dataset.selected = chip.dataset.tatibKind === '1' ? 'template' : 'normal';
    var form = group.closest('form');
    var field = form.querySelector('input[name="kind"]');
    if (field) field.value = chip.dataset.tatibKind;
    var template = chip.dataset.tatibKind === '1';
    var dateField = form.querySelector('.editor__date-field');
    if (dateField) dateField.hidden = template;
    var dateInput = form.querySelector('input[name="date"]');
    var dateLabel = form.querySelector('[data-date-picker-label]');
    if (template) {
      /* The picker pre-fills the nearest Sunday on load; a template carries no date at
         all, so the field is emptied rather than left holding one the server refuses.
         What it held is kept, so a switch back does not silently move the date. */
      if (dateInput) {
        group.dataset.savedDate = dateInput.value;
        dateInput.value = '';
      }
      if (dateLabel) dateLabel.textContent = 'Choose a date';
    } else if (dateInput && !dateInput.value) {
      group.dataset.savedDate = group.dataset.savedDate
        || dateInput.dataset.initialValue || '';
      if (!group.dataset.savedDate) {
        var today = new Date();
        var sunday = new Date(today.getTime());
        sunday.setDate(today.getDate() + ((7 - today.getDay()) % 7));
        group.dataset.savedDate = sunday.toISOString().slice(0, 10);
      }
      dateInput.value = group.dataset.savedDate;
      /* the trigger names the date, never the rule that chose it */
      if (dateLabel) {
        dateLabel.textContent = new Intl.DateTimeFormat('id-ID', {
          day: 'numeric', month: 'long', year: 'numeric'
        }).format(new Date(dateInput.value + 'T00:00:00'));
      }
    }
    /* the switch is a decision made before typing, so the caret goes to the name --
       with whatever was already typed kept, and the caret after it. */
    var nameInput = form.querySelector('input[name="name"]');
    if (nameInput) {
      nameInput.focus();
      var end = (nameInput.value || '').length;
      if (nameInput.setSelectionRange) nameInput.setSelectionRange(end, end);
    }
  });

  /* ---------- Copy as template (spec 167) ------------------------------------ */
  modal.addEventListener('click', function (event) {
    var openCopy = event.target.closest('[data-copy-open]');
    if (openCopy) {
      var layer = modal.querySelector('[data-copy-confirm]');
      if (!layer) return;
      layer.hidden = false;
      var accept = layer.querySelector('[data-copy-accept]');
      if (accept) accept.focus();
      return;
    }
    if (event.target.closest('[data-copy-cancel]')) {
      var confirm = modal.querySelector('[data-copy-confirm]');
      if (confirm) confirm.hidden = true;
      return;
    }
    var acceptCopy = event.target.closest('[data-copy-accept]');
    if (!acceptCopy) return;
    var triggerOpen = modal.querySelector('[data-copy-open]');
    if (!triggerOpen) return;
    acceptCopy.disabled = true;
    fetch(triggerOpen.dataset.copyUrl, {
      method: 'POST', credentials: 'same-origin',
      headers: { 'X-Requested-With': 'fetch', 'X-CSRFToken': csrfToken() }
    }).then(function (response) {
      return response.json().then(function (data) { return { ok: response.ok, data: data }; });
    }).then(function (result) {
      acceptCopy.disabled = false;
      if (!result.ok) { announce((result.data && result.data.error) || 'The copy failed.'); return; }
      window.location.href = result.data.url;
    }).catch(function () {
      acceptCopy.disabled = false;
      announce('The copy failed.');
    });
  });
})();
