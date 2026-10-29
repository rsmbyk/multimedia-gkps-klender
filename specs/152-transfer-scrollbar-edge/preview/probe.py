"""Measure the two columns of `preview.html`: the list's box, and the bar's painted edges.

Headed Chromium only. The headless build on this machine paints overlay scrollbars: the list
reports 0px of scrollbar gutter and no thumb is drawn at all, so a headless run measures a surface
nobody sees. `--headless` is offered to show exactly that, not to verify the slice.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/152-transfer-scrollbar-edge/preview/probe.py

Each column is measured on its own pass, scrolled into view, so the page's own stacking (two columns
above 1260px, one below it) does not hide either state from the screenshot. Two positions are
measured, because the thumb has two ends to report: at rest its top meets the list's top edge, and
scrolled to the end its bottom meets the dialog's bottom border. Writes
`shots/<state>-<theme>-<viewport>-<column>-{top,end}.png` and prints one row per distance.
"""

import argparse
import base64
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE / "preview.html"
SHOTS = HERE / "shots"

MEASURE = r"""
(colId) => {
  const col = document.getElementById(colId);
  const dialog = col.querySelector('dialog');
  const list = col.querySelector('.media-transfers__list');
  const row = col.querySelector('.media-transfers__row');
  const title = dialog.querySelector('h2');
  const group = col.querySelector('.media-transfers__group');
  const d = dialog.getBoundingClientRect(), l = list.getBoundingClientRect();
  const r = row.getBoundingClientRect(), t = title.getBoundingClientRect();
  const g = group ? group.getBoundingClientRect() : null;
  const cs = getComputedStyle(dialog);
  return {
    dialog: {left: d.left, right: d.right, top: d.top, bottom: d.bottom, border: parseFloat(cs.borderRightWidth)},
    list: {left: l.left, right: l.right, top: l.top, bottom: l.bottom},
    bar: list.offsetWidth - list.clientWidth,
    scrolls: list.scrollHeight > list.clientHeight + 1,
    rowLeft: r.left - d.left,
    rowRight: d.right - r.right,
    titleLeft: t.left - d.left,
    groupLeft: g ? g.left - d.left : null,
    listBottomToDialogBottom: d.bottom - l.bottom,
    listRightInsideDialog: d.right - l.right,
    titleBottomToListTop: l.top - t.bottom
  };
}
"""

# Reads the painted pixels: the thumb's own colour per theme, the first column to its right that is
# neither thumb nor canvas (the dialog's border), and the thumb's two vertical ends.
PIXELS = r"""
async ({b64, column, thumb, canvas}) => {
  const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
  const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
  const g = c.getContext('2d'); g.drawImage(img, 0, 0);
  const dpr = img.width / innerWidth;
  const at = (cx, cy) => { const d = g.getImageData(Math.round(cx * dpr), Math.round(cy * dpr), 1, 1).data; return [d[0], d[1], d[2]]; };
  const near = (d, c, tol) => Math.abs(d[0]-c[0])<=tol && Math.abs(d[1]-c[1])<=tol && Math.abs(d[2]-c[2])<=tol;
  const {list, dialog} = column;
  const y0 = Math.ceil(list.top) + 2, y1 = Math.floor(list.bottom) - 2;
  /* The thumb is as long as the visible fraction of the list, so look for the column with the
     longest run of thumb-coloured pixels rather than for one that is coloured all the way down. */
  let best = null;
  for (let x = Math.floor(list.right); x >= Math.floor(list.right) - 12; x -= 1) {
    let run = 0, start = null, bestRun = 0, bestStart = null;
    for (let y = y0; y < y1; y += 1) {
      if (near(at(x + 0.5, y), thumb, 10)) {
        if (start === null) start = y;
        run += 1;
        if (run > bestRun) { bestRun = run; bestStart = start; }
      } else { start = null; run = 0; }
    }
    if (bestRun > 8 && (!best || bestRun > best.run)) best = {x, run: bestRun, start: bestStart};
  }
  if (!best) return {thumb: null, borderColumn: null, paintedGapToBorder: null,
                     thumbTopToDialog: null, thumbBottomToDialog: null};
  const scanY = best.start + Math.floor(best.run / 2);
  /* The thumb's own right edge on this row, then the first column that is neither thumb nor canvas. */
  let thumbRight = best.x;
  while (thumbRight + 1 <= Math.ceil(dialog.right) + 2 && near(at(thumbRight + 1.5, scanY), thumb, 10)) thumbRight += 1;
  let borderX = null;
  for (let x = thumbRight + 1; x <= Math.ceil(dialog.right) + 4; x += 1) {
    const d = at(x + 0.5, scanY);
    if (!near(d, canvas, 6) && !near(d, thumb, 10)) { borderX = x; break; }
  }
  const thumbBottom = best.start + best.run;                      // exclusive
  return {thumb: {x0: best.x, x1: thumbRight, run: best.run, start: best.start, bottom: thumbBottom, scanY},
          borderColumn: borderX,
          paintedGapToBorder: borderX === null ? null : borderX - thumbRight - 1,
          thumbTopToDialog: best.start - (dialog.top + dialog.border),
          thumbBottomToDialog: Math.round((dialog.bottom - dialog.border - thumbBottom) * 10) / 10};
}
"""


def measure_column(page, col, shot_path, thumb, canvas, where):
    page.evaluate("(id) => document.getElementById(id).scrollIntoView({block: 'center'})", col)
    page.evaluate("""([id, where]) => { const l = document.getElementById(id).querySelector('.media-transfers__list');
                      l.scrollTop = where === 'end' ? l.scrollHeight : 0; }""", [col, where])
    page.wait_for_timeout(180)
    data = page.evaluate(MEASURE, col)
    shot = page.screenshot()
    shot_path.write_bytes(shot)
    data['pixels'] = page.evaluate(PIXELS, {'b64': base64.b64encode(shot).decode(), 'column': data,
                                            'thumb': thumb, 'canvas': canvas})
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', default='15', choices=['15', '2'])
    ap.add_argument('--theme', default='light', choices=['light', 'dark'])
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--height', type=int, default=760)
    ap.add_argument('--headless', action='store_true', help='shows the overlay-scrollbar surface; not a verification')
    a = ap.parse_args()

    SHOTS.mkdir(exist_ok=True)
    name = f"rows{a.rows}-{a.theme}-{a.width}x{a.height}"
    thumb = {'light': [180, 176, 166], 'dark': [69, 65, 58]}[a.theme]
    canvas = {'light': [247, 245, 241], 'dark': [20, 19, 15]}[a.theme]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=a.headless)
        page = browser.new_page(viewport={'width': a.width, 'height': a.height})
        page.goto(PAGE.as_uri(), wait_until='load')
        if a.rows == '2':
            page.click('#rowsBtn')
        if a.theme == 'dark':
            page.click('#themeBtn')
        page.wait_for_timeout(250)
        results = {}
        for col in ('today', 'after'):
            results[col] = {
                'rest': measure_column(page, col, SHOTS / f'{name}-{col}-top.png', thumb, canvas, 'start'),
                'end': measure_column(page, col, SHOTS / f'{name}-{col}-end.png', thumb, canvas, 'end'),
            }
        browser.close()

    print(json.dumps({'state': name, 'columns': results}, indent=2))
    print()
    print(f"{'':48} {'today':>13} {'after':>13}")
    t, f = results['today'], results['after']
    fmt = lambda v: '—' if v is None else (f'{v:.1f}' if isinstance(v, float) else str(v))
    rows = [
        ('dialog border box right', t['rest']['dialog']['right'], f['rest']['dialog']['right']),
        ('list box right', t['rest']['list']['right'], f['rest']['list']['right']),
        ('list box bottom', t['rest']['list']['bottom'], f['rest']['list']['bottom']),
        ('bar lane (px)', t['rest']['bar'], f['rest']['bar']),
        ('scrolls', t['rest']['scrolls'], f['rest']['scrolls']),
        ('thumb column (at rest)', t['rest']['pixels']['thumb']['x0'] if t['rest']['pixels']['thumb'] else 'none',
         f['rest']['pixels']['thumb']['x0'] if f['rest']['pixels']['thumb'] else 'none'),
        ('canvas bar → right border (px)', t['rest']['pixels']['paintedGapToBorder'], f['rest']['pixels']['paintedGapToBorder']),
        ('thumb bottom → dialog bottom edge (px, scrolled to end)', t['end']['pixels']['thumbBottomToDialog'], f['end']['pixels']['thumbBottomToDialog']),
        ('list right inside dialog border box', t['rest']['listRightInsideDialog'], f['rest']['listRightInsideDialog']),
        ('list bottom inside dialog border box', t['rest']['listBottomToDialogBottom'], f['rest']['listBottomToDialogBottom']),
        ('row content left', t['rest']['rowLeft'], f['rest']['rowLeft']),
        ('row content right', t['rest']['rowRight'], f['rest']['rowRight']),
        ('title left', t['rest']['titleLeft'], f['rest']['titleLeft']),
        ('age heading left', t['rest']['groupLeft'], f['rest']['groupLeft']),
        ('title bottom → list top', t['rest']['titleBottomToListTop'], f['rest']['titleBottomToListTop']),
    ]
    for label, tv, fv in rows:
        print(f'{label:48} {fmt(tv):>13} {fmt(fv):>13}')
    print(f"\nshots: {SHOTS}/{name}-{{today,after}}-{{top,end}}.png")
    return 0


if __name__ == '__main__':
    sys.exit(main())
