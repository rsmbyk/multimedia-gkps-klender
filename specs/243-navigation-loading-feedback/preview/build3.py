#!/usr/bin/env python3
"""Spec 243 preview v3: researched loading treatments, three surfaces.

Builds index.html from the real /bible/1/1/ shell. Three treatments:
quiet in-pane strip, shape-matched skeleton, placeholder child rows.
Each can be triggered from the rail, a first-level row, or a second-level row.
"""
import re

from build import HERE, catalogue_css, inline_images

PREVIEW_CSS = r'''
/* ---- Preview chrome ------------------------------------------------------ */
:root { --pv-top: 76px; }
body { padding-top: var(--pv-top); }
.pv-bar {
  position: fixed; inset: 0 0 auto 0; height: var(--pv-top); z-index: 9000;
  display: flex; flex-direction: column; justify-content: center; gap: 5px;
  padding: 6px 12px; background: var(--rail-bg);
  border-bottom: 1px solid var(--divider); color: var(--ink);
  font: 12px/1.3 ui-sans-serif, system-ui, sans-serif;
}
.pv-row { display: flex; align-items: center; gap: 7px; }
.pv-row__label { font-weight: 650; min-width: 72px; opacity: .85; }
.pv-row__hint { margin-left: auto; opacity: .72; white-space: nowrap; }
.pv-bar button {
  border: 1px solid var(--divider); border-radius: 6px; padding: 4px 9px;
  background: transparent; color: inherit; font: inherit; cursor: pointer;
}
.pv-bar button:hover { background: var(--icon-hover-bg); }
.pv-bar button[aria-pressed="true"] { background: var(--active-bg); color: var(--active-ink); border-color: transparent; }
.pv-bar button:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.pv-asset { display: inline-block; background-size: contain; background-repeat: no-repeat; background-position: center; }
.rail, .panel, .chapters, .topbar { top: var(--pv-top) !important; }

/* ---- Treatment A: a quiet busy strip in the destination pane ------------ */
.pv-strip {
  display: none; align-items: center; gap: 8px; padding: 6px 10px;
  background: var(--rail-bg); border-bottom: 1px solid var(--divider);
  color: var(--ink); font: 12px/1.3 ui-sans-serif, system-ui, sans-serif;
}
.pv-strip__spin {
  flex: none; width: 12px; height: 12px; border: 2px solid var(--divider);
  border-top-color: var(--active-bg); border-radius: 50%;
  animation: pv-spin .8s linear infinite;
}
.stage { position: relative !important; }
.pv-strip--stage {
  position: absolute; top: 10px; right: 14px; z-index: 6;
  padding: 7px 11px; border: 1px solid var(--divider); border-radius: 6px;
  background: var(--rail-bg); box-shadow: 0 1px 2px rgba(0,0,0,.09);
}

/* ---- Treatment B: shape-matched skeleton in the destination pane -------- */
#panelBody, #chBody, #readBody { position: relative !important; }
.pv-skel {
  display: none; position: absolute; inset: 0; z-index: 5; padding: 10px 12px;
  background: var(--canvas); overflow: hidden;
}
.pv-skel__row {
  display: flex; align-items: center; gap: 9px; height: 38px;
  border-bottom: 1px solid var(--divider);
}
.pv-skel__dot { width: 12px; height: 12px; border-radius: 50%; background: var(--divider); flex: none; }
.pv-skel__bar { height: 9px; border-radius: 4px; background: var(--divider); opacity: .72; }
.pv-skel__row:nth-child(1) .pv-skel__bar { width: 62%; }
.pv-skel__row:nth-child(2) .pv-skel__bar { width: 78%; }
.pv-skel__row:nth-child(3) .pv-skel__bar { width: 55%; }
.pv-skel__row:nth-child(4) .pv-skel__bar { width: 70%; }
.pv-skel__row:nth-child(5) .pv-skel__bar { width: 64%; }
.pv-skel__row:nth-child(6) .pv-skel__bar { width: 81%; }
.pv-skel__row:nth-child(7) .pv-skel__bar { width: 58%; }
.pv-skel__row:nth-child(8) .pv-skel__bar { width: 72%; }
.pv-skel__line { height: 13px; margin: 14px 0; border-radius: 4px; background: var(--divider); opacity: .62; }
.pv-skel__line:nth-child(1) { width: 56%; height: 20px; }
.pv-skel__line:nth-child(2) { width: 88%; }
.pv-skel__line:nth-child(3) { width: 94%; }
.pv-skel__line:nth-child(4) { width: 73%; }
.pv-skel__line:nth-child(5) { width: 91%; }
.pv-skel__line:nth-child(6) { width: 67%; }

/* ---- Treatment C: placeholder child rows under a stable selection ------- */
.pv-place {
  display: none; position: absolute; inset: 0; z-index: 5; padding: 10px 12px;
  background: var(--canvas);
}
.pv-place__row {
  display: flex; align-items: center; gap: 9px; height: 38px;
  border-bottom: 1px solid var(--divider); color: var(--head-ink);
  font: 12px/1.3 ui-sans-serif, system-ui, sans-serif;
}
.pv-place__caret { width: 8px; height: 8px; border-left: 2px solid var(--active-bg); border-bottom: 2px solid var(--active-bg); transform: rotate(-45deg); opacity: .55; }
.pv-place__bar { height: 9px; border-radius: 4px; background: var(--divider); opacity: .72; }
.pv-place__row:nth-child(1) .pv-place__bar { width: 66%; }
.pv-place__row:nth-child(2) .pv-place__bar { width: 52%; }
.pv-place__row:nth-child(3) .pv-place__bar { width: 74%; }
.pv-place__row:nth-child(4) .pv-place__bar { width: 58%; }

/* ---- Visibility matrix: only the destination panes go busy -------------- */
.pv-busy.pv-both-panel  #panelBody .pv-strip, .pv-busy.pv-both-ch    #chBody .pv-strip,
.pv-busy.pv-both-stage  .stage > .pv-strip { display: flex; }
.pv-busy.pv-both-panel  #panelBody .pv-skel, .pv-busy.pv-both-ch    #chBody .pv-skel,
.pv-busy.pv-both-stage  #readBody .pv-skel { display: block; }
.pv-busy.pv-both-panel  #panelBody > :not(.pv-skel):not(.pv-strip):not(.pv-place),
.pv-busy.pv-both-ch     #chBody > :not(.pv-skel):not(.pv-strip):not(.pv-place),
.pv-busy.pv-both-stage  #readBody > :not(.pv-skel):not(.pv-strip):not(.pv-place) { visibility: hidden; }
.pv-busy.pv-both-panel  #panelBody .pv-place, .pv-busy.pv-both-ch #chBody .pv-place { display: block; }
html[data-treatment="quiet"] #panelBody .pv-skel,
html[data-treatment="quiet"] #chBody .pv-skel,
html[data-treatment="quiet"] #readBody .pv-skel,
html[data-treatment="quiet"] #panelBody .pv-place,
html[data-treatment="quiet"] #chBody .pv-place { display: none !important; }
html[data-treatment="skeleton"] .pv-strip,
html[data-treatment="skeleton"] .pv-place { display: none !important; }
html[data-treatment="placeholder"] .pv-strip:not(.pv-strip--stage),
html[data-treatment="placeholder"] .pv-skel { display: none !important; }
html[data-treatment="quiet"] #panelBody > :not(.pv-skel):not(.pv-strip):not(.pv-place),
html[data-treatment="quiet"] #chBody > :not(.pv-skel):not(.pv-strip):not(.pv-place),
html[data-treatment="quiet"] #readBody > :not(.pv-skel):not(.pv-strip):not(.pv-place),
html[data-treatment="placeholder"] #readBody > :not(.pv-skel):not(.pv-strip):not(.pv-place) { visibility: visible !important; }

.pv-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
@media (prefers-reduced-motion: reduce) { .pv-strip__spin { animation: none; } }
@keyframes pv-spin { to { transform: rotate(360deg); } }
'''

JS = r'''
(function () {
  var root = document.documentElement;
  var hint = document.getElementById('pvHint');
  var treatments = [...document.querySelectorAll('.pv-bar button[data-treatment]')];
  var scenarios = [...document.querySelectorAll('.pv-bar button[data-scenario]')];
  var showTimer, settleTimer;
  var hints = {
    quiet: '0 ms: selection unchanged · 300 ms: quiet strip in destination',
    skeleton: '0 ms: selection unchanged · 300 ms: shape-matched skeleton',
    placeholder: '0 ms: selection unchanged · 300 ms: placeholder child rows'
  };
  function replay() {
    clearTimeout(showTimer); clearTimeout(settleTimer);
    root.classList.remove('pv-busy', 'pv-both-panel', 'pv-both-ch', 'pv-both-stage');
    var scenario = root.dataset.scenario;
    root.dataset.nav = 'open';
    root.dataset.ch = 'open';
    hint.textContent = hints[root.dataset.treatment];
    if (scenario === 'rail') root.classList.add('pv-both-panel', 'pv-both-ch', 'pv-both-stage');
    else if (scenario === 'first') root.classList.add('pv-both-ch', 'pv-both-stage');
    else root.classList.add('pv-both-stage');
    showTimer = setTimeout(function () {
      root.classList.add('pv-busy');
      document.getElementById('pvLive').textContent = 'Loading page';
    }, 300);
    settleTimer = setTimeout(function () {
      clearTimeout(showTimer);
      root.classList.remove('pv-busy', 'pv-both-panel', 'pv-both-ch', 'pv-both-stage');
      document.getElementById('pvLive').textContent = 'Page opened';
    }, 2400);
  }
  treatments.forEach(function (b) {
    b.addEventListener('click', function () {
      treatments.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      root.dataset.treatment = b.dataset.treatment;
      replay();
    });
  });
  scenarios.forEach(function (b) {
    b.addEventListener('click', function () {
      scenarios.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      root.dataset.scenario = b.dataset.scenario;
      replay();
    });
  });
  document.getElementById('pvReplay').addEventListener('click', replay);
  replay();
})();
'''


def main():
    raw = (HERE / 'source.html').read_text(encoding='utf-8')
    match = re.search(r'<body[^>]*>(.*)</body>', raw, re.S)
    if not match:
        raise ValueError('source.html has no <body>')
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', match.group(1), flags=re.S | re.I)
    body, _ = inline_images(body)
    body = re.sub(r'\b(?:href|src)="(?:/static/|/_static/)[^"]*"', 'href="#"', body)

    strip = ('<div class="pv-strip"><span class="pv-strip__spin" aria-hidden="true"></span>'
             'Loading…</div>')
    skel_list = '<div class="pv-skel">' + ''.join(
        '<div class="pv-skel__row"><span class="pv-skel__dot"></span>'
        '<span class="pv-skel__bar"></span></div>' for _ in range(8)) + '</div>'
    skel_lines = '<div class="pv-skel">' + ''.join(
        '<div class="pv-skel__line"></div>' for _ in range(6)) + '</div>'
    place = '<div class="pv-place">' + ''.join(
        '<div class="pv-place__row"><span class="pv-place__caret"></span>'
        '<span class="pv-place__bar"></span></div>' for _ in range(4)) + '</div>'

    body = body.replace('<div class="panel__body" id="panelBody" tabindex="0">',
                        '<div class="panel__body" id="panelBody" tabindex="0">'
                        + strip + skel_list + place, 1)
    body = body.replace('<div class="ch__body" id="chBody" tabindex="0">',
                        '<div class="ch__body" id="chBody" tabindex="0">'
                        + strip + skel_list + place, 1)
    body = body.replace('<div class="read__body" id="readBody">',
                        '<div class="read__body" id="readBody">' + skel_lines, 1)
    body = body.replace('<main class="stage">',
                        '<main class="stage"><div class="pv-strip pv-strip--stage">'
                        '<span class="pv-strip__spin" aria-hidden="true"></span>'
                        'Loading…</div>', 1)

    css, _ = catalogue_css(['tokens.css', 'components.css', 'generate.css'])
    doc = f'''<!doctype html>
<html lang="en" data-theme="dark" data-theme-mode="dark" data-nav="open"
      data-ch="closed" data-read="on" data-home="reading"
      data-section="alkitab" data-bible-edition="tb" data-ch-mode="chapter"
      data-treatment="quiet" data-scenario="first">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spec 243 — loading treatments, researched options</title>
<style>{css}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="pv-bar" role="toolbar" aria-label="Loading treatments">
  <div class="pv-row">
    <span class="pv-row__label">Treatment</span>
    <button type="button" data-treatment="quiet" aria-pressed="true">A · Quiet strip</button>
    <button type="button" data-treatment="skeleton" aria-pressed="false">B · Skeleton</button>
    <button type="button" data-treatment="placeholder" aria-pressed="false">C · Placeholder rows</button>
    <span class="pv-row__hint" id="pvHint"></span>
  </div>
  <div class="pv-row">
    <span class="pv-row__label">Clicked from</span>
    <button type="button" data-scenario="rail" aria-pressed="false">Rail</button>
    <button type="button" data-scenario="first" aria-pressed="true">First-level row</button>
    <button type="button" data-scenario="second" aria-pressed="false">Second-level row</button>
    <button type="button" id="pvReplay">Replay</button>
    <span class="pv-row__hint">300 ms delay · 2.4 s settle · no global bar, no row recolor</span>
  </div>
</div>
<div class="pv-app">
{body}
</div>
<div class="pv-sr" id="pvLive" role="status" aria-live="polite"></div>
<script>
{JS}
</script>
</body>
</html>
'''
    (HERE / 'index.html').write_text(doc, encoding='utf-8')
    print(f'wrote {HERE / "index.html"} ({len(doc)} bytes)')


if __name__ == '__main__':
    main()
