# Plan 060: Distinct song label typography

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-062
- **Bump:** patch

## Why

The screenshot renders the song reference, title, and lyric verse selection with nearly identical emphasis. Distinct typography will help the operator scan entries.

## Scope / edges

**In:** three independently styled text regions within existing song rows.

**Out:** redesigning the sidebar or changing its behavior and data.

## Approach

1. Build from current Spec 057, which adds the second-line verse label in the same sidebar.
2. Give the reference, title, and lyric verse selection separate semantic elements in the TOC renderer.
3. Apply scoped styles using the existing font and palette, keeping dark-theme contrast readable. Preserve safe rendering and row interactions.
4. Verify representative entries, long titles, narrow widths, both themes, and contrast in Playwright.

## TDD

- Domain/app tests: none for presentation alone; use TDD if a formatting rule proves necessary.
- E2E: `tests/e2e/test_song_label_typography.py`; run `python manage.py test tests.e2e.test_song_label_typography` after identifying the page and adding meaningful acceptance coverage.
- Regression: `DATABASE_URL=<local PostgreSQL URL> python manage.py test multimedia.web.tests.ServiceEntryViewTests --noinput`.

## Risks

- Screenshot source is not yet identified; do not invent a replacement sidebar.
- Muted metadata must retain readable contrast on the selected background.
- Splitting an existing flat label must not corrupt song titles or reference-free songs.
