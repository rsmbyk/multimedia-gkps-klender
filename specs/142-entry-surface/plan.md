# Implementation Plan: a service entry draws no box until it is pointed at

**Spec**: `specs/142-entry-surface/spec.md`
**Branch**: `feat/142-bare-entry-surface` (`474a9555`; the branch also carries `951afa6f`, which is
slice 143's add-bar work stacked on top and out of scope here)
**Bump**: `patch`
**Preview**: live at `/tatib/142/` and `/tatib/144/`; static comparison at
`specs/142-entry-surface/preview/preview.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS (`static/styles/design/components.css`, `tokens.css`); no Python, template or JS change |
| Primary dependencies | none added — the existing design tokens (`--icon-hover-bg`, `--canvas`, `--ink`) and the existing class names |
| Storage | none |
| Testing | Django's runner for `tests/test_design_tokens.py`; Playwright (Python) E2E via `StaticLiveServerTestCase` for `tests/e2e/test_tatib_entry_controls.py` and `tests/e2e/test_tatib_hover.py` |
| Target platform | every width the Tata Ibadah stage draws at, both themes |
| Project type | server-rendered Django web app, no build step |
| Performance goals | no request, no selector weight added; two declarations removed and two custom properties deleted |
| Constraints | the aria/HC rules of spec 004's palette (contrast asserted by `test_design_tokens`); the slice must not restyle the add rows, the controls, the sidebars, the editors, the dock or the projector |
| Scale / scope | 2 stylesheets, 2 E2E test modules; 0 templates, 0 JS, 0 migrations |

## Constitution Check

No `CONSTITUTION.md` exists; SDD-01 makes it optional and never auto-created, so the check is not
applicable. The repo's own constraints — palette pairs asserted by `tests/test_design_tokens.py`,
tokens rather than literals, one surface rule shared by `.tatib__item--acts` and `.tatib__eos` —
are honoured above.

Re-checked after Phase 1: pass. The slice removes paint and two tokens; it adds no dependency, no
route, and no stored value, and it cannot move any of the palette pairs the token test asserts.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity change; the three things the stylesheet reads (the entry box, the row
  fill, the five kinds) and what each one's styling is now.
- `contracts/` — `none` (no endpoint, payload, template variable or stored value).
- `quickstart.md` — the preview server, the two E2E commands and how to see both themes.

The design in one paragraph: the surface rule
`.tatib__item--acts, .tatib__eos { min-height: 56px; padding: 8px 8px 8px 12px }` loses its
`background` and its inset `box-shadow`; the two properties it read, `--tatib-entry-fill` and
`--tatib-entry-outline`, are deleted from both theme blocks in `tokens.css`. Everything else the
box owns — the padding, the 56px floor, the 9px radius, the reserved controls column, the media
tile's 64px inset, the section break's 2px rule and diamond — is untouched, and the existing
hover / deliberate-focus / modal-origin rule keeps filling the row with `--icon-hover-bg`, which is
now the only paint an entry can carry. The two E2E tests that read the tokens are rewritten to
assert the canvas instead of the fill.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `components.css` (surface rule) | `test` → `tests/e2e/test_tatib_entry_controls.py::EntryControlsE2ETests::test_the_resting_surface_is_the_canvas_in_both_themes` | computed `rgba(0, 0, 0, 0)` and `box-shadow: none`, light and dark |
| FR-002 | `components.css` (hover / focus / modal-origin rule) | `test` → `tests/e2e/test_tatib_hover.py::TatibHoverE2ETests` (`…_hovering_the_first_entry_…`, `…_quiet_focus_…`, `…_modal_origin_…`) | the fill still differs from rest; quiet restoration stays quiet |
| FR-003 | `components.css` (surface rule) | `test` → `…EntryControlsE2ETests::test_the_resting_surface_is_the_canvas_in_both_themes` | padding `8px 12px 8px`, `min-height: 56px`, reserved column ≥ controls + 4 |
| FR-004 | `components.css` (media + section-break rules) | `test` → `…EntryControlsE2ETests::test_the_divider_takes_the_same_box`; `inspection` — the media row's 80px floor, 64px tile inset and 42px tile on `/tatib/144/` | no test asserts the media numbers |
| FR-005 | `tokens.css` | `inspection` — `git grep -- '--tatib-entry-*'` returns nothing outside `specs/`; both themes resolve the properties empty | proven by absence, so no test can catch a re-introduction |
| FR-006 | `components.css`, `tokens.css` | `inspection` — the add rows, controls' backing, flash, sidebars, editors, dock and projector rules are untouched by the diff (`git diff --stat` names two stylesheets) | the diff is the evidence |
| SC-001 | `components.css` | `test` → `…::test_the_resting_surface_is_the_canvas_in_both_themes` | both themes, per test |
| SC-002 | `components.css` | `test` → `tests/e2e/test_tatib_hover.py::…::test_hovering_the_first_entry_moves_it_once_then_settles` | asserts the hover fill differs from rest |
| SC-003 | `components.css` | `test` → `…::test_the_resting_surface_is_the_canvas_in_both_themes` | text column 976px at 1440×900 measured in `spec.md` §UI/UX; the test holds the padding and floor |
| SC-004 | `components.css` | `inspection` — `/tatib/144/` draws 15 entries of all five kinds, each transparent at rest, media 80px, breaks still ruled | owner looked at it at gate 1 |
| SC-005 | `tokens.css` | `inspection` — the grep above, plus both themes returning empty from `getComputedStyle` | |
| SC-006 | both modules | `test` → `tests/test_design_tokens.py` (6 tests) and the two E2E modules; 8 E2E failures remain, all in slice 143's add-bar geometry | see `analysis.md` — the 8 are inherited by the stacked commit, not caused here |

**Verification split**: 7 test · 5 inspection · 0 manual (the 6 requirements + 6 criteria above are
counted once each: FR-001…FR-006, SC-001…SC-006, with FR-002…FR-005 and SC-001…SC-005 sharing rows)

## Complexity Tracking

No violation to justify. The slice removes code: two declarations, two custom properties, and the
two test bodies that read them.
