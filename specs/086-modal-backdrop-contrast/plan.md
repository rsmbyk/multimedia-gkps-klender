# Plan 086: Separate the modals from the page behind them

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-089
- **Bump:** patch

## Why

Both dialogs dim the page with the same hard-coded scrim, and it is the same value in both themes:

```css
.editor::backdrop { background: rgba(31, 31, 29, .38); }
.preview::backdrop { background: rgba(31, 31, 29, .38); }
```

In dark mode that is a scrim barely lighter than the surface beneath it — the dialog's canvas is
`#14130F` and the scrim is `rgba(31, 31, 29, .38)` — so the dialog and the page read as one plane, which
is exactly what the owner's screenshot shows. The dialog's own elevation does not help: `--shadow` in
dark is `0 6px 18px -10px rgba(0, 0, 0, .9)`, an 18px blur pulled back by a −10px spread. The dialog
also has no border at all (`border: 0`).

## Scope / edges

**In:**

- The scrim behind the entry Preview and the sidebar editor dialogs, and behind the Preview's own mode
  confirmation.
- The dialogs' edge: border and elevation.
- Both themes, through new tokens rather than new literals.

**Out:**

- The dialogs' size, radius, padding, contents, and behaviour.
- Blurring the page: spec 065 deliberately keeps the origin entry's highlight readable *behind* the
  scrim, so the scrim stays translucent and no `backdrop-filter` is introduced.
- The legacy OBS docks and the projector page.

## Approach

Move the scrim and the dialog elevation into the token layer, where they can differ by theme:

- `--backdrop`: light `rgba(20, 20, 18, .52)`, dark `rgba(0, 0, 0, .68)`.
- `--shadow-dialog`: light `0 20px 55px -24px rgba(20, 20, 18, .55)`,
  dark `0 26px 64px -26px rgba(0, 0, 0, .9)`.

Then point the two `::backdrop` rules and `.preview__confirm-layer` at `--backdrop`, give both dialogs a
`1px solid var(--divider)` edge and `--shadow-dialog`, and leave `--shadow` alone for the tooltips and
the drag copy that already use it.

The tokens test parses only `#rrggbb` values, so the two rgba tokens do not enter its pair list; the
scrim is not a text pair and is not asserted there.

## TDD

- Domain/app tests: N/A — visual only; `tests/test_design_tokens.py` keeps passing unchanged.
- E2E (Playwright): `tests/e2e/test_editor.py` and `tests/e2e/test_entry_preview.py` for the dialog
  still opening, closing, and being hit-testable; a computed-style check on the backdrop's colour in
  both themes.

## Risks

- A darker scrim must not swallow the origin entry's highlight that spec 065 preserves behind the
  backdrop; the preview shows that entry through the new scrim so the owner can confirm it stays
  readable.
- `::backdrop` is not a real element: Playwright reads it through `getComputedStyle(el, '::backdrop')`,
  which only Chrome supports reliably. The check belongs in the E2E module that already runs in
  Chromium.
