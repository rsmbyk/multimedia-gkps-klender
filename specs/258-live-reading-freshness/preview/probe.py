"""Measure the 258 freshness preview with the repo's Playwright."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PAGE = HERE / "index.html"
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)


def set_state(page, state):
    page.eval_on_selector(f'.preview-bar button[data-state="{state}"]', 'el => el.click()')
    page.wait_for_timeout(40)


def measure(page, state):
    set_state(page, state)
    return page.evaluate("""(state) => {
      const b = el => { const r = el.getBoundingClientRect();
        return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; };
      const badge = document.getElementById('badge');
      const add = document.querySelector('.entry__add-btn');
      const row = document.getElementById('newRow');
      return {
        state: state,
        stage: {invalid: document.getElementById('stage').dataset.invalid},
        badge: badge.hidden ? null : {text: badge.innerText.replace(/\\s+/g, ' ').trim(), box: b(badge),
          button: b(badge.querySelector('button'))},
        add: {box: b(add), opacity: getComputedStyle(add).opacity, cursor: getComputedStyle(add).cursor},
        row: row.hidden ? null : {box: b(row), animation: getComputedStyle(row).animationDuration,
          timing: getComputedStyle(row).animationTimingFunction}
      };
    }""", state)


def motion(page):
    set_state(page, 'sidebar')
    return page.evaluate("""() => new Promise(resolve => {
      const el = document.getElementById('newRow');
      el.classList.remove('row-enter'); void el.offsetWidth; el.classList.add('row-enter');
      const samples = [];
      const t0 = performance.now();
      function tick() {
        const t = performance.now() - t0;
        samples.push({t: Math.round(t), opacity: +getComputedStyle(el).opacity,
                      transform: getComputedStyle(el).transform});
        if (t < 240) requestAnimationFrame(tick); else resolve(samples);
      }
      requestAnimationFrame(tick);
    })""")


report = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.goto(PAGE.as_uri())
        page.evaluate("document.fonts.ready")
        page.evaluate("theme => document.documentElement.setAttribute('data-theme', theme)", theme)
        page.wait_for_timeout(80)
        report[theme] = {state: measure(page, state) for state in ("current", "invalid", "sidebar")}
        report[theme]["motion"] = motion(page)
        set_state(page, "invalid")
        page.screenshot(path=str(OUT / f"invalid-{theme}.png"), full_page=False)
        set_state(page, "sidebar")
        page.screenshot(path=str(OUT / f"sidebar-{theme}.png"), full_page=False)
        page.close()
    browser.close()

(OUT / "probe.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
