/* The entry preview (spec 032).
 *
 * A read-only modal: the pane's Preview button copies the entry's inline payload into
 * the dialog, which owns no header, scrolls its body, and keeps its Close at the foot.
 * Esc closes it (native <dialog>), as does a click on the overlay. Focus returns to the
 * trigger without leaving a row outline (spec 025).
 */
(function () {
  'use strict';

  var modal = document.getElementById('previewModal');
  var content = document.getElementById('previewContent');
  if (!modal || typeof modal.showModal !== 'function') return;

  var trigger = null;
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

  document.addEventListener('click', function (event) {
    var opener = event.target.closest('[data-preview-open]');
    if (opener) {
      event.preventDefault();
      trigger = opener;
      var anchor = opener.dataset.previewFor;
      var data = anchor && document.querySelector(
        '.entry__preview-src[data-preview-for="' + anchor + '"]');
      content.innerHTML = data ? data.textContent : '';
      wireTabs(content);
      if (!modal.open) modal.showModal();
      return;
    }
    var closer = event.target.closest('[data-preview-close]');
    if (closer && modal.contains(closer)) modal.close();
  });

  modal.addEventListener('click', function (event) {
    if (event.target === modal) modal.close();          /* the backdrop */
  });

  modal.addEventListener('close', function () {
    content.innerHTML = '';
    if (trigger && document.contains(trigger)) focusTools.restoreQuietly(trigger);
    trigger = null;
  });
})();
