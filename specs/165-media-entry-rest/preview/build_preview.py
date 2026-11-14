"""Build the static comparison preview for spec 165 from the live dock's own markup.

The runner block (`#viewRun`) is copied verbatim from the running product (service 149,
`/obs/dock`, screen 2 — the first media entry is the live one), so both columns are the
real screen with the change and without it. The Proposed column only appends the one
row the slice adds to each media entry's inner body. Stylesheets are frozen at the
slice's base commit so the "Now" column cannot drift into the "Proposed" one.
"""
import re
import subprocess

BASE_SHA = '59182b12'
ROOT = '/home/rsmbyk/Projects/multimedia-gkps-klender-164-rest'
OUT = f'{ROOT}/specs/165-media-entry-rest/preview'

STYLE = """
  /* ---- the comparison page's own frame (never the product's) ---- */
  html, body { margin: 0; }
  body {
    background: var(--canvas);
    color: var(--ink);
    font: 400 14.5px/1.5 var(--font-sans);
    padding: 28px 26px 40px;
  }
  header { max-width: 1120px; margin: 0 0 22px; }
  h1 { margin: 0 0 6px; font: 600 19px/1.3 var(--font-sans); color: var(--ink); }
  .lede { margin: 0; color: var(--head-ink); max-width: 78ch; }
  .lede b { color: var(--ink); font-weight: 600; }
  .cols { display: flex; gap: 26px; align-items: flex-start; flex-wrap: wrap; }
  .col { width: 420px; }
  .col h2 {
    margin: 0 0 2px; font: 650 10px/1 var(--font-sans); letter-spacing: .09em;
    text-transform: uppercase; color: var(--head-ink);
  }
  .col .tag { margin: 0 0 10px; min-height: 39px; font: 400 13px/1.5 var(--font-sans); color: var(--head-ink); }
  .panel {
    height: 620px; overflow: hidden; outline: 1px solid var(--divider);
    border-radius: 12px; background: var(--rail-bg);
  }
  .panel .dock { height: 100%; max-width: none; }
  .note {
    margin: 10px 0 0; font: 400 12.5px/1.6 var(--font-sans); color: var(--head-ink);
  }
  .note b { color: var(--ink); font-weight: 600; }
  .tools { margin: 0 0 16px; }
  .tools button {
    font: 600 12.5px/1 var(--font-sans); padding: 7px 11px; border-radius: 8px;
    border: 1px solid var(--divider); background: var(--card, transparent); color: var(--ink);
    cursor: pointer;
  }
"""


def frozen(path, dest):
    text = subprocess.run(['git', 'show', f'{BASE_SHA}:{path}'], cwd=ROOT,
                          check=True, capture_output=True, text=True).stdout
    open(f'{OUT}/{dest}', 'w').write(text)


def with_rest(html):
    """Append the slice's Rest row to every media entry's inner body."""
    def add(match):
        body = match.group(0)
        if 'screenerow--media' not in body:
            return body
        return body[:-len('</div>')] + (
            '<button type="button" tabindex="-1" data-screen="rest" aria-current="false"'
            ' class="screenerow screenerow--rest">Rest</button></div>')
    return re.sub(r'<div class="entryinner__body">.*?</div>', add, html, flags=re.S)


run = open(f'{ROOT}/scratch/viewrun-149.html').read()
proposed = with_rest(run)

page = f"""<!doctype html>
<html lang="id" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spec 164 — a rest after a media entry</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="obs-dock.css">
<style>{STYLE}</style>
</head>
<body>
<header>
  <h1>A media entry's inner list, before and after the slice</h1>
  <p class="lede">The operator dock at <b>/obs/dock</b>, service <b>149</b>, screen <b>2</b> — the first
  image is on screen, so its entry is the open one. The left column is the product as it ships on
  <b>{BASE_SHA}</b>; the right column is the same markup with the slice's one row added to each media
  entry. Every other row is copied from the live page.</p>
</header>
<p class="tools"><button type="button" id="theme">Switch theme</button></p>
<main class="cols">
  <section class="col">
    <h2>Now — shipped</h2>
    <p class="tag">A media entry shows its file and nothing after it.</p>
    <div class="panel">{run}</div>
    <p class="note">Service 149 builds <b>6 screens</b>: text, rest, then four images with no rest
    between them. Its last screen is the fourth image, so the display has no blank to go back to at
    the end of the service.</p>
  </section>
  <section class="col">
    <h2>Proposed — spec 165</h2>
    <p class="tag">Every media entry ends on a rest, as text, passage and song rows already do.</p>
    <div class="panel">{proposed}</div>
    <p class="note">The same service builds <b>10 screens</b>: text, rest, then image-rest four times.
    Each media entry gains exactly one row — <b>28.8px</b> tall, 3px under the media row — and the
    service ends on a rest.</p>
  </section>
</main>
<script>
  document.getElementById('theme').addEventListener('click', function () {{
    var root = document.documentElement;
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  }});
</script>
</body>
</html>
"""

open(f'{OUT}/preview.html', 'w').write(page)
frozen('static/styles/design/tokens.css', 'tokens.css')
frozen('static/styles/design/obs-dock.css', 'obs-dock.css')
print('wrote', OUT, 'rest rows:', proposed.count('screenerow--rest') - run.count('screenerow--rest'))
