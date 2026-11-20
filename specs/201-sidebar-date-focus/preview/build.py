from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = "92edc752"

assets = HERE / "assets"
assets.mkdir(exist_ok=True)
for name in ("tokens.css", "components.css"):
    blob = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{BASE}:static/styles/design/{name}"],
        capture_output=True, check=True,
    ).stdout
    (assets / name).write_bytes(blob)

rows = (HERE / "rows.html").read_text().strip()

CANDIDATE = """
/* ---- Harness chrome (not part of the proposal) ---- */
body.pv { display: block; margin: 0; padding: 18px 22px 32px; background: var(--canvas);
          color: var(--ink); font: 14px/1.5 ui-sans-serif, system-ui, sans-serif; }
.pv h1 { font-size: 19px; margin: 0 0 4px; }
.pv .lead { margin: 0 0 16px; color: var(--head-ink); max-width: 900px; }
.pv .panels { display: flex; gap: 20px; align-items: flex-start; }
.pv .pvpanel { width: 400px; flex: none; border: 1px solid var(--divider); border-radius: 10px;
             padding: 12px 12px 16px; background: var(--canvas); }
.pv .pvpanel__label { font-weight: 700; margin-bottom: 2px; }
.pv .pvpanel__sub { color: var(--head-ink); font-size: 12px; margin-bottom: 10px; }
.pv .pvcontrols { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
.pv .pvcontrols button { padding: 5px 9px; border: 1px solid var(--divider); border-radius: 7px;
                       background: var(--rail-bg); color: var(--ink); cursor: pointer; font-size: 12px; }
.pv .pvcontrols button[aria-pressed="true"] { border-color: var(--active-bg); background: var(--active-bg); color: var(--active-ink); }
.pv .readout { margin-top: 12px; padding: 9px 11px; border-radius: 8px; background: var(--rail-bg);
               color: var(--ink); font: 12px/1.6 ui-monospace, monospace; white-space: pre-wrap; }
.pv .group ul { max-width: 100%; }
.pv .pin { outline: 1px dashed var(--focus); outline-offset: -2px; }
@media (max-width: 900px) {
  .pv .panels { flex-direction: column; }
  .pv .pvpanel { width: 100%; max-width: 420px; }
}

/* ---- Harness simulation: a static page cannot hold a pointer, so the Hover state
        is a class that carries the very same declarations as li:hover. ---- */
.pv .sim-hover .book__s, .pv .sim-hover .book__today { display: none; }
.pv .sim-hover > .row-edit, .pv .sim-hover > .row-delete { opacity: 1; pointer-events: auto; }

/* ---- Candidate A — TODAY (base 92edc752), unwrapped from @media (hover: hover)
        so a pointerless preview still shows the shipped behaviour. ---- */
.panel--before li[data-editor-kind]:focus-within .book__s,
.panel--before li[data-editor-kind]:focus-within .book__today { display: none; }

/* ---- Candidate B — PROPOSED (spec 201). The date and Today badge step aside only
        when the row's action controls are actually revealed: hover, or keyboard
        focus on the pencil/trash themselves. A click on the row's link is not a
        reveal, so the date stays painted. The first pair neutralises the base
        sheet's own :focus-within rule inside this panel so the candidate is the
        only rule under test; hover still hides as it does today. ---- */
.panel--after li[data-editor-kind]:focus-within:not(:hover) .book__s,
.panel--after li[data-editor-kind]:focus-within:not(:hover) .book__today { display: revert; }
.panel--after li[data-editor-kind]:has(> .row-edit:focus-visible, > .row-delete:focus-visible) .book__s,
.panel--after li[data-editor-kind]:has(> .row-edit:focus-visible, > .row-delete:focus-visible) .book__today { display: none; }
"""

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Spec 201 — a clicked service keeps its date</title>
<link rel="stylesheet" href="assets/tokens.css">
<link rel="stylesheet" href="assets/components.css">
<style>__CANDIDATE__</style>
</head>
<body class="pv">
<h1>Spec 201 — a clicked service keeps its date</h1>
<p class="lead">Both panels carry the first group captured from the running Tata Ibadah sidebar
(<code>#panelBody section.group</code>, base __BASE__), with the base commit's own
<code>tokens.css</code> and <code>components.css</code>. Only the two marked rule blocks differ.
Press <b>Click row (pointer away)</b>, then <b>Click elsewhere</b>: today the date disappears after
the click and only returns when focus leaves; the proposal keeps it painted.</p>
<div class="panels">
__PANELS__
</div>
<script>
function setState(which, state) {
  const panel = document.querySelector('.panel--' + which);
  panel.querySelectorAll('li').forEach(li => li.classList.remove('sim-hover'));
  panel.querySelectorAll('a,button').forEach(el => { if (document.activeElement === el) el.blur(); });
  const li = panel.querySelector('li[data-editor-kind]');
  if (state === 'hover') li.classList.add('sim-hover');
  if (state === 'clicked') li.querySelector('.book').focus();
  if (state === 'elsewhere') panel.querySelector('.harness-blur').focus();
  panel.querySelectorAll('.pvcontrols button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.state === state)));
  const s = li.querySelector('.book__s');
  const today = li.querySelector('.book__today');
  const edit = li.querySelector('.row-edit');
  panel.querySelector('.readout').textContent =
    'date display      : ' + getComputedStyle(s).display + '\\n' +
    'date text         : ' + JSON.stringify(s.textContent.trim()) + '\\n' +
    'badge display     : ' + (today ? getComputedStyle(today).display : 'no badge in this row') + '\\n' +
    'li :focus-within  : ' + li.matches(':focus-within') + '\\n' +
    'active element    : ' + (document.activeElement ? document.activeElement.className || document.activeElement.tagName : 'none') + '\\n' +
    'edit opacity      : ' + getComputedStyle(edit).opacity + '\\n' +
    'li height         : ' + li.getBoundingClientRect().height.toFixed(1) + 'px';
}
document.querySelectorAll('.pvpanel').forEach(panel => {
  const which = panel.classList.contains('panel--before') ? 'before' : 'after';
  panel.querySelectorAll('.pvcontrols button').forEach(b =>
    b.addEventListener('click', () => setState(which, b.dataset.state)));
  setState(which, 'rest');
});
</script>
</body>
</html>
"""

def panel(which, label, sub):
    buttons = "".join(
        f'<button type="button" data-state="{s}" aria-pressed="false">{t}</button>'
        for s, t in [("rest", "At rest"), ("hover", "Hover"),
                     ("clicked", "Click row (pointer away)"), ("elsewhere", "Click elsewhere")]
    )
    return f"""<section class="pvpanel panel--{which}">
  <div class="pvpanel__label">{label}</div>
  <div class="pvpanel__sub">{sub}</div>
  <div class="pvcontrols">{buttons}<button class="harness-blur" type="button" hidden>blur target</button></div>
  <section class="group">{rows}</section>
  <pre class="readout"></pre>
</section>"""

html = (HTML.replace("__CANDIDATE__", CANDIDATE)
           .replace("__BASE__", BASE)
           .replace("__PANELS__", panel("before", "TODAY — base commit", "li:focus-within hides the date: it sticks after the click")
                               + panel("after", "PROPOSAL — spec 201", "date hides only for hover or action-button :focus-visible")))
(HERE / "index.html").write_text(html)
print("wrote", HERE / "index.html", len(html), "bytes; assets:", [p.name for p in assets.iterdir()])
