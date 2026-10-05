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
  var trigger = null;

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
    if (modal.open) modal.close();
  }

  function open(kind, id, book) {
    announce('');
    fetch(urlFor(kind, id, book), {
      credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch' }
    }).then(function (response) {
      if (response.status === 403) throw new Error('forbidden');
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.text();
    }).then(function (html) {
      content.innerHTML = html;
      if (!modal.open) modal.showModal();
      var first = content.querySelector('input:not([type=hidden]), select, textarea');
      if (first) first.focus();
    }).catch(function (error) {
      announce(error.message === 'forbidden'
        ? 'Editing is restricted to signed-in staff.'
        : 'Could not open the editor.');
    });
  }

  function submit(form) {
    var body = new FormData(form);
    announce('Saving...');
    fetch(form.action, {
      method: 'POST', body: body, credentials: 'same-origin',
      headers: { 'X-Requested-With': 'fetch' }
    }).then(function (response) {
      if (response.status === 400) {
        return response.text().then(function (html) {
          content.innerHTML = html;
          announce('Please correct the highlighted fields.');
          var invalid = content.querySelector('.is-invalid input, .is-invalid select, .is-invalid textarea');
          if (invalid) invalid.focus();
        });
      }
      if (response.status === 403) {
        announce('Editing is restricted to signed-in staff.');
        return null;
      }
      if (!response.ok) {
        announce('Could not save. Try again.');
        return null;
      }
      return response.json().then(function (data) {
        announce('');
        close();
        document.dispatchEvent(new CustomEvent('editor:saved', { detail: data }));
      });
    }).catch(function () { announce('Could not save. Try again.'); });
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
    submit(form);
  });

  modal.addEventListener('click', function (event) {
    if (event.target === modal) close();          /* the backdrop */
  });

  modal.addEventListener('close', function () {
    content.innerHTML = '';
    announce('');
    if (trigger && document.contains(trigger)) trigger.focus();
    trigger = null;
  });
})();
