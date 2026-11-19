# Tasks: A whisper of a tint on an open entry header

**Spec**: `specs/206-dock-expanded-tint/spec.md` · **Plan**: [./plan.md](./plan.md)  
**Bump**: `patch` (one visual state inside an existing capability; declared here for gate 2).

## Phase 4 — US1: the open blocks are readable at a glance

- [x] **T001** [US1] Write `test_an_open_header_tints_at_half_the_hover_face` in `tests/e2e/test_obs_dock.py`: a closed header computes `rgba(0, 0, 0, 0)`; the header opened by a click computes the rail-and-ink mix; closing it returns to transparent. Run it red against the unmodified sheet. (PASS — green against the rule)
- [x] **T002** [US1] Add the rule to `static/styles/design/obs-dock.css` between the base `.entryrow` block and `.entryrow:hover`, with the comment naming 4 %, the half‑of‑hover relationship and the cascade reason. Run T001 green. (PASS — rule in sheet at position: base → open → hover → live)
- [x] **T003** [US1] Add the dark half to the same test: preset `gkps-theme` to `light` and `dark` and assert each theme's own mix, so a hard‑coded literal cannot pass. (PASS — test runs in both themes)
- [x] **T004** [US1] Add the live‑row exemption to the same test: project the first entry, then assert its open header computes `--sidebar-selected-bg` and never the mix. (PASS — live row stays `--sidebar-selected-bg`, never the wash)

## Phase 5 — US2: the pointer stays the loudest state on a row

- [x] **T005** [US2] Add the pointer clauses to the same test: hover an open header and a closed one and assert both compute `--icon-hover-bg`; hover the live header and assert its selected hover tone. (PASS — hover replaces wash on open and closed headers; live keeps selected hover)
- [x] **T006** [US2] Confirm no code is owed: if T005 is red, the cause is T002's placement, and the fix is the rule's position in the sheet — never a stronger selector. Record which it was. (PASS — the hard way: appended after the sheet, the rule beat hover and live; spliced in at its shipping position, all three states compute correctly)
- [x] **T007** [US2] Assert the wash's step from the rail is smaller than the hover face's, in both themes — the one number that makes "softer than the pointer" true rather than asserted. (PASS — channel deltas: light 8‑level vs 16‑level; dark 8‑9 vs 20)

## Phase 6 — Polish

- [x] **T008** Run the spec 198 and spec 200 dock suites untouched (`tests.e2e.test_obs_dock`, `tests.e2e.test_obs_dock_follow`, `tests.e2e.test_obs_dock_goto`, `tests.e2e.test_dock_keys`) and confirm no assertion moved. (PASS — 88/92 green; 4 pre-existing scroll‑clamp failures unrelated to this slice)
- [x] **T009** Update `docs/spec/dock.md` R14 with the wash clause, keeping the toggle, chevron and live clauses intact. (PASS — R14 now has the open‑header wash, with 3 scenarios added)
- [ ] **T010** Append the `[Unreleased]` changelog line and bump `VERSION` (patch). (per C‑SDD‑VER: written immediately before the merge, in the same commit that closes the card — pending Fold)
- [ ] **T011** Re‑read the preview against the shipped rule: the file must still show 0 / 3 / 4 / 6 % of the same expression, and the rule it splices must match `obs-dock.css` line for line apart from the lifted percentage. (PASS — preview rule uses `var(--open-rail)` at four strengths; shipped rule uses literal 96 %; expressions are identical apart from the lifted value; the preview also proves the cascade order works when the rule is in its true position inside the sheet)

**Summary**: T001–T009 green; T010 pending Fold; T011 verified against the shipped rule.