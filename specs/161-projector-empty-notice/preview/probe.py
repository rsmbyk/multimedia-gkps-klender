#!/usr/bin/env python3
"""Measure and photograph the preview's four boards.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/161-projector-empty-notice/preview/probe.py

Writes `shots/boards.png` and prints the numbers `## UI/UX` quotes. The page fits each detour
board with `projector.js`'s own function and reports its own boxes on the 1920×1080 stage; this
script only drives it. Compare the printout against the live page's reading in the spec.
"""
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / "shots"


def main():
    SHOTS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1860, "height": 1220})
        page.goto((HERE / "preview.html").as_uri())
        page.wait_for_function("!!window.__preview")
        page.wait_for_timeout(400)
        boards = page.evaluate("() => window.__preview.measure()")
        page.locator(".boards").screenshot(path=str(SHOTS / "boards.png"))
        print(f"{'board':22} {'notice display':15} {'hidden':7} {'notice box':44} "
              f"{'stage':30} {'lines font':10} lines box")
        for board in boards:
            def box(value):
                if not value or not value.get("w"):
                    return "— (no box)"
                return (f"{value['w']}×{value['h']} at x {value['x']}–{value['x'] + value['w']}, "
                        f"y {value['y']}–{value['y'] + value['h']}")
            stage = f"{board['stage']['w']}×{board['stage']['h']}"
            name = f"{board['state']} · {board['column']}"
            print(f"{name:22} {board['noticeDisplay']:15} {str(board['noticeHidden']):7} "
                  f"{box(board['notice']):44} {stage:30} {str(board['fontSize']):10} "
                  f"{box(board['lines'])}")
        browser.close()


if __name__ == "__main__":
    main()
