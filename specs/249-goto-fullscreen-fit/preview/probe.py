"""Before/after evidence for spec 249: a Go To detour must follow a stage resize.

The base is the merged 247 build, whose resize path fits only the service screen;
the slice adds the detour to that path. Both use a real CDP viewport change, which
is the geometry signal F11 and an OS fullscreen transition deliver.
"""
import argparse
import json
from playwright.sync_api import sync_playwright

MEASURE = """() => {
  const detour = document.querySelector('.projector-detour');
  const lines = detour && detour.querySelector('.screen__lines');
  const stage = document.getElementById('projectorScreens');
  return {
    active: Boolean(detour && detour.classList.contains('is-active')),
    font: lines ? parseFloat(getComputedStyle(lines).fontSize) : null,
    key: detour && detour.dataset.fitted,
    stage: [stage.clientWidth, stage.clientHeight],
    inner: [innerWidth, innerHeight]
  };
}"""


def run(url, signal_first):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_function(
            "() => window.GKPSProjectorLibrary && GKPSProjectorLibrary.ready()", timeout=25000)
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('Kis 1')
        page.wait_for_timeout(500)
        page.keyboard.press('Enter')
        page.wait_for_function(
            "() => document.querySelector('.projector-detour').classList.contains('is-active')")
        page.wait_for_timeout(500)
        before = page.evaluate(MEASURE)
        if signal_first:
            page.evaluate("() => document.dispatchEvent(new Event('fullscreenchange'))")
            page.wait_for_timeout(80)
        cdp = ctx.new_cdp_session(page)
        cdp.send("Emulation.setDeviceMetricsOverride",
                 {"width": 1920, "height": 1080, "deviceScaleFactor": 1, "mobile": False})
        page.wait_for_timeout(500)
        grown = page.evaluate(MEASURE)
        cdp.send("Emulation.setDeviceMetricsOverride",
                 {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})
        page.wait_for_timeout(500)
        back = page.evaluate(MEASURE)
        browser.close()
        return before, grown, back


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--slice", required=True)
    args = ap.parse_args()
    for signal_first in (False, True):
        label = "fs-then-resize" if signal_first else "resize-only"
        for name, url in [("base", args.base), ("slice", args.slice)]:
            readings = run(url, signal_first)
            print(label, name, json.dumps({"before": readings[0], "grown": readings[1],
                                           "back": readings[2]}))


if __name__ == "__main__":
    main()
