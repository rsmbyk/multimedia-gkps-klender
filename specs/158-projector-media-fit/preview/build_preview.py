"""Build the spec-158 preview from the project's own materials.

Why a script: the preview must carry the projector's real stylesheets — bundled
fonts and cursor files included, or the sheet is measured in a fallback face — and its
real shortcut-sheet markup (glyphs included). A hand-copied sheet drifts the moment
the template changes.

  python3 build_preview.py            # refresh styles, media and markup

The media in `files/` are **generated stand-ins** of the sizes the slice was reviewed
with: a 182×277 portrait, a 787×444 landscape, and a 612×792 pt page. The real files
the review used belong to the service and are not committed — the sizes are what the
preview is for, and a receipt is nobody's test fixture.

What is NOT real, and why:
  * the media bytes live in files/ because a preview page cannot read the local
    Media Library companion (its CORS allowlist names the app's own port);
  * the page is a 4x bitmap rendered from the stand-in PDF, because a static page
    cannot import pdf.js's ES module from file://;
  * preview.js re-implements the fit and the pan; the product's projector.js carries
    the same rules (spec 158, implemented after gate 2).
"""
import pathlib
import re
import shutil
import struct
import subprocess
import zlib

PREVIEW = pathlib.Path(__file__).resolve().parent
REPO = PREVIEW.parents[2]
FILES = PREVIEW / "files"
STYLES = PREVIEW / "styles/design"

CSS = ("projector.css", "tokens.css", "fonts.css")
CURSORS = ("cursor-left.svg", "cursor-right.svg", "cursor-hide.svg",
           "cursor-show.svg", "cursor-fullscreen.svg")
# fonts.css ships beside the CSS and points at ../../assets/fonts; the preview keeps the
# stylesheet verbatim and only re-points those two URLs at the repo's own copies, so a
# 1.2 MB typeface is not committed twice. One rewrite, named here on purpose.
FONT_URL_IN_CSS = '../../assets/fonts/'
FONT_URL_IN_PREVIEW = '../../../../../static/assets/fonts/'
CONTROLS = REPO / "multimedia/web/templates/reading/projector_controls.html"

IMAGE = "image-182x277.png"
LANDSCAPE = "image-787x444.png"
PAGE = "page-612x792.pdf"
PAGE_BITMAP = "page-612x792.png"

NEW_GROUP = (
    '<section class="group">\n'
    '      <h3>Image and PDF</h3>\n'
    '      <p class="row"><span class="fn">Fit Width / Fit Height</span>'
    '<span class="combo"><span class="chord"><span class="k">T</span></span></span></p>\n'
    '    </section>'
)


def copy_assets():
    STYLES.mkdir(parents=True, exist_ok=True)
    for name in CSS + CURSORS:
        shutil.copyfile(REPO / "static/styles/design" / name, STYLES / name)
    fonts = STYLES / "fonts.css"
    fonts.write_text(fonts.read_text().replace(FONT_URL_IN_CSS, FONT_URL_IN_PREVIEW))


def _png(width, height, bands=12):
    """A banded gradient: enough for a crop to be visible at any scale."""
    rows = []
    for y in range(height):
        band = (y * bands) // height
        if (y * bands) % height == 0:
            colour = (247, 243, 233, 255)                      # a bright hairline per band
        else:
            tone = 30 + (band * 120) // max(1, bands - 1)
            colour = (min(255, tone + 90), min(255, tone + 45), tone, 255)
        rows.append(b'\0' + bytes(colour) * width)

    def chunk(kind, content):
        return (struct.pack('!I', len(content)) + kind + content
                + struct.pack('!I', zlib.crc32(kind + content) & 0xffffffff))

    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('!2I5B', width, height, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b''.join(rows), 9)) + chunk(b'IEND', b''))


def _pdf():
    """One 612×792 pt page with a heading and body lines — a document, not a receipt."""
    lines = ["Worship bulletin"]
    lines += [f"Stand-in page for spec 158 — line {n} of 28." for n in range(1, 29)]
    text = []
    text.append("BT /F2 26 Tf 72 700 Td (Worship bulletin) Tj ET")
    for index, line in enumerate(lines[1:]):
        y = 660 - index * 20
        text.append(f"BT /F1 12 Tf 72 {y} Td ({line}) Tj ET")
    stream = "\n".join(text).encode()

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    ]
    data = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, body in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f"{number} 0 obj\n".encode() + body + b"\nendobj\n")
    start = len(data)
    data.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode())
    data.extend(f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n".encode())
    return bytes(data)


def ensure_media():
    """Write the stand-ins, and re-render the page bitmap if the PDF changed."""
    FILES.mkdir(parents=True, exist_ok=True)
    wanted = {IMAGE: _png(182, 277, bands=10), LANDSCAPE: _png(787, 444, bands=14),
              PAGE: _pdf()}
    for name, payload in wanted.items():
        path = FILES / name
        if not path.exists() or path.read_bytes() != payload:
            path.write_bytes(payload)
    bitmap = FILES / PAGE_BITMAP
    if not bitmap.exists() or bitmap.stat().st_mtime < (FILES / PAGE).stat().st_mtime:
        subprocess.run(["pdftoppm", "-png", "-r", "288", "-f", "1", "-l", "1",
                        PAGE, "page-612x792"], cwd=FILES, check=True)
        produced = FILES / "page-612x792-1.png"
        if produced.exists():
            produced.replace(bitmap)


def found(pattern, text, what):
    match = re.search(pattern, text, re.S)
    if not match:
        raise SystemExit(f"cannot find {what} in {CONTROLS}")
    return match


def real_markup():
    source = CONTROLS.read_text()
    symbols = found(r"<svg xmlns=.*?</svg>", source, "the key symbols").group(0)
    sheet = found(r'<div class="sheet" id="key-list">.*?\n  </div>', source,
                  "the shortcut sheet").group(0)
    if "Image and PDF" in sheet:
        return symbols, sheet
    # the new group goes into the middle column, after Library Detour: that column
    # has room, where the third column would push the sheet past a 720p window.
    detour = found(r'<section class="group">\s*<h3>Library Detour</h3>.*?</section>', sheet,
                   "Library Detour")
    sheet = sheet[:detour.end()] + "\n    " + NEW_GROUP + sheet[detour.end():]
    return symbols, sheet


def splice(path, start, end, body):
    text = path.read_text()
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        raise SystemExit(f"markers {start} … {end} not found in {path}")
    path.write_text(pattern.sub(start + "\n" + body + "\n" + end, text, count=1))


def main():
    copy_assets()
    ensure_media()
    symbols, sheet = real_markup()
    page = PREVIEW / "index.html"
    splice(page, "<!-- real-symbols -->", "<!-- /real-symbols -->", symbols)
    splice(page, "<!-- real-sheet -->", "<!-- /real-sheet -->", sheet)
    print("preview rebuilt:", page)


if __name__ == "__main__":
    main()
