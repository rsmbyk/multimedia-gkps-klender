"""Build the spec 255 preview from the repo's own CSS and the real button markup."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / 'index.html'

tokens = (ROOT / 'static/styles/design/tokens.css').read_text()
components = (ROOT / 'static/styles/design/components.css').read_text()

SVG = '''<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7"
  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <rect x="3" y="3.4" width="11.4" height="13.2" rx="1.8"/>
  <path d="M6.2 6.8h5M6.2 9.6h5M6.2 12.4h3"/>
  <path d="M16.2 10.2v5.6M13.4 13h5.6"/></svg>'''

HTML = r'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Use template — saved indicator (spec 255)</title>
<style>
/*__CSS__*/
/* preview-only chrome */
body { margin: 0; background: var(--canvas); color: var(--ink); font: 400 14px/1.5 ui-sans-serif, system-ui, sans-serif; }
.pv { max-width: 900px; padding: 28px; }
.pv h1 { margin: 0 0 4px; font: 650 19px/1.3 ui-sans-serif, system-ui, sans-serif; }
.pv p.lead { margin: 0 0 20px; color: var(--head-ink); font-size: 12.5px; }
.pv-band { border: 1px solid var(--divider); border-radius: 12px; overflow: hidden; margin: 0 0 22px; }
.pv-headbar { display: flex; align-items: center; gap: 12px; padding: 14px 20px; background: var(--rail-bg); border-bottom: 1px solid var(--divider); }
.pv-date { color: var(--head-ink); font: 600 11px/1.2 ui-sans-serif, system-ui, sans-serif; letter-spacing: .08em; text-transform: uppercase; }
.pv-title { flex: 1; font: 650 17px/1.2 ui-sans-serif, system-ui, sans-serif; }
.pv-body { padding: 20px; background: var(--canvas); }
.pv-row { display: grid; grid-template-columns: 44px 1fr auto; align-items: center; gap: 16px; padding: 16px 0; border-top: 1px solid var(--divider); }
.pv-row:first-child { border-top: 0; }
.pv-key { display: grid; place-items: center; width: 30px; height: 30px; border-radius: 50%; border: 1px solid var(--divider); font: 650 13px/1 ui-sans-serif, system-ui, sans-serif; }
.pv-desc { color: var(--head-ink); font-size: 12.5px; }
.pv-desc strong { color: var(--ink); }
.pv-controls { display: flex; gap: 10px; align-items: center; margin: 0 0 18px; }
.pv-controls button { height: 34px; padding: 0 14px; border: 1px solid var(--divider); border-radius: 9px; background: none; color: var(--ink); cursor: pointer; font: 600 13px ui-sans-serif, system-ui, sans-serif; }
.pv-controls button[aria-pressed="true"] { border-color: var(--active-bg); color: var(--active-ink); background: var(--active-bg); }
.pv-readout { margin-top: 18px; padding: 12px; border-radius: 8px; background: var(--rail-bg); font: 400 11px/1.6 ui-monospace, monospace; white-space: pre-wrap; }
/* ---- the three candidate marks; only one ships ---- */
.read__project-btn[data-draft="true"][data-variant="a"] { position: relative; }
[data-variant="a"] .pv-dot { position: absolute; top: 3px; right: 3px; width: 7px; height: 7px; border-radius: 50%; background: var(--active-ink); display: none; }
[data-variant="b"] .pv-dot { display: none; }
[data-variant="c"] .pv-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--active-ink); flex: none; display: none; }
.read__project-btn[data-draft="true"][data-variant="a"] .pv-dot,
.read__project-btn[data-draft="true"][data-variant="c"] .pv-dot { display: block; }
[data-variant="b"] .pv-label-saved { display: none; }
.pv-label-saved { display: none; }
.read__project-btn[data-draft="true"][data-variant="b"] .pv-label { display: none; }
.read__project-btn[data-draft="true"][data-variant="b"] .pv-label-saved { display: inline; }
</style>
</head>
<body>
<div class="pv">
  <h1>Use template — saved-draft indicator</h1>
  <p class="lead">Spec 255. Same 34px button, same fill; only the mark differs. Toggle the saved state to compare.</p>

  <div class="pv-controls">
    <button type="button" id="toggle" aria-pressed="true">Saved draft: ON</button>
    <span class="pv-desc">click to compare the no-draft state</span>
  </div>

  <div class="pv-band">
    <div class="pv-headbar">
      <span class="pv-date">Template</span>
      <span class="pv-title">Ibadah Minggu</span>
      <div class="read__project" data-generate-group>
        <button type="button" class="read__project-btn">Media files</button>
        <button type="button" class="read__project-btn read__project-btn--primary" data-generate-open
                data-variant="a" data-draft="true" aria-label="Use template, draft saved">
          __SVG__<span class="pv-label">Use template</span><span class="pv-label-saved">Use template · draft saved</span><span class="pv-dot" aria-hidden="true"></span>
        </button>
      </div>
    </div>
    <div class="pv-body">
      <div class="pv-row" data-example="a">
        <span class="pv-key">A</span>
        <span class="pv-desc"><strong>Corner dot</strong> — a 7px dot inset 3px from the top-right, label unchanged. Accessible name: “Use template, draft saved”.</span>
        <div class="read__project" data-generate-group>
          <button type="button" class="read__project-btn read__project-btn--primary" data-generate-open
                  data-variant="a" data-draft="true" aria-label="Use template, draft saved">
            __SVG__<span class="pv-label">Use template</span><span class="pv-label-saved">Use template · draft saved</span><span class="pv-dot" aria-hidden="true"></span>
          </button>
        </div>
      </div>
      <div class="pv-row" data-example="b">
        <span class="pv-key">B</span>
        <span class="pv-desc"><strong>Label suffix</strong> — the label itself reads “Use template · draft saved”; the button widens by the text.</span>
        <div class="read__project" data-generate-group>
          <button type="button" class="read__project-btn read__project-btn--primary" data-generate-open
                  data-variant="b" data-draft="true">
            __SVG__<span class="pv-label">Use template</span><span class="pv-label-saved">Use template · draft saved</span><span class="pv-dot" aria-hidden="true"></span>
          </button>
        </div>
      </div>
      <div class="pv-row" data-example="c">
        <span class="pv-key">C</span>
        <span class="pv-desc"><strong>Inline dot</strong> — a 6px dot seated before the icon with the button's own 6px gap, pushing the label right.</span>
        <div class="read__project" data-generate-group>
          <button type="button" class="read__project-btn read__project-btn--primary" data-generate-open
                  data-variant="c" data-draft="true" aria-label="Use template, draft saved">
            <span class="pv-dot" aria-hidden="true"></span>__SVG__<span class="pv-label">Use template</span><span class="pv-label-saved">Use template · draft saved</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="pv-readout" id="readout"></div>
</div>
<script>
(function () {
  var toggle = document.getElementById('toggle');
  var readout = document.getElementById('readout');
  function measure() {
    var out = [];
    ['a', 'b', 'c'].forEach(function (v) {
      var btn = document.querySelector('[data-example="' + v + '"] [data-generate-open]');
      var dot = btn.querySelector('.pv-dot');
      var b = btn.getBoundingClientRect();
      var d = dot.getBoundingClientRect();
      var label = btn.querySelector('.pv-label').getBoundingClientRect();
      out.push(v.toUpperCase() + ': button ' + b.width.toFixed(1) + '×' + b.height.toFixed(1) +
        ' | dot ' + d.width.toFixed(1) + '×' + d.height.toFixed(1) +
        (d.width ? ' | dot@ ' + (d.left - b.left).toFixed(1) + ',' + (d.top - b.top).toFixed(1) : '') +
        ' | name "' + (btn.getAttribute('aria-label') || btn.innerText.trim()) + '"');
    });
    readout.textContent = out.join('\n');
  }
  toggle.addEventListener('click', function () {
    var on = toggle.getAttribute('aria-pressed') !== 'true';
    toggle.setAttribute('aria-pressed', String(on));
    toggle.textContent = 'Saved draft: ' + (on ? 'ON' : 'OFF');
    document.querySelectorAll('[data-generate-open]').forEach(function (btn) {
      var v = btn.dataset.variant;
      btn.dataset.draft = String(on);
      if (v === 'b') { btn.removeAttribute('aria-label'); }
      else { btn.setAttribute('aria-label', on ? 'Use template, draft saved' : 'Use template'); }
    });
    window.requestAnimationFrame(measure);
  });
  window.requestAnimationFrame(measure);
})();
</script>
</body>
</html>
'''

HTML = HTML.replace('/*__CSS__*/', tokens + '\n' + components).replace('__SVG__', SVG)
OUT.write_text(HTML)
print(f'wrote {OUT} ({OUT.stat().st_size} bytes)')