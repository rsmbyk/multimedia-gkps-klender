"""Measure the empty Tata Ibadah stage: is the block centred under the header, and
are the five add actions one row of square tiles?

    .venv/bin/python specs/130-empty-service-tiles/preview/probe_empty_stage.py URL
    .venv/bin/python specs/130-empty-service-tiles/preview/probe_empty_stage.py URL --layout-only

`--layout-only` prints the header/body margins instead, which is what the
regression check on a service that holds items needs.
"""

import sys

from playwright.sync_api import sync_playwright

VIEWPORTS = [(1440, 900), (1280, 800), (1024, 700), (390, 844)]

MEASURE = """
() => {
  const box = (sel) => {
    const element = document.querySelector(sel);
    if (!element) return null;
    const rect = element.getBoundingClientRect();
    const style = getComputedStyle(element);
    return {top: rect.top, bottom: rect.bottom, width: rect.width, height: rect.height,
            marginTop: style.marginTop, marginBottom: style.marginBottom,
            display: style.display};
  };
  const tiles = [...document.querySelectorAll('.entry__empty-btn')].map((button) => {
    const rect = button.getBoundingClientRect();
    return {label: button.textContent.trim(), glyphs: button.querySelectorAll('svg').length,
            x: rect.left, y: rect.top, width: rect.width, height: rect.height};
  });
  return {viewportHeight: innerHeight, header: box('.read__head'), body: box('#readBody'),
          empty: box('.entry__empty'), tiles};
}
"""


def report(label, data, layout_only):
    header, body, empty, tiles = (data["header"], data["body"], data["empty"], data["tiles"])
    if not layout_only and empty:
        centre = (empty["top"] + empty["bottom"]) / 2
        fraction = (centre - body["top"]) / body["height"] if body["height"] else 0
        clear = empty["top"] - header["bottom"]
        rows = [round(tile["y"], 1) for tile in tiles]
        arrangement = "one row" if len(set(rows)) == 1 else (
            " + ".join(str(rows.count(y)) for y in dict.fromkeys(rows)))
        squares = all(abs(tile["width"] - tile["height"]) < 1 for tile in tiles)
        smallest = min(min(tile["width"], tile["height"]) for tile in tiles)
        print(f'{label}: centre {fraction * 100:.1f}% of the reading area (quarter = 25%) · '
              f'clear of header {clear:.1f}px · {len(tiles)} tiles · {arrangement} · '
              f'square {squares} · smallest {smallest:.1f}px · '
              f'labels {[tile["label"] for tile in tiles]}')
        return
    print(f'{label}: header {header["height"]:.1f}px mb={header["marginBottom"]} · '
          f'body mt={body["marginTop"]} display={body["display"]} · '
          f'empty {"present" if empty else "absent"}')


def main():
    url = sys.argv[1]
    layout_only = "--layout-only" in sys.argv[2:]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for width, height in VIEWPORTS:
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(url, wait_until="load")
            page.wait_for_selector(".read__body")
            page.wait_for_timeout(300)
            report(f"{width}x{height}", page.evaluate(MEASURE), layout_only)
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
