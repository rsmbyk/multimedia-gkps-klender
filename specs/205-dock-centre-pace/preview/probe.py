#!/usr/bin/env python3
"""Spec 205 — measure the dock's re-centring pace under FAST advancing.

The owner's report: advancing quickly in following mode makes the list bob up and
down, because each re-centre is still easing in when the next step retargets it.
This probe reproduces that on the LIVE dock and measures it, so a before/after is
numbers rather than adjectives.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python probe.py --url http://127.0.0.1:8765 --label after

Needs the fixture service "Ibadah Pace Probe" (60 one-screen TEXT entries, so every
ArrowDown crosses into the next entry — the hardest case) and a dev server serving
the code under test.

Sampling note: a persistent in-page rAF/setTimeout loop started via evaluate_handle
reads a FROZEN scrollTop in this headless Chromium (even a direct write is invisible
to it), while individual fresh `evaluate` reads are live. So every frame here is its
own fresh evaluate that sleeps in-page first, then reads — the only method that
observed the glide. See shots/*.json for the raw frames.
"""
from __future__ import annotations

import argparse
import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SERVICE = "Ibadah Pace Probe"

# One fresh read per call: sleep ms in-page (lets the glide's rAF run), THEN read in
# the resolving task — a new task each call, so the scroll offset is live.
FRAME = """(ms) => new Promise(res => setTimeout(() => {
  const body = document.getElementById('runBody');
  const row = document.querySelector('.screenerow[aria-current="true"]')
           || document.querySelector('.entryrow[aria-current="true"]');
  const b = body.getBoundingClientRect();
  const r = row ? row.getBoundingClientRect() : null;
  const off = r ? ((r.top + r.bottom) / 2) - ((b.top + b.bottom) / 2) : null;
  res([Math.round(performance.now() - window.__t0), Math.round(body.scrollTop),
       off === null ? null : Math.round(off)]);
}, ms))"""

NOW = "() => performance.now()"

PROJECT = """index => {
  const li = document.querySelector('.entryli[data-index="' + index + '"]');
  if (!li) return false;
  const row = li.querySelector('.entryrow');
  if (row && row.getAttribute('aria-expanded') !== 'true') row.click();
  const screen = li.querySelector('.screenerow');
  if (screen) screen.click();
  return !!screen;
}"""

MEASURE = """() => {
  const body = document.getElementById('runBody');
  const row = document.querySelector('.screenerow[aria-current="true"]')
           || document.querySelector('.entryrow[aria-current="true"]');
  const b = body.getBoundingClientRect();
  const r = row ? row.getBoundingClientRect() : null;
  return {
    scroll: Math.round(body.scrollTop),
    off: r ? Math.round(((r.top + r.bottom) / 2) - ((b.top + b.bottom) / 2)) : null,
    live: (document.querySelector('.entryli[data-live="true"]') || {dataset:{}}).dataset.index,
    overflow: body.scrollHeight - body.clientHeight,
    pressed: document.getElementById('centreBtn').getAttribute('aria-pressed'),
  };
}"""


def wait(page, ms):
    page.evaluate("(ms) => new Promise(r => setTimeout(r, ms))", ms)


def analyse(frames):
    scrolls = [f[1] for f in frames]
    offs = [f[2] for f in frames if f[2] is not None]
    reversals, last, biggest = 0, 0, 0
    for i in range(1, len(scrolls)):
        d = scrolls[i] - scrolls[i - 1]
        biggest = max(biggest, abs(d))
        if not d:
            continue
        sign = 1 if d > 0 else -1
        if last and sign != last:
            reversals += 1
        last = sign
    peak = max((abs(o) for o in offs), default=0)
    return reversals, biggest, peak


def settle_ms(frames, last_press_t):
    after = [f for f in frames if f[0] >= last_press_t and f[2] is not None]
    for i, f in enumerate(after):
        if abs(f[2]) < 2 and all(abs(g[2]) < 2 for g in after[i:i + 5]):
            return f[0] - last_press_t
    return None


def place(page, index=30):
    page.evaluate(PROJECT, index)
    wait(page, 650)
    page.evaluate("document.getElementById('centreBtn').click()")
    wait(page, 450)


def collect(page, ms, gap=8):
    """Fresh-read frames for ms of wall time (t0 already set in-page)."""
    frames = []
    target = page.evaluate(NOW) + ms
    while True:
        frames.append(page.evaluate(FRAME, gap))
        if page.evaluate(NOW) >= target:
            break
    return frames


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', default='http://127.0.0.1:8765')
    ap.add_argument('--label', default='run')
    ap.add_argument('--steps', type=int, default=12)
    ap.add_argument('--cadences', default='120,200,300')
    args = ap.parse_args()
    SHOTS.mkdir(exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={'width': 420, 'height': 900},
                                  device_scale_factor=1, color_scheme='dark')
        page = ctx.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(args.url + '/obs/dock', wait_until='domcontentloaded')
        page.wait_for_selector('.servicerow')
        page.locator(f'.servicerow[data-name="{SERVICE}"]').first.click()
        page.wait_for_selector('.entryrow')
        wait(page, 400)

        place(page)
        m = page.evaluate(MEASURE)
        print(json.dumps({'label': args.label, 'kind': 'setup', **m}))
        if m['overflow'] <= 0:
            print('FIXTURE DOES NOT SCROLL — measurements would be trivial')
            return 1

        # Single-move curve: scroll away (browsing), then one centre-control glide.
        page.locator('#runBody').hover()
        page.mouse.wheel(0, 20000)
        page.evaluate("document.getElementById('runBody').dispatchEvent(new WheelEvent('wheel',{bubbles:true}))")
        wait(page, 250)
        page.evaluate("window.__t0 = performance.now()")
        page.evaluate("document.getElementById('centreBtn').click()")
        frames = collect(page, 550)
        (SHOTS / f'{args.label}-single.json').write_text(json.dumps(frames))
        rev, big, peak = analyse(frames)
        steps = [abs(frames[i][1] - frames[i - 1][1]) for i in range(1, len(frames))
                 if frames[i][1] != frames[i - 1][1]]
        moving = [f[0] for f in frames if f[1] != frames[0][1]]
        dur = (moving[-1] - moving[0]) if moving else None
        print(json.dumps({'label': args.label, 'kind': 'single-move',
                          'frames': len(frames), 'reversals': rev, 'max_step': big,
                          'landing_off': frames[-1][2], 'move_ms': dur, 'steps_px': steps}))

        # Rapid advancing: the complaint. Every ArrowDown crosses into the next entry.
        for cad in [int(c) for c in args.cadences.split(',')]:
            place(page)
            page.evaluate("window.__t0 = performance.now()")
            frames = []
            for _ in range(args.steps):
                page.keyboard.press('ArrowDown')
                frames += collect(page, cad)
            last_press = frames[-1][0] if frames else 0
            frames += collect(page, 800)
            (SHOTS / f'{args.label}-{cad}.json').write_text(json.dumps(frames))
            rev, big, peak = analyse(frames)
            seq = [f for f in frames if f[0] < last_press and f[2] is not None]
            mean_off = round(sum(abs(f[2]) for f in seq) / len(seq), 1) if seq else None
            end = page.evaluate(MEASURE)
            print(json.dumps({'label': args.label, 'kind': 'rapid', 'cadence_ms': cad,
                              'steps': args.steps, 'frames': len(frames),
                              'reversals': rev, 'max_step': big, 'peak_off': peak,
                              'mean_off_seq': mean_off, 'settle_ms': settle_ms(frames, last_press),
                              'final_off': frames[-1][2], 'live_end': end['live']}))
        if errors:
            print(json.dumps({'label': args.label, 'kind': 'errors', 'errors': errors}))
        browser.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())