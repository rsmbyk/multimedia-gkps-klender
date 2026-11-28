# Convergence: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-11-28

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| Dirty detection compared values after ModelForm had copied them onto the instance, so no-op saves looked changed | `partial` | FR-002 | `versions.form_changed` now compares against the locked stored row |
| The reference-count helper called `verse_set` on a Verse target, so the verse editor fragment 500'd | `missing` | FR-011 | `versions.referencing_service_ids` handles Verse, Song and Book |
| The new version columns leaked into legacy API payload fields | `unrequested` | FR-015 | `multimedia/api/tatib/serializers.py` excludes `version` |
| Historical bookmark-conversion tests wrote current-model rows into a schema without `version` | `contradicts` | FR-014 | `multimedia/tatib/tests.py` uses historical apps for tatib rows and the re-run |
| Page-rendering tests lacked a static manifest in the worktree | `partial` | FR-012 | `collectstatic` run; E2E then passed |

**Outcome**: 5 gaps fixed in the implementation; no requirement changed.

## Pass 2 — 2026-11-28

**Outcome**: Converged — nothing remains.

## Verification evidence

- 9 focused endpoint tests: `OK`.
- 13 Playwright tests in `tests/e2e/test_verse_reference_notice.py`: `OK` (including the new 560px confirmation case).
- 438 app tests: 7 failures, all reproduced on unmodified develop — scripture fragment placeholder (ITEM-261), shortcuts sheet, legacy tatib list, image projection and three slot endpoints (ITEM-217).
- Preview probe remains aligned with the shipped CSS: confirmation 560×157, note 265×18 on one line.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| Seven unit-lane failures identical on develop | `contradicts` | known red | 2026-11-28 — recorded on the board as ITEM-217 and ITEM-261 |

## Cap reached

<!-- not reached -->
