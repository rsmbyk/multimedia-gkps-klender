"""Build the static preview for spec 224 from the live pages' real markup.

Run with the live preview server up:
    .venv/bin/python specs/224-empty-song-add-verse-row/preview/build.py

The page keeps the product's own markup and stylesheet; the three states are
captured read-body fragments from the live server. The proposed state is the
empty fragment with exactly the `.verse-add` row removed — the template delta
under review. No server is needed to open index.html afterwards.
"""
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = 'http://127.0.0.1:8770'
SOURCES = {
    'empty_current': '/songs/1731/',
    'with_verses': '/songs/1387/',
}
START = '<div class="read__body" id="readBody">'
END = '</div>\n </article>'


def body_fragment(html):
    a = html.index(START) + len(START)
    b = html.index(END, a)
    return html[a:b]


PLACEMENT_CSS = """
.read[data-kind="song"]:has(.entry__empty) { display:flex; flex-direction:column; min-height:100%; }
.read[data-kind="song"]:has(.entry__empty) .read__head { margin-bottom:0; }
.read[data-kind="song"] .read__body:has(> .entry__empty) {
  display:grid; grid-template-rows:minmax(min-content,50%); align-content:start;
  align-items:center; justify-items:center; flex:1; margin-top:0;
  padding-top:0; padding-bottom:0; container-type:inline-size;
}
"""


def main():
    pages = {k: urllib.request.urlopen(BASE + v).read().decode() for k, v in SOURCES.items()}
    empty = body_fragment(pages['empty_current'])
    proposed = empty.replace(
        re.search(r'\n<div class="verse-add">.*?</div>\n', empty, re.S).group(0), '\n')
    assert proposed != empty and proposed.count('data-add-verse') == 1
    fragments = {
        'before': empty,
        'after': proposed,
        'placed': proposed,
        'with_verses': body_fragment(pages['with_verses']),
    }
    shell = pages['empty_current']
    stored = '\n'.join(
        f'<script type="text/plain" id="state-{k}">{v}</script>' for k, v in fragments.items())
    shell = shell.replace(START + body_fragment(shell) + END,
                          START + fragments['after'] + END)
    shell = shell.replace('href="/static/', 'href="../../../_static/')
    shell = shell.replace('src="/static/', 'src="../../../_static/')
    toolbar = """<div id="state-bar" style="position:fixed;top:0;right:0;z-index:9999;background:#222;color:#fff;padding:8px 12px;font:13px sans-serif">
Preview state:
<button type="button" data-state="placed">empty — placed (proposed)</button>
<button type="button" data-state="after">empty — gate only</button>
<button type="button" data-state="before">empty — before (current)</button>
<button type="button" data-state="with_verses">three verses (unchanged)</button>
</div>
<script>
(function () {
  var body = document.getElementById('readBody');
  var placement = document.getElementById('placement-candidate');
  document.getElementById('state-bar').addEventListener('click', function (e) {
    var b = e.target.closest('button[data-state]');
    if (!b) return;
    body.innerHTML = document.getElementById('state-' + b.dataset.state).textContent;
    placement.disabled = b.dataset.state !== 'placed';
    history.replaceState(null, '', '#' + b.dataset.state);
  });
  var initial = location.hash.slice(1);
  if (document.getElementById('state-' + initial)) {
    body.innerHTML = document.getElementById('state-' + initial).textContent;
    document.getElementById('state-bar').querySelector('button[data-state="' + initial + '"]').click();
  } else {
    placement.disabled = false;
  }
})();
</script>"""
    placement_tag = '<style id="placement-candidate" disabled>' + PLACEMENT_CSS + '</style>'
    shell = shell.replace('</body>', toolbar + '\n</body>')
    out = HERE / 'index.html'
    out.write_text(shell.replace('</head>', stored + placement_tag + '\n</head>'))
    print('wrote', out, out.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
