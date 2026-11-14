"""Spec 135 preview probe — how many lines a contents row actually paints.

Opens `after.html` from disk at three viewports and prints one record per row:
its index, the first 60 characters of its text, the number of line boxes the
label paints, the row's height, whether the label's content is taller than its
box, and whether it ends in a literal `…`.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/135-tatib-sidebar-row-clamp/preview/probe_rows.py
"""
import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
PAGE = (HERE / 'after.html').as_uri()

READ = """() => {
  const rows = [...document.querySelectorAll('#chList li')];
  return rows.map((li, i) => {
    const label = li.querySelector('.songrow__t');
    const link = li.querySelector('.songrow');
    if (!label) return {i: i + 1, kind: 'empty row'};
    const range = document.createRange();
    range.selectNodeContents(label);
    const tops = [...range.getClientRects()].map((r) => Math.round(r.top));
    const lines = [...new Set(tops)].sort((a, b) => a - b).length;
    const box = label.getBoundingClientRect();
    const rowBox = (link || li).getBoundingClientRect();
    const style = getComputedStyle(label);
    return {
      i: i + 1,
      fixture: li.dataset.fixture === '1',
      text: label.textContent.slice(0, 60),
      lines,
      h: +box.height.toFixed(1),
      rowH: +rowBox.height.toFixed(1),
      lineHeight: style.lineHeight,
      clamp: style.webkitLineClamp,
      clipped: label.scrollHeight > label.clientHeight + 1,
      literalEllipsis: label.textContent.trim().endsWith('…'),
    };
  });
}"""


def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height in ((1440, 900), (1280, 800), (390, 844)):
            page = browser.new_page(viewport={'width': width, 'height': height})
            page.goto(PAGE)
            page.wait_for_timeout(250)
            key = f'{width}x{height}'
            result[key] = {
                'panelWidth': page.evaluate(
                    "() => +document.querySelector('#chList').getBoundingClientRect().width.toFixed(1)"),
                'rows': page.evaluate(READ),
            }
            page.screenshot(path=str(HERE / f'after-{key}.png'), full_page=False)
            page.close()
        browser.close()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
