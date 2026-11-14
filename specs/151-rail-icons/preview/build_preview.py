#!/usr/bin/env python3
"""Build the rail-icon proposal preview (spec 151).

The markup is the live page's own — the rail and the Tata Ibadah stage are lifted
from the running app's server-rendered HTML — and the stylesheets are frozen at the
commit this slice branched from, so the "Now" column keeps showing today's marks
while the proposal is drawn over a live copy of the same DOM.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/151-rail-icons/preview/build_preview.py [--url URL]

Reads   http://127.0.0.1:63404/tatib/144/   (the compose web container, on develop)
Writes  preview.html + assets/{tokens,components}.css next to this file
"""
import argparse
import pathlib
import re
import shutil
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
FROZEN_AT = "24a6d6d2"          # develop, the commit this slice branched from
DEFAULT_URL = "http://127.0.0.1:63404/tatib/144/"

# --- the candidates -------------------------------------------------------
# Every path is drawn on the 24-unit grid the rail already uses; the rail paints
# them at 24px with stroke 1.7, the entry kind mark at 20px with stroke 1.8.
GLYPHS = {
    "bible": {
        "closed": ('<path d="M5 4.4c0-1 .8-1.8 1.8-1.8h10.4c1 0 1.8.8 1.8 1.8v15.4c0 1-.8 1.8-1.8 1.8H6.8'
                   'c-1 0-1.8-.8-1.8-1.8z"/><path d="M8 2.6v18.8"/>'
                   '<path d="M13.2 7.1v6.4M11.2 9.5h4"/>'),
        "open": ('<path d="M12 9.6c-1.6-1.3-3.8-1.9-6.9-1.7v10.4c3.1-.2 5.3.4 6.9 1.7 1.6-1.3 3.8-1.9 '
                 '6.9-1.7V7.9c-3.1-.2-5.3.4-6.9 1.7z"/><path d="M12 9.6v10.4"/>'
                 '<path d="M12 2.6v4.6M10.1 4.5h3.8"/>'),
    },
    "tatib": {
        "clipboard": ('<rect x="4.6" y="3.4" width="14.8" height="17.2" rx="2"/>'
                      '<rect x="8.6" y="1.9" width="6.8" height="3.4" rx="1.4"/>'
                      '<path d="M8.2 9.6h7.6M8.2 13h7.6M8.2 16.4h4.8"/>'),
        "steps": ('<path d="M6.4 4.2v15.6"/><circle cx="6.4" cy="6.2" r="1.5"/>'
                  '<circle cx="6.4" cy="12" r="1.5"/><circle cx="6.4" cy="17.8" r="1.5"/>'
                  '<path d="M10.6 6.2h9M10.6 12h6.6M10.6 17.8h9"/>'),
    },
    "song": {
        "pair": ('<path d="M9 17.4V5.6l10.2-2v11.6"/>'
                 '<circle cx="6.7" cy="17.4" r="2.4"/><circle cx="16.9" cy="15.2" r="2.4"/>'),
        "single": ('<path d="M10.9 17.4V5.9c0-.5.3-.9.8-1l6.1-1.3"/>'
                   '<path d="M10.9 5.9c3 .8 4.6 2.7 4.4 5.5"/>'
                   '<ellipse cx="8.4" cy="17.3" rx="2.5" ry="2.1"/>'),
    },
    "audio": {
        "waveform": '<path d="M3.6 10.2v3.6M7.2 7.2v9.6M10.8 4.4v15.2M14.4 7.2v9.6M18 10.2v3.6"/>',
        "speaker": ('<path d="M4.6 9.2h3.2L12.4 5v14L7.8 14.8H4.6z"/>'
                    '<path d="M15.6 9.2a4 4 0 0 1 0 5.6M18 6.8a7.6 7.6 0 0 1 0 10.4"/>'),
        # today's audio mark, for the "Now" column and the before/after difference
        "now": ('<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/>'
                '<circle cx="17" cy="16" r="3"/>'),
    },
}

for name in ("tokens.css", "components.css"):
    blob = subprocess.run(["git", "-C", str(REPO), "show", f"{FROZEN_AT}:static/styles/design/{name}"],
                          capture_output=True, check=True).stdout
    (HERE / "assets").mkdir(exist_ok=True)
    (HERE / "assets" / name).write_bytes(blob)

# The other media families keep the marks they ship with; only audio moves.
STAGE_JS = (REPO / "static" / "web" / "media-stage.js").read_text()
FAMILY = dict(re.findall(r"^\s+(\w+): '(<(?:path|rect)[^']*>)',$", STAGE_JS, re.M))
assert {"image", "video", "pdf", "slides"} <= set(FAMILY), FAMILY

parser = argparse.ArgumentParser()
parser.add_argument("--url", default=DEFAULT_URL)
url = parser.parse_args().url
html_page = subprocess.run(["curl", "-s", url], capture_output=True, text=True, check=True).stdout

rail_match = re.search(r'<aside class="rail".*?</aside>', html_page, re.S)
article_match = re.search(r'<article class="read" id="read".*?</article>', html_page, re.S)
assert rail_match and article_match, "the live page did not render a rail and a stage"
rail, article = rail_match.group(0), article_match.group(0)
# The page is opened from this folder, so the one server asset it draws (the rail's logo) is
# copied beside it rather than fetched through a /static route the folder does not have.
(HERE / "assets").mkdir(exist_ok=True)
shutil.copy2(REPO / "static" / "assets" / "gkps.png", HERE / "assets" / "gkps.png")
rail = rail.replace('"/static/assets/', '"assets/')
article = article.replace('"/static/assets/', '"assets/')

page = f"""<!doctype html>
<html lang="id" data-read="on">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rail icons — proposal (spec 151)</title>
<link rel="stylesheet" href="assets/tokens.css">
<link rel="stylesheet" href="assets/components.css">
<style>
  html, body {{ margin: 0; height: auto; }}
  body {{ display: block; background: var(--canvas); color: var(--ink); font-family: var(--font-sans); }}
  .bar {{
    position: sticky; top: 0; z-index: 60;
    display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px;
    padding: 10px 18px; border-bottom: 1px solid var(--divider);
    background: color-mix(in srgb, var(--rail-bg) 94%, var(--canvas));
  }}
  .bar h1 {{ margin: 0; font: 650 14px/1.2 var(--font-sans); letter-spacing: -.01em; }}
  .bar .sub {{ color: var(--head-ink); font: 500 12px/1.3 var(--font-sans); }}
  .bar .grow {{ flex: 1; }}
  .grp {{ display: flex; align-items: center; gap: 5px; }}
  .grp span {{ color: var(--head-ink); font: 600 11px/1 var(--font-sans); text-transform: uppercase; letter-spacing: .07em; }}
  .grp button, .bar > button {{
    padding: 6px 10px; border: 1px solid var(--divider); border-radius: 7px;
    background: var(--canvas); color: var(--ink); font: 600 12px/1 var(--font-sans); cursor: pointer;
  }}
  .grp button[aria-pressed="true"] {{ background: var(--active-bg); color: var(--active-ink); border-color: var(--active-bg); }}
  .split {{ width: 1px; height: 22px; background: var(--divider); margin: 0 2px; }}

  .wrap {{ padding: 26px 26px 90px; }}
  .demos {{ display: flex; gap: 30px; align-items: flex-start; flex-wrap: wrap; }}
  figure.demo {{ margin: 0; }}
  figure.demo figcaption {{
    margin: 0 0 9px; font: 650 12px/1 var(--font-sans); letter-spacing: .08em;
    text-transform: uppercase; color: var(--head-ink);
  }}
  figure.demo figcaption small {{ margin-left: 8px; font: 500 11px/1 var(--font-sans);
    letter-spacing: 0; text-transform: none; color: var(--head-ink); opacity: .75; }}
  .frame {{
    display: flex; width: 502px; height: 780px; overflow: auto; position: relative;
    scrollbar-gutter: stable;
    border: 1px solid var(--divider); border-radius: 12px; background: var(--canvas);
  }}
  .frame .rail {{ position: sticky; top: 0; height: 780px; flex: 0 0 var(--rail-w); }}
  .frame .read {{ display: block; flex: 0 0 420px; width: 420px; box-sizing: border-box; padding: 0 0 0 20px; }}
  .frame .read__body {{ container-type: inline-size; }}

  .strip {{ margin-top: 46px; display: flex; gap: 34px; align-items: flex-start; flex-wrap: wrap; }}
  .strip .cell {{ text-align: center; }}
  .strip .cell svg {{ width: 34px; height: 34px; display: block; margin: 0 auto 8px;
    fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }}
  .strip .cell b {{ display: block; font: 600 12px/1.3 var(--font-sans); }}
  .strip .cell small {{ display: block; color: var(--head-ink); font: 500 11px/1.3 var(--font-sans); }}
</style>
</head>
<body>
<div class="bar">
  <h1>Rail icons</h1><span class="sub">spec 151 · the rail and the stage, 1:1</span>
  <span class="grow"></span>
  <div class="grp" data-slot="bible"><span>Alkitab</span>
    <button data-v="open" aria-pressed="true">open + cross</button>
    <button data-v="closed" aria-pressed="false">closed + cross</button></div>
  <div class="grp" data-slot="tatib"><span>Tata Ibadah</span>
    <button data-v="clipboard" aria-pressed="true">clipboard</button>
    <button data-v="steps" aria-pressed="false">steps</button></div>
  <div class="grp" data-slot="song"><span>Kidung</span>
    <button data-v="pair" aria-pressed="true">beamed pair</button>
    <button data-v="single" aria-pressed="false">single note</button></div>
  <div class="grp" data-slot="audio"><span>Audio media</span>
    <button data-v="waveform" aria-pressed="true">waveform</button>
    <button data-v="speaker" aria-pressed="false">speaker</button></div>
  <span class="split"></span><button id="theme" type="button">Dark</button>
</div>

<div class="wrap">
  <div class="demos">
    <figure class="demo"><figcaption>Now — develop<small>scrolls inside</small></figcaption>
      <div class="frame" id="frameNow"></div></figure>
    <figure class="demo"><figcaption>Proposed<small>scrolls inside</small></figcaption>
      <div class="frame" id="frameProposed"></div></figure>
  </div>

  <div class="strip" id="strip"></div>
</div>

<template id="railSrc">{rail}</template>
<template id="readSrc">{article}</template>
<script>
const G = {{
  bible: {{
    closed: `{GLYPHS["bible"]["closed"]}`,
    open: `{GLYPHS["bible"]["open"]}`,
    shipped: '<path d="M12 6.6C10.3 5.2 7.9 4.6 4.5 4.8v13.4c3.4-.2 5.8.4 7.5 1.8 1.7-1.4 4.1-2 7.5-1.8V4.8c-3.4-.2-5.8.4-7.5 1.8z"/><path d="M12 6.6v13.4"/>'
  }},
  tatib: {{
    clipboard: `{GLYPHS["tatib"]["clipboard"]}`,
    steps: `{GLYPHS["tatib"]["steps"]}`
  }},
  song: {{
    pair: `{GLYPHS["song"]["pair"]}`,
    single: `{GLYPHS["song"]["single"]}`
  }},
  audio: {{
    waveform: `{GLYPHS["audio"]["waveform"]}`,
    speaker: `{GLYPHS["audio"]["speaker"]}`,
    now: `{GLYPHS["audio"]["now"]}`
  }}
}};
const FAMILY = {{
  image: `{FAMILY["image"]}`,
  video: `{FAMILY["video"]}`,
  pdf: `{FAMILY["pdf"]}`,
  slides: `{FAMILY["slides"]}`,
  missing: `{FAMILY.get("missing", "")}`
}};
const SVG = (paths) => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths + '</svg>';
const choose = {{ bible: 'open', tatib: 'clipboard', song: 'pair', audio: 'waveform' }};

function shell(frame, proposed) {{
  frame.replaceChildren();
  const rail = document.getElementById('railSrc').content.cloneNode(true).firstElementChild;
  const read = document.getElementById('readSrc').content.cloneNode(true).firstElementChild;
  if (proposed) {{
    rail.querySelector('[data-panel="alkitab"] svg').innerHTML = G.bible[choose.bible];
    rail.querySelector('[data-panel="tatib"] svg').innerHTML = G.tatib[choose.tatib];
    rail.querySelector('[data-panel="kidung"] svg').innerHTML = G.song[choose.song];
  }}
  read.querySelectorAll('.entry__kind-icon[data-kind-icon="song"] svg').forEach(svg => {{
    svg.innerHTML = proposed ? G.song[choose.song] : G.song.single;   // shipped mark
  }});
  if (proposed && choose.bible === 'open') {{
    read.querySelectorAll('.entry__kind-icon[data-kind-icon="scripture"] svg').forEach(svg => {{
      svg.innerHTML = G.bible.open;   // the rail's Bible is the passage's own mark
    }});
  }}
  read.querySelectorAll('.entry__media-icon[data-media-icon]').forEach(span => {{
    const family = span.dataset.mediaIcon;
    const mark = family === 'audio'
      ? (proposed ? G.audio[choose.audio] : G.audio.now)
      : (FAMILY[family] || FAMILY.missing);
    span.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true">' + mark + '</svg>';
  }});
  frame.append(rail, read);
}}

function strip() {{
  const scripture = choose.bible === 'open' ? G.bible.open : G.bible.shipped;
  const rows = [
    ['Alkitab rail', G.bible[choose.bible], '24px'],
    ['passage entry', scripture, '20px, kind mark'],
    ['Add Passage tile', scripture, '24px'],
    ['Kidung rail', G.song[choose.song], '24px'],
    ['song entry', G.song[choose.song], '20px, kind mark'],
    ['Add Song tile', G.song[choose.song], '24px'],
    ['audio media', G.audio[choose.audio], '23px, family chip'],
    ['Tata Ibadah rail', G.tatib[choose.tatib], '24px']
  ];
  document.getElementById('strip').replaceChildren(...rows.map(([name, paths, size]) => {{
    const cell = document.createElement('div'); cell.className = 'cell';
    cell.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + paths + '</svg><b>' + name + '</b><small>' + size + '</small>';
    return cell;
  }}));
}}

document.querySelectorAll('.grp').forEach(grp => {{
  grp.addEventListener('click', event => {{
    const button = event.target.closest('button'); if (!button) return;
    choose[grp.dataset.slot] = button.dataset.v;
    grp.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    shell(document.getElementById('frameProposed'), true);
    strip();
  }});
}});

const theme = document.getElementById('theme');
theme.addEventListener('click', () => {{
  const dark = document.documentElement.dataset.theme !== 'dark';
  document.documentElement.dataset.theme = dark ? 'dark' : '';
  theme.textContent = dark ? 'Light' : 'Dark';
}});
if (matchMedia('(prefers-color-scheme: dark)').matches) theme.click();

shell(document.getElementById('frameNow'), false);
shell(document.getElementById('frameProposed'), true);
strip();
</script>
</body>
</html>
"""

(HERE / "preview.html").write_text(page)
print(f"wrote {HERE / 'preview.html'} ({len(page):,} bytes) from {url}")
