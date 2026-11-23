"""Compare the projector cue before and after Back from a dock-started Go To.

Real code path: the dock's G find, the shared display state, the projector's detour,
then Back on the dock. Run against the slice worktree's server (default 8765).

    python specs/228-goto-cue-back-reset/preview/probe.py --base http://127.0.0.1:8765
"""
import argparse
import json

from playwright.sync_api import sync_playwright

READ = """() => {
  const cue = document.getElementById('corner-cue');
  return {
    goto: ((JSON.parse(localStorage.getItem('gkps-display') || 'null') || {}).goto || null),
    detour: !!document.querySelector('.projector-detour.is-active'),
    screens: document.querySelectorAll('.screen[data-screen]').length,
    text: cue.textContent.replace(/\\s+/g, ' ').trim(),
    prefix: (document.querySelector('#cue-prefix') || {}).textContent || '',
    flip: document.querySelectorAll('#cue-prefix .cue-translation').length,
    baits: document.querySelectorAll('#cue-baits .cue-bait').length,
    back: (document.querySelector('#cue-next-name') || {}).textContent || '',
    backHidden: document.getElementById('cue-next').hidden,
    visibility: getComputedStyle(cue).visibility,
    separatorDisplay: getComputedStyle(document.querySelector('.cue-separator')).display,
    zonePointerEvents: getComputedStyle(document.querySelector('.mouse-zone--next')).pointerEvents,
    cursorHidden: document.body.classList.contains('cursor-hidden'),
    bodyCursor: getComputedStyle(document.body).cursor,
    nextDisplay: getComputedStyle(document.getElementById('cue-next')).display,
    arrowBox: (r => ({w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10}))(
      document.getElementById('cue-arrow').getBoundingClientRect())
  };
}"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='http://127.0.0.1:8765')
    parser.add_argument('--query', default='Jahowa')
    args = parser.parse_args()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        dock = context.new_page()
        dock.goto(args.base + '/obs/dock')
        dock.wait_for_selector('.servicerow')
        dock.keyboard.press('g')
        dock.wait_for_selector('.bandswap.is-find')
        dock.wait_for_timeout(400)
        dock.fill('#findInput', args.query)
        dock.wait_for_timeout(400)
        dock.keyboard.press('Enter')
        dock.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.goto); }")
        dock.wait_for_timeout(500)

        projector = context.new_page()
        projector.goto(args.base + '/projector')
        projector.wait_for_function("() => window.GKPSProjectorLibrary"
                                    " && window.GKPSProjectorLibrary.ready()")
        projector.wait_for_timeout(500)
        during = projector.evaluate(READ)

        dock.locator('#offBack').click()
        dock.wait_for_function(
            "() => !((JSON.parse(localStorage.getItem('gkps-display') || 'null') || {}).goto)")
        projector.wait_for_timeout(500)
        after = projector.evaluate(READ)

        print(json.dumps({'during': during, 'after_back': after}, indent=2, ensure_ascii=False))
        browser.close()


if __name__ == '__main__':
    main()
