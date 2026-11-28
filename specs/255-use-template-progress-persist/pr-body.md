## What

Use template progress now lives in `localStorage` instead of `sessionStorage`, as a `v: 2` record
carrying a `savedAt` timestamp. Every settled slot, choice pick, step, name and date change rewrites
that timestamp, so the draft lasts **seven days (168 hours) from the last change**; an older record is
treated as absent and removed, and stale keys are swept at load and after a stage swap. A template
with a live draft marks its **Use template** button with a 7 × 7 px corner dot, 4 px inset from the
border box, and the button's accessible name becomes “Use template, draft saved” — the label and the
button's width are unchanged. The leave confirmation now says the progress is saved **on this browser
for seven days** rather than “in this browser session”, which the new lifetime made false.

## Why

`specs/255-use-template-progress-persist/spec.md`; card `ITEM-276`. Spec 253 (ITEM-270) kept progress
for one browser session, so closing the browser lost the work, and nothing on the stage said a draft
existed.

## Evidence

- **Verification**: 25 test · 0 inspection · 0 manual
- **Convergence**: Converged in 1 pass · accepted gaps: none
- **Folded**: `docs/spec/reading.md` — R67 added (R66 was taken by spec 257)
- **Board**: `ITEM-276` → In review
- **Refs** #657

69 E2E tests pass: the new module 16/16, spec 253's module 15/15 (its store assertions moved to
`localStorage`/`v: 2`, and its leave-confirmation assertion to the new wording), and
`tests.e2e.test_tatib_templates` 38/38 — zero console errors, re-run after rebasing onto `develop`
with spec 257's modal-scroll change. The indicator was chosen at Gate 1 from a three-variant preview
(`preview/index.html`, probe 10/10, chat-frame verifier PASS).

## Risk

Client-only: no model, migration, endpoint or template write. Records written by spec 253's session
store are not migrated and simply expire with that session — that feature reached `develop` today and
production does not carry it. A browser that refuses storage still opens and operates the modal, with
no mark and no resume. Reverting the squash commit restores the session-scoped behaviour with no data
migration.