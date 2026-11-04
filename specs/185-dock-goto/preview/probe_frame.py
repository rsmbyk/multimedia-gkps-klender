"""Render the preview the way the desktop chat does, and check it arrives whole.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python specs/185-dock-goto/preview/probe_frame.py

`::preview{file=…}` does not load the page by URL. The app reads the file's text and sets
it as an iframe's `srcdoc`, sandboxed with `allow-scripts` and — deliberately — no
`allow-same-origin` (apps/desktop/src/components/assistant-ui/inline-preview-directive.tsx).
In that opaque origin a relative `<link>`/`<script src>` does not resolve and `file://`
cannot be read, so a page that works when opened directly can render as bare markup in the
chat. That is exactly what happened to the first version of `sync.html`.

This reproduces the mechanism: the page's text goes in as `srcdoc`, and the checks run
inside the frame — styles applied, scripts run, fonts resolved, surfaces painted.
"""

import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)

WRAPPER = """<!doctype html><html><body style="margin:0;background:#14120F">
<iframe id="f" sandbox="allow-scripts" style="width:660px;height:900px;border:0"></iframe>
</body></html>"""

failures = []


def check(name, ok, detail=""):
    print(("  ok   " if ok else "  FAIL ") + name + ((" — " + str(detail)) if detail else ""))
    if not ok:
        failures.append(name)


def load(page, name):
    text = (HERE / name).read_text(encoding="utf-8")
    page.set_content(WRAPPER)
    # Passed as an evaluated argument, never spliced into HTML: the page's own
    # </script> tags would end the wrapper's script block.
    page.evaluate("(doc) => { document.getElementById('f').srcdoc = doc; }", text)
    page.wait_for_timeout(1500)
    frame = page.frames[1]
    height = frame.evaluate("document.documentElement.scrollHeight")
    page.evaluate("(h) => { document.getElementById('f').style.height = h + 'px'; }", height)
    page.set_viewport_size({"width": 700, "height": min(height + 40, 4000)})
    page.wait_for_timeout(250)
    return frame, height


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 700, "height": 940}, device_scale_factor=1.25)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))

        print("== the dock page")
        frame, height = load(page, "index.html")
        dock = frame.evaluate("""() => {
          const panel = document.getElementById('dockPanel');
          const rows = document.querySelectorAll('#entryList .entryrow').length;
          return {rows, width: panel ? Math.round(panel.getBoundingClientRect().width) : 0,
                  display: panel ? getComputedStyle(panel).display : '',
                  token: getComputedStyle(document.documentElement)
                           .getPropertyValue('--font-sans').trim().slice(0, 20),
                  height: document.documentElement.scrollHeight};
        }""")
        print(f"  {dock}")
        check("the stylesheet arrived", dock["display"] == "flex" and dock["width"] == 400, dock)
        check("the script built the runner", dock["rows"] == 27, dock["rows"])
        # The dock asks for --font-sans, which the product resolves from the machine
        # (tokens.css:83) — the bundled face is the display's, checked on the sync page.
        check("the tokens arrived", dock["token"].startswith("ui-sans-serif"), dock["token"])
        check("no script error", not errors, str(errors))
        page.screenshot(path=str(SHOTS / "frame-dock.png"), full_page=True)

        print("\n== the sync page")
        errors.clear()
        frame, height = load(page, "sync.html")
        state = frame.evaluate("""() => {
          const proj = document.querySelector('.sv-projector .screen.is-active');
          const lines = proj && proj.querySelector('.screen__lines');
          const overlay = document.getElementById('svOverlayStage');
          return {steps: document.querySelectorAll('#svSteps button').length,
                  rows: document.querySelectorAll('#entryList .entryrow').length,
                  projSize: lines ? getComputedStyle(lines).fontSize : '',
                  font: lines ? getComputedStyle(lines).fontFamily.split(',')[0] : '',
                  overlay: overlay ? overlay.dataset.kind : '',
                  height: document.documentElement.scrollHeight};
        }""")
        print(f"  {state}")
        check("the stylesheet arrived", state["steps"] == 9 and state["overlay"] == "liturgy", state)
        check("both scripts ran", state["rows"] == 27 and state["projSize"] != "", state)
        check("the bundled face resolved on the display", state["font"].strip('"') == "CMG Sans", state["font"])

        frame.evaluate("document.querySelector('#svSteps button:nth-child(5)').click()")
        page.wait_for_timeout(600)
        after = frame.evaluate("""() => ({
          head: document.querySelector('.sv-projector .screen__head')?.textContent || '',
          dock: document.getElementById('offLabel').textContent,
          overlay: document.querySelector('.obs-overlay__kicker')?.textContent || '',
          read: document.getElementById('svRead').innerText.replace(/\\n/g, ' | ')
        })""")
        print(f"  {after['read'][:120]}")
        check("a step reaches all three surfaces",
              after["head"] == after["dock"] == after["overlay"] == "Matius 5:3", after)
        check("each surface reported for itself",
              after["read"].count("Matius 5:3") >= 3, after["read"][:100])
        check("no script error", not errors, str(errors))
        page.screenshot(path=str(SHOTS / "frame-sync.png"), full_page=True)

        browser.close()

    print("\n== result")
    if failures:
        print("  FAILURES: " + ", ".join(failures))
        sys.exit(1)
    print("  all checks passed; shots in " + str(SHOTS))


if __name__ == "__main__":
    main()
