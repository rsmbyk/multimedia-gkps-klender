"""Build the static comparison preview from the live slice page.

Run: <repo>/.venv/bin/python specs/223-*/preview/build_preview.py
The page is the live page's real markup and stylesheets with scripts removed; the only
additions are the candidate switcher and the focus button at the bottom of this file.
"""
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
URL = "http://127.0.0.1:8767/songs/1820/"

ADDITION = r"""
<style id="candidate"></style>
<style id="previewUi">
  #ringPreviewBar { position: fixed; z-index: 99999; right: 12px; top: 12px; width: 330px;
    padding: 12px; border: 1px solid #7778; border-radius: 10px; background: #1b1b19ee;
    color: #f5f3ee; font: 13px/1.4 system-ui, sans-serif; }
  #ringPreviewBar h2 { margin: 0 0 8px; font: 600 14px/1.3 system-ui, sans-serif; }
  #ringPreviewBar button { margin: 0 4px 4px 0; padding: 5px 9px; border: 1px solid #7c9cf0;
    border-radius: 6px; background: transparent; color: #f5f3ee; cursor: pointer; }
  #ringPreviewBar button[aria-pressed="true"] { background: #7c9cf0; color: #111; }
  #ringPreviewBar p { margin: 8px 0 0; color: #c9c9c4; }
  #ringPreviewBar code { color: #9fc0ff; }
</style>
<div id="ringPreviewBar">
  <h2>Song-row focus ring at the list top</h2>
  <button type="button" data-candidate="current" aria-pressed="true">Current</button>
  <button type="button" data-candidate="a" aria-pressed="false">A · 3px space</button>
  <button type="button" data-candidate="b" aria-pressed="false">B · inset ring</button>
  <button type="button" id="ringFocusTop">Focus top row</button>
  <p id="ringPreviewNote">Pick a candidate, click <b>Focus top row</b>, then press any key —
  the browser paints its focus ring only once it sees the keyboard.</p>
</div>
<script>
(function () {
  var style = document.getElementById('candidate');
  var note = document.getElementById('ringPreviewNote');
  var buttons = document.querySelectorAll('#ringPreviewBar button[data-candidate]');
  var css = {
    current: '#chBody { padding-top: 0 !important; }',
    a: '#chBody { padding-top: 3px !important; }',
    b: '.songrow:focus-visible { outline: 2px solid var(--focus) !important; outline-offset: -2px !important; }'
  };
  var text = {
    current: 'Current: the ring needs 2px above the row, and #chBody has 0px — its top edge is clipped.',
    a: 'A: 3px of top space in the scrollport; row and all other styles unchanged, ring fully drawn.',
    b: 'B: a 2px --focus ring drawn inside the row; no geometry moves and no edge can clip it.'
  };
  function set(name) {
    style.textContent = css[name];
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.candidate === name)); });
    note.textContent = text[name] + ' Click Focus top row, then press any key.';
  }
  buttons.forEach(function (b) { b.addEventListener('click', function () { set(b.dataset.candidate); }); });
  var focusBtn = document.getElementById('ringFocusTop');
  focusBtn.addEventListener('pointerdown', function (e) { e.preventDefault(); });
  focusBtn.addEventListener('click', function (e) {
    e.preventDefault();
    var row = document.querySelector('#chList li > .songrow');
    if (row) row.focus({ preventScroll: true });
    note.textContent += ' Focus is on the top row — press a key now.';
  });
})();
</script>
"""


def main():
    (HERE / "assets").mkdir(exist_ok=True)
    for source, target in (("styles", "styles"), ("assets", "assets")):
        dst = HERE / "assets" / target
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(REPO / "static" / source, dst)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, color_scheme="dark")
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(400)
        html = page.evaluate("""() => {
          document.querySelectorAll('script').forEach(function (s) { s.remove(); });
          return document.documentElement.outerHTML;
        }""")
        browser.close()
    html = html.replace('href="/static/', 'href="assets/')
    html = html.replace('src="/static/', 'src="assets/')
    html = html.replace("url(/static/", "url(assets/")
    html = html.replace("</body>", ADDITION + "\n</body>")
    (HERE / "index.html").write_text(html, encoding="utf-8")
    print(f"wrote {HERE / 'index.html'} ({len(html)} chars), assets copied")


if __name__ == "__main__":
    main()
