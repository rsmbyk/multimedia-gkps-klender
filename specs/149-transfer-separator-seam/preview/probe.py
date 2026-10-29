#!/usr/bin/env python3
"""Measure the spec 149 preview in a real browser and write its screenshots.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/149-transfer-separator-seam/preview/probe.py

Reads the page's own readout table back, plus the geometry behind it, in both list lengths and
both themes, so the numbers quoted in `## UI/UX` are rendered ones. Screenshots land in `shots/`.
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE / "preview.html"
SHOTS = HERE / "shots"

GEOMETRY = """(() => {
  const read = col => {
    const dialog = document.querySelector('#' + col + ' dialog');
    const list = dialog.querySelector('#listNow, #listAfter');
    const d = dialog.getBoundingClientRect();
    const l = list.getBoundingClientRect();
    const cs = getComputedStyle(dialog);
    return {
      dialog: { x: Math.round(d.x), width: Math.round(d.width), height: Math.round(d.height), bottom: Math.round(d.bottom), overflowY: cs.overflowY },
      padding: cs.padding,
      list: { top: Math.round(l.top), bottom: Math.round(l.bottom), clientHeight: list.clientHeight, scrollHeight: list.scrollHeight, overflowY: getComputedStyle(list).overflowY },
      hr: (() => { const h = list.querySelector('.media-transfers__divider').getBoundingClientRect(); return { top: Math.round(h.top), height: Math.round(h.height) }; })(),
      rowBorders: [...list.querySelectorAll('.media-transfers__row')].slice(0, 3).map(r => getComputedStyle(r).borderBottomWidth),
      rows: list.querySelectorAll('.media-transfers__row').length,
      innerBottom: Math.round(d.bottom - parseFloat(cs.borderBottomWidth) - parseFloat(cs.paddingBottom)),
    };
  };
  return { now: read('colNow'), after: read('colAfter') };
})()"""


def snapshot(page, theme, length, tag):
    page.evaluate("t => document.documentElement.dataset.theme = t", theme)
    page.wait_for_timeout(200)
    page.screenshot(path=str(SHOTS / f"{tag}.png"), full_page=True)
    for col in ("colNow", "colAfter"):
        page.locator(f"#{col}").screenshot(path=str(SHOTS / f"{tag}-{col}.png"))
    for detail in ("detailNow", "detailAfter"):
        page.locator(f"#{detail}").screenshot(path=str(SHOTS / f"{tag}-{detail}.png"))
    return {
        "table": page.evaluate("""[...document.querySelectorAll('#metrics tbody tr')].map(tr => [...tr.children].map(c => c.textContent.trim()))"""),
        "geometry": page.evaluate(GEOMETRY),
    }


def main() -> int:
    SHOTS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1200}, device_scale_factor=1)
        page.goto(PAGE.as_uri())
        page.wait_for_timeout(700)

        out = {"viewport": page.evaluate("[innerWidth, innerHeight, devicePixelRatio]")}
        out["nine-light"] = snapshot(page, "light", 9, "nine-light")
        out["nine-dark"] = snapshot(page, "dark", 9, "nine-dark")

        page.click("#lengthBtn")
        page.wait_for_timeout(250)
        out["fifteen-light"] = snapshot(page, "light", 15, "fifteen-light")
        out["fifteen-dark"] = snapshot(page, "dark", 15, "fifteen-dark")

        print(json.dumps(out, indent=1))
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
