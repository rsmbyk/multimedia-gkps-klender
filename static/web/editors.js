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
  var focusTools = window.gkpsFocus || {
    restoreQuietly: function (target) {
      if (!target) return;
      target.classList.add('focus-restore-quiet');
      target.focus({ preventScroll: true });
    }
  };

  function urlFor(kind, id, book) {
    var pattern = modal.dataset.editorNew;
    if (id) pattern = modal.dataset.editorEdit.replace('/0/', '/' + id + '/');
    var url = pattern.replace('KIND', kind);
    if (!id && book) url += '?book=' + encodeURIComponent(book);
    return url;
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
    fetch(urlFor(kind, id, book), {
      credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch' }
    }).then(function (response) {
      if (response.status === 403) throw new Error('forbidden');
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.text().then(function (html) {
        if (!html.trim()) throw new Error('empty');
        return html;
      });
    }).then(function (html) {
      document.dispatchEvent(new CustomEvent('date-picker:cleanup'));
      content.innerHTML = html;
      if (!modal.open) modal.showModal();
      document.dispatchEvent(new CustomEvent('date-picker:initialize'));
      var first = content.querySelector('input:not([type=hidden]), select, textarea');
      if (first) first.focus();
    }).catch(function (error) {
      announce('');
      if (feedback) feedback.showFailure('Could not load editor',
        error.message === 'forbidden'
          ? 'Editing is restricted to signed-in staff.'
          : 'The editor could not be loaded. Try again.');
    });
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
        var restricted = new Error('forbidden');
        restricted.userMessage = 'Editing is restricted to signed-in staff.';
        throw restricted;
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

  /* One delegated listener each: the shells replace their rows on every swap. */
  document.addEventListener('click', function (event) {
    var closeButton = event.target.closest('[data-editor-close]');
    if (closeButton && modal.contains(closeButton)) { close(); return; }
    var opener = event.target.closest('[data-editor-open]');
    if (!opener || opener.disabled) return;
    event.preventDefault();
    trigger = opener;
    open(opener.dataset.editorOpen, opener.dataset.editorId, opener.dataset.editorBook);
  });

  content.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form.classList.contains('editor__form')) return;
    event.preventDefault();
    if (feedback && feedback.isDialogBusy(modal)) return;
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
      if (trigger.classList.contains('row-edit')) {
        var row = trigger.closest('li');
        focusTarget = row && row.querySelector('a.book, a.songrow') || trigger;
      }
      focusTools.restoreQuietly(focusTarget);
    }
    trigger = null;
  });
})();
