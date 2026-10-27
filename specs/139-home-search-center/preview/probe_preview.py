"""Measure and photograph the slice's static preview.

Run with the project's venv:

    .venv/bin/python specs/139-home-search-center/preview/probe_preview.py --shots

Prints, for `before-home.html` and `after-home.html`, the field's border box, the
logo's, the document's height and any horizontal overflow at each width — the
numbers the spec's UI/UX section quotes — and writes `shots/` when `--shots` is
passed. `--url <url>` measures a running instance instead of the static pages, so
the recorded numbers can be read off the stylesheet as it ships.
"""
import pathlib
import sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
WIDTHS = [(1920, 1000), (1440, 900), (1280, 800), (1024, 768), (834, 1112),
          (720, 900), (390, 844), (320, 568)]
SHOTS = "--shots" in sys.argv
LIVE = sys.argv[sys.argv.index("--url") + 1] if "--url" in sys.argv else None

RECT = """sel => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const b = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  if (cs.display === 'none') return 'hidden';
  return {top:+b.top.toFixed(1), bottom:+b.bottom.toFixed(1), h:+b.height.toFixed(1),
          cy:+((b.top+b.bottom)/2).toFixed(1), w:+b.width.toFixed(1)};
}"""


def main() -> None:
    (HERE / "shots").mkdir(exist_ok=True)
    targets = ([("live", LIVE)] if LIVE
               else [(label, (HERE / f"{label}-home.html").as_uri()) for label in ("before", "after")])
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, page_url in targets:
            for w, h in WIDTHS:
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto(page_url, wait_until="networkidle")
                page.wait_for_timeout(150)
                field = page.evaluate(RECT, ".search-home__input")
                logo = page.evaluate(RECT, ".search-home__logo")
                doc = page.evaluate("""() => ({h: document.documentElement.scrollHeight,
                                               ovx: document.documentElement.scrollWidth -
                                                    document.documentElement.clientWidth,
                                               vh: innerHeight})""")
                mid = h / 2
                print(f"{label:6} {w}x{h}: field cy={field['cy']:>6} (window {mid:>6}) "
                      f"delta={field['cy'] - mid:+.1f} box={field['top']}..{field['bottom']} "
                      f"logo_top={logo['top'] if logo != 'hidden' else 'hidden'} "
                      f"gap={round(field['top'] - logo['bottom'], 1) if logo != 'hidden' else '-'} "
                      f"docH={doc['h']} ovX={doc['ovx']}")
                if SHOTS and (w, h) in ((1440, 900), (390, 844)):
                    shot = HERE / "shots" / f"{label}-{w}x{h}.png"
                    page.screenshot(path=str(shot))
                    print(f"       wrote {shot.relative_to(HERE.parent)}")
                page.close()
        browser.close()


if __name__ == "__main__":
    main()
