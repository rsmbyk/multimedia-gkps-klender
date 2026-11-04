"""Assemble the spec-185 preview pages from the live app's own markup and data.

Writes into this folder:

    panels.js     the captured payloads (`window.__PV`), one copy
    index.html    the dock preview (the runner + the Go To)
    sync.html     the dock, a projector stage and the caption overlay following one state

The dock's shell is the product's `multimedia/web/templates/reading/obs_dock.html`;
the projector and overlay panels are the product's own stages and stylesheets. The sync
page draws all three **in one document**, because it is also reviewed inside the desktop
chat's preview frame, which does not run nested documents (iframes there stayed empty).

Data provenance (captured 2026-11-03 from the compose stack serving develop):

    service.json   /projector?service=142              the runner's content (27 entries)
    index.json     /projector/goto/index/             sliced to four songs and Matius
    songs.json     /projector/goto/song/{1390,1391,1434,667}/
    chapter.json   /projector/goto/chapter/40/5/      Matius 5, both editions

The pages carry the data in `panels.js` because a static page opened over file://
cannot fetch: the product fetches these payloads when a result is chosen, and the
README says so.

BOTH PAGES ARE SELF-CONTAINED. The desktop chat's `::preview{file=…}` frame loads a
page through `srcdoc` in a sandboxed iframe with an opaque origin, so a relative
`<link>` or `<script src>` does not resolve there — the first version rendered its
markup and none of its styles or scripts. Every stylesheet and script is therefore
inlined, and the two fonts are base64 data URIs (an opaque origin cannot read
`file://` either). The `.css` / `.js` files beside this one stay the source.
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


CSS_FILES = (
    "static/styles/design/tokens.css",
    "static/styles/design/fonts.css",
    "static/styles/design/obs-dock.css",
    "static/styles/design/projector.css",
    "static/styles/design/obs-overlay.css",
    "specs/185-dock-goto/preview/preview.css",
    "specs/185-dock-goto/preview/sync.css",
)

# In order, in one scope: the captured payloads, the fetch stand-in, the product's own
# lookup module, the dock's driver, and (sync page only) the other two surfaces.
JS_FILES = (
    "specs/185-dock-goto/preview/panels.js",
    "static/web/projector-library.js",
    "specs/185-dock-goto/preview/preview.js",
)


DOCK_MARKUP = """    <main class="dock" id="dockPanel" data-view="run" tabindex="-1" aria-label="Operator dock">
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
    </main>"""

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
<title>Go To — the dock (spec 185)</title>
<style>
__STYLE__
</style>
</head>
<body class="pv">

<header class="pv-bar">
  <span class="pv-group">
    <button type="button" data-state="rest">Service</button>
    <button type="button" data-state="find">Go To</button>
    <button type="button" data-state="nomatch">No match</button>
    <button type="button" data-state="loading">Loading</button>
    <button type="button" data-state="song">Song on air</button>
    <button type="button" data-state="passage">Passage on air</button>
    <button type="button" data-state="hidden">Words hidden</button>
  </span>
  <span class="pv-sp"></span>
  <span class="pv-group">
    <button type="button" data-width="400" aria-pressed="true">400</button>
    <button type="button" data-width="320">320</button>
    <button type="button" data-width="520">520</button>
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

SYNC = """<!doctype html>
<html lang="id" data-theme="dark" data-theme-mode="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>One state, three surfaces — the Go To (spec 185)</title>
<style>
__STYLE__
</style>
</head>
<body class="sv">

<header class="sv-bar">
  <span class="sv-steps" id="svSteps"></span>
  <span class="sv-nav">
    <button type="button" id="svPrev">← Previous</button>
    <button type="button" id="svNext">Next →</button>
  </span>
</header>

<h1 class="sv-title" id="svTitle"></h1>

<main class="sv-stage">
  <div>
    <p class="sv-cap">Dock · /obs/dock</p>
    <div class="sv-frame--dock"><div class="pv-frame" id="pvFrame">
__DOCK__
    </div></div>
    <div class="pv-read" id="pvRead" hidden></div>
    <p class="pv-note" id="pvNote" hidden></p>
  </div>

  <div class="sv-right">
    <div>
      <p class="sv-cap">Projector · /projector — 1920 × 1080 at 1/3</p>
      <div class="sv-panel">
        <div class="sv-canvas sv-projector">
          <main class="projector__screen">
            <div class="projector__screens" id="svProjScreens"></div>
          </main>
        </div>
      </div>
    </div>
    <div>
      <p class="sv-cap">Caption overlay · /obs/source/overlay — 1920 × 1080 at 1/3</p>
      <div class="sv-panel sv-panel--overlay">
        <div class="sv-canvas sv-overlay">
          <div class="obs-overlay__stage" id="svOverlayStage" aria-live="polite"></div>
        </div>
      </div>
    </div>
    <pre class="sv-state" id="svState"></pre>
  </div>
</main>

<footer class="sv-read" id="svRead"></footer>

<p class="sv-note">
  <b>What this page is.</b> The dock, a projector stage and the caption overlay, each drawn
  from the product's own markup and stylesheets, all in this one document because the chat's
  preview frame runs no nested documents. Every step below is one display state —
  <code>{service, screen, on, translation, goto, session}</code> — and all three surfaces paint
  from it alone. In the product that state lives in <code>localStorage['gkps-display']</code>
  and travels over <code>BroadcastChannel('gkps-service-display')</code>; there is no second
  channel here to make the surfaces agree, only the same state handed to each. The lines under
  the panels are each surface's own report of what it painted.
</p>

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

    def page(template, extra_js=()):
        script = "\n".join("<script>\n" + part + "\n</script>"
                            for part in scripts[:1] + [FETCH_SHIM] + scripts[1:]
                            + [read_js(rel) for rel in extra_js])
        return (template.replace("__DOCK__", DOCK_MARKUP)
                        .replace("__STYLE__", style)
                        .replace("__SCRIPT__", script))

    (HERE / "index.html").write_text(page(PAGE), encoding="utf-8")
    (HERE / "sync.html").write_text(
        page(SYNC, extra_js=("specs/185-dock-goto/preview/sync.js",)), encoding="utf-8")

    for stale in ("panel-projector.html", "panel-overlay.html"):
        path = HERE / stale
        if path.exists():
            path.unlink()
    print("wrote panels.js, index.html, sync.html")


if __name__ == "__main__":
    main()
