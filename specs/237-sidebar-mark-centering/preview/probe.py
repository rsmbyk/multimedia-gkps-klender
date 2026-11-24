"""Measure spec 237 on the live worktree server. Needs the venv's Playwright."""
import json

from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:8776/tatib/151/'
CHROME = '/usr/bin/google-chrome'

MEASURE = """(before) => {
  const rows = [...document.querySelectorAll('#chList a.songrow')].map(a => {
    const n = a.querySelector('.songrow__c'), m = a.querySelector('.songrow__mark');
    const t = a.querySelector('.songrow__t'), r = a.getBoundingClientRect();
    if (m) m.style.alignSelf = before ? 'baseline' : '';
    const mb = m && m.getBoundingClientRect(), nb = n.getBoundingClientRect();
    const tb = t.getBoundingClientRect();
    const badge = a.querySelector('.slot__badge');
    const bb = badge && badge.getBoundingClientRect();
    const centre = b => +(b.top + b.height / 2 - r.top - r.height / 2).toFixed(2);
    return {kind: m ? m.dataset.mark : null,
            rowH: +r.height.toFixed(2),
            number: centre(nb), mark: mb ? centre(mb) : null,
            markX: mb ? +(mb.left - r.left).toFixed(2) : null,
            labelX: +(tb.left - r.left).toFixed(2),
            badgeBottom: bb ? +(r.bottom - bb.bottom).toFixed(2) : null,
            align: m ? getComputedStyle(m).alignSelf : null};
  });
  return {pane: +document.querySelector('#chList').getBoundingClientRect().width.toFixed(2),
          rows};
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        try:
            for width in (1440, 1024, 390):
                page = browser.new_page(viewport={'width': width, 'height': 900},
                                        device_scale_factor=1)
                page.goto(URL)
                page.wait_for_load_state('networkidle')
                for theme in ('light', 'dark'):
                    page.evaluate('(t) => document.documentElement.dataset.theme = t', theme)
                    print(f'=== {width}px {theme} ===')
                    for mode in (True, False):
                        data = page.evaluate(MEASURE, mode)
                        print(('before' if mode else 'after ') + ' ' + json.dumps(data))
                page.close()
        finally:
            browser.close()


if __name__ == '__main__':
    main()
