"""Assemble the spec-160 preview from the projector template itself.

Reads the template **as `develop` has it** — `git show develop:<path>` — so the "today" copy stays
the sheet before this slice even after the slice lands, applies this slice's change for the "after"
copy, and writes `preview/preview.html` under the product's real `fonts.css`, `tokens.css` and
`projector.css`. Nothing here retypes a row.
"""
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RELATIVE = "multimedia/web/templates/reading/projector_controls.html"
BASE_REV = "develop"

SYMBOLS = re.compile(r'<svg xmlns="http://www\.w3\.org/2000/svg" style="display:none">.*?</svg>\n', re.S)
SHEET = re.compile(r'  <div class="sheet" id="key-list">.*?\n  </div>\n', re.S)

SPACE_ROW = ('<p class="row"><span class="fn">Play/Pause</span><span class="combo"><span class="chord">'
             '<span class="k sp glyph" title="Space" aria-label="Space"><span class="space-mark">␣</span>'
             '</span></span></span></p>')
GROUP = ('      <section class="group">\n'
         '        <h3>{heading}</h3>\n'
         '        {row}\n'
         '      </section>\n')


def after(sheet: str) -> str:
    """The sheet with Display's combined row removed and Audio + Video appended to column two."""
    combined = re.compile(r'        <p class="row"><span class="fn">Audio/Video Play/Pause</span>.*?</p>\n')
    assert len(combined.findall(sheet)) == 1, "expected exactly one combined row"
    sheet = combined.sub("", sheet)

    stacks = [m.start() for m in re.finditer(r'    <div class="stack">', sheet)]
    assert len(stacks) == 3, "expected three columns"
    end = sheet.index("    </div>\n", stacks[1])          # the second column's closing tag
    added = GROUP.format(heading="Audio", row=SPACE_ROW) + GROUP.format(heading="Video", row=SPACE_ROW)
    return sheet[:end] + added + sheet[end:]


def read_base_template() -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{BASE_REV}:{RELATIVE}"],
        capture_output=True, text=True, check=True,
    ).stdout


def build() -> str:
    template = read_base_template()
    symbols_match = SYMBOLS.search(template)
    sheet_match = SHEET.search(template)
    assert symbols_match and sheet_match, "the template's symbol sheet or sheet markup moved"
    symbols = symbols_match.group(0).rstrip("\n")
    sheet = sheet_match.group(0).rstrip("\n")
    body_today = sheet.replace('id="key-list"', 'id="sheet-today"')
    body_after = after(sheet).replace('id="key-list"', 'id="sheet-after"').replace(
        'class="sheet"', 'class="sheet preview-off"', 1)
    return PAGE.format(symbols=symbols, today=indent(body_today, 1), after=indent(body_after, 1))


def indent(block: str, levels: int) -> str:
    pad = "  " * levels
    return "\n".join(pad + line if line.strip() else line for line in block.splitlines())


PAGE = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Projector shortcuts sheet — spec 160 preview</title>
<!-- The product's own stylesheets, unmodified. -->
<link rel="stylesheet" href="../../../static/styles/design/fonts.css">
<link rel="stylesheet" href="../../../static/styles/design/tokens.css">
<link rel="stylesheet" href="../../../static/styles/design/projector.css">
<style>
  /* Preview chrome only: nothing here styles the product's sheet. */
  .preview-off {{ display: none !important; }}
  /* A stage tall enough for the whole sheet even in a short frame; the sheet keeps its real size. */
  body.projector {{ min-height: 720px; }}
  .preview-bar {{
    position: fixed; left: 16px; top: 16px; z-index: 9;
    display: flex; align-items: center; gap: 14px;
    padding: 8px 10px 8px 12px; border-radius: 8px;
    background: #14120f; border: 1px solid #3a372f;
    font: 12px/1.4 ui-sans-serif, system-ui, sans-serif; color: #b9b3a7;
  }}
  .preview-bar b {{ color: #ffd166; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; font-size: 10px; }}
  .preview-bar button {{
    font: inherit; color: #e8e4dc; background: #241f1a; border: 1px solid #4a463f;
    border-radius: 6px; padding: 4px 10px; cursor: pointer;
  }}
  .preview-bar button[aria-pressed="true"] {{ background: #3a3225; border-color: #6b5f45; color: #ffd166; }}
  .preview-bar output {{ font-variant-numeric: tabular-nums; color: #8e8a80; }}
</style>
</head>
<body class="projector keys-open">

{symbols}

  {today}

  {after}

<div class="preview-bar" role="group" aria-label="Preview">
  <b>Preview</b>
  <button type="button" data-variant="today" aria-pressed="false">Today</button>
  <button type="button" data-variant="after" aria-pressed="true">After</button>
  <output id="readout"></output>
</div>

<script>
  var sheets = {{ today: document.getElementById('sheet-today'), after: document.getElementById('sheet-after') }};
  var buttons = document.querySelectorAll('.preview-bar button');
  var readout = document.getElementById('readout');

  function show(variant) {{
    Object.keys(sheets).forEach(function (key) {{
      sheets[key].classList.toggle('preview-off', key !== variant);
    }});
    buttons.forEach(function (button) {{
      button.setAttribute('aria-pressed', String(button.dataset.variant === variant));
    }});
    measure(variant);
  }}

  function measure(variant) {{
    var sheet = sheets[variant];
    var box = sheet.getBoundingClientRect();
    var limit = window.innerHeight - 32;
    readout.textContent = Math.round(box.width) + ' × ' + Math.round(box.height)
      + 'px · limit ' + Math.round(limit) + 'px · '
      + (sheet.scrollHeight > Math.ceil(box.height) ? 'scrolls' : 'fits');
  }}

  buttons.forEach(function (button) {{
    button.addEventListener('click', function () {{ show(button.dataset.variant); }});
  }});

  document.addEventListener('keydown', function (event) {{
    if (event.key === 't' || event.key === 'T') show('today');
    if (event.key === 'a' || event.key === 'A') show('after');
  }});

  window.addEventListener('resize', function () {{
    measure(document.querySelector('.preview-bar button[aria-pressed="true"]').dataset.variant);
  }});

  show('after');
</script>
</body>
</html>
"""

if __name__ == "__main__":
    out = HERE / "preview.html"
    out.write_text(build())
    print(f"wrote {out} ({out.stat().st_size} bytes)")
