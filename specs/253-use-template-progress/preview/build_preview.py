"""Build a self-contained static preview for spec 253 from the project's own CSS.

The markup mirrors the real reading/_generate_modal.html slot rows and confirm layer;
the CSS is the repo's tokens.css + generate.css + components.css verbatim. Only the
demo script is new, and it implements the behaviour the spec proposes.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # repository root
OUT = Path(__file__).resolve().parent / 'index.html'

tokens = (ROOT / 'static/styles/design/tokens.css').read_text()
generate = (ROOT / 'static/styles/design/generate.css').read_text()
components = (ROOT / 'static/styles/design/components.css').read_text()

HTML = r'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Use template progress — spec 253 preview</title>
<style>
/*__CSS__*/
/* preview-only chrome, not a product component */
body { margin: 0; background: var(--canvas); color: var(--ink); font: 400 14px/1.5 ui-sans-serif, system-ui, sans-serif; }
.pv-wrap { display: grid; grid-template-columns: minmax(320px, 1fr) 300px; gap: 24px; padding: 24px; align-items: start; }
.pv-stage { position: relative; min-height: 780px; display: grid; place-items: center; }
.pv-panel { border: 1px solid var(--divider); border-radius: 12px; padding: 16px; background: var(--canvas); }
.pv-panel h2 { margin: 0 0 10px; font: 650 15px/1.3 ui-sans-serif, system-ui, sans-serif; }
.pv-panel p { margin: 0 0 12px; color: var(--head-ink); font-size: 12.5px; }
.pv-panel button { height: 34px; padding: 0 12px; margin: 0 6px 8px 0; border: 1px solid var(--divider); border-radius: 8px; background: none; color: var(--ink); cursor: pointer; font: 500 13px ui-sans-serif, system-ui, sans-serif; }
.pv-panel button:hover { background: var(--rail-bg); }
.pv-readout { margin-top: 12px; padding: 10px; border-radius: 8px; background: var(--rail-bg); font: 400 11px/1.6 ui-monospace, monospace; white-space: pre-wrap; word-break: break-all; min-height: 70px; }
.pv-note { margin-top: 8px; color: var(--head-ink); font-size: 11.5px; }
.pv-toast { position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%); padding: 10px 16px; border-radius: 8px; background: var(--ink); color: var(--canvas); font-size: 13px; opacity: 0; transition: opacity .18s ease; pointer-events: none; z-index: 20; }
.pv-toast.on { opacity: 1; }
/* the real modal is a <dialog>; here it is laid out as a centred sheet in the stage */
.pv-stage .generate { position: relative; width: min(840px, 100%); height: 760px; border: 1px solid var(--divider); border-radius: 12px; box-shadow: var(--shadow-dialog); overflow: hidden; display: flex; }
.pv-stage .generate[hidden] { display: none; }
.pv-stage .editor__content { flex: 1; min-width: 0; }
@media (max-width: 1000px) { .pv-wrap { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="pv-wrap">
  <div class="pv-stage">
    <div class="editor generate" id="generateModal" data-generate-tatib="101" data-generate-name="Ibadah Minggu" data-step="1">
      <div class="editor__content" data-editor-size="large">
        <header class="generate__head">
          <ol class="generate__steps" aria-label="Steps">
            <li data-step="1" aria-current="step"><span class="generate__step-mark"><i>1</i></span><span class="generate__step-label">Fill in the entries</span></li>
            <li data-step="2"><span class="generate__step-mark"><i>2</i></span><span class="generate__step-label">Name and date</span></li>
          </ol>
          <h2 class="editor__title" id="generateTitle">New Tata Ibadah</h2>
          <p class="generate__from">From template · <strong data-template-name>Ibadah Minggu</strong></p>
        </header>
        <div class="generate__body" data-generate-step="1">
          <div class="g-row g-fixed"><section class="tatib__item"><h2 class="read__sec">Pembukaan</h2><p class="tatib__tx">Doa pembukaan</p></section></div>
          <div class="g-row g-row--slot" data-slot-row="11" data-slot-kind-name="fill-in" data-slot-kind="song" data-set="false">
            <div class="g-main"><p class="g-label">Fill-in · Song</p><p class="g-title">Kidung Jemaat</p><p class="g-value" data-slot-value>Not set</p></div>
            <button class="g-action" type="button" data-slot-action>Set</button>
          </div>
          <div class="g-row g-row--slot" data-slot-row="12" data-slot-kind-name="choice" data-slot-kind="scripture" data-set="false" data-choice-row="12" data-choice-count="2">
            <div class="g-main"><p class="g-label">Choice · Scripture</p><p class="g-title">Firman</p><p class="g-value" data-slot-value>2 options</p></div>
            <button class="g-action" type="button" data-choice-open>Choose</button>
          </div>
        </div>
        <div class="generate__body generate__body--form" data-generate-step="2" hidden>
          <div class="editor__field"><label for="generateName">Name</label>
            <input type="text" id="generateName" value="Ibadah Minggu" data-generate-name-input></div>
          <div class="editor__field"><label for="generateDate">Date</label>
            <input type="date" id="generateDate" data-generate-date></div>
          <p class="pv-note">Continuous save writes on every change on this step too.</p>
        </div>
        <footer class="generate__foot">
          <p class="generate__status" data-generate-status role="status">—</p>
          <div class="generate__actions">
            <button class="editor__cancel" type="button" data-generate-back hidden>Back</button>
            <button class="editor__cancel" type="button" data-generate-close>Cancel</button>
            <button class="generate__next" type="button" data-generate-next disabled>Next</button>
            <button class="editor__save" type="button" data-generate-create hidden>Create</button>
          </div>
        </footer>

        <div class="choose-layer" data-choose="12" hidden>
          <div class="choose" role="dialog" aria-modal="true">
            <header class="choose__head"><h3>Firman</h3><p>2 options for this entry.</p></header>
            <div class="choose__list">
              <div class="choose__item" data-pick-label="Yohanes 3:16" data-pick-main="Yohanes 3:16" data-pick-mute="TB"><button class="choose__pick" type="button" data-choose-pick="21">Choose</button></div>
              <div class="choose__item" data-pick-label="Matius 5:13" data-pick-main="Matius 5:13" data-pick-mute="TB"><button class="choose__pick" type="button" data-choose-pick="22">Choose</button></div>
            </div>
            <footer class="choose__foot"><button type="button" data-choose-close>Cancel</button></footer>
          </div>
        </div>

        <div class="generate__confirm-layer" data-generate-leave hidden>
          <div class="editor__confirm" role="alertdialog" aria-modal="true" aria-labelledby="leaveTitle">
            <h3 id="leaveTitle">Leave this template?</h3>
            <p>Your progress is saved in this browser session. Reopen <strong data-template-name>Ibadah Minggu</strong> to pick up where you left off.</p>
            <div class="editor__confirm-actions">
              <button type="button" class="editor__cancel" data-leave-stay>Stay</button>
              <button type="button" class="editor__save" data-leave-accept>Leave</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <aside class="pv-panel">
    <h2>Use template — progress preview</h2>
    <p>Spec 253. Live behaviour is in the page: settle a slot, close, reopen. sessionStorage is keyed by template id.</p>
    <button type="button" data-open="101">Open template A</button>
    <button type="button" data-open="202">Open template B</button>
    <button type="button" data-reload>Reload page</button>
    <button type="button" data-clear>Clear session</button>
    <div class="pv-readout" data-readout></div>
    <p class="pv-note">A and B hold separate progress. Closing the browser session clears both.</p>
  </aside>
</div>
<div class="pv-toast" data-toast></div>
<script>
(function () {
  'use strict';
  var modal = document.getElementById('generateModal');
  var names = { '101': 'Ibadah Minggu', '202': 'Ibadah Paskah' };
  var rows = Array.prototype.slice.call(modal.querySelectorAll('.g-row--slot'));
  var status = modal.querySelector('[data-generate-status]');
  var nextButton = modal.querySelector('[data-generate-next]');
  var backButton = modal.querySelector('[data-generate-back]');
  var createButton = modal.querySelector('[data-generate-create]');
  var closeButton = modal.querySelector('[data-generate-close]');
  var nameInput = modal.querySelector('[data-generate-name-input]');
  var dateInput = modal.querySelector('[data-generate-date]');
  var leaveLayer = modal.querySelector('[data-generate-leave]');
  var chooser = modal.querySelector('[data-choose]');
  var settled = {}, current = '101', dirty = false, toastTimer;

  function key(id) { return 'gkps:generate:' + id; }
  function read(id) {
    try { return JSON.parse(sessionStorage.getItem(key(id)) || 'null'); }
    catch (e) { return null; }
  }
  function write() {
    try {
      sessionStorage.setItem(key(current), JSON.stringify({
        step: Number(modal.dataset.step || 1), settled: settled,
        name: nameInput.value, date: dateInput.value
      }));
    } catch (e) { /* storage unavailable: the modal still works */ }
    dirty = Object.keys(settled).length > 0;
    readout();
  }
  function clearSaved() {
    try { sessionStorage.removeItem(key(current)); } catch (e) {}
  }
  function readout() {
    var out = [];
    try {
      for (var i = 0; i < sessionStorage.length; i++) {
        var k = sessionStorage.key(i);
        if (k.indexOf('gkps:generate:') === 0) out.push(k + '\n  ' + sessionStorage.getItem(k));
      }
    } catch (e) { out.push('(storage unavailable in this frame — open the file in a browser)'); }
    document.querySelector('[data-readout]').textContent = out.length ? out.join('\n') : '(no saved progress)';
  }

  function paint(row, state) {
    var value = row.querySelector('[data-slot-value]');
    var action = row.querySelector('[data-slot-action], [data-choice-open]');
    row.dataset.set = state ? 'true' : 'false';
    if (state && state.main) { value.textContent = state.main + ' · ' + (state.mute || ''); }
    else { value.textContent = state ? state.label : (row.dataset.slotKindName === 'choice' ? row.dataset.choiceCount + ' options' : 'Not set'); }
    action.textContent = state ? 'Change' : (row.dataset.slotKindName === 'choice' ? 'Choose' : 'Set');
  }
  function refresh() {
    rows.forEach(function (row) {
      var id = row.dataset.slotRow;
      if (!document.body.contains(row)) return;
      paint(row, settled[id]);
    });
    var done = rows.filter(function (r) { return !!settled[r.dataset.slotRow]; }).length;
    var left = rows.length - done;
    status.textContent = left === 0 ? 'All ' + rows.length + ' entries settled.' : done + ' of ' + rows.length + ' settled — ' + left + ' left to fill in.';
    nextButton.disabled = left !== 0;
  }
  function setStep(step) {
    modal.dataset.step = String(step);
    modal.querySelector('[data-generate-step="1"]').hidden = step !== 1;
    modal.querySelector('[data-generate-step="2"]').hidden = step !== 2;
    modal.querySelectorAll('.generate__steps li').forEach(function (li) {
      if (li.dataset.step === String(step)) li.setAttribute('aria-current', 'step');
      else li.removeAttribute('aria-current');
    });
    nextButton.hidden = step === 2;
    backButton.hidden = step !== 2;
    createButton.hidden = step !== 2;
  }
  function openTemplate(id) {
    current = id;
    modal.dataset.generateTatib = id;
    modal.querySelectorAll('[data-template-name]').forEach(function (n) { n.textContent = names[id]; });
    var saved = read(id) || { settled: {}, step: 1, name: names[id], date: '' };
    settled = {};
    Object.keys(saved.settled || {}).forEach(function (sid) {
      if (rows.some(function (r) { return r.dataset.slotRow === sid; })) settled[sid] = saved.settled[sid];
    });
    nameInput.value = saved.name || names[id];
    dateInput.value = saved.date || '';
    setStep(saved.step || 1);
    refresh();
    leaveLayer.hidden = true;
    chooser.hidden = true;
    modal.hidden = false;
    toast('Opened template ' + id + (read(id) ? ' — progress restored' : ' — fresh'));
  }
  function attemptClose() {
    if (!chooser.hidden) { chooser.hidden = true; return; }
    if (dirty || Object.keys(settled).length) { leaveLayer.hidden = false; return; }
    modal.hidden = true;
  }
  function toast(text) {
    var el = document.querySelector('[data-toast]');
    el.textContent = text; el.classList.add('on');
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () { el.classList.remove('on'); }, 2400);
  }

  modal.querySelector('.pv-stage-scrim');
  modal.addEventListener('click', function (e) {
    if (e.target.closest('[data-slot-action]')) {
      var row = e.target.closest('.g-row--slot');
      settled[row.dataset.slotRow] = { label: 'KJ 152 · Kidung Jemaat' };
      write(); refresh(); return;
    }
    if (e.target.closest('[data-choice-open]')) { chooser.hidden = false; return; }
    var pick = e.target.closest('[data-choose-pick]');
    if (pick) {
      var item = pick.closest('.choose__item');
      settled['12'] = { main: item.dataset.pickMain, mute: item.dataset.pickMute };
      write(); refresh(); chooser.hidden = true; return;
    }
    if (e.target.closest('[data-choose-close]')) { chooser.hidden = true; return; }
    if (e.target.closest('[data-leave-stay]')) { leaveLayer.hidden = true; return; }
    if (e.target.closest('[data-leave-accept]')) { leaveLayer.hidden = true; modal.hidden = true; toast('Left — progress saved'); return; }
    if (e.target.closest('[data-generate-close]')) { attemptClose(); return; }
    if (e.target.closest('[data-generate-back]')) { setStep(1); return; }
    if (e.target.closest('[data-generate-next]') && !nextButton.disabled) { setStep(2); write(); return; }
    if (e.target.closest('[data-generate-create]')) { clearSaved(); modal.hidden = true; readout(); toast('Created — progress cleared'); return; }
  });
  nameInput.addEventListener('input', write);
  dateInput.addEventListener('change', write);
  modal.addEventListener('click', function (e) {
    if (e.target === leaveLayer) leaveLayer.hidden = true;
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) { e.preventDefault(); attemptClose(); }
  });
  document.querySelectorAll('[data-open]').forEach(function (b) {
    b.addEventListener('click', function () { openTemplate(b.dataset.open); });
  });
  document.querySelector('[data-reload]').addEventListener('click', function () { location.reload(); });
  document.querySelector('[data-clear]').addEventListener('click', function () {
    try { sessionStorage.clear(); } catch (e) {}
    readout(); toast('Browser session storage cleared');
  });
  readout();
  openTemplate('101');
})();
</script>
</body>
</html>
'''

HTML = HTML.replace('/*__CSS__*/', tokens + '\n' + generate + '\n' + components)
OUT.write_text(HTML)
print(f'wrote {OUT} ({OUT.stat().st_size} bytes)')
