"""Measure the song page's add-verse controls on the live preview (spec 224).

Run: .venv/bin/python specs/224-empty-song-add-verse-row/preview/probe.py
Writes preview/measurements.json and preview/shots/*.png (shots are gitignored).
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
BASE = 'http://127.0.0.1:8770'
OUT = HERE / 'measurements.json'
SHOTS = HERE / 'shots'

PAGES = {
    'empty_song': '/songs/1731/',       # Lang Margogoh Au — no live verses
    'song_with_verses': '/songs/1387/',  # Anggo Marhorja Tonduy In — three verses
    'tatib_empty': '/tatib/145/',       # the empty-state reference title
}


def box(page, selector):
    el = page.locator(selector).first
    if el.count() == 0:
        return None
    r = el.bounding_box()
    return None if r is None else {k: round(v, 1) for k, v in r.items()}


def main():
    SHOTS.mkdir(exist_ok=True)
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, path in PAGES.items():
            page = browser.new_page(viewport={'width': 1440, 'height': 900})
            page.goto(BASE + path, wait_until='networkidle')
            result[name] = {
                'url': path,
                'add_button_count': page.locator('[data-add-verse]').count(),
                'add_row_count': page.locator('.verse-add').count(),
                'add_row': box(page, '.verse-add'),
                'add_row_button': box(page, '.verse-add .verse-add__btn'),
                'empty_invitation': box(page, '.entry__empty'),
                'empty_button': box(page, '.entry__empty .verse-add__btn'),
                'verse_rows': page.locator('p.v').count(),
                'empty_title': box(page, '.entry__empty-title'),
            }
            page.screenshot(path=str(SHOTS / f'{name}.png'), full_page=True)
            page.close()
        browser.close()
    OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
