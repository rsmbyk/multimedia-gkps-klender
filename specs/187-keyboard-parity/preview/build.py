"""Assemble the spec-187 preview page from the live app's own markup and data.

Writes into this folder:

    panels.js     the captured payloads (`window.__PV`), one copy
    index.html    the dock preview — the runner and the K sheet

The dock's shell is the product's `multimedia/web/templates/reading/obs_dock.html`;
the list, the rows and the inner blocks are the product's own builders, copied into
`preview.js` from `static/web/obs-dock.js`. What this slice adds is drawn here as the
proposal: the shortcut sheet, and the runner that holds a go to with no service.

Data provenance (captured 2026-11-03 from the compose stack serving develop):

    service.json   /projector?service=142              the runner's content (27 entries)
    index.json     /projector/goto/index/             sliced to four songs and Matius
    songs.json     /projector/goto/song/{1390,1391,1434,667}/
    chapter.json   /projector/goto/chapter/40/5/      Matius 5, both editions

The page carries the data in `panels.js` because a static page opened over file://
cannot fetch: the product fetches these payloads when a result is chosen, and the
README says so.

THE PAGE IS SELF-CONTAINED. The desktop chat's `::preview{file=…}` frame loads a
page through `srcdoc` in a sandboxed iframe with an opaque origin, so a relative
`<link>` or `<script src>` does not resolve there. Every stylesheet and script is
therefore inlined, and the two fonts are base64 data URIs (an opaque origin cannot
read `file://` either). The `.css` / `.js` files beside this one stay the source.
"""

import base64
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def data(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def read_css(rel: str) -> str:
    """A stylesheet's text, with its font files embedded as data URIs."""
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")

    def embed(match):
        target = match.group(1)
        asset = (path.parent / target).resolve()
        if asset.suffix in (".ttf", ".woff2"):
            return "data:font/" + asset.suffix.lstrip(".") + ";base64," + \
                base64.b64encode(asset.read_bytes()).decode()
        return match.group(0)

    return re.sub(r'url\("([^"]+)"\)', embed, text)


def read_js(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def read_picker() -> str:
    """The picker section, captured from the live `/obs/dock`, with its logo inlined
    because the page is opened as `srcdoc` and cannot resolve `/static/...`."""
    html = (HERE / "picker.html").read_text(encoding="utf-8")
    logo = base64.b64encode((ROOT / "static/assets/gkps.png").read_bytes()).decode()
    return html.replace("__LOGO__", "data:image/png;base64," + logo)


CSS_FILES = (
    "static/styles/design/tokens.css",
    "static/styles/design/fonts.css",
    "static/styles/design/obs-dock.css",
    "specs/187-keyboard-parity/preview/preview.css",
)

# In order, in one scope: the captured payloads, the fetch stand-in, the product's own
# lookup module, and the dock's driver.
JS_FILES = (
    "specs/187-keyboard-parity/preview/panels.js",
    "static/web/projector-library.js",
    "specs/187-keyboard-parity/preview/preview.js",
)

# The projector's own key-cap symbols, so the dock's sheet draws the same arrows the
# operator already reads on the other surface (reading/projector_controls.html:1-32).
SYMBOLS = """    <svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
      <symbol id="arrow-right" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10m-4-4 4 4-4 4"/></symbol>
      <symbol id="arrow-left" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13 8H3m4-4-4 4 4 4"/></symbol>
      <symbol id="arrow-up" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M8 13V3m-4 4 4-4 4 4"/></symbol>
      <symbol id="arrow-down" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3v10m-4-4 4 4 4-4"/></symbol>
      <symbol id="shift-arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2 14 8h-3v4H5V8H2zM4.5 14h7"/></symbol>
      <symbol id="enter" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 3v8H3m0 0 3-3m-3 3 3 3"/></symbol>
      <symbol id="backspace" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h7a1.5 1.5 0 0 1 1.5 1.5v7A1.5 1.5 0 0 1 13 13H6L2 8z"/><path d="m8 6 4 4m0-4-4 4"/></symbol>
    </svg>"""


def key(text, cls=""):
    return '<span class="k' + (" " + cls if cls else "") + '">' + text + "</span>"


def glyph(symbol, cls="glyph"):
    """A keycap that draws a symbol. `cls` adds size classes (`ww`, `bk`); `glyph` is
    always applied, because it is the class that sizes the `<svg>` — a cap missing it
    stretches its symbol to the default 42 × 150 and clips it."""
    extra = " ".join(c for c in cls.replace("glyph", "").split() if c)
    classes = "k glyph" + ((" " + extra) if extra else "")
    return ('<span class="' + classes + '"><svg aria-hidden="true"><use href="#' + symbol
            + '"/></svg></span>')


CMD = key("⌘", "w")
SHIFT = glyph("shift-arrow", "glyph ww")
# The space key, drawn as the projector draws it: a three-unit cap carrying the open-box
# space mark (␣), stretched 1.3× wide — not the word `Space`.
SPACE = ('<span class="k sp glyph" aria-label="Space"><span class="space-mark">'
         '\u2423</span></span>')
OR = '<span class="or">or</span>'

# The dock's table, in the sheet's own order: group, then (label, [chords]) rows.
# One row per direction, as the projector's own sheet draws it — `next` and
# `previous`, `first` and `last` never share a row. A row whose shortcut the
# projector also has wears the projector's own wording, verbatim
# (`projector_controls.html`), so the two sheets name one act the same way; the
# dock-only rows are at the end of the list in DOCK_ONLY_LABELS.
SHEET = (
    ("Pick a service", (
        ("Move the Pick", [glyph("arrow-up"), glyph("arrow-down")]),
        ("Open the Service", [glyph("enter", "glyph ww")]),
    )),
    ("Service", (
        ("Next", [glyph("arrow-right"), glyph("arrow-down"), key("PgDn", "nav")]),
        ("Previous", [glyph("arrow-left"), glyph("arrow-up"), key("PgUp", "nav")]),
        ("First", [key("Home", "nav")]),
        ("Last", [key("End", "nav")]),
        ("Next Entry", [CMD + glyph("arrow-right")]),
        ("Previous Entry", [CMD + glyph("arrow-left")]),
        ("First Entry", [CMD + key("Home", "nav")]),
        ("Last Entry", [CMD + key("End", "nav")]),
    )),
    ("Song", (
        ("Next Bait", [SHIFT + glyph("arrow-right"), SHIFT + key("PgDn", "nav")]),
        ("Previous Bait", [SHIFT + glyph("arrow-left"), SHIFT + key("PgUp", "nav")]),
        ("First Bait", [SHIFT + key("Home", "nav")]),
        ("Last Bait", [SHIFT + key("End", "nav")]),
    )),
    ("Passage and go to", (
        ("Flip TB / SIM", [key("T")]),
        ("First Verse", [key("Home", "nav")]),
        ("Last Verse", [key("End", "nav")]),
        ("Next Chapter", [SHIFT + glyph("arrow-right"), SHIFT + key("PgDn", "nav")]),
        ("Previous Chapter", [SHIFT + glyph("arrow-left"), SHIFT + key("PgUp", "nav")]),
        ("First Chapter", [SHIFT + key("Home", "nav")]),
        ("Last Chapter", [SHIFT + key("End", "nav")]),
        ("Next Book", [CMD + glyph("arrow-right")]),
        ("Previous Book", [CMD + glyph("arrow-left")]),
        ("First Book", [CMD + key("Home", "nav")]),
        ("Last Book", [CMD + key("End", "nav")]),
    )),
    ("Display", (
        ("Show or Hide Words", [SPACE]),
        ("Keyboard Shortcuts", [key("K")]),
        ("Passage or Song", [key("G")]),
        ("Back to Services (hold)", [key("Esc", "w")]),
    )),
    ("Find", (
        ("Previous Match", [glyph("arrow-up")]),
        ("Next Match", [glyph("arrow-down")]),
        ("Open Match", [glyph("enter", "glyph ww")]),
        ("Close When Empty", [glyph("backspace", "bk")]),
        ("Close Find", [key("Esc", "w")]),
    )),
)

# The rows with no projector counterpart: the picker's own two and the held `Esc`
# that returns the dock to the picker (the projector's `Back to Service` is a tap
# out of a detour, a different act).
DOCK_ONLY_LABELS = {"Move the Pick", "Open the Service", "Back to Services (hold)"}


def sheet_groups():
    out = []
    for index, (title, rows) in enumerate(SHEET):
        first = " ksgroup--first" if index == 0 else ""
        # The picker's own keys exist only on the picker, so its group is marked and
        # the driver hides it whenever the runner is showing.
        picker = ' data-keys="pick"' if index == 0 else ""
        body = "\n".join(
            '            <p class="krow"><span class="kfn">%s</span>'
            '<span class="chord">%s</span></p>' % (label, OR.join(chords))
            for label, chords in rows)
        out.append('          <section class="ksgroup%s"%s>\n'
                   '            <h4>%s</h4>\n%s\n'
                   '          </section>' % (first, picker, title, body))
    return "\n".join(out)


DOCK_MARKUP = """__SYMBOLS__
    <main class="dock" id="dockPanel" data-view="run" tabindex="-1" aria-label="Operator dock">
__PICKER__

      <section class="view is-active" id="viewRun" aria-label="Runner">
        <div class="dock__head">
          <div class="dock__runheadrow">
            <div class="dock__runtitles">
              <p class="serviceline" id="runService">Ibadah Minggu</p>
              <p class="servicedate" id="runDate">4 Oktober 2026</p>
            </div>
            <button type="button" class="iconbtn" id="findBtn" title="Go to a passage or song"
                    aria-label="Go to a passage or song" tabindex="-1">
              <svg viewBox="0 0 20 20"><circle cx="8.7" cy="8.7" r="5.1"></circle><path d="M12.5 12.5 16.6 16.6"></path></svg>
            </button>
            <button type="button" class="iconbtn" id="switchBtn" title="Switch service"
                    aria-label="Switch service" tabindex="-1">
              <svg viewBox="0 0 20 20"><path d="M6 4h10M6 10h10M6 16h10"></path><path d="M3 4h.01M3 10h.01M3 16h.01" stroke-width="2.4"></path></svg>
            </button>
            <button type="button" class="iconbtn" id="blankBtn" aria-pressed="false"
                    title="Hide words" aria-label="Hide words" tabindex="-1">
              <svg class="glyph glyph--display" viewBox="0 0 20 20">
                <path d="M3 3l14 14"></path>
                <path d="M6.6 6.7C4.1 8.2 2.6 10 2.6 10s2.8 4.6 7.4 4.6c1.5 0 2.8-.4 3.9-1"></path>
                <path d="M9 5.5c.3 0 .7-.1 1-.1 4.6 0 7.4 4.6 7.4 4.6s-.8 1.4-2.2 2.6"></path>
              </svg>
              <svg class="glyph glyph--onscreen" viewBox="0 0 20 20">
                <path d="M2.6 10s2.8-4.6 7.4-4.6S17.4 10 17.4 10s-2.8 4.6-7.4 4.6S2.6 10 2.6 10z"></path>
                <circle cx="10" cy="10" r="2.6"></circle>
              </svg>
            </button>
          </div>
        </div>

        <div class="dock__body" id="runBody">
          <div class="offblock" id="offBlock" hidden>
            <div class="offstrip" id="offStrip">
              <span class="offstrip__label" id="offLabel"></span>
              <button type="button" class="offstrip__back" id="offBack" tabindex="-1">Back</button>
            </div>
            <div class="entryinner is-open" id="offInner">
              <div class="entryinner__clip">
                <div class="entryinner__body" id="offBody"></div>
              </div>
            </div>
          </div>
          <ul id="entryList"></ul>
          <p class="dock__note" id="runNote" hidden></p>
        </div>

        <div class="dock__transport">
          <div class="bandswap" id="bandSwap">
          <div class="bandswap__row transportrow" id="transportRow">
            <button type="button" class="transchip" id="transChip" hidden tabindex="-1"
                    aria-pressed="false" title="Flip TB / SIM (T)">TB</button>
            <div class="baits" id="baitStrip" hidden>
              <span class="baitstrip" id="baitChips"></span>
            </div>
            <span class="navpair">
              <button type="button" class="navbtn" id="prevBtn" tabindex="-1"
                      title="Previous screen" aria-label="Previous screen">
                <svg viewBox="0 0 20 20"><path d="M12 4 6 10l6 6"></path></svg>
              </button>
              <button type="button" class="navbtn" id="nextBtn" tabindex="-1"
                      title="Next screen" aria-label="Next screen">
                <svg viewBox="0 0 20 20"><path d="M8 4l6 6-6 6"></path></svg>
              </button>
            </span>
          </div>

          <div class="bandswap__row" id="findBand">
            <div class="findband">
            <div class="findrow">
              <input class="findfield" id="findInput" type="search" autocomplete="off"
                     spellcheck="false" placeholder="Passage or song">
            </div>
            <button type="button" class="findresult" id="findResult" disabled>
              <span class="findresult__label" id="findLabel">Start typing to find a match</span>
              <span class="findcount" id="findCount">0 / 0</span>
            </button>
            </div>
          </div>
          </div>
        </div>
      </section>
      <div class="findscrim" id="findScrim" hidden></div>

      <!-- The slice's proposal: the dock's own shortcut sheet, opened by K. -->
      <div class="keysheet" id="keysheet" hidden>
        <button type="button" class="keysheet__scrim" id="keysScrim"
                aria-label="Close shortcuts" tabindex="-1"></button>
        <section class="keysheet__panel" role="dialog" aria-modal="true"
                 aria-label="Keyboard shortcuts">
          <div class="keysheet__head">
            <h3 class="keysheet__title">Keyboard</h3>
            <button type="button" class="keysheet__close" id="keysClose"
                    aria-label="Close shortcuts" tabindex="-1">
              <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M6 6l8 8M14 6l-8 8"></path></svg>
            </button>
          </div>
          <div class="keysheet__body" id="keysBody">
__GROUPS__
          </div>
        </section>
      </div>
    </main>""".replace("__SYMBOLS__", SYMBOLS).replace("__GROUPS__", sheet_groups())

FETCH_SHIM = """/* This page may be opened over file:// or through the chat's srcdoc frame, where fetch
   cannot read the app's routes. The product's own lookup module is loaded unchanged; only
   its one index request is answered from the captured data. */
window.fetch = function (url) {
  var path = String(url);
  if (path.indexOf('/projector/goto/index/') !== -1) {
    return Promise.resolve(new Response(JSON.stringify(window.__PV.index),
      {status: 200, headers: {'Content-Type': 'application/json'}}));
  }
  return Promise.reject(new Error('preview: ' + path + ' is not served here'));
};"""


PAGE = """<!doctype html>
<html lang="id" data-theme="dark" data-theme-mode="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Keyboard parity — the dock (spec 187)</title>
<style>
__STYLE__
</style>
</head>
<body class="pv">

<header class="pv-bar">
  <span class="pv-group">
    <button type="button" data-state="rest">Service</button>
    <button type="button" data-state="pick">Picker</button>
    <button type="button" data-state="find">Go To</button>
    <button type="button" data-state="nomatch">No match</button>
    <button type="button" data-state="loading">Loading</button>
    <button type="button" data-state="song">Song on air</button>
    <button type="button" data-state="passage">Passage on air</button>
    <button type="button" data-state="hidden">Words hidden</button>
    <button type="button" data-state="alone">Go to alone</button>
    <button type="button" data-state="fetching">Fetching</button>
    <button type="button" data-state="keys">Shortcuts</button>
    <button type="button" data-state="pickkeys">Picker + shortcuts</button>
  </span>
  <span class="pv-sp"></span>
  <span class="pv-group">
    <button type="button" data-width="400" aria-pressed="true">400</button>
    <button type="button" data-width="320">320</button>
    <button type="button" data-width="520">520</button>
    <button type="button" data-height="800" aria-pressed="true">800h</button>
    <button type="button" data-height="1000">1000h</button>
    <button type="button" data-height="1200">1200h</button>
    <button type="button" data-theme="dark" aria-pressed="true">Dark</button>
    <button type="button" data-theme="light">Light</button>
  </span>
</header>

<main class="pv-stage">
  <div class="pv-frame" id="pvFrame">
__DOCK__
  </div>

  <aside class="pv-read" id="pvRead"></aside>
</main>

<p class="pv-note" id="pvNote"></p>

__SCRIPT__
</body>
</html>
"""


def main():
    captured = {"service": data("service.json"), "index": data("index.json"),
                "songs": data("songs.json"), "chapter": data("chapter.json")}
    panels = ("/* Captured from the running app on 2026-11-03 — see build.py. */\n"
              "window.__PV = " + json.dumps(captured, ensure_ascii=False) + ";\n")
    (HERE / "panels.js").write_text(panels, encoding="utf-8")

    style = "\n".join("/* " + rel + " */\n" + read_css(rel) for rel in CSS_FILES)
    scripts = [read_js(rel) for rel in JS_FILES]
    script = "\n".join("<script>\n" + part + "\n</script>"
                       for part in scripts[:1] + [FETCH_SHIM] + scripts[1:])

    (HERE / "index.html").write_text(
        PAGE.replace("__DOCK__", DOCK_MARKUP)
            .replace("__PICKER__", read_picker())
            .replace("__STYLE__", style)
            .replace("__SCRIPT__", script),
        encoding="utf-8")
    print("wrote panels.js, index.html")


if __name__ == "__main__":
    main()
