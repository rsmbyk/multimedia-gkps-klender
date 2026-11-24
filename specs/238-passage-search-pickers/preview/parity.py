#!/usr/bin/env python3
"""Measure the passage combobox against the song combobox on the live slice."""
import json

from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8792'


def box(page, sel):
    return page.eval_on_selector(sel, """el => {
      const s = getComputedStyle(el), r = el.getBoundingClientRect();
      return {h: +r.height.toFixed(2), w: +r.width.toFixed(2),
              x: +r.x.toFixed(2), y: +r.y.toFixed(2),
              radius: s.borderRadius, font: s.font, border: s.borderColor,
              bg: s.backgroundColor, color: s.color};
    }""")


def main():
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(BASE + '/tatib/151/', wait_until='networkidle')
        page.locator('[data-entry-open="scripture"]').first.dispatch_event('click')
        page.wait_for_selector('dialog[open]')
        page.wait_for_timeout(250)
        out['passage'] = box(page, '#entry-book-search')
        page.locator('#entry-book-search').focus()
        page.wait_for_timeout(150)
        out['book_menu'] = box(page, '#entry-book-menu') if page.locator('#entry-book-menu').is_visible() else None
        page.keyboard.press('Escape')

        page.locator('[data-editor-close]').click()
        page.wait_for_timeout(150)
        page.locator('[data-entry-open="song"]').first.dispatch_event('click')
        page.wait_for_selector('dialog[open]')
        page.wait_for_timeout(250)
        out['song'] = box(page, '#entry-song-search')
        page.locator('#entry-song-search').focus()
        page.wait_for_timeout(150)
        out['song_menu'] = box(page, '#entry-song-menu') if page.locator('#entry-song-menu').is_visible() else None
        print(json.dumps(out, indent=2))
        browser.close()


if __name__ == '__main__':
    main()
