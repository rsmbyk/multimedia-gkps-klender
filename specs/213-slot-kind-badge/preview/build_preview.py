"""Build the badge preview (spec 213) from the running slice server.

Copies the three real stylesheets beside the page and embeds the real `/tatib/151/`
stage markup, so every candidate is drawn by the product's own CSS against the real
rows. Re-run after any template or stylesheet change:

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/213-slot-kind-badge/preview/build_preview.py
"""
import pathlib
import re
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
SRC = REPO / 'static' / 'styles' / 'design'
BASE = 'http://127.0.0.1:8777'

CANDIDATES = [
    ('now', 'Now — no badge'),
    ('s11', 'A · 11px, inside the corner'),
    ('s13', 'B · 13px, overhanging'),
    ('s15', 'C · 15px, overhanging'),
]

# The badge, three sizes. `now` hides it. Each rule set is otherwise identical, so the
# only axis between A, B and C is the badge's box.
BADGE_CSS = """
/* the badge, drawn once; the candidates below only size and seat it */
#read .slot__mark .slot__badge {
  position: absolute; border-radius: 50%; display: grid; place-items: center;
  background: var(--canvas); color: var(--head-ink);
}
#read .slot__mark .slot__badge svg {
  width: 100%; height: 100%; fill: none; stroke: currentColor;
  stroke-linecap: round; stroke-linejoin: round;
}
[data-option="now"] #read .slot__mark .slot__badge { display: none; }

[data-option="s11"] #read .slot__mark .slot__badge {
  right: -2px; bottom: -2px; width: 11px; height: 11px;
}
[data-option="s11"] #read .slot__mark .slot__badge svg { width: 8.5px; height: 8.5px; stroke-width: 1.7; }

[data-option="s13"] #read .slot__mark .slot__badge {
  right: -4px; bottom: -3px; width: 13px; height: 13px;
}
[data-option="s13"] #read .slot__mark .slot__badge svg { width: 10px; height: 10px; stroke-width: 1.6; }

[data-option="s15"] #read .slot__mark .slot__badge {
  right: -5px; bottom: -4px; width: 15px; height: 15px;
}
[data-option="s15"] #read .slot__mark .slot__badge svg { width: 11.5px; height: 11.5px; stroke-width: 1.5; }
"""

PAGE_CSS = """
html, body { margin: 0; }
body { display: block; background: var(--canvas); color: var(--ink); font-family: var(--font-sans); }
.bar {
  position: sticky; top: 0; z-index: 40;
  display: flex; flex-wrap: wrap; align-items: center; gap: 6px;
  padding: 10px 16px;
  background: color-mix(in srgb, var(--rail-bg) 92%, var(--canvas));
  border-bottom: 1px solid var(--divider);
}
.bar button {
  padding: 7px 12px; border: 1px solid var(--divider); border-radius: 8px;
  background: var(--canvas); color: var(--ink);
  font: 600 12.5px/1 var(--font-sans); cursor: pointer;
}
.bar button[aria-pressed="true"] { background: var(--active-bg); color: var(--active-ink); border-color: var(--active-bg); }
.bar .note { margin-left: 6px; font: 500 12px/1.35 var(--font-sans); color: var(--head-ink); }
.bar .spacer { flex: 1; }
.cmp-stage { width: min(1040px, 100vw - 48px); margin: 0 auto; padding: 32px 0 120px; }
.read { display: block; }
.read__body { container: stage-pane / inline-size; }
/* the comparison page needs the row width a 400px pane gives */
.cmp-stage .read__body { width: 400px; }
.cmp-stage .tatib__item { margin-left: -10px; margin-right: -10px; }
/* a legend under the bar names the four kinds the page happens to carry */
.legend { display: flex; gap: 18px; flex-wrap: wrap; padding: 10px 16px 0;
  font: 500 12px/1.4 var(--font-sans); color: var(--head-ink); }
.legend b { color: var(--ink); font-weight: 600; }
"""

SCRIPT = """
(() => {
  const bar = document.querySelector('.bar');
  const note = document.getElementById('note');
  const set = (v) => {
    document.documentElement.dataset.option = v;
    bar.querySelectorAll('[data-opt]').forEach(b =>
      b.setAttribute('aria-pressed', String(b.dataset.opt === v)));
    note.textContent = document.querySelector(`[data-opt="${v}"]`).textContent;
  };
  bar.addEventListener('click', (e) => {
    const b = e.target.closest('[data-opt]');
    if (b) set(b.dataset.opt);
  });
  const theme = document.getElementById('theme');
  theme.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme === 'dark';
    document.documentElement.dataset.theme = dark ? 'light' : 'dark';
    theme.textContent = dark ? 'Dark' : 'Light';
  });
  const hover = document.getElementById('hover');
  hover.addEventListener('click', () => {
    const row = document.querySelectorAll('#read .tatib__item--slot')[1];
    row.classList.toggle('is-forced-hover');
    hover.setAttribute('aria-pressed', String(row.classList.contains('is-forced-hover')));
  });
})();
"""


def fetch_read():
    with urllib.request.urlopen(BASE + '/tatib/151/') as r:
        html = r.read().decode()
    m = re.search(r'<article class="read".*?</article>', html, re.S)
    if not m:
        raise SystemExit('no <article class="read"> in the served page')
    return m.group(0)


def main():
    # The three stylesheets are inlined rather than linked: the page has to render the same
    # way opened from disk, served, or shown in a chat frame, and a relative `assets/` link
    # is the one thing that can resolve differently in each.
    sheets = {name: (SRC / name).read_text() for name in
              ('tokens.css', 'components.css', 'generate.css')}

    article = fetch_read()
    kinds = re.findall(r'data-kind-badge="([^"]+)"', article)
    buttons = ''.join(
        f'<button type="button" data-opt="{v}" aria-pressed="{str(v == "s13").lower()}">{label}</button>'
        for v, label in CANDIDATES)
    legend = ('<div class="legend">'
              f'<span><b>{len(kinds)}</b> slot rows on this page</span>'
              '<span>kinds, in page order: <b>' + ', '.join(kinds) + '</b></span>'
              '<span>hover the second slot row to see the badge on the fill</span>'
              '</div>')

    head = """<!doctype html>
<html lang="id" data-read="on" data-option="s13" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Slot kind badge — candidates</title>
"""
    # the styles and the script carry braces, so they are concatenated rather than
    # interpolated: an f-string would read every `{` as a field.
    body_open = f"""<div class="bar" role="group" aria-label="Badge candidates">{buttons}
  <span class="note" id="note"></span><span class="spacer"></span>
  <button type="button" id="hover" aria-pressed="false">Hover a slot row</button>
  <button type="button" id="theme">Light</button>
</div>
{legend}
<div class="cmp-stage">
{article}
</div>
"""
    page = (head
            + '<style>\n' + sheets['tokens.css'] + '\n</style>\n'
            + '<style>\n' + sheets['components.css'] + '\n</style>\n'
            + '<style>\n' + sheets['generate.css'] + '\n</style>\n'
            + '<style>' + PAGE_CSS + '</style>\n'
            + '<style>' + BADGE_CSS + '</style>\n'
            + '<style>\n'
            + '/* the forced hover, for looking at the fill without holding the pointer still */\n'
            + '#read .tatib__item--slot.is-forced-hover { background: var(--icon-hover-bg); }\n'
            + '</style>\n</head>\n<body>\n'
            + body_open
            + '<script>' + SCRIPT + '</script>\n</body>\n</html>\n')
    (HERE / 'index.html').write_text(page)
    print('wrote', HERE / 'index.html', len(page), 'bytes;', len(kinds), 'badges')


if __name__ == '__main__':
    main()
