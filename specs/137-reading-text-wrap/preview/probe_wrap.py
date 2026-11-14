"""Spec 137 — the numbers quoted in `## UI/UX`, measured on the preview files.

Opens each `before-*.html` / `after-*.html` pair at three viewports and prints:

    title lines   the h1's own line count, and its box height
    doc overflow  how far the document's scrollWidth runs past the viewport
    spills        every text run painted past the box that owns it, and by how much

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/137-reading-text-wrap/preview/probe_wrap.py
"""
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
PAGES = ['tatib', 'songs', 'bible', 'search']
VIEWPORTS = [(1440, 900), (1280, 800), (390, 844)]

MEASURE = r"""
() => {
  const vw = document.documentElement.clientWidth;
  const out = {doc: Math.round(document.documentElement.scrollWidth - vw), spills: [], title: null};
  const name = (el) => {
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).join('.') : '';
    return el.tagName.toLowerCase() + cls;
  };
  const blockAncestor = (node) => {
    let el = node.parentElement;
    while (el && el !== document.body) {
      const d = getComputedStyle(el).display;
      if (!d.startsWith('inline') && d !== 'contents') return el;
      el = el.parentElement;
    }
    return el;
  };
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  let node;
  while ((node = walker.nextNode())) {
    if (!node.textContent.trim()) continue;
    const host = blockAncestor(node);
    if (!host || host.classList.contains('sr')) continue;
    const hs = getComputedStyle(host);
    if (hs.display === 'none' || hs.visibility === 'hidden') continue;
    const box = host.getBoundingClientRect();
    if (box.width <= 2) continue;
    const r = document.createRange();
    r.selectNodeContents(node);
    const rects = [...r.getClientRects()];
    if (!rects.length) continue;
    const right = Math.max(...rects.map(b => b.right));
    const spill = Math.round(right - (box.left + host.clientLeft + host.clientWidth));
    if (spill <= 1) continue;
    const key = name(host);
    if (seen.has(key)) continue;
    seen.add(key);
    out.spills.push({el: key, spill, clip: hs.overflowX});
  }
  const title = document.querySelector('.read__title');
  if (title && title.getBoundingClientRect().width) {
    const cs = getComputedStyle(title);
    const box = title.getBoundingClientRect();
    const lh = parseFloat(cs.lineHeight) || 1;
    out.title = {lines: Math.round(box.height / lh), height: Math.round(box.height),
                 width: Math.round(box.width), font: cs.fontSize,
                 lineHeight: Math.round(lh * 100) / 100, wrap: cs.overflowWrap};
  }
  return out;
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height in VIEWPORTS:
        print(f'\n### viewport {width}x{height}')
        for name in PAGES:
            page = browser.new_page(viewport={'width': width, 'height': height})
            row = {}
            for flavour in ('before', 'after'):
                page.goto((HERE / f'{flavour}-{name}.html').as_uri())
                page.wait_for_timeout(150)
                row[flavour] = page.evaluate(MEASURE)
            page.close()
            b, a = row['before'], row['after']
            t0, t1 = b['title'] or {}, a['title'] or {}
            print(f'  {name:<7} doc overflow {b["doc"]:>5} -> {a["doc"]:>3}px   '
                  f'title {t0.get("lines", "-")} -> {t1.get("lines", "-")} lines, '
                  f'{t0.get("height", "-")} -> {t1.get("height", "-")}px in '
                  f'{t1.get("width", "-")}px  ({t1.get("font", "-")}/'
                  f'{t1.get("lineHeight", "-")}, {t1.get("wrap", "-")})')
            for spill in b['spills']:
                fixed = next((x for x in a['spills'] if x['el'] == spill['el']), None)
                print(f'      spill {spill["el"]:<22} {spill["spill"]:>5} -> '
                      f'{fixed["spill"] if fixed else 0:>3}px  (overflow-x: {spill["clip"]})')
    browser.close()
