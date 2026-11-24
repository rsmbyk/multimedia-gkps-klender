#!/usr/bin/env python3
"""Live probe for spec 238: measure and exercise the passage search comboboxes."""
import json

from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8792'
FIELDS = ['#entry-book-search', '#entry-chapter-search', '#entry-verse_start-search']


def geom(page, selector):
    return page.eval_on_selector(selector, """el => {
      const s = getComputedStyle(el), r = el.getBoundingClientRect();
      return {tag: el.tagName, type: el.type || '', h: +r.height.toFixed(2),
              w: +r.width.toFixed(2), radius: s.borderRadius, font: s.font,
              border: s.borderColor, bg: s.backgroundColor,
              placeholder: el.placeholder, disabled: el.disabled,
              value: el.value, ariaExpanded: el.getAttribute('aria-expanded')};
    }""")


def main():
    out = {}
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' and '63174' not in m.text else None)
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(BASE + '/tatib/151/', wait_until='networkidle')

        # Open the passage modal.
        page.locator('[data-entry-open="scripture"]').first.dispatch_event('click')
        page.wait_for_selector('dialog[open]')
        page.wait_for_timeout(300)

        out['fields_before'] = {s: geom(page, s) for s in FIELDS}
        out['book_options_total'] = page.locator('#entry-book-options [data-book]').count()

        # Book: focus, group count, type-to-filter, keyboard choose.
        book = page.locator('#entry-book-search')
        book.focus()
        page.wait_for_timeout(100)
        out['book_focus'] = {
            'menu_open': page.locator('#entry-book-menu').is_visible(),
            'expanded': book.get_attribute('aria-expanded'),
            'selected_len': page.evaluate("() => { const e=document.activeElement; return e.selectionEnd-e.selectionStart; }"),
            'visible_options': page.locator('#entry-book-options [data-book]:not([hidden])').count(),
            'groups_visible': page.locator('#entry-book-options [data-picker-group]:not([hidden])').count(),
        }
        book.fill('mat')
        page.wait_for_timeout(250)
        out['book_filter_mat'] = {
            'visible': page.locator('#entry-book-options [data-book]:not([hidden])').count(),
            'labels': page.locator('#entry-book-options [data-book]:not([hidden]) .book__n').all_text_contents()[:12],
            'active': page.locator('#entry-book-options [data-book].is-active').count(),
        }
        book.press('Enter')
        page.wait_for_timeout(500)
        out['book_chosen'] = {
            'value': book.input_value(),
            'hidden': page.locator('#id_book_translation').input_value(),
            'menu_open': page.locator('#entry-book-menu').is_visible(),
            'chapter_disabled': page.locator('#entry-chapter-search').is_disabled(),
        }
        page.locator('#editorTitle').click()
        book.focus()
        page.wait_for_timeout(120)
        out['book_refocus'] = page.evaluate(
            "() => { const e=document.querySelector('#entry-book-search');"
            " return {len:e.value.length, sel:e.selectionEnd-e.selectionStart}; }")

        # Chapter: type-to-filter + keyboard choose.
        chapter = page.locator('#entry-chapter-search')
        out['chapter_after_book'] = geom(page, '#entry-chapter-search')
        chapter.focus()
        page.wait_for_timeout(120)
        out['chapter_focus'] = {
            'options': page.locator('#entry-chapter-options [data-picker-option]:not([hidden])').count(),
            'menu_open': page.locator('#entry-chapter-menu').is_visible(),
        }
        chapter.fill('1')
        page.wait_for_timeout(220)
        out['chapter_filter_1'] = {
            'visible': page.locator('#entry-chapter-options [data-picker-option]:not([hidden])').count(),
            'labels': page.locator('#entry-chapter-options [data-picker-option]:not([hidden])').all_text_contents()[:10],
        }
        chapter.press('ArrowDown')
        page.wait_for_timeout(60)
        out['chapter_active_after_arrow'] = page.locator('#entry-chapter-options [data-picker-option].is-active').count()
        chapter.press('Enter')
        page.wait_for_timeout(500)
        out['chapter_chosen'] = {
            'value': chapter.input_value(),
            'hidden': page.locator('#id_chapter').input_value(),
            'from_disabled': page.locator('#entry-verse_start-search').is_disabled(),
        }

        # From verse: type-to-filter + click choose.
        frm = page.locator('#entry-verse_start-search')
        out['from_after_chapter'] = geom(page, '#entry-verse_start-search')
        frm.focus()
        page.wait_for_timeout(120)
        out['from_focus'] = {
            'options': page.locator('#entry-verse_start-options [data-picker-option]:not([hidden])').count(),
            'menu_open': page.locator('#entry-verse_start-menu').is_visible(),
        }
        frm.fill('1')
        page.wait_for_timeout(220)
        out['from_filter_1'] = {
            'visible': page.locator('#entry-verse_start-options [data-picker-option]:not([hidden])').count(),
            'labels': page.locator('#entry-verse_start-options [data-picker-option]:not([hidden])').all_text_contents()[:10],
        }
        page.locator('#entry-verse_start-options [data-picker-option]:not([hidden])').first.click()
        page.wait_for_timeout(300)
        out['from_chosen'] = {
            'value': frm.input_value(),
            'hidden': page.locator('#id_verse_start').input_value(),
            'to_disabled': page.locator('#entry-verse_end-trigger').is_disabled(),
        }

        out['checkpoints'] = {}
        def snap(label):
            out['checkpoints'][label] = {
                'chapter_field': page.locator('#entry-chapter-search').input_value(),
                'chapter_hidden': page.locator('#id_chapter').input_value(),
                'from_field': page.locator('#entry-verse_start-search').input_value(),
                'from_hidden': page.locator('#id_verse_start').input_value(),
                'book_field': page.locator('#entry-book-search').input_value(),
                'book_hidden': page.locator('#id_book_translation').input_value(),
            }

        snap('after_from_chosen')
        # Escape and outside click.
        page.locator('#entry-chapter-search').focus()
        page.wait_for_timeout(120)
        page.locator('#entry-chapter-search').press('Escape')
        snap('after_escape')
        out['escape_closes'] = {
            'menu_visible': page.locator('#entry-chapter-menu').is_visible(),
            'dialog_open': page.locator('dialog[open]').count() > 0,
        }
        page.locator('#entry-verse_start-search').focus()
        page.wait_for_timeout(120)
        page.locator('#editorTitle').click()
        page.wait_for_timeout(80)
        snap('after_outside')
        out['outside_closes'] = {
            'menu_visible': page.locator('#entry-verse_start-menu').is_visible(),
            'expanded': page.locator('#entry-verse_start-search').get_attribute('aria-expanded'),
        }

        out['fields_after'] = {s: geom(page, s) for s in FIELDS}
        out['errors'] = errors[:10]
        print(json.dumps(out, indent=2, ensure_ascii=False))
        browser.close()


if __name__ == '__main__':
    main()
