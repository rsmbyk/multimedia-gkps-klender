# Plan: A whisper of a tint on an open entry header

**Spec**: `specs/206-dock-expanded-tint/spec.md` · **Bump**: `patch` (one visual state inside an
existing capability; declared here for gate 2).

## Technical context

- Python 3.12, Django 4.0; design CSS served by WhiteNoise and read by the OBS browser source.
- `color-mix()` is already used across `components.css` and `obs-dock.css`, including this exact
  rail-and-ink form on `.nextband:hover`; no polyfill, no build step.
- No new dependency, no migration, no endpoint, no JavaScript, no template change.
- E2E: Playwright (Python) through Django's `LiveServerTestCase`, the existing
  `tests/e2e/test_obs_dock.py`.

## Constitution check

No `CONSTITUTION.md` in the repo (SDD-01); nothing to check. Before Phase 0 and after Phase 1 the
answer is the same.

## Decisions

Recorded in [research.md](./research.md): the rail mix rather than an alpha overlay (D001), no new
token (D002), cascade by source order because all three selectors weigh the same (D003), hover
replaces the wash (D004), no transition added (D005), computed-style assertions against a probe
built from the same expression (D006).

## Change surface

| File | Change |
| --- | --- |
| `static/styles/design/obs-dock.css` | One rule — `.entryrow[aria-expanded="true"]` — inserted between the base `.entryrow` block and `.entryrow:hover` |
| `tests/e2e/test_obs_dock.py` | One test for the wash, its hover replacement and the live exemption |
| `docs/spec/dock.md` | R14's painted-state clause, at Fold |
| `CHANGELOG.md`, `VERSION` | Release bookkeeping, at Fold |

## Traceability

| Requirement | Component | Verified by |
| --- | --- | --- |
| FR-001 wash on an expanded header | `obs-dock.css` — the new rule | `test` — `tests/e2e/test_obs_dock.py::test_an_open_header_tints_at_half_the_hover_face` |
| FR-002 no wash on a closed header | the row's existing `background: none` | `test` — same test (a closed row computes `rgba(0, 0, 0, 0)`) |
| FR-003 source order over specificity | `obs-dock.css` — rule placement | `inspection` — the rule sits after the base `.entryrow` block and before `.entryrow:hover`; its selector names one class and one attribute, (0,2,0) |
| FR-004 hover replaces the wash | `.entryrow:hover`, unchanged | `test` — same test (open and closed headers compute the same face under the pointer) |
| FR-005 the live row keeps its fill | `.entryrow[aria-current="true"]`, unchanged | `test` — same test (live header at rest and hovered, never the wash) |
| FR-006 full-line coverage, chevron inside | the rule changes `background` only | `inspection` — one declaration in the rule; the chevron sits inside the row and the spec 198 test still asserts containment |
| FR-007 no new transition | the rule declares none | `inspection` — the rule has no `transition`; `.entryrow`'s own `background var(--ease)` carries the change |
| FR-008 the attribute is the only key | `aria-expanded`, set by `paintEntry` | `test` — same test (break rows and empty entries carry no attribute and stay transparent) |
| SC-001 exact mix, both themes | the rule plus tokens | `test` — same test, light and dark contexts |
| SC-002 hover on an open header | `.entryrow:hover` | `test` — same test |
| SC-003 live row, open and hovered | `.entryrow[aria-current="true"]:hover` | `test` — same test |
| SC-004 no other state changed | the rest of `obs-dock.css` | `test` — the spec 198 and spec 200 dock suites re-run untouched |
| SC-005 wash is a smaller step than hover | the two computed values | `test` — same test compares the channel deltas |
| US1 scenario 1 — opening lands the wash | `paintEntry` flips `aria-expanded` | `test` — same test after the header click |
| US1 scenario 2 — softer than hover, both themes | tokens | `test` — same test |
| US1 scenario 3 — closing removes it | `paintEntry` flips back | `test` — same test closes the header again |
| US1 scenario 4 — the live row is exempt | `.entryrow[aria-current="true"]` | `test` — same test |
| US2 scenarios 1–3 — the pointer stays louder | `.entryrow:hover`, `:hover` on the live row | `test` — same test |
| `dock/R14` delta | `docs/spec/dock.md` | `inspection` — the clause names the 4 % wash, the cascade position and the exemptions; the toggle, chevron and live clauses stand |

## Exit gate

1. **Requirement coverage** — all eight FRs and five SCs carry a component and a method.
2. **Entity coverage** — none: the data model is empty, and the slice adds no row, field or key.
3. **Interface coverage** — none: no endpoint, event, storage key or channel message changes; the
   changed interface is the CSS rule itself, named in the table.
4. **Decision provenance** — every decision in `research.md` carries a rationale, the rejected
   alternative and its source (the sheet, the tokens, or the gate-1 preview).
5. **Constitution conformance** — no constitution to violate.
6. **Zero unknowns** — `research.md` records 0.
7. **Verification declared** — fifteen `test` rows, four `inspection` rows, no `manual` row; the
   split is restated at gate 2.

`quickstart.md` runs: the command is the suite this slice edits, and the preview needs no server.
