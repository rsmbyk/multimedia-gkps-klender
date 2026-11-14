/* Quiet only focus restored by a modal or shell refresh. Deliberate navigation
   removes the temporary marker before the browser moves focus. */
(function () {
  'use strict';

  function clearQuietMarkers() {
    document.querySelectorAll('.focus-restore-quiet').forEach(function (element) {
      element.classList.remove('focus-restore-quiet');
    });
  }

  window.gkpsFocus = {
    restoreQuietly: function (target) {
      if (!target) return;
      if (target.tabIndex < 0 && !target.hasAttribute('tabindex')) {
        target.setAttribute('tabindex', '-1');
      }
      target.classList.add('focus-restore-quiet');
      target.focus({ preventScroll: true });
    }
  };

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Tab') clearQuietMarkers();
  }, true);
})();
