#!/usr/bin/env python3
"""Assemble spec 243's static preview from the real reading shell.

Reads source.html (a fetch of /bible/1/1/ from the local dev server), inlines
the project's own stylesheets and image assets, and writes a self-contained
index.html that works in the chat preview's opaque-origin frame.
"""
import base64
import mimetypes
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def asset_uri(url):
    path = url.split('?', 1)[0]
    if not path.startswith(('/static/', '/_static/')):
        return None
    rel = path.lstrip('/').replace('_static/', 'static/', 1)
    candidates = [ROOT / rel]
    # Manifest-stamped names: assets/gkps.<hash>.png -> assets/gkps.png
    candidates.append(ROOT / re.sub(r'\.([0-9a-zA-Z_-]{8,})(\.[a-z0-9]+)$', r'\2', rel))
    for candidate in candidates:
        if candidate.is_file():
            mime = mimetypes.guess_type(candidate.name)[0] or 'application/octet-stream'
            return f'data:{mime};base64,' + base64.b64encode(candidate.read_bytes()).decode()
    return None


def inline_images(markup):
    made = []

    def replace(match):
        tag = match.group(0)
        src = re.search(r'\bsrc="([^"]+)"', tag)
        uri = asset_uri(src.group(1)) if src else None
        width = re.search(r'\bwidth="(\d+)"', tag)
        height = re.search(r'\bheight="(\d+)"', tag)
        alt = re.search(r'\balt="([^"]*)"', tag)
        cls = re.search(r'\bclass="([^"]*)"', tag)
        if not uri:
            return ''
        made.append(uri)
        style = (f'width:{width.group(1) if width else 32}px;'
                 f'height:{height.group(1) if height else 32}px;'
                 f'background-image:url({uri})')
        return (f'<span class="pv-asset {cls.group(1) if cls else ""}" '
                f'style="{style}" role="img" aria-label="{alt.group(1) if alt else ""}"></span>')

    return re.sub(r'<img\b[^>]*>', replace, markup, flags=re.I), made


def catalogue_css(paths):
    chunks, extra_css = [], []
    for name in paths:
        css = (ROOT / 'static/styles/design' / name).read_text(encoding='utf-8')

        def url_replace(match):
            uri = asset_uri(match.group(1).strip('"\''))
            return f'url("{uri}")' if uri else match.group(0)

        css = re.sub(r'url\(([^)]+)\)', url_replace, css)
        chunks.append('/* ' + name + ' */\n' + css)
    return '\n'.join(chunks), extra_css


PREVIEW_CSS = r'''
/* ---- Preview chrome: the four candidate loading signs -------------------- */
:root { --pv-top: 44px; }
body { padding-top: var(--pv-top); }
.pv-bar {
  position: fixed; inset: 0 0 auto 0; height: var(--pv-top); z-index: 9000;
  display: flex; align-items: center; gap: 8px; padding: 0 12px;
  background: var(--rail-bg); border-bottom: 1px solid var(--divider);
  color: var(--ink); font: 12px/1.35 ui-sans-serif, system-ui, sans-serif;
}
.pv-bar__title { font-weight: 650; margin-right: 6px; white-space: nowrap; }
.pv-bar__hint { margin-left: auto; opacity: .72; white-space: nowrap; }
.pv-bar button {
  border: 1px solid var(--divider); border-radius: 6px; padding: 5px 9px;
  background: transparent; color: inherit; font: inherit; cursor: pointer;
}
.pv-bar button:hover { background: var(--icon-hover-bg); }
.pv-bar button[aria-pressed="true"] { background: var(--active-bg); color: var(--active-ink); border-color: transparent; }
.pv-bar button:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.pv-asset { display: inline-block; background-size: contain; background-repeat: no-repeat; background-position: center; }
.rail, .panel, .chapters, .topbar { top: var(--pv-top) !important; }

/* A: one thin bar at the window top, plus a quiet mark on the clicked row. */
.pv-progress {
  position: fixed; top: 0; left: 0; right: 0; height: 3px; z-index: 9500;
  overflow: hidden; background: color-mix(in srgb, var(--active-bg) 22%, transparent);
}
.pv-progress::before {
  content: ""; position: absolute; top: 0; bottom: 0; width: 28%;
  background: var(--active-bg); animation: pv-slide 1.05s var(--ease-timing) infinite;
}
@keyframes pv-slide { from { transform: translateX(-100%); } to { transform: translateX(460%); } }
html[data-pv="a"].pv-loading .pv-row-target { box-shadow: inset 3px 0 var(--active-bg); }
html[data-pv="a"].pv-loading .pv-row-target .book__n { opacity: .58; }

/* B: a spinner on the clicked row only. */
html[data-pv="b"] .pv-row-target { position: relative; }
.pv-row-spin {
  display: none;
  position: absolute; right: 10px; top: 50%; width: 12px; height: 12px;
  margin-top: -6px; border: 2px solid var(--divider);
  border-top-color: var(--active-bg); border-radius: 50%;
  animation: pv-spin .72s linear infinite;
}
html[data-pv="b"].pv-loading .pv-row-spin { display: block; }
@keyframes pv-spin { to { transform: rotate(360deg); } }

/* C: the reading stage itself is visibly busy. */
.stage { position: relative !important; }
.pv-veil {
  position: absolute; inset: 0; z-index: 6; display: flex; gap: 10px;
  align-items: center; justify-content: center;
  background: color-mix(in srgb, var(--canvas) 76%, transparent);
  color: var(--ink); font: 13px/1.4 ui-sans-serif, system-ui, sans-serif;
}
.pv-veil__spin {
  width: 18px; height: 18px; border: 2px solid var(--divider);
  border-top-color: var(--active-bg); border-radius: 50%;
  animation: pv-spin .72s linear infinite;
}

/* D: the edit-feedback toast's pending shape, reused for navigation. */
.pv-toast {
  position: fixed; right: 20px; bottom: 20px; z-index: 9200;
  width: min(360px, calc(100vw - 24px)); min-height: 56px;
  display: flex; align-items: center; gap: 11px; padding: 13px 14px;
  border: 1px solid var(--divider); border-left: 3px solid #C4922E;
  border-radius: 10px; background: var(--rail-bg); color: var(--ink);
  box-shadow: 0 1px 2px rgba(0,0,0,.09);
  font: 14px/1.35 ui-sans-serif, system-ui, sans-serif;
}
.pv-toast__spin {
  flex: none; width: 18px; height: 18px; border: 2px solid var(--divider);
  border-top-color: #C4922E; border-radius: 50%;
  animation: pv-spin .8s linear infinite;
}
.pv-toast b { display: block; font-size: 14px; font-weight: 600; }
.pv-toast span { display: block; margin-top: 2px; font-size: 12.5px; opacity: .7; }
@media (max-width: 740px) { .pv-toast { right: 12px; bottom: 12px; } }
@media (prefers-reduced-motion: reduce) {
  .pv-progress::before, .pv-row-spin, .pv-veil__spin, .pv-toast__spin { animation: none; }
}
.pv-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.pv-progress[hidden], .pv-veil[hidden], .pv-toast[hidden] { display: none !important; }
'''


def main():
    raw = (HERE / 'source.html').read_text(encoding='utf-8')
    body_match = re.search(r'<body[^>]*>(.*)</body>', raw, re.S)
    if not body_match:
        raise ValueError('source.html has no <body>')
    body = body_match.group(1)
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', body, flags=re.S | re.I)
    body, images = inline_images(body)
    body = re.sub(r'\b(?:href|src)="(?:/static/|/_static/)[^"]*"', 'href="#"', body)

    # Mark one sidebar row as the row the operator just clicked: Keluaran,
    # or the first book row when that edition has no Keluaran entry.
    rows = list(re.finditer(r'<a class="book"[^>]*>', body))
    if rows:
        chosen = next((r for r in rows if 'data-name="Keluaran"' in r.group(0)), rows[0])
        tag = chosen.group(0)
        tag = tag.replace('class="book"', 'class="book pv-row-target"', 1)
        body = body[:chosen.start()] + tag + body[chosen.end():]
        close = body.find('</a>', chosen.end())
        if close != -1:
            body = (body[:close] + '<span class="pv-row-spin" aria-hidden="true"></span>'
                    + body[close:])

    css, _ = catalogue_css(['tokens.css', 'components.css', 'generate.css'])
    css = css.replace('data-theme="light"', 'data-theme="dark"')

    # The stage overlay belongs inside the stage: at narrow widths the sidebar
    # is a drawer above it and must stay bright and clickable.
    body = body.replace('<main class="stage">',
                        '<main class="stage">\n<div class="pv-veil" id="pvVeil" hidden>'
                        '<span class="pv-veil__spin"></span>Loading…</div>', 1)

    doc = f'''<!doctype html>
<html lang="en" data-theme="dark" data-theme-mode="dark" data-nav="open"
      data-ch="closed" data-read="on" data-home="reading"
      data-section="alkitab" data-bible-edition="tb" data-ch-mode="chapter"
      data-pv="a">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spec 243 — loading signs, four candidates</title>
<style>{css}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="pv-bar" role="toolbar" aria-label="Loading sign options">
  <span class="pv-bar__title">Loading sign</span>
  <button type="button" data-pv="a" aria-pressed="true">A · Top bar + row</button>
  <button type="button" data-pv="b" aria-pressed="false">B · Row spinner</button>
  <button type="button" data-pv="c" aria-pressed="false">C · Stage overlay</button>
  <button type="button" data-pv="d" aria-pressed="false">D · Edit toast</button>
  <button type="button" id="pvReplay">Replay slow fetch</button>
  <span class="pv-bar__hint">180 ms delay · 2.4 s fetch · dark theme</span>
</div>
<div id="pvProgress" class="pv-progress" role="progressbar" aria-label="Loading page" hidden></div>
<div class="pv-app">
{body}
</div>
<div class="pv-toast" id="pvToast" hidden>
  <span class="pv-toast__spin" aria-hidden="true"></span>
  <span><b>Opening page…</b><span>Fetching from the church computer</span></span>
</div>
<div class="pv-sr" id="pvLive" role="status" aria-live="polite"></div>
<script>
(function () {{
  var root = document.documentElement;
  var progress = document.getElementById('pvProgress');
  var veil = document.getElementById('pvVeil');
  var toast = document.getElementById('pvToast');
  var live = document.getElementById('pvLive');
  var buttons = [...document.querySelectorAll('.pv-bar button[data-pv]')];
  var showTimer = null, settleTimer = null;
  function paint() {{
    progress.hidden = root.dataset.pv !== 'a';
    veil.hidden = root.dataset.pv !== 'c';
    toast.hidden = root.dataset.pv !== 'd';
    live.textContent = 'Loading page';
  }}
  function settle() {{
    clearTimeout(showTimer); clearTimeout(settleTimer);
    root.classList.remove('pv-loading');
    progress.hidden = veil.hidden = toast.hidden = true;
    live.textContent = 'Page opened';
  }}
  function replay() {{
    clearTimeout(showTimer); clearTimeout(settleTimer);
    root.classList.remove('pv-loading');
    progress.hidden = veil.hidden = toast.hidden = true;
    root.classList.add('pv-loading');
    showTimer = setTimeout(paint, 180);
    settleTimer = setTimeout(settle, 2400);
  }}
  buttons.forEach(function (button) {{
    button.addEventListener('click', function () {{
      buttons.forEach(function (b) {{ b.setAttribute('aria-pressed', String(b === button)); }});
      root.dataset.pv = button.dataset.pv;
      if (root.classList.contains('pv-loading')) {{
        clearTimeout(showTimer);
        if (root.dataset.pv === 'a') showTimer = setTimeout(paint, 0);
        else paint();
      }}
    }});
  }});
  document.getElementById('pvReplay').addEventListener('click', replay);
  document.addEventListener('click', function (event) {{
    if (event.target.closest('.pv-bar')) return;
    if (event.target.closest('.book, .ch-num, .songrow')) {{
      event.preventDefault(); replay();
    }}
  }});
  replay();
}})();
</script>
</body>
</html>
'''
    (HERE / 'index.html').write_text(doc, encoding='utf-8')
    print(f'wrote {HERE / "index.html"} ({len(doc)} bytes, {len(images)} inlined images)')


if __name__ == '__main__':
    main()
