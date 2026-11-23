# Convergence: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-11-23

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| — | `missing` | FR-001…006, US1 AC1–5, US2 AC1–4, SC-001…005, both edges | No gap found; each traceability row was checked by its declared method below |

**Evidence by method**

- **test** — `bash preview/test.sh` on the throwaway `gkps224` database: 13 tests, `OK` in 7.967s.
  The eight existing `test_verses` cases, three `test_verse_add_gate` cases and two
  `test_song_empty_placement` cases all pass. The red run before the product edits failed on the
  intended assertions only: `'class="verse-add"' unexpectedly found`, `2 != 1` for the button
  count, and `47.61px` between the two empty titles at 1440×900.
- **inspection** — `git diff` on the product files holds one changed template condition
  (`song.html:45`) and one comment plus three selectors in `components.css:2523-2540`. No JS, view,
  endpoint, copy, token or animation changed; every new selector contains `:has(.entry__empty)`, so
  a song with verses cannot match. The hymn/restriction guard remains inside the same condition.
- **manual** — `preview/probe.py` on the live worktree at 8770 after `collectstatic`: empty song
  `[data-add-verse]` count 1, `.verse-add` count 0, title top y=253.9 against the Tata Ibadah
  reference y=253.5 (Δ0.4px); surviving button still 111.8×38 at x=1060.1. A song with verses keeps
  one row at x=856, y=681.3 with three verse rows above it and no invitation. At 900×700 the two
  titles read 199.0 and 198.6 (Δ0.4px); at 390×844 they read 240.4 and 234.9 (Δ5.5px, the recorded
  tolerance from the wrapped song title). Pressing the invitation's button on the live page opens
  `New verse`; Escape closes it without a write.

**Outcome**: no findings; no new tasks appended.

## Pass 2 — 2026-11-23

**Outcome**: Converged — nothing remains. The acceptance gaps recorded before gate 2 (the static
preview's limits and the 5.5px mobile residual) are accepted and outside the 1px criterion; Fold
proceeds with every requirement.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| Static preview cannot exercise the server-side `{% if %}`; the live route and probe cover it | `partial` | low | gate 1, 2026-11-23 |
| 5.5px title gap at 390×844 from the wrapped song title | `partial` | low | gate 1 (revised), 2026-11-23 |
