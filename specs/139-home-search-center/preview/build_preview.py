"""Rebuild the slice's static preview from the rendered landing page.

The preview is the real page: the HTML the server renders, the project's own
stylesheets and assets, and one extra file — `after.css` — holding only the
rules this slice changes. `before-home.html` is the same page without it.

    .venv/bin/python specs/139-home-search-center/preview/build_preview.py [source-url]

`source-url` is any running instance of this project whose landing page renders
today's markup (the default is the compose `web` service). Nothing is written
outside this directory.
"""
import pathlib
import re
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:63404/"
TO_STATIC = "../../../static/"


def fetch() -> str:
    with urllib.request.urlopen(SOURCE, timeout=20) as response:
        return response.read().decode("utf-8")


def localise(html: str) -> str:
    """Point every /static/ reference at the repository's own `static/` folder."""
    return html.replace('="/static/', f'="{TO_STATIC}').replace("='/static/", f"='{TO_STATIC}")


def main() -> None:
    html = localise(fetch())
    if '="/static/' in html or "='/static/" in html:
        raise SystemExit("a /static/ reference survived the rewrite")
    here = re.search(r'<link rel="shortcut icon"[^>]*>', html)
    (HERE / "before-home.html").write_text(html, encoding="utf-8")
    after = html.replace(
        '<link rel="stylesheet" href="%sstyles/design/components.css">' % TO_STATIC,
        '<link rel="stylesheet" href="%sstyles/design/components.css">\n'
        '<link rel="stylesheet" href="after.css">' % TO_STATIC,
        1,
    )
    if "after.css" not in after:
        raise SystemExit("components.css link not found — the markup changed")
    (HERE / "after-home.html").write_text(after, encoding="utf-8")
    print("wrote before-home.html and after-home.html from", SOURCE, "| favicon:", bool(here))


if __name__ == "__main__":
    main()
