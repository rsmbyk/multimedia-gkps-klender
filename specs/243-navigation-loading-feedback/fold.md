# Fold: visible pending state for rail and sidebar fetches

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-26

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R61` | Rail/sidebar items lock immediately (rail icon dims in place; row dims and its edit/delete/add controls disable); 3px bars run at the top edge of the sections that will be refreshed; list-only fetches leave the reading page untouched; stage writes get `aria-busy` and a seeded placeholder with the real page anatomy; later clicks cancel by the stated write-vs-list rule. Five scenarios. |

Header: `last folded` moves to 2026-11-26 and `243-navigation-loading-feedback` is prepended to
`slices`.

## Drift guard

- **Files changed in this capability**: `static/web/reading.js`,
  `static/styles/design/components.css`, `tests/e2e/test_navigation_pending.py`,
  `docs/spec/reading.md`, `specs/243-navigation-loading-feedback/`. Board card, `VERSION` and
  `CHANGELOG.md` are NOT changed — delivery is not authorized.
- **Declared no behaviour change**: no — R61 describes the corrected client behaviour; the spec
  pack, capability doc and tests record the same change.

## Before / after

| | Before | After |
| --- | --- | --- |
| reading `R<n>` count | 60 | 61 |
| `slices` entries | 63 | 64 |
| spec packs under `specs/` (this branch) | 242 max | 243 added |

## Number collision

The slice planned `R61`. Before folding, every local and remote ref was searched with
`git grep '^### R61' -- docs/spec/reading.md`; no ref carried that number. No renumbering was needed.

## Late asks

The three post-gate-2 asks are folded into R61 rather than appearing only in code: the song
placeholder's real layout and case, the non-hymn songbook-name eyebrow, and the row controls sharing
the row's lock. They are recorded in `spec.md` §Clarifications and tasks T026–T028.

## Not folded

No requirements were excluded — Converge reported no accepted gaps.
