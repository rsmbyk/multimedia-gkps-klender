# Convergence: The stage's entry links read as text until hovered

**Spec**: `specs/140-stage-link-affordance/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-27

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| At 1280 with both sidebars open the stage is 260px wide, so an entry's floating controls (252px, `right: 8px; top: 8px`) sit exactly over its title; the pointer cannot rest on the title there, so the underline is unreachable by mouse at that width. Keyboard focus still reaches the title and draws the line; the resting paint is ink with no line at every width. | `partial` | FR-002, US1/AC2 | Measured on `/tatib/144/`: link 978–1153px, controls 966–1218px, the three buttons 970–1214px at 1280×900; at 1440×900 the controls move to 1126–1378 and the title's left end is free. The overlay is spec 055/068's approved trade, not this slice's rule, and moving it is a placement change. |

Everything else checked by the method the plan declared:

| Requirement | Checked by | Result |
| --- | --- | --- |
| FR-001, SC-001, SC-002, US1/AC1 | `test` — `ReadingE2ETests.test_stage_entry_links_read_as_ink_until_hovered` | every `.entry__jump` computes its heading's colour, `text-decoration-line: none`; `rgb(31,31,29)` light, `rgb(245,243,238)` dark |
| FR-002, SC-003, US1/AC2, US1/AC3 | `test` — same test | hover and `:focus-visible` compute `underline`, `3px` offset, colour unchanged |
| FR-003 | `test` — same test | `:focus-visible` true after Tab reached the link |
| FR-004, SC-005, US2/AC2 | `test` — `tests.test_design_tokens` (6 tests) and `tests.e2e.test_media_library` (22 tests) | both OK; `.media-library__uses a` still `var(--link)` |
| SC-004 | `test` — `tests.test_design_tokens` | `--ink`/`--canvas` pair still asserted AA |
| US1/AC4 | `inspection` — pointer moved off the title in the test | line gone (`none`) |
| US1/AC5 | `inspection` — preview, the long `…581. Sangap di Jahowa` title | underline follows both wrapped lines (screenshot, `scratch/hover-wrapped-light.png`) |
| US2/AC1 | `inspection` — `git diff` | `.result-row:hover .result-row__title` untouched |
| US2/AC3 | `inspection` — `git diff` | one rule replaced, two token comments reworded; no other selector |

**Red proof** (TDD-02): with the spec 056 rule restored in the working tree, the new test failed at
`self.assertEqual(rest['color'], rest['heading'])` — `'rgb(28, 92, 60)' != 'rgb(31, 31, 29)'`. The
rule was then restored and the test passed.

**Outcome**: 1 gap reported. The owner's decision was to close it inside this slice and to keep the
labels wherever the window has room, collapsing them to icons on a phone (recorded in `research.md`
D006). Tasks T010–T013 were appended and implemented.

## Pass 2 — 2026-10-27

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| — | — | — | The controls now own a column sized to the pane, not the window: at 1440 (pane 400px) the labels are 1×1 and visually hidden, the buttons are 27px, the title runs 978–1153px and the controls 1281–1378px; at 1920 (pane 880px) the labels are back (252px of buttons), the title still 978–1153px and the controls 1606–1858px; at 390 the title is 20–176px and the controls 277–374px. Hover underlines the title at 1440 and 390 on the running page, and the E2E asserts all three widths. |

**Outcome**: Converged — nothing remains.

## Accepted gaps

None. The one pass-1 gap was fixed in this slice at the owner's direction, not accepted.
