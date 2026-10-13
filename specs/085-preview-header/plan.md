# Plan 085: Show the entry's identity in the Preview dialog's header

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-088
- **Bump:** patch

## Why

The Preview dialog has no header at all (spec 032 built it headerless on purpose): its body starts
straight into the entry, so the thing being previewed is identified by a line that scrolls away with the
content.

```html
<dialog class="preview" id="previewModal" aria-label="Preview">
  <div class="preview__body" id="previewContent" tabindex="0"></div>
```

Inside that body each kind prints its own identity line — `.preview__ref` for a Text title or a passage
reference, `.preview__song` for a song's `HAL 3 — Sai puji Naibata` heading, with the song's verse tabs
under it. The owner wants that identity pinned in a header above the scroll, and the verse tabs belong
there with it.

## Scope / edges

**In:**

- The Preview dialog's chrome: a header region and what it carries for every kind.
- The Text title, the passage reference, the song heading, and the song verse tabs.
- Accessibility naming of the dialog, and the script's tab wiring scope.

**Out:**

- The body's content, the screen-break controls and footer (spec 069/079), the unread-notice, the
  tablist's own geometry (spec 073), and the entry pane's Preview triggers.
- Adding a close button: Escape, the overlay, and the body's own dismissal stay the ways out, as the
  editor dialog also has no `x`.

## Approach

Give the dialog a `.preview__head` above `.preview__body`, in the same flex column the footer already
uses, so the header does not scroll with the body. The header's identity line is filled per kind from
the same data the body used to print, and the song's `.preview__tabs` moves into the row beside it. The
dialog keeps `aria-label="Preview"` when it has no identity to show and switches to `aria-labelledby`
when it has one. On close, the header is cleared with the body.

## TDD

- Domain/app tests: N/A — the preview markup is a script template already covered by the view tests;
  the header adds no new server rule.
- E2E (Playwright): `tests/e2e/test_entry_preview.py` — a passage preview, a song preview with its tabs,
  a titled and an untitled Text preview, and the overlay/Escape dismissal. Also the break suites that
  drive the footer and the body (`test_text_screen_breaks.py`, `test_unified_text_screen_mode.py`,
  `test_single_screen_text_breaks.py`) for regressions, and `tests/e2e/test_tatib_hover.py` for the
  origin highlight while the modal is open.

## Risks

- Moving the tabs out of `#previewContent` breaks `wireTabs(content)`, which queries within the body:
  it has to scan the whole dialog, or the tab clicks die silently on the current build.
- `#previewContent` is a focusable scroller with its own arrow-key handling; the header must not add a
  second tab stop or steal that focus.
- Song headings can be long; the header must truncate rather than wrap the tabs out of reach.
