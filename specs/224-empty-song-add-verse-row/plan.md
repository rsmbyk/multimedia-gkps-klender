# Implementation Plan: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md`
**Branch**: `fix/224-empty-song-add-verse-row`
**Bump**: `patch` — 1.36.9 → 1.36.10 (re-check `VERSION` and card IDs on `origin/develop` before delivery)
**Preview**: `static preview at specs/224-empty-song-add-verse-row/preview/index.html`, with live comparison routes
**Gate 1**: accepted 2026-11-23; card `ITEM-239` moved to `Ready`, anchored on issue #590.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 / Django 4.0 template plus three CSS declarations; no JavaScript change |
| Primary dependencies | none added; Playwright already installed for the preview probe |
| Storage | none; no model or migration |
| Testing | `multimedia.web.reading.test_verse_add_gate` (three Django template cases), `tests/e2e/test_song_empty_placement.py` (two targeted Playwright geometry cases), plus the existing verb cases as regression |
| Target platform | server-rendered reading page; the probe measures at 1440×900 |
| Project type | server-rendered Django templates, vanilla JS, no build step |
| Performance goals | none; one template condition removed from the empty path |
| Constraints | the surviving button's box, copy, hover/focus rules, verse verbs and permission guards stay byte-identical; the placement rule applies only when the song is empty |
| Scale / scope | one template condition, one scoped CSS block, two small test modules, spec pack, card/board/index, capability delta |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply.
The constraint row above stands in its place.

Re-checked after Phase 1: **pass** — no new dependency, no request, no stored value, no script hook; the CSS reuses the selectors and grid shape already present for the Tata Ibadah empty state.

## Phase 0 — Research

See `research.md`. Eight decisions, each from a code read, measurement or process rule.
**Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — two existing context values, no entities; the four template states.
- `contracts/none.md` — no interface changes.
- `quickstart.md` — DB-isolated test command, live routes and static preview.

### The design

Two scoped edits.

**US1 — one control.** In `multimedia/web/templates/reading/song.html`, line 45, change:

```
{% if can_edit_verses %}
```

to:

```
{% if can_edit_verses and verse_rows %}
```

The `.verse-add` block stays where it is, after the verse loop; the `.entry__empty` block beneath it
is untouched, including its identical `.verse-add__btn` markup. No JavaScript, view, endpoint, copy
or permission rule changes. With verses, the rendered bytes are identical to today.

**US2 — the placement.** In `static/styles/design/components.css`, add three scoped rules beside
the Tata Ibadah block at `:2503-2522`, reusing its grid shape:

```css
.read[data-kind="song"]:has(.entry__empty) { display: flex; flex-direction: column; min-height: 100%; }
.read[data-kind="song"]:has(.entry__empty) .read__head { margin-bottom: 0; }
.read[data-kind="song"] .read__body:has(> .entry__empty) {
  display: grid; grid-template-rows: minmax(min-content, 50%); align-content: start;
  align-items: center; justify-items: center; flex: 1; margin-top: 0;
  padding-top: 0; padding-bottom: 0; container-type: inline-size;
}
```

`padding-top: 0` instead of the Tata Ibadah block's 12px is the measured offset: the song's header is
3.2px taller and its invitation 14px shorter, so a 12px floor would leave the title at y=262.9;
zero puts it at y=253.9 against the reference y=253.5. No token, animation or global rule changes.

**Deliberately not done.** No CSS `display: none`, no client-side hiding, no change to the empty
invitation's copy, button box or the with-verses page, no reordering of the two template blocks, no
new endpoint.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 row gated on live verses | `templates/reading/song.html:45` | `test` → `test_verse_add_gate.py::test_empty_song_has_no_after_verse_row` | |
| FR-002 exactly one control on empty | same template, unchanged invitation | `test` → `::test_empty_song_has_one_add_verse_button` | `[data-add-verse]` count 1 |
| FR-003 with-verses row unchanged | same template | `test` → `::test_song_with_verses_keeps_its_single_add_row` | box x=856, y=681.3, 520×38 |
| FR-004 copy, box, verbs, guards unchanged | the diff; untouched CSS/JS/views | `inspection` — only one template condition changes; existing `test_verses` verb cases re-run | |
| FR-005 capability text states the gate | `docs/spec/reading.md` R40 | `inspection` — Fold delta reruns the sentence and adds the scenario | |
| US1 AC1 empty song one button | as FR-001/FR-002 | `test` → the two empty cases | |
| US1 AC2 first save from invitation | unchanged endpoint and modal JS | `test` → existing `VerseVerbTests::test_add_verse_appends_last` | |
| US1 AC3 with-verses row unchanged | as FR-003 | `test` → `::test_song_with_verses_keeps_its_single_add_row` | |
| US1 AC4 hymn / restricted pages clear | `can_edit_verses` in the same gate | `inspection` — the existing guard remains in the condition | guard unchanged |
| US1 AC5 soft-deleted-only reads empty | `verse_rows` filter | `test` → `::test_empty_song_has_no_after_verse_row` | fixture deletes its only verse |
| Edge: identical button markup | `.verse-add__btn` in both blocks | `inspection` — only the wrapper condition changes | |
| Edge: collapsed 14px margin raises invitation | `.verse-add` CSS | `manual` — `probe.py` after the change; invitation y 205.9 → 153.9 | no CSS edit |
| SC-001 empty page has 1 button, 0 rows | rendered HTML | `test` → the two empty cases | |
| SC-002 with-verses box unchanged | rendered HTML | `test` → `::test_song_with_verses_keeps_its_single_add_row` | |
| SC-003 surviving button box unchanged | rendered HTML | `manual` — `probe.py` readings before/after | 111.8×38 at x=1060.1 |
| SC-004 first save still works | verse verbs | `test` → existing `test_add_verse_appends_last`; `manual` — click through the live empty state | |
| FR-006 quarter-band placement | `components.css` three scoped rules | `test` → `test_song_empty_placement.py::test_empty_song_title_matches_the_tata_ibadah_title` | |
| US2 AC1 desktop title parity | as FR-006 | `test` → `::test_empty_song_title_matches_the_tata_ibadah_title` | 1440×900, Δ≤1px |
| US2 AC2 tablet title parity | as FR-006 | `test` → `::test_empty_song_title_matches_the_tata_ibadah_title_at_900x700` | Δ≤1px |
| US2 AC3 with-verses page unchanged | untouched selectors | `inspection` — the new selectors all contain `:has(.entry__empty)` | |
| US2 AC4 mobile tolerance | same mechanism, taller song header | `manual` — measure both routes at 390×844 and record Δ≈5.5px in `converge.md` | not a criterion |
| Edge: taller header residual | song header 83.9 vs tatib 80.7 | `manual` — as US2 AC4 | |
| SC-005 shared title position | as FR-006 | `test` → the two placement cases | 253.9 vs 253.5; 199.0 vs 198.6 |

**Verification split: 14 test · 5 inspection · 5 manual** across 23 rows (rows naming two methods
are counted in both).

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-006, US1 AC1–AC5, US2 AC1–AC4, both edges and SC-001…SC-005 each carry a row |
| Entity coverage | `data-model.md` covers both context values and all four template states; nothing stored |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D008 in `research.md`, each with code, measurement or process evidence |
| Constitution conformance | no constitution exists; the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 14 `test` · 5 `inspection` · 5 `manual`; every `test` row names a module and case |
| `quickstart.md` runnable | yes — `preview/test.sh` and `preview/serve.sh` run against this worktree |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/224-empty-song-add-verse-row/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  fold.md
  contracts/none.md  checklists/requirements.md
  preview/{index.html,README.md,build.py,probe.py,serve.sh,test.sh,measurements.json}
```

### Source

```
multimedia/web/templates/reading/song.html   line 45 condition gains `and verse_rows`
static/styles/design/components.css        three song-empty placement rules beside the tatib block
multimedia/web/reading/test_verse_add_gate.py  new, three targeted cases
tests/e2e/test_song_empty_placement.py      new, two targeted geometry cases
docs/spec/reading.md                         R40 modified at Fold
backlog/items/ITEM-239-empty-song-add-verse-row.md
backlog/board.md                             Ready → In review → Done in the slice PR
specs/README.md                              index row Draft → Accepted
VERSION, CHANGELOG.md                        patch bump and one line at delivery
```

### Structure Decision

No new product module: the behaviour is one server-rendered condition plus one scoped CSS block.
The template cases get their own module because `test_verses.py` owns verb endpoints, and the
geometry cases get a small E2E module because layout cannot be measured in a Django test client.
