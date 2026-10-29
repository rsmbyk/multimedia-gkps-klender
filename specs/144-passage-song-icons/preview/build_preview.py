#!/usr/bin/env python3
"""Regenerate the kind-mark comparison preview.

The markup is the live page's own (a service's entries are data, not code); the stylesheets are
FROZEN at the commit this slice branched from, so the "Now" column keeps showing the stage without
a kind mark while the working tree grows one.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/144-passage-song-icons/preview/build_preview.py

Reads   http://127.0.0.1:8830/tatib/144/   (the slice's own server)
Writes  preview.html + assets/{tokens,components,fonts}.css next to this file
"""
import json
import pathlib
import re
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
URL = "http://127.0.0.1:8830/tatib/144/"
FROZEN_AT = "05379336"          # develop, the commit this slice branched from

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

# The marks are what the template will render server-side. They are injected here because this
# page is a photograph of the shipped page, and the shipped page has no marks yet.
GLYPHS = {
    "scripture": '<path d="M12 6.6C10.3 5.2 7.9 4.6 4.5 4.8v13.4c3.4-.2 5.8.4 7.5 1.8 '
                 '1.7-1.4 4.1-2 7.5-1.8V4.8c-3.4-.2-5.8.4-7.5 1.8z"/><path d="M12 6.6v13.4"/>',
    "song": '<path d="M10.9 17.4V5.9c0-.5.3-.9.8-1l6.1-1.3"/><path d="M10.9 5.9c3 .8 4.6 2.7 '
            '4.4 5.5"/><ellipse cx="8.4" cy="17.3" rx="2.5" ry="2.1"/>',
    "text": '<path d="M5 7h14M5 12h14M5 17h9"/>',
}


def with_marks(fragment: str) -> str:
    """Put a kind mark inside every entry section, the way the template will."""
    def one(match: re.Match) -> str:
        opening, body = match.group(1), match.group(2)
        if "tatib__item--media" in opening:
            return opening + body
        if 'class="entry__kind-icon"' in body:
            return opening + body       # the template draws it now (spec 144 shipped)
        if 'href="/bible/' in body:
            kind = "scripture"
        elif 'href="/songs/' in body:
            kind = "song"
        else:
            kind = "text"
        opening = opening.replace(
            'class="', f'class="tatib__item--{kind} tatib__item--marked ', 1)
        mark = (f'<span class="entry__kind-icon" aria-hidden="true" data-kind-icon="{kind}">'
                f'<svg viewBox="0 0 24 24">{GLYPHS[kind]}</svg></span>')
        # The mark rides inside the heading when the row has one: D needs it on the title's
        # own first line, and A/B/C lift it out of the flow (the section is its positioning
        # box). It is never the section's first child either way, because two shipped rules
        # key on `> :first-child` and a mark in that seat gave the title its 30px pericope
        # margin back (measured: the row grew 56px -> 69.8px).
        if '<h2 class="read__sec">' in body:
            body = body.replace('<h2 class="read__sec">', '<h2 class="read__sec">' + mark, 1)
        else:
            head, sep, tail = body.partition('</section>')
            body = head + mark + sep + tail
        return opening + body

    return re.sub(
        r'(<section class="tatib__item[^"]*"[^>]*>)(.*?)(?=<section class="tatib__item|</article>)',
        one, fragment, flags=re.S,
    )


# The media chip's glyph is injected by media-stage.js at runtime, which a static page never
# runs. The comparison needs the real chip (glyph and all), so it is filled in here from the
# same path table that script carries.
MEDIA_GLYPHS = {
    "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9" r="1.5"/>'
             '<path d="m4 17 5-5 3.5 3.5 2.5-2.5 5 5"/>',
    "audio": '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
    "pdf": '<path d="M6 2h8l5 5v15H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM14 2v5h5M8 16h8M8 19h6"/>',
    "video": '<rect x="3" y="5" width="18" height="15" rx="2"/><path d="M3 10h18M7 5l3 5m4-5 3 5"/>'
             '<path d="m10 12 5 3-5 3z"/>',
    "slides": '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M12 18v3m-4 0h8M7 9h10M7 12h7"/>',
}


def with_media_glyphs(fragment: str) -> str:
    def one(match: re.Match) -> str:
        family = match.group(1)
        paths = MEDIA_GLYPHS.get(family, MEDIA_GLYPHS["image"])
        return (f'<span class="entry__media-icon" aria-hidden="true" data-media-icon="{family}">'
                f'<svg viewBox="0 0 24 24">{paths}</svg></span>')

    return re.sub(
        r'<span class="entry__media-icon" aria-hidden="true" data-media-icon="([a-z]+)"></span>',
        one, fragment)


article = with_media_glyphs(with_marks(article))

OPTIONS = [
    ("now", "Now"),
    ("glyph", "A · Glyph in the media column"),
    ("line", "B · Glyph on the title"),
    ("ring", "C · Outline chip"),
    ("tint", "D · Tinted chip"),
]
NOTES = {
    "now": "no mark — what ships today",
    "glyph": "20px glyph in --head-ink, its centre on the media chip's centre line; title on the media title's column (64px)",
    "line": "the same glyph riding the title's first line, on a hanging indent; title indented 30px — ADOPTED",
    "ring": "30px rounded square, 1px --divider ring, no fill; title indented 42px",
    "tint": "30px rounded square at --head-ink 9%, like a smaller media chip; title indented 42px",
}

# NOTHING in this block ships: each candidate is a handful of declarations scoped to
# [data-option=...], laid over the frozen stylesheet so the columns differ by one idea each.
CSS = """
.entry__kind-icon { display: none; }
.entry__kind-icon svg { width: 100%; height: 100%; fill: none; stroke: currentColor;
  stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }

/* A — a bare glyph in the media chip's own column: its centre sits on the chip's centre
   line (13px + 21px = 34px from the row's edge), and the title takes the media title's
   column (64px), so a passage row and a media row share one left rail. */
[data-option="glyph"] .tatib__item--scripture .entry__kind-icon,
[data-option="glyph"] .tatib__item--song .entry__kind-icon {
  display: grid; place-items: center; position: absolute; left: 24px; top: 50%;
  transform: translateY(-50%); width: 20px; height: 20px; color: var(--head-ink);
}
[data-option="glyph"] .tatib__item--scripture,
[data-option="glyph"] .tatib__item--song { padding-left: 64px; }

/* B — a 30px outline chip: the media chip's anatomy without its fill */
[data-option="ring"] .tatib__item--scripture .entry__kind-icon,
[data-option="ring"] .tatib__item--song .entry__kind-icon {
  display: grid; place-items: center; position: absolute; left: 13px; top: 50%;
  transform: translateY(-50%); width: 30px; height: 30px; border-radius: 7px;
  color: var(--head-ink); box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--divider) 90%, transparent);
}
[data-option="ring"] .tatib__item--scripture .entry__kind-icon svg,
[data-option="ring"] .tatib__item--song .entry__kind-icon svg { width: 16px; height: 16px; }
[data-option="ring"] .tatib__item--scripture,
[data-option="ring"] .tatib__item--song { padding-left: 55px; }

/* C — a 30px tinted chip: the media chip in the stage's meta colour */
[data-option="tint"] .tatib__item--scripture .entry__kind-icon,
[data-option="tint"] .tatib__item--song .entry__kind-icon {
  display: grid; place-items: center; position: absolute; left: 13px; top: 50%;
  transform: translateY(-50%); width: 30px; height: 30px; border-radius: 7px;
  color: var(--head-ink); background: color-mix(in srgb, var(--head-ink) 9%, var(--canvas));
}
[data-option="tint"] .tatib__item--scripture .entry__kind-icon svg,
[data-option="tint"] .tatib__item--song .entry__kind-icon svg { width: 16px; height: 16px; }
[data-option="tint"] .tatib__item--scripture,
[data-option="tint"] .tatib__item--song { padding-left: 55px; }

/* D — the same 20px glyph, riding the title's own first line: the mark is inside the
   heading, the heading carries a hanging indent, so the glyph never floats between a
   title and its "Bait" line */
[data-option="line"] .tatib__item--scripture > .read__sec,
[data-option="line"] .tatib__item--song > .read__sec { padding-left: 30px; text-indent: -30px; }
[data-option="line"] .tatib__item--scripture > .read__sec > .entry__kind-icon,
[data-option="line"] .tatib__item--song > .read__sec > .entry__kind-icon {
  display: inline-block; width: 20px; height: 20px; margin-right: 6px;
  text-indent: 0; vertical-align: -4px; color: var(--head-ink);
}
/* the "Bait" line belongs to the title, so it lines up under the title's words, not under the glyph */
[data-option="line"] .tatib__item--song > .read__sub { padding-left: 30px; }

/* the second axis of the question: does a text row get a mark too? off by default */
[data-mark-text="on"] .tatib__item--text .entry__kind-icon { display: block; position: absolute;
  left: 12px; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; color: var(--head-ink); }
[data-mark-text="on"] .tatib__item--text .entry__kind-icon svg { width: 100%; height: 100%; }
[data-mark-text="on"][data-option="glyph"] .tatib__item--text,
[data-mark-text="on"][data-option="line"] .tatib__item--text { padding-left: 64px; }
[data-mark-text="on"][data-option="ring"] .tatib__item--text,
[data-mark-text="on"][data-option="tint"] .tatib__item--text { padding-left: 55px; }
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
  /* the comparison pages need the row width a 400px pane gives, not the 1040px column */
  .cmp-stage .read__body { width: 400px; }
  .cmp-stage .tatib__item { margin-left: -10px; margin-right: -10px; }
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
  const textBtn = document.getElementById('marktext');
  textBtn.addEventListener('click', () => {
    const on = root.dataset.markText !== 'on';
    root.dataset.markText = on ? 'on' : 'off';
    textBtn.setAttribute('aria-pressed', String(on));
  });
  const hoverBtn = document.getElementById('hover');
  hoverBtn.addEventListener('click', () => {
    const rows = document.querySelectorAll('.tatib__item');
    hoverBtn.setAttribute('aria-pressed', String(rows[1].classList.toggle('is-modal-origin')));
  });
  const themeBtn = document.getElementById('theme');
  themeBtn.addEventListener('click', () => {
    const dark = root.dataset.theme !== 'dark';
    root.dataset.theme = dark ? 'dark' : 'light';
    themeBtn.textContent = dark ? 'Light' : 'Dark';
  });
"""

# every row that carries a mark gets the class the indent rides on
buttons = "".join(
    '<button type="button" data-opt="%s" aria-pressed="%s">%s</button>'
    % (k, "true" if k == "glyph" else "false", label)
    for k, label in OPTIONS
)

page = (
    '<!doctype html>\n<html lang="id" data-read="on" data-option="glyph" data-mark-text="off">\n<head>\n'
    '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    "<title>Kind marks — comparison</title>\n"
    '<link rel="stylesheet" href="assets/tokens.css">\n'
    '<link rel="stylesheet" href="assets/components.css">\n'
    "<style>" + SHELL + "</style>\n<style>" + CSS + "</style>\n</head>\n<body>\n"
    '<div class="bar" role="group" aria-label="Kind-mark candidates">'
    + buttons
    + '<span class="note" id="note"></span><span class="spacer"></span>'
    '<button type="button" id="marktext" aria-pressed="false">Mark text rows too</button>'
    '<button type="button" id="hover" aria-label="Show the hover state on the second entry">Show hover</button>'
    '<button type="button" id="theme">Dark</button></div>\n'
    '<div class="cmp-stage">\n' + article + "\n</div>\n"
    "<script>" + JS.replace("__NOTES__", json.dumps(NOTES)) + "</script>\n</body>\n</html>\n"
)

# A four-column sheet, for judging the candidates against each other rather than from memory.
COLS = [("glyph", "A · Glyph on the row"), ("line", "B · Glyph on the title"),
        ("ring", "C · Outline chip"), ("tint", "D · Tinted chip")]
columns = "".join(
    f'<div class="col"><p class="col__cap">{label}</p>'
    f'<div class="col__stage" data-option="{key}">{article}</div></div>'
    for key, label in COLS
)
compare = (
    '<!doctype html>\n<html lang="id" data-read="on" data-mark-text="off">\n<head>\n'
    '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    "<title>Kind marks — four columns</title>\n"
    '<link rel="stylesheet" href="assets/tokens.css">\n'
    '<link rel="stylesheet" href="assets/components.css">\n'
    "<style>" + SHELL + "</style>\n<style>" + CSS + """</style>
<style>
  .cols { display: flex; gap: 28px; padding: 24px; align-items: flex-start; }
  .col { width: 400px; flex: none; }
  .col__cap { margin: 0 0 10px; font: 600 13px/1.2 var(--font-sans); color: var(--ink); }
  .col__stage .read { display: block; }
  .col__stage .read__body { container: stage-pane / inline-size; width: 400px; }
  .col__stage .tatib__item { margin-left: -10px; margin-right: -10px; }
</style>\n</head>\n<body>\n<div class="cols">""" + columns + "</div>\n</body>\n</html>\n"
)
(HERE / "compare.html").write_text(compare, encoding="utf-8")
print(f"wrote {HERE/'compare.html'} ({len(compare)} bytes)")

(HERE / "preview.html").write_text(page, encoding="utf-8")
print(f"wrote {HERE/'preview.html'} ({len(page)} bytes), styles frozen at {FROZEN_AT}")
print("marked rows:", len(re.findall(r'tatib__item--marked', page)),
      "| scripture:", len(re.findall(r'data-kind-icon="scripture"', page)),
      "| song:", len(re.findall(r'data-kind-icon="song"', page)),
      "| text:", len(re.findall(r'data-kind-icon="text"', page)))
