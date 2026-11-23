#!/usr/bin/env python3
"""Measure the verse editor's header rules on a live route (spec 226).

Default URL is the compose web service serving the base checkout.  With
--inject-fix the candidate CSS is injected in the browser before the dialog
opens, so the after state can be measured before the product file changes.
Screenshots and the read-back go to specs/226-.../preview/shots/ (gitignored).
"""
import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

SHOTS = Path(__file__).resolve().parent / "shots"
REPORT = SHOTS.parent / "report.json"

MEASURE = """() => {
  const box = el => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return {
      text: el.textContent.trim(),
      x: +r.x.toFixed(1), y: +r.y.toFixed(1),
      w: +r.width.toFixed(1), h: +r.height.toFixed(1),
      bottom: +r.bottom.toFixed(1),
      borderBottomWidth: s.borderBottomWidth,
      borderBottomColor: s.borderBottomColor,
      fontSize: s.fontSize, fontWeight: s.fontWeight,
      padding: s.padding, margin: s.margin
    };
  };
  const head = document.querySelector('#editorContent .editor__head');
  const title = head.querySelector('.editor__title');
  const range = document.createRange(); range.selectNodeContents(title);
  const tr = range.getBoundingClientRect();
  return {
    title: box(title),
    head: box(head),
    dialog: box(document.getElementById('editorModal')),
    gapTop: +(tr.y - document.getElementById('editorModal').getBoundingClientRect().y).toFixed(1),
    gapBelowText: +(head.getBoundingClientRect().bottom - 1 - tr.bottom).toFixed(1),
    ruledDescendants: [...head.querySelectorAll('*')]
      .filter(el => parseFloat(getComputedStyle(el).borderBottomWidth) > 0)
      .map(el => ({ cls: el.className, w: getComputedStyle(el).borderBottomWidth }))
  };
}"""

CANDIDATE = """
.editor:has([data-editor-size="large"]) .editor__head { padding: 20px 26px 14px; }
.editor:has([data-editor-size="large"]) .editor__title { margin: 0; padding: 0; border: 0; font-size: 21px; }
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:63404/songs/1820/")
    parser.add_argument("--inject-fix", action="store_true")
    parser.add_argument("--width", type=int, default=1366)
    parser.add_argument("--height", type=int, default=900)
    args = parser.parse_args()
    SHOTS.mkdir(parents=True, exist_ok=True)

    states, errors = {}, []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.goto(args.url, wait_until="networkidle")
        if args.inject_fix:
            page.add_style_tag(content=CANDIDATE)

        for state, selector in (("new", "[data-add-verse]"), ("edit", "[data-verse-edit]")):
            if page.locator(selector).count() == 0:
                states[state] = {"error": "control not found", "selector": selector}
                continue
            page.locator(selector).first.click(force=True)
            page.wait_for_selector("#editorModal[open] #editorTitle")
            page.wait_for_function(
                "document.querySelector('#editorTitle').textContent.trim().length > 0"
            )
            page.wait_for_timeout(250)
            states[state] = page.evaluate(MEASURE)
            dialog = page.locator("#editorModal")
            dialog.screenshot(path=str(SHOTS / ("%s-header.png" % state)))
            page.keyboard.press("Escape")
            page.wait_for_function("!document.getElementById('editorModal').open")

        browser.close()

    report = {
        "url": args.url,
        "viewport": "%dx%d" % (args.width, args.height),
        "candidate_injected": args.inject_fix,
        "states": states,
        "page_errors": errors,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
