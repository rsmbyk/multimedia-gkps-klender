# Plan 029: Single-screen text entry

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-031
- **Bump:** minor

## Why

A text entry is split into screens of two lines by `_line_pairs()` (spec 006), which is right for
lyrics and liturgies read line by line. Some texts — a whole prayer, a long announcement — are
wanted whole, on one screen. Add a **Single-Screen Text** kind: the entire body on one screen, the
font shrinking until it fits, and only if it cannot shrink further, ellipsized.

## Scope / edges

**In:**

- A new `ServiceEntryKind` value, `SINGLE_SCREEN_TEXT = 4` (label "Single-Screen Text", URL slug
  `single_screen_text` derived from the enum name). It shares the text rules: `clean()` requires a
  non-empty `text`, and `resolve()` returns `(title, text)`.
- An editor form and an add button for it, alongside Passage / Song / Text / Break.
- The projector renders its whole body on **one** screen — no `_line_pairs()` splitting. Blank
  lines stay as paragraph breaks on that one screen.
- The projector's fit loop shrinks the font until the text fits; there is no readable minimum (the
  loop goes as small as it will). Only if it still overflows at that smallest size is the text
  hard-truncated and a literal "…" appended, so it never overflows the screen (owner's decision:
  hard truncation, not CSS clamp).
- The reading pane shows it like a text entry (its own full text, then subject to spec 031's clamp).

**Out:**

- The existing **Text** kind and its two-line splitting (spec 006) — unchanged.
- Scripture, song, and section break rendering.
- Any change to the OBS dock / source.

## Approach

- `multimedia/tatib/models.py` — add `SINGLE_SCREEN_TEXT = 4` to `ServiceEntryKind`; extend
  `clean()` so this kind requires `text`; `resolve()`'s final branch already returns
  `(title, text)`. Generate the choices migration.
- `multimedia/web/reading/entries.py` — add the kind to `KINDS`, map it to `TextEntryForm` in
  `FORMS`, and give it a `TITLES` entry so the modal reads "New single-screen text". `kind_name()`
  yields `single_screen_text` from the enum name.
- `multimedia/web/templates/reading/tatib.html` — add the add button to the per-item add bar and
  the empty-state actions.
- `multimedia/web/reading/views.py` — in `_projector_screens()`, route this kind to a single screen
  carrying the whole body (split on `\n`, blanks preserved), and mark it as single-fit so the
  template can flag it. Do not call `_line_pairs()`.
- `multimedia/web/templates/reading/projector.html` — render the single-fit marker on the section.
- `static/web/projector.js` — in the fit path, for a single-fit screen, keep the shrink loop and,
  when it bottoms out while still overflowing, truncate the trailing content and append "…"; re-run
  on resize (already wired via `render(true)`).
- `static/web/entries.js` — the add button carries `data-entry-open="single_screen_text"`; the kind
  flows through the existing new/edit plumbing with no extra code.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — the kind's `clean()` rules; `kind_name()` /
  `KINDS` round trip; `_projector_screens()` yields one screen for a multi-line body with blanks
  preserved; the projector marks the screen as single-fit; the editor form is offered.
- E2E: `tests/e2e/test_projector.py` — the whole body shows on one screen; the font shrinks to fit;
  a body too long to fit at the smallest size is ellipsized, not overflowed.

## Risks

- **Unreadably small text.** No readable minimum is a deliberate owner choice; the operator sees it.
- **Truncation timing.** The fit/truncate pass must run after fonts load and on resize, or a late
  font swap can overflow the screen.
- **Kind sprawl.** `kind_name()` derives the slug from the enum name; keep the enum name and the URL
  slug in step.
