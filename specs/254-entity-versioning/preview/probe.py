"""Measure the 254 deletion-notice preview with the repo's own Playwright."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PAGE = HERE / "index.html"
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)


def measure(page, state):
    page.eval_on_selector(f'.preview-bar button[data-show="{state}"]', 'el => el.click()')
    page.wait_for_timeout(60)
    return page.evaluate("""() => {
      const open = document.querySelector('dialog[open]');
      const actions = open.querySelector('.editor__actions');
      const note = open.querySelector('.editor__refnote');
      const del = open.querySelector('.editor__danger');
      const bar = document.querySelector('.preview-bar').getBoundingClientRect();
      const box = open.getBoundingClientRect();
      const rect = el => { const r = el.getBoundingClientRect(); return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; };
      return {
        toolbar: {w: Math.round(bar.width), h: Math.round(bar.height)},
        dialog: rect(open),
        actionOrder: Array.from(actions.children).map(el => el.className),
        note: note ? {text: note.innerText.replace(/\\s+/g, ' ').trim(), font: getComputedStyle(note).font, color: getComputedStyle(note).color, box: rect(note), describedBy: del.getAttribute('aria-describedby')} : null,
        danger: {text: del.innerText.trim(), disabled: del.disabled, box: rect(del), opacity: getComputedStyle(del).opacity}
      };
    }""")


report = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(PAGE.as_uri())
        page.evaluate("document.fonts.ready")
        page.evaluate("theme => document.documentElement.setAttribute('data-theme', theme)", theme)
        page.wait_for_timeout(100)
        report[theme] = {state: measure(page, state) for state in ("song", "songbook", "verse", "clear")}
        page.eval_on_selector('.preview-bar button[data-show="song"]', 'el => el.click()')
        page.screenshot(path=str(OUT / f"song-{theme}.png"), full_page=False)
        page.eval_on_selector('.preview-bar button[data-show="clear"]', 'el => el.click()')
        page.screenshot(path=str(OUT / f"clear-{theme}.png"), full_page=False)
        page.close()
    browser.close()

(OUT / "probe.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
