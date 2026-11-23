# Plan: A song opened from the sidebar can edit its verses

**Spec**: `specs/230-song-verse-script-boot/spec.md`
**Branch**: `fix/230-song-verse-script-boot`
**Bump**: `patch` — 1.36.15 → 1.36.16
**Preview**: `specs/230-song-verse-script-boot/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; JavaScript (ES5-style, no build step) |
| Primary dependencies | Django 4.0, DRF, Playwright (Python) for E2E; no new dependency |
| Storage | PostgreSQL via the local compose DB; no schema change |
| Testing | Django `StaticLiveServerTestCase` + Playwright for user-visible acceptance |
| Target platform | Browsers served by the public reading shell (desktop and phone) |
| Project type | Django server-rendered templates + vanilla JS, in-page `fetch` navigation |
| Performance goals | No new request: the script is fetched once at shell boot, not on song arrival |
| Constraints | `songs_verse.js` binds on `document`; the shell swaps fragments with `importNode`, which never executes a script; script paths go through `{% static %}` |
| Scale / scope | Two template lines, one new E2E module, one capability requirement; no model/endpoint change |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| `CONSTITUTION.md` exists | pass | Not present in this repo (SDD-01); no principles to check |
| Dependency-free implementation | pass | One template include moved; no library added |
| Self-hosted assets | pass | `{% static %}` resolves the repo's own file |
| Visible change needs a preview | pass | Live preview on port 8771, with a before/after probe |
| Repo process is binding | pass | Slice, card, gates and Fold all followed |

Re-checked after Phase 1: **pass** — no violations, no Complexity Tracking entries.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entity changes; the change is two template lines`
- `contracts/` — `none` — no HTTP, model or event contract changes
- `quickstart.md` — live preview, E2E command and probe

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `tests/e2e/test_song_verse_script_boot.py` | `test` → `test_add_verse_opens_from_sidebar` | dialog `New verse` after three clicks |
| US1/AC2 | same | `test` → `test_edit_verse_opens_from_sidebar` | dialog `Edit verse 1` |
| US1/AC3 | same | `test` → `test_direct_load_still_opens_both_dialogs` | no regression on hard load |
| US1/AC4 | `reading/base.html` | `test` → `test_script_boots_at_shell_load` | 1 tag at `/`, executed before the swap |
| US1/AC5 | `reading/song.html` | `inspection` — git diff touches no markup/CSS; probe box Δ0.00px | |
| US2/AC1 | `reading/base.html` | `test` → `test_direct_load_still_opens_both_dialogs` | one live script node |
| US2/AC2 | `reading/song.html` | `test` → `test_script_boots_at_shell_load` | fragment contributes none |
| US2/AC3 | `tests/e2e/test_song_verse_script_boot.py` | `test` → `test_add_verse_opens_from_sidebar` | one editor request, one dialog |
| FR-001 | `multimedia/web/templates/reading/base.html` | `inspection` — include uses `{% static %}` beside `reorder.js` | |
| FR-002 | `multimedia/web/templates/reading/song.html` | `test` → `test_script_boots_at_shell_load` | zero script tags in the fragment |
| FR-003 | `static/web/songs_verse.js` | `test` → `test_add_verse_opens_from_sidebar` | |
| FR-004 | `static/web/songs_verse.js` | `test` → `test_edit_verse_opens_from_sidebar` | drag/delete covered by inspection of the unchanged handler |
| FR-005 | `reading/base.html` | `test` → `test_direct_load_still_opens_both_dialogs` | |
| FR-006 | whole tree | `inspection` — diff scope; button box before/after | |
| FR-007 | `docs/spec/reading.md` | `inspection` — `R55` block at Fold | |
| SC-001 | probe + E2E | `test` → `test_add_verse_opens_from_sidebar` | closed before, open after |
| SC-002 | probe + E2E | `test` → `test_edit_verse_opens_from_sidebar` | |
| SC-003 | probe + E2E | `test` → `test_script_boots_at_shell_load` | 0→1 at home, 1 after nav |
| SC-004 | probe + E2E | `test` → `test_direct_load_still_opens_both_dialogs` | |
| SC-005 | `preview/probe.py` | `inspection` — 111.765625×38 at x=900, y=681.34375 in both trees | |
| SC-006 | `preview/probe.py` + E2E | `test` → `test_add_verse_opens_from_sidebar` | page-error list empty |

**Verification split**: 16 test · 5 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/230-song-verse-script-boot/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/none.md  checklists/requirements.md  preview/{README.md,probe.py}
```

### Source

```
multimedia/web/templates/reading/base.html   +1 include, with {% static %}
multimedia/web/templates/reading/song.html   -1 include
tests/e2e/test_song_verse_script_boot.py     new (Playwright acceptance)
docs/spec/reading.md                         +R55 at Fold
```

### Structure Decision

The shell already owns the other reading scripts; the fragment keeps markup only. Tests sit in
`tests/e2e/` per the repo's TDD custom because the failure is a browser navigation behaviour
that no Django response test can observe.
