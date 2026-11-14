/* Spec 167 preview — the states, driven by hand. This file never ships: it stands in
   for the handlers the slice will add, so every state in the spec is reachable. */
(function () {
  'use strict';

  var hint = document.querySelector('[data-hint]');
  var dialogs = Array.prototype.slice.call(document.querySelectorAll('dialog'));
  var surfaces = Array.prototype.slice.call(document.querySelectorAll('[data-surface]'));
  var scenario = document.getElementById('read');
  var kindsSheet = document.getElementById('kinds');
  var activeSurface = 'template';

  function pressSurface(name) {
    activeSurface = name;
    surfaces.forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.surface === name));
    });
  }
  function showKinds(on) {
    scenario.hidden = on;
    kindsSheet.hidden = !on;
  }
  function closeAll() {
    dialogs.forEach(function (dialog) { if (dialog.open) dialog.close(); });
  }
  function open(id) {
    closeAll();
    document.getElementById(id).showModal();
  }
  function say(message) { hint.textContent = message; }

  dialogs.forEach(function (dialog) {
    dialog.addEventListener('close', function () {
      if (!dialogs.some(function (other) { return other.open; })) pressSurface(activeSurface);
    });
  });

  surfaces.forEach(function (button) {
    button.addEventListener('click', function () {
      var surface = button.dataset.surface;
      pressSurface(surface);
      if (surface === 'template') {
        showKinds(false); closeAll();
        say('Hover an entry for its add bar, or use “Show add bars”.');
      }
      if (surface === 'kinds') {
        showKinds(true); closeAll();
        say('Every entry kind as a fixed entry, a fill-in and a choice.');
      }
      if (surface === 'new') { setKind('normal'); open('newModal'); }
      if (surface === 'edit') { open('editModal'); }
      if (surface === 'generate') { resetGenerate(); open('generateModal'); }
      if (surface === 'empty') { open('emptyChoiceModal'); say('A choice with no options: its control is disabled and its row says so.'); }
    });
  });

  document.addEventListener('click', function (event) {
    var closer = event.target.closest('[data-close]');
    if (closer) {
      var dialog = closer.closest('dialog');
      if (dialog) dialog.close();
    }
  });

  /* ---------- New Tata Ibadah: the type switch ---------- */
  var kindSwitch = document.querySelector('[data-kind-switch]');
  var newDate = document.querySelector('[data-new-date]');

  function setKind(kind) {
    kindSwitch.dataset.selected = kind;
    Array.prototype.forEach.call(kindSwitch.querySelectorAll('[data-kind]'), function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.kind === kind));
    });
    newDate.hidden = kind === 'template';
  }
  Array.prototype.forEach.call(kindSwitch.querySelectorAll('[data-kind]'), function (button) {
    button.addEventListener('click', function () { setKind(button.dataset.kind); });
  });

  /* The date cannot be emptied: a Normal always carries one, so the modal simply saves. */
  document.querySelector('#newModal .editor__save').addEventListener('click', function () {
    var isNormal = kindSwitch.dataset.selected === 'normal';
    document.getElementById('newModal').close();
    say(isNormal ? 'A normal Tata Ibadah was created.' : 'A template was created — no date, and it cannot be projected.');
  });

  /* ---------- Edit: Copy as template ---------- */
  var copyLayer = document.querySelector('[data-copy-confirm]');
  document.querySelector('[data-copy-open]').addEventListener('click', function () {
    copyLayer.hidden = false;
  });
  document.querySelector('[data-copy-cancel]').addEventListener('click', function () {
    copyLayer.hidden = true;
  });
  document.querySelector('[data-copy-accept]').addEventListener('click', function () {
    copyLayer.hidden = true;
    document.getElementById('editModal').close();
    say('A template holding these entries was created — the app opens it, with the panel on Templates.');
  });

  /* ---------- Use template: step 1 ---------- */
  var generate = document.getElementById('generateModal');
  var stepOne = generate.querySelector('[data-generate-step="1"]');
  var stepTwo = generate.querySelector('[data-generate-step="2"]');
  var stepItems = Array.prototype.slice.call(generate.querySelectorAll('.generate__steps li'));
  var nextButton = generate.querySelector('[data-generate-next]');
  var createButton = generate.querySelector('[data-generate-create]');
  var backButton = generate.querySelector('[data-generate-back]');
  var cancelButtons = Array.prototype.slice.call(generate.querySelectorAll('.generate__actions [data-close]'));
  var status = generate.querySelector('[data-generate-status]');
  var slotRows = Array.prototype.slice.call(generate.querySelectorAll('[data-slot-row]'));
  var choiceRows = Array.prototype.slice.call(generate.querySelectorAll('[data-choice-row]'));
  var rows = slotRows.concat(choiceRows);
  var initial = rows.map(function (row) {
    var target = row.querySelector('[data-slot-value], [data-choice-value]');
    return { set: row.dataset.set, html: target ? target.innerHTML : '' };
  });

  function isChoice(row) { return row.hasAttribute('data-choice-row'); }
  function settledCount() {
    return rows.filter(function (row) { return row.dataset.set === 'true'; }).length;
  }
  function refresh() {
    var settled = settledCount();
    var left = rows.length - settled;
    nextButton.disabled = left > 0;
    status.textContent = left
      ? settled + ' of ' + rows.length + ' settled — ' + left + ' left to fill in.'
      : 'All ' + rows.length + ' entries settled.';
  }
  function setRow(row, value, label, bait, html) {
    row.dataset.set = 'true';
    var target = row.querySelector('[data-slot-value], [data-choice-value]');
    if (target) {
      if (html) target.innerHTML = html;
      else target.textContent = value;
      /* a chosen song carries its verses inline, muted: `KJ 152 — Ada Kuasa · Bait 1, 2, 3` */
      if (bait) {
        var verses = document.createElement('span');
        verses.className = 'g-bait';
        verses.textContent = ' · ' + bait;
        target.appendChild(verses);
      }
    }
    var action = row.querySelector('[data-slot-action], [data-choice-open]');
    if (action) action.textContent = label || 'Change';
    refresh();
  }
  function unsetRow(row) {
    row.dataset.set = 'false';
    var target = row.querySelector('[data-slot-value], [data-choice-value]');
    if (target) target.textContent = isChoice(row) ? 'Not set · ' + (row.dataset.options || 2) + ' options' : 'Not set';
    var action = row.querySelector('[data-slot-action], [data-choice-open]');
    if (action) action.textContent = isChoice(row) ? 'Choose' : 'Set';
    refresh();
  }
  var SAMPLE = {
    text: 'Ya Tuhan, kami berdoa bagi jemaat-Mu.',
    passage: 'Matius 5:13',
    song: 'NKB 12 — Nyanyikanlah Nyanyian Baru',
    media: 'Video · kesaksian.mp4'
  };
  var SAMPLE_VERSE = { song: 'Bait 1, 4' };
  var SAMPLE_HTML = { media: 'Video · <span class="g-quiet">kesaksian.mp4</span>' };

  slotRows.forEach(function (row) {
    row.querySelector('[data-slot-action]').addEventListener('click', function () {
      /* In the product this opens that kind's New modal; the preview toggles the row so
         both states — an unsettled slot and a settled one — are reachable by hand. */
      if (row.dataset.set === 'true') unsetRow(row);
      else setRow(row, SAMPLE[row.dataset.slotRow] || 'Set', null,
                  SAMPLE_VERSE[row.dataset.slotRow], SAMPLE_HTML[row.dataset.slotRow]);
    });
  });

  /* ---------- Use template: one chooser per choice, each with its own kind ---------- */
  /* A chooser is a layer INSIDE the generate modal, not a dialog of its own, so it has to own
     its dismissal: Escape, Cancel and a click on its backdrop close the chooser alone, and the
     focus goes back to the row's control. Otherwise Escape closes the whole modal — the layer
     disappears with it and the operator loses every slot they had settled. */
  var openChooser = null, chooserOpener = null;
  function hideChooser() {
    if (!openChooser) return;
    openChooser.hidden = true;
    openChooser = null;
    if (chooserOpener && document.contains(chooserOpener)) chooserOpener.focus();
    chooserOpener = null;
  }
  function showChooser(layer, opener) {
    hideChooser();
    layer.hidden = false;
    openChooser = layer;
    chooserOpener = opener;
    var first = layer.querySelector('[data-choose-pick]:not([disabled])') || layer.querySelector('[data-choose-close]');
    if (first) first.focus();
  }
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && openChooser) { event.preventDefault(); hideChooser(); }
  });
  generate.addEventListener('cancel', function (event) {
    if (openChooser) { event.preventDefault(); hideChooser(); }
  });

  choiceRows.forEach(function (row) {
    var layer = generate.querySelector('[data-choose="' + row.dataset.choiceRow + '"]');
    var opener = row.querySelector('[data-choice-open]');
    opener.addEventListener('click', function () { showChooser(layer, opener); });
    layer.querySelector('[data-choose-close]').addEventListener('click', hideChooser);
    layer.addEventListener('click', function (event) {
      if (event.target === layer) hideChooser();
    });
    var picks = Array.prototype.slice.call(layer.querySelectorAll('[data-choose-pick]'));
    picks.forEach(function (button) {
      button.addEventListener('click', function () {
        picks.forEach(function (other) {
          other.setAttribute('aria-pressed', String(other === button));
        });
        var item = button.closest('.choose__item');
        var meta = item ? item.querySelector('.choose__meta') : null;
        var bait = row.dataset.choiceRow === 'song' && meta ? meta.textContent : null;
        var value = button.dataset.choosePick;
        var metaText = meta ? meta.textContent.trim() : '';
        var html = null;
        /* A media value always leads with the family; a filename (an untitled media) and a
           title-less text's opening line are quiet next to it. */
        if (row.dataset.choiceRow.indexOf('media') === 0) {
          var parts = metaText.split(' · ');
          var family = parts[0];
          if (family) {
            value = family + ' · ' + value;
            if (parts.length === 1) {
              html = family + ' · <span class="g-quiet">' + button.dataset.choosePick + '</span>';
            }
          }
        }
        if ((row.dataset.choiceRow === 'text' || row.dataset.choiceRow === 'text-plain') && !metaText) {
          html = '<span class="g-quiet">' + value + '</span>';
        }
        setRow(row, value, null, bait, html);
        layer.hidden = true;
      });
    });
    Array.prototype.forEach.call(layer.querySelectorAll('[data-choose-preview]'), function (button) {
      button.addEventListener('click', function () {
        var content = button.closest('.choose__item').querySelector('.choose__content');
        content.hidden = !content.hidden;
        button.setAttribute('aria-expanded', String(!content.hidden));
        button.textContent = content.hidden ? 'Preview' : 'Hide';
      });
    });
  });

  /* ---------- Use template: two steps ---------- */
  function showStep(step) {
    generate.dataset.step = String(step);
    stepOne.hidden = step !== 1;
    stepTwo.hidden = step !== 2;
    stepItems.forEach(function (item) {
      var number = item.querySelector('span i');
      var done = step === 2 && item.dataset.step === '1';
      item.toggleAttribute('data-done', done);
      number.innerHTML = done
        ? '<svg viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M2.5 6.3 4.8 8.6 9.5 3.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        : item.dataset.step;
      if (item.dataset.step === String(step)) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
    });
    var onStepTwo = step === 2;
    nextButton.hidden = onStepTwo;
    createButton.hidden = !onStepTwo;
    backButton.hidden = !onStepTwo;
    cancelButtons.forEach(function (button) { button.hidden = onStepTwo; });
    if (onStepTwo) status.textContent = 'Ready to create.';
    else refresh();
  }
  function resetGenerate() {
    rows.forEach(function (row, index) {
      if (initial[index].set === 'true' && !isChoice(row)) {
        /* restore the row's own authored value, not a sample — a media row's citation is its
           title or filename and the SAMPLE map cannot know it. */
        row.dataset.set = 'true';
        var target = row.querySelector('[data-slot-value], [data-choice-value]');
        if (target) target.innerHTML = initial[index].html;
        var action = row.querySelector('[data-slot-action]');
        if (action) action.textContent = 'Change';
      } else {
        unsetRow(row);
      }
    });
    Array.prototype.forEach.call(generate.querySelectorAll('[data-choose]'), function (layer) {
      layer.hidden = true;
    });
    generate.querySelector('[data-create-confirm]').hidden = true;
    showStep(1);
    refresh();
  }

  nextButton.addEventListener('click', function () { if (!nextButton.disabled) showStep(2); });
  backButton.addEventListener('click', function () { showStep(1); });
  createButton.addEventListener('click', function () {
    generate.querySelector('[data-create-confirm]').hidden = false;
  });
  generate.querySelector('[data-create-cancel]').addEventListener('click', function () {
    generate.querySelector('[data-create-confirm]').hidden = true;
  });
  generate.querySelector('[data-create-accept]').addEventListener('click', function () {
    generate.querySelector('[data-create-confirm]').hidden = true;
    generate.close();
    say('The dated Tata Ibadah was created from the template; the template is unchanged.');
  });

  /* ---------- harness: add bars, theme ---------- */
  /* + Fill-in and + Choice open their own small modals; their kind picker is a chip group. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-add]'), function (button) {
    button.addEventListener('click', function () {
      open(button.dataset.add === 'fillin' ? 'fillinModal' : 'choiceModal');
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll('.kind-pick'), function (group) {
    group.addEventListener('click', function (event) {
      var picked = event.target.closest('button');
      if (!picked) return;
      Array.prototype.forEach.call(group.querySelectorAll('button'), function (button) {
        button.setAttribute('aria-pressed', String(button === picked));
      });
    });
  });

  var barsButton = document.querySelector('[data-toggle-bars]');
  barsButton.addEventListener('click', function () {
    var on = barsButton.getAttribute('aria-pressed') !== 'true';
    barsButton.setAttribute('aria-pressed', String(on));
    Array.prototype.forEach.call(document.querySelectorAll('.entry__add, .entry__start'), function (bar) {
      bar.classList.toggle('is-revealed', on);
    });
  });
  var themeButton = document.querySelector('[data-toggle-theme]');
  themeButton.addEventListener('click', function () {
    var dark = document.documentElement.dataset.theme === 'dark';
    document.documentElement.dataset.theme = dark ? 'light' : 'dark';
    themeButton.textContent = dark ? 'Dark' : 'Light';
  });

  /* initial state */
  setKind('normal');
  refresh();
})();
