from pathlib import Path
import subprocess

REPO = Path('/home/rsmbyk/Projects/multimedia-gkps-klender-257')
OUT = REPO / 'specs/257-modal-scroll-containment/preview/index.html'
BASE_SHA = '1cd9f081'
DIR = 'static/styles/design/'


def base_css(name):
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{BASE_SHA}:{DIR}{name}'], text=True)


def slice_css(name):
    return (REPO / DIR / name).read_text()


shared = '\n'.join(slice_css(n) for n in ('tokens.css', 'fonts.css', 'generate.css'))
before = base_css('components.css')
after = slice_css('components.css')

html = """<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<title>Spec 257 — modal scroll containment</title>
<style>%s</style>
<style id="css-before">%s</style>
<style id="css-after">%s</style>
<style>
  body { margin: 0; font-family: ui-sans-serif, system-ui, sans-serif; }
  .probebar { position: fixed; z-index: 5; top: 0; left: 0; right: 0; display: flex; flex-wrap: wrap; gap: 8px;
    align-items: center; padding: 8px 12px; background: var(--canvas); border-bottom: 1px solid var(--divider); }
  .probebar button { min-height: 30px; padding: 0 10px; border: 1px solid var(--divider); border-radius: 7px;
    background: var(--rail-bg); color: var(--ink); cursor: pointer; }
  .probebar button[aria-pressed="true"] { background: var(--active-bg); color: var(--active-ink); }
  .probebar .note { color: var(--head-ink); font-size: 12px; }
  .probe-page { padding: 64px 22px 0; }
  .probe-page h1 { font-size: 17px; }
  .probe-page .row { height: 28px; border-bottom: 1px solid var(--divider); }
  #readout { position: fixed; z-index: 6; right: 12px; bottom: 12px; padding: 8px 10px; max-width: 340px;
    background: var(--canvas); border: 1px solid var(--divider); border-radius: 8px; font: 12px/1.5 monospace; white-space: pre-line; }
  .editor__picker-menu { position: static; }
</style>
</head>
<body>
<div class="probebar">
  <button id="before" aria-pressed="true">Before (base CSS)</button>
  <button id="after" aria-pressed="false">After (slice CSS)</button>
  <button id="openEditor">Open editor</button>
  <button id="openPicker">Open picker</button>
  <button id="openPreview">Open preview</button>
  <span class="note">Scroll the page, then scroll the modal to its end — or open the short variant.</span>
</div>
<main class="probe-page"><h1>Page behind the modal — scroll this</h1><div id="pageRows"></div></main>
<dialog class="editor" id="editorModal"><div class="editor__content" id="editorContent"></div></dialog>
<dialog class="preview" id="previewModal"><div class="preview__body" id="previewBody"></div></dialog>
<output id="readout"></output>
<script>
(function () {
  var before = document.getElementById('before'), after = document.getElementById('after');
  var styleBefore = document.getElementById('css-before'), styleAfter = document.getElementById('css-after');
  styleAfter.disabled = true;
  function variant(which) {
    var isBefore = which === 'before';
    styleBefore.disabled = !isBefore; styleAfter.disabled = isBefore;
    before.setAttribute('aria-pressed', String(isBefore)); after.setAttribute('aria-pressed', String(!isBefore));
  }
  before.addEventListener('click', function () { variant('before'); });
  after.addEventListener('click', function () { variant('after'); });
  function rows(n, prefix) {
    var out = '';
    for (var i = 0; i < n; i++) out += '<p class="' + prefix + '" style="height:28px;margin:0">' + prefix + ' ' + i + '</p>';
    return out;
  }
  document.getElementById('pageRows').innerHTML = rows(80, 'page-row');
  document.getElementById('openEditor').addEventListener('click', function () {
    var body = document.getElementById('editorContent');
    body.innerHTML = '<p style="margin:0 0 10px">Wheel here; the editor body has 40 rows.</p>' + rows(40, 'editor-row');
    document.getElementById('editorModal').showModal();
  });
  document.getElementById('openPicker').addEventListener('click', function () {
    var body = document.getElementById('editorContent');
    body.innerHTML = rows(10, 'editor-row') +
      '<div class="editor__picker-menu"><div class="editor__picker-options">' + rows(40, 'option') + '</div></div>';
    document.getElementById('editorModal').showModal();
  });
  document.getElementById('openPreview').addEventListener('click', function () {
    document.getElementById('previewBody').innerHTML = rows(40, 'preview-row');
    document.getElementById('previewModal').showModal();
  });
  document.addEventListener('click', function (e) {
    if (e.target.tagName === 'DIALOG') e.target.close();
  });
  function show() {
    var open = document.querySelector('dialog[open]');
    var inner = open && (open.querySelector('.editor__picker-options') || open.querySelector('.editor__content') || open.querySelector('.preview__body'));
    var content = document.getElementById('editorContent');
    document.getElementById('readout').textContent =
      'variant: ' + (styleBefore.disabled ? 'after' : 'before') +
      '\\ndialog open: ' + (open ? open.id : 'none') +
      '\\ndoc scrollY: ' + Math.round(scrollY) +
      '\\nroot overflow-y: ' + getComputedStyle(document.documentElement).overflowY +
      '\\ninner over-scroll: ' + (inner ? getComputedStyle(inner).overscrollBehaviorY : '—') +
      '\\ninner scrollTop: ' + (inner ? inner.scrollTop : '—') +
      '\\neditor scrollTop: ' + content.scrollTop;
  }
  setInterval(show, 120);
})();
</script>
</body>
</html>
""" % (shared, before, after)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html)
print(f'wrote {OUT} ({OUT.stat().st_size} bytes)')
