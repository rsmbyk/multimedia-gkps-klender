"""Build the static preview for slice 162 from the project's own rendered form.

The fragment is fetched from the running app (unmodified code), so the markup,
class names and labels are the product's own; this script only swaps the one
summary line (and adds the checked verses the script would draw) to show each
state as it would be.

    python specs/162-song-verse-empty-state/preview/build_preview.py

`--fragment path` reads a saved fragment instead of fetching one.
"""

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
URL = 'http://127.0.0.1:8842/editor/entry/new/?kind=song&tatib=149'

VERSE_ROW = ('<div><label class="editor__verse"><input type="checkbox" name="verses" '
             'value="{n}" checked> <span>{n}</span></label></div>')

STATES = [
    {
        'id': 'no-song',
        'title': 'No song picked',
        'reach': 'open New song — nothing else',
        'song_label': 'Choose a song',
        'verses': [],
        'today': ('Pick a song first', True, None),
        'proposed': ('Pick a song first', True, None),
    },
    {
        'id': 'song-with-verses',
        'title': 'A song with verses — KJ 152',
        'reach': 'pick KJ 152 Ada Kuasa',
        'song_label': 'KJ 152 Ada Kuasa',
        'verses': [1, 2, 3],
        'today': ('All verses', False, None),
        'proposed': ('All verses', False, None),
    },
    {
        'id': 'song-without-verses',
        'title': 'A song with no verses — lagu kosong',
        'reach': 'pick lagu kosong (no verse stored)',
        'song_label': 'lagu kosong',
        'verses': [],
        'today': ('Pick a song first', True, None),
        'proposed': ('This song has no verses', True, None),
    },
    {
        'id': 'save-refusal',
        'title': 'Save pressed on that song',
        'reach': 'pick lagu kosong, press Save',
        'song_label': 'lagu kosong',
        'verses': [],
        'today': ('Pick a song first', True,
                  'Keep at least one verse in the service.'),
        'proposed': ('This song has no verses', True,
                     'This song has no verses: pick another song.'),
    },
]


def fetch_fragment() -> str:
    import urllib.request
    with urllib.request.urlopen(URL) as response:
        return response.read().decode()


def panel(fragment: str, state: dict, which: str) -> str:
    text, disabled, error = state[which]
    song_label = state['song_label']
    verses = state['verses']
    html = fragment
    html = re.sub(r'(<span data-picker-label>).*?(</span>)',
                  lambda m: m.group(1) + song_label + m.group(2), html, count=1)
    html = re.sub(r'(<span data-verses-summary>).*?(</span>)',
                  lambda m: m.group(1) + text + m.group(2), html, count=1)
    if disabled:
        html = html.replace('data-verses-trigger aria-haspopup="true"',
                            'data-verses-trigger disabled aria-haspopup="true"', 1)
    boxes = ''.join(VERSE_ROW.format(n=n) for n in verses)
    html = re.sub(r'(<div id="id_verses">\s*</div>)',
                  '<div id="id_verses">' + boxes + '</div>', html)
    if error:
        html = html.replace(
            '</div>\n    \n  </div>\n\n  \n',
            '</div>\n    <p class="editor__error" role="alert">' + error + '</p>\n  </div>\n\n  \n')
    return (f'<div class="editor preview-sheet" open data-state="{state["id"]}">'
            f'{html}</div>')


def build(fragment: str) -> str:
    rows = []
    for state in STATES:
        rows.append(f"""
    <section class="preview-row" data-state="{state['id']}">
      <header>
        <h2>{state['title']}</h2>
        <p>Reach it: {state['reach']}</p>
      </header>
      <div class="preview-pair">
        <figure>
          <figcaption>Today</figcaption>
          {panel(fragment, state, 'today')}
        </figure>
        <figure>
          <figcaption>Proposed</figcaption>
          {panel(fragment, state, 'proposed')}
        </figure>
      </div>
    </section>""")
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Preview — a song with no verses is named (slice 162)</title>
<link rel="stylesheet" href="../../../static/styles/design/tokens.css">
<link rel="stylesheet" href="../../../static/styles/design/components.css">
<style>
  /* Preview chrome only. Nothing here is product style: the sheets below are the
     real dialog (`.editor`) and the real form fragment, laid out side by side
     instead of stacked as fixed-position dialogs. */
  body {{ margin: 0; padding: 28px 32px 60px; background: var(--canvas); color: var(--ink);
         font-family: var(--font-ui, system-ui, sans-serif); display: block; }}
  h1 {{ font-size: 19px; margin: 0 0 6px; }}
  .preview-lede {{ margin: 0 0 26px; color: var(--head-ink); font-size: 14px; max-width: 74ch; }}
  .preview-row {{ border-top: 1px solid var(--divider); padding: 20px 0 26px; }}
  .preview-row > header h2 {{ font-size: 15px; margin: 0; }}
  .preview-row > header p {{ margin: 2px 0 14px; font-size: 13px; color: var(--head-ink); }}
  .preview-pair {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px;
                   align-items: start; }}
  .preview-pair figure {{ margin: 0; }}
  .preview-pair figcaption {{ font-size: 12px; letter-spacing: .04em; text-transform: uppercase;
                              color: var(--head-ink); margin-bottom: 8px; }}
  .preview-sheet {{ position: static; width: min(30rem, 100%); max-height: none; }}
  .preview-sheet[data-state="song-without-verses"] .editor__picker-trigger[disabled],
  .preview-sheet[data-state="save-refusal"] .editor__picker-trigger[disabled] {{ opacity: 1; }}
  @media (max-width: 860px) {{ .preview-pair {{ grid-template-columns: minmax(0, 1fr); }} }}
</style>
</head>
<body>
  <h1>A song with no verses is named, not mistaken for no song</h1>
  <p class="preview-lede">Slice 162 · static preview built from the app's own rendered form
  (<code>/editor/entry/new/?kind=song&amp;tatib=149</code>) and its own stylesheets. Compare the
  <strong>Verses</strong> field in each pair. The dialog is laid out inline here; in the product it
  is the same <code>&lt;dialog class="editor"&gt;</code>.</p>
  {''.join(rows)}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--fragment', help='a saved fragment file instead of a live fetch')
    args = parser.parse_args()
    fragment = (pathlib.Path(args.fragment).read_text()
                if args.fragment else fetch_fragment())
    out = HERE / 'preview.html'
    out.write_text(build(fragment))
    print(f'wrote {out} ({out.stat().st_size} bytes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
