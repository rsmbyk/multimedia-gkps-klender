"""Spec 138 prototype builder — the drawer shell over the real pages.

Takes the pages this worktree's own server serves, strips their scripts (so the
page's own nav logic cannot fight the prototype), points the stylesheets at
`../../../static/`, and appends the proposal: `proto.css` and `proto.js`.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/138-sidebar-overlay-stack/preview/build_prototype.py [base]

Default base: `http://127.0.0.1:8772` (this worktree's `runserver`).
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8772').rstrip('/')
HERE = pathlib.Path(__file__).parent

PAGES = [
    ('tatib', '/tatib/149/'),
    ('songs', '/songs/1817/'),
]

# A clean start: the reading pane on, every level closed. The page's own scripts
# would have set these; the builder sets them because the scripts are gone.
START = """() => {
  document.querySelectorAll('script').forEach((node) => node.remove());
  const html = document.documentElement;
  html.dataset.read = 'on';
  html.dataset.nav = 'closed';
  html.dataset.ch = 'closed';
  html.dataset.rail = 'closed';
}"""


def build(page, name, path, css, js):
    page.goto(f'{BASE}{path}')
    page.wait_for_load_state('networkidle')
    page.evaluate(START)
    html = page.evaluate('document.documentElement.outerHTML')
    html = re.sub(r'(href|src)="/static/', r'\1="../../../static/', html)
    html = html.replace('</head>', f'<style>\n{css}\n</style>\n</head>')
    html = html.replace('</body>', f'<script>\n{js}\n</script>\n</body>')
    out = HERE / f'prototype-{name}.html'
    out.write_text(html, encoding='utf-8')
    return out


def main():
    css = (HERE / 'proto.css').read_text(encoding='utf-8')
    js = (HERE / 'proto.js').read_text(encoding='utf-8')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        for name, path in PAGES:
            out = build(page, name, path, css, js)
            print(f'{name:<6} {path:<20} {out.name}')
        browser.close()


if __name__ == '__main__':
    main()
