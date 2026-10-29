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
  var feedback = window.gkpsEditFeedback;
  if (feedback) feedback.guardDialog(modal);

  var trigger = null;
  var keyboardOpened = false;
  var origin = null;
  var split = null;
  var breaks = null;
  var defaultMode = 'multi_line';
  var pendingMode = null;
  var pendingButton = null;
  var saving = false;
  var imageController = null;
  var imageUrl = null;
  var imageToken = 0;
  var imageSize = null;
  var imageCloseTimer = null;
  var imageStatusAvailable = null;
  var audioController = null;
  var audioPlayer = null;
  var audioUrl = null;
  var audioToken = 0;
  var videoController = null;
  var videoPlayer = null;
  var videoUrl = null;
  var videoToken = 0;
  var pdfController = null;
  var pdfDocument = null;
  var pdfToken = 0;
  var pdfPage = 1;
  var focusTools = window.gkpsFocus || {
    restoreQuietly: function (target) {
      if (target) target.focus({ preventScroll: true });
    }
  };

  function sizeImagePreview() {
    if (!imageSize || !modal.open) return;
    var width = Math.max(1, window.innerWidth - 32 - 44);
    var height = Math.max(1, window.innerHeight - 48 - 52 - 44);
    var scale = Math.min(width / imageSize.width, height / imageSize.height);
    var image = content.querySelector('.preview__image img');
    if (!image) return;
    image.style.width = Math.floor(imageSize.width * scale) + 'px';
    image.style.height = Math.floor(imageSize.height * scale) + 'px';
    modal.style.width = Math.ceil(imageSize.width * scale + 44) + 'px';
  }
  window.addEventListener('resize', sizeImagePreview);

  function clearImagePreview() {
    imageToken++;
    if (imageController) imageController.abort();
    imageController = null;
    if (imageUrl) URL.revokeObjectURL(imageUrl);
    imageUrl = null;
    imageSize = null;
    imageStatusAvailable = null;
    modal.style.width = '';
    modal.classList.remove('is-image-preview', 'is-closing');
    clearTimeout(imageCloseTimer);
  }

  function loadImagePreview() {
    var host = content.querySelector('[data-preview-image]');
    if (!host) return;
    var image = host.querySelector('img');
    var unavailable = host.querySelector('.preview__image-unavailable');
    unavailable.hidden = true;
    image.hidden = true;
    imageController = new AbortController();
    var token = ++imageToken;
    window.GKPSMediaImage.load(host.dataset.previewImage, imageController.signal)
      .then(function (result) {
        if (token !== imageToken || !modal.open) { URL.revokeObjectURL(result.url); return; }
        imageController = null;
        imageUrl = result.url;
        imageSize = result;
        image.src = imageUrl;
        image.hidden = false;
        sizeImagePreview();
      }).catch(function () {
        if (token === imageToken && modal.open) {
          imageController = null;
          unavailable.hidden = false;
        }
      });
  }

  function clearAudioPreview() {
    audioToken++;
    if (audioController) audioController.abort();
    audioController = null;
    if (audioPlayer) audioPlayer.stop();
    audioPlayer = null;
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    audioUrl = null;
    modal.classList.remove('is-audio-preview');
  }

  function loadAudioPreview() {
    var host = content.querySelector('[data-preview-audio]');
    if (!host) return;
    var player = host.querySelector('.audio-player');
    var missing = host.querySelector('.preview__audio-unavailable');
    player.hidden = true;
    missing.hidden = true;
    audioController = new AbortController();
    var token = ++audioToken;
    window.GKPSMediaAudio.load(host.dataset.previewAudio, audioController.signal).then(function (url) {
      if (token !== audioToken || !modal.open) { URL.revokeObjectURL(url); return; }
      audioUrl = url;
      audioPlayer = window.GKPSMediaAudio.attach(host, {
        onReady: function () { if (token === audioToken) player.hidden = false; },
        onError: function () { if (token === audioToken) { player.hidden = true; missing.hidden = false; } }
      });
      audioPlayer.setUrl(url);
    }).catch(function () {
      if (token === audioToken && modal.open) missing.hidden = false;
    }).finally(function () { if (token === audioToken) audioController = null; });
  }

  function clearVideoPreview() {
    videoToken++;
    if (videoController) videoController.abort();
    videoController = null;
    if (videoPlayer) videoPlayer.stop();
    videoPlayer = null;
    if (videoUrl) URL.revokeObjectURL(videoUrl);
    videoUrl = null;
    modal.classList.remove('is-video-preview');
  }

  function loadVideoPreview() {
    var host = content.querySelector('[data-preview-video]');
    if (!host) return;
    var player = host.querySelector('video');
    var unavailable = content.querySelector('.preview__video-unavailable');
    player.hidden = true;
    unavailable.hidden = true;
    videoController = new AbortController();
    var token = ++videoToken;
    window.GKPSMediaVideo.load(host.dataset.previewVideo, videoController.signal).then(function (url) {
      if (token !== videoToken || !modal.open) { URL.revokeObjectURL(url); return; }
      videoUrl = url;
      videoPlayer = window.GKPSMediaVideo.attach(host, {
        onReady: function () { if (token === videoToken) player.hidden = false; },
        onError: function () {
          if (token === videoToken) {
            if (videoPlayer) videoPlayer.stop();
            videoPlayer = null;
            if (videoUrl) URL.revokeObjectURL(videoUrl);
            videoUrl = null;
            player.hidden = true;
            unavailable.hidden = false;
          }
        }
      });
      videoPlayer.setUrl(url);
    }).catch(function () {
      if (token === videoToken && modal.open) unavailable.hidden = false;
    }).finally(function () { if (token === videoToken) videoController = null; });
  }

  function clearPDFPreview() {
    pdfToken++;
    if (pdfController) pdfController.abort();
    pdfController = null;
    if (pdfDocument) pdfDocument.destroy();
    pdfDocument = null;
    pdfPage = 1;
    modal.style.width = '';
    modal.classList.remove('is-pdf-preview');
  }

  async function drawPDFPreview() {
    if (!pdfDocument || !modal.open) return;
    var host = content.querySelector('[data-preview-pdf], [data-preview-slides]');
    if (!host) return;
    if (pdfController) pdfController.abort();
    pdfController = new AbortController();
    var signal = pdfController.signal;
    var token = ++pdfToken;
    var previous = host.querySelector('canvas');
    var canvas = previous.cloneNode(false);
    previous.replaceWith(canvas);
    var width = Math.max(1, window.innerWidth - 32 - 44);
    var height = Math.max(1, window.innerHeight - 48 - 52 - 44 - 74);
    try {
      var size = await window.GKPSMediaPDF.paint(pdfDocument, pdfPage, canvas, width, height, signal);
      if (signal.aborted || token !== pdfToken || !modal.open) return;
      host.querySelector('.preview__pdf-page').hidden = false;
      if (host.querySelector('.preview__pdf-preparing')) host.querySelector('.preview__pdf-preparing').hidden = true;
      host.querySelector('.preview__pdf-controls').hidden = false;
      host.querySelector('.preview__pdf-unavailable').hidden = true;
      host.querySelector('[data-pdf-count]').textContent = pdfPage + ' / ' + pdfDocument.numPages;
      host.querySelector('[data-pdf-prev]').disabled = pdfPage === 1;
      host.querySelector('[data-pdf-next]').disabled = pdfPage === pdfDocument.numPages;
      modal.style.width = Math.ceil(size.width + 44) + 'px';
    } catch (error) {
      if (signal.aborted || token !== pdfToken) return;
      host.querySelector('.preview__pdf-page').hidden = true;
      if (host.querySelector('.preview__pdf-preparing')) host.querySelector('.preview__pdf-preparing').hidden = true;
      host.querySelector('.preview__pdf-controls').hidden = true;
      host.querySelector('.preview__pdf-unavailable').hidden = false;
      modal.style.width = '';
    }
  }

  function loadPDFPreview() {
    var host = content.querySelector('[data-preview-pdf], [data-preview-slides]');
    if (!host) return;
    host.querySelector('.preview__pdf-page').hidden = true;
    if (host.querySelector('.preview__pdf-preparing')) host.querySelector('.preview__pdf-preparing').hidden = false;
    pdfController = new AbortController();
    var signal = pdfController.signal;
    var token = ++pdfToken;
    var loading = host.dataset.previewSlides
      ? window.GKPSMediaPDF.loadSlides(host.dataset.previewSlides, signal)
      : window.GKPSMediaPDF.load(host.dataset.previewPdf, signal);
    loading.then(function (document) {
      if (signal.aborted || token !== pdfToken || !modal.open) { document.destroy(); return; }
      pdfDocument = document;
      drawPDFPreview();
    }).catch(function () {
      if (signal.aborted || token !== pdfToken || !modal.open) return;
      host.querySelector('.preview__pdf-page').hidden = true;
      if (host.querySelector('.preview__pdf-preparing')) host.querySelector('.preview__pdf-preparing').hidden = true;
      host.querySelector('.preview__pdf-unavailable').hidden = false;
    });
  }
  window.addEventListener('resize', function () { if (modal.open && pdfDocument) drawPDFPreview(); });
  content.addEventListener('click', function (event) {
    if (!pdfDocument) return;
    var button = event.target.closest('[data-pdf-prev], [data-pdf-next]');
    if (!button) return;
    pdfPage += button.hasAttribute('data-pdf-next') ? 1 : -1;
    drawPDFPreview();
  });

  document.addEventListener('media:status', function (event) {
    if (!modal.open || !modal.classList.contains('is-image-preview')) return;
    var host = content.querySelector('[data-preview-image]');
    if (!host) return;
    var available = (event.detail.files || []).some(function (file) {
      return file.sha256 === host.dataset.previewImage;
    });
    if (available && imageStatusAvailable === false && !imageUrl && !imageController) loadImagePreview();
    imageStatusAvailable = available;
    if (!available && imageUrl) {
      imageToken++;
      URL.revokeObjectURL(imageUrl);
      imageUrl = null;
      imageSize = null;
      modal.style.width = '';
      var image = host.querySelector('img');
      image.hidden = true;
      image.removeAttribute('src');
      host.querySelector('.preview__image-unavailable').hidden = false;
    }
  });

  function closePreview() {
    if (!modal.open || modal.classList.contains('is-closing')) return;
    if (!(modal.classList.contains('is-image-preview') || modal.classList.contains('is-audio-preview')
        || modal.classList.contains('is-video-preview') || modal.classList.contains('is-pdf-preview'))
        || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      modal.close(); return;
    }
    imageToken++;
    if (imageController) imageController.abort();
    if (audioPlayer) audioPlayer.audio.pause();
    audioToken++;
    if (audioController) audioController.abort();
    if (videoPlayer) videoPlayer.pause();
    videoToken++;
    if (videoController) videoController.abort();
    if (pdfController) pdfController.abort();
    modal.classList.add('is-closing');
    imageCloseTimer = setTimeout(function () { modal.close(); }, 170);
  }

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
     payload renders as its reference or heading, and a song's verse tabs with it -- into a band of
     their own under the header since spec 153, so the title keeps the header's whole width. An
     entry with nothing to name -- an untitled Text -- keeps the headerless dialog it has always had. */
  function liftIdentity() {
    var identity = content.querySelector('.preview__ref, .preview__song');
    var tabs = content.querySelector('.preview__tabs');
    head.hidden = !identity;
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
    if (saving || !split) return;
    saving = true;
    var activeSplit = split;
    var action = feedback && feedback.beginAction({
      pendingTitle: 'Saving screen breaks…',
      successTitle: 'Screen breaks saved',
      failureTitle: 'Could not save screen breaks',
      failureMessage: 'Your screen-break changes were not saved. Try again.'
    });
    var release = feedback ? feedback.setDialogBusy(modal) : null;
    fetch(activeSplit.dataset.saveUrl, {
      method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf()},
      body: JSON.stringify({breaks: next, default_screen_mode: nextMode || defaultMode,
        text_signature: activeSplit.dataset.textSignature,
        screen_state_signature: activeSplit.dataset.screenStateSignature})
    }).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok) {
          var failure = new Error('request-failed');
          failure.userMessage = feedback
            ? feedback.cleanMessage(data && data.error,
              'Your screen-break changes were not saved. Try again.')
            : 'Your screen-break changes were not saved. Try again.';
          throw failure;
        }
        if (!data || data.ok !== true || typeof data.default_screen_mode !== 'string'
            || typeof data.screen_state_signature !== 'string') {
          throw new Error('unexpected');
        }
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
      if (action) action.success();
      document.dispatchEvent(new CustomEvent('editor:saved', {detail: {kind: 'entry'}}));
    }).catch(function (failure) {
      if (action) action.failure(failure.userMessage
        || (failure.message === 'unexpected'
          ? 'The server returned an unexpected response.'
          : 'Your screen-break changes were not saved. Try again.'));
    }).finally(function () {
      saving = false;
      if (release) release();
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
      clearImagePreview();
      clearAudioPreview();
      clearVideoPreview();
      clearPDFPreview();
      trigger = opener;
      keyboardOpened = event.detail === 0;
      var anchor = opener.dataset.previewFor;
      var data = anchor && document.querySelector(
        '.entry__preview-src[data-preview-for="' + anchor + '"]');
      content.innerHTML = data ? data.textContent : '';
      modal.classList.toggle('is-image-preview', Boolean(content.querySelector('[data-preview-image]')));
      modal.classList.toggle('is-audio-preview', Boolean(content.querySelector('[data-preview-audio]')));
      modal.classList.toggle('is-video-preview', Boolean(content.querySelector('[data-preview-video]')));
      modal.classList.toggle('is-pdf-preview', Boolean(content.querySelector('[data-preview-pdf], [data-preview-slides]')));
      liftIdentity();
      /* the scope is the whole dialog: a song's tabs live in the header, its panels in the body */
      wireTabs(modal);
      wireSplit();
      if (!modal.open) {
        modal.showModal();
        origin = opener.closest('.tatib__item, .tatib__eos');
        if (origin) origin.classList.add('is-modal-origin');
      }
      /* The dialog opens on what is read, not on a control (spec 153): the verse tabs used to be its
         first focusable descendant, so showModal() landed on tab 1 and painted its ring. The scroller
         already takes that focus wherever there are no tabs, and its arrow/PageUp/PageDown handling
         lives there. */
      content.focus({ preventScroll: true });
      if (modal.classList.contains('is-image-preview')) loadImagePreview();
      if (modal.classList.contains('is-audio-preview')) loadAudioPreview();
      if (modal.classList.contains('is-video-preview')) loadVideoPreview();
      if (modal.classList.contains('is-pdf-preview')) loadPDFPreview();
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
    if (confirmLayer.hidden && modal.classList.contains('is-pdf-preview') && pdfDocument
        && (event.key === 'ArrowLeft' || event.key === 'ArrowRight')) {
      event.preventDefault();
      var target = pdfPage + (event.key === 'ArrowRight' ? 1 : -1);
      if (target >= 1 && target <= pdfDocument.numPages) { pdfPage = target; drawPDFPreview(); }
      return;
    }
    if (confirmLayer.hidden && modal.classList.contains('is-audio-preview') && event.key === ' '
        && !event.repeat && !event.altKey && !event.ctrlKey && !event.metaKey
        && event.target !== content.querySelector('[data-audio-seek]')) {
      event.preventDefault();
      if (audioPlayer) audioPlayer.toggle();
      return;
    }
    if (confirmLayer.hidden && modal.classList.contains('is-video-preview') && event.key === ' '
        && !event.repeat && !event.altKey && !event.ctrlKey && !event.metaKey
        && !event.shiftKey && !event.target.closest('button, input, select, textarea, [contenteditable="true"]')) {
      event.preventDefault();
      if (videoPlayer) videoPlayer.toggle();
      return;
    }
    if (confirmLayer.hidden && event.key === 'Tab' && tabsHost && !tabsHost.hidden && footer.hidden) {
      /* The verse tabs sit before the scroller in the dialog's own order, and the scroller is its last
         focusable element: the two ends of the reading loop hand focus to each other, so the tabs stay
         one Tab away from the body the dialog opens on (spec 153). No other preview's order changes. */
      var selectedTab = tabsHost.querySelector('.preview__tab[aria-selected="true"]')
        || tabsHost.querySelector('.preview__tab');
      if (!event.shiftKey && document.activeElement === content) {
        event.preventDefault();
        if (selectedTab) selectedTab.focus();
        return;
      }
      if (event.shiftKey && document.activeElement === selectedTab) {
        event.preventDefault();
        content.focus({ preventScroll: true });
        return;
      }
    }
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
    else if (modal.classList.contains('is-image-preview') || modal.classList.contains('is-audio-preview')
        || modal.classList.contains('is-video-preview') || modal.classList.contains('is-pdf-preview')) { event.preventDefault(); closePreview(); }
  });

  modal.addEventListener('click', function (event) {
    if (event.target === modal && confirmLayer.hidden && !saving) closePreview();
  });

  modal.addEventListener('close', function () {
    clearImagePreview();
    clearAudioPreview();
    clearVideoPreview();
    clearPDFPreview();
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
