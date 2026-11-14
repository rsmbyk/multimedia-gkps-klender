"""Spec 135 preview builder — the Tata Ibadah sidebar with three-line rows.

Takes the real page the worktree's server serves at `/tatib/<id>/` (the code is
unchanged), strips its scripts so nothing rewrites the panel, re-marks every
contents row into the proposed single clamped block, appends two fixture rows for
the cases the live service does not carry, and writes `preview/after.html` with
the stylesheets pointed at the repository's own files.

The shell, the panel, the type, the colours and every row's text are the
project's; only the row's inner markup and the clamp rule are the proposal.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/135-tatib-sidebar-row-clamp/preview/build_preview.py [url] [service]

Defaults: `http://127.0.0.1:8769`, `/tatib/144/`.
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8769').rstrip('/')
SERVICE = sys.argv[2] if len(sys.argv) > 2 else '/tatib/144/'
HERE = pathlib.Path(__file__).parent

# The proposal, in the order it would sit in components.css: one clamped box per
# row label, its lines separated by a <br>, an ellipsis when the box overflows.
PROPOSAL = """
/* --- spec 135 preview: a contents row is three lines, ellipsized --- */
.songrow__t {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  overflow-wrap: anywhere;
  min-width: 0;
}
.songrow__t--lines,
.songrow__t--song { display: -webkit-box; }
/* A song that has a Bait line spends at most two lines on its heading, so the
   Bait line is always drawn as the third. No <br> between them: the heading and
   the Bait line are the box's own items. */
.songrow__t--song:has(.songrow__verses) .songrow__heading {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}
.songrow__line--blank { min-height: 0; }
"""

REMARK = """() => {
  const list = document.querySelector('#chList');
  if (!list) return 0;
  let changed = 0;
  [...list.querySelectorAll('li')].forEach((li) => {
    const t = li.querySelector('.songrow__t');
    if (!t) return;
    if (t.classList.contains('songrow__t--song')) {
      const heading = t.querySelector('.songrow__heading');
      const verses = t.querySelector('.songrow__verses');
      t.innerHTML = '';
      if (heading) t.appendChild(heading);
      if (verses) t.appendChild(verses);      // its own item: no <br>, no extra line
      changed++;
    } else if (t.classList.contains('songrow__t--lines')) {
      const lines = [...t.querySelectorAll('.songrow__line')];
      t.classList.remove('songrow__t--lines');
      t.innerHTML = '';
      lines.forEach((line, i) => {
        if (i) t.appendChild(document.createElement('br'));
        t.appendChild(document.createTextNode(line.textContent.replace(/\\u00a0/g, ' ').trim()));
      });
      changed++;
    }
  });
  return changed;
}"""

# Two rows the live service does not carry: a body that overflows three lines,
# and a 64-character title. Both are marked so the reviewer can tell them apart.
FIXTURES = """(rows) => {
  const list = document.querySelector('#chList');
  const n = list.querySelectorAll('li').length;
  rows.forEach((row, i) => {
    const li = document.createElement('li');
    li.dataset.fixture = '1';
    li.dataset.num = String(n + i + 1);
    const a = document.createElement('a');
    a.className = 'songrow';
    a.href = '#';
    a.dataset.i = 'fixture-' + (i + 1);
    const c = document.createElement('span');
    c.className = 'songrow__c';
    c.textContent = String(n + i + 1);
    const t = document.createElement('span');
    t.className = 'songrow__t';
    row.forEach((line, j) => {
      if (j) t.appendChild(document.createElement('br'));
      t.appendChild(document.createTextNode(line));
    });
    a.appendChild(c);
    a.appendChild(t);
    li.appendChild(a);
    list.appendChild(li);
  });
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(f'{BASE}{SERVICE}')
        page.wait_for_selector('#chList li', state='attached')

        # Keep the shell, drop the scripts that would rewrite the panel, and open
        # both sidebars so the contents list is on screen in a static file.
        page.evaluate("""() => {
          document.querySelectorAll('script').forEach((s) => s.remove());
          const html = document.documentElement;
          html.dataset.nav = 'open';
          html.dataset.ch = 'open';
          html.dataset.read = 'on';
        }""")
        changed = page.evaluate(REMARK)
        page.evaluate(FIXTURES, [
            # an untitled text body of six lines: the server keeps the first three
            # and marks the cut, exactly as the spec requires
            ['Nyanyian Pembuka', 'Jemaat menyanyikan bait pertama bersama-sama',
             'Liturgis membacakan ayat kedua sebelum doa pembuka\u2026'],
            # a 64-character title, the column's own limit: it fits in three lines
            # and must not be cut at sixty
            ['606. Saudara, Mari Kita Menyanyikan Pujian bagi Tuhan yang Setia'],
        ])
        page.wait_for_timeout(150)
        html = page.evaluate('document.documentElement.outerHTML')
        browser.close()

    html = re.sub(r'href="/static/', 'href="../../../static/', html)
    html = re.sub(r'src="/static/', 'src="../../../static/', html)
    html = html.replace('</head>', f'<style>{PROPOSAL}</style>\n</head>')
    (HERE / 'after.html').write_text(html, encoding='utf-8')
    print(f're-marked {changed} rows; wrote {HERE / "after.html"}')


if __name__ == '__main__':
    main()
