/* Shared edit-request feedback for the public reading shell (spec 093). */
(function () {
  'use strict';

  var host = document.getElementById('editToastHost');
  var items = [];
  var reducedMotion = window.matchMedia
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pendingLocks = new WeakMap();
  var noop = function () {};

  function isOpen() {
    return host && host.matches(':popover-open');
  }

  function showHost() {
    if (!host || typeof host.showPopover !== 'function') return;
    try {
      if (!isOpen()) host.showPopover();
    } catch (error) { /* The notification must never affect the edit request. */ }
  }

  function raiseHost() {
    if (!host || typeof host.showPopover !== 'function') return;
    try {
      if (isOpen()) host.hidePopover();
      host.showPopover();
    } catch (error) { /* A failed layer promotion does not change request state. */ }
  }

  function cleanMessage(value, fallback) {
    if (typeof value !== 'string') return fallback;
    var cleaned = value.replace(/[\u0000-\u001f\u007f]/g, ' ').trim();
    return cleaned ? cleaned.slice(0, 180) : fallback;
  }

  function liveItems() {
    return items.filter(function (item) { return !item.closing && !!item.node; });
  }

  function getStack() {
    var stack = host.querySelector('.edit-toasts__stack');
    if (!stack) {
      stack = document.createElement('div');
      stack.className = 'edit-toasts__stack';
      host.appendChild(stack);
    }
    return stack;
  }

  function scrollNewestIntoView() {
    if (!host) return;
    window.requestAnimationFrame(function () {
      host.scrollTop = host.scrollHeight;
    });
  }

  function render(item, state) {
    if (!host) return;
    var stack = getStack();
    if (!item.node) {
      var node = document.createElement('div');
      node.className = 'edit-toast';
      node.setAttribute('role', 'status');
      node.setAttribute('aria-atomic', 'true');
      var mark = document.createElement('span');
      mark.className = 'edit-toast__mark';
      mark.setAttribute('aria-hidden', 'true');
      var copy = document.createElement('span');
      copy.className = 'edit-toast__copy';
      var title = document.createElement('strong');
      title.className = 'edit-toast__title';
      var message = document.createElement('span');
      message.className = 'edit-toast__message';
      copy.append(title, message);
      node.append(mark, copy);
      item.node = node;
      item.mark = mark;
      item.title = title;
      item.message = message;
      stack.appendChild(node);
      showHost();
      scrollNewestIntoView();
      window.requestAnimationFrame(function () {
        if (item.node && !item.closing) item.node.classList.add('is-visible');
      });
    }

    var node = item.node;
    node.dataset.state = state;
    node.setAttribute('aria-busy', state === 'pending' ? 'true' : 'false');
    node.classList.remove('is-pending', 'is-success', 'is-failure');
    node.classList.add('is-' + state);
    node.setAttribute('role', state === 'failure' ? 'alert' : 'status');
    item.mark.replaceChildren();

    if (state === 'pending') {
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 20 20');
      svg.setAttribute('aria-hidden', 'true');
      var ring = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      ring.setAttribute('cx', '10'); ring.setAttribute('cy', '10'); ring.setAttribute('r', '7');
      svg.appendChild(ring);
      item.mark.appendChild(svg);
      item.title.textContent = item.options.pendingTitle;
      item.message.textContent = item.options.pendingMessage;
      removeDismiss(item);
    } else {
      item.mark.textContent = state === 'success' ? '✓' : '!';
      item.title.textContent = state === 'success'
        ? item.options.successTitle : item.options.failureTitle;
      item.message.textContent = state === 'success'
        ? item.options.successMessage : item.resultMessage;
      addDismiss(item);
    }

    promoteForOpenDialogs();
    if (state !== 'pending') shortenTimersWhenCrowded();
  }

  function addDismiss(item) {
    if (item.dismiss || !item.node) return;
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'edit-toast__dismiss';
    button.setAttribute('aria-label', 'Dismiss notification');
    button.textContent = '×';
    button.addEventListener('click', function () { closeItem(item); });
    item.node.appendChild(button);
    item.dismiss = button;
  }

  function removeDismiss(item) {
    if (!item.dismiss) return;
    item.dismiss.remove();
    item.dismiss = null;
  }

  function durationFor(state, crowded) {
    if (crowded) return state === 'success' ? 1000 : 1618;
    return state === 'success' ? 2000 : 3230;
  }

  function scheduleClose(item, duration) {
    window.clearTimeout(item.closeTimer);
    item.duration = duration;
    item.closeAt = item.settledAt + duration;
    if (item.node) item.node.dataset.closeMs = String(duration);
    item.closeTimer = window.setTimeout(function () { closeItem(item); },
      Math.max(0, item.closeAt - Date.now()));
  }

  function shortenTimersWhenCrowded() {
    if (liveItems().length < 4) return;
    items.forEach(function (item) {
      if (item.state === 'pending' || !item.settledAt || item.shortened || item.closing) return;
      item.shortened = true;
      scheduleClose(item, durationFor(item.state, true));
    });
  }

  function closeItem(item) {
    if (!item || item.closing) return;
    item.closing = true;
    window.clearTimeout(item.pendingTimer);
    window.clearTimeout(item.closeTimer);
    if (!item.node) {
      items = items.filter(function (each) { return each !== item; });
      return;
    }
    item.node.classList.add('is-exiting');
    window.setTimeout(function () {
      if (item.node) item.node.remove();
      items = items.filter(function (each) { return each !== item; });
    }, reducedMotion ? 0 : 140);
  }

  function defaults(options) {
    options = options || {};
    return {
      pendingTitle: options.pendingTitle || 'Saving changes…',
      pendingMessage: options.pendingMessage || 'Please wait',
      successTitle: options.successTitle || 'Changes saved',
      successMessage: options.successMessage || 'Your changes were saved.',
      failureTitle: options.failureTitle || 'Could not save changes',
      failureMessage: options.failureMessage || 'Your change was not saved. Try again.'
    };
  }

  function beginAction(options) {
    var item = {
      options: defaults(options), state: 'pending', node: null,
      settledAt: 0, closing: false, shortened: false
    };
    items.push(item);
    item.pendingTimer = window.setTimeout(function () {
      if (!item.closing && item.state === 'pending') {
        render(item, 'pending');
        shortenTimersWhenCrowded();
      }
    }, 180);

    function settle(state, message) {
      if (item.closing || item.state !== 'pending') return;
      window.clearTimeout(item.pendingTimer);
      item.state = state;
      item.settledAt = Date.now();
      item.resultMessage = state === 'failure'
        ? cleanMessage(message, item.options.failureMessage) : item.options.successMessage;
      render(item, state);
      if (!item.closeTimer) {
        scheduleClose(item, durationFor(state, liveItems().length >= 4));
      }
    }

    return {
      success: function (message) {
        if (message) item.options.successMessage = cleanMessage(message, item.options.successMessage);
        settle('success');
      },
      failure: function (message) { settle('failure', message); }
    };
  }

  function showFailure(title, message) {
    var action = beginAction({
      pendingTitle: title || 'Request failed',
      pendingMessage: message || 'The request could not be completed.',
      failureTitle: title || 'Request failed',
      failureMessage: message || 'The request could not be completed.'
    });
    action.failure(message);
  }

  function lockControl(control) {
    if (!control || !('disabled' in control)) return noop;
    var wasDisabled = control.disabled;
    var wasBusy = control.getAttribute('aria-busy');
    control.disabled = true;
    control.setAttribute('aria-busy', 'true');
    return function () {
      control.disabled = wasDisabled;
      if (wasBusy === null) control.removeAttribute('aria-busy');
      else control.setAttribute('aria-busy', wasBusy);
    };
  }

  function setDialogBusy(dialog) {
    if (!dialog) return noop;
    if (pendingLocks.has(dialog)) return pendingLocks.get(dialog).release;
    var controls = Array.prototype.slice.call(dialog.querySelectorAll(
      'button:not(.edit-toast__dismiss), input, select, textarea, [contenteditable="true"]'));
    var states = controls.map(function (control) {
      var state = {control: control};
      if ('disabled' in control) {
        state.disabled = control.disabled;
        control.disabled = true;
      } else {
        state.contentEditable = control.getAttribute('contenteditable');
        control.setAttribute('contenteditable', 'false');
      }
      return state;
    });
    dialog.setAttribute('aria-busy', 'true');
    dialog.dataset.requestPending = 'true';
    var lock = {release: function () {
      states.forEach(function (state) {
        if (!state.control.isConnected) return;
        if ('disabled' in state.control) state.control.disabled = state.disabled;
        else if (state.contentEditable === null) state.control.removeAttribute('contenteditable');
        else state.control.setAttribute('contenteditable', state.contentEditable);
      });
      dialog.removeAttribute('aria-busy');
      delete dialog.dataset.requestPending;
      pendingLocks.delete(dialog);
    }};
    pendingLocks.set(dialog, lock);
    return lock.release;
  }

  function isDialogBusy(dialog) { return !!dialog && pendingLocks.has(dialog); }

  function guardDialog(dialog) {
    if (!dialog || dialog.dataset.feedbackGuarded === 'true') return;
    dialog.dataset.feedbackGuarded = 'true';
    dialog.addEventListener('cancel', function (event) {
      if (!isDialogBusy(dialog)) return;
      event.preventDefault();
      event.stopImmediatePropagation();
    }, true);
    dialog.addEventListener('click', function (event) {
      if (!isDialogBusy(dialog) || event.target !== dialog) return;
      event.preventDefault();
      event.stopImmediatePropagation();
    }, true);
  }

  function promoteForOpenDialogs() {
    if (!host) return;
    var dialog = document.querySelector('dialog[open]');
    var target = dialog || document.body;
    if (host.parentElement !== target) {
      var wasOpen = isOpen();
      if (wasOpen) host.hidePopover();
      target.appendChild(host);
      if (wasOpen) host.showPopover();
    } else if (dialog) {
      raiseHost();
    }
  }

  if (host) {
    host.setAttribute('popover', 'manual');
    host.setAttribute('role', 'region');
    host.setAttribute('aria-label', 'Edit request feedback');
    host.setAttribute('aria-live', 'polite');
    host.setAttribute('aria-relevant', 'additions text');
    showHost();
    var dialogObserver = new MutationObserver(function (records) {
      if (records.some(function (record) { return record.target.matches('dialog'); })) {
        promoteForOpenDialogs();
      }
    });
    dialogObserver.observe(document.documentElement, {
      subtree: true, attributes: true, attributeFilter: ['open']
    });
  }

  window.gkpsEditFeedback = {
    beginAction: beginAction,
    showFailure: showFailure,
    lockControl: lockControl,
    setDialogBusy: setDialogBusy,
    isDialogBusy: isDialogBusy,
    guardDialog: guardDialog,
    cleanMessage: cleanMessage
  };
})();
