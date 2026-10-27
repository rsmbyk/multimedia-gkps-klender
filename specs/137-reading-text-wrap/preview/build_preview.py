"""Spec 137 preview builder — a reading page's text wraps at its pane.

Takes the real pages the worktree's own server serves, drops the scripts so
nothing rewrites them, opens the shell's panels, adds a fixture where the live
data has no long value to show, and writes two files per page:

    after-<name>.html    the worktree as it stands — the rule in components.css
    before-<name>.html   the same page with the rule's one declaration restored to
                         today's value, so the before and after are a one-property
                         comparison and not two different builds

Everything else is the project's own: shell, rail, panels, stage, type, colours,
tokens and stylesheets, pointing at `../../../static/`.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/137-reading-text-wrap/preview/build_preview.py [base]

Default base: `http://127.0.0.1:8768` (this worktree's `runserver`).
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8768').rstrip('/')
HERE = pathlib.Path(__file__).parent

# Today's value for the one declaration the slice adds, so `before-*` is the page as
# it renders on develop rather than a second, separately-built page.
BEFORE = """
/* --- spec 137 preview: the page as it renders before the slice --- */
.read, .search-results, .preview { overflow-wrap: normal; }
"""

OPEN_SHELL = """(openRead) => {
  document.querySelectorAll('script').forEach((s) => s.remove());
  const html = document.documentElement;
  html.dataset.nav = 'open';
  html.dataset.ch = 'open';
  html.dataset.read = openRead ? 'on' : 'off';
}"""

# Where the live data has no long value, one fixture carries the case. Every fixture is
# marked `data-fixture="1"` so a reviewer can tell the project's text from the builder's.
FIXTURES = {
    # a Bible pericope heading and a verse, both one unbroken run
    'bible': """() => {
      const sec = document.querySelector('.read__sec');
      if (sec) { sec.dataset.fixture = '1'; sec.textContent = 'PembagianTanahDanPerjanjianYangKekalBagiSeluruhSukuBangsaIsraelDiTanahPerjanjian'; }
      const v = document.querySelector('.v');
      if (v) {
        const span = v.querySelector('span:last-child');
        if (span) { span.dataset.fixture = '1'; span.textContent = 'https://drive.google.com/drive/folders/18A0dI3cwJxzSGTxim3ENlj4GwrB2Yatd'; }
      }
    }""",
    # one search result row whose title and meta are unbroken runs
    'search': """() => {
      const row = document.querySelector('.result-row');
      if (!row) return;
      row.dataset.fixture = '1';
      const title = row.querySelector('.result-row__title');
      const meta = row.querySelector('.result-row__meta');
      if (title) title.textContent = 'PembagianTanahDanPerjanjianYangKekalBagiSeluruhSukuBangsaIsraelDiTanahPerjanjianYangDijanjikanKepadaAbrahamIshakDanYakubBesertaSeluruhKeturunannya';
      if (meta) meta.textContent = 'https://drive.google.com/drive/folders/18A0dI3cwJxzSGTxim3ENlj4GwrB2Yatd';
    }""",
}

PAGES = [
    ('tatib', '/tatib/149/', None, True, 'Tata Ibadah service whose title and body are unbroken runs'),
    ('songs', '/songs/1817/', None, True, 'Song whose title is one unbroken run'),
    ('bible', '/bible/1/1/', FIXTURES['bible'], True, 'Bible chapter: pericope heading and verse fixture'),
    ('search', '/search?q=ibadah', FIXTURES['search'], False, 'Search results: first row replaced by fixtures'),
]


def snapshot(page, path, extra_style, fixture, open_read):
    page.goto(f'{BASE}{path}')
    page.wait_for_timeout(200)
    page.evaluate(OPEN_SHELL, open_read)
    if fixture:
        page.evaluate(fixture)
    page.wait_for_timeout(120)
    html = page.evaluate('document.documentElement.outerHTML')
    html = re.sub(r'(href|src)="/static/', r'\1="../../../static/', html)
    if extra_style:
        html = html.replace('</head>', f'<style>{extra_style}</style>\n</head>')
    return html


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        for name, path, fixture, open_read, note in PAGES:
            before = snapshot(page, path, BEFORE, fixture, open_read)
            after = snapshot(page, path, None, fixture, open_read)
            (HERE / f'before-{name}.html').write_text(before, encoding='utf-8')
            (HERE / f'after-{name}.html').write_text(after, encoding='utf-8')
            print(f'{name:<7} {path:<20} {note}')
        browser.close()


if __name__ == '__main__':
    main()
