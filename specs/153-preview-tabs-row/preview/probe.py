#!/usr/bin/env python3
"""Measure the spec 153 preview in a real browser and write its screenshots.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/153-preview-tabs-row/preview/probe.py

Reads the page's own measurements back — header, title, tab band, first tab — in both states and
both themes, then opens each demo dialog by pointer and by keyboard and records what took focus.
Screenshots land in `shots/` (not committed).
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE / "preview.html"
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)

FOCUS = """() => {
  const a = document.activeElement;
  const modal = a.closest('dialog');
  const tab = modal && modal.querySelector('.preview__tab');
  const body = modal && modal.querySelector('.preview__body');
  return {
    active: a.tagName.toLowerCase() + (a.className ? '.' + a.className.split(' ')[0] : ''),
    activeId: a.id || null,
    focusVisible: a.matches(':focus-visible'),
    tabFocusVisible: tab ? tab.matches(':focus-visible') : null,
    bodyFocusVisible: body ? body.matches(':focus-visible') : null,
  };
}"""


def shot(page, name):
    page.screenshot(path=str(SHOTS / name))
    return str(SHOTS / name)


def main():
    report = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(PAGE.as_uri())
        page.wait_for_timeout(300)

        report["console_errors"] = errors
        report["1440"] = page.evaluate("window.measurePreview()")
        report["table"] = page.inner_text("#metrics")
        shot(page, "1440-light.png")

        # pointer open
        for which, button in (("now", "#focusNow"), ("after", "#focusAfter")):
            page.click(button)
            page.wait_for_timeout(200)
            report[f"pointer-{which}"] = page.evaluate(FOCUS)
            shot(page, f"focus-{which}-pointer.png")
            page.keyboard.press("Escape")
            page.wait_for_timeout(250)

        # keyboard open: focus the button, press Enter
        for which, button in (("now", "#focusNow"), ("after", "#focusAfter")):
            page.locator(button).focus()
            page.keyboard.press("Enter")
            page.wait_for_timeout(200)
            report[f"keyboard-{which}"] = page.evaluate(FOCUS)
            shot(page, f"focus-{which}-keyboard.png")
            page.keyboard.press("Escape")
            page.wait_for_timeout(250)

        # dark theme
        page.click("#themeBtn")
        page.wait_for_timeout(200)
        report["dark"] = page.evaluate("window.measurePreview()")
        shot(page, "1440-dark.png")
        page.click("#themeBtn")

        # a phone
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(300)
        report["390"] = page.evaluate("window.measurePreview()")
        report["390-table"] = page.inner_text("#metrics")
        report["390-tablist"] = page.evaluate("""() => {
          const tablist = document.querySelector('#colAfter .preview__tabs');
          const first = tablist && tablist.querySelector('.preview__tab');
          return tablist && {
            scrollWidth: tablist.scrollWidth, clientWidth: tablist.clientWidth,
            tab: first ? [first.getBoundingClientRect().width, first.getBoundingClientRect().height,
                          getComputedStyle(first).borderRadius] : null,
          };
        }""")
        shot(page, "390-after.png")
        browser.close()

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
