"""Build the spec 140 preview: the entry controls' own column, labels on desktop.

Run from the repo root:  python specs/140-stage-link-affordance/preview/build_controls.py

Writes `controls.html` (desktop/laptop, the two stage widths the shell produces) and
`phone.html` (the same markup at a 390px viewport, where the labels collapse),
assembled from the product's real stylesheets and the stage's real class names.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent

EYE = ("<svg viewBox=\"0 0 20 20\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" "
       "stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M2.6 10s2.8-4.6 "
       "7.4-4.6S17.4 10 17.4 10s-2.8 4.6-7.4 4.6S2.6 10 2.6 10z\"></path><circle cx=\"10\" cy=\"10\" "
       "r=\"2.1\"></circle></svg>")
PENCIL = ("<svg viewBox=\"0 0 20 20\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" "
          "stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M13.4 3.6l3 "
          "3-8.6 8.6H4.4v-3z\"></path><path d=\"M11.6 5.4l3 3\"></path></svg>")
TRASH = ("<svg viewBox=\"0 0 20 20\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" "
         "stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M3.6 "
         "5.4h12.8\"></path><path d=\"M8.2 5.4V3.8h3.6v1.6\"></path><path d=\"M5.4 5.4l.8 "
         "10.4h7.6l.8-10.4\"></path><path d=\"M8.6 8.6v4.4M11.4 8.6v4.4\"></path></svg>")

SHORT = "Kisah Para Rasul 1:1"
LONG = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa581. Sangap di Jahowa"


def entry(title, pk, long_title=False):
    bait = '' if long_title else '\n      <p class="read__sub">Bait 1–3</p>'
    return f"""    <section class="tatib__item tatib__item--entry tatib__item--acts" data-anchor="e{pk}">
      <h2 class="read__sec"><a class="entry__jump" href="#" title="Open {title}" aria-label="Open {title}">{title}</a></h2>{bait}
      <span class="entry__acts">
        <button type="button" class="entry__ctrl">{EYE}<span class="entry__ctrl-label">Preview</span></button>
        <button type="button" class="entry__ctrl">{PENCIL}<span class="entry__ctrl-label">Edit</span></button>
        <button type="button" class="entry__ctrl entry__ctrl--danger">{TRASH}<span class="entry__ctrl-label">Delete</span></button>
      </span>
    </section>"""


def box(label, width):
    return f"""    <figure>
      <figcaption>{label} — <code>{width}px</code></figcaption>
      <div class="pbox" style="--w:{width}px">
        <article class="read" data-kind="tatib"><div class="read__body">
{entry(SHORT, 1)}
{entry(LONG, 2, long_title=True)}
        </div></article>
      </div>
    </figure>"""


SHELL = ('data-nav="open" data-ch="open" data-read="on" data-home="reading" '
         'data-section="tatib" data-ch-mode="song" data-browser-offline="false" '
         'data-bible-edition="tb"')

BASE_CSS = """
  body {
    display: block;  /* the product's body is a flex shell; this page is not */
    margin: 0; padding: 26px 22px 70px;
    background: var(--canvas); color: var(--ink);
    font: 14px/1.5 ui-sans-serif, system-ui, sans-serif;
  }
  header { display: flex; align-items: baseline; gap: 16px; margin-bottom: 6px; }
  h1 { font: 640 17px/1.3 ui-sans-serif, system-ui, sans-serif; margin: 0; letter-spacing: .01em; }
  .sub { color: var(--head-ink); font-size: 13px; margin: 0 0 24px; max-width: 80ch; }
  #themeBtn { margin-left: auto; }
  .variant { margin: 0 0 34px; }
  .variant h2 {
    font: 640 13px/1.4 ui-sans-serif, system-ui, sans-serif; letter-spacing: .06em;
    text-transform: uppercase; color: var(--head-ink); margin: 0 0 4px;
  }
  .variant p.why { margin: 0 0 14px; color: var(--head-ink); max-width: 82ch; font-size: 13px; }
  .pair { display: flex; gap: 34px; align-items: flex-start; flex-wrap: wrap; }
  figure { margin: 0; }
  figcaption { font: 500 11.5px/1.4 ui-sans-serif, system-ui, sans-serif; color: var(--head-ink);
               letter-spacing: .04em; margin-bottom: 6px; }
  .pbox {
    width: var(--w); padding: 10px 0;
    background: var(--canvas);
    border: 1px dashed var(--divider); border-radius: 10px;
  }
  .pbox .read { width: 100%; }
  iframe { border: 1px dashed var(--divider); border-radius: 10px; background: var(--canvas); }
"""

THEME_JS = """
document.getElementById('themeBtn').addEventListener('click', () => {
  const root = document.documentElement;
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
});
"""


def head(title):
    return f"""<!doctype html>
<html lang="en" data-theme="light" data-theme-mode="system" {SHELL}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../../../static/styles/design/tokens.css">
<link rel="stylesheet" href="../../../static/styles/design/components.css">
<style>{BASE_CSS}</style>
</head>
<body>
"""


def desktop():
    header = ('<header><h1>Where the entry controls sit</h1>'
              '<button type="button" id="themeBtn" class="entry__ctrl">Theme</button></header>')
    intro = ('<p class="sub">The controls keep their labels wherever the window has room and sit in a '
             'column of their own, so a title is never drawn under them. Below 720px the labels collapse '
             'to icons — the breakpoint at which the rail becomes a phone toolbar. Hover an entry to '
             'reveal the controls; hover a title for the underline.</p>')
    block = f"""<section class="variant">
  <h2>Desktop and laptop</h2>
  <p class="why">The pane is what has to hold the words. At a 1440px window with both sidebars open it is 400px — too narrow for the labels — so the controls are icons and the title keeps its one line. At 1920px it is 880px, the labels return, and the title column reserves 264px.</p>
  <div class="pair">
{box('1440px window, both sidebars open', 400)}
{box('1920px window', 880)}
  </div>
</section>
<section class="variant">
  <h2>Phone</h2>
  <p class="why">At 390px the labels give way to three icons and the reserved column narrows to 106px. The phone stage is the same page in a 390px frame.</p>
  <iframe src="phone.html" width="390" height="640" title="The stage at 390px"></iframe>
</section>
<script>{THEME_JS}</script>
</body>
</html>
"""
    (HERE / 'controls.html').write_text(head('Spec 140 — where the entry controls sit')
                                        + header + intro + block)


def phone():
    header = '<header><h1>390px</h1><button type="button" id="themeBtn" class="entry__ctrl">Theme</button></header>'
    intro = ('<p class="sub">Labels collapsed; the reserved column is 106px. A touch screen never '
             'hovers, so this is the resting paint.</p>')
    block = f"""<section class="variant">
  <div class="pair">
{box('phone stage', 390)}
  </div>
</section>
<script>{THEME_JS}</script>
</body>
</html>
"""
    (HERE / 'phone.html').write_text(head('Spec 140 — the stage on a phone') + header + intro + block)


if __name__ == '__main__':
    desktop()
    phone()
    print(HERE / 'controls.html')
    print(HERE / 'phone.html')
