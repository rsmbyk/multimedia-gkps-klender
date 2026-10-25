"""Measure the Break control's removal (spec 131).

Opens the served branch, photographs the two surfaces that offer the retired kind --
an add row beside an item and the empty service's action row -- reads the geometry
before and after deleting the Break control from the live DOM, and saves both frames.
The "after" frame is the project's own markup and stylesheet with one button removed,
so it is a materials-faithful preview rather than a redraw.

On the finished branch there is no control to remove, so both readings are the shipped
one; pass `--shipped` to photograph that state under its own names:

    python specs/131-retire-break-entry/preview/probe_break_controls.py            # the gate-1 preview
    python specs/131-retire-break-entry/preview/probe_break_controls.py --shipped  # the shipped surfaces

Both run against a dev server on 127.0.0.1:8803.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8803'
SERVICE_WITH_ITEMS = 144
SERVICE_EMPTY = 145
OUT = Path(__file__).resolve().parent


def read_add_row(page):
    return page.evaluate("""() => {
        const rows = [...document.querySelectorAll('.entry__add')];
        const row = rows.find(r => r.getBoundingClientRect().height > 0) || rows[0];
        const box = row.querySelector('.entry__add-inner').getBoundingClientRect();
        const buttons = [...row.querySelectorAll('.entry__add-btn')].map(b => {
            const r = b.getBoundingClientRect();
            return {label: b.textContent.trim(), kind: b.dataset.entryOpen,
                    x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width),
                    h: Math.round(r.height)};
        });
        const centre = document.querySelector('#readBody').getBoundingClientRect();
        return {box: {w: Math.round(box.width), h: Math.round(box.height),
                      x: Math.round(box.x)},
                rowCentreOffset: Math.round((box.x + box.width / 2) - (centre.x + centre.width / 2)),
                buttons};
    }""")


def read_empty(page):
    return page.evaluate("""() => {
        const actions = document.querySelector('.entry__empty-actions');
        if (!actions) return null;
        const box = actions.getBoundingClientRect();
        return {box: {w: Math.round(box.width), h: Math.round(box.height),
                      x: Math.round(box.x)},
                buttons: [...actions.querySelectorAll('.entry__empty-btn')].map(b => {
                    const r = b.getBoundingClientRect();
                    return {label: b.textContent.trim(), kind: b.dataset.entryOpen,
                            w: Math.round(r.width), h: Math.round(r.height)};
                })};
    }""")


def drop_break(page):
    page.evaluate("""() => {
        document.querySelectorAll('[data-entry-open="section_break"]').forEach(b => b.remove());
        /* The empty menu is a five-track grid (spec 130); four kinds make four tracks. */
        const actions = document.querySelector('.entry__empty-actions');
        if (actions) actions.style.gridTemplateColumns = 'repeat(4, minmax(0, 52px))';
    }""")
    page.wait_for_timeout(120)


def main():
    shipped = '--shipped' in sys.argv
    suffix = '-shipped' if shipped else ''
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_context(viewport={'width': 1440, 'height': 900}).new_page()

        page.goto(f'{BASE}/tatib/{SERVICE_WITH_ITEMS}/')
        page.wait_for_load_state('networkidle')
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(400)
        before_row = read_add_row(page)
        page.screenshot(path=str(OUT / f'add-row-before{suffix}.png'),
                        clip=page.locator('.entry__start, .entry__add').first.bounding_box())
        if not shipped:
            drop_break(page)
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(300)
        after_row = read_add_row(page)
        page.screenshot(path=str(OUT / f'add-row-after{suffix}.png'),
                        clip=page.locator('.entry__start, .entry__add').first.bounding_box())

        page.goto(f'{BASE}/tatib/{SERVICE_EMPTY}/')
        page.wait_for_load_state('networkidle')
        before_empty = read_empty(page)
        if before_empty:
            page.screenshot(path=str(OUT / f'empty-before{suffix}.png'),
                            clip=page.locator('.entry__empty').bounding_box())
            if not shipped:
                drop_break(page)
            after_empty = read_empty(page)
            page.screenshot(path=str(OUT / f'empty-after{suffix}.png'),
                            clip=page.locator('.entry__empty').bounding_box())
        else:
            after_empty = None

        browser.close()

    print(json.dumps({'add_row_before': before_row, 'add_row_after': after_row,
                      'empty_before': before_empty, 'empty_after': after_empty}, indent=2))


if __name__ == '__main__':
    main()
