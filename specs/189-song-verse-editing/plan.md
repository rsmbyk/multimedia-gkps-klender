# Implementation Plan: song verse editing on the song page

**Spec**: `specs/189-song-verse-editing/spec.md`
**Branch**: `feat/189-song-verse-editing`
**Bump**: `minor` — new user-visible capability (four verbs on the song page) plus the number→ID storage migration; ships with a data migration; no breaking API change for consumers beyond the verse payload shape change recorded in contract.
**Preview**: `specs/189-song-verse-editing/preview/` — static preview at `preview/index.html`, built by `preview/build.py` from the product's own `shell.html`, tokens/components/generate CSS and editor dialog, with this slice's controls in `preview.css` + `preview.js`; probe `preview/probe.py` writes `preview/report.json`. Accepted at Gate 1 (2026-11-09). Ice: `preview/README.md` lists what is simulated (all four verbs local; endpoints E2E-owned).

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 + DRF; vanilla JS + jQuery (server-rendered templates) |
| Primary dependencies | PostgreSQL, WhiteNoise, `@vercel/python` deploy; editor modal pattern spec 005 (`entries.js` style) |
| Storage | `songs.Verse`, `tatib.ServiceEntry.verses` JSON list; new data migration; partial unique on live `(song, number)` |
| Testing | Django runner (`<app>/tests.py`), `tests/` for cross-cutting, `coverage`; Playwright (Python) E2E via `LiveServerTestCase` |
| Target platform | GKPS Klender worship multimedia (song page `/songs/<id>/`, entry editor, projector/display) |
| Project type | Server-rendered + static JS frontend |
| Performance goals | DRF writes are row-small; drag stays rAF + FLIP (`static/web/reorder.js` shape), no server round-trip mid-drag; collapsed list 44px makes long songs fit |
| Constraints | RE: hymn read-only (spec 005); pointer-only reorder (owner); number=position invariant; legacy setlist untouched; ghost = sidebar shape |
| Scale / scope | 281 ordinary songs, ~1,655 verses named by entries, 448 affected entries — migration must cover all without loss |

## Constitution Check

No `CONSTITUTION.md` present (archive-skip per SDD-01). Principles taken from confirmed product rules in spec: read-only hymn (005), one-editor pattern (005), number=position, reference-by-ID stability (081 rule: numbers renumber as the order is made).

| Principle | Status | Note |
| --- | --- | --- |
| Hymn read-only, enforced server + template | pass | enforced in new endpoints + `song.html` conditional |
| Shared editor dialog, single fetch path | pass | `verse` added as 4th kind |
| Numbers renumber live (spec 081 rule) | pass | renumber on cross, not release |
| No slapdash ghost/ring | pass | surface + shadow only, no 1px ring (FR-006b) |
| Frozen crossing thresholds mid-drag | pass | sidebar `placeRowAt` frozen mids, prevents stall |
| User-visible acceptance = Playwright E2E, not snapshots | pass | traceability declares test rows |

Re-checked after Phase 1: pass — no violations introduced (choices justified above in Research D001–D006).

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `Song`, `Verse`, `ServiceEntry.verses` (ID list), invariants, legacy setlist not modelled.
- `contracts/` — `README.md` + `verse.md` (4 POST writes, picker GET, derived read).
- `quickstart.md` — static preview (runnable today) + local stack; verb tests marked not-yet-runnable until Tasks.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1-3 (add) | `multimedia/web/reading/song.html`, `multimedia/web/reading/verses.py`, `multimedia/songs/models.py:Verse`, `multimedia/api/songs/serializers.py` | `test` → `multimedia/web/reading/tests.py::test_add_verse_appends_last` | modal `New verse`, empty Lyrics, focus in it |
| US2/AC1-3 (edit) | same | `test` → `multimedia/web/reading/tests.py::test_edit_verse_keeps_number` | hover tools, gutter yields, modal `Edit verse n` |
| US3/AC1 (collapse for gesture) | `multimedia/web/templates/reading/song.html`, `static/web/songs/verses.js` (new) | `inspection` — preview `B · Grab collapse` state, 44px solid rows, fill+shadow | mirrors approved B |
| US3/AC2 (expand + write, no reload) | `static/web/songs/verses.js`, `POST /editor/verse/reorder/` | `test` → `multimedia/web/reading/tests.py::test_reorder_writes_order` | numbers 1…4 |
| US3/AC3 (entry keeps lyrics, new numbers) | `multimedia/tatib/models.py:ServiceEntry.resolve` (now `pk__in`), `multimedia/web/reading/views.py` | `test` → `multimedia/tatib/tests.py::test_entry_keeps_lyric_after_reorder` | same two lyrics, `Bait` updated |
| US3/AC4 (no-op drop, no toast) | `static/web/songs/verses.js` | `inspection` — drag returning to start writes nothing |  |
| US3/AC5 (pointer-only) | `static/web/songs/verses.js`, `song.html` | `inspection` — no arrow/key handler present, rest page bare | deliberate departure from reorder.js arm |
| US3/AC6 (one slot once, no rebound) | `static/web/songs/verses.js` (+ frozen mids) | `test` → `tests/e2e/test_song_verse_drag.py` | trace reversal count 0 |
| US4/AC1-3 (delete guard) | `POST /editor/verse/<pk>/delete/`, edit modal | `test` → `multimedia/web/reading/tests.py::test_delete_refused_when_referenced` | disabled delete + count line |
| US5/AC1-4 (ID stability across verbs) | `multimedia/tatib/models.py`, `multimedia/web/reading/entries.py` | `test` → `multimedia/tatib/tests.py::test_entry_survives_four_verbs` | add/edit/reorder keep lyric, label follows number |
| FR-001 | `song.html`, `multimedia/web/reading/verses.py` | `test` → `multimedia/web/reading/tests.py::test_hymn_page_draws_no_controls` | hymn → none drawn, server 403 |
| FR-002/002a | `song.html`, `.verse-add` | `inspection` — dashed row on lyric column, 111.8×38 |  |
| FR-003 | `POST /editor/verse/new/save/` | covered by US1 test |  |
| FR-004/004a | `song.html`, `preview.css` (→ real CSS) | `inspection` — gutter tools, lyric col unmoved |  |
| FR-005 | `POST /editor/verse/<pk>/save/` | covered by US2 test |  |
| FR-006/006a-g | `static/web/songs/verses.js` | `inspection` — 44px rows, fill+shadow, `from→now`, seams rule | ghost + sidebar FLIP |
| FR-006e | `static/web/songs/verses.js` (frozen mids + live clientY) | `test` → `tests/e2e/test_song_verse_drag.py::test_slot_follows_live_cursor_not_origin` | current cursor, not original (owner 2026-11-09) |
| FR-006f | `song.html` grip hittable at rest | `inspection` — press without prior hover starts drag |  |
| FR-007/012 | `multimedia/songs/models.py`, reorder view | `test` → `multimedia/web/reading/tests.py::test_numbers_stay_1_to_n_after_each_verb` | DB check after each verb |
| FR-008/016 | `multimedia/tatib/models.py`, `entries.py` picker | `test` → `multimedia/tatib/tests.py::test_picker_id_value_current_number_label` | value=ID, label=current number |
| FR-009 | migration `multimedia/tatib/migrations/xxxx_verse_refs_to_ids.py` | `test` → `multimedia/tatib/tests.py::test_migration_maps_numbers_to_ids` | SC-007 10-entry check |
| FR-013 | `multimedia/web/reading/verses.py` | `test` → `multimedia/web/reading/tests.py::test_verse_endpoints_enforce` | ordinary-only, live, POST+CSRF, permutation, song match |
| FR-014 | `multimedia/web/reading/verses.py` unit | `test` → `multimedia/web/reading/tests.py::test_write_leaves_other_fields` | title/book/other lyrics untouched |
| FR-015 | migration + API pins | `inspection` — no setlist code touched in diff | drift allowed |
| SC-001 | Playwright walk | `test` → `tests/e2e/test_song_verse_verbs.py` | four verbs no reload |
| SC-002 | row numbers + lyric text | `test` → `tests/e2e/test_song_verse_verbs.py` |  |
| SC-003 | entry body + `Bait` line | `test` → `tests/e2e/test_song_verse_verbs.py` | fixture song |
| SC-004 | rendered page + 4 refused writes | `test` → `multimedia/web/reading/tests.py::test_hymn_refusals` |  |
| SC-005 | disabled action + count | `test` → `multimedia/web/reading/tests.py::test_delete_disabled_states_count` | fixture count |
| SC-006 | DB after each verb | `test` → `multimedia/web/reading/tests.py::test_numbers_stay_1_to_n_after_each_verb` |  |
| SC-007 | 10 entries before/after | `test` → `multimedia/tatib/tests.py::test_migration_maps_numbers_to_ids` |  |

**Verification split**: 22 test · 6 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| Pointer-only reorder departs from reorder.js key-grip grammar | Owner decision (drag-only) | Arrows would duplicate sidebar grammar against explicit owner ask; cost recorded as assumption |
| Reorder departs from reorder.js frozen-mids live-measurement for verse (freeze at grab, live cursor) | Sidebar message: stall-free, stable feel; owner wanted live-cursor judgement | Live re-measure stalls ("one short") and reads as snappy; parked slot jumps |

## Project Structure

### Documentation

```
specs/189-song-verse-editing/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/templates/reading/song.html
multimedia/web/templates/reading/_editor_modal.html (verse kind 4th)
multimedia/web/reading/verses.py        (new, 4 POST views + picker)
multimedia/web/reading/urls.py           (add verse routes)
multimedia/web/reading/entries.py        (picker value/label: ID + current #)
multimedia/web/reading/views.py          (resolve via pk__in, order by number)
multimedia/tatib/models.py               (ServiceEntry.resolve/body/label)
multimedia/tatib/migrations/xxxx_verse_refs_to_ids.py
multimedia/songs/models.py               (live-only unique)
static/web/songs/verses.js               (new ghost drag; port reorder.js shape)
static/web/reorder.js                    (read there, no change)
static/styles/design/components.css      (verse tools/ghost carried bits; most from preview.css)
multimedia/web/reading/tests.py, multimedia/tatib/tests.py, tests/e2e/test_song_verse_*.py
```

### Structure Decision

Implement inside existing `reading` app + `tatib`/`songs` models, matching their existing shapes (`entries.py` form, `views.py` stage resolution, `bookmarks` pattern for soft-delete). New drag JS lives in `static/web/songs/` mirroring `static/web/reorder.js` (ghost + frozen mids) with `.v` selectors — not reusing the sidebar module, since verses collapse and only the gospel audience carries both ordinal and identity.
