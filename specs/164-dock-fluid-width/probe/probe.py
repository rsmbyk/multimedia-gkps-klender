"""Measure the dock panel at every width the spec names.

Usage:
    python specs/164-dock-fluid-width/probe/probe.py [base-url]

Defaults to http://127.0.0.1:8799. Prints one markdown row per width: the panel's
box, the picker body's display, the first service row's width, whether the bucket
head is sticky, and the page's horizontal overflow.
"""
import sys
import time

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8799'
WIDTHS = (320, 420, 560, 720, 900, 1440, 1920, 2560)

READ = """() => {
  const dock = document.querySelector('.dock').getBoundingClientRect();
  const body = document.getElementById('pickBody');
  const row = body.querySelector('.servicerow');
  const head = body.querySelector('.group__head');
  const style = getComputedStyle(body);
  return {
    vw: document.documentElement.clientWidth,
    dockX: +dock.x.toFixed(1), dockW: +dock.width.toFixed(1), dockH: +dock.height.toFixed(1),
    display: style.display,
    contentW: body.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight),
    rowW: row ? +row.getBoundingClientRect().width.toFixed(1) : null,
    rows: body.querySelectorAll('.servicerow').length,
    head: head ? getComputedStyle(head).position : null,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
}"""


def main():
    print('| viewport | panel | x | picker display | row | sticky head | overflow |')
    print('| --- | --- | --- | --- | --- | --- | --- |')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 900})
        page.goto(BASE + '/obs/dock', wait_until='domcontentloaded')
        page.wait_for_selector('#pickBody .servicerow', state='attached')
        for width in WIDTHS:
            page.set_viewport_size({'width': width, 'height': 900})
            for attempt in range(3):
                try:
                    box = page.evaluate(READ)
                    break
                except Exception:  # a re-layout can race the read; retry once or twice
                    time.sleep(0.2)
            else:
                raise SystemExit(f'could not read the dock at {width}px')
            print(f"| {width} | {box['dockW']:.0f} × {box['dockH']:.0f} | {box['dockX']:.0f} | "
                  f"{box['display']} | {box['rowW']:.0f} | {box['head']} | {box['overflow']} |")
        browser.close()


if __name__ == '__main__':
    main()
