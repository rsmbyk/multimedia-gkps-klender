"""Read the corner cue while a Go To stands on a projector with no service.

Real code path: the projector's own G find, the shared display state, the detour.
Run against the slice worktree's server (default http://127.0.0.1:8765).

    python specs/227-goto-cue-empty-service/preview/probe.py --base http://127.0.0.1:8765
"""
import argparse
import json

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='http://127.0.0.1:8765')
    parser.add_argument('--query', default='Jahowa')
    args = parser.parse_args()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={'width': 420, 'height': 800})
        page = context.new_page()
        page.goto(args.base + '/projector')
        page.wait_for_function("() => window.GKPSProjectorLibrary"
                               " && window.GKPSProjectorLibrary.ready()")
        page.keyboard.press('g')
        page.wait_for_selector('#projectorFind:not([hidden])')
        page.fill('#projectorFindInput', args.query)
        page.wait_for_timeout(500)
        page.keyboard.press('Enter')
        page.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.goto); }")
        page.wait_for_selector('.projector-detour.is-active')
        readout = page.evaluate("""() => {
          const box = selector => {
            const el = document.querySelector(selector);
            if (!el) return null;
            const r = el.getBoundingClientRect();
            const round = n => Math.round(n * 10) / 10;
            return {x: round(r.x), y: round(r.y), w: round(r.width), h: round(r.height),
                    text: el.textContent.trim()};
          };
          return {
            cue: box('#corner-cue'),
            prefix: box('#cue-prefix'),
            flip: box('#cue-prefix .cue-translation'),
            baits: [...document.querySelectorAll('#cue-baits .cue-bait')]
              .map(el => el.textContent.trim()),
            back: box('#cue-next-name'),
            head: box('.projector-detour.is-active .screen__head')
          };
        }""")
        print(json.dumps(readout, indent=2, ensure_ascii=False))
        browser.close()


if __name__ == '__main__':
    main()
