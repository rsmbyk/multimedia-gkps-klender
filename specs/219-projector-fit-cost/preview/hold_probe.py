"""Hold the arrow key down and watch how many screens are painted at once.

A real key hold sends a keydown roughly every 30 ms. Each one advances the projector, and
each advance starts a crossfade that lasts 240 ms -- so if the crossfade is not finished
when the next advance arrives, the previous ones are still part-faded and their words
overlap the new screen's. This counts, per frame, how many screens have any opacity, and
saves the worst frame.

    <venv>/bin/python specs/219-projector-fit-cost/preview/hold_probe.py \
        --url http://127.0.0.1:8791 --service 144 --out shots
"""
import argparse
import json
import pathlib
import time

from playwright.sync_api import sync_playwright

RECORDER = """() => {
  const screens = [...document.querySelectorAll('#projectorScreens .screen[data-screen]')];
  window.__hold = {frames: 0, worst: 0, samples: []};
  function frame() {
    const visible = screens.map((el) => parseFloat(getComputedStyle(el).opacity))
                           .filter((o) => o > 0.02);
    const state = window.__hold;
    state.frames += 1;
    state.worst = Math.max(state.worst, visible.length);
    if (visible.length > 1) {
      state.samples.push({screen: Number(document.body.dataset.currentScreen),
                          visible: visible.map((o) => +o.toFixed(2))});
    }
    if (state.frames < 240) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  return 'recording';
}"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:8791')
    parser.add_argument('--service', default='144')
    parser.add_argument('--out', default='')
    args = parser.parse_args()

    out = pathlib.Path(args.out or '.').resolve()
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(f'{args.url}/projector?service={args.service}')
        page.wait_for_load_state('networkidle')
        page.wait_for_selector('.screen.is-active')
        page.evaluate("() => document.dispatchEvent("
                      "new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}))")
        page.wait_for_timeout(600)                 # the display is on, first screen settled
        page.evaluate(RECORDER)
        client = page.context.new_cdp_session(page)
        # A held key repeats itself about every 35 ms; Playwright's keyboard.down() fires one
        # keydown and stops, so the repeats are sent as the browser's own autoRepeat events.
        for _ in range(34):
            client.send('Input.dispatchKeyEvent', {
                'type': 'keyDown', 'key': 'ArrowRight', 'code': 'ArrowRight',
                'windowsVirtualKeyCode': 39, 'nativeVirtualKeyCode': 39, 'autoRepeat': True})
            page.wait_for_timeout(35)
        page.screenshot(path=str(out / 'held-arrow.png'))
        page.wait_for_timeout(500)
        report = json.loads(page.evaluate('() => JSON.stringify(window.__hold)'))
        browser.close()

    print(f'frames recorded {report["frames"]}  screens painted at once, worst frame '
          f'{report["worst"]}')
    for sample in report['samples'][:8]:
        print(f'  at screen {sample["screen"]}: opacities {sample["visible"]}')
    print(f'frames with more than one screen painted: {len(report["samples"])}')
    print(f'screenshot {out / "held-arrow.png"}')


if __name__ == '__main__':
    main()
