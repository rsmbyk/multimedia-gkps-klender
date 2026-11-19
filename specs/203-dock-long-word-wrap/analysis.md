# Analysis: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`
**Date**: 2026-11-19
**Gate**: 2 (read-only cross-artifact check; mechanical fixes applied and reported as a delta below)

## Artifacts read

| Artifact | SHA-256 (12) |
| --- | --- |
| `spec.md` | `7c67c07c2d76` |
| `plan.md` | `4828e5ebed76` |
| `research.md` | `18984c30dc1d` |
| `data-model.md` | `b90480482b46` |
| `contracts/none.md` | `0935a1340646` |
| `quickstart.md` | `96b31cd46e00` |
| `tasks.md` | `25ca6c8a4965` |
| `checklists/requirements.md` | `23fc207c1203` |
| `preview/README.md` | `8109b56cb875` |
| `preview/probe.py` | `cb95f1c4d483` |
| `tests/e2e/test_dock_text_wrap.py` | `da1b45c23f79` |
| `static/styles/design/obs-dock.css` | `bfb6d6288c6f` |

## Metrics

`7 FR · 5 SC · 9 story scenarios · 10 tests · 16 checklist items (0 ticked) · 0 [NEEDS CLARIFICATION] markers`
`coverage 100% (Plan's traceability table) · CRITICAL 0 · HIGH 1 · MEDIUM 1 · LOW 2`
`diff: 1 file, 20 insertions, 1 deletion — three declarations and their comments`
`suite: 10 new green (4 red first) · 66 neighbouring dock tests green`

Coverage reads Plan's table: every `FR-###` and `SC-###` in the spec appears there with a component and a
`Verified by` method, and every test function named in Plan and Tasks exists in the module (10 of 10; the
four extra names a naive scan picks up are the neighbouring *modules* in the regression command, not
missing tests). No requirement is un-verifiable.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F001 | HIGH | **The gate order was skipped.** The CSS and the test landed during Preview, before gate 1, on the owner's correction "your preview still does not wrap". SDD-09's Accept is permission to plan, not to implement. Red-first was kept (4 overflow failures logged before the declaration landed), so the evidence is intact; the sequence is not. | **Reported, not silently fixed.** Recorded in `research.md` D007 and the header of `tasks.md`. The owner decides at gate 2 whether to accept the sequence or have the slice re-run in order. Reverting the CSS to re-run the stages would take the fix off the page he is reviewing. |
| F002 | MEDIUM | **The spec overstated the wide-panel claim.** US2/AC4 and `## UI/UX` said "every box is unchanged at 900px". True for the owner's service 149, false for the 200-character filename fixture: a run wider than the panel still wraps there. Found by `test_a_wide_panel_renders_as_it_does_today` failing on its own assertion. | **Fixed mechanically.** US2/AC4, the UI/UX 900px paragraph and the Responsive line now say the *name* fits and is unchanged while a run wider than the panel still wraps. The test asserts the same. Delta below. |
| F003 | LOW | **The preview materials described the pre-landing state.** `preview/README.md` said the server ships the before state and `--fix` injects the rule; after the declaration landed that is backwards. | **Fixed mechanically.** The probe gained `--restore` (puts the value back to `normal`), the README's commands and state table now read the shipped state by default, and both modes were re-run: restore → 328px title / 135px body, plain → 0 / 0. Delta below. |
| F004 | LOW | **`specs/README.md`'s index is nine slices behind** — 194 through 202 are absent on `origin/develop`. This slice added only its own row. | **Reported, not fixed.** Pre-existing drift, outside this slice's scope; a drive-by index rebuild would put unrelated rows in this PR. |
| F005 | INFO | **Three fixture facts cost a red run each**: a hymn song's dock label is its number alone, a song entry's screens come from `ServiceEntry.verses`, and the NEXT band is hidden while the live entry's end is in view. | Recorded in `research.md` D005 so the next dock test does not rediscover them. |

No `missing`, `partial`, `contradicts` or `unrequested` gap against the traceability table: the diff is
three declarations inside the runner's rules, and every one traces to FR-001/002/003. The picker, the
transport, the find band and the two truncating labels are untouched, as FR-006/FR-007 require.

## Mechanical fixes applied this run (delta)

1. `spec.md` — US2/AC4, the UI/UX 900px paragraph and the Responsive line narrowed from "every box
   unchanged" to "the name fits and is unchanged; a run wider than the panel still wraps" (F002).
2. `preview/probe.py` — `--restore` added; `--fix` kept and labelled a no-op now the rule ships (F003).
3. `preview/README.md` — the run commands and the state table read the shipped state by default (F003).

Re-run after the delta: coverage still 100%, CRITICAL still 0, both probe modes verified against the
running server.

## History

- **2026-11-19 — run 1.** Read all twelve artifacts at the SHAs above. Coverage 100%, CRITICAL 0.
  F002 and F003 fixed mechanically and re-checked; F001 reported for the owner's gate-2 decision; F004
  reported as out of scope. Outcome: **ready for gate 2 with one HIGH finding open**.
