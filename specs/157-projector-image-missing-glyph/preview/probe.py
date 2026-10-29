#!/usr/bin/env python3
"""Measure and photograph the two boards at each state.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/157-projector-image-missing-glyph/preview/probe.py

Writes `shots/<state>.png` (board area only) and prints the numbers the spec's `## UI/UX`
quotes. The page reports its own boxes on the 1920×1200 stage — this script only drives it.
"""
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / "shots"
STATES = ("loaded", "failed", "pending")


def main():
    SHOTS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1900, "height": 1100})
        page.goto((HERE / "preview.html").as_uri())
        page.wait_for_timeout(150)
        for state in STATES:
            m = page.evaluate("(state) => window.__preview.apply(state)", state)
            page.wait_for_timeout(120)
            page.locator(".boards").screenshot(path=str(SHOTS / f"{state}.png"))
            print(f"\n== {state}")
            report(m)
        # The same two boards at a 1280×720 stage: nothing here is size-dependent, so the
        # offset should be the same 40px and disappear the same way.
        for stage in (("1920x1200", 1920, 1200), ("1280x720", 1280, 720)):
            print(f"\n== stage {stage[0]} — loaded")
            m = page.evaluate(
                """([w, h]) => {
                    document.querySelectorAll('.board__stage').forEach(function (board) {
                        board.style.width = w + 'px'; board.style.height = h + 'px';
                    });
                    return window.__preview.apply('loaded');
                }""",
                [stage[1], stage[2]],
            )
            report(m)
        browser.close()


def report(m):
    for name, board in zip(("today", "slice"), m):
        glyph = (f"{board['glyph']['w']}×{board['glyph']['h']}@x{board['glyph']['x']}"
                 if board['glyph']['w'] else "— (no box)")
        image = (f"{board['image']['w']}×{board['image']['h']}@x{board['image']['x']}"
                 f" centre={board['imageCentre']} offset={board['offset']:+}px"
                 if board['image']['w'] else "nothing painted")
        print(f"  {name:6} glyph display={board['glyphDisplay']:5} "
              f"hidden-attr={str(board['glyphHiddenAttr']):5} glyph={glyph:22} image={image}")


if __name__ == "__main__":
    main()
