# Implementation Plan: The stage's entry links read as text until hovered

**Slice**: `specs/140-stage-link-affordance` · **Branch**: `feat/140-stage-link-affordance`
**Date**: 2026-10-27 · **Status**: Draft (gate 1 accepted the spec on 2026-10-27)
**bump**: `patch` — a user-visible change to how an existing surface looks, not a new capability and
not a stored behaviour. One `CHANGELOG.md` line under `## [Unreleased]` → `### Changed`.

## Technical Context

| | |
| --- | --- |
| Language | Python 3.12, Django 4.0 templates |
| Front end | server-rendered templates, hand-written CSS; no framework, no build step |
| Files | `static/styles/design/components.css` (the rule and the controls' column), `multimedia/web/templates/reading/tatib.html` (the labels wrapped for one collapse rule), `static/styles/design/tokens.css` (the `--link` comment in both theme blocks), `tests/e2e/test_reading.py` (the test it retires) |
| Data | none — no migration, no payload, no endpoint |
| Tests | Playwright E2E through `StaticLiveServerTestCase`, the repository's user-visible acceptance layer |
| Constraints | only `.entry__jump` changes; `--link` and every other anchor keep today's treatment; no new token, font, icon or dependency |

## Constitution Check

`CONSTITUTION.md` does not exist and is never auto-created (SDD-01).

- Before Phase 0: n/a — no constitution.
- After Phase 1: n/a — no constitution.

## Phase 0 — Research

See `research.md`. Six decisions, **unknowns remaining: 0**.

## Phase 1 — Design

- `data-model.md` — no entities; the invariants the rule must keep.
- `contracts/` — `none`: no endpoint, payload or module interface. The only seam is a CSS class the
  template already emits.
- `quickstart.md` — the commands that serve the page and run the four suites.

### The change

```css
/* components.css, replacing the spec 056 rule */
.entry__jump { color: inherit; text-decoration: none; }
.entry__jump:hover,
.entry__jump:focus-visible {
  text-decoration: underline;
  text-underline-offset: 3px;
}
```

`tokens.css`: both `--link` comments stop naming the stage and name the surface that still uses the
token — the media library's "used by" links.

```css
/* components.css: the controls' own column, so no title is drawn under them.
   The question is the pane's width, not the window's, so the pane is the
   container the rules ask. */
.read__body { container: stage-pane / inline-size; }
.tatib__item--acts { padding-right: 106px; }
@container stage-pane (min-width: 700px) {
  .tatib__item--acts { padding-right: 264px; }
}

/* the labels collapse while the pane is narrow, staying in the accessibility tree */
.entry__ctrl { gap: 0; padding: 5px 6px; }
.entry__ctrl .entry__ctrl-label {
  position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0;
  overflow: hidden; clip-path: inset(50%); white-space: nowrap;
}
@container stage-pane (min-width: 700px) {
  .entry__ctrl { gap: 6px; padding: 5px 10px; }
  .entry__ctrl .entry__ctrl-label {
    position: static; width: auto; height: auto; margin: 0;
    clip-path: none; white-space: normal;
  }
}
```

`tatib.html`: each action's visible word is wrapped in `<span class="entry__ctrl-label">` — eight
buttons across the entry, the old item and the divider — so one rule collapses all of them.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` — `.entry__jump` | `test` → `tests/e2e/test_reading.py::ReadingE2ETests::test_stage_entry_links_read_as_ink_until_hovered` | colour equals the enclosing heading's, both themes |
| FR-002 | same rule | `test` → same test | hover: underline, 3px offset, colour unchanged |
| FR-003 | same rule | `test` → same test | `:focus-visible` matches; same underline |
| FR-004 | `tokens.css`, `.media-library__uses a` rule | `test` → `tests/test_design_tokens.py::DesignTokenTests::test_light_text_pairs_meet_aa` + `tests/e2e/test_media_library.py` | the `--link`/`--canvas` pair survives and still guards a live use |
| SC-001 | as FR-001 | `test` | `#1F1F1D` light, `#F5F3EE` dark |
| SC-002 | as FR-001 | `test` | `text-decoration-line: none` on every title at rest |
| SC-003 | as FR-002 | `test` | `underline`, `3px`, colour unchanged |
| SC-004 | `static/styles/design/tokens.css` | `test` → `tests/test_design_tokens.py` | `--ink`/`--canvas` is 15.16:1 and 16.76:1 |
| SC-005 | `tests/e2e/test_media_library.py` | `test` | the media library's links keep `--link` |
| US1/AC1 | `.entry__jump` | `test` → the new test | titles at rest |
| US1/AC2 | `.entry__jump:hover` | `test` → the new test | one line, 3px under, and the title ends before the controls begin |
| US1/AC3 | `.entry__jump:focus-visible` | `test` → the new test | keyboard reaches the same cue |
| US1/AC4 | `.entry__jump` | `inspection` — move the pointer off a hovered title and look for no line | the state is the absence of `:hover` |
| US1/AC5 | `.entry__jump` | `inspection` — hover the long `…581. Sangap di Jahowa` title and check both lines carry the line | measured while building the preview: underline followed both wrapped lines |
| US2/AC1 | search rows | `inspection` — hover a search result | `.result-row:hover .result-row__title` untouched |
| US2/AC2 | media library | `test` → `tests/e2e/test_media_library.py` | `--link` still applied |
| US2/AC3 | every other anchor | `inspection` — `git diff` shows the entry rule, the controls' column and the label wrapper | no selector outside the stage's entries and their controls |
| UI/UX responsive | `components.css` container query, `tatib.html` | `test` → the new test | pane 400px at 1440 (icons, hidden labels) and 880px at 1920 (labels `static`); 390px phone keeps icons |
| US1/AC2 (narrow) | `.tatib__item--acts` | `test` → the new test | at 390 and at 1440 the title still ends before the controls |

**Verification split**: 15 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/140-stage-link-affordance/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/none.md  checklists/requirements.md  preview/README.md
```

### Source

```
static/styles/design/components.css          # the link rule, the controls' column, the label collapse
multimedia/web/templates/reading/tatib.html   # each control's word wrapped in .entry__ctrl-label
static/styles/design/tokens.css              # two comments: what --link is for now
tests/e2e/test_reading.py                    # one test rewritten in ReadingE2ETests
```

### Structure Decision

The rule belongs where spec 056 put it — beside the Tata Ibadah stage rules in `components.css`, not
in a new sheet — and the test stays in the class that already owns the reading page's theme
assertions. No new module, no new fixture, no new dependency.
