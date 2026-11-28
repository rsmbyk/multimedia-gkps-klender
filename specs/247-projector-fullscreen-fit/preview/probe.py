"""Before/after evidence for spec 247.

Models a fullscreen transition that changes the projector stage without a window
`resize` event: the stage box is enlarged, then `fullscreenchange` is dispatched.
On unfixed code the fitted font size stays at the old stage's size.
"""
import argparse
import json
from playwright.sync_api import sync_playwright

MEASURE = """() => {
  const active = document.querySelector('.screen.is-active') ||
    document.querySelector('[data-screen="' + (document.body.dataset.currentScreen || 0) + '"]');
  const lines = active && active.querySelector('.screen__lines');
  const head = active && active.querySelector('.screen__head');
  const stage = document.getElementById('projectorScreens');
  return {
    stage: [stage.clientWidth, stage.clientHeight],
    font: lines ? parseFloat(getComputedStyle(lines).fontSize) : null,
    headFont: head ? parseFloat(getComputedStyle(head).fontSize) : null,
    fitted: active && active.dataset.fitted,
    text: lines ? lines.innerText.slice(0, 48) : null
  };
}"""

CHANGE = """() => {
  document.querySelector('.projector__screen').style.setProperty('height', '1100px', 'important');
  document.dispatchEvent(new Event('fullscreenchange'));
  matchMedia('(display-mode: fullscreen)').dispatchEvent(new Event('change'));
}"""

RESTORE = """() => {
  document.querySelector('.projector__screen').style.removeProperty('height');
  document.dispatchEvent(new Event('fullscreenchange'));
  matchMedia('(display-mode: fullscreen)').dispatchEvent(new Event('change'));
}"""


def run(url, viewport):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport=viewport, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(url, wait_until="load")
        page.evaluate("() => document.fonts.ready")
        page.wait_for_timeout(500)
        before = page.evaluate(MEASURE)
        page.evaluate(CHANGE)
        page.wait_for_timeout(200)
        after = page.evaluate(MEASURE)
        page.evaluate(RESTORE)
        page.wait_for_timeout(200)
        restored = page.evaluate(MEASURE)
        browser.close()
        return before, after, restored


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--slice", required=True)
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    args = ap.parse_args()
    viewport = {"width": args.width, "height": args.height}
    for name, url in [("base", args.base), ("slice", args.slice)]:
        before, after, restored = run(url, viewport)
        print(name, json.dumps({"before": before, "after": after, "restored": restored}))


if __name__ == "__main__":
    main()
