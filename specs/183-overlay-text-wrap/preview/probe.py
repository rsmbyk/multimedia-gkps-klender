"""Measure the overlay's text wrap on the live page (slice 183).

    python specs/183-overlay-text-wrap/preview/probe.py --base http://127.0.0.1:8816 --out scratch/shots

Writes one JSON per run and a screenshot per case. `--normal` restores the one
declaration this slice adds, so the same script reads the before state from the after
tree (and vice versa).
"""

import argparse
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import screens  # noqa: E402  — the projector's own screen list

# entry index -> what it is (the screen is resolved from the service's own screen list)
CASES = [
    (0, 'text-long-word'),      # the report: a liturgy line with a 120-char run
    (1, 'text-pasted-url'),     # a speaker mark plus a 140-char URL
    (2, 'song-long-word'),      # the caption, 66-character run
    (3, 'passage-long-title'),  # a verse whose title is one long run
    (4, 'text-short'),          # control: short liturgy
    (5, 'text-untitled-short'),  # control: the smallest panel
    (6, 'text-long-kicker'),    # the plate's heading is a 64-character run
]

MEASURE = """(caseName) => {
  const stage = document.querySelector('.obs-overlay__stage');
  const plate = stage.querySelector('.obs-overlay__plate');
  const caption = stage.querySelector('.obs-overlay__caption');
  const root = plate || caption;
  const box = (el) => { const r = el.getBoundingClientRect();
    return {x: +r.x.toFixed(2), y: +r.y.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2)}; };
  const ink = (el) => {
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()];
    if (!rects.length) return null;
    return {left: +Math.min(...rects.map(r => r.left)).toFixed(2),
            right: +Math.max(...rects.map(r => r.right)).toFixed(2),
            lines: new Set(rects.map(r => Math.round(r.top))).size};
  };
  const spillOf = (el, limitRight) => {
    const i = ink(el); if (!i) return null;
    const r = el.getBoundingClientRect();
    return {inkRight: i.right, inkLeft: i.left, lines: i.lines,
            boxRight: +r.right.toFixed(2),
            spillBox: +(i.right - r.right).toFixed(2),
            spillLimit: +(i.right - limitRight).toFixed(2),
            spillLeft: +(r.left - i.left).toFixed(2)};
  };
  const wrapOf = (el) => { const s = getComputedStyle(el);
    return {overflowWrap: s.overflowWrap, wordBreak: s.wordBreak, whiteSpace: s.whiteSpace}; };
  const out = {case: caseName, stage: box(stage),
    root: plate ? 'plate' : 'caption', box: box(root),
    scrollWidth: root.scrollWidth, clientWidth: root.clientWidth,
    texts: {}};
  if (plate) {
    const pr = parseFloat(getComputedStyle(plate).paddingRight);
    const pl = parseFloat(getComputedStyle(plate).paddingLeft);
    const plateRight = plate.getBoundingClientRect().right;
    out.padding = {left: pl, right: pr};
    out.font = getComputedStyle(plate).fontSize;
    for (const sel of ['.obs-overlay__kicker', '.obs-overlay__title', '.obs-overlay__line']) {
      const el = plate.querySelector(sel); if (!el) continue;
      out.texts[sel] = {text: el.textContent.trim().slice(0, 40), box: box(el),
        wrap: wrapOf(el), ink: spillOf(el, plateRight)};
    }
  } else if (caption) {
    out.font = getComputedStyle(caption).fontSize;
    out.texts.caption = {text: caption.textContent.slice(0, 40), box: box(caption),
      wrap: wrapOf(caption), ink: spillOf(caption, caption.getBoundingClientRect().right)};
  }
  return out;
}"""

RESET = """() => {
  const stage = document.querySelector('.obs-overlay__stage');
  stage.querySelectorAll('*').forEach(el => {
    el.style.setProperty('overflow-wrap', 'normal', 'important');
  });
}"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='http://127.0.0.1:8816')
    parser.add_argument('--out', default='scratch/shots')
    parser.add_argument('--normal', action='store_true',
                        help='restore overflow-wrap: normal, i.e. the state before this slice')
    parser.add_argument('--size', default='1920x1080')
    parser.add_argument('--service', type=int, default=3)
    args = parser.parse_args()
    width, height = (int(n) for n in args.size.split('x'))
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    label = 'before' if args.normal else 'after'

    results = []
    screen_list = screens.screens(args.base, args.service)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': width, 'height': height},
                                      device_scale_factor=1)
        page = context.new_page()
        page.goto(args.base + '/obs/source/overlay')
        page.evaluate("""(service) => localStorage.setItem('gkps-display',
            JSON.stringify({service: service, screen: 0, on: true, translation: null}))""",
                      args.service)
        for entry_index, name in CASES:
            screen = screens.first_screen_of(screen_list, entry_index)
            page.evaluate("""([screen]) => localStorage.setItem('gkps-display',
                JSON.stringify({service: %d, screen: screen, on: true, translation: null}))"""
                          % args.service, [screen])
            page.reload()
            selector = '.obs-overlay__caption' if name.startswith('song') else '.obs-overlay__plate'
            page.wait_for_selector(selector)
            page.wait_for_timeout(350)          # the arrival animation settles
            if args.normal:
                page.evaluate(RESET)
                page.wait_for_timeout(60)
            data = page.evaluate(MEASURE, name)
            data['screen'] = screen
            data['entry'] = entry_index
            results.append(data)
            shot = out / f'{label}-{screen:02d}-{name}.png'
            page.screenshot(path=str(shot))
        browser.close()

    (out / f'{label}-{args.size}.json').write_text(json.dumps(results, indent=2))
    for row in results:
        line = [f"{row['screen']:>2} {row['case']:<20} {row['root']:<8} "
                f"box={row['box']['w']}x{row['box']['h']}"]
        for sel, t in row['texts'].items():
            i = t['ink']
            if i:
                line.append(f"{sel.split('__')[-1]} lines={i['lines']} "
                            f"spillBox={i['spillBox']} spillPlate={i['spillLimit']}")
        print(' | '.join(line))


if __name__ == '__main__':
    main()
