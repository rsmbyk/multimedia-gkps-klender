#!/usr/bin/env python3
"""Regenerate the entry-surface comparison preview.

The markup is the live page's own (a service's entries are data, not code); the stylesheets
are FROZEN at the commit before this slice, because the comparison has to keep showing the
spec 068 box as its "Now" column after the box is gone from the working tree.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/142-entry-surface/preview/build_preview.py

Reads   http://127.0.0.1:8820/tatib/142/   (the slice's own server)
Writes  preview.html + assets/{tokens,components,fonts}.css next to this file
"""
import json
import pathlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
URL = "http://127.0.0.1:8820/tatib/142/"
FROZEN_AT = "ca71c850"          # develop, immediately before this slice

for name in ("tokens.css", "components.css", "fonts.css"):
    blob = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{FROZEN_AT}:static/styles/design/{name}"],
        capture_output=True, check=True,
    ).stdout
    (HERE / "assets").mkdir(exist_ok=True)
    (HERE / "assets" / name).write_bytes(blob)

html = subprocess.run(["curl", "-s", URL], capture_output=True, text=True, check=True).stdout
start = html.index('<article class="read" id="read"')
end = html.index("</article>", start) + len("</article>")
article = html[start:end]

OPTIONS = [
    ("now", "Now"),
    ("bare", "A · Bare"),
    ("rules", "B · Rules"),
    ("gutter", "C · Gutter"),
    ("felt", "D · Felt"),
]
NOTES = {
    "now": "border + 1.2% fill — spec 068, what shipped before this slice",
    "bare": "no chrome at rest; the gap between entries carries the separation — ADOPTED",
    "rules": "one hairline between entries — the section break already owns a rule",
    "gutter": "L : / J : in a 37.6px hanging column",
    "felt": "no ring; the fill goes from 1.2% to 4% so it can be seen",
}

# NOTHING in this block ships: each candidate is three to eight declarations scoped to
# [data-option=...], laid over the frozen stylesheet so the columns differ by one idea each.
CSS = """
/* the rhythm knob is the add row between entries, not `.tatib__item + .tatib__item`:
   that selector never matches while the editor draws the bars, so its 2px is dead code */
[data-option="bare"] .tatib__item--acts,
[data-option="bare"] .tatib__eos { background: transparent; box-shadow: none; }
[data-option="bare"] .entry__add { margin-block: 10px; }

[data-option="rules"] .tatib__item--acts,
[data-option="rules"] .tatib__eos { background: transparent; box-shadow: none; }
[data-option="rules"] .entry__add { margin-block: 2px; }
[data-option="rules"] .tatib__item + .entry__add + .tatib__item,
[data-option="rules"] .tatib__item + .entry__add + .tatib__eos,
[data-option="rules"] .tatib__eos + .entry__add + .tatib__item,
[data-option="rules"] .tatib__eos + .entry__add + .tatib__eos {
  border-top: 1px solid color-mix(in srgb, var(--divider) 55%, transparent);
  padding-top: 14px; margin-top: 14px;
}

[data-option="gutter"] .tatib__item--acts,
[data-option="gutter"] .tatib__eos { background: transparent; box-shadow: none; }
[data-option="gutter"] .entry__add { margin-block: 12px; }
[data-option="gutter"] .read[data-kind="tatib"] .tatib__tx {
  display: grid; grid-template-columns: 2.35rem minmax(0, 1fr);
}
[data-option="gutter"] .tatib__sp { margin-right: 0; }

[data-option="felt"] .tatib__item--acts,
[data-option="felt"] .tatib__eos {
  background: color-mix(in srgb, var(--ink) 4%, var(--canvas));
  box-shadow: none; border-radius: 12px;
}
"""

SHELL = """
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
  .cmp-stage { width: min(1040px, 100vw - 48px); margin: 0 auto; padding: 40px 0 120px; }
  .read { display: block; }
  .read__body { container: stage-pane / inline-size; }
"""

JS = """
  const root = document.documentElement;
  const NOTES = __NOTES__;
  const note = document.getElementById('note');
  const showNote = () => { note.textContent = NOTES[root.dataset.option] || ''; };
  showNote();
  document.querySelectorAll('[data-opt]').forEach(b => b.addEventListener('click', () => {
    root.dataset.option = b.dataset.opt;
    document.querySelectorAll('[data-opt]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    showNote();
  }));
  const hoverBtn = document.getElementById('hover');
  hoverBtn.addEventListener('click', () => {
    const rows = document.querySelectorAll('.tatib__item, .tatib__eos');
    hoverBtn.setAttribute('aria-pressed', String(rows[1].classList.toggle('is-modal-origin')));
  });
  const themeBtn = document.getElementById('theme');
  themeBtn.addEventListener('click', () => {
    const dark = root.dataset.theme !== 'dark';
    root.dataset.theme = dark ? 'dark' : 'light';
    themeBtn.textContent = dark ? 'Light' : 'Dark';
  });
"""

buttons = "".join(
    '<button type="button" data-opt="%s" aria-pressed="%s">%s</button>'
    % (k, "true" if k == "now" else "false", label)
    for k, label in OPTIONS
)

page = (
    '<!doctype html>\n<html lang="id" data-read="on" data-option="now">\n<head>\n'
    '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    "<title>Entry surface — comparison</title>\n"
    '<link rel="stylesheet" href="assets/tokens.css">\n'
    '<link rel="stylesheet" href="assets/components.css">\n'
    "<style>" + SHELL + "</style>\n<style>" + CSS + "</style>\n</head>\n<body>\n"
    '<div class="bar" role="group" aria-label="Entry surface candidates">'
    + buttons
    + '<span class="note" id="note"></span><span class="spacer"></span>'
    '<button type="button" id="hover" aria-label="Show the hover state on the second entry">Show hover</button>'
    '<button type="button" id="theme">Dark</button></div>\n'
    '<div class="cmp-stage">\n' + article + "\n</div>\n"
    "<script>" + JS.replace("__NOTES__", json.dumps(NOTES)) + "</script>\n</body>\n</html>\n"
)

(HERE / "preview.html").write_text(page, encoding="utf-8")
print(f"wrote {HERE/'preview.html'} ({len(page)} bytes), styles frozen at {FROZEN_AT}")
