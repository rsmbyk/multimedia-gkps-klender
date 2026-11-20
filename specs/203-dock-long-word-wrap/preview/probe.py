"""Spec 203 — measure the dock's long-word overflow, before and after the fix.

Runs against a live dock (the runner is JS-built from a fetched library, so a
static page cannot show it). Point it at any server:

    python probe.py --base http://127.0.0.1:8767 --service 149 --out shots/before

Every number is read from the rendered box, never computed from the rule.
"""

import argparse
import json
import pathlib

from playwright.sync_api import sync_playwright

MEASURE = """
() => {
  const box = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return {
      text: (el.textContent || '').trim().slice(0, 48),
      left: +r.left.toFixed(1), right: +r.right.toFixed(1),
      width: +r.width.toFixed(1), height: +r.height.toFixed(1),
      scrollWidth: el.scrollWidth, clientWidth: el.clientWidth,
      overflowX: el.scrollWidth - el.clientWidth,
      overflowWrap: cs.overflowWrap, wordBreak: cs.wordBreak,
      whiteSpace: cs.whiteSpace, minWidth: cs.minWidth,
      lines: Math.round(r.height / parseFloat(cs.lineHeight || '1')),
    };
  };
  const pick = (sel) => Array.from(document.querySelectorAll(sel)).map(box);
  const body = document.getElementById('runBody');
  const head = document.querySelector('#viewRun .dock__head');
  return {
    viewport: { w: innerWidth, h: innerHeight },
    docOverflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    head: box(head),
    runtitles: box(document.querySelector('.dock__runtitles')),
    serviceline: box(document.getElementById('runService')),
    servicedate: box(document.getElementById('runDate')),
    body: box(body),
    entryHeaders: pick('#entryList .entryrow__t'),
    entryRows: pick('#entryList .entryrow'),
    screenLines: pick('#entryList .screenerow__line'),
    screenRows: pick('#entryList .screenerow'),
    pickerNames: pick('#pickBody .servicerow__n'),
    nextband: box(document.querySelector('.nextband__label')),
    offstrip: box(document.querySelector('.offstrip__label')),
    numbers: pick('#entryList .entryrow__c'),
    chevrons: Array.from(document.querySelectorAll('#entryList .entrychev')).map((el) => {
      const r = el.getBoundingClientRect();
      const row = el.closest('.entryrow').getBoundingClientRect();
      return { offRight: +(row.right - r.right).toFixed(1),
               offCentre: +((r.top + r.bottom) / 2 - (row.top + row.bottom) / 2).toFixed(1),
               hidden: el.hasAttribute('hidden') };
    }),
  };
}
"""


# The rule this slice ships, and its value restored. The live server ships the rule, so
# `--restore` reads the BEFORE state and a plain run reads the AFTER state — one server,
# one page, both readings.
CANDIDATE = '.serviceline, .entryrow__t, .screenerow { overflow-wrap: anywhere; }'
RESTORE = '.serviceline, .entryrow__t, .screenerow { overflow-wrap: normal; }'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8767')
    ap.add_argument('--service', default='149')
    ap.add_argument('--width', type=int, default=456)
    ap.add_argument('--height', type=int, default=1087)
    ap.add_argument('--out', default='shots/before')
    ap.add_argument('--expand', action='store_true', help='open every entry block')
    ap.add_argument('--fix', action='store_true', help='inject the shipped rule (a no-op now it ships)')
    ap.add_argument('--restore', action='store_true', help='restore overflow-wrap: normal — the before state')
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={'width': args.width, 'height': args.height},
            color_scheme='dark', device_scale_factor=1)
        page.goto(args.base + '/obs/dock', wait_until='networkidle')
        if args.restore:
            page.add_style_tag(content=RESTORE)
        elif args.fix:
            page.add_style_tag(content=CANDIDATE)
        page.wait_for_selector('#pickBody .servicerow')
        page.screenshot(path=str(out / 'picker.png'))
        picker = page.evaluate(MEASURE)

        page.click(f'.servicerow[data-service="{args.service}"]')
        page.wait_for_selector('#viewRun.is-active')
        page.wait_for_selector('#entryList .entryrow')
        page.wait_for_timeout(400)

        if args.expand:
            for row in page.query_selector_all('#entryList .entryrow[aria-expanded="false"]'):
                row.click()
                page.wait_for_timeout(260)
            page.wait_for_timeout(300)

        page.screenshot(path=str(out / 'runner.png'), full_page=True)
        runner = page.evaluate(MEASURE)
        browser.close()

    data = {'width': args.width, 'picker': picker, 'runner': runner}
    (out / 'measure.json').write_text(json.dumps(data, indent=2))

    print(f"--- viewport {args.width}px ---")
    print('doc overflowX:', runner['docOverflowX'])
    for key in ('head', 'runtitles', 'serviceline', 'body'):
        b = runner[key]
        if b:
            print(f"{key:12} w={b['width']:7.1f} scroll={b['scrollWidth']:5} "
                  f"client={b['clientWidth']:5} over={b['overflowX']:5} "
                  f"wrap={b['overflowWrap']} lines={b['lines']}")
    for label, key in (('entry header', 'entryHeaders'), ('screen line', 'screenLines')):
        for b in runner[key]:
            print(f"{label:12} over={b['overflowX']:5} w={b['width']:7.1f} "
                  f"right={b['right']:7.1f} wrap={b['overflowWrap']:10} {b['text']!r}")
    print('wrote', out / 'measure.json')


if __name__ == '__main__':
    main()
