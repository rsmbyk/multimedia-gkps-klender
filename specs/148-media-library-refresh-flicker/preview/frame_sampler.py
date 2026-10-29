"""Frame sampler for the Media Library refresh: does the list hold still?

Drives one refresh from a click (a row's Remove, cancelled) and records the top of every
`.media-library__file` on every animation frame, from the click to the settled list.

    .venv/bin/python specs/148-media-library-refresh-flicker/preview/frame_sampler.py [url]

The url defaults to the compose `web` service; pass another one to read a worktree dev
server, e.g. http://localhost:8765/media-library/ .
"""
import sys

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:63404/media-library/"
ROWS = 5  # rows sampled per frame: enough to show the growing jolt, cheap to print

SAMPLER = """
window.__samples = [];
(function sample() {
  var list = document.getElementById('mediaFileList');
  if (list) {
    var rows = [].slice.call(list.querySelectorAll('.media-library__file'));
    window.__samples.push({
      n: rows.length,
      placeholder: list.querySelectorAll('.media-library__unused').length,
      tops: rows.slice(0, %d).map(function (r) { return Math.round(r.getBoundingClientRect().top); }),
      listH: Math.round(list.getBoundingClientRect().height)
    });
  }
  requestAnimationFrame(sample);
})();
""" % ROWS


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1100})
        page.add_init_script(SAMPLER)
        page.goto(URL, wait_until="load")
        page.wait_for_timeout(2500)

        clicked = page.evaluate(
            """() => {
              window.__samples = [];
              const buttons = [...document.querySelectorAll('.media-library__remove')].filter(b => !b.disabled);
              if (!buttons.length) return 'no removable row';
              buttons[0].click();
              return buttons[0].getAttribute('aria-label');
            }"""
        )
        page.wait_for_timeout(1200)
        page.keyboard.press("Escape")
        samples = page.evaluate("() => window.__samples")
        browser.close()

    print("clicked:", clicked)
    seen, columns = set(), {}
    for sample in samples:
        key = (sample["n"], tuple(sample["tops"]), sample["listH"])
        if key in seen:
            continue
        seen.add(key)
        print("  rows=%d placeholders=%d listH=%d tops=%s"
              % (sample["n"], sample["placeholder"], sample["listH"], sample["tops"]))
        for index, top in enumerate(sample["tops"]):
            columns.setdefault(index, []).append(top)

    worst = 0
    for index, tops in sorted(columns.items()):
        jolt = max(tops) - min(tops)
        worst = max(worst, jolt)
        print("row %d: top %d..%d  jolt=%dpx" % (index + 1, min(tops), max(tops), jolt))

    with_placeholder = sum(1 for s in samples if s["placeholder"] > 1)
    print("\nworst jolt: %dpx | frames showing the placeholder on more than one row: %d of %d"
          % (worst, with_placeholder, len(samples)))
    return 0 if worst == 0 and not with_placeholder else 1


if __name__ == "__main__":
    sys.exit(main())
