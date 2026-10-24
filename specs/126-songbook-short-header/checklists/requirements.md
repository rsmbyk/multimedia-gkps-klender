# Requirements Checklist: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md` · **Created**: 2026-10-24

Built-in Specify quality gate. Validated immediately after the spec was written; the *"no
`[NEEDS CLARIFICATION]` markers remain"* item is deliberately absent, because markers are Specify's
output and Clarify's exit condition guarantees they are closed.

## Content Quality

- [x] CHK001 The spec states what the header shows, not which function or field produces it. [Content Quality]
- [x] CHK002 No implementation detail leaks into the requirements — the view, the renderer's function names and CSS class names appear only where the spec must name the surface (the header element, the routes). [Content Quality]
- [x] CHK003 Every requirement is testable by reading a rendered page or comparing two rendered documents. [Content Quality]
- [x] CHK004 User stories are ordered and labelled by priority, and US1 alone is a viable slice. [Content Quality]

## Requirement Completeness

- [x] CHK005 The trigger is stated as a class — any song of any hymn songbook — not as the one song in the screenshot. [Completeness]
- [x] CHK006 The unchanged surfaces are enumerated rather than left implied. [Completeness]
- [x] CHK007 The empty-short-name, unnumbered-song, no-citation and soft-deleted-book cases are decided. [Completeness]
- [x] CHK008 Both renderers are covered by a requirement, so the saved view cannot diverge. [Completeness]
- [x] CHK009 Every `FR-###` names the capability it touches, and both capabilities are declared new because no `docs/spec/` tree exists yet. [Completeness]
- [x] CHK010 Success criteria are measurable without naming a test file. [Completeness]

## Feature Readiness

- [x] CHK011 The user-facing outcome is observable on a running page, and the spec says how. [Readiness]
- [x] CHK012 The visual consequence of the shorter text — the header stops wrapping on a narrow stage — is recorded as numbers from the running page. [Readiness]
- [x] CHK013 The two genuinely open choices (the tab title, the ordinary songbook's short name) are marked, not guessed. [Readiness]
- [x] CHK014 Nothing in the spec requires a data, model or migration change. [Readiness]

**Validation run 1 (2026-10-24)**: 14 items, 14 satisfied, 0 failures — 0 iterations needed. Two
`[NEEDS CLARIFICATION]` markers were left by Specify (FR-005, FR-006) and both were closed in Clarify the
same day; the spec now carries none.
