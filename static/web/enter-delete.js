/* Enter accepts an open delete confirmation, wherever focus sits (spec 256).
   The destructive controls carry [data-enter-delete]; the handler stays away
   from every other dialog, form and key. */
(function () {
  'use strict';

  function usable(button) {
    return !button.disabled
      && !button.classList.contains('disabled')
      && button.getAttribute('aria-disabled') !== 'true';
  }

  function destructiveControl() {
    var buttons = document.querySelectorAll('[data-enter-delete]');
    for (var index = buttons.length - 1; index >= 0; index -= 1) {
      var button = buttons[index];
      if (button.closest('[hidden]')) continue;
      var dialog = button.closest('dialog');
      if (dialog && !dialog.open) continue;
      if (!button.getClientRects().length) continue;
      return button;
    }
    return null;
  }

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Enter' || event.defaultPrevented || event.repeat
        || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    var button = destructiveControl();
    if (!button || !usable(button)) return;
    event.preventDefault();
    event.stopPropagation();
    button.click();
  }, true);
})();
