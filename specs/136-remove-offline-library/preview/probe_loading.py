"""Spec 136 preview probe — the numbers the spec's UI/UX section quotes.

Measures two things: the reading rail with and without the offline control (the live page from the
worktree's server, then the preview built from it), and the Go To's loading state in each of the
three projector previews (spinner sizes, its place beside the shortcuts button, the locked field).

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/136-remove-offline-library/preview/probe_loading.py [base]

Defaults: `http://127.0.0.1:8769`.
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8769').rstrip('/')
HERE = pathlib.Path(__file__).parent

RAIL = """() => {
  const foot = document.querySelector('.rail__foot');
  const buttons = [...(foot ? foot.querySelectorAll('button') : [])].map((b) => ({
    label: b.getAttribute('aria-label'), rect: b.getBoundingClientRect().toJSON(),
  }));
  return {
    railHeight: document.querySelector('.rail') ? document.querySelector('.rail').getBoundingClientRect().height : null,
    footHeight: foot ? foot.getBoundingClientRect().height : null,
    buttons,
    offlinePanel: !!document.querySelector('#offlineSyncPanel'),
    offlineLabel: !!document.querySelector('#offlineSavedSource'),
    offlineScripts: [...document.querySelectorAll('script[src]')].filter((s) => /offline/.test(s.src)).length,
    offlineStyle: [...document.querySelectorAll('link[rel=stylesheet]')].filter((l) => /offline\.css/.test(l.href)).length,
  };
}"""

PROJECTOR = """() => {
  const rect = (sel) => {
    const node = document.querySelector(sel);
    if (!node) return null;
    const box = node.getBoundingClientRect();
    const style = getComputedStyle(node);
    return {x: box.x, y: box.y, width: box.width, height: box.height,
            display: style.display, visibility: style.visibility,
            animation: style.animationName + ' ' + style.animationDuration};
  };
  const keys = document.querySelector('.keys');
  const cue = document.querySelector('.cue-loading');
  const row = document.querySelector('#projectorFindResults');
  const cell = document.querySelector('.projector-find__spinner');
  const input = document.querySelector('#projectorFindInput');
  return {
    panel: rect('#projectorFind'),
    row: rect('#projectorFindResults'),
    rowLoading: row ? row.classList.contains('is-loading') : null,
    cell: rect('.projector-find__spinner'),
    count: rect('.projector-find__count'),
    inputDisabled: input ? input.disabled : null,
    cue: rect('.cue-loading'),
    keys: rect('.keys'),
    gapToKeys: cue && keys ? keys.getBoundingClientRect().left - cue.getBoundingClientRect().right : null,
    centreDelta: cue && keys ? (cue.getBoundingClientRect().top + cue.getBoundingClientRect().height / 2)
      - (keys.getBoundingClientRect().top + keys.getBoundingClientRect().height / 2) : null,
  };
}"""


def main():
    report = {}
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(BASE + '/home/', wait_until='networkidle')
        report['reading_before'] = page.evaluate(RAIL)
        page.goto((HERE / 'after.html').as_uri(), wait_until='load')
        report['reading_after'] = page.evaluate(RAIL)
        page.screenshot(path=str(HERE / 'after-1440x900.png'), full_page=False)
        page.set_viewport_size({'width': 390, 'height': 844})
        report['reading_after_narrow'] = page.evaluate(RAIL)
        page.screenshot(path=str(HERE / 'after-390x844.png'), full_page=False)

        for name in ('projector-index-loading', 'projector-selection-loading',
                     'projector-selection-error', 'projector-chapter-loading'):
            page.set_viewport_size({'width': 1440, 'height': 900})
            page.goto((HERE / f'{name}.html').as_uri(), wait_until='load')
            page.wait_for_timeout(350)          # let the panel's 180ms entry animation settle
            report[name] = page.evaluate(PROJECTOR)
            page.screenshot(path=str(HERE / f'{name}.png'), full_page=False)

        # Reduced motion: the spinners must not spin.
        context = browser.new_context(reduced_motion='reduce', viewport={'width': 1440, 'height': 900})
        still = context.new_page()
        still.goto((HERE / 'projector-selection-loading.html').as_uri(), wait_until='load')
        report['reduced_motion'] = still.evaluate("() => [getComputedStyle(document.querySelector('.cue-loading')).animationName, getComputedStyle(document.querySelector('.projector-find__spinner')).animationName]")
        browser.close()
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
