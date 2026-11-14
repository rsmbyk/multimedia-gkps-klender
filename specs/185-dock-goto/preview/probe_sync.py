"""Drive the sync page: one state, three surfaces, nine steps (spec 185).

    ~/Projects/multimedia-gkps-klender/.venv/bin/python specs/185-dock-goto/preview/probe_sync.py

Each step is asserted against the three surfaces' own DOM — the dock's block and rows, the
projector's stage, the overlay's stage — rather than against the page's report lines. The
report lines are then checked to carry the same words, because they are what the owner reads.

The page draws all three in one document (the chat's preview frame runs no nested
documents), so this reads the page itself: there are no frames to switch into.
"""

import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = (HERE / "sync.html").as_uri()
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)

failures = []


def check(name, ok, detail: object = ""):
    print(("  ok   " if ok else "  FAIL ") + name + ((" — " + str(detail)) if detail else ""))
    if not ok:
        failures.append(name)


DOCK = """() => {
  const block = document.getElementById('offBlock');
  const label = document.getElementById('offLabel');
  const chip = document.getElementById('transChip');
  return {block: !block.hidden,
          band: document.getElementById('bandSwap').classList.contains('is-find'),
          label: label ? label.textContent : '',
          chip: chip && !chip.hidden ? chip.textContent : '',
          rows: document.querySelectorAll('#offBody [data-pos]').length,
          eye: document.getElementById('blankBtn').title};
}"""

PROJECTOR = """() => {
  const canvas = document.querySelector('.sv-projector');
  const s = document.querySelector('.sv-projector .screen.is-active');
  const lines = s ? s.querySelector('.screen__lines') : null;
  return {showing: canvas.dataset.showing,
          head: s && s.querySelector('.screen__head') ? s.querySelector('.screen__head').textContent : '',
          line: lines && lines.querySelector('.screen__line') ? lines.querySelector('.screen__line').textContent : '',
          size: lines ? parseFloat(getComputedStyle(lines).fontSize) : 0,
          count: lines ? lines.querySelectorAll('.screen__line').length : 0};
}"""

OVERLAY = """() => {
  const stage = document.getElementById('svOverlayStage');
  const words = stage.querySelector('.obs-overlay__words');
  const line = words || stage.querySelector('.obs-overlay__caption span, .obs-overlay__line');
  return {kind: stage.dataset.kind,
          kicker: stage.querySelector('.obs-overlay__kicker') ? stage.querySelector('.obs-overlay__kicker').textContent : '',
          line: line ? line.textContent : ''};
}"""


def words(text):
    """The words a surface paints, without the speaker mark's 'L:' glue."""
    return re.sub(r"^[^:]{0,8}:\s*", "", " ".join(text.split()))


def step(page, number):
    page.click(f'#svSteps button:nth-child({number})')
    page.wait_for_timeout(420)
    return {name: page.evaluate(script) for name, script in
            (("dock", DOCK), ("projector", PROJECTOR), ("overlay", OVERLAY))}


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1000, "height": 1030}, device_scale_factor=1.5)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(PAGE)
        page.wait_for_timeout(900)

        print("== the page")
        check("nine steps are offered", page.locator("#svSteps button").count() == 9)
        check("one document, no frames", len(page.frames) == 1, len(page.frames))
        check("no script error", not errors, str(errors))

        print("\n== 1 · the service is on air")
        s = step(page, 1)
        page.screenshot(path=str(SHOTS / "sync-1.png"), full_page=True)
        print(f"  dock {s['dock']}\n  projector {s['projector']}\n  overlay {s['overlay']}")
        check("the dock shows the service, nothing else", not s["dock"]["block"] and not s["dock"]["band"])
        check("the projector shows the service's screen",
              s["projector"]["showing"] == "true" and bool(s["projector"]["line"]))
        check("the overlay paints the same screen",
              s["overlay"]["kind"] == "liturgy"
              and words(s["overlay"]["line"])[:24] == words(s["projector"]["line"])[:24],
              (s["overlay"]["line"][:30], s["projector"]["line"][:30]))

        print("\n== 2 · G opens the go to")
        s2 = step(page, 2)
        page.screenshot(path=str(SHOTS / "sync-2.png"), full_page=True)
        check("the band is open in the dock", s2["dock"]["band"])
        check("nothing on air changed", s2["projector"] == s["projector"] and s2["overlay"] == s["overlay"])

        print("\n== 3 · NKB 43 is chosen")
        s3 = step(page, 3)
        page.screenshot(path=str(SHOTS / "sync-3.png"), full_page=True)
        print(f"  dock {s3['dock']}\n  projector {s3['projector']}\n  overlay {s3['overlay']}")
        check("the dock draws the go to block",
              s3["dock"]["block"] and "NKB 43" in s3["dock"]["label"], s3["dock"]["label"])
        check("the projector paints the same lyric",
              words(s3["projector"]["line"]) == words(s3["overlay"]["line"]) and bool(s3["projector"]["line"]))
        check("the overlay paints it as a caption", s3["overlay"]["kind"] == "song")

        print("\n== 4 · it steps")
        s4 = step(page, 4)
        check("all three follow the step",
              words(s4["projector"]["line"]) == words(s4["overlay"]["line"])
              and s4["projector"]["line"] != s3["projector"]["line"])

        print("\n== 5 · Matius 5:3 is chosen")
        s5 = step(page, 5)
        page.screenshot(path=str(SHOTS / "sync-5.png"), full_page=True)
        print(f"  dock {s5['dock']}\n  projector {s5['projector']}\n  overlay {s5['overlay']}")
        check("the dock names it", s5["dock"]["label"] == "Matius 5:3" and s5["dock"]["chip"] == "TB",
              (s5["dock"]["label"], s5["dock"]["chip"]))
        check("the dock lists the verse", s5["dock"]["rows"] >= 3, s5["dock"]["rows"])
        check("the projector fits the whole verse",
              s5["projector"]["head"] == "Matius 5:3" and 2 <= s5["projector"]["size"] <= 200
              and words(s5["projector"]["line"]) == words(s5["overlay"]["line"]))
        check("the overlay paints a passage plate",
              s5["overlay"]["kind"] == "passage" and s5["overlay"]["kicker"] == "Matius 5:3")

        print("\n== 6 · the edition flips")
        s6 = step(page, 6)
        page.screenshot(path=str(SHOTS / "sync-6.png"), full_page=True)
        print(f"  dock {s6['dock']}\n  projector {s6['projector']}\n  overlay {s6['overlay']}")
        check("the projector and overlay show the Simalungun edition",
              s6["projector"]["head"] == "Mateus 5:3" and s6["overlay"]["kicker"] == "Mateus 5:3"
              and words(s6["projector"]["line"]) == words(s6["overlay"]["line"]))
        check("the dock keeps the TB reference and shows the chip",
              s6["dock"]["label"] == "Matius 5:3" and s6["dock"]["chip"] == "SIM",
              (s6["dock"]["label"], s6["dock"]["chip"]))

        print("\n== 7 · the words are hidden")
        s7 = step(page, 7)
        page.screenshot(path=str(SHOTS / "sync-7.png"), full_page=True)
        print(f"  dock {s7['dock']}\n  projector {s7['projector']}\n  overlay {s7['overlay']}")
        check("the projector paints no words", s7["projector"]["showing"] == "false")
        check("the overlay paints nothing", s7["overlay"]["line"] == "" and s7["overlay"]["kind"] == "")
        check("the dock keeps the block and offers the words back",
              s7["dock"]["block"] and s7["dock"]["eye"] == "Show words", s7["dock"]["eye"])

        print("\n== 8 · Back")
        s8 = step(page, 8)
        page.screenshot(path=str(SHOTS / "sync-8.png"), full_page=True)
        print(f"  dock {s8['dock']}\n  projector {s8['projector']}\n  overlay {s8['overlay']}")
        check("the block is gone and the service is back", not s8["dock"]["block"])
        check("the blocks keep the words hidden, as they were left",
              s8["projector"]["showing"] == "false"
              and s8["projector"]["line"] == s["projector"]["line"]
              and s8["overlay"]["line"] == "")

        print("\n== 9 · the words come back")
        s9 = step(page, 9)
        page.screenshot(path=str(SHOTS / "sync-9.png"), full_page=True)
        check("every surface names the service's screen again",
              s9["projector"]["showing"] == "true"
              and words(s9["projector"]["line"]) == words(s9["overlay"]["line"])
              and s9["projector"]["line"] == s["projector"]["line"])

        print("\n== the adapters")
        values = page.evaluate("""() => {
          const canvas = document.querySelector('.sv-projector');
          const cs = getComputedStyle(canvas);
          const screen = document.querySelector('.sv-projector .screen.is-active');
          const line = screen.querySelector('.screen__line');
          const lcs = line ? getComputedStyle(line) : null;
          const overlay = document.getElementById('svOverlayStage');
          return {canvas_bg: cs.backgroundColor, ink: cs.color, family: cs.fontFamily,
                  weight: cs.fontWeight,
                  leading: lcs ? (parseFloat(lcs.lineHeight) / parseFloat(lcs.fontSize)) : 0,
                  head: cs.getPropertyValue('--display-head').trim(),
                  stage_pos: getComputedStyle(overlay).position,
                  stage_box: [overlay.clientWidth, overlay.clientHeight]};
        }""")
        print(f"  {values}")
        check("the projector panel takes the display's ink and canvas",
              values["ink"] == "rgb(245, 243, 238)" and values["canvas_bg"] == "rgb(20, 19, 15)",
              (values["ink"], values["canvas_bg"]))
        check("it takes the display's face, weight and leading",
              values["family"].lstrip('\"').startswith("CMG Sans") and values["weight"] == "700"
              and abs(values["leading"] - 1.37) < 0.01, values["leading"])
        check("it takes the display heading colour", values["head"] == "#FFD166", values["head"])
        check("the overlay stage resolves against 1920 × 1080 inside its panel",
              values["stage_pos"] == "absolute" and values["stage_box"] == [1920, 1080],
              values["stage_box"])

        print("\n== the page's own report")
        probe = words(s9["projector"]["line"])[:28]
        report = " ".join(page.inner_text("#svRead").split())
        check("the report carries the same words as the surfaces",
              probe in report and report.count(probe) >= 2, report[:160])

        browser.close()

    print("\n== result")
    if failures:
        print("  FAILURES: " + ", ".join(failures))
        sys.exit(1)
    print("  all checks passed; shots in " + str(SHOTS))


if __name__ == "__main__":
    main()
